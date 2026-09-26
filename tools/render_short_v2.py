"""Stranger Files short renderer v2: transitions, shake, flicker, light leaks,
animated title, word-by-word captions, CCTV overlay. Outputs silent video."""
import json, math, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

W, H, FPS = 1080, 1920, 30
D = "/tmp/claude-0/-home-user-Negin/d5288e51-5e9b-5613-adee-5159b473691a/scratchpad/"
P = D + "ph/"
ANTON = D + "Anton.ttf"
RED, WHITE = (225, 30, 30), (245, 245, 245)
random.seed(7)

def load(n, box=None):
    im = Image.open(P + n).convert("RGB")
    return im.crop(box) if box else im

hib = load("Hearst-hibernia-yell.jpg")
mug = load("PattyHearstmug.jpg", (640, 0, 1280, 853))
mugp = load("PattyHearstmug.jpg", (0, 0, 640, 853))
mar = load("Patty_Hearst_escorted_by_marshals.jpg")
col = load("Patti_Hearst1.jpg")

# shots: (start, end, img, fx, fy, z0, z1, pan_dx, title_lines, label, cctv, color)
SHOTS = [
    (0.00, 1.60, hib, 0.50, 0.50, 1.00, 1.08, 0.00, [("1974", WHITE, 150)], None, True, False),
    (1.60, 3.90, hib, 0.72, 0.15, 1.50, 1.80, 0.00, [("THIS HEIRESS", WHITE, 120), ("ROBBED A BANK", RED, 120)], "APRIL 15, 1974", True, False),
    (3.90, 6.00, hib, 0.735, 0.15, 2.00, 2.30, 0.00, [("WITH A RIFLE", RED, 140)], None, True, False),
    (6.00, 8.60, mug, 0.50, 0.42, 1.05, 1.18, 0.00, [("PATTY HEARST", WHITE, 140)], "AGE 19", False, False),
    (8.60, 11.80, mugp, 0.45, 0.45, 1.20, 1.05, 0.00, [("KIDNAPPED", RED, 150), ("2 MONTHS EARLIER", WHITE, 95)], "FEB 4, 1974", False, False),
    (11.80, 14.20, mar, 0.58, 0.45, 1.25, 1.40, -0.03, [("BRAINWASHED?", WHITE, 140)], None, False, False),
    (14.20, 15.90, mar, 0.55, 0.40, 1.60, 1.75, 0.02, [("THE JURY", WHITE, 120), ("SAID NO", RED, 150)], "1976 TRIAL", False, False),
    (15.90, 19.00, col, 0.50, 0.40, 1.00, 1.14, 0.00, [("PARDONED", RED, 170)], "2001", False, True),
    (19.00, 22.60, hib, 0.73, 0.15, 1.90, 2.30, 0.00, [("VICTIM", WHITE, 170), ("OR CRIMINAL?", RED, 150)], None, True, False),
]
TOTAL = SHOTS[-1][1]
# transition type at each cut (index of incoming shot)
TRANS = {1: "zoom", 2: "punch", 3: "flash", 4: "whip", 5: "glitch", 6: "punch", 7: "flash", 8: "glitch"}
TD = 0.20  # half-duration of transitions

words = json.load(open(P + "words.json"))
# merge hyphenated pieces
merged = []
for w, s, e in words:
    if w.startswith("-") and merged:
        merged[-1][0] += w
        merged[-1][2] = e
    else:
        merged.append([w, s, e])
words = [[w.upper().strip(".,?"), s, e] for w, s, e in merged]
# group into caption chunks of up to 3 words, break on long gaps
chunks, cur = [], []
for w in words:
    if cur and (len(cur) == 3 or w[1] - cur[-1][2] > 0.35):
        chunks.append(cur); cur = []
    cur.append(w)
chunks.append(cur)

fcache = {}
def font(s):
    if s not in fcache:
        fcache[s] = ImageFont.truetype(ANTON, s)
    return fcache[s]

def cover(im, fx, fy, z, dx=0.0, sx=0.0, sy=0.0):
    iw, ih = im.size
    base_h = min(ih, iw * H / W)
    ch = base_h / z
    cw = ch * W / H
    cx = fx * iw + dx * iw + sx
    cy = fy * ih + sy
    cx = min(max(cx, cw / 2), iw - cw / 2)
    cy = min(max(cy, ch / 2), ih - ch / 2)
    return im.crop((cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)).resize((W, H), Image.BICUBIC)

def ease_out_back(x):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

# vignette mask
yy, xx = np.mgrid[0:H, 0:W]
r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
VIG = np.clip(1.15 - 0.55 * r ** 2, 0.35, 1.0)[..., None].astype(np.float32)
# light leak (red/orange radial) precomputed
leak = np.zeros((H, W, 3), np.float32)
lr = np.sqrt(((xx - W * 0.9) / (W * 0.8)) ** 2 + ((yy - H * 0.15) / (H * 0.5)) ** 2)
lv = np.clip(1 - lr, 0, 1) ** 2
leak[..., 0] = lv * 255
leak[..., 1] = lv * 70
leak[..., 2] = lv * 20
grains = [np.random.normal(0, 14, (H // 2, W // 2)).astype(np.float32) for _ in range(8)]
grains = [np.kron(g, np.ones((2, 2), np.float32))[..., None] for g in grains]

def shot_frame(i, t):
    s0, s1, im, fx, fy, z0, z1, dx, _, _, _, color = SHOTS[i]
    k = min(max((t - s0) / (s1 - s0), 0), 1)
    ke = 0.5 - 0.5 * math.cos(math.pi * k)
    z = z0 + (z1 - z0) * ke
    # handheld shake
    sx = 6 * math.sin(t * 2.1 + i) + 3 * math.sin(t * 5.3)
    sy = 5 * math.cos(t * 1.7 + i) + 3 * math.sin(t * 4.1)
    fr = cover(im, fx, fy, z, dx * ke, sx, sy)
    if not color:
        fr = fr.convert("L").convert("RGB")
    return fr, z

def zoomed(img, s):
    if abs(s - 1) < 1e-3:
        return img
    w2, h2 = int(W * s), int(H * s)
    big = img.resize((w2, h2), Image.BILINEAR)
    return big.crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))

def radial_blur(img, strength):
    acc = np.zeros((H, W, 3), np.float32)
    n = 5
    for j in range(n):
        acc += np.asarray(zoomed(img, 1 + strength * j / n), np.float32)
    return Image.fromarray((acc / n).astype(np.uint8))

def whip_blur(img, shift):
    a = np.asarray(img, np.float32)
    acc = np.zeros_like(a)
    n = 6
    for j in range(n):
        acc += np.roll(a, int(shift * j / n), axis=1)
    return Image.fromarray((acc / n).astype(np.uint8))

def glitch(img, amt):
    a = np.asarray(img).copy()
    o = int(30 * amt)
    a[..., 0] = np.roll(a[..., 0], o, axis=1)
    a[..., 2] = np.roll(a[..., 2], -o, axis=1)
    for _ in range(int(10 * amt)):
        y = random.randint(0, H - 60); h = random.randint(8, 60)
        a[y:y + h] = np.roll(a[y:y + h], random.randint(-80, 80), axis=1)
    return Image.fromarray(a)

def draw_title(c, i, t):
    s0 = SHOTS[i][0]
    lines, label, cctv = SHOTS[i][8], SHOTS[i][9], SHOTS[i][10]
    d = ImageDraw.Draw(c)
    age = t - s0
    y = 1000 if cctv else 230
    for n, (txt, colr, sz) in enumerate(lines):
        la = age - 0.07 * n
        if la <= 0:
            y += int(sz * 1.08); continue
        sc = ease_out_back(min(la / 0.28, 1.0))
        fs = max(8, int(sz * sc))
        f = font(fs)
        tw = d.textlength(txt, font=f)
        d.text(((W - tw) / 2, y + (sz - fs) / 2), txt, font=f, fill=colr, stroke_width=max(2, int(8 * sc)), stroke_fill=(0, 0, 0))
        y += int(sz * 1.08)
    if label and age > 0.25:
        f = font(58)
        tw = d.textlength(label, font=f)
        # slide-in from left
        p = min((age - 0.25) / 0.25, 1)
        x0 = -tw - 80 + (W / 2 - tw / 2 + tw + 80) * (1 - (1 - p) ** 3)
        d.rectangle([x0 - 20, y + 20, x0 + tw + 20, y + 110], fill=RED)
        d.text((x0, y + 28), label, font=f, fill=WHITE)
    if cctv:
        blink = int(t * 2) % 2 == 0
        if blink:
            d.ellipse([60, 90, 94, 124], fill=RED)
        d.text((110, 78), "REC", font=font(52), fill=WHITE, stroke_width=3, stroke_fill=(0, 0, 0))
        secs = 13 + int(t)
        d.text((W - 430, 78), f"APR 15 1974  10:40:{secs:02d}", font=font(40), fill=WHITE, stroke_width=3, stroke_fill=(0, 0, 0))

def draw_caption(c, t):
    ch = next((ch for ch in chunks if ch[0][1] - 0.05 <= t <= ch[-1][2] + 0.25), None)
    if not ch:
        return
    d = ImageDraw.Draw(c)
    f = font(92)
    parts = [w[0] for w in ch]
    widths = [d.textlength(p + " ", font=f) for p in parts]
    total = sum(widths)
    x = (W - total) / 2
    y = 1500
    age = t - ch[0][1]
    pop = ease_out_back(min(max(age / 0.18, 0), 1))
    for (w, s, e), wd in zip(ch, widths):
        active = s <= t <= e + 0.05
        colr = (255, 214, 0) if active else WHITE
        yy2 = y - (10 if active else 0) + (1 - pop) * 40
        d.text((x, yy2), w, font=f, fill=colr, stroke_width=8, stroke_fill=(0, 0, 0))
        x += wd

def render():
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    out = D + "hearst_v2b_visuals.mp4"
    p = subprocess.Popen([ff, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", "-preset", "fast", out],
                         stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n = int(TOTAL * FPS)
    for fi in range(n):
        t = fi / FPS
        i = next(k for k, s in enumerate(SHOTS) if s[0] <= t < s[1])
        fr, _ = shot_frame(i, t)
        # transitions around cut points
        for j, tt in TRANS.items():
            cut = SHOTS[j][0]
            dt = t - cut
            if -TD <= dt < TD:
                x = (dt + TD) / (2 * TD)  # 0..1
                if tt == "zoom":
                    fr = radial_blur(fr, 0.25 * (1 - abs(2 * x - 1)))
                elif tt == "punch":
                    fr = zoomed(fr, 1 + 0.12 * max(0, 1 - abs(dt) / TD))
                elif tt == "whip":
                    fr = whip_blur(fr, 260 * (1 - abs(2 * x - 1)))
                elif tt == "glitch":
                    fr = glitch(fr, 1 - abs(2 * x - 1))
                elif tt == "flash":
                    a = max(0, 1 - abs(dt) / TD)
                    fr = Image.blend(fr, Image.new("RGB", (W, H), (255, 255, 255)), a * 0.85)
        a = np.asarray(fr, np.float32)
        # flicker + contrast
        a = (a - 128) * 1.18 + 128 + random.uniform(-6, 6)
        # red light leak pulse on transitions and slow drift
        lk = 0.10 + 0.08 * math.sin(t * 0.9)
        for j in TRANS:
            if abs(t - SHOTS[j][0]) < 0.35:
                lk += 0.25 * (1 - abs(t - SHOTS[j][0]) / 0.35)
        a = a + leak * lk
        a = a * VIG + grains[fi % 8]
        # letterbox-ish top gradient for title legibility
        a[:900] *= np.linspace(0.45, 1.0, 900, dtype=np.float32)[:, None, None]
        a[1350:] *= np.linspace(1.0, 0.55, H - 1350, dtype=np.float32)[:, None, None]
        c = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        draw_title(c, i, t)
        draw_caption(c, t)
        p.stdin.write(c.tobytes())
    p.stdin.close(); p.wait()
    print("done", out)

if __name__ == "__main__":
    render()
