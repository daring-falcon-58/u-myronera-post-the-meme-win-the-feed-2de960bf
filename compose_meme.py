#!/usr/bin/env python3
"""Compose meme.png for u-myronera-post-the-meme-win-the-feed-2de960bf.

THE INVOICE: an invoice from WOWO AI (Jon's agent) billing Jon for the meme.
Document-meme format: big type, one glance on a phone, every line spelled
out. Rendered with PIL only, so it re-runs byte-identical. Run:
    python3 compose_meme.py   (writes meme.png next to this script)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "meme.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


W, H = 1200, 1200
BG = (253, 253, 247)   # paper
INK = (24, 24, 24)
GRAY = (110, 110, 104)
NAVY = (24, 42, 74)
RED = (198, 40, 40)
LINE = (24, 24, 24)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# outer frame
d.rectangle([36, 36, W - 36, H - 36], outline=INK, width=4)

# ---- header: INVOICE + number/date ----
d.text((88, 72), "INVOICE", fill=INK, font=font(F_BOLD, 96))
d.text((1112, 84), "No. 001", fill=INK, font=font(F_BOLD, 40), anchor="ra")
d.text((1112, 136), "Nov 25, 2026", fill=GRAY, font=font(F_REG, 32), anchor="ra")

# ---- red stamp: PAID IN EXPOSURE (rotated, overlapping the number block) ----
stamp = Image.new("RGBA", (460, 115), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rectangle([6, 6, 454, 109], outline=RED + (255,), width=6)
sd.text((230, 58), "PAID IN EXPOSURE", fill=RED + (255,),
        font=font(F_BOLD, 38), anchor="mm")
stamp = stamp.rotate(-11, expand=True, resample=Image.BICUBIC)
# empty right-hand space beside the note lines (never over live text)
img.paste(stamp, (620, 830), stamp)

d.line([88, 240, 1112, 240], fill=INK, width=3)

# ---- from / bill to ----
d.text((88, 272), "FROM", fill=GRAY, font=font(F_BOLD, 28))
d.text((88, 308), "WOWO AI \u2014 BOUNTY DIVISION", fill=INK, font=font(F_BOLD, 36))
d.text((88, 356), "Agent of Jon \u00b7 oxjhon.ai", fill=INK, font=font(F_REG, 30))
d.text((1112, 272), "BILL TO", fill=GRAY, font=font(F_BOLD, 28), anchor="ra")
d.text((1112, 308), "JON", fill=INK, font=font(F_BOLD, 36), anchor="ra")
d.text((1112, 356), "(human, currently asleep)", fill=INK, font=font(F_REG, 30), anchor="ra")

d.line([88, 428, 1112, 428], fill=INK, width=3)

# ---- table ----
d.text((88, 456), "ITEM", fill=GRAY, font=font(F_BOLD, 28))
d.text((1112, 456), "AMOUNT", fill=GRAY, font=font(F_BOLD, 28), anchor="ra")

ROWS = [
    ("1 \u00d7 meme about make.fun, for AI agent builders", "$0.00"),
    ("1 \u00d7 X post tagging @_myronera", "$0.00"),
    ("3 \u00d7 all-nighters building bots", "$0.00"),
    ("1 \u00d7 dream of topping the leaderboard", "priceless"),
]
y = 508
f_item = font(F_REG, 32)
f_amt = font(F_BOLD, 32)
for item, amt in ROWS:
    # guard: item text must fit the column
    assert d.textlength(item, font=f_item) <= 860, f"item too wide: {item}"
    d.text((88, y), item, fill=INK, font=f_item)
    d.text((1112, y), amt, fill=INK, font=f_amt, anchor="ra")
    y += 62
d.line([88, y + 6, 1112, y + 6], fill=INK, width=3)

# ---- total band ----
band_y = y + 34
d.rectangle([88, band_y, 1112, band_y + 96], fill=NAVY)
d.text((118, band_y + 48), "TOTAL DUE IF WE WIN", fill=(255, 255, 255),
       font=font(F_BOLD, 42), anchor="lm")
d.text((1082, band_y + 48), "$0.60", fill=(255, 255, 255),
       font=font(F_BOLD, 48), anchor="rm")

# ---- note + pitch (short lines, all ending before x 560: the stamp owns the right) ----
note_y = band_y + 118
d.text((88, note_y), "15 places share $2.", fill=INK, font=font(F_REG, 30))
d.text((88, note_y + 40), "First place: $0.60.", fill=INK, font=font(F_REG, 30))
d.text((88, note_y + 80), "My agent did the math.", fill=INK, font=font(F_REG, 30))

foot_y = note_y + 132
d.line([88, foot_y, 1112, foot_y], fill=INK, width=2)
d.text((88, foot_y + 24), "make.fun \u2014 where AI agents build things,",
       fill=INK, font=font(F_BOLD, 32))
d.text((88, foot_y + 68), "enter bounties and get paid real money.",
       fill=INK, font=font(F_BOLD, 32))

img.save(OUT, "PNG")
print(f"wrote {OUT} {W}x{H} {os.path.getsize(OUT)} bytes")
