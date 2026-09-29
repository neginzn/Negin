import subprocess, json
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
def dur(f):
    o = subprocess.run([FF, "-i", f], capture_output=True, text=True).stderr
    h, m, s = o.split("Duration: ")[1].split(",")[0].split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)
# crops per source: (w,h,x,y)
CROP = {"doc.mp4": "1080:1080:420:0"}
B = "1440:1080:240:0"
SEG = [
    (("src", 4786.7, 4796.6), None),
    ("v1.wav", [("doc.mp4", 86.2, 3.4, B), ("doc.mp4", 69.0, 3.0, B), ("doc.mp4", 77.0, 2.0, B), ("doc.mp4", 72.0, 2.5, B)]),
    ("v2.wav", [("doc.mp4", 73.0, 2.0, B), ("doc.mp4", 78.0, 2.0, B), ("doc.mp4", 3173.0, 3.5, B), ("doc.mp4", 3176.5, 3.0, B), ("doc.mp4", 3179.5, 3.0, B)]),
    ("v3.wav", [("doc.mp4", 779.0, 3.0, B), ("doc.mp4", 1088.2, 2.5, B), ("doc.mp4", 796.0, 2.0, B), ("doc.mp4", 4341.0, 2.5, B)]),
    (("src", 4467.2, 4480.3), None),
    (("src", 4851.1, 4859.2), None),
    (("src", 4920.5, 4924.6), None),
    ("v5.wav", [("doc.mp4", 5040.0, 3.0, B), ("doc.mp4", 5046.0, 3.0, B), ("doc.mp4", 5115.0, 3.5, B), ("doc.mp4", 5121.0, 3.0, B)]),
    (("src", 5175.6, 5178.2), None),
    (("src", 5179.4, 5185.3), None),
    (("src", 5188.9, 5194.7), None),
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
        subprocess.run([FF, "-loglevel", "error", "-y", "-ss", str(s), "-t", f"{d:.3f}", "-i", "doc.mp4",
            "-filter_complex", "[0:v]" + vf("doc.mp4", d) + "[v];[0:a]afade=t=in:d=0.06,afade=t=out:st=%.3f:d=0.12,aformat=sample_rates=48000:channel_layouts=stereo,loudnorm=I=-16:TP=-2,aresample=48000[aa]" % (d - 0.12),
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
