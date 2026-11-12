"""Beeld-voor-beeld controle van de ondertitels in de eindvideo.
python3 -I verify_captions.py video.mp4 plan.json cards.json ../assemble3.py fonts/Montserrat-VF.ttf [eindkaart.png eindkaart_t0 fade]

Voor elk beeld van de video: welke kaart hoort er volgens cards.json te staan (zelfde regel als de montage: op hele beelden),
en staat die er ook? De kaart wordt opnieuw getekend met de functie layer() uit assemble3.py; in de video moeten de pixels
van de witte letters wit zijn en de pixels van de donkere rand donker. Daarnaast: staat de vorige of de volgende kaart er
niet ook, en staat er niets waar geen kaart hoort. Met de drie extra argumenten wordt ook de eindkaart nagemeten.
Dit meet of de juiste letters op de juiste beelden staan; of ze prettig lezen is een oordeel voor een mens."""
import json, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

video, plan_p, cards_p, asm_p, font_p = sys.argv[1:6]
W, H, FPS = 1080, 1920, 24
Y0, Y1 = 960, 1680          # de band waarin alle kaarten vallen (ondertitelhoogte 0,63 en 0,75; grote kaarten twee regels)
plan = json.load(open(plan_p)); cards = [list(c) for c in json.load(open(cards_p))]
font = ImageFont.truetype(font_p, int(0.03 * H / 0.72)); font.set_variation_by_name('Black')
big = ImageFont.truetype(font_p, int(0.052 * H / 0.72)); big.set_variation_by_name('Black')
src = open(asm_p, encoding='utf-8').read()
m = re.search(r"^def layer\(.*?(?=^layers = \{\})", src, flags=re.S | re.M)
ns = dict(W=W, H=H, font=font, big=big, Image=Image, ImageDraw=ImageDraw, ImageFilter=ImageFilter)
exec(m.group(0), ns); layer = ns['layer']

shots = sorted(plan['shots'], key=lambda s: s['t0'])
def cap_y(fi):
    for s in shots:
        if round(s['t0'] * FPS) <= fi < round(s['t1'] * FPS): return s.get('cap_y', 0.63)
    return shots[-1].get('cap_y', 0.63)
def card_at(fi):
    for k, (a, b, text, isbig) in enumerate(cards):
        if round(a * FPS) <= fi < round(b * FPS): return k
    return None

masks = {}
def mask(k, cy):
    key = (cards[k][2], cards[k][3], cy)
    if key not in masks:
        a = np.asarray(layer(cards[k][2], cards[k][3], cy))[Y0:Y1]
        fill = (a[..., 0] > 250) & (a[..., 3] == 255); ring = (a[..., 0] < 40) & (a[..., 3] == 255)
        fill = np.asarray(Image.fromarray((fill * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5))) > 0      # alleen het hart van de letters
        ring = np.asarray(Image.fromarray((ring * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3))) > 0      # alleen het hart van de rand
        assert fill.sum() > 500 and ring.sum() > 500, key
        assert not a[:3].any() and not a[-3:].any(), ('kaart valt buiten de band', key)
        masks[key] = (fill, ring)
    return masks[key]
def present(g, k, cy):
    fill, ring = mask(k, cy)
    return float(g[fill].mean()), float(g[ring].mean())

proc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', video, '-vf', f'crop={W}:{Y1 - Y0}:0:{Y0}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], stdout=subprocess.PIPE)
n = W * (Y1 - Y0); fi = 0; bad = []; worst_fill = 255; worst_ring = 0; seen = {}; ghost = 0
FILL_MIN, RING_MAX = 215, 110
while True:
    raw = proc.stdout.read(n)
    if len(raw) < n: break
    g = np.frombuffer(raw, np.uint8).reshape(Y1 - Y0, W); cy = cap_y(fi); k = card_at(fi)
    if k is not None:
        f, r = present(g, k, cy); seen[k] = seen.get(k, 0) + 1
        worst_fill = min(worst_fill, f); worst_ring = max(worst_ring, r)
        if f < FILL_MIN or r > RING_MAX: bad.append((fi, f'kaart {k + 1} "{cards[k][2]}" hoort er te staan maar is niet (goed) te zien: letters {f:.0f}, rand {r:.0f}'))
    for j in ((k - 1, k + 1) if k is not None else [q for q in range(len(cards)) if abs(round(cards[q][0] * FPS) - fi) < 60 or abs(round(cards[q][1] * FPS) - fi) < 60]):
        if j < 0 or j >= len(cards) or (k is not None and cards[j][2] == cards[k][2]): continue
        fill, ring = mask(j, cy)
        if k is not None:   # alleen de pixels die niet ook bij de kaart van dit beeld horen
            cf, cr = mask(k, cy); fill = fill & ~cf & ~cr; ring = ring & ~cf & ~cr
            if fill.sum() < 300 or ring.sum() < 300: continue
        f, r = float(g[fill].mean()), float(g[ring].mean())
        if f >= FILL_MIN and r <= RING_MAX:
            ghost += 1; bad.append((fi, f'kaart {j + 1} "{cards[j][2]}" is te zien terwijl {"kaart %d" % (k + 1) if k is not None else "geen kaart"} er hoort te staan'))
    fi += 1
proc.wait()
print('beelden', fi, '| kaarten', len(cards), '| kaarten gezien', len(seen), '| zwakste letters', round(worst_fill), '(min %d)' % FILL_MIN, '| lichtste rand', round(worst_ring), '(max %d)' % RING_MAX)
exp = {k: round(cards[k][1] * FPS) - round(cards[k][0] * FPS) for k in range(len(cards))}
short = [(k + 1, cards[k][2], seen.get(k, 0), exp[k]) for k in exp if seen.get(k, 0) != exp[k]]
print('kaarten met een ander aantal beelden dan gepland:', short if short else 'geen')
print('kortste kaart:', min((exp[k], cards[k][2]) for k in exp), 'beelden')
nocard = [f for f in range(fi) if card_at(f) is None]
print('beelden zonder kaart:', len(nocard), '| fouten:', len(bad))
for f, msg in bad[:40]: print('  !! beeld %d (%.2f s): %s' % (f, f / FPS, msg))

if len(sys.argv) > 6:   # eindkaart
    ov = np.asarray(Image.open(sys.argv[6]).convert('RGBA')); t0 = float(sys.argv[7]); fade = float(sys.argv[8])
    white = (ov[..., :3].min(-1) > 245) & (ov[..., 3] > 250)
    white = np.asarray(Image.fromarray((white * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3))) > 0
    ys = np.where(white.any(1))[0]; xs = np.where(white.any(0))[0]
    print('eindkaart: witte letters tussen y=%d en y=%d (%.1f%% tot %.1f%% van de hoogte), x=%d tot %d, %d pixels' % (ys[0], ys[-1], 100 * ys[0] / H, 100 * ys[-1] / H, xs[0], xs[-1], white.sum()))
    res = []
    for t in (t0 - 0.2, t0 + fade / 2, t0 + fade + 0.1, t0 + 2.0, t0 + 4.0, 89.9):
        raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{t:.3f}', '-i', video, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
        g = np.frombuffer(raw, np.uint8).reshape(H, W); res.append((round(t, 2), round(float(g[white].mean()))))
    print('eindkaart: helderheid van de letterpixels per tijdstip:', res, '(voor de fade laag, daarna tegen 255)')
