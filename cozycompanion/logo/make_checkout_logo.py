"""Checkout header image: the CozyCompanion wordmark with the three key USPs underneath (owner, 2026-11-05).
Transparent PNG, 1200 px wide; text sized to stay readable when Shopify shows the logo ~300-400 px wide."""
import os
from PIL import Image, ImageDraw, ImageFont
S = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(S, "..", "ads", "fonts")
ROSE, CHAR = (183, 110, 121, 255), (26, 26, 26, 255)
W = 1200
logo = Image.open(os.path.join(S, "logo-dark.png")).convert("RGBA"); logo = logo.crop(logo.getbbox())
lw = 740; logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
items = ["FREE SHIPPING", "3–5 DAY DELIVERY", "30-DAY RETURNS"]
font = ImageFont.truetype(os.path.join(F, "Jost-500.ttf"), 60); sp = 2; gap = 64
d0 = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
def tw(t): return sum(d0.textlength(c, font=font) for c in t) + sp * (len(t) - 1)
while sum(tw(t) for t in items) + gap * (len(items) - 1) > W - 40:
    font = ImageFont.truetype(os.path.join(F, "Jost-500.ttf"), font.size - 2)
total = sum(tw(t) for t in items) + gap * (len(items) - 1)
H = 30 + logo.height + 34 + 2 + 30 + font.size + 26
im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
im.alpha_composite(logo, ((W - lw) // 2, 30))
y = 30 + logo.height + 34
d.line(((W - 260) // 2, y, (W + 260) // 2, y), fill=ROSE, width=2)
x = (W - total) / 2; y += 30
for i, t in enumerate(items):
    for c in t:
        d.text((x, y), c, font=font, fill=CHAR); x += d.textlength(c, font=font) + sp
    x -= sp
    if i < len(items) - 1:
        cx = x + gap / 2; cy = y + font.size * 0.62
        d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=ROSE); x += gap
im.save(os.path.join(S, "checkout-logo-usps.png")); print(im.size, "font", font.size)
