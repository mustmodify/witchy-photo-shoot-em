"""Build index.html from chapters.json + manifest.json + assets/*.svg.

Usage: python -I scripts/build_html.py [--noindex]
"""
import json
import os
import re
import sys
from html import escape

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "witchy-photo-shoot-em"
BASE = f"https://mustmodify.github.io/{REPO}/"
NOINDEX = "--noindex" in sys.argv

cfg = json.load(open(os.path.join(root, "chapters.json"), encoding="utf-8"))
manifest = {m["file"]: m for m in json.load(open(os.path.join(root, "manifest.json"), encoding="utf-8"))}
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII"]
ALT = {
    0: "Em in the white dress with a basket",
    1: "Em in the black dress at the cauldron",
    2: "Em in the black dress at the cauldron",
    3: "Em in the black dress at the cauldron",
    4: "Em in the black dress and hat with the iron tripod",
    5: "Em in the black dress and wide-brimmed hat",
    6: "Em in the oak tree",
}


def svg(name, cls="", extra=""):
    s = open(os.path.join(root, "assets", name + ".svg"), encoding="utf-8").read()
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S).strip()
    s = s.replace(' xmlns="http://www.w3.org/2000/svg"', "")
    return s.replace("<svg", f'<svg class="{cls}" aria-hidden="true" focusable="false"{extra}', 1)


def num(f):
    return f[4:8]


total = sum(len(c["frames"]) for c in cfg["chapters"])
title = cfg["title"]
desc = f"Review album: {total} picked frames from the {cfg['date'] and '5 October 2026'} shoot. Tap a photo, send me the numbers."

# chapter index
index = []
for i, c in enumerate(cfg["chapters"]):
    index.append(
        f'<a href="#{c["id"]}" data-target="{c["id"]}">{svg(c["icon"], "ci")}'
        f'<span>{escape(c["title"])}</span><small>{len(c["frames"])}</small></a>'
    )

sections = []
seen = 0
for i, c in enumerate(cfg["chapters"]):
    parts = [
        f'<section class="chapter" id="{c["id"]}">',
        '<header class="ch-head">',
        svg(c["icon"], "ch-icon"),
        f'<p class="label">Chapter {ROMAN[i]}</p>',
        f'<h2>{escape(c["title"])}</h2>',
        f'<p class="deck">{escape(c["deck"])}</p>',
        f'<p class="count">{len(c["frames"])} frames</p>',
        "</header>",
        '<div class="grid">',
    ]
    last_move = None
    for f in c["frames"]:
        m = manifest[f["file"]]
        mv = f.get("movement")
        if mv and mv != last_move:
            parts.append(f'<h3 class="movement label">{escape(mv)}</h3>')
            last_move = mv
        n = num(f["file"])
        lazy = "" if seen < 8 else ' loading="lazy"'
        seen += 1
        alt = f'{ALT[i]}, {c["title"]}, frame {n}'
        cls = ' class="wide"' if m["w"] > m["h"] else ""
        parts.append(
            f'<figure class="frame"{cls}>'
            f'<a href="images/{f["file"]}" data-w="{m["w"]}" data-h="{m["h"]}" data-n="{n}" '
            f'data-chapter="{escape(c["title"])}">'
            f'<img src="images/thumbs/{f["file"]}" width="{m["tw"]}" height="{m["th"]}"{lazy} '
            f'decoding="async" alt="{escape(alt)}"></a>'
            f"<figcaption>{n}</figcaption></figure>"
        )
    parts.append("</div></section>")
    sections.append("\n".join(parts))
    if i < len(cfg["chapters"]) - 1:
        sections.append(svg("divider", "divider"))

footer_icons = "".join(svg(n, "fi") for n in ["moth", "herb-sprig", "cauldron", "candle", "snake", "basket"])
hero = cfg["hero"]
strands = "".join(
    f'<div class="strand s{k}">{svg("hanging-crystal")}</div>' for k in (1, 2, 3)
)

CSS = open(os.path.join(root, "scripts", "page.css"), encoding="utf-8").read()
JS = open(os.path.join(root, "scripts", "page.js"), encoding="utf-8").read()

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<style>[hidden]{{display:none!important}}</style>
<meta name="description" content="{escape(desc)}">
<meta name="theme-color" content="#15130f">
{'<meta name="robots" content="noindex">' if NOINDEX else ''}
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{BASE}">
<meta property="og:image" content="{BASE}images/og-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(desc)}">
<meta name="twitter:image" content="{BASE}images/og-card.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=EB+Garamond:ital,wght@0,400;1,400&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
<header class="hero">
<picture>
<source media="(min-width: 700px)" srcset="images/hero-landscape.jpg" width="1600" height="900">
<img src="images/{hero['portrait']}" width="{manifest[hero['portrait']]['w']}" height="{manifest[hero['portrait']]['h']}" alt="Em in the black dress and wide-brimmed hat">
</picture>
<div class="hero-fade"></div>
{strands}
<div class="orb moon">{svg("moon-face")}</div>
<div class="orb sun">{svg("sun-face")}</div>
<div class="hero-text">
<p class="label">A review album</p>
<h1>{escape(title)}</h1>
<p class="meta">5 October 2026 · {total} picks · photographs by {escape(cfg['photographer'])}</p>
</div>
</header>
<main>
<section class="how">
<p>Tap any photo to open it. Arrow keys or swipe to move, Esc to close. Every frame shows its number; send me the numbers you love and the ones to drop.</p>
{svg("divider", "divider")}
</section>
<nav class="index" aria-label="Chapters">
{chr(10).join(index)}
</nav>
{chr(10).join(sections)}
</main>
<footer>
<div class="icons">{footer_icons}</div>
<p>Shot 5 October 2026 · {total} frames · photographs © {escape(cfg['photographer'])} · made with Storylight</p>
</footer>
<dialog id="lightbox" hidden aria-label="Photo viewer">
<div class="lb-bar"><span id="lb-info"></span><button type="button" id="lb-close" aria-label="Close">&times;</button></div>
<button type="button" class="lb-nav prev" id="lb-prev" aria-label="Previous photo">&#8249;</button>
<img id="lb-img" alt="">
<button type="button" class="lb-nav next" id="lb-next" aria-label="Next photo">&#8250;</button>
<div class="lb-progress"><i id="lb-bar"></i></div>
</dialog>
<script>
{JS}
</script>
</body>
</html>
"""
open(os.path.join(root, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
print("index.html", len(html), "bytes,", total, "frames")
