#!/usr/bin/env python3
"""Render a 1000x1500 Pinterest pin image for a post. Usage: make_pin.py _posts/FILE.md OUT.png"""
import re, sys, hashlib, pathlib, textwrap
from PIL import Image, ImageDraw, ImageFont
HERE = pathlib.Path(__file__).parent
PALETTES = [("#1f3b2d", "#e9dcc3", "#c9a46a"), ("#23344a", "#e6eef5", "#e08a3c"),
            ("#3b2a1f", "#f1e6d6", "#7fa36b"), ("#2b2d42", "#edf2f4", "#ef8354")]
def fm(path):
    t = pathlib.Path(path).read_text()
    m = re.match(r"---\n(.*?)\n---", t, re.S).group(1)
    get = lambda k: (re.search(rf'^{k}:\s*"?(.*?)"?\s*$', m, re.M) or [None, ""])[1]
    return get("pin_title") or get("title"), get("pin_text")
def wrap(draw, text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]
def main(post, out):
    title, sub = fm(post)
    bg, fg, accent = PALETTES[int(hashlib.md5(title.encode()).hexdigest(), 16) % len(PALETTES)]
    W, H = 1000, 1500
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    # simple mountain silhouette
    d.polygon([(0, 1150), (260, 860), (420, 1010), (640, 760), (1000, 1120), (1000, 1500), (0, 1500)], fill=accent)
    d.polygon([(0, 1260), (330, 1040), (560, 1180), (800, 1000), (1000, 1200), (1000, 1500), (0, 1500)], fill=fg)
    tf = ImageFont.truetype(str(HERE / "fonts/DejaVuSerif-Bold.ttf"), 84)
    sf = ImageFont.truetype(str(HERE / "fonts/DejaVuSans.ttf"), 44)
    y = 170
    for line in wrap(d, title, tf, W - 160):
        d.text((80, y), line, font=tf, fill=fg); y += 104
    d.rectangle([80, y + 20, 240, y + 30], fill=accent); y += 80
    for line in wrap(d, sub, sf, W - 160):
        d.text((80, y), line, font=sf, fill=fg); y += 60
    brand = ImageFont.truetype(str(HERE / "fonts/DejaVuSans.ttf"), 38)
    d.text((80, 1400), "TRAILHEAD PICKS", font=brand, fill=bg)
    im.save(out, optimize=True)
if __name__ == "__main__":
    main(*sys.argv[1:3])
