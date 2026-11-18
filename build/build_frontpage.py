#!/usr/bin/env python3
"""Render the make.fun news-image-20261117 front page, v2 (1024x1024 JPEG).

Newspaper front page for Tuesday 17 November 2026: 50 verified stories,
masthead date, lead on the US strike on Qeshm Island, three secondary leads,
a 15-story medium grid, a world map with story dots, and a 31-brief column.
Everything is drawn with PIL from scratch; output is deterministic.
"""
import json
import math
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
F_DATE = font("DejaVuSerif-Bold.ttf", 38)
F_TAG = font("DejaVuSans.ttf", 11)
F_LEAD_KICK = font("DejaVuSans-Bold.ttf", 11)
F_LEAD_HEAD = font("DejaVuSerif-Bold.ttf", 32)
F_LEAD_DECK = font("DejaVuSans.ttf", 13)
F_LEAD_NOTE = font("DejaVuSans.ttf", 12)
F_SUB_KICK = font("DejaVuSans-Bold.ttf", 10)
F_SUB_HEAD = font("DejaVuSerif-Bold.ttf", 15)
F_SUB_DECK = font("DejaVuSans.ttf", 11)
F_MED_KICK = font("DejaVuSans-Bold.ttf", 9)
F_MED_HEAD = font("DejaVuSerif-Bold.ttf", 12)
F_MED_FACT = font("DejaVuSans.ttf", 10)
F_SEC = font("DejaVuSans-Bold.ttf", 13)
F_BRIEF = font("DejaVuSans.ttf", 9)
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
d.text((28, 8), "THE WORLD'S NEWS IN ONE PICTURE", font=F_KICK, fill=RED)
right = "50 STORIES  ·  6 CONTINENTS"
d.text((W - 28 - d.textlength(right, font=F_KICK), 8), right, font=F_KICK, fill=INK)
d.text((28, 26), "TUESDAY 17 NOVEMBER 2026", font=F_DATE, fill=INK)
d.text((28, 68), "The day in one image — every story happened on 17 November 2026",
       font=F_TAG, fill=GREY)
hline(28, W - 28, 88, 2)
hline(28, W - 28, 92, 1)

# ---------------------------------------------------------------- lead story
d.text((28, 100), "MIDDLE EAST  ·  US–IRAN WAR — DAY 264", font=F_LEAD_KICK, fill=RED)
head_lines = wrap("US jets strike Iran's Qeshm Island", F_LEAD_HEAD, 560)
y = text_block(28, 118, head_lines, F_LEAD_HEAD, leading=38)
deck = wrap("US fighter jets hit an IRGC missile launch site on Qeshm Island "
            "in the Strait of Hormuz, on day 264 of the US–Iran war.",
            F_LEAD_DECK, 560)
y = text_block(28, y + 5, deck, F_LEAD_DECK, leading=17)
note = wrap("Tehran's drones also hit US bases in Bahrain and Kuwait, and a "
            "fourth tanker burned after a mine strike in the strait.",
            F_LEAD_NOTE, 560)
text_block(28, y + 7, note, F_LEAD_NOTE, fill=(70, 70, 70), leading=16)

# Lead illustration: schematic Strait of Hormuz (x 612..996, y 100..292).
ix0, iy0, ix1, iy1 = 612, 100, 996, 292
d.rectangle([ix0, iy0, ix1, iy1], fill=SEA, outline=(150, 165, 170))
d.polygon([(ix0, iy0), (ix1, iy0), (ix1, iy0 + 50), (ix0 + 250, iy0 + 60),
           (ix0 + 180, iy0 + 38), (ix0, iy0 + 44)], fill=LAND, outline=COAST)
d.polygon([(ix0, iy1), (ix1, iy1), (ix1, iy1 - 56), (ix0 + 300, iy1 - 42),
           (ix0 + 200, iy1 - 58), (ix0, iy1 - 46)], fill=LAND, outline=COAST)
d.polygon([(ix0 + 150, iy0 + 112), (ix0 + 300, iy0 + 90), (ix0 + 330, iy0 + 106),
           (ix0 + 170, iy0 + 130)], fill=(214, 196, 150), outline=(120, 100, 60))
d.text((ix0 + 14, iy0 + 144), "STRAIT OF HORMUZ", font=F_MAP_LAB, fill=(40, 70, 90))
d.text((ix0 + 176, iy0 + 80), "QESHM ISLAND", font=F_MAP_LAB, fill=(90, 70, 30))
d.text((ix0 + 14, iy0 + 8), "IRAN", font=F_MAP_LAB, fill=(90, 70, 30))
d.text((ix0 + 14, iy1 - 22), "ARABIAN PENINSULA", font=F_MAP_LAB, fill=(90, 70, 30))
jx, jy = ix0 + 240, iy0 + 58
d.polygon([(jx - 26, jy + 6), (jx + 18, jy), (jx - 26, jy - 6)], fill=(40, 40, 40))
d.polygon([(jx - 6, jy), (jx - 2, jy - 14), (jx + 4, jy)], fill=(60, 60, 60))
tx, ty = ix0 + 250, iy0 + 106
d.ellipse([tx - 9, ty - 9, tx + 9, ty + 9], outline=RED, width=2)
d.line([tx - 13, ty, tx + 13, ty], fill=RED, width=2)
d.line([tx, ty - 13, tx, ty + 13], fill=RED, width=2)
d.text((ix0 + 268, iy0 + 94), "missile site hit", font=F_MAP_LAB, fill=RED)
hline(28, W - 28, 300, 1)

# ---------------------------------------------------------------- three secondary leads
SUBS = [
    dict(n=12, kick="EUROPE  ·  UKRAINE WAR", col=BLUE,
         head="Kerch Bridge span falls into strait",
         deck="Ukrainian drones and missiles brought down a 227-metre road arch, "
              "cutting Russia's only direct road link to Crimea.",
         art="bridge"),
    dict(n=22, kick="AFRICA  ·  HEALTH", col=GREEN,
         head="Ebola passes 11,300 cases in Congo",
         deck="DR Congo outbreak reached 11,376 cases and 5,568 deaths, "
              "more than doubling in three months.",
         art="virus"),
    dict(n=41, kick="SCIENCE  ·  SPACE", col=PURPLE,
         head="Vulcan rocket fails, 40 satellites lost",
         deck="ULA's Vulcan failed shortly after its 15 November launch, "
              "destroying 40 Amazon Leo satellites.",
         art="rocket"),
]


def draw_bridge(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 228))
    d.rectangle([x, y + h - 28, x + w, y + h], fill=(110, 150, 185))
    d.rectangle([x + 8, y + 48, x + w // 2 - 14, y + 56], fill=(60, 60, 60))
    d.line([x + w // 2 - 14, y + 56, x + w // 2 + 26, y + h - 28], fill=(60, 60, 60), width=6)
    d.rectangle([x + w // 2 + 26, y + h - 32, x + w - 8, y + h - 24], fill=(90, 90, 90))
    for tx in (x + 60, x + w - 70):
        d.rectangle([tx, y + 12, tx + 8, y + 56], fill=(50, 50, 50))
        d.line([tx + 4, y + 12, tx + 4, y + 48], fill=(200, 200, 200), width=1)
    d.text((x + 10, y + 6), "227-m arch down", font=F_MAP_LAB, fill=(30, 30, 30))


def draw_virus(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    cx, cy = x + w // 2, y + h // 2
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        x1 = cx + 20 * math.cos(a)
        y1 = cy + 20 * math.sin(a)
        x2 = cx + 28 * math.cos(a)
        y2 = cy + 28 * math.sin(a)
        d.line([x1, y1, x2, y2], fill=(120, 90, 40), width=3)
        d.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=(120, 90, 40))
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(178, 120, 60))
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(140, 80, 30))
    d.rounded_rectangle([x + 10, y + h - 22, x + w - 10, y + h - 4], radius=3, fill=(255, 255, 255))
    d.text((x + 16, y + h - 19), "11,376 cases · 5,568 deaths", font=F_MAP_LAB, fill=RED)


def draw_rocket(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 26, 52))
    cx = x + w // 2
    # Rocket kept fully inside the art box (h=64): nose, body, fins, flame.
    d.polygon([(cx - 8, y + 14), (cx, y + 2), (cx + 8, y + 14)], fill=RED)
    d.polygon([(cx - 8, y + 14), (cx + 8, y + 14), (cx + 6, y + 44), (cx - 6, y + 44)],
              fill=(235, 235, 235))
    d.polygon([(cx - 14, y + 44), (cx - 14, y + 52), (cx - 6, y + 44)], fill=(200, 200, 200))
    d.polygon([(cx + 14, y + 44), (cx + 14, y + 52), (cx + 6, y + 44)], fill=(200, 200, 200))
    d.polygon([(cx - 5, y + 52), (cx, y + 62), (cx + 5, y + 52)], fill=(255, 150, 40))
    d.text((x + 10, y + 6), "40 satellites lost", font=F_MAP_LAB, fill=(255, 255, 255))


ART = {"bridge": draw_bridge, "virus": draw_virus, "rocket": draw_rocket}
SUB_W = 312
for i, s in enumerate(SUBS):
    x = 28 + i * (SUB_W + 8)
    y = 310
    ART[s["art"]](x, y, SUB_W, 64)
    ky = y + 72
    num_badge(x + 9, ky + 7, 9, s["n"], fill=s["col"])
    d.text((x + 24, ky), s["kick"], font=F_SUB_KICK, fill=s["col"])
    hy = ky + 16
    hl = wrap(s["head"], F_SUB_HEAD, SUB_W)
    hy = text_block(x, hy, hl, F_SUB_HEAD, leading=18)
    dl = wrap(s["deck"], F_SUB_DECK, SUB_W)
    text_block(x, hy + 2, dl, F_SUB_DECK, leading=14)
hline(28, W - 28, 458, 1)

# ---------------------------------------------------------------- medium grid (15 stories, 3 cols x 5 rows)
MED = [
    (2, "MIDDLE EAST", "Iran drones target US base in Bahrain",
     "Drones hit a US radar in Bahrain; no casualties.", BLUE),
    (4, "MIDDLE EAST", "Fourth Hormuz tanker burns",
     "Hit a naval mine; Oman evacuated 24 crew.", RED),
    (5, "GAZA", "Gaza winter rains flood shelters",
     "Winter rain flooded tents; 1.7m displaced.", BLUE),
    (13, "UKRAINE", "Russia hits Kyiv's Dnipro bridges",
     "Russia hit Kyiv's Dnipro bridges late Monday.", BLUE),
    (17, "EUROPE", "Deutsche Bank leak exposes oligarchs",
     "Leak of 15M files; shares fell 6%+ on Tuesday.", BLUE),
    (18, "EUROPE", "France hit by nationwide wage protests",
     "146,000 marched across France for higher wages.", BLUE),
    (23, "AFRICA", "Ebola reaches Kenya and Nigeria",
     "Kenya: nine cases, two deaths; Nigeria: one case.", GREEN),
    (28, "ASIA", "Trump opens Asia trip in Manila",
     "Trump arrived for a Quad summit in Manila.", ORANGE),
    (35, "AMERICAS", "US loses measles-free status",
     "US lost measles-free status after 25 years.", RED),
    (36, "AMERICAS", "NSA network goes down in outage wave",
     "NSA network went offline amid a US outage wave.", RED),
    (40, "CLIMATE", "COP31 draft deal under fire",
     "Draft drew fire over fossil fuels, $120bn goal.", TEAL),
    (42, "SPACE", "Voyager 1 reaches one light-day",
     "Voyager 1 is the first object one light-day away.", PURPLE),
    (48, "TECH", "Nvidia posts record revenue amid scandal",
     "Record revenue amid scandal around ex-chief Huang.", BROWN),
    (49, "TECH", "US widens chip-export scrutiny",
     "US widened chip controls to SE Asia and Brazil.", BROWN),
    (39, "SPORT", "Brazil thrash Singapore 7–0",
     "Vinícius nets a hat-trick inside 21 minutes.", GREEN),
]
CELL_W, CELL_H = 312, 48
for i, (n, sec, head, fact, col) in enumerate(MED):
    cx = 28 + (i % 3) * (CELL_W + 8)
    cy = 468 + (i // 3) * CELL_H
    num_badge(cx + 9, cy + 7, 8, n, fill=col)
    d.text((cx + 24, cy + 1), sec, font=F_MED_KICK, fill=col)
    hl = wrap(head, F_MED_HEAD, CELL_W - 24)
    hy = text_block(cx + 24, cy + 13, hl[:2], F_MED_HEAD, leading=14)
    fl = wrap(fact, F_MED_FACT, CELL_W - 24)
    text_block(cx + 24, hy + 1, fl[:1], F_MED_FACT, fill=(70, 70, 70), leading=12)
hline(28, W - 28, 712, 1)

# ---------------------------------------------------------------- bottom: map + briefs
d.text((28, 722), "WHERE IT HAPPENED", font=F_SEC, fill=INK)
d.text((28, 740), "numbers = stories 1–50 · dots = briefs", font=F_TAG, fill=GREY)
MAP = (28, 760, 500, 962)
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
NUMBERED = [
    (1, 56.5, 26.8, "mideast"), (12, 36.5, 45.3, "europe"),
    (22, 23.0, -3.0, "africa"), (41, -80.6, 28.4, "americas"),
    (2, 50.5, 26.2, "mideast"), (4, 56.0, 26.5, "mideast"),
    (5, 34.5, 31.5, "mideast"), (13, 30.5, 50.4, "europe"),
    (17, 8.7, 50.1, "europe"), (18, 2.35, 48.85, "europe"),
    (23, 37.0, 0.0, "africa"), (28, 121.0, 14.6, "asia"),
    (35, -97.0, 38.0, "americas"), (36, -76.7, 39.1, "americas"),
    (40, 30.7, 36.9, "europe"), (42, -150.0, 0.0, "americas"),
    (48, -122.0, 37.4, "americas"), (49, 103.0, 1.3, "asia"),
    (39, -52.0, -10.0, "americas"),
]
OFFSETS = {1: (16, -12), 2: (-16, 10), 4: (14, 12), 5: (16, -10),
           12: (-14, -12), 13: (14, -12), 17: (-14, 10), 18: (14, 10),
           40: (14, 12), 36: (14, -12), 48: (-14, 10)}
for n, lon, lat, reg in NUMBERED:
    x, y = project(lon, lat, MAP)
    dx, dy = OFFSETS.get(n, (0, 0))
    if dx or dy:
        d.line([x, y, x + dx, y + dy], fill=(90, 90, 90), width=1)
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=REG[reg])
        x, y = x + dx, y + dy
    num_badge(x, y, 8, n, fill=REG[reg])
BRIEF_DOTS = [
    (47.7, 29.3, "mideast"), (-0.1, 51.5, "europe"), (35.5, 33.3, "mideast"),
    (45.0, 24.0, "mideast"), (-77.0, 38.9, "americas"), (35.5, 31.9, "mideast"),
    (35.0, 31.7, "mideast"), (28.8, 47.0, "europe"), (5.7, 58.9, "europe"),
    (30.0, -2.0, "africa"), (4.35, 50.85, "europe"), (-3.7, 40.4, "europe"),
    (35.2, 32.0, "mideast"), (28.0, -26.0, "africa"), (-9.2, 11.4, "africa"),
    (7.5, 9.0, "africa"), (25.0, 60.2, "europe"), (77.2, 28.6, "asia"),
    (139.7, 35.7, "asia"), (114.0, 12.0, "asia"), (133.0, 36.3, "asia"),
    (100.5, 13.75, "asia"), (121.3, 14.9, "asia"), (-74.0, 40.7, "americas"),
    (-62.0, -4.0, "americas"), (8.0, 50.0, "europe"), (-120.0, 0.0, "americas"),
    (12.5, 55.7, "europe"), (20.0, 10.0, "africa"), (-40.0, 30.0, "americas"),
    (90.4, 23.8, "asia"),
]
for lon, lat, reg in BRIEF_DOTS:
    x, y = project(lon, lat, MAP)
    d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=REG[reg], outline=(255, 255, 255))

# briefs list (right side, two columns, 16 rows; 31 used)
BX = 524
d.text((BX, 722), "ALSO ON 17 NOVEMBER", font=F_SEC, fill=INK)
BRIEFS = [
    (3, "Kuwait reports Iranian drone attack"),
    (6, "West urges Israel to open Gaza"),
    (7, "Israel strikes southern Lebanon"),
    (8, "Houthis hit Saudi pipeline"),
    (9, "Trump weighs dirty-bomb report"),
    (10, "Settlers shoot woman dead"),
    (11, "Knesset elects Netanyahu rival"),
    (14, "Russian drones cross Moldova"),
    (15, "Equinor hit by cyberattack"),
    (16, "Five EU states plan Rwanda hub"),
    (19, "EU raises growth forecast to 1.2%"),
    (20, "Spain raises minimum wage 5.3%"),
    (21, "UK sanctions settlement builders"),
    (24, "17 killed in South Africa shootings"),
    (25, "Guinea arrests 1,200 miners"),
    (26, "Nigeria inflation eases to 14.06%"),
    (27, "Simon Ekpa freed in Finland"),
    (29, "Modi joins ASEAN-India summit"),
    (30, "India and Japan hold 2+2 talks"),
    (31, "China builds S. China Sea runway"),
    (32, "Japan scrambles jets at Russians"),
    (33, "US and Thailand sign trade deal"),
    (34, "Asia launches AZEC 2.0 framework"),
    (37, "Wall Street falls on tech slide"),
    (38, "Isolated Awá filmed in Amazon"),
    (43, "Euclid maps 900 million galaxies"),
    (44, "El Niño nears 1997 record"),
    (45, "Climate spreads resistant bacteria"),
    (46, "Displacement cuts child vaccination"),
    (47, "Alzheimer's light therapy flops"),
    (50, "India beat Pakistan for SAFF title"),
]
for i, (n, txt) in enumerate(BRIEFS):
    col = i // 16
    row = i % 16
    x = BX + col * 236
    y = 760 + row * 14
    num_badge(x + 7, y + 6, 7, n, fill=GREEN)
    d.text((x + 19, y), txt, font=F_BRIEF, fill=INK)

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
