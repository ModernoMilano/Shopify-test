"""Bouwt de zip met de 25 foto's en 5 video's van het vaste model (draait in de Higgsfield-sandbox).

Verwacht src/<id>.png en src/<id>.mp4, en naast dit script fotos.tsv en videos.tsv:
  fotos.tsv:  nr <tab> id <tab> titel <tab> bijsnede (x0,y0,x1,y1 of -)
  videos.tsv: nr <tab> id <tab> titel <tab> bewerking (- | trim:<sec> | croptop:<px>, te combineren met +)
Bijsneden en inkorten zijn de enige bewerkingen: geen retouches. De randdetector van de 100-set meldt alleen nog
(felle lucht gaf valse treffers); de dubbele controle beoordeelt de hoeken.
"""
import os, subprocess, zipfile
import numpy as np
from PIL import Image

ROOT = "ModernoMilano - Luca - 25 foto's en 5 video's"
FOTO, VIDEO = os.path.join(ROOT, "Foto's"), os.path.join(ROOT, "Video's")


def border(g, cap=0.035):
    """Filmrand per kant (t, b, l, r) in px; zie output/2026-10-07-100-gevarieerd/build_zip.py."""
    a = np.asarray(g.convert('L')).astype(np.int16); h, w = a.shape
    out = []
    for get, n in [(lambda i: a[i], h), (lambda i: a[h - 1 - i], h), (lambda i: a[:, i], w), (lambda i: a[:, w - 1 - i], w)]:
        k = 0
        for m in (lambda x: x < 22, lambda x: x > 246):
            if min(m(get(j)).mean() for j in range(3)) >= 0.6:
                lim = int(n * cap); k = 0
                while k < lim and m(get(k)).mean() >= 0.01: k += 1
                k += 6; break
        out.append(k)
    return tuple(out)


def fit(g, x0, y0, x1, y1, W, H):
    cw, ch = x1 - x0, y1 - y0
    if cw / ch > W / H: nw = round(ch * W / H); x0 += (cw - nw) // 2; x1 = x0 + nw
    else: nh = round(cw * H / W); y0 += (ch - nh) // 2; y1 = y0 + nh
    return g.crop((x0, y0, x1, y1))


def main():
    os.makedirs(FOTO, exist_ok=True); os.makedirs(VIDEO, exist_ok=True); os.makedirs('prev', exist_ok=True)
    log, thumbs = [], []
    for line in open('fotos.tsv', encoding='utf-8'):
        n, i, title, crop = line.rstrip('\n').split('\t')
        g = Image.open(f'src/{i}.png').convert('RGB')
        if crop != '-':
            x0, y0, x1, y1 = map(int, crop.split(',')); g = g.crop((x0, y0, x1, y1)); log.append(f'{i}: bijgesneden {crop}')
        W, H = g.size
        t, b, l, r = border(g)
        if t or b or l or r:
            # Alleen melden: bij deze set zag de detector felle lucht en donkere kanten aan voor een filmrand,
            # en de dubbele controle heeft de hoeken van elke foto al nagelopen.
            log.append(f'{i}: mogelijke rand t{t} b{b} l{l} r{r} (niet gesneden)')
        g.save(f'{FOTO}/{int(n):02d} {title}.jpg', quality=95)
        thumbs.append(g.resize((160, 200)))
        log.append(f'{int(n):02d} {i} {g.size[0]}x{g.size[1]}')
    grid = Image.new('RGB', (800, 1000), 'white')
    for k, t in enumerate(thumbs): grid.paste(t, ((k % 5) * 160, (k // 5) * 200))
    grid.save('prev/grid.jpg', quality=60)
    for line in open('videos.tsv', encoding='utf-8'):
        n, i, title, op = line.rstrip('\n').split('\t')
        dst = f'{VIDEO}/{int(n)} {title}.mp4'
        enc = ['-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-an', '-movflags', '+faststart']
        if op == '-':
            cmd = ['ffmpeg', '-v', 'error', '-y', '-i', f'src/{i}.mp4', '-c', 'copy', '-an', dst]
        else:
            vf, extra = [], []
            for part in op.split('+'):  # bijvoorbeeld croptop:150+trim:3.5
                if part.startswith('trim:'):
                    extra = ['-t', part[5:]]
                elif part.startswith('croptop:'):
                    top = int(part[8:]); h = 1920 - top; w = round(h * 9 / 16) // 2 * 2
                    vf = ['-vf', f'crop={w}:{h}:(iw-{w})/2:{top},scale=1080:1920:flags=lanczos']
                else:
                    raise SystemExit(f'onbekende bewerking {part}')
            cmd = ['ffmpeg', '-v', 'error', '-y', '-i', f'src/{i}.mp4', *extra, *vf, *enc, dst]
        subprocess.run(cmd, check=True); log.append(f'video {n} {i} {op}')
    with zipfile.ZipFile('out.zip', 'w', zipfile.ZIP_STORED) as z:
        for d in (FOTO, VIDEO):
            for f in sorted(os.listdir(d)): z.write(f'{d}/{f}', f'{d}/{f}')
    print('\n'.join(log)); print('foto', len(os.listdir(FOTO)), 'video', len(os.listdir(VIDEO)), 'MB', round(os.path.getsize('out.zip') / 1e6, 1))


if __name__ == '__main__':
    main()
