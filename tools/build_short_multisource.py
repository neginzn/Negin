import subprocess, json
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
def dur(f):
    o = subprocess.run([FF, "-i", f], capture_output=True, text=True).stderr
    h, m, s = o.split("Duration: ")[1].split(",")[0].split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)
# crops per source: (w,h,x,y)
CROP = {"src.mp4": "720:720:0:60", "n1.mp4": "1000:430:140:90", "n2.mp4": "1080:540:100:80"}
# segments: (audio, [(file, start, max_dur), ...])  audio = wav file, or ("src", a, b) for reel audio (visual = reel)
SEG = [
    (("src", 11.0, 14.8), None),
    ("v1.wav", [("n1.mp4", 64.3, 3.4, "760:430:260:85"), ("n1.mp4", 59.2, 3.4, "700:470:260:40"), ("n2.mp4", 44.05, 0.9, "700:500:0:80"), ("n2.mp4", 37.1, 1.8, "760:500:290:80")]),
    ("v2.wav", [("n2.mp4", 41.1, 1.8, "720:500:280:80"), ("n2.mp4", 39.05, 1.9, "640:500:200:80"), ("n2.mp4", 42.95, 0.95, "760:490:520:90"), ("n2.mp4", 44.05, 0.9, "700:500:0:80"), ("n2.mp4", 41.1, 1.8, "720:500:280:80"), ("n2.mp4", 45.1, 2.0, "720:500:250:80"), ("n2.mp4", 92.0, 1.3, "660:500:500:80"), ("n2.mp4", 34.4, 2.4, "720:500:380:80")]),
    ("v3.wav", [("n2.mp4", 34.4, 2.4, "720:500:380:80"), ("n2.mp4", 37.1, 1.8, "760:500:290:80"), ("n1.mp4", 59.2, 3.4, "700:470:260:40")]),
    ("v4.wav", [("n2.mp4", 95.0, 2.2, "960:500:160:80"), ("n2.mp4", 92.0, 1.3, "660:500:500:80"), ("n1.mp4", 63.05, 2.0, "640:490:520:20")]),
    (("src", 19.0, 41.5), None),
    ("v5.wav", [("n2.mp4", 92.0, 1.3, "660:500:500:80"), ("n1.mp4", 63.05, 2.0, "640:490:520:20")]),
    (("src", 56.1, 58.35), None),
    (("src", 61.45, 74.85), None),
    ("v6.wav", [("n2.mp4", 110.0, 5.4, "1000:500:140:80")]),
    (("src", 0.0, 4.85), None),
]
def vf(f, d, c=None):
    return (f"crop={c or CROP[f]},eq=saturation=0.75:contrast=1.05,split[a][b];"
            "[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.3[bg];"
            f"[a]scale=w='1080*(1+0.05*t/{d:.3f})':h=-2:eval=frame,crop=1080:ih[fg];"
            "[bg][fg]overlay=0:(H-h)/2-80,format=yuv420p,fps=30")
def shot(f, st, d, out, c=None):
    subprocess.run([FF, "-loglevel", "error", "-y", "-ss", str(st), "-t", f"{d:.3f}", "-i", f, "-filter_complex", "[0:v]" + vf(f, d, c) + "[v]",
                    "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "19", out], check=True)
parts = []
for i, (a, shots) in enumerate(SEG):
    out = f"seg{i:02d}.mp4"
    if isinstance(a, tuple):
        _, s, e = a; d = e - s
        subprocess.run([FF, "-loglevel", "error", "-y", "-ss", str(s), "-t", f"{d:.3f}", "-i", "src.mp4",
            "-filter_complex", "[0:v]" + vf("src.mp4", d) + "[v];[0:a]afade=t=in:d=0.06,afade=t=out:st=%.3f:d=0.12,aformat=sample_rates=48000:channel_layouts=stereo,volume=1.5[aa]" % (d - 0.12),
            "-map", "[v]", "-map", "[aa]", "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-c:a", "aac", "-b:a", "192k", out], check=True)
        parts.append((out, d, "src"))
        continue
    d = dur(a) + 0.4
    left, k, vids = d, 0, []
    while left > 0.05:
        f, st, md, c = shots[k % len(shots)]
        sd = min(md, left)
        if left - sd < 0.5: sd = left
        vo = f"s{i:02d}_{k}.mp4"; shot(f, st, sd, vo, c); vids.append(vo); left -= sd; k += 1
    open("sl.txt", "w").write("".join(f"file '{v}'\n" for v in vids))
    subprocess.run([FF, "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", "sl.txt", "-i", a,
        "-filter_complex", "[1:a]apad,atrim=0:%.3f,aformat=sample_rates=48000:channel_layouts=stereo[aa]" % d,
        "-map", "0:v", "-map", "[aa]", "-t", f"{d:.3f}", "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-c:a", "aac", "-b:a", "192k", out], check=True)
    parts.append((out, d, "vo"))
open("list.txt", "w").write("".join(f"file '{p}'\n" for p, _, _ in parts))
subprocess.run([FF, "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", "joined.mp4"], check=True)
json.dump(parts, open("parts.json", "w"))
print("total", sum(d for _, d, _ in parts))
