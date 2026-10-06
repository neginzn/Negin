"""Cut-out (puppet) animation renderer — no AI service needed.

Takes a character image (PNG, ideally with a transparent background) and renders a
vertical 1080x1920 MP4 clip with simple, kid-friendly motion. Because it uses the
original artwork, the character always looks exactly the same.

Usage:
  python3 tools/animate.py --char characters/img/bunny.png --motion bounce \
      --seconds 6 --bg "#BDE7FF" --out footage/bunny_bounce.mp4

Motions: idle, bounce, jump, sway, wiggle, slide_in, zoom_in, spin_hop, walk
Optional: --bg-image path, --scale 0.6, --x 0.5 --y 0.72 (anchor of feet, 0..1)
"""
import argparse
import math
import subprocess

from PIL import Image

W, H, FPS = 1080, 1920, 30


def ease_out_back(t):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def motion_at(name, t, T):
    """Returns (dx, dy, angle_deg, sx, sy) — offsets in px, rotation, and scale."""
    p = t / T
    if name == "idle":  # gentle breathing
        s = 1 + 0.02 * math.sin(2 * math.pi * t / 2.0)
        return 0, 0, 0, 1 / s ** 0.5, s
    if name == "bounce":
        ph = (t * 2.0) % 1.0
        h = abs(math.sin(math.pi * ph))
        squash = 1 - 0.12 * max(0, 1 - h * 6)  # squash near the ground
        return 0, -160 * h, 0, 2 - squash, squash
    if name == "jump":
        ph = (t / 1.5) % 1.0
        if ph < 0.15:  # crouch
            k = math.sin(math.pi * ph / 0.15)
            return 0, 0, 0, 1 + 0.12 * k, 1 - 0.15 * k
        h = math.sin(math.pi * (ph - 0.15) / 0.85)
        return 0, -420 * h, 0, 0.95, 1.06
    if name == "sway":
        return 0, 0, 6 * math.sin(2 * math.pi * t / 1.6), 1, 1
    if name == "wiggle":  # excited
        return 12 * math.sin(2 * math.pi * t * 4), 0, 4 * math.sin(2 * math.pi * t * 4), 1, 1
    if name == "slide_in":
        k = ease_out_back(min(1, t / 1.2))
        return (1 - k) * -W, 0, 0, 1, 1
    if name == "zoom_in":  # pop in, then idle
        k = ease_out_back(min(1, t / 0.8)) if t < 0.8 else 1
        s = max(0.01, k) * (1 + 0.02 * math.sin(2 * math.pi * t / 2.0))
        return 0, 0, 0, s, s
    if name == "spin_hop":
        ph = (t / 2.0) % 1.0
        h = math.sin(math.pi * ph)
        return 0, -300 * h, 360 * ph, 1, 1
    if name == "walk":  # waddle across the screen
        x = -W * 0.6 + (W * 1.2) * p
        step = abs(math.sin(2 * math.pi * t * 1.5))
        return x, -30 * step, 5 * math.sin(2 * math.pi * t * 1.5), 1, 1
    raise SystemExit(f"unknown motion: {name}")


def make_bg(args):
    if args.bg_image:
        bg = Image.open(args.bg_image).convert("RGB")
        r = max(W / bg.width, H / bg.height)
        bg = bg.resize((round(bg.width * r), round(bg.height * r)), Image.LANCZOS)
        left, top = (bg.width - W) // 2, (bg.height - H) // 2
        return bg.crop((left, top, left + W, top + H))
    return Image.new("RGB", (W, H), args.bg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--char", required=True)
    ap.add_argument("--motion", default="bounce")
    ap.add_argument("--seconds", type=float, default=6)
    ap.add_argument("--bg", default="#BDE7FF")
    ap.add_argument("--bg-image")
    ap.add_argument("--scale", type=float, default=0.6, help="character width / frame width")
    ap.add_argument("--x", type=float, default=0.5)
    ap.add_argument("--y", type=float, default=0.75, help="where the feet sit (0 top .. 1 bottom)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    char = Image.open(args.char).convert("RGBA")
    base_w = round(W * args.scale)
    char = char.resize((base_w, round(char.height * base_w / char.width)), Image.LANCZOS)
    bg = make_bg(args)

    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
         "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", args.out],
        stdin=subprocess.PIPE)
    n = round(args.seconds * FPS)
    for i in range(n):
        t = i / FPS
        dx, dy, ang, sx, sy = motion_at(args.motion, t, args.seconds)
        cw, ch = max(1, round(char.width * sx)), max(1, round(char.height * sy))
        c = char.resize((cw, ch), Image.BILINEAR)
        if ang:
            c = c.rotate(-ang, resample=Image.BICUBIC, expand=True)
        frame = bg.copy()
        fx = round(W * args.x + dx - c.width / 2)
        fy = round(H * args.y + dy - c.height + (c.height - ch) / 2)  # feet anchored
        frame.paste(c, (fx, fy), c)
        ff.stdin.write(frame.tobytes())
    ff.stdin.close()
    ff.wait()
    print(f"wrote {args.out} ({args.seconds}s, {args.motion})")


if __name__ == "__main__":
    main()
