"""Instagram/Facebook profile picture: the CC monogram rebuilt from Cormorant (vector-sharp at any size) in a
rose-gold foil finish. Renders at 4x and downsamples. Output 1080x1080 (Instagram shows it as a circle, so the
monogram sits well inside the centre). Variants: cream (main), charcoal, white."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
S = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(S, "..", "ads", "fonts", "Cormorant-600.ttf")
N, SC = 1080, 4
W = N * SC

def monogram_mask(size):
    """Two overlapping Cs like the original logo: the second sits lower right and over the first."""
    m = Image.new("L", (W, W), 0); d = ImageDraw.Draw(m)
    f = ImageFont.truetype(FONT, size)
    bb = d.textbbox((0, 0), "C", font=f); gw, gh = bb[2] - bb[0], bb[3] - bb[1]
    dx, dy = int(gw * 0.36), int(gh * 0.30)
    tw, th = gw + dx, gh + dy
    x0, y0 = (W - tw) // 2 - bb[0], (W - th) // 2 - bb[1]
    d.text((x0, y0), "C", font=f, fill=255)
    d.text((x0 + dx, y0 + dy), "C", font=f, fill=255)
    return m

def foil(mask, light, mid, dark):
    """Metallic rose-gold: diagonal gradient + soft highlight band + a hair of inner shade."""
    g = Image.new("RGB", (W, W)); px = g.load()
    grad = Image.linear_gradient("L").rotate(-35, expand=False).resize((W, W))
    band = Image.linear_gradient("L").rotate(-35).resize((W, W)).point(lambda v: int(255 * max(0, 1 - abs(v - 120) / 70) ** 2))
    base = Image.composite(Image.new("RGB", (W, W), light), Image.new("RGB", (W, W), dark), grad)
    base = Image.blend(base, Image.new("RGB", (W, W), mid), 0.35)
    hi = Image.new("RGB", (W, W), (250, 228, 228))
    base = Image.composite(hi, base, band.point(lambda v: int(v * 0.55)))
    inner = mask.filter(ImageFilter.GaussianBlur(W // 400))
    shade = ImageChops.subtract(mask, inner).point(lambda v: min(255, v * 3))
    base = Image.composite(Image.new("RGB", (W, W), dark), base, shade.point(lambda v: int(v * 0.5)))
    return base

def render(bg, ring, out, glyph=1.08, light=(214, 150, 160), mid=(183, 110, 121), dark=(140, 72, 84), shadow=True):
    canvas = Image.new("RGB", (W, W), bg)
    if isinstance(bg, tuple) and bg != (255, 255, 255):   # soft radial glow, lighter in the centre
        glow = Image.radial_gradient("L").resize((W, W)).point(lambda v: int((255 - v) * 0.22))
        canvas = Image.composite(Image.new("RGB", (W, W), tuple(min(255, c + 14) for c in bg)), canvas, glow)
    mask = monogram_mask(int(W * glyph / 1.55))
    if shadow:
        sh = mask.filter(ImageFilter.GaussianBlur(W // 140)).point(lambda v: int(v * 0.18))
        sh = ImageChops.offset(sh, 0, W // 180)
        canvas = Image.composite(Image.new("RGB", (W, W), (60, 30, 35)), canvas, sh)
    canvas = Image.composite(foil(mask, light, mid, dark), canvas, mask)
    if ring:
        d = ImageDraw.Draw(canvas); r = int(W * 0.445); c = W // 2; t = max(2, W // 540)
        d.ellipse((c - r, c - r, c + r, c + r), outline=ring, width=t)
    canvas.resize((N, N), Image.LANCZOS).save(os.path.join(S, out), quality=95)

render((245, 241, 237), (199, 140, 150), "profile-cc-cream-1080.png")
render((26, 26, 26), (183, 110, 121), "profile-cc-charcoal-1080.png", light=(226, 168, 176), mid=(196, 124, 135), dark=(150, 82, 94), shadow=False)
render((255, 255, 255), None, "profile-cc-white-1080.png")
print("ok")
