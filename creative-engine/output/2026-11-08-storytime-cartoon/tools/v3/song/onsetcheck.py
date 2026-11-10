"""Controleer het echte begin van de zang in een deel: whisper op een uitgeknipt stuk rond de (onbetrouwbare) eerste woordtijd.
Gebruik: python3 onsetcheck.py <part> [window_start] [window_len]  -> print eerste gehoorde woorden met tijden in deel-tijd."""
import sys, json, subprocess
from faster_whisper import WhisperModel
part = sys.argv[1]
T = json.load(open('transcripts.json'))[part]['words']
guess = T[0]['t0'] if T else 0.0
ws = float(sys.argv[2]) if len(sys.argv) > 2 else max(0.0, guess - 2.0)
wl = float(sys.argv[3]) if len(sys.argv) > 3 else 9.0
subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',f'{ws:.2f}','-t',f'{wl:.2f}','-i',part+'.wav','-ac','1','-ar','16000',f'crop_{part}.wav'],check=True)
m = WhisperModel("small", device="cpu", compute_type="int8")
segs,_ = m.transcribe(f'crop_{part}.wav', language='en', word_timestamps=True, vad_filter=False, beam_size=5)
out = []
for s in segs:
    for w in (s.words or []): out.append((round(w.start+ws,2), w.word.strip()))
print(part, 'whisper-guess', guess, 'window', ws, ws+wl)
print(' '.join(f"{w}@{t}" for t,w in out[:14]))
