"""CozyCompanion logo with USP row and 30-day guarantee bar -> logo/logo-usp-badge.png (+ preview)."""
import os
from PIL import Image, ImageDraw, ImageFont
L = os.path.dirname(os.path.abspath(__file__))
F = lambda n, s: ImageFont.truetype(os.path.join(L, "..", "ads", "fonts", n), s)
CHAR, ROSE, BAR, WHITE = (26, 26, 26), (183, 110, 121), (238, 234, 229), (255, 255, 255)
S = 2  # supersample for smooth icons
W, H = 1200 * S, 420 * S
im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
logo = Image.open(os.path.join(L, "logo-dark.png")).convert("RGBA"); logo = logo.crop(logo.getbbox())
lw = 900 * S; logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
im.paste(logo, ((W - lw) // 2, 20 * S), logo)
y = 20 * S + logo.height + 34 * S

def lock(x, y, s):
    w = 3 * S
    d.arc((x + s*0.22, y, x + s*0.78, y + s*0.62), 180, 360, fill=ROSE, width=w)
    for xx in (x + s*0.22, x + s*0.78): d.line((xx, y + s*0.31, xx, y + s*0.45), fill=ROSE, width=w)
    d.rounded_rectangle((x + s*0.08, y + s*0.42, x + s*0.92, y + s), radius=4*S, fill=ROSE)
def truck(x, y, s):
    d.rounded_rectangle((x, y + s*0.2, x + s*0.62, y + s*0.75), radius=2*S, fill=ROSE)
    d.polygon([(x + s*0.62, y + s*0.38), (x + s*0.86, y + s*0.38), (x + s, y + s*0.56), (x + s, y + s*0.75), (x + s*0.62, y + s*0.75)], fill=ROSE)
    for cx in (x + s*0.2, x + s*0.8):
        d.ellipse((cx - s*0.12, y + s*0.68, cx + s*0.12, y + s*0.92), fill=ROSE, outline=WHITE, width=2*S)
def check(x, y, s):
    d.ellipse((x, y, x + s, y + s), fill=ROSE)
    d.line([(x + s*0.27, y + s*0.52), (x + s*0.44, y + s*0.68), (x + s*0.74, y + s*0.34)], fill=WHITE, width=4*S, joint="curve")

items = [(lock, "Secure checkout"), (truck, "Tracked worldwide shipping"), (check, "PayPal & cards")]
f = F("Jost-500.ttf", 27 * S); ic = 27 * S; gap_i = 10 * S; gap = 36 * S
widths = [ic + gap_i + d.textlength(t, font=f) for _, t in items]
x = (W - (sum(widths) + gap * (len(items) - 1))) / 2
for (fn, t), w in zip(items, widths):
    fn(x, y + 5 * S, ic); d.text((x + ic + gap_i, y - 1 * S), t, font=f, fill=CHAR); x += w + gap
y += 70 * S
bx0, bx1 = (W - lw) // 2, (W + lw) // 2
d.rectangle((bx0, y, bx1, y + 74 * S), fill=BAR)
g = "30 DAY MONEY BACK GUARANTEE"; fg = F("Jost-400.ttf", 36 * S); sp = 6 * S
ws = [d.textlength(ch, font=fg) for ch in g]; x = (W - (sum(ws) + sp * (len(g) - 1))) / 2
for ch, w in zip(g, ws):
    d.text((x, y + 15 * S), ch, font=fg, fill=CHAR); x += w + sp
im = im.crop(im.getbbox()); im = im.resize((im.width // S, im.height // S), Image.LANCZOS)
im.save(os.path.join(L, "logo-usp-badge.png"))
bg = Image.new("RGB", im.size, WHITE); bg.paste(im, (0, 0), im); bg.save(os.path.join(L, "logo-usp-badge-preview.jpg"), quality=92)
print(im.size)
