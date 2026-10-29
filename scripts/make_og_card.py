"""Make the 1200x630 social card and a 1600px hero crop from Storylight's
rendered JPEGs (a centre crop and resize of an already-developed picture;
no raw decoding).

Usage: python -I scripts/make_og_card.py
"""
import json
import os
from PIL import Image

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(open(os.path.join(root, "chapters.json")))


def cover(src, w, h, dst, quality=84):
    im = Image.open(src).convert("RGB")
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    im = im.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    left = (im.width - w) // 2
    top = (im.height - h) // 2
    im.crop((left, top, left + w, top + h)).save(dst, "JPEG", quality=quality,
                                                 optimize=True, progressive=True)
    print(dst, w, h)


images = os.path.join(root, "images")
cover(os.path.join(images, cfg["og_source"]), 1200, 630,
      os.path.join(images, "og-card.jpg"))
cover(os.path.join(images, cfg["hero"]["landscape"]), 1600, 900,
      os.path.join(images, "hero-landscape.jpg"))
