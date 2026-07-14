#!/usr/bin/env python3
"""Generate a vertical (9:16) product ad video from Shopify product images.

Takes a JSON config describing the scenes (image + caption) and an end card,
and renders an MP4 with Ken Burns motion, crossfades, and text overlays
using ffmpeg. Designed for Instagram Reels / TikTok / Facebook ads.

Usage:
    python3 scripts/make_ad.py config.json

Config format (see ads/ for examples):
{
  "output": "ad.mp4",
  "width": 1080, "height": 1920, "fps": 30,
  "scene_duration": 3.2,
  "crossfade": 0.5,
  "scenes": [
    {"image": "img/hero.png", "headline": ["Shedding", "everywhere?"]},
    ...
  ],
  "endcard": {
    "duration": 3.6,
    "bg": "0xFFF3E4",
    "title": ["3-in-1 Steam", "Grooming Brush"],
    "price": "From €17.99",
    "cta": "Shop Now",
    "brand": "PawsyCozy"
  }
}
"""
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def esc(text: str) -> str:
    """Escape text for use inside an ffmpeg drawtext filter."""
    return (
        text.replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "’")  # typographic apostrophe avoids quoting pain
        .replace(",", "\\,")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace(";", "\\;")
    )


def drawtext(text, *, font=FONT_BOLD, size=64, color="white", x="(w-text_w)/2",
             y="h-600", box=True, boxcolor="black@0.45", boxborder=28,
             fade_in=0.0, line_spacing=14):
    parts = [
        f"fontfile={font}",
        f"text='{esc(text)}'",
        f"fontsize={size}",
        f"fontcolor={color}",
        f"x={x}",
        f"y={y}",
        f"line_spacing={line_spacing}",
    ]
    if box:
        parts.append(f"box=1:boxcolor={boxcolor}:boxborderw={boxborder}")
    if fade_in > 0:
        parts.append(f"alpha='min(1,t/{fade_in})'")
    return "drawtext=" + ":".join(parts)


def resolve_image(ref: str, base: Path) -> str:
    """Return a local path for an image reference; download http(s) URLs."""
    if not ref.startswith(("http://", "https://")):
        return str((base / ref).resolve())
    cache = base / ".image_cache"
    cache.mkdir(exist_ok=True)
    ext = Path(ref.split("?")[0]).suffix or ".jpg"
    dest = cache / (hashlib.sha256(ref.encode()).hexdigest()[:16] + ext)
    if not dest.exists():
        print("Downloading", ref)
        with urllib.request.urlopen(ref) as r:
            dest.write_bytes(r.read())
    return str(dest.resolve())


def build(config_path: str) -> None:
    cfg = json.loads(Path(config_path).read_text())
    base = Path(config_path).parent
    w, h = cfg.get("width", 1080), cfg.get("height", 1920)
    fps = cfg.get("fps", 30)
    dur = cfg.get("scene_duration", 3.2)
    xf = cfg.get("crossfade", 0.5)
    scenes = cfg["scenes"]
    end = cfg.get("endcard")
    end_dur = end.get("duration", 3.6) if end else 0

    inputs = []
    filters = []
    for i, sc in enumerate(scenes):
        img = resolve_image(sc["image"], base)
        inputs += ["-loop", "1", "-t", f"{dur}", "-i", img]
        frames = int(dur * fps)
        # Alternate zoom-in / zoom-out for visual variety.
        if i % 2 == 0:
            zoom = f"1+0.12*on/{frames}"
        else:
            zoom = f"1.12-0.12*on/{frames}"
        chain = (
            f"[{i}:v]scale={w * 2}:{h * 2}:force_original_aspect_ratio=increase,"
            f"crop={w * 2}:{h * 2},"
            f"zoompan=z='{zoom}':x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2'"
            f":d={frames}:s={w}x{h}:fps={fps},"
            f"format=yuv420p"
        )
        headline = sc.get("headline")
        if headline:
            text = "\n".join(headline) if isinstance(headline, list) else headline
            chain += "," + drawtext(text, size=sc.get("fontsize", 72),
                                    y=sc.get("y", "h-640"), fade_in=0.4)
        filters.append(chain + f"[v{i}]")

    n = len(scenes)
    if end:
        bg = end.get("bg", "0x101010")
        dark = end.get("fg", "0x2B1D12")
        accent = end.get("accent", "0xE8641B")
        chain = f"color=c={bg}:s={w}x{h}:d={end_dur}:r={fps},format=yuv420p"
        title = end.get("title")
        if title:
            text = "\n".join(title) if isinstance(title, list) else title
            chain += "," + drawtext(text, size=84, color=dark, y="h*0.34",
                                    box=False, fade_in=0.3)
        if end.get("price"):
            chain += "," + drawtext(end["price"], size=72, color="white",
                                    y="h*0.50", boxcolor=f"{accent}@1.0",
                                    boxborder=32, fade_in=0.5)
        if end.get("cta"):
            chain += "," + drawtext(end["cta"], size=64, color="white",
                                    y="h*0.63", boxcolor=f"{dark}@1.0",
                                    boxborder=30, fade_in=0.7)
        if end.get("brand"):
            chain += "," + drawtext(end["brand"], size=46, color=dark,
                                    y="h*0.88", box=False, fade_in=0.3)
        filters.append(chain + f"[v{n}]")
        n += 1

    # Chain crossfades: each clip overlaps the previous by `xf` seconds.
    prev = "[v0]"
    offset = 0.0
    for i in range(1, n):
        clip_dur = dur if i - 1 < len(scenes) else end_dur
        offset += clip_dur - xf
        out = f"[x{i}]" if i < n - 1 else "[xlast]"
        filters.append(
            f"{prev}[v{i}]xfade=transition=fade:duration={xf}:offset={offset:.3f}{out}"
        )
        prev = out
    total = len(scenes) * dur + end_dur - (n - 1) * xf
    filters.append(
        f"{prev}fade=t=out:st={total - 0.6:.3f}:d=0.6,format=yuv420p[vout]"
    )

    output = str((base / cfg.get("output", "ad.mp4")).resolve())
    cmd = (
        ["ffmpeg", "-y", *inputs,
         "-f", "lavfi", "-t", f"{total:.3f}", "-i",
         "anullsrc=channel_layout=stereo:sample_rate=44100",
         "-filter_complex", ";".join(filters),
         "-map", "[vout]", "-map", f"{len(scenes)}:a",
         "-c:v", "libx264", "-preset", "medium", "-crf", "21",
         "-c:a", "aac", "-b:a", "96k", "-shortest",
         "-movflags", "+faststart", output]
    )
    print("Rendering", output, f"({total:.1f}s)")
    subprocess.run(cmd, check=True)
    print("Done:", output)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg is required (apt-get install ffmpeg)")
    build(sys.argv[1])
