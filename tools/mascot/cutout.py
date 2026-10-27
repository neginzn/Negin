import sys, numpy as np
from PIL import Image, ImageFilter
from collections import deque
src, outdir = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert('RGB')).astype(np.int16)
H, W, _ = im.shape
mn = im.min(2); mx = im.max(2)
bgl = (mn > 215) & ((mx - mn) < 25)          # white-ish candidate
# label bg-like components (4-connected BFS)
lab = np.zeros((H, W), np.int32); n = 0; info = []
for y in range(H):
    for x in range(W):
        if bgl[y, x] and not lab[y, x]:
            n += 1; q = deque([(y, x)]); lab[y, x] = n; cnt = 0; border = False
            while q:
                cy, cx = q.popleft(); cnt += 1
                if cy in (0, H-1) or cx in (0, W-1): border = True
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny, nx = cy+dy, cx+dx
                    if 0 <= ny < H and 0 <= nx < W and bgl[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = n; q.append((ny, nx))
            info.append((n, cnt, border, cy))
bg = np.zeros((H, W), bool)
for k, cnt, border, cy in info:
    if border or cnt > 350 or (cnt > 15 and cy > 300):          # enclosed holes bigger than an eye
        bg |= lab == k
alpha = np.where(bg, 0, 255).astype(np.uint8)
a = Image.fromarray(alpha).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
rgba = Image.fromarray(im.astype(np.uint8)).convert('RGBA'); rgba.putalpha(a)
A = np.asarray(a) > 20
cols = np.where(A.any(0))[0]
# split into poses by column gaps
groups = []; start = cols[0]; prev = cols[0]
for c in cols[1:]:
    if c - prev > 1: groups.append((start, prev)); start = c
    prev = c
groups.append((start, prev))
rows = np.where(A.any(1))[0]; top, bot = rows[0], rows[-1]
print('groups', groups, 'rows', top, bot)
for i, (x0, x1) in enumerate(groups):
    sub = A[:, x0:x1+1]; r = np.where(sub.any(1))[0]
    print(i, x0, x1, r[0], r[-1])
    one = rgba.copy(); al = np.asarray(one.getchannel('A')).copy()
    al[:, :x0] = 0; al[:, x1+1:] = 0; one.putalpha(Image.fromarray(al))
    one.crop((x0-6, top-6, x1+7, bot+7)).save(f'{outdir}/pose{i}.png')
