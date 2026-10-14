"""Maakt film3.py uit film.py (11 okt): dezelfde montage, maar met een optionele "look" (ffmpeg-filterketen uit
looks_defs.py, de oude-camerafilter) over het hele beeld, aangebracht VOOR de ondertitels en het logo, zodat de letters
en het woordmerk schoon blijven. Gebruik: python3 mk_film3.py  (in ~/tw, naast film.py)"""
import re

s = open("film.py").read()
a, b = s.index("def video(cfg, out_dir):"), s.index("def main(cfg_path, out, audio_only=False):")
NEW = '''def video(cfg, out_dir):
    local = {k: (u if os.path.exists(u) else get(u, f"src/{k}{os.path.splitext(u.split('?')[0])[1]}"))
             for k, u in cfg["src"].items()}
    cuts = cfg["cuts"]
    starts, t = [], 0
    for c in cuts:
        t -= round(c.get("xfade", 0) * FPS)
        starts.append(t)
        t += round(c["dur"] * FPS)
    total = t
    lspec = cfg.get("logo")
    llayer = logo_layer(local[lspec["src"]], lspec) if lspec else None
    lstart = total - round(lspec.get("seconds", 2.0) * FPS) if lspec else total
    subs = cfg.get("subs")
    sublayers = [(round(s["t"][0] * FPS), round(s["t"][1] * FPS), subs_layer(s["text"], subs)) for s in (subs or {}).get("lines", [])]
    pic = "pic"
    shutil.rmtree(pic, ignore_errors=True)
    os.makedirs(pic)
    os.makedirs(out_dir, exist_ok=True)
    buf = {}
    # 1. het beeld zonder tekst en logo
    for i, c in enumerate(cuts):
        xf = round(c.get("xfade", 0) * FPS)
        for k, fr in enumerate(padded(frames_of(c, local, i), round(c["dur"] * FPS))):
            g = starts[i] + k
            fr = fr.convert("RGB")
            if k < xf and (g in buf):
                a = (k + 1) / (xf + 1)
                fr = Image.blend(buf.pop(g), fr, a)
            nxt = cuts[i + 1] if i + 1 < len(cuts) else None
            if nxt and nxt.get("xfade") and g >= starts[i + 1]:
                buf[g] = fr
                continue
            fr.save(f"{pic}/{g + 1:05d}.jpg", quality=97)
        shutil.rmtree(f"tmp{i}", ignore_errors=True)
    # 2. de look (oude-camerafilter) over het hele beeld, onder de tekst en het logo
    look = cfg.get("look")
    if look:
        shutil.rmtree("pic2", ignore_errors=True)
        os.makedirs("pic2")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{pic}/%05d.jpg", "-vf", look,
                        "-q:v", "1", "-start_number", "1", "pic2/%05d.jpg"], check=True)
        shutil.rmtree(pic, ignore_errors=True)
        pic = "pic2"
    # 3. fade-in, kaarten, logo
    for g in range(total):
        fr = Image.open(f"{pic}/{g + 1:05d}.jpg").convert("RGBA")
        fi = cfg.get("fade_in", 0)
        if fi and g < round(fi * FPS):
            fr = Image.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), with_alpha(fr, (g + 1) / round(fi * FPS)))
        for a0, a1, lay in sublayers:
            if a0 <= g < a1:
                a = min(1.0, (g - a0 + 1) / 4, (a1 - g) / 4)
                fr = Image.alpha_composite(fr, with_alpha(lay, a))
        if llayer is not None and g >= lstart:
            a = min(1.0, (g - lstart + 1) / max(1, round(lspec.get("fade", 0.5) * FPS)))
            bl = lspec.get("black", 0)
            if bl:
                b = min(1.0, (g - lstart + 1) / max(1, round(bl * FPS)))
                fr = Image.alpha_composite(fr, Image.new("RGBA", (W, H), (0, 0, 0, round(255 * b))))
            fr = Image.alpha_composite(fr, with_alpha(llayer, a))
        fr.convert("RGB").save(f"{out_dir}/{g + 1:05d}.jpg", quality=95)
    shutil.rmtree(pic, ignore_errors=True)
    return total


'''
s = s[:a] + NEW + s[b:]
s = s.replace('"""Monteert de lange merkfilm', '"""film3.py = film.py met een optionele "look" (cfg["look"]: ffmpeg-filterketen) onder de tekst.\n\nMonteert de lange merkfilm', 1)
open("film3.py", "w").write(s)
print("film3.py", len(s))
