"""Meet hoe een clip ingezoomd en verschoven moet worden zodat zijn eerste frame op het laatste frame van de vorige clip valt.

Gebruik (in de Higgsfield-sandbox): python3 align.py <laatste frame vorige clip> <eerste frame volgende clip>
Uitvoer: JSON met "crop" ([x0, y0, x1, y1] als fractie van de volgende clip) voor montage.py, plus de gevonden schaal en
verschuiving. Waarom: Seedance 2.5 begint een clip soms iets wijder dan het aangeleverde startbeeld (reel Total Bordeaux,
8 okt: 5 tot 10%), en dan verspringt de uitsnede bij een snede op de beweging.

Werkt op randen (gradiënt), zodat een lichter gilet of een andere belichting de meting niet stuurt.
"""
import json, sys
import numpy as np
from PIL import Image, ImageFilter

WORK = 360  # meetbreedte in px


def edges(im, w):
    g = im.convert("L").resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1))
    a = np.asarray(g).astype(np.float32)
    gx, gy = np.zeros_like(a), np.zeros_like(a)
    gx[:, 1:-1] = a[:, 2:] - a[:, :-2]
    gy[1:-1, :] = a[2:, :] - a[:-2, :]
    m = np.hypot(gx, gy)
    return m / (m.mean() + 1e-6)


def score(ref, nxt_img, s, dx, dy):
    """Zoom de volgende clip met factor s (>1 = inzoomen) rond het midden, verschuif (dx, dy) meetpixels, vergelijk."""
    H, W = ref.shape
    w, h = nxt_img.size
    cw, ch = w / s, h / s
    x0 = (w - cw) / 2 + dx * w / W / s
    y0 = (h - ch) / 2 + dy * h / H / s
    if x0 < 0 or y0 < 0 or x0 + cw > w or y0 + ch > h:
        return None, None
    box = (x0, y0, x0 + cw, y0 + ch)
    e = edges(nxt_img.resize((W, H), Image.LANCZOS, box=box), W)
    e = e[:H, :W]
    m = 12  # randen van het beeld negeren
    return float(np.abs(e[m:-m, m:-m] - ref[m:-m, m:-m]).mean()), (box[0] / w, box[1] / h, box[2] / w, box[3] / h)


def main(prev_last, next_first):
    a = Image.open(prev_last).convert("RGB")
    b = Image.open(next_first).convert("RGB").resize(a.size, Image.LANCZOS)
    ref = edges(a, WORK)
    best = (1e9, None, None)
    for s in np.arange(1.00, 1.16, 0.01):  # grof
        for dx in range(-24, 25, 4):
            for dy in range(-24, 25, 4):
                d, box = score(ref, b, s, dx, dy)
                if d is not None and d < best[0]:
                    best = (d, (s, dx, dy), box)
    s0, dx0, dy0 = best[1]
    for s in np.arange(s0 - 0.01, s0 + 0.011, 0.0025):  # fijn
        for dx in np.arange(dx0 - 4, dx0 + 4.1, 1):
            for dy in np.arange(dy0 - 4, dy0 + 4.1, 1):
                d, box = score(ref, b, s, dx, dy)
                if d is not None and d < best[0]:
                    best = (d, (float(s), float(dx), float(dy)), box)
    none, _ = score(ref, b, 1.0, 0, 0)
    print(json.dumps({"crop": [round(v, 4) for v in best[2]], "scale": round(best[1][0], 4),
                      "shift_px_at_360": [best[1][1], best[1][2]], "diff": round(best[0], 4),
                      "diff_without_crop": round(none, 4)}))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
