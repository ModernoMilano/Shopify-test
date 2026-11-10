"""Transcribeer een songdeel (faster-whisper, woordtijden) en meet per zin de toonhoogte (librosa pyin), zodat we zien
welke zinnen door de rapper (lage f0, ~90-140 Hz) en welke door de zangeres (hoge f0, ~180-350 Hz) worden gedaan.
Gebruik: python3 analyze.py <naam>  (verwacht <naam>.mp3; schrijft <naam>.wav, transcript in transcripts.json)"""
import sys, json, os, subprocess
import numpy as np, librosa
name = sys.argv[1]
subprocess.run(['ffmpeg','-loglevel','error','-y','-i',name+'.mp3','-ac','1','-ar','16000',name+'.wav'],check=True)
from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu", compute_type="int8")
segs, info = model.transcribe(name+'.wav', language="en", word_timestamps=True, vad_filter=False, beam_size=5)
y, sr = librosa.load(name+'.wav', sr=16000)
from scipy.signal import butter, sosfiltfilt
sos = butter(4, [140, 3000], btype='band', fs=sr, output='sos'); yv = sosfiltfilt(sos, y)
yh = librosa.effects.harmonic(yv, margin=3.0)
f0, vf, vp = librosa.pyin(yh, fmin=85, fmax=600, sr=sr, frame_length=1024, hop_length=160)
t = librosa.frames_to_time(np.arange(len(f0)), sr=sr, hop_length=160)
words=[]; lines=[]
for s in segs:
    m = (t>=s.start)&(t<s.end)&vf
    med = float(np.nanmedian(f0[m])) if m.sum()>5 else float('nan')
    voice = 'ZIJ' if med>185 else ('HIJ' if med==med else '?')
    lines.append({"t0":round(s.start,2),"t1":round(s.end,2),"f0":round(med,1) if med==med else None,"voice":voice,"text":s.text.strip()})
    for w in (s.words or []): words.append({"w":w.word.strip(),"t0":round(w.start,2),"t1":round(w.end,2),"p":round(w.probability,2)})
old = json.load(open('transcripts.json')) if os.path.exists('transcripts.json') else {}
old[name] = {"text":" ".join(l['text'] for l in lines),"words":words,"lines":lines}
json.dump(old, open('transcripts.json','w'), indent=1)
dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',name+'.mp3'],capture_output=True,text=True).stdout)
print(name, 'dur', round(dur,2), 'first word', words[0]['t0'] if words else None, 'last', words[-1]['t1'] if words else None)
for l in lines: print(f"{l['t0']:6.2f}-{l['t1']:6.2f} {str(l['f0']):>6} {l['voice']:3} {l['text']}")
open('done_'+name+'.flag','w').write('ok')
