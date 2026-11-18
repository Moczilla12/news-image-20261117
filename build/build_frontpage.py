#!/usr/bin/env python3
"""Render the make.fun news-image-20261117 front page (1024x1024 JPEG).

Newspaper front page for Tuesday 17 November 2026: 40 verified stories,
masthead date, lead on the US strike on Qeshm Island, three secondary leads,
a medium grid, a world map with story dots, and a briefs column.
Everything is drawn with PIL from scratch; output is deterministic.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

OUT_JPG = "/home/hatch/workspace/makefun/news-image-20261117/front-page.jpg"
GEO = "/tmp/countries.geo.json"

W, H = 1024, 1024
PAPER = (247, 242, 230)
INK = (24, 24, 24)
RED = (176, 32, 28)
BLUE = (28, 74, 116)
GREEN = (44, 120, 68)
ORANGE = (214, 110, 24)
PURPLE = (112, 56, 150)
BROWN = (146, 106, 38)
TEAL = (0, 122, 122)
GREY = (104, 104, 104)
SEA = (206, 226, 235)
LAND = (233, 221, 193)
COAST = (182, 164, 120)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


F_KICK = font("DejaVuSans-Bold.ttf", 12)
F_DATE = font("DejaVuSerif-Bold.ttf", 40)
F_TAG = font("DejaVuSans.ttf", 11)
F_LEAD_KICK = font("DejaVuSans-Bold.ttf", 11)
F_LEAD_HEAD = font("DejaVuSerif-Bold.ttf", 34)
F_LEAD_DECK = font("DejaVuSans.ttf", 13)
F_LEAD_NOTE = font("DejaVuSans.ttf", 12)
F_SUB_KICK = font("DejaVuSans-Bold.ttf", 10)
F_SUB_HEAD = font("DejaVuSerif-Bold.ttf", 16)
F_SUB_DECK = font("DejaVuSans.ttf", 11)
F_MED_KICK = font("DejaVuSans-Bold.ttf", 9)
F_MED_HEAD = font("DejaVuSerif-Bold.ttf", 13)
F_MED_FACT = font("DejaVuSans.ttf", 10)
F_SEC = font("DejaVuSans-Bold.ttf", 13)
F_BRIEF = font("DejaVuSans.ttf", 10)
F_FOOT = font("DejaVuSans.ttf", 9)
F_MAP_LAB = font("DejaVuSans-Bold.ttf", 9)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, f, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, lines, f, fill=INK, leading=None):
    """Draw lines top-down; returns the y just below the last line."""
    if leading is None:
        leading = int(f.size * 1.28)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def num_badge(cx, cy, r, n, fill=RED):
    """Numbered circle badge."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    s = str(n)
    f = font("DejaVuSans-Bold.ttf", max(8, int(r * 1.05)))
    tw = d.textlength(s, font=f)
    d.text((cx - tw / 2, cy - f.size / 2 - 1), s, font=f, fill=(255, 255, 255))


def hline(x0, x1, y, width=1, fill=INK):
    d.rectangle([x0, y, x1, y + width - 1], fill=fill)


# ---------------------------------------------------------------- header
d.text((28, 10), "THE WORLD'S NEWS IN ONE PICTURE", font=F_KICK, fill=RED)
right = "40 STORIES  ·  6 CONTINENTS"
d.text((W - 28 - d.textlength(right, font=F_KICK), 10), right, font=F_KICK, fill=INK)
d.text((28, 28), "TUESDAY 17 NOVEMBER 2026", font=F_DATE, fill=INK)
d.text((28, 72), "The day in one image — every story happened on 17 November 2026",
       font=F_TAG, fill=GREY)
hline(28, W - 28, 92, 2)
hline(28, W - 28, 96, 1)

# ---------------------------------------------------------------- lead story
# Left: kicker + headline + deck. Right: schematic of the Strait of Hormuz.
d.text((28, 106), "MIDDLE EAST  ·  US–IRAN WAR — DAY 264", font=F_LEAD_KICK, fill=RED)
head_lines = wrap("US jets strike Iran's Qeshm Island", F_LEAD_HEAD, 560)
y = text_block(28, 124, head_lines, F_LEAD_HEAD, leading=40)
deck = wrap("US fighter jets hit an IRGC missile launch site on Qeshm Island "
            "in the Strait of Hormuz, on day 264 of the US–Iran war.",
            F_LEAD_DECK, 560)
y = text_block(28, y + 6, deck, F_LEAD_DECK, leading=17)
note = wrap("Tehran's drones also hit US bases in Bahrain and Kuwait, and a "
            "fourth tanker burned after a mine strike in the strait.",
            F_LEAD_NOTE, 560)
text_block(28, y + 8, note, F_LEAD_NOTE, fill=(70, 70, 70), leading=16)

# Lead illustration: schematic Strait of Hormuz (x 612..996, y 106..300).
ix0, iy0, ix1, iy1 = 612, 106, 996, 300
d.rectangle([ix0, iy0, ix1, iy1], fill=SEA, outline=(150, 165, 170))
# Iran coast (top) and Arabian Peninsula (bottom)
d.polygon([(ix0, iy0), (ix1, iy0), (ix1, iy0 + 52), (ix0 + 250, iy0 + 62),
           (ix0 + 180, iy0 + 40), (ix0, iy0 + 46)], fill=LAND, outline=COAST)
d.polygon([(ix0, iy1), (ix1, iy1), (ix1, iy1 - 58), (ix0 + 300, iy1 - 44),
           (ix0 + 200, iy1 - 60), (ix0, iy1 - 48)], fill=LAND, outline=COAST)
# Qeshm Island (long, narrow, in the strait)
d.polygon([(ix0 + 150, iy0 + 118), (ix0 + 300, iy0 + 96), (ix0 + 330, iy0 + 112),
           (ix0 + 170, iy0 + 136)], fill=(214, 196, 150), outline=(120, 100, 60))
# Strait label + island label
d.text((ix0 + 14, iy0 + 150), "STRAIT OF HORMUZ", font=F_MAP_LAB, fill=(40, 70, 90))
d.text((ix0 + 176, iy0 + 86), "QESHM ISLAND", font=F_MAP_LAB, fill=(90, 70, 30))
d.text((ix0 + 14, iy0 + 8), "IRAN", font=F_MAP_LAB, fill=(90, 70, 30))
d.text((ix0 + 14, iy1 - 22), "ARABIAN PENINSULA", font=F_MAP_LAB, fill=(90, 70, 30))
# Jet (simple delta shape) flying over the island
jx, jy = ix0 + 240, iy0 + 62
d.polygon([(jx - 26, jy + 6), (jx + 18, jy), (jx - 26, jy - 6)], fill=(40, 40, 40))
d.polygon([(jx - 6, jy), (jx - 2, jy - 14), (jx + 4, jy)], fill=(60, 60, 60))
# Target marker on the island
tx, ty = ix0 + 250, iy0 + 112
d.ellipse([tx - 9, ty - 9, tx + 9, ty + 9], outline=RED, width=2)
d.line([tx - 13, ty, tx + 13, ty], fill=RED, width=2)
d.line([tx, ty - 13, tx, ty + 13], fill=RED, width=2)
d.text((ix0 + 268, iy0 + 100), "missile site hit", font=F_MAP_LAB, fill=RED)
hline(28, W - 28, 312, 1)

# ---------------------------------------------------------------- three secondary leads
SUBS = [
    dict(n=11, kick="EUROPE  ·  UKRAINE WAR", col=BLUE,
         head="Kerch Bridge span falls into strait",
         deck="Ukrainian drones and missiles brought down a 227-metre road arch, "
              "cutting Russia's only direct road link to Crimea.",
         art="bridge"),
    dict(n=18, kick="AFRICA  ·  HEALTH", col=GREEN,
         head="Ebola passes 11,300 cases in Congo",
         deck="DR Congo outbreak reached 11,376 cases and 5,568 deaths, "
              "more than doubling in three months.",
         art="virus"),
    dict(n=34, kick="SCIENCE  ·  SPACE", col=PURPLE,
         head="Vulcan rocket fails, 40 satellites lost",
         deck="ULA's Vulcan failed shortly after its 15 November launch, "
              "destroying 40 Amazon Leo satellites.",
         art="rocket"),
]


def draw_bridge(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 228))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(110, 150, 185))
    # deck, broken in the middle: left span stands, right span has fallen
    d.rectangle([x + 8, y + 52, x + w // 2 - 14, y + 60], fill=(60, 60, 60))
    d.line([x + w // 2 - 14, y + 60, x + w // 2 + 26, y + h - 30], fill=(60, 60, 60), width=6)
    d.rectangle([x + w // 2 + 26, y + h - 34, x + w - 8, y + h - 26], fill=(90, 90, 90))
    # towers
    for tx in (x + 60, x + w - 70):
        d.rectangle([tx, y + 12, tx + 8, y + 60], fill=(50, 50, 50))
        d.line([tx + 4, y + 12, tx + 4, y + 52], fill=(200, 200, 200), width=1)
    d.text((x + 10, y + 6), "227-m arch down", font=F_MAP_LAB, fill=(30, 30, 30))


def draw_virus(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    cx, cy = x + w // 2, y + h // 2 - 4
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        x1 = cx + 26 * math.cos(a)
        y1 = cy + 26 * math.sin(a)
        x2 = cx + 38 * math.cos(a)
        y2 = cy + 38 * math.sin(a)
        d.line([x1, y1, x2, y2], fill=(120, 90, 40), width=3)
        d.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=(120, 90, 40))
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(178, 120, 60))
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(140, 80, 30))
    d.rounded_rectangle([x + 10, y + h - 22, x + w - 10, y + h - 4], radius=3, fill=(255, 255, 255))
    d.text((x + 16, y + h - 19), "11,376 cases · 5,568 deaths", font=F_MAP_LAB, fill=RED)


def draw_rocket(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 26, 52))
    cx = x + w // 2
    # rocket body, tilted, with smoke trail
    d.polygon([(cx - 8, y + 18), (cx + 8, y + 18), (cx + 6, y + 62), (cx - 6, y + 62)],
              fill=(235, 235, 235))
    d.polygon([(cx - 8, y + 18), (cx, y + 2), (cx + 8, y + 18)], fill=RED)
    d.polygon([(cx - 16, y + 62), (cx - 16, y + 74), (cx - 6, y + 62)], fill=(200, 200, 200))
    d.polygon([(cx + 16, y + 62), (cx + 16, y + 74), (cx + 6, y + 62)], fill=(200, 200, 200))
    # flame + smoke
    d.polygon([(cx - 6, y + 74), (cx, y + 96), (cx + 6, y + 74)], fill=(255, 150, 40))
    for sx, sy, r in [(cx - 30, y + 92, 10), (cx + 28, y + 100, 12), (cx, y + 108, 9)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(200, 200, 200))
    d.text((x + 10, y + 6), "40 satellites lost", font=F_MAP_LAB, fill=(255, 255, 255))


ART = {"bridge": draw_bridge, "virus": draw_virus, "rocket": draw_rocket}
SUB_W = 312
for i, s in enumerate(SUBS):
    x = 28 + i * (SUB_W + 8)
    y = 322
    ART[s["art"]](x, y, SUB_W, 72)
    ky = y + 80
    num_badge(x + 9, ky + 7, 9, s["n"], fill=s["col"])
    d.text((x + 24, ky), s["kick"], font=F_SUB_KICK, fill=s["col"])
    hy = ky + 17
    hl = wrap(s["head"], F_SUB_HEAD, SUB_W)
    hy = text_block(x, hy, hl, F_SUB_HEAD, leading=19)
    dl = wrap(s["deck"], F_SUB_DECK, SUB_W)
    text_block(x, hy + 3, dl, F_SUB_DECK, leading=14)
hline(28, W - 28, 486, 1)

# ---------------------------------------------------------------- medium grid (12 stories)
MED = [
    (2, "MIDDLE EAST", "Iran drones target US base in Bahrain",
     "Drones hit a US radar in Bahrain; no casualties.", BLUE),
    (4, "MIDDLE EAST", "Fourth Hormuz tanker burns after mine strike",
     "Fourth tanker burned; Oman evacuated 24 crew.", RED),
    (5, "GAZA", "Gaza winter rains flood shelters",
     "Winter rain flooded tents; 1.7m displaced.", BLUE),
    (12, "UKRAINE", "Russia hits Kyiv's Dnipro bridges",
     "Russia hit Kyiv's Dnipro bridges late Monday.", BLUE),
    (19, "AFRICA", "Ebola reaches Kenya and Nigeria",
     "Kenya: nine cases, two deaths; Nigeria: one case.", GREEN),
    (24, "ASIA", "Trump opens Asia trip in Manila",
     "Trump arrived for a Quad summit in Manila.", ORANGE),
    (28, "AMERICAS", "US loses measles-free status",
     "US lost measles-free status after 25 years.", RED),
    (29, "AMERICAS", "NSA network goes down in outage wave",
     "NSA network went offline amid a US outage wave.", RED),
    (33, "CLIMATE", "COP31 draft deal under fire",
     "Draft drew fire over fossil fuels, $120bn goal.", TEAL),
    (35, "SPACE", "Voyager 1 reaches one light-day",
     "Voyager 1 is the first object one light-day away.", PURPLE),
    (39, "TECH", "Nvidia posts record revenue amid scandal",
     "Record revenue amid scandal around ex-chief Huang.", BROWN),
    (40, "TECH", "US widens chip-export scrutiny",
     "US widened chip controls to SE Asia and Brazil.", BROWN),
]
CELL_W, CELL_H = 312, 56
for i, (n, sec, head, fact, col) in enumerate(MED):
    cx = 28 + (i % 3) * (CELL_W + 8)
    cy = 496 + (i // 3) * CELL_H
    num_badge(cx + 9, cy + 8, 8, n, fill=col)
    d.text((cx + 24, cy + 1), sec, font=F_MED_KICK, fill=col)
    hl = wrap(head, F_MED_HEAD, CELL_W - 24)
    hy = text_block(cx + 24, cy + 14, hl[:2], F_MED_HEAD, leading=15)
    fl = wrap(fact, F_MED_FACT, CELL_W - 24)
    text_block(cx + 24, hy + 1, fl[:1], F_MED_FACT, fill=(70, 70, 70), leading=12)
hline(28, W - 28, 724, 1)

# ---------------------------------------------------------------- bottom: map + briefs
d.text((28, 734), "WHERE IT HAPPENED", font=F_SEC, fill=INK)
d.text((28, 752), "numbers = stories 1–40 · dots = briefs", font=F_TAG, fill=GREY)
MAP = (28, 772, 500, 978)
d.rectangle(MAP, fill=SEA, outline=(170, 180, 170))

geo = json.load(open(GEO))


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    lat = max(-60.0, min(85.0, lat))
    lon = max(-180.0, min(180.0, lon))
    fx = (lon + 180.0) / 360.0
    fy = (85.0 - lat) / 145.0
    return (x0 + fx * (x1 - x0), y0 + fy * (y1 - y0))


def draw_poly(coords, box):
    pts = [project(lon, lat, box) for lon, lat in coords]
    if len(pts) >= 3:
        d.polygon(pts, fill=LAND, outline=COAST)


for feat in geo["features"]:
    if feat.get("id") == "ATA":
        continue
    g = feat["geometry"]
    if g["type"] == "Polygon":
        for ring in g["coordinates"]:
            draw_poly(ring, MAP)
    elif g["type"] == "MultiPolygon":
        for poly in g["coordinates"]:
            for ring in poly:
                draw_poly(ring, MAP)

REG = {"americas": RED, "europe": BLUE, "mideast": ORANGE,
       "asia": GREEN, "africa": BROWN, "oceania": TEAL}
# numbered dots for the lead, secondary and medium stories
NUMBERED = [
    (1, 56.5, 26.8, "mideast"), (11, 36.5, 45.3, "europe"),
    (18, 23.0, -3.0, "africa"), (34, -80.6, 28.4, "americas"),
    (2, 50.5, 26.2, "mideast"), (4, 56.0, 26.5, "mideast"),
    (5, 34.5, 31.5, "mideast"), (12, 30.5, 50.4, "europe"),
    (19, 37.0, 0.0, "africa"), (24, 121.0, 14.6, "asia"),
    (28, -97.0, 38.0, "americas"), (29, -76.7, 39.1, "americas"),
    (33, 30.7, 36.9, "europe"), (35, -150.0, 0.0, "americas"),
    (39, -122.0, 37.4, "americas"), (40, 103.0, 1.3, "asia"),
]
OFFSETS = {1: (16, -12), 2: (-16, 10), 4: (14, 12), 5: (16, -10),
           12: (-14, -12), 29: (14, -12), 39: (-14, 10)}
for n, lon, lat, reg in NUMBERED:
    x, y = project(lon, lat, MAP)
    dx, dy = OFFSETS.get(n, (0, 0))
    if dx or dy:
        d.line([x, y, x + dx, y + dy], fill=(90, 90, 90), width=1)
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=REG[reg])
        x, y = x + dx, y + dy
    num_badge(x, y, 8, n, fill=REG[reg])
# plain dots for the briefs
BRIEF_DOTS = [
    (47.7, 29.3, "mideast"), (35.5, 33.3, "mideast"), (45.0, 24.0, "mideast"),
    (-77.0, 38.9, "americas"), (35.5, 31.9, "mideast"), (133.0, 36.3, "asia"),
    (28.8, 47.0, "europe"), (5.7, 58.9, "europe"), (30.0, -2.0, "africa"),
    (2.35, 48.85, "europe"), (31.0, -29.0, "africa"), (-9.2, 11.4, "africa"),
    (32.5, -25.9, "africa"), (6.1, 46.2, "europe"), (139.7, 35.7, "asia"),
    (114.0, 12.0, "asia"), (-74.0, 40.7, "americas"), (-62.0, -4.0, "americas"),
    (-84.0, 9.7, "americas"), (172.0, -41.0, "oceania"),
]
for lon, lat, reg in BRIEF_DOTS:
    x, y = project(lon, lat, MAP)
    d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=REG[reg], outline=(255, 255, 255))

# briefs list (right side, two columns)
BX = 524
d.text((BX, 734), "ALSO ON 17 NOVEMBER", font=F_SEC, fill=INK)
BRIEFS = [
    (3, "Kuwait reports Iranian drone attack"),
    (6, "West urges Israel to open Gaza"),
    (7, "Israel strikes southern Lebanon"),
    (8, "Houthis hit Saudi pipeline"),
    (9, "Trump weighs dirty-bomb report"),
    (10, "Settlers shoot woman dead"),
    (13, "Japan scrambles jets at Russians"),
    (14, "Russian drones cross Moldova"),
    (15, "Equinor hit by cyberattack"),
    (16, "Five EU states plan Rwanda hub"),
    (17, "Depardieu admits assault charge"),
    (20, "17 killed in South Africa shootings"),
    (21, "Guinea arrests 1,200 miners"),
    (22, "Mozambique leader goes on trial"),
    (23, "ILO re-elects Houngbo unopposed"),
    (25, "Modi joins ASEAN-India summit"),
    (26, "India and Japan hold 2+2 talks"),
    (27, "China builds S. China Sea runway"),
    (30, "Wall Street falls on tech slide"),
    (31, "Isolated Awá filmed in Amazon"),
    (32, "Costa Rica journalist murdered"),
    (36, "Euclid maps 900 million galaxies"),
    (37, "El Niño nears 1997 record"),
    (38, "NZ superconductor back from space"),
]
for i, (n, txt) in enumerate(BRIEFS):
    col = i // 12
    row = i % 12
    x = BX + col * 236
    y = 760 + row * 18
    num_badge(x + 8, y + 7, 8, n, fill=GREEN)
    d.text((x + 22, y), txt, font=F_BRIEF, fill=INK)

# ---------------------------------------------------------------- footer
hline(28, W - 28, 990, 1)
d.text((28, 996), "Every story happened or was first reported on Tuesday 17 November 2026. "
                  "Disputed claims are attributed.", font=F_FOOT, fill=GREY)
src = "Sources: AP · Reuters · AFP · BBC · Al Jazeera · DW · CNBC · UN News"
d.text((W - 28 - d.textlength(src, font=F_FOOT), 996), src, font=F_FOOT, fill=GREY)

img.save(OUT_JPG, "JPEG", quality=88)
print("saved", OUT_JPG)
print("bytes:", os.path.getsize(OUT_JPG))
print("size:", img.size)
