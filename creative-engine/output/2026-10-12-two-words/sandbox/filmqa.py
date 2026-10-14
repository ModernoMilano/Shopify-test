"""Controlebladen van een gemonteerde film (draait in de sandbox, ~1 min; in de achtergrond starten).

python3 filmqa.py <film.mp4> <timing.json> <tag>  ->  qa/film/<tag>_cuts1..4.jpg  (per snede: begin, midden, eind)
                                                      qa/film/<tag>_cards.jpg     (elke ondertitelkaart op haar midden, uitsnede)
                                                      qa/film/<tag>_logo.jpg      (vier frames van het slot)
                                                      qa/film/<tag>_audio.jpg     (stem-omhullende met kaarten en snedes)
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

film, timing, tag = sys.argv[1:4]
T = json.load(open(timing))
os.makedirs("qa/film", exist_ok=True)
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
total = T["total"]


def frame(t):
    p = "qa/film/_f.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0.0, min(t, total - 0.03)):.3f}", "-i", film, "-frames:v", "1", "-q:v", "2", p], check=True)
    return Image.open(p).convert("RGB")


def thumb(t, w=250):
    im = frame(t)
    return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)


rows = T["rows"]
tw, th, pad, cap = 250, 444, 6, 24
for s in range(4):
    part = rows[s * 8:(s + 1) * 8]
    sheet = Image.new("RGB", (6 * (tw + pad) + pad, 4 * (th + cap + pad) + pad), (28, 28, 28))
    d = ImageDraw.Draw(sheet)
    for n, r in enumerate(part):
        i = s * 8 + n
        rr, cc = divmod(n, 2)
        for k, (lab, t) in enumerate([("begin", r["start"] + 0.08), ("midden", r["start"] + r["dur"] / 2), ("eind", r["start"] + r["dur"] - 0.08)]):
            x = pad + (cc * 3 + k) * (tw + pad)
            y = pad + rr * (th + cap + pad)
            d.text((x + 2, y + 3), f"{i:02d} {r['key']} {lab} {t:.2f}s", font=F, fill=(235, 225, 205))
            sheet.paste(thumb(t), (x, y + cap))
    sheet.save(f"qa/film/{tag}_cuts{s + 1}.jpg", quality=72)

subs = T["subs"]
cols, cw, ch = 2, 540, 118
nrow = (len(subs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (cw + pad) + pad, nrow * (ch + cap + pad) + pad), (28, 28, 28))
d = ImageDraw.Draw(sheet)
for n, sb in enumerate(subs):
    rr, cc = divmod(n, cols)
    t = (sb["t"][0] + sb["t"][1]) / 2
    im = frame(t)
    im = im.crop((0, int(0.56 * im.height), im.width, int(0.70 * im.height))).resize((cw, int(0.14 * im.height * cw / im.width)), Image.LANCZOS)
    x, y = pad + cc * (cw + pad), pad + rr * (ch + cap + pad)
    d.text((x + 2, y + 3), f"{n:02d} {sb['t'][0]:.2f}-{sb['t'][1]:.2f}s  verwacht: {sb['text']}", font=F, fill=(235, 225, 205))
    sheet.paste(im, (x, y + cap))
sheet.save(f"qa/film/{tag}_cards.jpg", quality=80)

last = rows[-1]
ts = [last["start"] + 0.1, last["start"] + 0.7, last["start"] + 1.9, total - 0.05]
sheet = Image.new("RGB", (4 * (tw + pad) + pad, th + cap + 2 * pad), (28, 28, 28))
d = ImageDraw.Draw(sheet)
for k, t in enumerate(ts):
    d.text((pad + k * (tw + pad) + 2, pad + 3), f"slot {t:.2f}s", font=F, fill=(235, 225, 205))
    sheet.paste(thumb(t), (pad + k * (tw + pad), pad + cap))
sheet.save(f"qa/film/{tag}_logo.jpg", quality=80)

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", film, "-f", "f32le", "-ac", "1", "-ar", "8000", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32)
h = 160  # 20 ms
k = len(x) // h
env = np.abs(x[:k * h].reshape(k, h)).max(1)
pps = 50  # px per seconde
half = total / 2
sheet = Image.new("RGB", (int(half * pps) + 40, 2 * 330), (250, 248, 244))
d = ImageDraw.Draw(sheet)
for part in range(2):
    y0 = part * 330
    t0 = part * half
    d.line((0, y0 + 300, sheet.width, y0 + 300), fill=(120, 120, 120))
    for i, e in enumerate(env):
        t = i * h / 8000
        if t0 <= t < t0 + half:
            xx = int((t - t0) * pps)
            d.line((xx, y0 + 300, xx, y0 + 300 - int(min(1.0, e * 1.6) * 240)), fill=(60, 60, 60))
    for r in rows:
        if t0 <= r["start"] < t0 + half:
            xx = int((r["start"] - t0) * pps)
            d.line((xx, y0 + 20, xx, y0 + 300), fill=(200, 60, 60))
            d.text((xx + 2, y0 + 4), r["key"], font=F, fill=(200, 60, 60))
    for sb in subs:
        a, b = sb["t"]
        if b > t0 and a < t0 + half:
            d.rectangle((int((max(a, t0) - t0) * pps), y0 + 306, int((min(b, t0 + half) - t0) * pps), y0 + 318), fill=(230, 190, 60))
    for l in T["lines"]:
        if t0 <= l["at"] < t0 + half:
            xx = int((l["at"] - t0) * pps)
            d.line((xx, y0 + 40, xx, y0 + 300), fill=(40, 150, 60))
            d.text((xx + 2, y0 + 24), f"L{l['n']}", font=F, fill=(40, 150, 60))
    for s in range(int(half) + 1):
        xx = int(s * pps)
        d.text((xx, y0 + 320), f"{t0 + s:.0f}", font=F, fill=(90, 90, 90))
sheet.save(f"qa/film/{tag}_audio.jpg", quality=80)
print("klaar", tag, [os.path.getsize(f"qa/film/{tag}_{n}.jpg") // 1024 for n in ["cuts1", "cuts2", "cuts3", "cuts4", "cards", "logo", "audio"]], "KB")
