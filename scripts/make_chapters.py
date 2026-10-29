"""Build chapters.json from picks.txt (chronological order of the 413 picks).

The camera counter wrapped from _T1A9999 to _T1A0001 mid-shoot, so
chronological order is the 9xxx frames first, then the 0xxx frames. picks.txt
is already in that order. Chapter boundaries were confirmed by eye on
Storylight contact sheets (see reference/contact-sheet-*.jpg).
"""
import json
import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
order = [f"_T1A{n}.jpg" for n in open(os.path.join(root, "picks.txt")).read().split()]

# (first frame of chapter, id, title, deck, icon)
CHAPTERS = [
    ("_T1A9075", "the-gathering", "The Gathering",
     "White dress, basket and herbs. Em works the hillside, gathering what the woods offer.", "herb-sprig"),
    ("_T1A9764", "first-smoke", "First Smoke",
     "The black dress, no hat yet. The cauldron is lit and stirred.", "cauldron"),
    ("_T1A9814", "the-cauldron", "The Cauldron",
     "The hat goes on. Cauldron among the roots and the lichen-covered rock, hard afternoon light.", "witch-hat"),
    ("_T1A0226", "low-fire", "Low Fire",
     "Hat off, seated in the ferns beside the smoking cauldron. The quiet, shadowed set.", "candle"),
    ("_T1A0478", "iron-and-smoke", "Iron & Smoke",
     "The iron tripod. Hat, staff and cauldron, backlit through the yellow leaves.", "crystal-ball"),
    ("_T1A0648", "the-witch", "The Witch",
     "Close portraits. Wide-brimmed hat, choker and corset, a wand of twisted wood.", "moon-face"),
    ("_T1A0720", "into-the-trees", "Into the Trees",
     "Up into the old oak. The last light of the shoot.", "triple-moon"),
]

# Optional sub-moments inside The Gathering, from Storylight's pile names.
MOVEMENTS = [
    ("_T1A9075", "Gathering"),
    ("_T1A9210", "Power and the Stone"),
    ("_T1A9257", "The Walk"),
    ("_T1A9391", "Curiosity and Reaching"),
    ("_T1A9489", "Among the Trees"),
]

starts = {c[0] + ".jpg": i for i, c in enumerate(CHAPTERS)}
mv_starts = {m[0] + ".jpg": m[1] for m in MOVEMENTS}

chapters = []
current = None
movement = None
for f in order:
    if f in starts:
        c = CHAPTERS[starts[f]]
        current = {"id": c[1], "title": c[2], "deck": c[3], "icon": c[4], "frames": []}
        chapters.append(current)
    if f in mv_starts:
        movement = mv_starts[f]
    entry = {"file": f}
    if current["id"] == "the-gathering":
        entry["movement"] = movement
    current["frames"].append(entry)

out = {
    "title": "Witchy Photo Shoot with Em",
    "date": "2026-10-05",
    "photographer": "JW",
    "hero": {"landscape": "_T1A9841.jpg", "portrait": "_T1A0663.jpg"},
    "og_source": "_T1A0162.jpg",
    "chapters": chapters,
}
with open(os.path.join(root, "chapters.json"), "w") as fh:
    json.dump(out, fh, indent=1)

for c in chapters:
    print(f"{c['id']:16} {len(c['frames']):4}  {c['frames'][0]['file']} .. {c['frames'][-1]['file']}")
print("total", sum(len(c["frames"]) for c in chapters))
