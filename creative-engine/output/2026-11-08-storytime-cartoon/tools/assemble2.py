# Rap-video assembler (draait in de Higgsfield-sandbox, map ~/tb/rapvid).
# Gebruik: python3 assemble2.py plan.json uit.mp4
# plan: {"audio","words","end_hold","start_t"?,"end_t"?,"shots":[{"clip"|"still","t0","t1","offset"?,"overlay"?}]}  (overlay = png over het hele shot, bv. de eindkaarttekst)
# - words = timeline_words.json [{w,t0,t1}] (ware lyrics, tijden uit faster-whisper via align.py)
# - kaarten van 1-2 woorden, nooit over een punt/vraagteken heen; MODERNO MILANO en DAY <n> worden grote kaarten
# - Montserrat Black, wit met donkere rand en zachte schaduw, op 63% hoogte
# - clips worden geschaald naar 1080x1920/24 fps; te korte clips houden het laatste beeld vast
import json, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H, FPS = 1080, 1920, 24
plan = json.load(open(sys.argv[1])); out = sys.argv[2]
words = json.load(open(plan['words']))
font = ImageFont.truetype('fonts/Montserrat-VF.ttf', int(0.03 * H / 0.72)); font.set_variation_by_name('Black')
big = ImageFont.truetype('fonts/Montserrat-VF.ttf', int(0.052 * H / 0.72)); big.set_variation_by_name('Black')
BIG = re.compile(r'^(DAY (ONE|FOUR|NINE|TWELVE|SIXTEEN|TWENTY-THREE)|MODERNO MILANO)$')
def clean(w): return re.sub(r'[“”"]', '', w).upper()
cards = []; i = 0
while i < len(words):
    w = words[i]; grp = [w]
    if len(clean(w['w']).strip('.,:!?')) < 7 and i + 1 < len(words) and words[i+1]['t0'] - w['t1'] < 0.6 and len(clean(words[i+1]['w']).strip('.,:!?')) < 9 and not clean(words[i+1]['w']).startswith('MODERNO') and not clean(w['w']).startswith('DAY') and clean(w['w'])[-1:] not in '.!?:;':
        grp.append(words[i+1])
    text = ' '.join(clean(x['w']) for x in grp); t0 = grp[0]['t0']; t1 = grp[-1]['t1']; i += len(grp)
    if text.startswith('MODERNO') and i < len(words) and clean(words[i]['w']).startswith('MILANO'):
        text = 'MODERNO MILANO'; t1 = words[i]['t1']; i += 1
    if text.startswith('DAY') and len(grp) == 1 and i < len(words):
        text = 'DAY ' + clean(words[i]['w']).strip('.,:!?'); t1 = words[i]['t1']; i += 1
    cards.append([t0, t1, text.strip(), bool(BIG.match(text.strip().strip('.,:!?')))])
for k in range(len(cards) - 1):
    nt0 = cards[k+1][0]; t1 = cards[k][1]
    cards[k][1] = min(nt0, t1 + 0.6) if nt0 - t1 < 1.0 else t1 + 0.25
# flitskaarten (< 0.2 s in beeld) samenvoegen met de volgende kaart, hooguit 3 woorden, grote kaarten nooit
k = 0
while k < len(cards) - 1:
    cur, nxt = cards[k], cards[k+1]
    if not cur[3] and not nxt[3] and nxt[0] - cur[0] < 0.2 and len((cur[2] + ' ' + nxt[2]).split()) <= 3:
        cards[k+1] = [cur[0], nxt[1], cur[2] + ' ' + nxt[2], False]; del cards[k]
    else: k += 1
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
def read_still(path, n):
    im = Image.open(path).convert('RGB'); s = max(W / im.size[0], H / im.size[1])
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
    fr = read_still(s['still'], n) if 'still' in s else read_clip(s['clip'], s.get('offset', 0.0), n)
    ov = Image.open(s['overlay']).convert('RGBA') if 'overlay' in s else None
    for k in range(n):
        t = (max(n0, frame_idx) + k) / FPS; im = Image.fromarray(fr[k]).convert('RGBA')
        if ov is not None: im.alpha_composite(ov)
        for (a, b, text, isbig) in cards:
            if a <= t < b:
                key = (text, isbig)
                if key not in layers: layers[key] = layer(text, isbig)
                im.alpha_composite(layers[key]); break
        proc.stdin.write(im.convert('RGB').tobytes())
    frame_idx = n1
proc.stdin.close(); proc.wait(); print('klaar', out)
