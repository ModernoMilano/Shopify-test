"""Knip een herhaald stuk uit een deel, op de maat. Gebruik: python3 cutpart.py <part> <start> <end> [bars_multiple=1]
Zoekt de beats het dichtst bij start en end, maakt de lengte een geheel aantal maten, knipt met 30 ms crossfade.
Bewaart het origineel als <part>_orig.mp3 en schrijft een nieuw <part>.mp3; verwijdert done_<part>.flag zodat analyze opnieuw loopt."""
import sys, os, shutil, subprocess, numpy as np, librosa, soundfile as sf
part, start, end = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
SR = 48000
src = part + '_orig.mp3'
if not os.path.exists(src): shutil.copy(part + '.mp3', src)
y, _ = librosa.load(src, sr=SR, mono=False)
if y.ndim == 1: y = np.stack([y, y])
tempo, b = librosa.beat.beat_track(y=librosa.to_mono(y), sr=SR, units='time', start_bpm=90)
tempo = float(np.atleast_1d(tempo)[0]); beat = 60.0 / tempo
i0 = int(np.argmin(np.abs(b - start))); t0 = b[i0]
n_beats = int(round((end - t0) / beat)); n_beats = max(4, int(round(n_beats / 4.0)) * 4)
t1 = t0 + n_beats * beat
# lijn t1 op de dichtstbijzijnde echte beat
i1 = int(np.argmin(np.abs(b - t1))); t1 = b[i1] if abs(b[i1] - t1) < 0.12 else t1
xf = int(0.03 * SR); a = y[:, :int(t0 * SR)]; c = y[:, int(t1 * SR):]
fade = a[:, -xf:] * np.linspace(1, 0, xf) + c[:, :xf] * np.linspace(0, 1, xf)
out = np.concatenate([a[:, :-xf], fade, c[:, xf:]], axis=1)
sf.write('tmp_cut.wav', out.T, SR)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'tmp_cut.wav', '-c:a', 'libmp3lame', '-b:a', '256k', part + '.mp3'], check=True)
for f in ['done_' + part + '.flag']:
    if os.path.exists(f): os.remove(f)
print(part, 'tempo', round(tempo, 1), 'cut', round(t0, 2), '->', round(t1, 2), 'removed', round(t1 - t0, 2), 's =', n_beats, 'beats; new length', round(out.shape[1] / SR, 2))
