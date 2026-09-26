import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import imageio_ffmpeg

W, H, FPS = 1080, 1920, 30
D = "/tmp/claude-0/-home-user-Negin/d5288e51-5e9b-5613-adee-5159b473691a/scratchpad/"
P = D + "ph/"
ANTON = D + "Anton.ttf"
RED, WHITE = (225, 30, 30), (245, 245, 245)

def load(n, box=None):
    im = Image.open(P + n).convert("RGB")
    return im.crop(box) if box else im

hib = load("Hearst-hibernia-yell.jpg")
mug = load("PattyHearstmug.jpg", (640, 0, 1280, 853))
mar = load("Patty_Hearst_escorted_by_marshals.jpg")
col = load("Patti_Hearst1.jpg")

# (start, end, img, focus_x, focus_y, zoom_from, zoom_to, lines, label)
SEGS = [
    (0.0, 6.0, hib, 0.72, 0.30, 1.30, 2.10, [("THIS HEIRESS", WHITE, 130), ("ROBBED A BANK", RED, 130)], "APRIL 15, 1974"),
    (6.0, 11.8, mug, 0.50, 0.40, 1.05, 1.20, [("PATTY HEARST", WHITE, 140), ("KIDNAPPED 2 MONTHS", RED, 105), ("EARLIER", RED, 105)], None),
    (11.8, 15.9, mar, 0.55, 0.45, 1.10, 1.25, [("BRAINWASHED?", WHITE, 140), ("THE JURY SAID NO", RED, 115)], "1976 TRIAL"),
    (15.9, 19.0, col, 0.50, 0.40, 1.00, 1.12, [("PARDONED", RED, 160)], "2001"),
    (19.0, 22.6, hib, 0.72, 0.28, 2.10, 2.40, [("VICTIM", WHITE, 170), ("OR CRIMINAL?", RED, 150)], None),
]
TOTAL = SEGS[-1][1]

def font(s):
    return ImageFont.truetype(ANTON, s)

def cover(im, fx, fy, z):
    # crop a 9:16 window of the image centered on focus, scaled by zoom z
    iw, ih = im.size
    base_h = min(ih, iw * H / W)
    ch = base_h / z
    cw = ch * W / H
    cx = min(max(fx * iw, cw / 2), iw - cw / 2)
    cy = min(max(fy * ih, ch / 2), ih - ch / 2)
    return im.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.BICUBIC)

def overlay(c, lines, label, bottom=False):
    # dark gradient top for text legibility
    grad = Image.new("L", (W, H))
    g = ImageDraw.Draw(grad)
    for y in range(0, 900):
        v = int(190 * (1 - y / 900))
        g.line([(0, (H - 1 - y) if bottom else y), (W, (H - 1 - y) if bottom else y)], fill=v)
    c = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), c, grad)
    d = ImageDraw.Draw(c)
    y = 1230 if bottom else 200
    for t, colr, s in lines:
        f = font(s)
        tw = d.textlength(t, font=f)
        d.text(((W - tw) / 2, y), t, font=f, fill=colr, stroke_width=7, stroke_fill=(0, 0, 0))
        y += int(s * 1.1)
    if label:
        f = font(60)
        tw = d.textlength(label, font=f)
        x0 = (W - tw) / 2 - 20
        ly = 1110 if bottom else 1560
        d.rectangle([x0, ly, x0 + tw + 40, ly + 90], fill=RED)
        d.text(((W - tw) / 2, ly + 8), label, font=f, fill=WHITE)
    # REC corner
    d.ellipse([60, 80, 90, 110], fill=RED)
    d.text((105, 66), "REC", font=font(48), fill=WHITE, stroke_width=4, stroke_fill=(0, 0, 0))
    return c

grain = [Image.effect_noise((W // 4, H // 4), 45).resize((W, H)).convert("RGB") for _ in range(6)]
ff = imageio_ffmpeg.get_ffmpeg_exe()
out = D + "hearst_visuals.mp4"
p = subprocess.Popen([ff, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "fast", out],
                     stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
for i in range(int(TOTAL * FPS)):
    t = i / FPS
    s0, s1, im, fx, fy, z0, z1, lines, label = next(s for s in SEGS if s[0] <= t < s[1])
    k = (t - s0) / (s1 - s0)
    z = z0 + (z1 - z0) * k
    # quick punch-in on each cut
    since = t - s0
    if since < 0.15 and s0 > 0:
        z *= 1.06 - 0.4 * since
    frame = cover(im, fx, fy, z)
    frame = ImageEnhance.Contrast(frame.convert("L").convert("RGB")).enhance(1.25) if im is not col else ImageEnhance.Contrast(frame).enhance(1.1)
    frame = overlay(frame, lines, label, bottom=(im is hib))
    frame = Image.blend(frame, grain[i % 6], 0.07)
    p.stdin.write(frame.tobytes())
p.stdin.close()
p.wait()
print("done")
