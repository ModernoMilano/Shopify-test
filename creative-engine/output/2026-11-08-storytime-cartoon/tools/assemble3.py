"""Montage: python3 assemble3.py plan.json uit.mp4   (of: ... plan.json - cards  -> alleen de ondertitelkaarten tonen)
Verschil met assemble2: flitskaarten worden nooit over een regelgrens samengevoegd, een overlay kan infaden (overlay_fade)
en een stilstaand beeld kan langzaam inzoomen (zoom), voor een proefversie waarin een clip nog ontbreekt."""
import json, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H, FPS = 1080, 1920, 24
plan = json.load(open(sys.argv[1])); out = sys.argv[2]
words = json.load(open(plan['words']))
font = ImageFont.truetype('fonts/Montserrat-VF.ttf', int(0.03 * H / 0.72)); font.set_variation_by_name('Black')
big = ImageFont.truetype('fonts/Montserrat-VF.ttf', int(0.052 * H / 0.72)); big.set_variation_by_name('Black')
BIG = re.compile(r'^(DAY (ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN|TWELVE|FIFTEEN|SIXTEEN|TWENTY|TWENTY-THREE)|MODERNO MILANO)$')
def clean(w): return re.sub(r'[“”"]', '', w).upper()
cards = []; i = 0
while i < len(words):
    w = words[i]; grp = [w]
    if len(clean(w['w']).strip('.,:!?')) < 7 and i + 1 < len(words) and words[i+1]['t0'] - w['t1'] < 0.6 and len(clean(words[i+1]['w']).strip('.,:!?')) < 9 and not clean(words[i+1]['w']).startswith('MODERNO') and clean(w['w']).strip('.,:!?') != 'DAY' and clean(w['w'])[-1:] not in '.!?:;' and not words[i+1].get('line_start'):
        grp.append(words[i+1])
    text = ' '.join(clean(x['w']) for x in grp); t0 = grp[0]['t0']; t1 = grp[-1]['t1']; i += len(grp)
    if text.startswith('MODERNO') and i < len(words) and clean(words[i]['w']).startswith('MILANO'):
        text = 'MODERNO MILANO'; t1 = words[i]['t1']; i += 1
    if text.strip('.,:!?') == 'DAY' and len(grp) == 1 and i < len(words):
        text = 'DAY ' + clean(words[i]['w']).strip('.,:!?'); t1 = words[i]['t1']; i += 1
    cards.append([t0, t1, text.strip(), bool(BIG.match(text.strip().strip('.,:!?')))])
for k in range(len(cards) - 1):
    nt0 = cards[k+1][0]; t1 = cards[k][1]
    cards[k][1] = min(nt0, t1 + 0.6) if nt0 - t1 < 1.0 else t1 + 0.25
# flitskaarten (< 0.2 s in beeld) samenvoegen, hooguit 3 woorden, grote kaarten nooit, en nooit over een regelgrens:
# is de volgende kaart het begin van een nieuwe regel, dan gaat de flitskaart bij de vorige kaart van dezelfde regel
LS = {round(w['t0'], 3) for w in words if w.get('line_start')}
def starts_line(c): return round(c[0], 3) in LS
k = 0
while k < len(cards) - 1:
    cur, nxt = cards[k], cards[k+1]
    if cur[3] or nxt[0] - cur[0] >= 0.2: k += 1; continue
    if not starts_line(nxt):
        if not nxt[3] and len((cur[2] + ' ' + nxt[2]).split()) <= 3:
            cards[k+1] = [cur[0], nxt[1], cur[2] + ' ' + nxt[2], False]; del cards[k]; continue
    elif k > 0 and not starts_line(cur) and not cards[k-1][3] and len((cards[k-1][2] + ' ' + cur[2]).split()) <= 3:
        cards[k-1] = [cards[k-1][0], cur[1], cards[k-1][2] + ' ' + cur[2], False]; del cards[k]; continue
    k += 1
for k in range(len(cards) - 1):
    if cards[k][1] > cards[k+1][0]: cards[k][1] = cards[k+1][0]
if len(sys.argv) > 3 and sys.argv[3] == 'cards':
    for c in cards: print('%6.2f-%6.2f %s%s' % (c[0], c[1], 'BIG ' if c[3] else '    ', c[2]))
    raise SystemExit
print('cards', len(cards), 'big', sum(1 for c in cards if c[3]))
def layer(text, isbig):
    ft = big if isbig else font
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); lines = [text]
    if d.textlength(text, font=ft) > 0.9 * W and ' ' in text:
        cut = text.rfind(' ', 0, len(text) // 2 + 3); lines = [text[:cut], text[cut+1:]]
    lh = ft.size * 1.15; total = lh * len(lines); y = 0.63 * H - total / 2
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    for n, ln in enumerate(lines):
        x = (W - d.textlength(ln, font=ft)) / 2
        ds.text((x + 4, y + n * lh + 8), ln, font=ft, fill=(0, 0, 0, 170), stroke_width=6, stroke_fill=(0, 0, 0, 170))
        d.text((x, y + n * lh), ln, font=ft, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(20, 20, 20, 255))
    sh = sh.filter(ImageFilter.GaussianBlur(8)); sh.alpha_composite(im); return sh
layers = {}
def read_clip(path, offset, n):
    cmd = ['ffmpeg', '-loglevel', 'error', '-ss', f'{offset:.3f}', '-i', path, '-vf', f'scale={W}:{H}:flags=lanczos,fps={FPS}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    if len(fr) == 0: raise SystemExit('leeg: ' + path)
    if len(fr) < n: fr = np.concatenate([fr, np.repeat(fr[-1:], n - len(fr), axis=0)])
    return fr[:n]
def read_still(path, n, zoom=None):
    im = Image.open(path).convert('RGB'); s = max(W / im.size[0], H / im.size[1])
    if zoom:   # langzame inzoom vanuit het midden, bijvoorbeeld [1.0, 1.05], voor een proefversie waarin een clip nog ontbreekt
        out = np.empty((n, H, W, 3), np.uint8); cx, cy = im.size[0] / 2, im.size[1] / 2
        for k in range(n):
            z = zoom[0] + (zoom[1] - zoom[0]) * k / max(1, n - 1); cw, ch = W / (s * z), H / (s * z)
            out[k] = np.asarray(im.resize((W, H), Image.BICUBIC, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)))
        return out
    im = im.resize((round(im.size[0] * s), round(im.size[1] * s)), Image.LANCZOS); l = (im.size[0] - W) // 2; t = (im.size[1] - H) // 2
    return np.repeat(np.asarray(im.crop((l, t, l + W, t + H)))[None], n, axis=0)
audio_dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', plan['audio']], capture_output=True, text=True).stdout)
shots = sorted(plan['shots'], key=lambda s: s['t0'])
end_t = plan.get('end_t', audio_dur); start_t = plan.get('start_t', 0.0)
if plan.get('end_hold', True) and shots[-1]['t1'] < end_t: shots[-1]['t1'] = end_t
print('audio', round(audio_dur, 2), 'end', round(shots[-1]['t1'], 2))
cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-ss', f'{start_t:.3f}', '-i', plan['audio'],
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE); frame_idx = round(start_t * FPS)
for s in shots:
    n0 = round(s['t0'] * FPS); n1 = round(s['t1'] * FPS)
    for _ in range(max(0, n0 - frame_idx)): proc.stdin.write(np.zeros((H, W, 3), np.uint8).tobytes())
    n = n1 - max(n0, frame_idx)
    if n <= 0: continue
    fr = read_still(s['still'], n, s.get('zoom')) if 'still' in s else read_clip(s['clip'], s.get('offset', 0.0), n)
    ov = Image.open(s['overlay']).convert('RGBA') if 'overlay' in s else None
    for k in range(n):
        t = (max(n0, frame_idx) + k) / FPS; im = Image.fromarray(fr[k]).convert('RGBA')
        if ov is not None:
            fade = s.get('overlay_fade', 0.0)  # seconden infaden vanaf het begin van dit shot
            a = min(1.0, (k + 1) / (fade * FPS)) if fade > 0 else 1.0
            if a < 1.0:
                o2 = ov.copy(); o2.putalpha(ov.getchannel('A').point(lambda v, a=a: int(v * a))); im.alpha_composite(o2)
            else: im.alpha_composite(ov)
        for (a, b, text, isbig) in cards:
            if a <= t < b:
                key = (text, isbig)
                if key not in layers: layers[key] = layer(text, isbig)
                im.alpha_composite(layers[key]); break
        proc.stdin.write(im.convert('RGB').tobytes())
    frame_idx = n1
proc.stdin.close(); proc.wait(); print('klaar', out)
