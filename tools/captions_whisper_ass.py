from faster_whisper import WhisperModel
import subprocess, imageio_ffmpeg, re
FF = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([FF, "-loglevel", "error", "-y", "-i", "joined.mp4", "-vn", "-ac", "1", "-ar", "16000", "j.wav"], check=True)
m = WhisperModel('base.en', device='cpu', compute_type='int8')
segs, _ = m.transcribe('j.wav', word_timestamps=True)
words = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
chunks, cur = [], []
for w in words:
    if cur and (len(cur) >= 3 or w[1] - cur[-1][2] > 0.4 or cur[-1][0].endswith(('.', '?', '!', ','))):
        chunks.append(cur); cur = []
    cur.append(w)
if cur: chunks.append(cur)
def ts(t):
    return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
FIX = {"SCULMAN": "SCOLMAN", "SCALMAN": "SCOLMAN", "WHY IS THE": "IT'S THE", "SENSE THAT,": "SENTENCE,", "SKOLMAN": "SCOLMAN", "NEIGHBORS": "NABORS", "NABERS": "NABORS", " -YEAR -OLD": "-YEAR-OLD",
       "WISCONSIN -A PRISON": "WISCONSIN STATE PRISON", "IT'S THE SENSE": "IT'S THE SENTENCE"}
ass = """[Script Info]
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Anton,92,&H00F0F0F0,&H00F0F0F0,&H00000000,&H64000000,0,0,0,0,100,100,1,0,1,4,2,2,60,60,440,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
out = []
for i, c in enumerate(chunks):
    st = c[0][1]; en = c[-1][2] + 0.15
    if i + 1 < len(chunks): en = min(en, chunks[i + 1][0][1])
    txt = " ".join(w[0] for w in c).upper()
    for a, b in FIX.items(): txt = txt.replace(a, b)
    if txt.strip(" ,.") in ("ONE", "SO", "UM") or "***" in txt or txt.strip(" ,.") in ("YOU", "SIR", "IT'S JUST A", "COME ON ASS", "YOU LAUGH"): continue
    out.append(txt)
    ass += f"Dialogue: 0,{ts(st)},{ts(en)},Cap,,0,0,0,,{{\\fad(80,80)}}{txt}\n"
open('caps.ass', 'w').write(ass)
print(" | ".join(out))
