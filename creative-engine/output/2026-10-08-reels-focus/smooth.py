"""Haalt het haperen uit Seedance-clips (draait in de Higgsfield-sandbox, zonder credits).

Gebruik: python3 smooth.py <in.mp4> <uit.mp4> [--report]

Wat Seedance 2.5 doet (gemeten 9 okt op alle clips van Total Bordeaux en Il lago, ook in de concepten):
- de clip wordt in stukken van 24 frames gemaakt; op elke naad verschuift het beeld bijna twee keer zo veel als normaal en
  springt de helderheid even: een schok elke seconde;
- een licht pulseren om de 4 frames;
- soms bijna-dubbele frames (detail C van Il lago: twee per seconde).
Samen met de trage beweging leest dat als "laggy slow motion" (eigenaar, 9 okt).

Wat dit script doet: per stap de beweging meten met optische flow (DIS), die beweging gelijkmatig over de tijd verdelen
(Gauss-gladmaken van de snelheid, het begin en eind blijven gelijk) en elk nieuw frame op zijn tijdstip maken uit de twee
frames eromheen, met optische flow. Daarna de helderheid per frame gladmaken. Aantal frames, lengte en 24 fps blijven gelijk,
dus de montage hoeft niet te veranderen. Geen korrel en geen LUT.
"""
import os, subprocess, sys, tempfile
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


def interp(a, b, f_small, t):
    """Frame op tijd t (0..1) tussen a en b; f_small = flow a->b op halve grootte."""
    h, w = a.shape[:2]
    f = cv2.resize(f_small, (w, h), interpolation=cv2.INTER_LINEAR) * (w / f_small.shape[1])
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    t = np.float32(t)
    wa = cv2.remap(a, gx - t * f[..., 0], gy - t * f[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    wb = cv2.remap(b, gx + (1 - t) * f[..., 0], gy + (1 - t) * f[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    t = float(t)
    return cv2.addWeighted(wa, 1 - t, wb, t, 0)


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
                cache[i] = flow(frames[i], frames[i + 1])
            out.append(interp(frames[i], frames[i + 1], cache[i], t))
    return out, tau


def deflicker(frames, s=4.0):
    lum = np.array([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).mean() for f in frames])
    target = gauss1d(lum, s)
    return [np.clip(f.astype(np.float32) * (target[k] / max(lum[k], 1e-3)), 0, 255).astype(np.uint8)
            for k, f in enumerate(frames)], lum, target


def write(frames, path, fps=24):
    tmp = tempfile.mkdtemp()
    for k, f in enumerate(frames):
        cv2.imwrite(f"{tmp}/{k:05d}.png", f, [cv2.IMWRITE_PNG_COMPRESSION, 1])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(fps), "-i", f"{tmp}/%05d.png", "-c:v", "libx264", "-crf", "12",
                    "-preset", "medium", "-pix_fmt", "yuv420p", path], check=True)


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
