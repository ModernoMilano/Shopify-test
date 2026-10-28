"""Build the 4:5 (1080x1350) Meta ad images: scene + hook + brand + CTA, in the CozyCompanion style.
Raw scenes live in ads/raw (Higgsfield), output in ads/out."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
A = os.path.dirname(os.path.abspath(__file__))
F = lambda n, s: ImageFont.truetype(os.path.join(A, "fonts", n), s)
CHAR, ROSE, CREAM = (26, 26, 26), (183, 110, 121), (245, 241, 237)
W, H = 1080, 1350

ADS = [  # id, scene, hook, sub, cta
 ("nestle_1_senior", "ad_n1", "Old joints feel the cold first.", "Gentle, adjustable warmth for their favorite nap spot.", "Shop Nestle"),
 ("nestle_2_spot",   "ad_n2", "The warmest spot in the house is now theirs.", "3 heat levels · waterproof · chew-resistant cord", "Shop Nestle"),
 ("nestle_3_thermo", "ad_n3", "Keep the thermostat low. Keep them toasty.", "A 20 W heated pad warms their spot, not the whole house.", "Shop Nestle"),
 ("nestle_4_lap",    "ad_n4", "Sorry, your lap just lost.", "The heated pad cats choose over everything.", "Shop Nestle"),
 ("nestle_5_safe",   "ad_n5", "Warmth you don't have to worry about.", "Anti-bite cord · 3 heat levels · waterproof cover", "Shop Nestle"),
 ("roam_1_bed",      "ad_r1", "Your back seat just became a dog bed.", "One flat, cozy bed across the whole seat.", "Shop Roam"),
 ("roam_2_mud",      "ad_r2", "Muddy paws? Your seats will never know.", "Waterproof, quilted and wipe-clean.", "Shop Roam"),
 ("roam_3_trip",     "ad_r3", "Holiday road trip? Bring the whole family.", "Room to stretch out for every mile.", "Shop Roam"),
 ("roam_4_flat",     "ad_r4", "No more sliding into the footwell.", "A firm base bridges the gap into one flat bed.", "Shop Roam"),
 ("roam_5_before",   None,    "Same seat. Same dog. One upgrade.", "Roam back seat dog bed & cover", "Shop Roam"),
 ("glance_1_late",   "ad_g1", "Stuck late at work? Dinner's still on time.", "Scheduled, portioned meals, served automatically.", "Shop Glance"),
 ("glance_2_6am",    "ad_g2", "The 6 a.m. wake-up call? Cancelled.", "Breakfast is served on schedule, so you can sleep in.", "Shop Glance"),
 ("glance_3_away",   "ad_g3", "Weekend away. Zero guilt.", "4L of food on schedule, with battery backup.", "Shop Glance"),
 ("glance_4_two",    "ad_g4", "Two pets. Two bowls. No food fights.", "Double-bowl feeder with a built-in HD camera.", "Shop Glance"),
 ("glance_5_watch",  "ad_g5", "Watch them eat from anywhere.", "HD camera with live view in the app.", "Shop Glance"),
]

def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))

def wrap(d, text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]

def shadow_text(im, xy, text, font, fill):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((xy[0] + 2, xy[1] + 3), text, font=font, fill=(0, 0, 0, 170))
    im.paste(Image.new("RGB", im.size, (0, 0, 0)), (0, 0), layer.getchannel("A").filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(im).text(xy, text, font=font, fill=fill)

def scrim(img, top_h, bot_h):
    g = Image.new("L", (1, H), 0)
    for y in range(H):
        a = 0
        if y < top_h: a = int(215 * (1 - y / top_h) ** 1.1)
        if y > H - bot_h: a = max(a, int(200 * ((y - (H - bot_h)) / bot_h) ** 1.3))
        g.putpixel((0, y), a)
    dark = Image.new("RGB", (W, H), CHAR)
    return Image.composite(dark, img, g.resize((W, H)))

def before_after():
    b = cover(Image.open(os.path.join(A, "raw", "ad_r5before.jpg")), W // 2, H)
    a = cover(Image.open(os.path.join(A, "raw", "ad_r1.jpg")), W // 2, H)
    im = Image.new("RGB", (W, H)); im.paste(b, (0, 0)); im.paste(a, (W // 2, 0))
    d = ImageDraw.Draw(im); d.rectangle((W // 2 - 3, 0, W // 2 + 3, H), fill=CREAM)
    return im

logo = Image.open(os.path.join(A, "..", "logo", "logo-light.png")).convert("RGBA")
logo = logo.crop(logo.getbbox()); logo = Image.merge('RGBA', (*[Image.new('L', logo.size, c) for c in CREAM], logo.getchannel('A'))); logo = logo.resize((300, round(300 * logo.height / logo.width)), Image.LANCZOS)

for aid, scene, hook, sub, cta in ADS:
    im = before_after() if scene is None else cover(Image.open(os.path.join(A, "raw", f"{scene}.jpg")).convert("RGB"), W, H)
    im = scrim(im, 560, 300)
    d = ImageDraw.Draw(im)
    fh = F("Cormorant-600.ttf", 92)
    lines = wrap(d, hook, fh, 940)
    if len(lines) > 3: fh = F("Cormorant-600.ttf", 78); lines = wrap(d, hook, fh, 940)
    y = 78
    for ln in lines:
        shadow_text(im, (70, y), ln, fh, CREAM); y += int(fh.size * 1.02)
    d.rectangle((70, y + 22, 150, y + 26), fill=ROSE)
    fs = F("Jost-400.ttf", 36)
    y += 50
    for ln in wrap(d, sub, fs, 900):
        shadow_text(im, (70, y), ln, fs, CREAM); y += 48
    if scene is None:
        fl = F("Jost-500.ttf", 30)
        for x, t in ((W // 4, "BEFORE"), (3 * W // 4, "AFTER")):
            tw = d.textlength(t, font=fl); d.rounded_rectangle((x - tw / 2 - 22, 1000, x + tw / 2 + 22, 1052), 26, fill=CREAM)
            d.text((x - tw / 2, 1006), t, font=fl, fill=CHAR)
    # bottom: logo left, CTA pill right
    im.paste(logo, (70, H - 70 - logo.height), logo)
    fc = F("Jost-500.ttf", 34); label = cta + "  →"
    tw = d.textlength(label, font=fc); x1 = W - 70; x0 = x1 - tw - 64
    d.rounded_rectangle((x0, H - 130, x1, H - 56), 37, fill=ROSE)
    d.text((x0 + 32, H - 116), label, font=fc, fill=CREAM)
    im.save(os.path.join(A, "out", f"{aid}.jpg"), quality=94)
    print(aid)
