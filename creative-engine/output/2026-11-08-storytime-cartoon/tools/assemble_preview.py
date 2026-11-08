"""Preview-montage: Kling-clips (720x1276) -> 1080x1920 24 fps, stem + muziek, woord-voor-woord ondertitels in de stijl van het
voorbeeld (Montserrat Black, caps, wit, donkere outline + zachte schaduw, caphoogte 3% van H, gecentreerd op 63% van H)."""
import json, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, FPS = 1080, 1920, 24
plan = json.load(open(sys.argv[1])); out = sys.argv[2]
font = ImageFont.truetype('fonts/Montserrat-VF.ttf', int(0.03 * H / 0.72))  # cap height ~3% of H (Montserrat caps ~0.72 em)
font.set_variation_by_name('Black')
big = ImageFont.truetype('fonts/Montserrat-VF.ttf', int(0.055 * H / 0.72)); big.set_variation_by_name('Black')

def frames(src, n):
    cmd = ['ffmpeg', '-loglevel', 'error', '-i', src, '-vf', f'scale={W}:{H}:flags=lanczos,fps={FPS}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    if len(fr) < n:
        fr = np.concatenate([fr, np.repeat(fr[-1:], n - len(fr), axis=0)])
    return fr[:n]

def caption_layer(text, size_big=False):
    ft = big if size_big else font
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    lines = [text] if len(text) <= 18 else [text[:text.rfind(' ', 0, len(text) // 2 + 4)], text[text.rfind(' ', 0, len(text) // 2 + 4) + 1:]]
    lh = ft.size * 1.15; total = lh * len(lines); y = 0.63 * H - total / 2
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=ft); x = (W - tw) / 2
        ds.text((x + 4, y + i * lh + 8), ln, font=ft, fill=(0, 0, 0, 170), stroke_width=6, stroke_fill=(0, 0, 0, 170))
        d.text((x, y + i * lh), ln, font=ft, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(20, 20, 20, 255))
    sh = sh.filter(ImageFilter.GaussianBlur(8)); sh.alpha_composite(layer); return sh

# timeline
t = 0.0; segs = []; cards = []
for s in plan['shots']:
    n = round(s['dur'] * FPS); segs.append((s['clip'], n, t))
    for c in s.get('cards', []):
        cards.append((t + c['t0'], t + c['t1'], c['text'], c.get('big', False)))
    t += s['dur']
total_frames = sum(n for _, n, _ in segs); print('frames', total_frames, 'sec', total_frames / FPS)
layers = {}
cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
       '-i', plan['audio'], '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
       '-shortest', '-movflags', '+faststart', out]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for clip, n, t0 in segs:
    fr = frames(clip, n)
    for i in range(n):
        tt = t0 + i / FPS
        im = Image.fromarray(fr[i]).convert('RGBA')
        for a, b, text, bg in cards:
            if a <= tt < b:
                key = (text, bg)
                if key not in layers: layers[key] = caption_layer(text, bg)
                im.alpha_composite(layers[key])
        proc.stdin.write(im.convert('RGB').tobytes())
proc.stdin.close(); proc.wait(); print('klaar', out)
