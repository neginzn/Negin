import subprocess, json
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
def dur(f):
    o = subprocess.run([FF, "-i", f], capture_output=True, text=True).stderr
    h, m, s = o.split("Duration: ")[1].split(",")[0].split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)
# (kind, video_src_start, audio: 'vo:file' or 'src', duration or None)
SEG = [
    ("vo", 2.0, "v1.wav"),
    ("vo", 23.5, "v2.wav"),
    ("src", 42.2, 49.4),
    ("vo", 99.6, "v3.wav"),
    ("src", 107.2, 122.9),
    ("vo", 136.6, "v4.wav"),
    ("src", 162.8, 168.6),
    ("vo", 172.6, "v5.wav"),
]
VF = ("crop=720:600:0:280,eq=saturation=0.75:contrast=1.05,split[a][b];"
      "[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.3[bg];"
      "[a]scale=w='1080*(1+0.05*t/{d})':h=-2:eval=frame,crop=1080:900[fg];"
      "[bg][fg]overlay=0:430,format=yuv420p")
parts = []
for i, (k, vs, a) in enumerate(SEG):
    out = f"seg{i}.mp4"
    if k == "vo":
        d = dur(a) + 0.45
        cmd = [FF, "-loglevel", "error", "-y", "-ss", str(vs), "-t", f"{d:.3f}", "-i", "src.mp4", "-i", a,
               "-filter_complex", "[0:v]" + VF.format(d=d) + "[v];[1:a]apad,atrim=0:%.3f,aformat=sample_rates=48000:channel_layouts=stereo[aa]" % d,
               "-map", "[v]", "-map", "[aa]"]
    else:
        d = a - vs
        cmd = [FF, "-loglevel", "error", "-y", "-ss", str(vs), "-t", f"{d:.3f}", "-i", "src.mp4",
               "-filter_complex", "[0:v]" + VF.format(d=d) + "[v];[0:a]afade=t=in:d=0.08,afade=t=out:st=%.3f:d=0.15,aformat=sample_rates=48000:channel_layouts=stereo,volume=1.4[aa]" % (d - 0.15),
               "-map", "[v]", "-map", "[aa]"]
    cmd += ["-r", "30", "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-c:a", "aac", "-b:a", "192k", out]
    subprocess.run(cmd, check=True)
    parts.append((out, d, k))
open("list.txt", "w").write("".join(f"file '{p}'\n" for p, _, _ in parts))
subprocess.run([FF, "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", "joined.mp4"], check=True)
json.dump([[p, d, k] for p, d, k in parts], open("parts.json", "w"))
print("total", sum(d for _, d, _ in parts))
