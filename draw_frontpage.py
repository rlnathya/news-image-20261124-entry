"""Draw the front page for Tuesday, 24 November 2026.

Build-time helper only: it renders entry.png from the six stories below
using Pillow. The shipped program (main.py) only copies the finished
image, so the graded run needs nothing but the standard library.
"""

import hashlib
import math
import os
from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
PAPER = (246, 241, 231)
INK = (17, 17, 17)
MUTED = (90, 84, 72)
RULE = (17, 17, 17)
ACCENT = (140, 29, 24)

FONT_DIRS = (
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
    "/usr/share/fonts/truetype/liberation",
)


def load_font(stem, size):
    """Find a TTF by stem in the usual font dirs; fall back to default."""
    for folder in FONT_DIRS:
        path = os.path.join(folder, stem)
        if os.path.isfile(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


SERIF_B = lambda s: load_font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: load_font("DejaVuSerif.ttf", s)
SANS_B = lambda s: load_font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: load_font("DejaVuSans.ttf", s)


def wrap(draw, text, font, width):
    """Greedy word wrap returning a list of lines that fit width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centre(draw, y, text, font, fill, box=(0, 1024)):
    """Draw text centred horizontally inside box at height y."""
    wide = draw.textlength(text, font=font)
    draw.text(((box[0] + box[1] - wide) / 2, y), text, font=font, fill=fill)


def star_points(cx, cy, outer, inner):
    """Points of a five-pointed star centred at (cx, cy)."""
    pts = []
    for i in range(10):
        radius = outer if i % 2 == 0 else inner
        angle = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return pts


def glyph_scales(draw, box, colour):
    """Simple scales-of-justice emblem inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    draw.line([(cx, y0 + 14), (cx, y1 - 16)], fill=colour, width=5)
    draw.line([(x0 + 14, y0 + 30), (x1 - 14, y0 + 30)], fill=colour, width=5)
    draw.ellipse([cx - 6, y0 + 8, cx + 6, y0 + 20], fill=colour)
    for side in (-1, 1):
        px = cx + side * 26
        draw.line([(px, y0 + 30), (px - 13, y0 + 52)], fill=colour, width=3)
        draw.line([(px, y0 + 30), (px + 13, y0 + 52)], fill=colour, width=3)
        draw.line([(px - 13, y0 + 52), (px + 13, y0 + 52)], fill=colour, width=3)


def glyph_star(draw, box, colour):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    draw.polygon(star_points(cx, cy, 30, 12), fill=colour)


def glyph_ring(draw, box, colour):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for i in range(12):
        angle = -math.pi / 2 + i * math.pi / 6
        px, py = cx + 26 * math.cos(angle), cy + 26 * math.sin(angle)
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=colour)


def glyph_arena(draw, box, colour):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 8
    draw.arc([x0 + 12, y0 + 8, x1 - 12, y1 - 8], start=180, end=360, fill=colour, width=5)
    draw.line([(x0 + 12, cy + 16), (x1 - 12, cy + 16)], fill=colour, width=5)
    for row, count in ((0, 5), (1, 4)):
        yy = y0 + 34 + row * 14
        for i in range(count):
            xx = cx + (i - (count - 1) / 2) * 13
            draw.ellipse([xx - 3, yy - 3, xx + 3, yy + 3], fill=colour)


def glyph_shirt(draw, box, colour):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    pts = [
        (cx - 16, y0 + 16), (cx - 34, y0 + 26), (cx - 24, y0 + 42),
        (cx - 24, y1 - 14), (cx + 24, y1 - 14), (cx + 24, y0 + 42),
        (cx + 34, y0 + 26), (cx + 16, y0 + 16), (cx, y0 + 26),
    ]
    draw.polygon(pts, fill=colour)


GLYPHS = {
    "scales": glyph_scales,
    "star": glyph_star,
    "ring": glyph_ring,
    "arena": glyph_arena,
    "shirt": glyph_shirt,
}


def paint_lead_panel(draw, x0, y0, x1, y1):
    """Dark panel with a rising market line for the lead story."""
    draw.rectangle([x0, y0, x1, y1], fill=(22, 39, 62))
    for gx in range(x0 + 40, x1, 40):
        draw.line([(gx, y0 + 12), (gx, y1 - 12)], fill=(38, 60, 88), width=1)
    for gy in range(y0 + 40, y1, 40):
        draw.line([(x0 + 12, gy), (x1 - 12, gy)], fill=(38, 60, 88), width=1)
    line = [
        (x0 + 24, y1 - 78), (x0 + 84, y1 - 108), (x0 + 128, y1 - 96),
        (x0 + 178, y1 - 138), (x0 + 224, y1 - 128), (x0 + 272, y1 - 178),
        (x0 + 304, y1 - 196),
    ]
    draw.line(line, fill=(74, 222, 128), width=6, joint="curve")
    tip = line[-1]
    draw.polygon(
        [(tip[0], tip[1] - 16), (tip[0] + 18, tip[1] + 2), (tip[0] - 2, tip[1] + 10)],
        fill=(74, 222, 128),
    )
    draw.text((x0 + 22, y0 + 16), "+31%", font=SANS_B(62), fill=(255, 255, 255))
    draw.text((x0 + 22, y0 + 88), "NVIDIA SHARES", font=SANS_B(17), fill=(148, 197, 255))
    draw.text(
        (x0 + 22, y1 - 40),
        "NASDAQ +6.5%  ·  S&P +4.7%",
        font=SANS_B(17),
        fill=(214, 226, 240),
    )


def paint_story_cell(draw, x, y, wide, story):
    """One grid cell: colour chip with glyph, kicker, headline, summary."""
    chip = story["chip"]
    draw.rectangle([x, y, x + 92, y + 92], fill=chip)
    GLYPHS[story["glyph"]](draw, (x, y, x + 92, y + 92), (255, 255, 255))
    tx, tw = x + 108, wide - 108
    draw.text((tx, y + 2), story["kicker"], font=SANS_B(15), fill=story["chip"])
    head = wrap(draw, story["headline"], SANS_B(25), tw)
    hy = y + 24
    for row in head[:2]:
        draw.text((tx, hy), row, font=SANS_B(25), fill=INK)
        hy += 29
    body = wrap(draw, story["summary"], SANS(18), tw)
    by = hy + 4
    for row in body[:3]:
        draw.text((tx, by), row, font=SANS(18), fill=MUTED)
        by += 22


STORIES = [
    {
        "kicker": "IRAN · HUMAN RIGHTS",
        "headline": "Singer flogged 74 times for show without hijab",
        "summary": "Parastoo Ahmadi lashed in Qom over a 2024 online concert; four band members punished too.",
        "chip": (140, 29, 24),
        "glyph": "scales",
    },
    {
        "kicker": "CHINA · ESPIONAGE",
        "headline": "Official sentenced to death for leaking secrets",
        "summary": "Beijing says the official sent 100 reports abroad, 35 of them state secrets.",
        "chip": (179, 84, 30),
        "glyph": "star",
    },
    {
        "kicker": "EUROPE · SANCTIONS",
        "headline": "EU unveils 22nd sanctions package on Russia",
        "summary": "Brussels targets banks, crypto platforms and Russian teams under the EU flag.",
        "chip": (31, 58, 147),
        "glyph": "ring",
    },
    {
        "kicker": "BRITAIN · MANCHESTER",
        "headline": "12,000 flee arena after mystery substance",
        "summary": "Don Toliver concert evacuated; 89 treated, one in hospital. London show postponed.",
        "chip": (15, 118, 110),
        "glyph": "arena",
    },
]


def build():
    img = Image.new("RGB", CANVAS, PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead.
    draw.rectangle([36, 28, 988, 30], fill=RULE)
    centre(draw, 42, "THE WORLD", SERIF_B(88), INK)
    centre(draw, 140, "TUESDAY, 24 NOVEMBER 2026", SANS_B(28), INK)
    centre(draw, 172, "SIX STORIES THAT DEFINED THE DAY", SANS(15), MUTED)
    draw.rectangle([36, 196, 988, 198], fill=RULE)
    draw.rectangle([36, 202, 988, 203], fill=RULE)

    # Lead story: text left, market panel right.
    draw.text((36, 222), "UNITED STATES · BUSINESS", font=SANS_B(19), fill=ACCENT)
    lead_head = ["HUANG IS BACK", "AT NVIDIA"]
    hy = 248
    for row in lead_head:
        draw.text((36, hy), row, font=SERIF_B(58), fill=INK)
        hy += 64
    deck = wrap(
        draw,
        "Board reinstates the ousted chief after a White House push. "
        "Shares soar 31% — the biggest one-day gain on record — "
        "and lift the Nasdaq 6.5%.",
        SANS(23),
        592,
    )
    dy = 386
    for row in deck:
        draw.text((36, dy), row, font=SANS(23), fill=(44, 40, 34))
        dy += 30
    paint_lead_panel(draw, 660, 216, 988, 486)

    # Rule, then the four-cell grid.
    draw.rectangle([36, 506, 988, 508], fill=RULE)
    positions = [(36, 526, 458), (530, 526, 458), (36, 692, 458), (530, 692, 458)]
    for (cx, cy, cw), story in zip(positions, STORIES):
        paint_story_cell(draw, cx, cy, cw, story)

    # Bottom strip: the sixth story, full width.
    draw.rectangle([36, 856, 988, 858], fill=RULE)
    draw.rectangle([36, 872, 128, 964], fill=(146, 64, 14))
    GLYPHS["shirt"](draw, (36, 872, 128, 964), (255, 255, 255))
    draw.text((144, 874), "BANGLADESH · LABOUR", font=SANS_B(15), fill=(146, 64, 14))
    draw.text(
        (144, 896),
        "Garment workers reject pay offer as too low",
        font=SANS_B(28),
        fill=INK,
    )
    strip = wrap(
        draw,
        "Wage-board talks stall as the owners' offer falls far short of the "
        "30,000-taka demand; strikes go on.",
        SANS(19),
        844,
    )
    sy = 930
    for row in strip[:2]:
        draw.text((144, sy), row, font=SANS(19), fill=MUTED)
        sy += 24

    # Ticker bar.
    draw.rectangle([36, 978, 988, 1018], fill=(17, 17, 17))
    ticker = (
        "ALSO TODAY:  Seoul minister quits over AI cheating   •   "
        "O'Hare ground stop   •   "
        "Kyiv confirms corvette sinking"
    )
    size = 17
    while draw.textlength(ticker, font=SANS_B(size)) > 936 and size > 13:
        size -= 1
    draw.text((52, 978 + (40 - size) / 2 - 4), ticker, font=SANS_B(size), fill=(255, 255, 255))

    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "entry.png")
    picture = build()
    picture.save(target, format="PNG")
    raw = open(target, "rb").read()
    print("entry.png", len(raw), "bytes,", picture.size[0], "x", picture.size[1])
    print("sha256", hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()
