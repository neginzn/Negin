"""Brick-letter banner for the What If channel (2560x1440).
Letters are built from studded bricks on a baseplate. Spelling is exact because it is drawn by code.
Usage: python make_brick_banner.py "SUBSCRIBE" out.png
"""
import sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 2560, 1440
CELL = 29                       # brick width / baseplate stud pitch in px (text must fit the 1546px mobile-safe width)
CELL_H = 44                     # letter bricks are taller than wide (upright bricks) so the word is bigger
SS = 4                          # supersampling for the brick tile

G = {
 'S': [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
 'U': ["#...#"] * 6 + [".###."],
 'B': ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
 'C': [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
 'R': ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
 'I': ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
 'E': ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
 'W': ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
 'H': ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
 'A': [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
 'T': ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
 'F': ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
 'O': [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
 'Y': ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
 'N': ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
 'L': ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
 'D': ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
 'K': ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
 'P': ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
 ' ': ["..."] * 7,
}
PALETTE = [(226, 52, 44), (250, 198, 24), (28, 108, 214), (48, 168, 84)]


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def brick_tile(color, n=CELL, m=CELL_H):
    N = n * SS
    M = m * SS
    t = Image.new("RGBA", (N, M), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    pad = int(N * 0.035)
    d.rounded_rectangle((pad, pad, N - pad, M - pad), radius=int(N * 0.14), fill=shade(color, 0.72))
    d.rounded_rectangle((pad, pad, N - pad - int(N * 0.05), M - pad - int(N * 0.05)), radius=int(N * 0.13), fill=color)
    d.rounded_rectangle((pad + int(N * .04), pad + int(N * .04), N - pad - int(N * .12), int(N * .25)),
                        radius=int(N * .08), fill=shade(color, 1.18))
    cx, cy = N * 0.5, M * 0.5
    r = N * 0.30
    d.ellipse((cx - r, cy - r + N * .05, cx + r, cy + r + N * .05), fill=shade(color, 0.62))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=shade(color, 1.05))
    d.ellipse((cx - r * .78, cy - r * .78, cx + r * .70, cy + r * .70), fill=color)
    d.pieslice((cx - r * .6, cy - r * .6, cx + r * .1, cy + r * .1), 180, 270, fill=shade(color, 1.35))
    return t.resize((n, m), Image.LANCZOS)


def baseplate(x0, y0):
    bg = np.zeros((H, W, 3), np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    top = np.array([24, 58, 120], np.float32)
    bot = np.array([12, 30, 72], np.float32)
    k = (yy / H)[..., None]
    bg[:] = top * (1 - k) + bot * k
    rad = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)[..., None]
    bg *= (1.12 - 0.35 * np.clip(rad, 0, 1.3))
    im = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(im)
    gx = x0 % CELL
    gy = y0 % CELL
    r = CELL * 0.30
    for y in range(gy - CELL, H + CELL, CELL):
        for x in range(gx - CELL, W + CELL, CELL):
            cx, cy = x + CELL / 2, y + CELL / 2
            d.ellipse((cx - r, cy - r + 2, cx + r, cy + r + 2), fill=(8, 20, 52, 150))
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(30, 68, 132, 255))
            d.ellipse((cx - r * .8, cy - r * .8, cx + r * .7, cy + r * .7), fill=(33, 74, 142, 255))
            d.pieslice((cx - r * .6, cy - r * .6, cx + r * .1, cy + r * .1), 180, 270, fill=(48, 92, 164, 255))
    return im


def main(text="SUBSCRIBE", out="banner.png"):
    text = text.upper()
    cols = sum(len(G[c][0]) for c in text) + (len(text) - 1)
    rows = 7
    x0 = (W - cols * CELL) // 2
    y0 = (H - rows * CELL_H) // 2
    img = baseplate(x0, y0)

    cells = []
    cx = 0
    for i, ch in enumerate(text):
        g = G[ch]
        for r in range(rows):
            for c, v in enumerate(g[r]):
                if v == "#":
                    cells.append((cx + c, r, PALETTE[i % len(PALETTE)]))
        cx += len(g[0]) + 1

    random.seed(7)
    deco = []
    for gy in range(0, H // CELL + 1):
        for gx in range(0, W // CELL + 1):
            px = (x0 % CELL) - CELL + gx * CELL
            py = (y0 % CELL) - CELL + gy * CELL
            if (px < 260 or px > W - 260) and random.random() < 0.035:
                deco.append((px, py, random.choice(PALETTE)))

    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for px, py, _ in deco:
        sd.rectangle((px + 6, py + 9, px + CELL + 6, py + CELL + 9), fill=(0, 0, 0, 140))
    for c, r, _ in cells:
        px, py = x0 + c * CELL, y0 + r * CELL_H
        sd.rectangle((px + 8, py + 12, px + CELL + 8, py + CELL_H + 12), fill=(0, 0, 0, 150))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))

    cache = {}
    def tile(col):
        if col not in cache:
            cache[col] = brick_tile(col)
        return cache[col]
    for px, py, col in deco:
        img.alpha_composite(brick_tile(col, CELL, CELL), (int(px), int(py)))
    for c, r, col in cells:
        img.alpha_composite(tile(col), (x0 + c * CELL, y0 + r * CELL_H))
    img.convert("RGB").save(out)
    print(out, "cols", cols, "text width px", cols * CELL, "(mobile-safe max 1546)")


if __name__ == "__main__":
    main(*(sys.argv[1:3]))
