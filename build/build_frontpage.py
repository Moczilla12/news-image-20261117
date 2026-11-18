#!/usr/bin/env python3
"""Render the make.fun news-image-20261117 front page, v3 (1024x1024 JPEG).

Newspaper front page for Tuesday 17 November 2026: 43 verified stories.
Three large leads with rich AI illustrations (Kerch Bridge, Hormuz strait
map, Quad summit), ten medium stories (one AI illustration for Ebola, nine
refined PIL drawings), a world map with story dots, and a 30-brief column.
All facts verified against reporting dated 17 Nov 2026; nothing invented.
Output is deterministic.
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

REPO = "/home/hatch/workspace/makefun/news-image-20261117"
OUT_JPG = REPO + "/front-page.jpg"
GEO = "/tmp/countries.geo.json"
ASSETS = REPO + "/assets_v3"

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
F_DATE = font("DejaVuSerif-Bold.ttf", 48)
F_TAG = font("DejaVuSans.ttf", 11)
F_LEAD_KICK = font("DejaVuSans-Bold.ttf", 11)
F_LEAD_HEAD = font("DejaVuSerif-Bold.ttf", 17)
F_LEAD_FACT = font("DejaVuSans.ttf", 11)
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


def load_ai(fname, w, h, focus=0.5):
    """Load an AI illustration, crop to the w:h aspect (focus 0=top, 1=bottom),
    and resize. PIL reads WEBP fine."""
    im = Image.open(os.path.join(ASSETS, fname)).convert("RGB")
    iw, ih = im.size
    target = w / h
    src = iw / ih
    if src > target:
        nw = int(ih * target)
        x0 = (iw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, ih))
    else:
        nh = int(iw / target)
        y0 = int((ih - nh) * focus)
        im = im.crop((0, y0, iw, y0 + nh))
    return im.resize((w, h), Image.LANCZOS)


# ---------------------------------------------------------------- header
d.text((28, 8), "THE WORLD'S NEWS IN ONE PICTURE", font=F_KICK, fill=RED)
right = "43 STORIES  ·  6 CONTINENTS  ·  ALL FROM TUESDAY"
d.text((W - 28 - d.textlength(right, font=F_KICK), 8), right, font=F_KICK, fill=INK)
d.text((28, 26), "Tuesday 17 November 2026", font=F_DATE, fill=INK)
d.text((28, 80), "The day in one image — every story happened on 17 November 2026",
       font=F_TAG, fill=GREY)
hline(28, W - 28, 96, 2)
hline(28, W - 28, 100, 1)

# ---------------------------------------------------------------- top row: 3 large leads
LEADS = [
    dict(n=1, kick="EUROPE  ·  UKRAINE WAR", col=BLUE,
         fname="media-generation-kerch-bridge-0-b1fd1fd1-db7d-4bde-8b9f-1ba033b62e23.webp",
         focus=0.5,
         head="Ukraine says a Crimean Bridge road span fell into the sea",
         fact="Second strike in two days; Zelensky hails an 'unprecedented "
              "operation'. The Kremlin vows to rebuild."),
    dict(n=2, kick="MIDDLE EAST  ·  IRAN WAR", col=RED,
         fname="media-generation-hormuz-map-0-47bf7104-8b0e-400f-8fd1-7665f5c40b68.webp",
         focus=0.5,
         head="US jets strike Iran's Qeshm Island",
         fact="US jets hit an IRGC missile site on Qeshm Island, on day 264 of "
              "the US–Iran war."),
    dict(n=3, kick="ASIA  ·  DIPLOMACY", col=ORANGE,
         fname="media-generation-quad-summit-0-f4d9dd6c-1875-41d0-872a-e057aac0e9ea.webp",
         focus=0.3,
         head="Trump meets Quad leaders in Manila",
         fact="First Quad leaders' meeting of Trump's second term; Trump says "
              "the four signed critical-minerals deals."),
]
LEAD_W = 312
for i, s in enumerate(LEADS):
    x = 28 + i * (LEAD_W + 8)
    y = 108
    im_ai = load_ai(s["fname"], LEAD_W, 150, focus=s["focus"])
    img.paste(im_ai, (x, y))
    d.rectangle([x, y, x + LEAD_W - 1, y + 149], outline=(150, 150, 150))
    num_badge(x + 13, y + 13, 10, s["n"], fill=s["col"])
    ky = y + 158
    d.text((x, ky), s["kick"], font=F_LEAD_KICK, fill=s["col"])
    hy = ky + 16
    hl = wrap(s["head"], F_LEAD_HEAD, LEAD_W)
    hy = text_block(x, hy, hl[:2], F_LEAD_HEAD, leading=20)
    fl = wrap(s["fact"], F_LEAD_FACT, LEAD_W)
    text_block(x, hy + 3, fl[:3], F_LEAD_FACT, fill=(70, 70, 70), leading=14)
hline(28, W - 28, 356, 1)

# ---------------------------------------------------------------- PIL art for medium stories
def art_turbines(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(186, 218, 236))
    d.ellipse([x + w - 34, y + 5, x + w - 10, y + 29], fill=(255, 214, 90))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(110, 175, 105))
    for tx, th in [(x + 34, 42), (x + 94, 50), (x + 152, 38)]:
        d.line([tx, y + h - 12, tx, y + h - 12 - th], fill=(255, 255, 255), width=3)
        cx, cy = tx, y + h - 12 - th
        for ang in (90, 210, 330):
            a = math.radians(ang)
            d.line([cx, cy, cx + 11 * math.cos(a), cy - 11 * math.sin(a)],
                   fill=(255, 255, 255), width=2)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(220, 220, 220))


def art_vials(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 235, 240))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(150, 170, 180))
    for i, col in enumerate([(90, 160, 220), (90, 200, 140), (230, 120, 90)]):
        vx = x + 22 + i * 52
        d.rectangle([vx, y + 22, vx + 26, y + h - 16], fill=(255, 255, 255),
                    outline=(120, 120, 120))
        d.rectangle([vx + 2, y + 34, vx + 24, y + h - 18], fill=col)
        d.rectangle([vx + 6, y + 14, vx + 20, y + 22], fill=(60, 60, 60))
        d.rectangle([vx + 8, y + 40, vx + 18, y + 46], fill=(255, 255, 255))


def art_chip(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 54))
    cx, cy = x + 52, y + h // 2
    for k in range(-2, 3):
        d.line([cx - 26, cy + k * 9, cx - 16, cy + k * 9], fill=(200, 200, 200), width=2)
        d.line([cx + 16, cy + k * 9, cx + 26, cy + k * 9], fill=(200, 200, 200), width=2)
    d.rectangle([cx - 16, cy - 18, cx + 16, cy + 18], fill=(40, 90, 160),
                outline=(150, 200, 255))
    d.rectangle([cx - 8, cy - 9, cx + 8, cy + 9], fill=(90, 160, 230))
    pts = [(x + 108, y + h - 14), (x + 128, y + h - 30), (x + 146, y + h - 22),
           (x + 168, y + h - 44), (x + 182, y + 12)]
    d.line(pts, fill=(90, 220, 120), width=3)
    d.polygon([(pts[-1][0] - 6, pts[-1][1] + 2), (pts[-1][0] + 6, pts[-1][1] + 2),
               (pts[-1][0], pts[-1][1] - 7)], fill=(90, 220, 120))


def art_tents(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(190, 170, 120))
    for i, (tx, tw, col) in enumerate([(x + 14, 52, (245, 245, 240)),
                                       (x + 70, 60, (225, 225, 215)),
                                       (x + 132, 48, (245, 245, 240))]):
        d.polygon([(tx, y + h - 14), (tx + tw // 2, y + 14), (tx + tw, y + h - 14)],
                  fill=col, outline=(120, 110, 90))
        d.line([tx + tw // 2, y + 14, tx + tw // 2, y + h - 14], fill=(160, 150, 120), width=1)
        d.polygon([(tx + tw // 2 - 5, y + h - 14), (tx + tw // 2 + 5, y + h - 14),
                   (tx + tw // 2, y + h - 26)], fill=(90, 90, 90))


def art_ger(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(170, 205, 235))
    d.polygon([(x, y + 34), (x + 70, y + 18), (x + w, y + 30), (x + w, y + h),
               (x, y + h)], fill=(120, 175, 105))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(95, 150, 85))
    cx, cy = x + w // 2, y + h - 26
    d.polygon([(cx - 42, cy), (cx, cy - 20), (cx + 42, cy)], fill=(250, 244, 230),
              outline=(150, 130, 100))
    d.rectangle([cx - 42, cy, cx + 42, y + h - 10], fill=(245, 238, 220),
                outline=(150, 130, 100))
    d.rectangle([cx - 7, y + h - 26, cx + 7, y + h - 10], fill=(120, 80, 40))
    d.ellipse([cx - 4, cy - 24, cx + 4, cy - 16], fill=(200, 60, 40))


def art_parliament(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 222, 236))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(150, 160, 170))
    cx = x + w // 2
    d.polygon([(cx - 62, y + 24), (cx, y + 6), (cx + 62, y + 24)], fill=(240, 235, 220),
              outline=(120, 110, 90))
    d.ellipse([cx - 14, y + 2, cx + 14, y + 24], fill=(220, 210, 190),
              outline=(120, 110, 90))
    for k in range(-2, 3):
        px = cx + k * 24
        d.rectangle([px - 4, y + 26, px + 4, y + h - 16], fill=(250, 246, 235),
                    outline=(140, 130, 110))
    d.rectangle([cx - 66, y + h - 16, cx + 66, y + h - 10], fill=(230, 224, 205),
                outline=(120, 110, 90))


def art_factory(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    d.rectangle([x + 16, y + 30, x + 24, y + 58], fill=(150, 90, 70))
    d.ellipse([x + 12, y + 20, x + 28, y + 32], fill=(200, 200, 200))
    d.polygon([(x + 30, y + 58), (x + 30, y + 34), (x + 58, y + 46), (x + 86, y + 34),
               (x + 114, y + 46), (x + 142, y + 34), (x + 170, y + 46), (x + 170, y + 58)],
              fill=(180, 90, 80))
    d.rectangle([x + 30, y + 46, x + 170, y + 58], fill=(200, 120, 100))
    for k in range(5):
        wx = x + 40 + k * 28
        d.rectangle([wx, y + 50, wx + 12, y + 58], fill=(255, 240, 180))
    d.rectangle([x + 84, y + 12, x + 104, y + 30], fill=(255, 255, 255),
                outline=(120, 120, 120))
    d.rectangle([x + 90, y + 8, x + 98, y + 12], fill=(90, 90, 90))


def art_plane(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(175, 210, 235))
    d.ellipse([x + 12, y + 8, x + 52, y + 22], fill=(255, 255, 255))
    d.ellipse([x + 140, y + 44, x + 178, y + 56], fill=(255, 255, 255))
    cx, cy = x + w // 2, y + h // 2 + 4
    d.polygon([(cx - 62, cy - 4), (cx + 52, cy - 4), (cx + 66, cy + 2),
               (cx + 52, cy + 8), (cx - 62, cy + 8)], fill=(70, 80, 95))
    d.polygon([(cx - 8, cy - 4), (cx + 18, cy - 22), (cx + 30, cy - 22),
               (cx + 22, cy - 4)], fill=(90, 100, 115))
    d.polygon([(cx - 30, cy + 8), (cx - 6, cy + 22), (cx + 6, cy + 22),
               (cx + 2, cy + 8)], fill=(90, 100, 115))
    d.polygon([(cx - 62, cy - 4), (cx - 74, cy - 18), (cx - 62, cy - 4),
               (cx - 52, cy + 2)], fill=(90, 100, 115))
    d.ellipse([cx + 52, cy - 2, cx + 62, cy + 4], fill=(180, 220, 240))


def art_gavel(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 220, 205))
    d.ellipse([x + 118, y + 40, x + 176, y + 58], fill=(120, 85, 50))
    d.rectangle([x + 122, y + 58, x + 172, y + 62], fill=(90, 60, 35))
    d.rectangle([x + 34, y + 22, x + 96, y + 40], fill=(150, 105, 60),
                outline=(90, 60, 35))
    d.rectangle([x + 96, y + 28, x + 132, y + 34], fill=(120, 85, 50))
    d.rectangle([x + 30, y + 20, x + 38, y + 42], fill=(90, 60, 35))


ART = {"turbines": art_turbines, "vials": art_vials, "chip": art_chip,
       "tents": art_tents, "ger": art_ger, "parliament": art_parliament,
       "factory": art_factory, "plane": art_plane, "gavel": art_gavel}

# ---------------------------------------------------------------- row 2: 5 medium stories
ROW2 = [
    dict(n=4, kick="AFRICA  ·  HEALTH", col=GREEN, ai="ebola",
         head="Ebola passes 11,300 cases in Congo",
         fact="DR Congo outbreak reached 11,376 cases and 5,568 deaths."),
    dict(n=5, kick="GLOBAL  ·  CLIMATE", col=TEAL, art="turbines",
         head="COP31 divided over a fossil-fuel phase-out",
         fact="Nations weigh the first draft; the Antalya talks end Friday."),
    dict(n=6, kick="AMERICAS  ·  HEALTH", col=RED, art="vials",
         head="US, Mexico and Bolivia lose measles-free status",
         fact="PAHO cites a year of spread; the US has 5,412 cases in 2026."),
    dict(n=7, kick="US  ·  BUSINESS", col=BROWN, art="chip",
         head="Nvidia's quarterly sales double to $115.8bn",
         fact="Reported after the close. Earlier the Dow fell 849 points (−1.6%)."),
    dict(n=8, kick="MIDDLE EAST  ·  GAZA", col=BLUE, art="tents",
         head="Gaza truce at risk of collapse, UN is told",
         fact="Board of Peace report; UN agencies say 1.4m face acute hunger."),
]

# ---------------------------------------------------------------- row 3: 5 medium stories
ROW3 = [
    dict(n=9, kick="ASIA  ·  POLITICS", col=ORANGE, art="ger",
         head="Mongolia's president says he will resign",
         fact="Khürelsükh denies a $25m bribe claim; parliament must accept."),
    dict(n=10, kick="EUROPE  ·  POLITICS", col=BLUE, art="parliament",
         head="Serbia's student-led majority takes its seats",
         fact="Student List holds 140 of 250; Vučić's party goes into opposition."),
    dict(n=11, kick="ASIA  ·  LABOUR", col=GREEN, art="factory",
         head="Bangladesh police tear-gas garment workers",
         fact="They want Tk 30,000 a month, up from 12,500; ~500 factories shut."),
    dict(n=12, kick="RUSSIA  ·  AIR CRASH", col=RED, art="plane",
         head="Russian An-12 crash in Siberia kills all 19",
         fact="The air force plane came down near Kemerovo; a fault is suspected."),
    dict(n=13, kick="AFRICA  ·  JUSTICE", col=BROWN, art="gavel",
         head="Mozambique puts opposition leader on trial",
         fact="Venâncio Mondlane faces 5 charges over deadly 2024 protests."),
]

MED_W = 187


def draw_medium_row(stories, y0):
    for i, s in enumerate(stories):
        x = 28 + i * (MED_W + 8)
        if s.get("ai") == "ebola":
            im_ai = load_ai(
                "media-generation-ebola-tent-0-b4886177-b384-4ea4-b19f-d12ee522edf9.webp",
                MED_W, 68, focus=0.55)
            img.paste(im_ai, (x, y0))
        else:
            ART[s["art"]](x, y0, MED_W, 68)
        d.rectangle([x, y0, x + MED_W - 1, y0 + 67], outline=(150, 150, 150))
        num_badge(x + 11, y0 + 11, 9, s["n"], fill=s["col"])
        ky = y0 + 74
        d.text((x, ky), s["kick"], font=F_MED_KICK, fill=s["col"])
        hy = ky + 13
        hl = wrap(s["head"], F_MED_HEAD, MED_W)
        hy = text_block(x, hy, hl[:2], F_MED_HEAD, leading=15)
        fl = wrap(s["fact"], F_MED_FACT, MED_W)
        text_block(x, hy + 1, fl[:2], F_MED_FACT, fill=(70, 70, 70), leading=12)


draw_medium_row(ROW2, 364)
draw_medium_row(ROW3, 510)
hline(28, W - 28, 656, 1)

# ---------------------------------------------------------------- bottom: map + briefs
d.text((28, 664), "WHERE IT HAPPENED", font=F_SEC, fill=INK)
d.text((524, 664), "ALSO ON 17 NOVEMBER", font=F_SEC, fill=INK)
MAP = (28, 684, 498, 886)
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
    (1, 36.5, 45.3, "europe"), (2, 56.5, 26.8, "mideast"),
    (3, 121.0, 14.6, "asia"), (4, 23.0, -3.0, "africa"),
    (5, 30.7, 36.9, "europe"), (6, -97.0, 38.0, "americas"),
    (7, -122.0, 37.4, "americas"), (8, 34.5, 31.5, "mideast"),
    (9, 106.9, 47.9, "asia"), (10, 20.5, 44.8, "europe"),
    (11, 90.4, 23.8, "asia"), (12, 86.0, 55.3, "asia"),
    (13, 32.6, -25.9, "africa"),
]
OFFSETS = {2: (16, -12), 8: (-16, 10), 5: (14, -12), 11: (14, 12),
           1: (-14, -12), 3: (14, 10), 6: (14, -12), 7: (-14, 10)}
for n, lon, lat, reg in NUMBERED:
    x, y = project(lon, lat, MAP)
    dx, dy = OFFSETS.get(n, (0, 0))
    if dx or dy:
        d.line([x, y, x + dx, y + dy], fill=(90, 90, 90), width=1)
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=REG[reg])
        x, y = x + dx, y + dy
    num_badge(x, y, 8, n, fill=REG[reg])
BRIEF_DOTS = [
    (50.5, 26.2, "mideast"), (56.0, 26.5, "mideast"), (35.5, 33.3, "mideast"),
    (45.0, 24.0, "mideast"), (-77.0, 38.9, "americas"), (35.2, 31.8, "mideast"),
    (30.5, 50.4, "europe"), (28.8, 47.0, "europe"), (8.7, 50.1, "europe"),
    (2.35, 48.85, "europe"), (4.35, 50.85, "europe"), (-0.1, 51.5, "europe"),
    (37.0, 0.0, "africa"), (28.0, -26.0, "africa"), (7.5, 9.0, "africa"),
    (25.0, 60.2, "europe"), (77.2, 28.6, "asia"), (114.0, 12.0, "asia"),
    (139.7, 35.7, "asia"), (100.5, 13.75, "asia"), (106.8, -6.2, "asia"),
    (-76.7, 39.1, "americas"), (-74.0, 40.7, "americas"), (-52.0, -10.0, "americas"),
    (-80.6, 28.4, "americas"), (-150.0, 0.0, "americas"), (8.65, 49.87, "europe"),
    (12.5, 55.7, "europe"), (-71.0, 42.3, "americas"), (88.4, 22.6, "asia"),
]
for lon, lat, reg in BRIEF_DOTS:
    x, y = project(lon, lat, MAP)
    d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=REG[reg], outline=(255, 255, 255))

d.text((28, 894), "Numbers 1–13 are the big stories; dots are the briefs.",
       font=F_TAG, fill=GREY)

# briefs list (right side, two columns of 15; numbers 14–43)
BRIEFS = [
    (14, "Iran drones target US base in Bahrain"),
    (15, "Fourth Hormuz tanker burns"),
    (16, "Israel strikes southern Lebanon"),
    (17, "Houthis hit Saudi pipeline"),
    (18, "Trump weighs dirty-bomb report"),
    (19, "Knesset elects Netanyahu rival"),
    (20, "Russia hits Kyiv's Dnipro bridges"),
    (21, "Russian drones cross Moldova"),
    (22, "Deutsche Bank leak exposes oligarchs"),
    (23, "France hit by nationwide wage protests"),
    (24, "EU raises growth forecast to 1.2%"),
    (25, "UK sanctions settlement builders"),
    (26, "Ebola reaches Kenya and Nigeria"),
    (27, "17 killed in South Africa shootings"),
    (28, "Nigeria inflation eases to 14.06%"),
    (29, "Simon Ekpa freed in Finland"),
    (30, "Modi joins ASEAN-India summit"),
    (31, "China builds S. China Sea runway"),
    (32, "Japan scrambles jets at Russians"),
    (33, "US and Thailand sign trade deal"),
    (34, "Asia launches AZEC 2.0 framework"),
    (35, "NSA network goes down in outage wave"),
    (36, "Wall Street falls on tech slide"),
    (37, "Brazil thrash Singapore 7–0"),
    (38, "Vulcan rocket fails, 40 satellites lost"),
    (39, "Voyager 1 reaches one light-day"),
    (40, "Euclid maps 900 million galaxies"),
    (41, "Climate spreads resistant bacteria"),
    (42, "Alzheimer's light therapy flops"),
    (43, "India beat Pakistan for SAFF title"),
]
for i, (n, txt) in enumerate(BRIEFS):
    col = i // 15
    row = i % 15
    x = 524 + col * 236
    y = 684 + row * 20
    num_badge(x + 7, y + 6, 7, n, fill=GREEN)
    d.text((x + 19, y), txt, font=F_BRIEF, fill=INK)

# ---------------------------------------------------------------- footer
hline(28, W - 28, 992, 1)
d.text((28, 998), "Every story here happened or was first reported on Tuesday 17 November 2026. "
                  "Contested claims are marked as claims.", font=F_FOOT, fill=GREY)
src = "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN. Original drawings."
d.text((W - 28 - d.textlength(src, font=F_FOOT), 998), src, font=F_FOOT, fill=GREY)

img.save(OUT_JPG, "JPEG", quality=88)
print("saved", OUT_JPG)
print("bytes:", os.path.getsize(OUT_JPG))
print("size:", img.size)
