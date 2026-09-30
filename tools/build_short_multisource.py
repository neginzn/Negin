import subprocess, json
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
def dur(f):
    o = subprocess.run([FF, "-i", f], capture_output=True, text=True).stderr
    h, m, s = o.split("Duration: ")[1].split(",")[0].split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)
R = "720:720:0:60"          # reel (crop out burned captions + logo)
SEG = [
    (("src", "src.mp4", 12.6, 20.5, R), None),
    ("v1.wav", [("n1.mp4", 72.2, 3.3, "960:540:160:10"), ("n1.mp4", 59.2, 3.3, "720:540:300:10"), ("n5.mp4", 126.0, 3.0, "900:520:190:30")]),
    ("v2.wav", [("n5.mp4", 134.0, 2.5, "900:520:190:30"), ("n5.mp4", 76.2, 3.2, "900:520:190:20"), ("n6.mp4", 356.0, 4.0, "640:540:620:40"), ("n5.mp4", 122.2, 2.5, "900:520:190:30")]),
    ("v3.wav", [("n1.mp4", 82.3, 3.0, "900:520:190:30"), ("n5.mp4", 128.0, 2.5, "900:520:190:30"), ("n6.mp4", 81.0, 3.0, "720:540:280:20")]),
    ("v4.wav", [("n6.mp4", 84.0, 3.0, "720:540:280:20")]),
    (("src", "n6.mp4", 6.7, 14.0, "720:540:280:20"), None),
    ("v5.wav", [("n6.mp4", 93.5, 3.5, "900:520:190:20")]),
    (("src", "n4.mp4", 32.2, 40.1, "720:540:240:20"), None),
    ("v6.wav", [("n1.mp4", 50.2, 3.5, "900:520:190:20")]),
    (("src", "src.mp4", 131.5, 138.95, R), None),
    (("src", "src.mp4", 145.9, 148.25, R), None),
    (("src", "src.mp4", 166.6, 170.7, R), None),
    (("src", "n4.mp4", 236.6, 239.75, "720:540:240:20"), None),
]
def vf(c, d):
    return (f"crop={c},eq=saturation=0.75:contrast=1.05,split[a][b];"
            "[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.3[bg];"
            f"[a]scale=w='1080*(1+0.05*t/{d:.3f})':h=-2:eval=frame,crop=1080:ih[fg];"
            "[bg][fg]overlay=0:(H-h)/2-80,format=yuv420p,fps=30")
def shot(f, st, d, out, c):
    subprocess.run([FF, "-loglevel", "error", "-y", "-ss", str(st), "-t", f"{d:.3f}", "-i", f, "-filter_complex", "[0:v]" + vf(c, d) + "[v]",
                    "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "19", out], check=True)
parts = []
for i, (a, shots) in enumerate(SEG):
    out = f"seg{i:02d}.mp4"
    if isinstance(a, tuple):
        _, f, s, e, c = a; d = e - s
        subprocess.run([FF, "-loglevel", "error", "-y", "-ss", str(s), "-t", f"{d:.3f}", "-i", f,
            "-filter_complex", "[0:v]" + vf(c, d) + "[v];[0:a]afade=t=in:d=0.06,afade=t=out:st=%.3f:d=0.12,aformat=sample_rates=48000:channel_layouts=stereo,loudnorm=I=-16:TP=-2,aresample=48000[aa]" % (d - 0.12),
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
