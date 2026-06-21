#!/usr/bin/env python3
"""绿幕抠图 → 透明 PNG + 裁剪。用法: chroma_key.py in.png out.png"""
import sys
from PIL import Image
import numpy as np

def key(inp, outp):
    im = Image.open(inp).convert("RGBA")
    a = np.array(im).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # 绿幕判定:绿明显压过红蓝
    green = (g > 90) & (g - r > 40) & (g - b > 40)
    # 边缘半透明过渡带:绿略占优
    soft = (g - np.maximum(r, b) > 15) & (g - np.maximum(r, b) <= 40)
    alpha = a[..., 3].copy()
    alpha[green] = 0
    alpha[soft] = (alpha[soft] * 0.4).astype(np.int16)
    # 去绿边溢色:把残留绿降到红蓝最大值
    spill = (g > np.maximum(r, b)) & (alpha[..., ] > 0)
    a[..., 1] = np.where(spill, np.maximum(r, b), g)
    a[..., 3] = alpha
    a = np.clip(a, 0, 255).astype(np.uint8)
    out = Image.fromarray(a, "RGBA")
    # 裁剪到非透明包围盒
    bbox = out.getbbox()
    if bbox:
        out = out.crop(bbox)
    out.save(outp)
    print(f"OK {inp} -> {outp} size={out.size}")

if __name__ == "__main__":
    key(sys.argv[1], sys.argv[2])
