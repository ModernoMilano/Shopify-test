"""Technische controle van de eindvideo: python3 -I check_final.py video.mp4 liedje.mp3
Meet: formaat, lengte, aantal beelden, verschuiving van het geluid ten opzichte van het liedje (kruiscorrelatie),
hoe goed het geluid op het liedje lijkt, en of er zwarte beelden in zitten.
Dit zijn metingen; of het goed klinkt kan alleen iemand met oren beoordelen."""
import json, subprocess, sys
import numpy as np

video, song = sys.argv[1], sys.argv[2]
SR = 8000


def probe(p):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,size,bit_rate:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels,duration',
                          '-of', 'json', p], capture_output=True, text=True).stdout
    return json.loads(out)


def pcm(p):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-vn', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


pv, ps = probe(video), probe(song)
vs = [s for s in pv['streams'] if s['codec_type'] == 'video'][0]
au = [s for s in pv['streams'] if s['codec_type'] == 'audio'][0]
print('video  :', vs['codec_name'], f"{vs['width']}x{vs['height']}", vs['r_frame_rate'], 'beelden', vs.get('nb_frames'), 'lengte', round(float(pv['format']['duration']), 3), 's',
      'grootte', round(int(pv['format']['size']) / 1e6, 1), 'MB', 'bitrate', round(int(pv['format']['bit_rate']) / 1e6, 2), 'Mbit/s')
print('geluid :', au['codec_name'], au['sample_rate'], 'Hz', au['channels'], 'kanalen', 'lengte', round(float(au['duration']), 3), 's')
print('liedje : lengte', round(float(ps['format']['duration']), 3), 's')

a, b = pcm(video), pcm(song)
n = min(len(a), len(b))
# kruiscorrelatie over het hele stuk (FFT), zoekbereik +/- 2 s
m = 1 << int(np.ceil(np.log2(2 * n)))
fa, fb = np.fft.rfft(a[:n], m), np.fft.rfft(b[:n], m)
cc = np.fft.irfft(fa * np.conj(fb), m)
rng = 2 * SR
lags = np.concatenate([np.arange(0, rng + 1), np.arange(-rng, 0)])
vals = np.concatenate([cc[:rng + 1], cc[-rng:]])
lag = int(lags[int(np.argmax(vals))])
print('verschuiving geluid t.o.v. liedje:', round(1000 * lag / SR, 1), 'ms (0 = gelijk)')
if lag >= 0: x, y = a[lag:n], b[:n - lag]
else: x, y = a[:n + lag], b[-lag:n]
k = min(len(x), len(y)); x, y = x[:k], y[:k]
print('gelijkenis (correlatie) over de hele lengte:', round(float(np.corrcoef(x, y)[0, 1]), 4))
for t0 in (0, 20, 40, 60, 80):
    i0, i1 = t0 * SR, min(k, (t0 + 10) * SR)
    if i1 - i0 > SR and np.std(x[i0:i1]) > 1e-6 and np.std(y[i0:i1]) > 1e-6:
        print(f'  {t0:>2}-{t0 + 10} s: correlatie', round(float(np.corrcoef(x[i0:i1], y[i0:i1])[0, 1]), 4),
              'niveau video/liedje', round(float(np.sqrt(np.mean(x[i0:i1] ** 2)) / np.sqrt(np.mean(y[i0:i1] ** 2))), 3))

# zwarte of bijna zwarte beelden: elk 6e beeld, klein
W, H = 54, 96
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', video, '-vf', f'select=not(mod(n\\,6)),scale={W}:{H}', '-vsync', '0', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, dtype=np.uint8).reshape(-1, H, W)
mean = fr.reshape(len(fr), -1).mean(1)
dark = [round(i * 6 / 24, 2) for i in np.where(mean < 12)[0]]
print('beelden bekeken:', len(fr), '| donkerste gemiddelde helderheid:', round(float(mean.min()), 1), '| bijna zwart op (s):', dark if dark else 'geen')
