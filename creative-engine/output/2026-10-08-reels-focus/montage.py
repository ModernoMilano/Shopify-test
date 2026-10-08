"""Monteert een reel uit Seedance-clips en stills (draait in de Higgsfield-sandbox, zonder credits).

Gebruik: python3 montage.py <edit.json> <uit.mp4>
edit.json:
  {"fonts": {"serif": "f/cg600.ttf"},
   "src":   {"A": "<url mp4>", "MAC": "<url png>", ...},
   "cuts":  [{"src": "MAC", "dur": 1.3, "zoom": [1.0, 1.06]},           # still: langzaam inzoomen
             {"src": "B", "dur": 1.0, "crop": [0.3, 0.25, 0.75, 0.6]},  # detail uit een still (fracties)
             {"src": "A", "from": 0.2, "dur": 2.2},                     # clip: stuk vanaf 'from'
             ...],
   "text":  [{"cut": 0, "lines": [["One gilet.", 96]], "y": 0.6}, ...],  # y = midden van het tekstblok (0-1)
   "logo":  {"src": "LOGO", "width": 0.4, "seconds": 2.0, "y": 0.5, "fade": 0.5, "dim": 0.18}}
            # logo (PNG met alfa) de laatste 'seconds' in het midden; komt in 'fade' s op, beeld 'dim' donkerder

Harde snedes, 24 fps (zoals de clips), 1080x1920. Geen korrel en geen LUT (SKILL.md, "Echt, niet AI"): de beelden blijven zoals het
model ze maakt. Tekst: gele schreefletter met zachte schaduw (Canva-bord 4-01), buiten de onderste 22% (de Instagram-knoppen).
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 24  # Seedance 2.5 levert 24 fps; omzetten naar 30 geeft haperingen
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


def still_frames(path, dur, zoom, crop=None):
    im = Image.open(path).convert("RGB")
    if crop:  # [x0, y0, x1, y1] als fractie van het beeld, bv. een detail uit een 4K-startbeeld
        w, h = im.size
        im = im.crop((round(crop[0] * w), round(crop[1] * h), round(crop[2] * w), round(crop[3] * h)))
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


def logo_layer(path, spec):
    """Het logo op breedte spec['width'] (fractie van 1080) met een zachte schaduw, op een doorzichtige laag van 1080x1920."""
    lg = Image.open(path).convert("RGBA")
    lg = lg.crop(lg.getbbox())
    lw = round(W * spec.get("width", 0.4))
    lg = lg.resize((lw, round(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    x, y = (W - lg.size[0]) // 2, round(spec.get("y", 0.5) * H - lg.size[1] / 2)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 255), (x + 2, y + 3), lg.getchannel("A").point(lambda v: int(v * 0.45)))
    lay = Image.alpha_composite(lay, sh.filter(ImageFilter.GaussianBlur(5)))
    lay.alpha_composite(lg, (x, y))
    return lay


def with_alpha(layer, a):
    if a >= 1:
        return layer
    out = layer.copy()
    out.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
    return out


def main(cfg_path, out):
    cfg = json.load(open(cfg_path))
    os.makedirs("src", exist_ok=True)
    os.makedirs("frames", exist_ok=True)
    local = {k: get(u, f"src/{k}{os.path.splitext(u.split('?')[0])[1]}") for k, u in cfg["src"].items()}
    texts = {t["cut"]: t for t in cfg.get("text", [])}
    lspec = cfg.get("logo")
    total = sum(round(c["dur"] * FPS) for c in cfg["cuts"])
    llayer = logo_layer(local[lspec["src"]], lspec) if lspec else None
    lstart = total - round(lspec.get("seconds", 2.0) * FPS) if lspec else total
    n = 0
    for i, c in enumerate(cfg["cuts"]):
        p = local[c["src"]]
        frames = (clip_frames(p, c.get("from", 0), c["dur"], f"tmp{i}") if p.endswith(".mp4")
                  else still_frames(p, c["dur"], c.get("zoom", [1.0, 1.05]), c.get("crop")))
        t = texts.get(i)
        layer = text_layer(t["lines"], t.get("y", 0.6), cfg["fonts"]) if t else None
        for k, fr in enumerate(frames):
            fr = fr.convert("RGBA")
            if layer is not None:
                a = min(1.0, (k + 1) / 5)  # tekst komt in 0,2 s op
                lay = layer
                if a < 1:
                    lay = layer.copy()
                    lay.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
                fr = Image.alpha_composite(fr, lay)
            if llayer is not None and n >= lstart:
                a = min(1.0, (n - lstart + 1) / max(1, round(lspec.get("fade", 0.5) * FPS)))
                dim = lspec.get("dim", 0.0) * a
                if dim:
                    fr = Image.alpha_composite(fr, Image.new("RGBA", (W, H), (8, 5, 4, round(255 * dim))))
                fr = Image.alpha_composite(fr, with_alpha(llayer, a))
            n += 1
            fr.convert("RGB").save(f"frames/{n:05d}.jpg", quality=95)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", "frames/%05d.jpg", "-c:v", "libx264",
                    "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], check=True)
    print(out, n, "frames", round(n / FPS, 2), "s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
