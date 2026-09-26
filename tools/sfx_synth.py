"""Synthesize dark drone music + SFX (whoosh, hit, riser, shutter, glitch) as WAVs."""
import numpy as np, wave
SR = 44100
P = "/tmp/claude-0/-home-user-Negin/d5288e51-5e9b-5613-adee-5159b473691a/scratchpad/ph/"
rng = np.random.default_rng(3)

def save(name, x):
    x = np.clip(x, -1, 1)
    st = np.stack([x, x], 1) if x.ndim == 1 else x
    with wave.open(P + name, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())

def lowpass(x, a):
    y = np.zeros_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc); y[i] = acc
    return y

def env(n, att, rel):
    e = np.ones(n)
    a = int(att * SR); r = int(rel * SR)
    e[:a] = np.linspace(0, 1, a) if a else 1
    e[-r:] *= np.linspace(1, 0, r) if r else 1
    return e

T = 22.6
n = int(T * SR); t = np.arange(n) / SR
# drone: detuned low sines + slow LFO + filtered noise bed
drone = (0.35 * np.sin(2 * np.pi * 55 * t) + 0.25 * np.sin(2 * np.pi * 55.4 * t)
         + 0.18 * np.sin(2 * np.pi * 82.4 * t + np.sin(t * 0.3)) + 0.10 * np.sin(2 * np.pi * 110 * t))
drone *= 0.7 + 0.3 * np.sin(2 * np.pi * 0.12 * t)
noise = lowpass(rng.normal(0, 1, n) * 0.6, 0.02)
# tension pulse (heartbeat-ish) every 1.2s
pulse = np.zeros(n)
for k in np.arange(0.3, T, 1.2):
    i = int(k * SR); m = int(0.25 * SR)
    if i + m < n:
        tt = np.arange(m) / SR
        pulse[i:i + m] += np.sin(2 * np.pi * 48 * tt) * np.exp(-tt * 18) * 0.9
music = (drone + noise * 0.5 + pulse * 0.6)
music *= env(n, 0.05, 1.5)
music = music / np.max(np.abs(music)) * 0.9
save("music.wav", music)

# whoosh: noise swept through lowpass with rising/falling cutoff
m = int(0.45 * SR)
x = rng.normal(0, 1, m)
a = np.concatenate([np.linspace(0.01, 0.35, m // 2), np.linspace(0.35, 0.01, m - m // 2)])
y = np.zeros(m); acc = 0.0
for i in range(m):
    acc += a[i] * (x[i] - acc); y[i] = acc
y *= np.hanning(m)
save("whoosh.wav", y / np.max(np.abs(y)) * 0.9)

# hit / boom
m = int(1.2 * SR); tt = np.arange(m) / SR
f = 60 * np.exp(-tt * 3) + 35
ph = 2 * np.pi * np.cumsum(f) / SR
boom = np.sin(ph) * np.exp(-tt * 3.5) + lowpass(rng.normal(0, 1, m), 0.05) * np.exp(-tt * 12) * 0.8
save("hit.wav", boom / np.max(np.abs(boom)) * 0.95)

# riser: rising filtered noise + rising tone
m = int(1.6 * SR); tt = np.arange(m) / SR
f = 200 + 1200 * (tt / tt[-1]) ** 2
tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3
nz = rng.normal(0, 1, m); acc = 0.0; y = np.zeros(m)
for i in range(m):
    acc += (0.02 + 0.3 * (i / m)) * (nz[i] - acc); y[i] = acc
r = (tone + y * 0.8) * (tt / tt[-1]) ** 1.5
save("riser.wav", r / np.max(np.abs(r)) * 0.8)

# camera shutter: two short clicks
m = int(0.18 * SR); s = np.zeros(m)
for off in (0, int(0.07 * SR)):
    k = int(0.012 * SR)
    s[off:off + k] += rng.normal(0, 1, k) * np.exp(-np.arange(k) / (0.002 * SR))
save("shutter.wav", s / np.max(np.abs(s)) * 0.8)

# glitch: bitcrushed noise bursts
m = int(0.3 * SR); g = np.zeros(m)
for k in range(6):
    i = rng.integers(0, m - 2000); L = rng.integers(400, 2000)
    g[i:i + L] = np.sign(np.sin(2 * np.pi * rng.integers(200, 1500) * np.arange(L) / SR)) * 0.6
g = np.round(g * 4) / 4
save("glitch.wav", g)
print("sfx done")
