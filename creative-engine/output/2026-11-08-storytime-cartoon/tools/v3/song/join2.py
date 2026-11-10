"""Vloeiender aan elkaar plakken van losse ElevenLabs-delen: snijden op de maat (beat voor het eerste woord, beat na het
laatste woord), loudness gelijk, en op elke naad een omgekeerde 'swell' van het inkomende deel onder het uitgaande deel
(maskeert de klankwissel), daarna een korte crossfade. Gebruik: python3 join2.py plan.json out.wav"""
import json, subprocess, sys, numpy as np, librosa, soundfile as sf
plan=json.load(open(sys.argv[1])); out=sys.argv[2]; SR=48000
def load(mp3):
    y,_=librosa.load(mp3, sr=SR, mono=False); 
    if y.ndim==1: y=np.stack([y,y])
    return y
def beats(y):
    tempo, b = librosa.beat.beat_track(y=librosa.to_mono(y), sr=SR, units='time', start_bpm=88)
    return float(np.atleast_1d(tempo)[0]), b
segs=[]
for p in plan['parts']:
    y=load(p['mp3']); tempo,b=beats(y)
    # startpunt: laatste beat vóór (eerste woord - 0.15 s), anders eerste woord - 0.4
    cand=[t for t in b if t < p['first']-0.15]; t0=max(cand[-1], p['first']-1.0) if cand else max(0,p['first']-0.4)
    cand2=[t for t in b if t > p['last']+0.3]; t1=min(cand2[0]+ (60/tempo)*p.get('tail_beats',1), y.shape[1]/SR) if cand2 else min(p['last']+p.get('tail',1.2), y.shape[1]/SR)
    if 'tail' in p and p['tail']>2.0: t1=min(p['last']+p['tail'], y.shape[1]/SR)
    seg=y[:, int(t0*SR):int(t1*SR)]
    # loudness naar -14 LUFS via ffmpeg loudnorm (eenvoudig: RMS-normalisatie hier, loudnorm op het eind)
    rms=np.sqrt(np.mean(seg**2)); seg=seg*(0.12/max(rms,1e-6))
    print(p['mp3'],'tempo',round(tempo,1),'cut',round(t0,2),round(t1,2),'len',round(t1-t0,2))
    segs.append(seg)
xf=plan.get('xfade',0.35); sw=plan.get('swell',1.2)
cur=segs[0]
for nxt in segs[1:]:
    n_sw=int(sw*SR); n_xf=int(xf*SR)
    # swell: eerste sw seconden van het inkomende deel, omgekeerd, fade-in, -8 dB, onder de staart van cur
    swell=nxt[:, :n_sw][:, ::-1]*np.linspace(0,1,n_sw)**2*0.4
    cur=cur.copy(); cur[:, -n_sw:]+=swell
    # crossfade
    a=cur[:, -n_xf:]*np.linspace(1,0,n_xf); b=nxt[:, :n_xf]*np.linspace(0,1,n_xf)
    cur=np.concatenate([cur[:, :-n_xf], a+b, nxt[:, n_xf:]], axis=1)
sf.write('tmp_join2.wav', cur.T, SR)
subprocess.run(['ffmpeg','-loglevel','error','-y','-i','tmp_join2.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=9','-c:a','pcm_s16le',out],check=True)
subprocess.run(['ffmpeg','-loglevel','error','-y','-i',out,'-c:a','libmp3lame','-b:a','256k',out.replace('.wav','.mp3')],check=True)
print('done', subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out],capture_output=True,text=True).stdout.strip())
