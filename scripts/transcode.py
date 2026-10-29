"""Transcode Storylight's developed JPEG renders to web weight.

Storylight (frame_render, long_edge 1600) already produced the developed,
upright picture for every pick. This script does NOT decode raws or fix
orientation; it only re-encodes Storylight's JPEG output at a web quality
and writes a small thumbnail for the grid, then records sizes in
manifest.json.

Usage:
  python -I scripts/transcode.py <staging-dir> <images-dir> picks.txt
"""
import json
import os
import sys
from PIL import Image


def lp(path):
    # Windows long-path prefix: the staging folder is > 260 chars.
    path = os.path.abspath(path)
    return path if path.startswith("\\\\?\\") else "\\\\?\\" + path


staging, out_dir, picks_file = lp(sys.argv[1]), lp(sys.argv[2]), lp(sys.argv[3])
thumb_dir = os.path.join(out_dir, "thumbs")
os.makedirs(thumb_dir, exist_ok=True)

with open(picks_file) as f:
    order = [f"_T1A{n}" for n in f.read().split()]

manifest = []
missing = []
odd_orientation = []
for stem in order:
    src = os.path.join(staging, stem + ".jpg")
    if not os.path.exists(src):
        missing.append(stem)
        continue
    im = Image.open(src)
    orient = im.getexif().get(0x0112)
    if orient not in (None, 1):
        odd_orientation.append((stem, orient))
    im = im.convert("RGB")
    w, h = im.size
    im.save(os.path.join(out_dir, stem + ".jpg"), "JPEG",
            quality=82, optimize=True, progressive=True)
    t = im.copy()
    t.thumbnail((560, 560), Image.LANCZOS)
    t.save(os.path.join(thumb_dir, stem + ".jpg"), "JPEG",
           quality=78, optimize=True, progressive=True)
    manifest.append({"file": stem + ".jpg", "w": w, "h": h,
                     "tw": t.size[0], "th": t.size[1]})

with open(os.path.join(os.path.dirname(out_dir), "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=0)

print(f"transcoded {len(manifest)} frames; missing {len(missing)}: {missing}")
print(f"orientation tags other than 1: {odd_orientation}")
