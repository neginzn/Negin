from faster_whisper import WhisperModel
import json, re
m = WhisperModel('small.en', device='cpu', compute_type='int8')
TR = {'src.mp4': json.load(open('tr.json')), 'n4.mp4': json.load(open('n4.json')), 'n6.mp4': json.load(open('n6.json'))}
build = open('build.py').read()
exec(build[build.index('R = '):build.index(']\ndef vf') + 1])
parts = json.load(open('parts.json'))
words, off, bounds = [], 0.0, []
for (a, _), (p, d, k) in zip(SEG, parts):
    if isinstance(a, tuple):
        _, f, s, e, _c = a
        for seg in TR[f]:
            for ws, we, w in seg['w']:
                if ws >= s - 0.05 and ws < e - 0.05:
                    words.append((w.strip(), off + ws - s, off + min(we, e) - s))
    else:
        segs, _ = m.transcribe(a, word_timestamps=True, initial_prompt="Sade Robinson, Maxwell Anderson, Milwaukee.")
        words += [(w.word.strip(), off + w.start, off + w.end) for sg in segs for w in sg.words]
    off += d
    bounds.append(off)
W = []
i = 0
while i < len(words):
    w = words[i]; lw = w[0].lower()
    if lw == 'abuse' and i + 1 < len(words) and words[i+1][0].lower().startswith('you'):
        W += [('be', w[1], w[2]), ('excused.', words[i+1][1], words[i+1][2])]; i += 2; continue
    if lw == 'cold,' and i + 1 < len(words) and words[i+1][0].lower() == 'blooded':
        W.append(('cold-blooded', w[1], words[i+1][2])); i += 2; continue
    if w[0].startswith('-') and W:
        p = W.pop(); W.append((p[0] + w[0], p[1], w[2])); i += 1; continue
    W.append((w[0].replace('Prince', 'prints').replace('ilene', 'Aileen').replace('warnose', 'Wuornos').replace('rock', 'Rock'), w[1], w[2])); i += 1
words = W
chunks, cur = [], []
for w in words:
    if cur and (any(cur[-1][1] < b <= w[1] + 0.05 for b in bounds) or len(cur) >= 3 or w[1] - cur[-1][2] > 0.4 or cur[-1][0].endswith(('.', '?', '!', ','))):
        chunks.append(cur); cur = []
    cur.append(w)
if cur: chunks.append(cur)
def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
FIX = {"CHEAP": "CHEAT", "ABUSE YOU": "BE EXCUSED", "ANNA": "ANA", "MA 'AM": "MA'AM", " -YEAR -OLD": "-YEAR-OLD", "COLD -BLOODED": "COLD-BLOODED", "COLD, BLOODED": "COLD-BLOODED",
       "IS NOT GOING TO GO CHEAT": "WOULDN'T CHEAT", "LIKE, MAKE ME SICK": "LIKE... MAKE ME SICK"}
ass = open('../sk/caps.ass').read().split('[Events]')[0] + "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
out = []
for i, c in enumerate(chunks):
    st = c[0][1]; en = c[-1][2] + 0.15
    if i + 1 < len(chunks): en = min(en, chunks[i + 1][0][1])
    txt = " ".join(w[0] for w in c).upper()
    for a, b in FIX.items(): txt = txt.replace(a, b)
    out.append(txt)
    ass += f"Dialogue: 0,{ts(st)},{ts(en)},Cap,,0,0,0,,{{\\fad(80,80)}}{txt}\n"
open('caps.ass', 'w').write(ass)
print(" | ".join(out))
