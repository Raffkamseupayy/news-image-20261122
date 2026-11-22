#!/usr/bin/env python3
"""Deterministic news front page for 2026-11-22 (UTC). No network, no randomness.

Builds news_2026_11_22.png (1024x1024): masthead + 6 news panels + footer.
Run:  python3 build_image.py            # writes news_2026_11_22.png next to this file
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "news_2026_11_22.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_BOOK = os.path.join(FONT_DIR, "DejaVuSans.ttf")
F_MONO = os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")

BG = (13, 15, 23)
PAPER = (245, 241, 231)
RED = (206, 38, 44)
INK = (24, 26, 32)
GREY = (150, 154, 164)
CREAM = (233, 227, 211)

PANELS = [
    # (headline, body lines, tag, accent color)
    ("COP31 ADOPTS ANTALYA DEAL IN OVERTIME",
     ["Nearly 200 countries gavel through the",
      "summit's cover decision a day late; the text",
      "drops every mention of fossil fuels."],
     "ANTALYA, TURKIYE", (30, 150, 90)),
    ("UKRAINE: STRIKE HITS ZELENSKYY'S CITY",
     ["Ballistic missiles hit Kryvyi Rih, killing 2",
      "and wounding 60 as rescuers are struck in a",
      "second wave; Kerch Bridge hit again."],
     "KRYVYI RIH, UKRAINE", (206, 38, 44)),
    ("RUSSIAN MISSILES DOWN IN POLAND",
     ["Two missiles and a drone land in NATO's",
      "Poland during drills; Tusk calls it a",
      "provocation, NATO vows to defend it."],
     "SOUTHEASTERN POLAND", (70, 120, 210)),
    ("TIBET QUAKE TOLL RISES TO 32",
     ["Rescuers dig through Nagqu after Tuesday's",
      "magnitude-7.0 quake; hundreds of homes",
      "collapsed at high altitude."],
     "NAGQU, CHINA", (190, 110, 40)),
    ("JAPAN QUAKE INJURES 19; MORE FEARED",
     ["A 5.7 quake shakes Shizuoka and Aichi near",
      "Toyohashi, shattering shop windows; the",
      "agency warns of a bigger quake in days."],
     "SHIZUOKA, JAPAN", (200, 60, 110)),
    ("FBI: CRIME DATABASE BREACHED",
     ["Hackers target the NCIC system used by US",
      "law enforcement; NVIDIA accounting probed",
      "by SEC; Bitcoin sinks to 2-year low."],
     "WASHINGTON, US", (120, 90, 200)),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_panel(draw, xy, pw, ph, headline, body, tag, accent):
    x, y = xy
    draw.rectangle([x, y, x + pw, y + ph], fill=PAPER, outline=(210, 205, 192), width=2)
    draw.rectangle([x, y, x + 7, y + ph], fill=accent)
    tx = x + 20
    tw = pw - 38
    hf = font(F_BOLD, 23)
    yy = y + 14
    for ln in wrap(draw, headline, hf, tw):
        draw.text((tx, yy), ln, font=hf, fill=INK)
        yy += 27
    yy += 2
    bf = font(F_BOOK, 16)
    for ln in body:
        for seg in wrap(draw, ln, bf, tw):
            draw.text((tx, yy), seg, font=bf, fill=(70, 72, 80))
            yy += 21
    tf = font(F_MONO, 14)
    draw.text((tx, y + ph - 26), tag, font=tf, fill=accent)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.text((30, 24), "THE DAILY SIGNAL", font=font(F_BOLD, 48), fill=PAPER)
    d.text((36, 86), "WORLD NEWS  \u00b7  SUNDAY, 22 NOVEMBER 2026", font=font(F_MONO, 23), fill=CREAM)
    d.text((36, 118), "Six stories that shaped the day, in one page.", font=font(F_BOOK, 18), fill=GREY)
    d.line([30, 150, W - 30, 150], fill=RED, width=4)

    # ---- panel grid: 2 columns x 3 rows ----
    gx, gy, gap = 30, 172, 14
    pw = (W - 2 * 30 - gap) // 2          # 475
    ph = 240
    slots = [(gx + (i % 2) * (pw + gap), gy + (i // 2) * (ph + gap)) for i in range(6)]
    for (x, y), (head, body, tag, accent) in zip(slots, PANELS):
        draw_panel(d, (x, y), pw, ph, head, body, tag, accent)

    # ---- footer strip ----
    d.line([30, H - 62, W - 30, H - 62], fill=(60, 62, 74), width=2)
    d.text((30, H - 46), "news-image-20261122  \u00b7  all times UTC  \u00b7  sources: wire reports of 22 Nov 2026",
           font=font(F_MONO, 16), fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
