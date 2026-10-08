"""Monteert een reel uit Seedance-clips en stills (draait in de Higgsfield-sandbox, zonder credits).

Gebruik: python3 montage.py <edit.json> <uit.mp4>
edit.json:
  {"fonts": {"serif": "f/cg600.ttf"},
   "src":   {"A": "<url mp4>", "MAC": "<url png>", ...},
   "cuts":  [{"src": "MAC", "dur": 1.3, "zoom": [1.0, 1.06]},           # still: langzaam inzoomen
             {"src": "A", "from": 0.2, "dur": 2.2},                     # clip: stuk vanaf 'from'
             ...],
   "text":  [{"cut": 0, "lines": [["One gilet.", 96]], "y": 0.6}, ...]}  # y = midden van het tekstblok (0-1)

Harde snedes, 30 fps, 1080x1920. Lichte korrel en één kleurcorrectie over alles, zodat stills en clips bij elkaar
passen. Tekst: gele schreefletter met zachte schaduw (Canva-bord 4-01), buiten de onderste 22% (de Instagram-knoppen).
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
YELLOW, CREAM = (242, 209, 107), (245, 238, 225)


def get(url, dst):
    if not os.path.exists(dst):
        subprocess.run(["curl", "-sfL", url, "-o", dst], check=True)
    return dst


def cover(im):
    """Vult 1080x1920 zonder vervorming (bijsnijden in het midden)."""
    w, h = im.size
    s = max(W / w, H / h)
    nw, nh = w * s, h * s
    return im.resize((W, H), Image.LANCZOS, box=((nw - W) / 2 / s, (nh - H) / 2 / s, (nw + W) / 2 / s, (nh + H) / 2 / s))


def still_frames(path, dur, zoom):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    s = max(W / w, H / h)
    bw, bh = W / s, H / s  # het 9:16-venster in bronpixels
    n = round(dur * FPS)
    for k in range(n):
        z = zoom[0] + (zoom[1] - zoom[0]) * (k / max(1, n - 1))
        cw, ch = bw / z, bh / z
        x0, y0 = (w - cw) / 2, (h - ch) / 2
        yield im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))


def clip_frames(path, start, dur, tmp):
    os.makedirs(tmp, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-i", path, "-t", str(dur), "-vf", f"fps={FPS}",
                    "-q:v", "2", f"{tmp}/%04d.jpg"], check=True)
    files = sorted(os.listdir(tmp))[: round(dur * FPS)]
    for f in files:
        yield cover(Image.open(f"{tmp}/{f}").convert("RGB"))


def text_layer(lines, yc, fonts):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(lay), ImageDraw.Draw(sh)
    specs = []
    for ln in lines:
        s, size = ln[0], ln[1]
        style = ln[2] if len(ln) > 2 else "title"
        f = ImageFont.truetype(fonts["serif"], size)
        track = 9 if style == "small" else 0
        if style == "small":
            s = s.upper()
        wdt = sum(d.textlength(c, font=f) for c in s) + track * (len(s) - 1)
        specs.append((s, f, track, wdt, size * 1.25, CREAM if style == "small" else YELLOW))
    total = sum(x[4] for x in specs)
    y = yc * H - total / 2
    # Een zachte donkere waas achter het tekstblok, zodat geel ook op crème en licht hout leesbaar blijft.
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bw = max(x[3] for x in specs) + 220
    ImageDraw.Draw(scrim).ellipse(((W - bw) / 2, y - 70, (W + bw) / 2, y + total + 50), fill=(20, 12, 8, 105))
    scrim = scrim.filter(ImageFilter.GaussianBlur(45))
    for s, f, track, wdt, lh, col in specs:
        x = (W - wdt) / 2
        for c in s:
            ds.text((x + 2, y + 3), c, font=f, fill=(0, 0, 0, 150))
            d.text((x, y), c, font=f, fill=col + (255,))
            x += d.textlength(c, font=f) + track
        y += lh
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    return Image.alpha_composite(Image.alpha_composite(scrim, sh), lay)


def grade(fr, rng):
    a = np.asarray(fr).astype(np.float32)
    a = 12 + a * (243 - 12) / 255  # zachte zwarten en witten
    a += rng.normal(0, 2.6, a.shape[:2])[..., None]  # fijne korrel, gelijk over de kanalen
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def main(cfg_path, out):
    cfg = json.load(open(cfg_path))
    os.makedirs("src", exist_ok=True)
    os.makedirs("frames", exist_ok=True)
    local = {k: get(u, f"src/{k}{os.path.splitext(u.split('?')[0])[1]}") for k, u in cfg["src"].items()}
    texts = {t["cut"]: t for t in cfg.get("text", [])}
    rng = np.random.default_rng(7)
    n = 0
    for i, c in enumerate(cfg["cuts"]):
        p = local[c["src"]]
        frames = (clip_frames(p, c.get("from", 0), c["dur"], f"tmp{i}") if p.endswith(".mp4")
                  else still_frames(p, c["dur"], c.get("zoom", [1.0, 1.05])))
        t = texts.get(i)
        layer = text_layer(t["lines"], t.get("y", 0.6), cfg["fonts"]) if t else None
        for k, fr in enumerate(frames):
            fr = grade(fr, rng).convert("RGBA")
            if layer is not None:
                a = min(1.0, (k + 1) / 6)  # tekst komt in 0,2 s op
                lay = layer
                if a < 1:
                    lay = layer.copy()
                    lay.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
                fr = Image.alpha_composite(fr, lay)
            n += 1
            fr.convert("RGB").save(f"frames/{n:05d}.jpg", quality=95)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", "frames/%05d.jpg", "-c:v", "libx264",
                    "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], check=True)
    print(out, n, "frames", round(n / FPS, 2), "s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
