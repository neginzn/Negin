#!/usr/bin/env python3
"""
ساخت مونتاژ عکس هماهنگ با صدا، با حرکت نرم زوم (کن برنز).

نمونه:
    python3 tools/montage.py --images ./photos --audio vo.m4a --out final.mp4

ورودی عکس: JPG / PNG / HEIC (آیفون) — چرخش EXIF خودکار اصلاح می‌شود.
خروجی: MP4 آمادهٔ یوتیوب، صدا میکس‌شده روی ‎-14 LUFS.
"""
import argparse, json, math, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

IMG_EXT = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp", ".bmp", ".tif", ".tiff"}


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def natural_key(p: Path):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)]


def probe_duration(path: Path) -> float:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "json", str(path)]).stdout
    return float(json.loads(out)["format"]["duration"])


def prepare_images(src_dir: Path, work: Path, W: int, H: int):
    """HEIC→JPG، اصلاح چرخش، و جاگذاری روی بوم با پس‌زمینهٔ بلور."""
    from PIL import Image, ImageOps, ImageFilter
    import pillow_heif
    pillow_heif.register_heif_opener()

    files = sorted([p for p in src_dir.iterdir()
                    if p.is_file() and p.suffix.lower() in IMG_EXT], key=natural_key)
    if not files:
        sys.exit(f"هیچ عکسی در {src_dir} پیدا نشد.")

    # بوم را دو برابر رزولوشن نهایی می‌سازیم تا زوم کیفیت را خراب نکند
    CW, CH = W * 2, H * 2
    out_dir = work / "prepared"
    out_dir.mkdir(parents=True, exist_ok=True)
    prepared = []

    for i, f in enumerate(files, 1):
        im = Image.open(f)
        im = ImageOps.exif_transpose(im).convert("RGB")

        fitted = ImageOps.contain(im, (CW, CH), Image.LANCZOS)
        if fitted.size == (CW, CH):
            canvas = fitted
        else:
            # پس‌زمینهٔ بلور به‌جای نوار سیاه (عکس عمودی گوشی)
            bg = ImageOps.fit(im, (CW, CH), Image.LANCZOS)
            bg = bg.filter(ImageFilter.GaussianBlur(radius=CW // 40))
            bg = Image.eval(bg, lambda v: int(v * 0.55))
            canvas = bg
            canvas.paste(fitted, ((CW - fitted.width) // 2, (CH - fitted.height) // 2))

        dst = out_dir / f"img_{i:03d}.jpg"
        canvas.save(dst, "JPEG", quality=95)
        prepared.append((dst, f.name))
    return prepared


def read_shots(path: Path, count: int):
    """فایل زمان‌بندی: هر خط «شماره یا نام عکس | مدت به ثانیه»"""
    durations = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [x.strip() for x in line.split("|")]
        durations.append(float(parts[-1]))
    if len(durations) != count:
        sys.exit(f"فایل زمان‌بندی {len(durations)} ردیف دارد ولی {count} عکس هست.")
    return durations


def kenburns_filter(idx: int, frames: int, W: int, H: int, fps: int, zoom: float):
    """حرکت نرم؛ جهت زوم و پن یک‌درمیان عوض می‌شود تا یکنواخت نباشد."""
    zoom_in = (idx % 2 == 0)
    if zoom_in:
        z = f"1+{zoom:.4f}*on/{max(frames - 1, 1)}"
    else:
        z = f"{1 + zoom:.4f}-{zoom:.4f}*on/{max(frames - 1, 1)}"

    # پن ملایم افقی، جهتش هر بار عوض می‌شود
    drift = (idx % 4) - 1.5  # -1.5 .. 1.5
    x = f"iw/2-(iw/zoom/2)+{drift * 40:.1f}*on/{max(frames - 1, 1)}"
    y = f"ih/2-(ih/zoom/2)"
    return (f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={fps}")


def build_shot(img: Path, dst: Path, dur: float, idx: int, W: int, H: int,
               fps: int, zoom: float, grade: bool):
    frames = max(int(round(dur * fps)), 2)
    vf = [f"scale={W*2}:{H*2}:flags=lanczos",
          kenburns_filter(idx, frames, W, H, fps, zoom)]
    if grade:
        # لوک ملایم مستند: کمی کم‌اشباع، سایهٔ سرد، های‌لایت گرم، وینیت ظریف
        vf += ["eq=saturation=0.88:contrast=1.06",
               "colorbalance=rs=-0.03:bs=0.05:rh=0.03:bh=-0.02",
               "vignette=PI/5"]
    vf.append("format=yuv420p")
    run(["ffmpeg", "-y", "-loop", "1", "-i", str(img), "-t", f"{dur:.3f}",
         "-vf", ",".join(vf), "-r", str(fps),
         "-c:v", "libx264", "-preset", "medium", "-crf", "16", str(dst)])


def concat_with_xfade(clips, durs, out: Path, fps: int, xfade: float):
    if len(clips) == 1:
        shutil.copy(clips[0], out)
        return durs[0]
    inputs, parts = [], []
    for c in clips:
        inputs += ["-i", str(c)]
    prev, offset = "0:v", durs[0] - xfade
    for i in range(1, len(clips)):
        label = f"v{i}"
        parts.append(f"[{prev}][{i}:v]xfade=transition=fade:duration={xfade}:"
                     f"offset={offset:.3f}[{label}]")
        prev = label
        if i < len(clips) - 1:
            offset += durs[i] - xfade
    total = sum(durs) - xfade * (len(clips) - 1)
    run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(parts),
         "-map", f"[{prev}]", "-r", str(fps),
         "-c:v", "libx264", "-preset", "medium", "-crf", "16", str(out)])
    return total


def clean_and_normalize(src: Path, dst: Path, work: Path, denoise: bool):
    """تمیزکردن صدا + لادنس دومرحله‌ای روی ‎-14 LUFS / ‎-1 dBTP"""
    chain = ["highpass=f=80"]
    if denoise:
        chain += ["afftdn=nf=-25"]
    chain += ["acompressor=threshold=-18dB:ratio=3:attack=10:release=200"]
    base = ",".join(chain)

    meas = subprocess.run(
        ["ffmpeg", "-i", str(src), "-af", base + ",loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
         "-f", "null", "-"], capture_output=True, text=True)
    stats = None
    m = re.findall(r"\{[^{}]*input_i[^{}]*\}", meas.stderr, re.S)
    if m:
        try:
            stats = json.loads(m[-1])
        except json.JSONDecodeError:
            stats = None

    if stats:
        ln = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={stats['input_i']}:"
              f"measured_TP={stats['input_tp']}:measured_LRA={stats['input_lra']}:"
              f"measured_thresh={stats['input_thresh']}:offset={stats['target_offset']}:"
              f"linear=true:print_format=summary")
    else:
        ln = "loudnorm=I=-14:TP=-1:LRA=11"

    run(["ffmpeg", "-y", "-i", str(src), "-af", f"{base},{ln},alimiter=limit=0.891",
         "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(dst)])


def main():
    ap = argparse.ArgumentParser(description="مونتاژ عکس هماهنگ با صدا")
    ap.add_argument("--images", required=True, type=Path)
    ap.add_argument("--audio", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--music", type=Path, help="موسیقی پس‌زمینه (با داکینگ خودکار)")
    ap.add_argument("--shots", type=Path, help="فایل زمان‌بندی دستی")
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--xfade", type=float, default=0.7, help="مدت دیزالو بین عکس‌ها")
    ap.add_argument("--zoom", type=float, default=0.12, help="شدت زوم (۰.۱۲ = ۱۲٪)")
    ap.add_argument("--grade", action="store_true", help="اعمال لوک مستند")
    ap.add_argument("--no-denoise", action="store_true")
    ap.add_argument("--keep-temp", action="store_true")
    args = ap.parse_args()

    W, H = (int(x) for x in args.size.lower().split("x"))
    work = Path(tempfile.mkdtemp(prefix="montage_"))
    print(f"پوشهٔ کار: {work}")

    audio_dur = probe_duration(args.audio)
    print(f"مدت صدا: {audio_dur:.2f} ثانیه")

    prepared = prepare_images(args.images, work, W, H)
    n = len(prepared)
    print(f"{n} عکس آماده شد")

    if args.shots:
        durs = read_shots(args.shots, n)
    else:
        # تقسیم مساوی، با احتساب همپوشانی دیزالوها تا طول دقیقاً اندازهٔ صدا شود
        total_needed = audio_dur + args.xfade * (n - 1)
        durs = [total_needed / n] * n
        if min(durs) < 2.0:
            print(f"⚠️  هر عکس فقط {min(durs):.1f} ثانیه می‌ماند — عکس کمتر یا صدای بلندتر بهتر است.")

    clips = []
    for i, ((img, orig), d) in enumerate(zip(prepared, durs)):
        dst = work / f"shot_{i:03d}.mp4"
        print(f"  [{i+1}/{n}] {orig} → {d:.2f}s")
        build_shot(img, dst, d, i, W, H, args.fps, args.zoom, args.grade)
        clips.append(dst)

    silent = work / "video.mp4"
    total = concat_with_xfade(clips, durs, silent, args.fps, args.xfade)
    print(f"طول تصویر: {total:.2f}s | طول صدا: {audio_dur:.2f}s")

    clean = work / "audio.wav"
    clean_and_normalize(args.audio, clean, work, denoise=not args.no_denoise)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.music:
        music_args = ["-i", str(args.music)]
        fc = ("[2:a]volume=0.18,aloop=loop=-1:size=2e9[bg];"
              "[bg][1:a]sidechaincompress=threshold=0.03:ratio=8:attack=15:release=400[duck];"
              "[1:a][duck]amix=inputs=2:duration=first:dropout_transition=0,"
              "loudnorm=I=-14:TP=-1:LRA=11[a]")
        run(["ffmpeg", "-y", "-i", str(silent), "-i", str(clean), *music_args,
             "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
             "-c:v", "libx264", "-preset", "slow", "-crf", "18",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
             "-movflags", "+faststart", "-shortest", str(args.out)])
    else:
        run(["ffmpeg", "-y", "-i", str(silent), "-i", str(clean),
             "-map", "0:v", "-map", "1:a",
             "-c:v", "libx264", "-preset", "slow", "-crf", "18",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
             "-movflags", "+faststart", "-shortest", str(args.out)])

    print(f"\n✅ خروجی: {args.out}  ({args.out.stat().st_size/1e6:.1f} MB)")
    if not args.keep_temp:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
