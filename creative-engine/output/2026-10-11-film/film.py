"""Monteert de lange merkfilm met voice-over en geluid (draait in de Higgsfield-sandbox, zonder credits).

Gebruik: python3 film.py <film-edit.json> <uit.mp4> [--audio-only]
Naast dit script moeten montage.py en smooth.py staan (uit output/2026-10-08-reels-focus): het beeld wordt op dezelfde manier
gemaakt als bij de reels (harde snedes, 24 fps, 1080x1920, geen korrel en geen LUT, alleen een belichtingsfactor per shot).

film-edit.json:
  {"src":  {"A": "<pad of url mp4>", "LOGO": "<pad of url png>", ...},     # clips: liefst al gladgemaakt met smooth.py
   "cuts": [{"src": "A", "from": 0.0, "dur": 4.0, "gain": 0.95, "crop": [...], "zoom": [1.0, 1.03],
             "xfade": 0.5}, ...],  # xfade: zachte overvloeiing van de vorige snede naar deze, in seconden (standaard hard)
   "fade_in": 0.5,                 # uit zwart aan het begin
   "logo": {"src": "LOGO", "width": 0.28, "seconds": 3.0, "y": 0.5, "fade": 0.6, "black": 1.0},
            # het logo klein in het midden, zonder effect (eigenaar, 10 okt). "black": het beeld gaat in zoveel seconden
            # naar zwart onder het logo, zodat de film eindigt op het logo op zwart.
   "subs": {"font": "f/cormorant.ttf", "weight": "Medium", "size": 46, "y": 0.605,
            "lines": [{"t": [1.2, 3.4], "text": "My father had one rule about clothes."}, ...]},
            # optioneel; y = bovenkant van de tekst als fractie; houd alles tussen y 270 en 1250 px (de knoppen en het
            # bijschrift van Instagram, brief hoofdstuk 6)
   "audio": {"vo": [{"file": "vo/01.wav", "at": 0.8, "db": 0}, ...],
             "beds": [{"gen": "rain", "from": 0, "to": 4.3, "db": -30, "fade": [0.3, 0.4]}, ...],
             "hits": [{"gen": "boom", "at": 58.0, "db": -16}],
             "duck": 4.0,             # dB dat de lagen zakken als de stem spreekt
             "lufs": -14.0, "tp": -1.5}}

De geluidslagen worden hier zelf gemaakt uit gefilterde ruis en sinussen (er is geen muziek- of geluidsmodel voor gewoon
gebruik op Higgsfield): regen, branding, water van het meer, lucht buiten, stilte binnen, een lage zwelling en een lage klap
onder het logo. Ze blijven zacht: de muziek komt er bij het posten bij uit de Instagram-bibliotheek (SKILL.md).
"""
import json, os, shutil, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import montage  # noqa: E402
from montage import FPS, H, W, clip_frames, get, logo_layer, still_frames, with_alpha  # noqa: E402

SR = 48000
RNG = np.random.default_rng(11)


# ---------- geluid ----------

def shaped_noise(n, shape, ch=2):
    """Ruis met een spectrum: shape(f) geeft de amplitude per frequentie (Hz). Twee kanalen met eigen ruis (breed stereo)."""
    f = np.fft.rfftfreq(n, 1 / SR)
    g = shape(np.maximum(f, 1.0))
    out = []
    for _ in range(ch):
        x = np.fft.irfft(np.fft.rfft(RNG.standard_normal(n)) * g, n)
        out.append(x / (np.sqrt(np.mean(x ** 2)) + 1e-12))
    return np.stack(out, 1)


def band(lo, hi, tilt=0.0):
    """Zachte banddoorlaat met een helling (tilt = dB per octaaf, negatief is donkerder)."""
    def s(f):
        a = 1 / (1 + (lo / f) ** 4) / (1 + (f / hi) ** 4)
        return np.sqrt(a) * (f / 1000.0) ** (tilt / 6.02)
    return s


def slow_env(n, rate, depth, smooth_s):
    """Langzame, onregelmatige amplitude tussen 1-depth en 1 (golven, windvlagen)."""
    k = max(2, int(n / SR * rate) + 2)
    pts = RNG.random(k)
    env = np.interp(np.linspace(0, k - 1, n), np.arange(k), pts)
    w = int(smooth_s * SR) | 1
    env = np.convolve(env, np.hanning(w) / np.hanning(w).sum(), mode="same")
    env = (env - env.min()) / (np.ptp(env) + 1e-9)
    return (1 - depth + depth * env)[:, None]


def _fftconv(x, k):
    n = len(x) + len(k) - 1
    N = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(k, N), N)[:len(x)]


def _burst(fc, ms):
    """Kort tikje ruis rond fc Hz dat in ms milliseconden uitsterft (een druppel)."""
    L = int(SR * ms / 1000 * 6)
    t = np.arange(L) / SR
    F = np.fft.rfft(RNG.standard_normal(L) * np.exp(-t / (ms / 1000)))
    F *= np.exp(-0.5 * (np.log2(np.maximum(np.fft.rfftfreq(L, 1 / SR), 1) / fc) / 0.7) ** 2)
    k = np.fft.irfft(F, L)
    return k / (np.abs(k).max() + 1e-9)


def _bubble(f0, ms):
    """Korte stijgende toon: het belletje van een druppel in een plas (Minnaert)."""
    L = int(SR * ms / 1000 * 5)
    t = np.arange(L) / SR
    return np.sin(2 * np.pi * np.cumsum(f0 * (1 + 2.5 * t / (ms / 1000 * 5))) / SR) * np.exp(-t / (ms / 1000))


def _events(n, rate, sigma=0.8):
    k = RNG.poisson(rate * n / SR)
    x = np.zeros(n)
    np.add.at(x, RNG.integers(0, n, k), RNG.lognormal(0, sigma, k) * RNG.choice([-1, 1], k))
    return x


def gen_rain(n):
    """Duizenden losse druppels van verschillende grootte plus belletjes, met zacht ruisen erachter. Met de
    AudioSet-herkenner (AST) getoetst: 'Rain on surface' 0,42, 'Rain' 0,19, 'Raindrop' 0,18 (11 okt). Gewone gefilterde
    ruis las als 'Static'."""
    out = []
    for _ in range(2):
        x = np.zeros(n)
        for fc, ms, rate, a in [(6500, 0.6, 2200, 0.5), (4200, 0.9, 1500, 0.6), (2600, 1.4, 700, 0.7),
                                (1500, 2.5, 120, 0.9), (800, 4.0, 25, 1.0)]:
            x += _fftconv(_events(n, rate), _burst(fc, ms)) * a / np.sqrt(rate)
        for f0, ms, rate in [(1800, 6, 60), (2600, 4, 90), (3500, 3, 120)]:
            x += _fftconv(_events(n, rate, 1.0), _bubble(f0, ms)) * 0.35 / np.sqrt(rate)
        x /= np.std(x) + 1e-12
        out.append(x + shaped_noise(n, band(300, 6000, -4), 1)[:, 0] * 0.25)
    return np.stack(out, 1)


def _swells(n, period=(5.0, 8.0), att=(0.6, 1.2), dec=(1.5, 3.0), floor=0.2):
    t = np.arange(n) / SR
    e = np.zeros(n)
    s = RNG.uniform(0, 2)
    while s < n / SR:
        a, A, D = RNG.uniform(0.6, 1), RNG.uniform(*att), RNG.uniform(*dec)
        tt = t - s
        e += a * np.where(tt < 0, 0, np.where(tt < A, np.sin(np.pi / 2 * tt / A) ** 2, np.exp(-(tt - A) / D)))
        s += RNG.uniform(*period)
    return floor + e


def gen_surf(n):
    """Verre branding, donker (achter glas): golven met een aanloop en een lange uitloop, een bruisende staart en een lage
    rommel. AST: 'Ocean' 0,26, 'Waves, surf' 0,25 (11 okt)."""
    out = []
    for _ in range(2):
        e = _swells(n)
        roar = shaped_noise(n, band(100, 3000, -4), 1)[:, 0] * e
        fizz = _fftconv(_events(n, 6000, 0.9), _burst(3500, 0.8)) / np.sqrt(6000)
        fizz = fizz / (np.std(fizz) + 1e-12) * np.roll(e, int(0.5 * SR)) ** 1.5 * 0.3
        rum = shaped_noise(n, band(25, 200, -6), 1)[:, 0] * e * 0.6
        out.append(roar + fizz + rum)
    return np.stack(out, 1)


def gen_birds(n):
    """Een paar verre vogels: groepjes korte FM-tjilpen. AST: 'Chirp, tweet' 0,71, 'Bird' 0,53 (11 okt)."""
    out = np.zeros((n, 2))
    s = RNG.uniform(0.2, 1.0)
    while s < n / SR - 0.6:
        kind, base, pan = RNG.integers(0, 3), RNG.uniform(2800, 5200), RNG.uniform(0.2, 0.8)
        for _ in range(RNG.integers(2, 6)):
            L = int(SR * RNG.uniform(0.04, 0.11))
            tt = np.arange(L) / SR
            d = L / SR
            f = (base * (1 + 0.35 * np.sin(2 * np.pi * tt / d)) if kind == 0 else
                 base * (1.3 - 0.6 * tt / d) if kind == 1 else base + 600 * np.sin(2 * np.pi * 35 * tt))
            x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) ** 2 * RNG.uniform(0.4, 1)
            i = int(s * SR)
            if i + L < n:
                out[i:i + L, 0] += x * (1 - pan)
                out[i:i + L, 1] += x * pan
            s += d + RNG.uniform(0.03, 0.12)
        s += RNG.uniform(0.8, 2.5)
    return out


def gen_lake(n):
    """Water tegen de boot en een beetje wind. AST: 'Waves, surf' 0,20, 'Ocean' 0,10 (11 okt)."""
    lap = shaped_noise(n, band(150, 1100, -2)) * slow_env(n, 1.1, 0.8, 0.35)
    wind = shaped_noise(n, band(80, 1500, -4)) * slow_env(n, 0.2, 0.6, 2.0) * 0.5
    return lap * 0.8 + wind


def gen_air(n):
    return shaped_noise(n, band(60, 1400, -4)) * slow_env(n, 0.25, 0.5, 1.5) * 0.8


def gen_room(n):
    return shaped_noise(n, band(30, 260, -3)) * 0.6 + shaped_noise(n, band(300, 3000, -6)) * 0.05


def gen_city_night(n):
    return shaped_noise(n, band(35, 220, -4)) * slow_env(n, 0.15, 0.4, 3.0)


def gen_sub(n, f0=41.0):
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f0 * t) + 0.25 * np.sin(2 * np.pi * 2 * f0 * t)
    env = np.sin(np.pi * np.clip(t / (n / SR), 0, 1)) ** 2  # zwelt op en zakt weer
    return np.stack([x * env] * 2, 1)


def gen_boom(n):
    t = np.arange(n) / SR
    f = 38 + 34 * np.exp(-t / 0.25)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * np.exp(-t / 1.4)
    click = np.convolve(RNG.standard_normal(n) * np.exp(-t / 0.012), np.ones(24) / 24, mode="same") * 0.25
    return np.stack([x + click] * 2, 1)


def gen_thump(n):
    """Eén zachte, lage, niet-tonale klap onder het logo (brief: geen toonhoogte die met de muziek botst): ruis door een
    laagdoorlaat met een snelle val."""
    t = np.arange(n) / SR
    x = shaped_noise(n, band(25, 160, -6), 1)[:, 0] * np.exp(-t / 0.35) * (1 - np.exp(-t / 0.004))
    return np.stack([x, x], 1)


GEN = {"thump": gen_thump, "rain": gen_rain, "surf": gen_surf, "lake": gen_lake, "birds": gen_birds, "air": gen_air, "room": gen_room,
       "city_night": gen_city_night, "sub": gen_sub, "boom": gen_boom}


def db(x):
    return 10 ** (x / 20)


def read_wav(path):
    """Leest elk audiobestand via ffmpeg als 48 kHz stereo float."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64)


def fade(x, fin, fout):
    n = len(x)
    e = np.ones(n)
    a, b = int(fin * SR), int(fout * SR)
    if a:
        e[:a] = np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    if b:
        e[n - b:] = np.cos(np.linspace(0, np.pi / 2, b)) ** 2
    return x * e[:, None]


def mix(spec, total_s):
    n = int(round(total_s * SR))
    vo = np.zeros((n, 2))
    for v in spec.get("vo", []):
        x = read_wav(v["file"])
        if "rms" in v:  # elke zin op dezelfde luidheid (gemeten waar hij spreekt), dan pas de correctie in dB
            loud = x[np.abs(x).max(1) > 0.02]
            x = x / (np.sqrt(np.mean(loud ** 2)) + 1e-9) * db(v["rms"])
        x = x * db(v.get("db", 0))
        a = int(round(v["at"] * SR))
        x = x[: max(0, n - a)]
        vo[a:a + len(x)] += x
    beds = np.zeros((n, 2))
    for b in spec.get("beds", []) + spec.get("hits", []):
        a = int(round((b.get("from", b.get("at"))) * SR))
        e = int(round(b["to"] * SR)) if "to" in b else a + int(b.get("len", 3.5) * SR)
        e = min(e, n)
        x = GEN[b["gen"]](e - a)
        x = x / (np.sqrt(np.mean(x ** 2)) + 1e-12) * db(b.get("db", -30))  # rms in dBFS
        fi, fo = b.get("fade", [0.4, 0.4])
        beds[a:e] += fade(x, fi, fo)
    # de lagen zakken onder de stem (zijketen: omhullende van de stem)
    env = np.abs(vo).max(1)
    w = int(0.12 * SR)
    env = np.convolve(env, np.ones(w) / w, mode="same")
    act = np.clip(env / (env.max() * 0.08 + 1e-9), 0, 1)
    w2 = int(0.35 * SR)
    act = np.convolve(act, np.hanning(w2) / np.hanning(w2).sum(), mode="same")
    beds *= db(-spec.get("duck", 4.0) * act)[:, None]
    out = vo + beds
    return out, vo, beds


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((x * 32767).astype("<i2").tobytes())


def loudnorm(src, dst, lufs, tp):
    """Twee keer meten (EBU R128): eerst meten, dan lineair op het doel brengen met een true-peak-limiet."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", f"loudnorm=I={lufs}:TP={tp}:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    af = (f"loudnorm=I={lufs}:TP={tp}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", af, "-ar", str(SR), dst], check=True)
    return m


# ---------- beeld ----------

def subs_layer(text, spec):
    """Eén ondertitelkaart: schreefletter, gebroken wit, met een zachte vage schaduw zodat hij ook op de witte villa
    leesbaar blijft (brief: geen balk, geen vette woorden, geen karaoke)."""
    from PIL import ImageFilter
    f = ImageFont.truetype(spec["font"], spec.get("size", 46))
    if spec.get("weight"):  # variabel lettertype (Cormorant Garamond): "Regular", "Medium", "SemiBold"
        f.set_variation_by_name(spec["weight"])
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(lay), ImageDraw.Draw(sh)
    tw = d.textlength(text, font=f)
    x, y = (W - tw) / 2, spec.get("y", 0.605) * H
    ds.text((x, y + 2), text, font=f, fill=(0, 0, 0, spec.get("shadow", 150)))
    sh = sh.filter(ImageFilter.GaussianBlur(3.5))
    d.text((x, y), text, font=f, fill=(246, 240, 230, 240))
    return Image.alpha_composite(sh, lay)


def frames_of(c, local, i):
    p = local[c["src"]]
    fr = (clip_frames(p, c.get("from", 0), c["dur"], f"tmp{i}", c.get("crop"), c.get("zoom")) if p.endswith(".mp4")
          else still_frames(p, c["dur"], c.get("zoom", [1.0, 1.05]), c.get("crop")))
    if c.get("gain"):  # alleen de belichting van één shot gelijktrekken; geen kleurlook, geen LUT
        g = float(c["gain"])
        fr = (Image.eval(x, lambda v, g=g: min(255, round(v * g))) for x in fr)
    return fr


def padded(gen, n):
    """Precies n frames: ffmpeg geeft met -ss/-t soms een frame minder (lagoC vanaf 0,6 s: 76 in plaats van 77), en een gat
    in de reeks breekt het coderen af. Het laatste frame wordt dan herhaald."""
    last, i = None, 0
    for x in gen:
        if i >= n:
            break
        last, i = x, i + 1
        yield x
    while last is not None and i < n:
        i += 1
        yield last


def video(cfg, out_dir):
    local = {k: (u if os.path.exists(u) else get(u, f"src/{k}{os.path.splitext(u.split('?')[0])[1]}"))
             for k, u in cfg["src"].items()}
    cuts = cfg["cuts"]
    # Een overvloeiing laat de nieuwe snede eerder beginnen: de totale lengte is de som min de overlappen.
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
    os.makedirs(out_dir, exist_ok=True)
    buf = {}  # frames van de vorige snede die nog in een overvloeiing vallen
    n = 0
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
                buf[g] = fr  # dit frame wordt gemengd met het begin van de volgende snede
                continue
            fr = fr.convert("RGBA")
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
            n += 1
            fr.convert("RGB").save(f"{out_dir}/{g + 1:05d}.jpg", quality=95)
        shutil.rmtree(f"tmp{i}", ignore_errors=True)
    return total


def main(cfg_path, out, audio_only=False):
    cfg = json.load(open(cfg_path))
    os.makedirs("src", exist_ok=True)
    cuts = cfg["cuts"]
    total = sum(round(c["dur"] * FPS) for c in cuts) - sum(round(c.get("xfade", 0) * FPS) for c in cuts)
    secs = total / FPS
    a = cfg.get("audio", {})
    full, vo, beds = mix(a, secs)
    write_wav("mix_raw.wav", full / max(1.0, np.abs(full).max()))
    write_wav("vo_only.wav", vo / max(1.0, np.abs(vo).max()))
    if np.abs(full).max() < 1e-6:  # beeldmontage zonder geluid: niets te meten
        shutil.copy("mix_raw.wav", "mix.wav")
    else:
        m = loudnorm("mix_raw.wav", "mix.wav", a.get("lufs", -14.0), a.get("tp", -1.5))
        print("mix gemeten:", m["input_i"], "LUFS ->", a.get("lufs", -14.0))
    if audio_only:
        return
    video(cfg, "frames")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", "frames/%05d.jpg", "-i", "mix.wav",
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", out], check=True)
    shutil.rmtree("frames", ignore_errors=True)
    print(out, total, "frames", round(secs, 2), "s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], "--audio-only" in sys.argv)
