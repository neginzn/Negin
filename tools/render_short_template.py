import subprocess, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import imageio_ffmpeg

W, H, FPS = 1080, 1920, 30
D = "/tmp/claude-0/-home-user-Negin/d5288e51-5e9b-5613-adee-5159b473691a/scratchpad/"
ANTON = D + "Anton.ttf"
RED = (220, 30, 30)
WHITE = (245, 245, 245)

def load(name, box=None):
    im = Image.open(D + name).convert("RGB")
    if box:
        im = im.crop(box)
    return im

img64 = load("Edmund_Kemper_1964_Mugshot.jpg", (0, 0, 640, 1009))
img73f = load("Edmund_Kemper_mug_shot_-_1973.jpg", (0, 0, 405, 520))
img73p = load("Edmund_Kemper_mug_shot_-_1973.jpg", (412, 0, 794, 520))
imgpr = load("Edmund_Kemper_1973.jpg")
img19 = load("Edmund_Kemper_2019_mugshot.jpg")

# (start, end, image or None, [(text, color, size)], small label)
SEGS = [
    (0.0, 3.5, img64, [("AT 15", WHITE, 150), ("HE KILLED HIS", WHITE, 110), ("GRANDPARENTS", RED, 120)], "1964"),
    (3.5, 7.5, img73f, [("BY 1973:", WHITE, 110), ("6 YOUNG WOMEN", RED, 110), ("HIS MOTHER", RED, 110), ("HER FRIEND", RED, 110)], "1973"),
    (7.5, 10.0, imgpr, [("LISTEN TO HOW", WHITE, 115), ("HE TALKS", WHITE, 115), ("ABOUT IT", RED, 130)], None),
    (10.0, 25.0, None, [("INTERVIEW CLIP", (150, 150, 150), 110), ("PLACE HERE", (150, 150, 150), 90), ("(10-15 SEC)", (110, 110, 110), 70)], None),
    (25.0, 31.0, img73p, [("HE CALLED", WHITE, 130), ("THE POLICE", WHITE, 130), ("HIMSELF", RED, 150)], "APRIL 1973"),
    (31.0, 36.0, img19, [("STILL IN PRISON", WHITE, 120), ("TODAY", RED, 150)], "2019"),
    (36.0, 40.0, img73f, [("WHAT SCARES", WHITE, 125), ("YOU MORE?", RED, 150)], None),
]
TOTAL = SEGS[-1][1]

def font(sz):
    return ImageFont.truetype(ANTON, sz)

def bg_for(im):
    b = im.copy()
    r = max(W / b.width, H / b.height)
    b = b.resize((int(b.width * r) + 2, int(b.height * r) + 2))
    b = b.crop(((b.width - W) // 2, (b.height - H) // 2, (b.width - W) // 2 + W, (b.height - H) // 2 + H))
    b = b.filter(ImageFilter.GaussianBlur(35))
    return ImageEnhance.Brightness(b).enhance(0.35)

def draw_text(canvas, lines, label):
    d = ImageDraw.Draw(canvas)
    y = 170
    for text, color, sz in lines:
        f = font(sz)
        tw = d.textlength(text, font=f)
        d.text(((W - tw) / 2, y), text, font=f, fill=color, stroke_width=6, stroke_fill=(0, 0, 0))
        y += int(sz * 1.12)
    if label:
        f = font(58)
        tw = d.textlength(label, font=f)
        pad = 18
        x0 = (W - tw) / 2 - pad
        d.rectangle([x0, 1690, x0 + tw + 2 * pad, 1690 + 80], fill=(0, 0, 0))
        d.text(((W - tw) / 2, 1698), label, font=f, fill=WHITE)

grain = [Image.effect_noise((W // 4, H // 4), 40).resize((W, H)).convert("RGB") for _ in range(6)]

bgs = {id(s[2]): bg_for(s[2]) for s in SEGS if s[2] is not None}
dark = Image.new("RGB", (W, H), (12, 12, 12))

ff = imageio_ffmpeg.get_ffmpeg_exe()
out = D + "kemper_short_visuals.mp4"
p = subprocess.Popen([ff, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", out],
                     stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

n = int(TOTAL * FPS)
for i in range(n):
    t = i / FPS
    seg = next(s for s in SEGS if s[0] <= t < s[1])
    s0, s1, im, lines, label = seg
    prog = (t - s0) / (s1 - s0)
    if im is None:
        canvas = dark.copy()
        d = ImageDraw.Draw(canvas)
        d.rectangle([90, 700, W - 90, 1400], outline=(90, 90, 90), width=6)
        lines2 = lines
        draw_text(canvas, [], None)
        y = 830
        for text, color, sz in lines2:
            f = font(sz)
            tw = d.textlength(text, font=f)
            d.text(((W - tw) / 2, y), text, font=f, fill=color)
            y += int(sz * 1.25)
    else:
        canvas = bgs[id(im)].copy()
        zoom = 1.0 + 0.08 * prog
        fw = int(940 * zoom)
        fh = int(im.height * fw / im.width)
        maxh = int(740 * zoom)
        if fh > maxh:
            fh = maxh
            fw = int(im.width * fh / im.height)
        fg = im.resize((fw, fh), Image.LANCZOS)
        fg = ImageEnhance.Contrast(fg).enhance(1.15)
        cx, cy = W // 2, 1200
        canvas.paste(fg, (cx - fw // 2, cy - fh // 2))
        draw_text(canvas, lines, label)
    canvas = Image.blend(canvas, grain[i % 6], 0.06)
    # fade in/out at segment boundaries
    fade = 6
    fi = int((t - s0) * FPS)
    fo = int((s1 - t) * FPS)
    k = min(1.0, fi / fade, fo / fade) if (fi < fade or fo < fade) else 1.0
    if k < 1.0:
        canvas = ImageEnhance.Brightness(canvas).enhance(max(0.0, k))
    p.stdin.write(canvas.tobytes())

p.stdin.close()
p.wait()
print("done", out)
