#!/usr/bin/env python3
"""压黑(near-black -> pure black) + 提亮 + 横向拼接 spritesheet for ADD blend.

Usage:
  process_fx.py crush  <frames_dir> <glob>           # crush+brighten frames in place
  process_fx.py stitch <frames_dir> <glob> <out.png> # horizontal stitch (1 row)
  process_fx.py bright <frames_dir> <glob>           # report per-frame mean brightness
"""
import sys, glob, os
import numpy as np
from PIL import Image


def list_frames(frames_dir, pattern):
    files = sorted(glob.glob(os.path.join(frames_dir, pattern)))
    return files


def crush_frame(path, thresh=34, gain=1.15):
    img = Image.open(path).convert('RGB')
    a = np.array(img).astype(int)
    m = a.max(2)                      # per-pixel max channel
    mask = m < thresh                 # near-black pixels
    a[mask] = 0                       # force to pure black
    a = np.clip(a * gain, 0, 255)     # brighten the fire
    out = Image.fromarray(a.astype('uint8'), 'RGB')
    out.save(path)


def brightness(frames_dir, pattern):
    for f in list_frames(frames_dir, pattern):
        a = np.array(Image.open(f).convert('RGB')).astype(int)
        print(f"{os.path.basename(f)}\t{a.max(2).mean():.3f}")


def stitch(frames_dir, pattern, out_path):
    files = list_frames(frames_dir, pattern)
    imgs = [Image.open(f).convert('RGB') for f in files]
    w, h = imgs[0].size
    sheet = Image.new('RGB', (w * len(imgs), h), (0, 0, 0))
    for i, im in enumerate(imgs):
        if im.size != (w, h):
            im = im.resize((w, h))
        sheet.paste(im, (i * w, 0))
    sheet.save(out_path)
    print(f"N={len(imgs)} cell={w}x{h} sheet={sheet.size[0]}x{sheet.size[1]} -> {out_path}")


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'crush':
        for f in list_frames(sys.argv[2], sys.argv[3]):
            crush_frame(f)
        print(f"crushed {len(list_frames(sys.argv[2], sys.argv[3]))} frames")
    elif cmd == 'bright':
        brightness(sys.argv[2], sys.argv[3])
    elif cmd == 'stitch':
        stitch(sys.argv[2], sys.argv[3], sys.argv[4])
