"""Black Week nabewerking: clips aaneen, tekst-, logo- en ladder-overlays, eindkaart. 1080x1920, 25 fps, H.264 hoge
bitrate, zonder geluid. Alle tekst, prijzen en logo's komen hier scherp in de nabewerking, nooit uit het beeldmodel.

Gebruik (in de Higgsfield-sandbox, met fonts/ en logo/ naast het script):
  python3 bw_build.py render videos.json V2 A out/P2_BlackWeek_HookA.mp4
  python3 bw_build.py endcards videos.json out/endcards        (alleen de eindkaarten als PNG, ter controle)

videos.json: per video "hooks" {"A":part,"B":part}, "body": part, "end": part (+ "end_variants": {"B": [extra overlays]}).
Een part = {"segments":[...], "overlays":[...]} met lokale tijden; het script plakt ze achter elkaar (hook 0-3 s,
body 3-8 s, end 8-10.5 s).
Segment: {"src": clip.mp4, "from": s, "dur": s}  (Seedance 24 fps -> 25 fps door 4% sneller af te spelen, elk bronframe
         één keer: geen dubbele frames)
         {"still": beeld.png, "dur": s, "zoom": [1.0, 1.02]}   {"hold": true, "dur": s}  (laatste frame vasthouden)
         {"color": [r,g,b], "dur": s}  (plaatsvervanger)      opties: "fade_in": s (vanuit zwart), "dim": 0..1
Overlay: {"type":"text","lines":[...],"font":"oswald"|"montserrat","size":px,"color":"white"|"brown"|"gold",
          "line_colors":[...],"tracking":0.02,"x":0.5,"y":0.3,"t0":0,"t1":3,"fade":0.25,"shadow":auto,"max_width":0.88}
         {"type":"logo","file":"white"|"black","width":0.42,"y":0.40,"tagline":true,...}
         {"type":"ladder","cells":[...],"size":48,"color":"white","sep_color":"gold","y":0.6,...}
Veilige zone (brief): alles belangrijks tussen 22% en 78% van de hoogte; het script waarschuwt als tekst daarbuiten valt.
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 25
COL = {"white": (255, 255, 255), "brown": (38, 32, 26), "gold": (214, 182, 128), "cream": (244, 238, 228)}
FONT_FILES = {"oswald": ("fonts/Oswald-VF.ttf", "Bold"), "montserrat": ("fonts/Montserrat-VF.ttf", "Medium")}
LOGO_FILES = {"white": "logo/logo_white.png", "black": "logo/logo_black.png"}
TAGLINE = "TIMELESS. REFINED. YOU."
SAFE = (0.22, 0.78)
_fonts = {}


def font(name, size):
    key = (name, size)
    if key not in _fonts:
        path, var = FONT_FILES[name]
        ft = ImageFont.truetype(path, size)
        ft.set_variation_by_name(var)
        _fonts[key] = ft
    return _fonts[key]


def text_width(ft, s, tracking, size):
    return sum(ft.getlength(ch) for ch in s) + tracking * size * max(0, len(s) - 1)


def draw_tracked(d, x, y, s, ft, fill, tracking, size):
    cx = x
    for ch in s:
        d.text((cx, y), ch, font=ft, fill=fill)
        cx += ft.getlength(ch) + tracking * size


def fit_size(name, lines, size, tracking, max_w):
    while size > 20:
        ft = font(name, size)
        if max(text_width(ft, s, tracking, size) for s in lines) <= max_w:
            return size
        size -= 2
    return size


def warn_safe(name, top, bottom):
    if top < SAFE[0] * H or bottom > SAFE[1] * H:
        print(f"  LET OP: '{name}' valt buiten de veilige zone ({top:.0f}-{bottom:.0f} px)", file=sys.stderr)


def text_layer(spec):
    lines = spec["lines"]
    name = spec.get("font", "oswald")
    tracking = spec.get("tracking", 0.02 if name == "oswald" else 0.04)
    size = fit_size(name, lines, spec.get("size", 88), tracking, spec.get("max_width", 0.88) * W)
    ft = font(name, size)
    gap = spec.get("line_gap", 0.22)
    lh = size * (1 + gap)
    total = lh * len(lines) - size * gap
    y0 = spec.get("y", 0.5) * H - total / 2
    colors = spec.get("line_colors")
    color = spec.get("color", "white")
    shadow = spec.get("shadow", color != "brown")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    for i, s in enumerate(lines):
        tw = text_width(ft, s, tracking, size)
        x = spec.get("x", 0.5) * W - tw / 2
        c = COL[colors[i] if colors else color]
        draw_tracked(d, x, y0 + i * lh, s, ft, c + (255,), tracking, size)
        if shadow:
            draw_tracked(ds, x + 3, y0 + i * lh + 5, s, ft, (0, 0, 0, 150), tracking, size)
    warn_safe(lines[0], y0, y0 + total + size * 0.3)
    if shadow:
        sh = sh.filter(ImageFilter.GaussianBlur(10))
        sh.alpha_composite(layer)
        layer = sh
    return layer


def logo_layer(spec):
    lg = Image.open(LOGO_FILES[spec.get("file", "white")]).convert("RGBA")
    lw = round(spec.get("width", 0.42) * W)
    lg = lg.resize((lw, round(lg.size[1] * lw / lg.size[0])), Image.LANCZOS)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x, y = round(spec.get("x", 0.5) * W - lw / 2), round(spec.get("y", 0.4) * H - lg.size[1] / 2)
    layer.alpha_composite(lg, (x, y))
    bottom = y + lg.size[1]
    if spec.get("tagline", True):
        tl = text_layer({"lines": [TAGLINE], "font": "montserrat", "size": spec.get("tagline_size", 26), "tracking": 0.4,
                         "color": "white" if spec.get("file", "white") == "white" else "brown",
                         "y": (bottom + spec.get("tagline_gap", 34)) / H, "shadow": spec.get("file", "white") == "white"})
        layer.alpha_composite(tl)
        bottom += spec.get("tagline_gap", 34) + 40
    warn_safe("logo", y, bottom)
    return layer


def ladder_layer(spec):
    cells = spec["cells"]
    name = spec.get("font", "oswald")
    tracking = spec.get("tracking", 0.02)
    sep = "  |  "
    joined = sep.join(cells)
    size = fit_size(name, [joined], spec.get("size", 50), tracking, spec.get("max_width", 0.9) * W)
    ft = font(name, size)
    tw = text_width(ft, joined, tracking, size)
    x = spec.get("x", 0.5) * W - tw / 2
    y = spec.get("y", 0.6) * H - size / 2
    color, sepc = COL[spec.get("color", "white")], COL[spec.get("sep_color", "gold")]
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    shadow = spec.get("shadow", spec.get("color", "white") != "brown")
    cx = x
    for i, cell in enumerate(cells):
        draw_tracked(d, cx, y, cell, ft, color + (255,), tracking, size)
        if shadow:
            draw_tracked(ds, cx + 3, y + 5, cell, ft, (0, 0, 0, 150), tracking, size)
        cx += text_width(ft, cell, tracking, size) + tracking * size
        if i < len(cells) - 1:
            draw_tracked(d, cx, y, sep, ft, sepc + (255,), tracking, size)
            cx += text_width(ft, sep, tracking, size) + tracking * size
    warn_safe("ladder", y, y + size * 1.3)
    if shadow:
        sh = sh.filter(ImageFilter.GaussianBlur(10))
        sh.alpha_composite(layer)
        layer = sh
    return layer


LAYERS = {"text": text_layer, "logo": logo_layer, "ladder": ladder_layer}


def alpha_at(spec, t):
    t0, t1, fade = spec.get("t0", 0.0), spec.get("t1", 1e9), spec.get("fade", 0.25)
    if t < t0 or t > t1:
        return 0.0
    a = 1.0
    if fade > 0:
        a = min(a, (t - t0) / fade, (t1 - t) / fade if spec.get("fade_out", True) else 1.0)
    return max(0.0, min(1.0, a))


def ffmpeg_frames(src, start, n):
    """n frames vanaf bron-tijd start, 24 fps-bron 4% versneld naar 25 fps (elk bronframe één keer)."""
    cmd = ["ffmpeg", "-loglevel", "error", "-ss", f"{start:.3f}", "-t", f"{n / 24 + 0.5:.3f}", "-i", src,
           "-vf", f"setpts=PTS*24/{FPS},fps={FPS},scale={W}:{H}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)[:n]
    if len(frames) < n:
        print(f"  LET OP: {src} geeft maar {len(frames)} van {n} frames; het laatste wordt herhaald", file=sys.stderr)
        frames = np.concatenate([frames, np.repeat(frames[-1:], n - len(frames), axis=0)])
    return frames


def still_frames(path, n, zoom):
    im = Image.open(path).convert("RGB")
    im = im.resize((W, round(W * im.size[1] / im.size[0])), Image.LANCZOS) if im.size[0] / im.size[1] < W / H else \
        im.resize((round(H * im.size[0] / im.size[1]), H), Image.LANCZOS)
    cx, cy = im.size[0] / 2, im.size[1] / 2
    out = []
    for i in range(n):
        z = zoom[0] + (zoom[1] - zoom[0]) * i / max(1, n - 1)
        w, h = W / z, H / z
        out.append(np.asarray(im.crop((round(cx - w / 2), round(cy - h / 2), round(cx + w / 2), round(cy + h / 2)))
                              .resize((W, H), Image.LANCZOS)))
    return np.stack(out)


def segment_frames(seg, last):
    n = round(seg["dur"] * FPS)
    if "src" in seg:
        fr = ffmpeg_frames(seg["src"], seg.get("from", 0.0), n)
    elif "still" in seg:
        fr = still_frames(seg["still"], n, seg.get("zoom", [1.0, 1.0]))
    elif seg.get("hold"):
        fr = np.repeat(last[None], n, axis=0)
    else:
        fr = np.zeros((n, H, W, 3), np.uint8) + np.array(seg.get("color", [0, 0, 0]), np.uint8)
    fr = fr.astype(np.float32)
    if seg.get("dim"):
        fr *= 1 - seg["dim"]
    if seg.get("fade_in"):
        k = round(seg["fade_in"] * FPS)
        fr[:k] *= (np.arange(k) / k)[:, None, None, None]
    return fr.astype(np.uint8)


def build_parts(video, hook):
    parts = [video["hooks"][hook], video["body"], video["end"]]
    extra = video.get("end_variants", {}).get(hook, [])
    offsets = [0.0]
    for p in parts[:-1]:
        offsets.append(offsets[-1] + sum(s["dur"] for s in p["segments"]))
    overlays = []
    for p, off in zip(parts, offsets):
        for o in p.get("overlays", []):
            overlays.append(dict(o, t0=o.get("t0", 0.0) + off, t1=o.get("t1", 1e9 if "t1" not in o else o["t1"]) + off))
    for o in extra:
        overlays.append(dict(o, t0=o.get("t0", 0.0) + offsets[2], t1=o.get("t1", 1e9) + offsets[2]))
    segments = [s for p in parts for s in p["segments"]]
    return segments, overlays


def render(video, hook, out):
    segments, overlays = build_parts(video, hook)
    layers = [(o, LAYERS[o["type"]](o)) for o in overlays]
    total = sum(s["dur"] for s in segments)
    print(f"{out}: {total:.2f} s, {len(segments)} segmenten, {len(overlays)} overlays")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-vf", "noise=alls=3:allf=t+u", "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", "-an", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t = 0.0
    last = None
    for seg in segments:
        frames = segment_frames(seg, last)
        for fr in frames:
            im = Image.fromarray(fr).convert("RGBA")
            for o, layer in layers:
                a = alpha_at(o, t)
                if a > 0:
                    l2 = layer if a >= 1 else Image.fromarray((np.asarray(layer) * np.array([1, 1, 1, a])).astype(np.uint8))
                    im.alpha_composite(l2)
            proc.stdin.write(im.convert("RGB").tobytes())
            t += 1 / FPS
        last = frames[-1]
    proc.stdin.close()
    proc.wait()
    print("klaar:", out)


def endcards(videos, outdir):
    os.makedirs(outdir, exist_ok=True)
    for vid, video in videos.items():
        for hook in ("A", "B"):
            seg = video["end"]["segments"][0]
            fr = segment_frames(dict(seg, dur=1 / FPS, fade_in=0), None)[0]
            im = Image.fromarray(fr).convert("RGBA")
            _, overlays = build_parts(video, hook)
            off = sum(s["dur"] for s in video["hooks"][hook]["segments"]) + sum(s["dur"] for s in video["body"]["segments"])
            for o in overlays:
                if o["t0"] >= off - 1e-6:
                    im.alpha_composite(LAYERS[o["type"]](o))
            im.convert("RGB").save(os.path.join(outdir, f"{vid}_{video['name']}_Hook{hook}_end.png"))
            print("eindkaart", vid, hook)


if __name__ == "__main__":
    cmd = sys.argv[1]
    videos = json.load(open(sys.argv[2]))
    if cmd == "render":
        render(videos[sys.argv[3]], sys.argv[4], sys.argv[5])
    elif cmd == "endcards":
        endcards(videos, sys.argv[3])
