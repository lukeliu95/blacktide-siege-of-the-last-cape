#!/usr/bin/env python3
"""Horizontally pack keyed frames into a 1-row Phaser spritesheet.
Each cell = one keyed frame downsampled to ~200px wide (keeping aspect), all
cells the same WxH so Phaser can slice on a fixed frameWidth/frameHeight grid.
"""
from PIL import Image
import glob, os, json, sys

BASE = "/Users/lukeliu/gei-workspace/output/normandy-bunker-shooter/assets/anim/zombie-exploder"
TARGET_W = 200
frames = sorted(glob.glob(os.path.join(BASE, "_frames", "*.png")))
if not frames:
    print("NO_FRAMES")
    sys.exit(1)

imgs = [Image.open(fp).convert("RGBA") for fp in frames]
# All source frames share the same dimensions (we never cropped), so scale is uniform.
sw, sh = imgs[0].size
scale = TARGET_W / sw
cw = TARGET_W
ch = max(1, round(sh * scale))
imgs = [im.resize((cw, ch), Image.LANCZOS) for im in imgs]

n = len(imgs)
sheet = Image.new("RGBA", (cw * n, ch), (0, 0, 0, 0))
for i, im in enumerate(imgs):
    sheet.paste(im, (i * cw, 0), im)

out = os.path.join(BASE, "walk-sheet-sm.png")
sheet.save(out)
meta = {"frames": n, "frameW": cw, "frameH": ch, "sheetW": cw * n, "sheetH": ch, "sheet": out}
print(json.dumps(meta))
with open(os.path.join(BASE, "walk-sheet-sm.json"), "w") as f:
    json.dump(meta, f, indent=2)
