"""Stranger Files detective mascot animator.

Composites the detective (assets/mascot) over a clip: pop/slide/rise in,
point at a target, idle bob, random blinks, mouth flap driven by a voice track.

    python mascot.py plan.json

plan.json:
{
  "bg": "clip.mp4",            # background video (scaled to 1920x1080); or "bg_color": [0,255,0] + "duration": 6
  "voice": "voice.wav",        # optional: drives the mouth and is used as the output audio
  "keep_bg_audio": false,      # mix the background clip's audio under the voice
  "out": "out.mp4",            # .mp4 = composite, .mov = transparent ProRes 4444 (bg ignored)
  "fps": 30,
  "stroke": 5,                 # white sticker outline in px (0 = off)
  "segments": [
    {"t0": 0.4, "t1": 5.0, "pose": "point_right", "h": 620,
     "target": [1300, 520],    # fingertip lands here (pointing poses); or "anchor": [x, y] = feet position
     "enter": "pop", "exit": "pop",     # pop | slide_left | slide_right | rise | none
     "flip": false, "talk": true,
     "poses": [[2.5, "neutral"]]        # optional pose switches (absolute seconds)
    }
  ]
}
"""
import json, math, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

FF = '/usr/bin/ffmpeg'
W, H = 1920, 1080
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'mascot')
MOUTH_LEVELS = 5


def blur(a, sigma):
    if a.ndim == 3:
        return np.dstack([blur(a[:, :, c], sigma) for c in range(a.shape[2])])
    r = max(1, int(round(sigma * 0.9)))   # 3 box passes ~ gaussian
    a = a.astype(np.float64)
    for ax in (0, 1):
        for _ in range(3):
            p = np.pad(a, [(r + 1, r) if i == ax else (0, 0) for i in range(2)], mode='edge')
            c = np.cumsum(p, axis=ax)
            n = c.shape[ax]
            a = (np.take(c, range(2 * r + 1, n), axis=ax) - np.take(c, range(0, n - 2 * r - 1), axis=ax)) / (2 * r + 1)
    return a


def inpaint(img, mask, sigma=10):
    """Fill mask with the surrounding head texture (normalized convolution)."""
    arr = np.asarray(img).astype(np.float32)
    lum = arr[:, :, :3].mean(2)
    valid = (~mask) & (arr[:, :, 3] > 250) & (lum > 80) & (lum < 205)
    v = valid.astype(np.float32)
    fill = blur(arr[:, :, :3] * v[:, :, None], sigma) / np.maximum(blur(v, sigma), 1e-4)[:, :, None]
    m = blur(mask.astype(np.float32) * 255, 1.2)
    m = np.minimum(m, arr[:, :, 3]) / 255
    out = arr.copy()
    out[:, :, :3] = arr[:, :, :3] * (1 - m[:, :, None]) + fill * m[:, :, None]
    return Image.fromarray(out.clip(0, 255).astype(np.uint8), 'RGBA')


def grow(mask, px):
    return np.asarray(Image.fromarray(mask.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(2 * px + 1))) > 0


def region(shape, cx, cy, rx, ry):
    ys, xs = np.ogrid[:shape[0], :shape[1]]
    return ((xs - cx) / rx) ** 2 + ((ys - cy) / ry) ** 2 <= 1


def build_variants(name, info):
    """Return dict[(mouth_level, blink)] -> RGBA at 2x for one pose."""
    base = Image.open(os.path.join(ASSETS, name + '.png')).convert('RGBA')
    SS = 2
    base = base.resize((base.width * SS, base.height * SS), Image.LANCZOS)
    arr = np.asarray(base).astype(int)
    lum = arr[:, :, :3].mean(2)
    eyes = [(ex * SS, ey * SS) for ex, ey in info['eyes']]
    eye_mask = np.zeros(lum.shape, bool)
    for ex, ey in eyes:
        eye_mask |= region(lum.shape, ex, ey - 4, 34, 28) & (lum > 175)
    eye_mask = grow(eye_mask, 4)
    closed = inpaint(base, eye_mask)
    glow = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    for k, (ex, ey) in enumerate(eyes):
        tilt = 4 if k == 0 else -4          # inner ends lower = keeps the frown
        d.line([(ex - 13, ey + 2 - tilt), (ex + 13, ey + 2 + tilt)], fill=(255, 255, 250, 255), width=6)
    halo = glow.filter(ImageFilter.GaussianBlur(5))
    closed.alpha_composite(halo)
    closed.alpha_composite(glow)

    mouth = info.get('mouth')
    mouth_clean = {}
    if mouth:
        x0, x1, my = (v * SS for v in mouth)
        mm = region(lum.shape, (x0 + x1) / 2, my, (x1 - x0) / 2 + 22, 20) & (lum < 95)
        mm = grow(mm, 3)
        for bl, im in ((0, base), (1, closed)):
            mouth_clean[bl] = inpaint(im, mm)
    out = {}
    for lv in (range(MOUTH_LEVELS) if mouth else [0]):
        for blink in (0, 1):
            src = closed if blink else base
            if not (mouth and lv):
                out[(lv, blink)] = src
                continue
            im = mouth_clean[blink].copy()
            cx = (x0 + x1) / 2
            half_w = (x1 - x0) * (0.24 + 0.035 * lv)
            hh = 3 + 5.5 * lv
            d = ImageDraw.Draw(im)
            d.ellipse((cx - half_w, my - hh * 0.45, cx + half_w, my + hh * 0.55),
                      fill=(32, 22, 22, 255), outline=(15, 12, 12, 255), width=3)
            if lv >= 3:
                d.chord((cx - half_w * 0.6, my + hh * 0.05, cx + half_w * 0.6, my + hh * 0.55),
                        0, 180, fill=(150, 60, 60, 255))
            out[(lv, blink)] = im
    return out


def with_stroke(im, px):
    if px <= 0:
        return im
    pad = px + 2
    big = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    big.alpha_composite(im, (pad, pad))
    a = big.getchannel('A').point(lambda v: 255 if v > 40 else 0)
    k = 2 * px + 1
    a = a.filter(ImageFilter.MaxFilter(k if k % 2 else k + 1)).filter(ImageFilter.GaussianBlur(1))
    st = Image.new('RGBA', big.size, (245, 245, 240, 0))
    st.putalpha(a)
    st.alpha_composite(big)
    return st


def put(frame, spr, x, y):
    sx0, sy0 = max(0, -x), max(0, -y)
    sx1, sy1 = min(spr.width, W - x), min(spr.height, H - y)
    if sx1 > sx0 and sy1 > sy0:
        frame.alpha_composite(spr.crop((sx0, sy0, sx1, sy1)), (x + sx0, y + sy0))


def ease_out_back(x, s=1.9):
    x -= 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def ease_in_back(x, s=1.9):
    return (s + 1) * x ** 3 - s * x ** 2


def mouth_track(path, fps, n):
    raw = subprocess.run([FF, '-v', 'error', '-i', path, '-ac', '1', '-ar', '16000', '-af', 'highpass=f=200,lowpass=f=3500', '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = 16000 / fps
    env = np.array([np.sqrt(np.mean(a[int(i * hop):int(i * hop + hop * 1.5)] ** 2) + 1e-9)
                    if int(i * hop) < len(a) else 0 for i in range(n)])
    if env.max() <= 0:
        return np.zeros(n, int)
    floor = np.percentile(env, 20)
    ref = np.percentile(env, 92)
    env = np.clip((env - floor * 1.3) / max(ref - floor * 1.3, 1e-6), 0, 1.2)
    sm = np.zeros_like(env)
    for i, v in enumerate(env):
        p = sm[i - 1] if i else 0
        sm[i] = v if v > p else p * 0.55 + v * 0.45
    lv = np.where(sm < 0.18, 0, np.clip(np.round(sm * 4), 1, 4)).astype(int)
    run = 0
    for i in range(1, n):  # keep the jaw moving on sustained loud vowels
        run = run + 1 if lv[i] == lv[i - 1] and lv[i] > 1 else 0
        if run and run % 4 == 0:
            lv[i] -= 1
    return lv


def blink_track(n, fps, seed):
    rnd = random.Random(seed)
    b = np.zeros(n, bool)
    t = rnd.uniform(0.8, 2.0)
    while t * fps < n:
        i = int(t * fps)
        b[i:i + 3] = True
        t += rnd.uniform(2.2, 4.8)
    return b


def main(plan_path):
    plan = json.load(open(plan_path))
    base_dir = os.path.dirname(os.path.abspath(plan_path))
    rel = lambda p: p if os.path.isabs(p) else os.path.join(base_dir, p)
    meta = {k: v for k, v in json.load(open(os.path.join(ASSETS, 'meta.json'))).items() if not k.startswith('_')}
    fps = plan.get('fps', 30)
    out = rel(plan['out'])
    alpha_out = out.lower().endswith('.mov')
    bg = rel(plan['bg']) if plan.get('bg') else None
    voice = rel(plan['voice']) if plan.get('voice') else None

    if 'duration' in plan:
        dur = plan['duration']
    else:
        src = bg or voice
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src],
                                   capture_output=True, text=True).stdout)
    n = int(round(dur * fps))
    mouth = mouth_track(voice or bg, fps, n) if (voice or bg) else np.zeros(n, int)
    blinks = blink_track(n, fps, plan.get('seed', 7))
    stroke = plan.get('stroke', 5)

    used = {s['pose'] for s in plan['segments']} | {p for s in plan['segments'] for _, p in s.get('poses', [])}
    variants = {p: build_variants(p, meta[p]) for p in used}
    cache = {}

    def sprite(pose, lv, bl, h, flip):
        key = (pose, lv, bl, h, flip)
        if key not in cache:
            v = variants[pose]
            im = v.get((lv, bl)) or v[(0, bl)]
            s = h / im.height
            im = im.resize((max(1, round(im.width * s)), h), Image.LANCZOS)
            if flip:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            cache[key] = with_stroke(im, stroke)
        return cache[key]

    def feet_anchor(seg, pose, h, flip):
        if 'anchor' in seg:
            return seg['anchor']
        img = Image.open(os.path.join(ASSETS, pose + '.png'))
        s = h / img.height
        tip = meta[pose]['tip']
        tx, ty = seg['target']
        tipx = (img.width - tip[0]) if flip else tip[0]
        dx = (tipx - img.width / 2) * s
        dy = (img.height - tip[1]) * s
        back = -14 if (tipx > img.width / 2) else 14
        return [tx - dx + back, ty + dy]

    if alpha_out:
        enc = [FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
               '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', out]
    else:
        enc = [FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-']
        audio_inputs = []
        if voice:
            audio_inputs.append(voice)
        if bg and (plan.get('keep_bg_audio') or not voice):
            audio_inputs.append(bg)
        for a in audio_inputs:
            enc += ['-i', a]
        if len(audio_inputs) == 2:
            enc += ['-filter_complex', '[2:a]volume=0.35[b];[1:a][b]amix=inputs=2:duration=first:normalize=0[a]', '-map', '0:v', '-map', '[a]']
        elif audio_inputs:
            enc += ['-map', '0:v', '-map', '1:a?']
        enc += ['-t', f'{dur:.3f}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out]
    pe = subprocess.Popen(enc, stdin=subprocess.PIPE)

    pd = None
    if bg and not alpha_out:
        vf = f'scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps={fps}'
        pd = subprocess.Popen([FF, '-v', 'error', '-i', bg, '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                              stdout=subprocess.PIPE)
    bgc = tuple(plan.get('bg_color', (0, 0, 0)))
    last = None
    for i in range(n):
        t = i / fps
        if pd:
            buf = pd.stdout.read(W * H * 3)
            if len(buf) == W * H * 3:
                last = Image.frombuffer('RGB', (W, H), buf).convert('RGBA')
            frame = last.copy() if last else Image.new('RGBA', (W, H), bgc + (255,))
        else:
            frame = Image.new('RGBA', (W, H), (0, 0, 0, 0) if alpha_out else bgc + (255,))

        for si, seg in enumerate(plan['segments']):
            t0, t1 = seg['t0'], seg['t1']
            if not (t0 <= t < t1):
                continue
            pose, switched = seg['pose'], t0
            for ts, p in seg.get('poses', []):
                if t >= ts:
                    pose, switched = p, ts
            h = seg.get('h', 600)
            flip = seg.get('flip', False)
            ax, ay = feet_anchor(seg, pose, h, flip)
            lt = t - t0
            ein, eout = seg.get('enter', 'pop'), seg.get('exit', 'pop')
            din, dout = 0.38, 0.28
            scale, ox, oy = 1.0, 0.0, 0.0
            if ein != 'none' and lt < din:
                k = ease_out_back(lt / din)
                if ein == 'pop': scale = max(0.01, k)
                elif ein == 'slide_left': ox = -(1 - k) * (ax + h)
                elif ein == 'slide_right': ox = (1 - k) * (W - ax + h)
                elif ein == 'rise': oy = (1 - k) * (H - ay + h * 1.05)
            rt = t1 - t
            if eout != 'none' and rt < dout:
                k = ease_in_back(1 - rt / dout)
                if eout == 'pop': scale = max(0.01, 1 - k)
                elif eout == 'slide_left': ox = -k * (ax + h)
                elif eout == 'slide_right': ox = k * (W - ax + h)
                elif eout == 'rise': oy = k * (H - ay + h * 1.05)
            # pose-change squash and idle bob
            st = t - switched
            if switched != t0 and st < 0.15:
                scale *= 0.94 + 0.06 * (st / 0.15)
            oy += math.sin(2 * math.pi * lt / 1.7 + si) * h * 0.006
            lv = int(mouth[i]) if seg.get('talk', True) and meta[pose]['mouth'] else 0
            spr = sprite(pose, lv, bool(blinks[i]), h, flip)
            if abs(scale - 1) > 1e-3:
                spr = spr.resize((max(1, round(spr.width * scale)), max(1, round(spr.height * scale))), Image.BILINEAR)
            x = int(round(ax + ox - spr.width / 2))
            y = int(round(ay + oy - spr.height + (stroke + 2) * scale))
            put(frame, spr, x, y)
        pe.stdin.write(frame.tobytes() if alpha_out else frame.convert('RGB').tobytes())
    pe.stdin.close()
    pe.wait()
    if pd:
        pd.stdout.close()
        pd.wait()
    print('wrote', out)


if __name__ == '__main__':
    main(sys.argv[1])
