#!/usr/bin/env python3
"""Adaptive chroma-key for AI-video frames.
AI video green backgrounds are often matte olive, not pure bright green, so we
use greenness = g-(r+b)/2 combined with luminance to separate background (bright)
from the character. Two-tier (hard/soft) + green-spill suppression. Frames are
NOT cropped so every frame stays the same WxH for alignment in the sheet.
"""
from PIL import Image
import numpy as np, glob, os, sys

BASE = "/Users/lukeliu/gei-workspace/output/normandy-bunker-shooter/assets/anim/zombie-exploder"
frames = sorted(glob.glob(os.path.join(BASE, "_frames", "*.png")))
if not frames:
    print("NO_FRAMES")
    sys.exit(1)

# Auto-sample the background greenness/luminance from frame corners so the
# thresholds adapt to whatever olive/green the model produced.
samples_grn, samples_lum = [], []
for fp in frames:
    a = np.array(Image.open(fp).convert("RGB")).astype(np.int16)
    h, w, _ = a.shape
    m = 12  # corner patch
    corners = np.concatenate([
        a[:m, :m].reshape(-1, 3), a[:m, -m:].reshape(-1, 3),
        a[-m:, :m].reshape(-1, 3), a[-m:, -m:].reshape(-1, 3),
    ])
    r, g, b = corners[:, 0], corners[:, 1], corners[:, 2]
    grn = g - (r + b) // 2
    lum = (r + g + b) // 3
    samples_grn.append(np.median(grn))
    samples_lum.append(np.median(lum))

bg_grn = float(np.median(samples_grn))
bg_lum = float(np.median(samples_lum))
print(f"sampled bg greenness median={bg_grn:.1f} luminance median={bg_lum:.1f}")

# Derive thresholds from the sampled background but floor them so a weak-green
# background still keys. hard cut at ~60% of bg greenness, soft band below.
hard_grn = max(18, bg_grn * 0.55)
soft_grn = max(8, hard_grn * 0.45)
lum_floor = max(50, bg_lum * 0.55)
print(f"thresholds: hard_grn>{hard_grn:.0f} soft_grn>{soft_grn:.0f} lum>{lum_floor:.0f}")

for fp in frames:
    im = Image.open(fp).convert("RGBA")
    a = np.array(im).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    grn = g - (r.astype(int) + b) // 2
    lum = (r + g + b) // 3
    bg = (grn > hard_grn) & (lum > lum_floor)
    soft = (grn > soft_grn) & (grn <= hard_grn)
    al = a[..., 3].copy()
    al[bg] = 0
    al[soft] = (al[soft] * 0.4).astype(np.int16)
    # green-spill suppression: clamp green channel down to max(r,b) where it leaks
    spill = g > np.maximum(r, b)
    a[..., 1] = np.where(spill, np.maximum(r, b), g)
    a[..., 3] = al

    # --- cleanup ---
    h, w = al.shape
    # 1) erase the model watermark box in the top-right corner
    a[0:62, w - 135:w, 3] = 0
    # 2) remove isolated speckle: keep only the largest connected alpha blob
    mask = a[..., 3] > 40
    try:
        from scipy import ndimage
        lab, num = ndimage.label(mask)
        if num > 1:
            sizes = ndimage.sum(np.ones_like(lab), lab, range(1, num + 1))
            keep = (np.argmax(sizes) + 1)
            big = lab == keep
            a[..., 3] = np.where(big, a[..., 3], 0)
    except Exception:
        # scipy not available: cheap morphological despeckle via 3x3 neighbour count
        m = mask.astype(np.uint8)
        nb = (np.roll(m, 1, 0) + np.roll(m, -1, 0) + np.roll(m, 1, 1) + np.roll(m, -1, 1))
        lonely = (m == 1) & (nb == 0)
        a[..., 3] = np.where(lonely, 0, a[..., 3])

    Image.fromarray(np.clip(a, 0, 255).astype("uint8")).save(fp)
print(f"keyed {len(frames)} frames")
