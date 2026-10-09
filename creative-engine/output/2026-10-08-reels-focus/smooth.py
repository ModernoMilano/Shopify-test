"""Haalt het haperen uit Seedance-clips (draait in de Higgsfield-sandbox, zonder credits).

Gebruik: python3 smooth.py <in.mp4> <uit.mp4> [--report]

Wat Seedance 2.5 doet (gemeten 9 okt op alle clips van Total Bordeaux en Il lago, ook in de concepten):
- de clip wordt in stukken van 24 frames gemaakt; op elke naad verschuift het beeld bijna twee keer zo veel als normaal en
  springt de helderheid even: een schok elke seconde;
- een licht pulseren om de 4 frames;
- soms bijna-dubbele frames (detail C van Il lago: twee per seconde).
Samen met de trage beweging leest dat als "laggy slow motion" (eigenaar, 9 okt).

Wat dit script doet: per stap de beweging meten met optische flow (DIS), die beweging gelijkmatig over de tijd verdelen
(Gauss-gladmaken van de snelheid, het begin en eind blijven gelijk) en elk nieuw frame op zijn tijdstip maken door het
dichtstbijzijnde echte frame met optische flow op volle grootte op zijn plek te schuiven (bicubisch). Twee frames mengen
gebeurt niet: dat maakte de tussenbeelden zachter dan de echte en gaf een "ademende" scherpte (controle 9 okt). Ook het
middelen met de buren is eruit: dat kostte de helft van het fijne detail (rits, haar) voor een pulseren van 0,36 grijswaarde
dat niemand ziet. Tot slot de helderheid per frame gladmaken. Aantal frames, lengte en 24 fps blijven gelijk, dus de montage
hoeft niet te veranderen. Geen korrel en geen LUT.
"""
import os, shutil, subprocess, sys, tempfile
import cv2
import numpy as np

SIGMA = 3.0  # frames; haalt pieken om de 4 en 24 frames weg, maar laat versnellen over een halve seconde staan


def read(path):
    cap = cv2.VideoCapture(path)
    out = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        out.append(f)
    return out


def gauss1d(x, s):
    r = int(3 * s + 0.5)
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / s) ** 2)
    k /= k.sum()
    xp = np.pad(x, r, mode="edge")
    return np.convolve(xp, k, mode="valid")


DIS = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)


def flow(a, b, scale=0.5):
    g1 = cv2.cvtColor(cv2.resize(a, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(cv2.resize(b, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
    f = DIS.calc(g1, g2, None)
    return f


def interp(a, b, f, t):
    """Frame op tijd t (0..1) tussen a en b: het dichtstbijzijnde frame, met flow f (a->b, volle grootte) op zijn plek
    geschoven. Eén frame verschuiven houdt het detail; twee mengen maakt het zacht."""
    h, w = a.shape[:2]
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    if t <= 0.5:
        src, k = a, np.float32(-t)
    else:
        src, k = b, np.float32(1 - t)
    return cv2.remap(src, gx + k * f[..., 0], gy + k * f[..., 1], cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def steps(frames):
    """Beweging per stap: gemiddelde lengte van de optische flow, in pixels op halve grootte."""
    return np.array([float(np.sqrt((flow(a, b) ** 2).sum(-1)).mean()) for a, b in zip(frames, frames[1:])])


def retime(frames, m):
    n = len(frames)
    eps = max(1e-3, 0.02 * float(np.median(m)))
    m = m + eps
    C = np.r_[0.0, np.cumsum(m)]
    v = gauss1d(m, SIGMA)
    v *= m.sum() / v.sum()
    T = np.r_[0.0, np.cumsum(v)]
    tau = np.interp(T, C, np.arange(n, dtype=np.float64))
    out, cache = [], {}
    for k in range(n):
        i = min(int(np.floor(tau[k])), n - 2)
        t = tau[k] - i
        if t < 0.02:
            out.append(frames[i])
        elif t > 0.98:
            out.append(frames[i + 1])
        else:
            if i not in cache:
                cache.clear()
                cache[i] = flow(frames[i], frames[i + 1], scale=1.0)
            out.append(interp(frames[i], frames[i + 1], cache[i], t))
    return out, tau


def deflicker(frames, s=4.0, min_gain=0.002):
    """Helderheid per frame gladmaken (de sprong op de naden). Afronden, niet afkappen, en kleine verschillen laten
    staan: anders wisselen pixels per frame een grijswaarde en dat leest als ruis."""
    lum = np.array([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).mean() for f in frames])
    target = gauss1d(lum, s)
    out = []
    for k, f in enumerate(frames):
        g = target[k] / max(lum[k], 1e-3)
        out.append(f if abs(g - 1) < min_gain else np.clip(np.rint(f.astype(np.float32) * g), 0, 255).astype(np.uint8))
    return out, lum, target


def write(frames, path, fps=24):
    tmp = tempfile.mkdtemp()
    for k, f in enumerate(frames):
        cv2.imwrite(f"{tmp}/{k:05d}.png", f, [cv2.IMWRITE_PNG_COMPRESSION, 1])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(fps), "-i", f"{tmp}/%05d.png", "-c:v", "libx264", "-crf", "12",
                    "-preset", "medium", "-pix_fmt", "yuv420p", path], check=True)
    shutil.rmtree(tmp, ignore_errors=True)  # anders loopt de schijf van de sandbox vol (9 okt)


def report(m, label):
    r = [m[i] / np.median(np.r_[m[max(0, i - 3):i], m[i + 1:i + 4]]) for i in range(len(m))]
    hi = [i + 1 for i in range(len(m)) if r[i] > 1.5]
    lo = [i + 1 for i in range(len(m)) if r[i] < 0.4]
    print(f"{label}: median step {np.median(m):.3f} px, jumps {hi}, near-dups {lo}")


def process(src, dst, show=False):
    fr = read(src)
    m = steps(fr)
    out, tau = retime(fr, m)
    out, lum, target = deflicker(out)
    write(out, dst)
    if show:
        report(m, "voor")
        report(steps(out), "na")
    return dst


if __name__ == "__main__":
    process(sys.argv[1], sys.argv[2], "--report" in sys.argv)
