#!/usr/bin/env python3
"""Generate a simple favicon.ico into `static/` using Pillow.

This script creates a 64x64 icon with a colored background and a letter 'C'.
It writes `static/favicon.ico` which will be included by collectstatic.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / 'static'
STATIC_DIR.mkdir(parents=True, exist_ok=True)
OUT = STATIC_DIR / 'favicon.ico'

W = H = 64
bg = (31, 111, 235)
fg = (255, 255, 255)

img = Image.new('RGBA', (W, H), bg)
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype('arial.ttf', 36)
except Exception:
    font = ImageFont.load_default()

text = 'C'
try:
    # Pillow >=8.0 provides textbbox; use it when available
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
except Exception:
    try:
        w, h = font.getsize(text)
    except Exception:
        w, h = 32, 32

draw.text(((W - w) / 2, (H - h) / 2), text, font=font, fill=fg)

# Save as .ico with multiple sizes
img.save(OUT, format='ICO', sizes=[(64,64),(32,32),(16,16)])
print('Wrote', OUT)
