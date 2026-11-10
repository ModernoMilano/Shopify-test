"""Corrigeer het begin van een deel: whisper zonder VAD smeert de eerste woorden soms over een instrumentale intro.
Gebruik: python3 fixonset.py <part>. Bepaalt met VAD de echte start van het eerste woord en schuift de woorden die
daarvoor liggen naar een gelijkmatige verdeling tot het eerste 'betrouwbare' woord."""
import json, sys
from faster_whisper import WhisperModel
part=sys.argv[1]
m=WhisperModel("small", device="cpu", compute_type="int8")
segs,_=m.transcribe(part+'.wav', language='en', word_timestamps=True, vad_filter=True, beam_size=5)
vw=[(w.word.strip(), float(w.start), float(w.end)) for s in segs for w in (s.words or [])]
true0=vw[0][1] if vw else 0.0
if len(sys.argv)>2: true0=float(sys.argv[2])
for fn in ['words_%s.json'%part]:
    W=json.load(open(fn)); 
    if W and W[0]['t0'] < true0-0.8:
        # alle woorden die eindigen voor true0+0.3 opnieuw verdelen tussen true0 en het eerste woord dat na true0 begint
        k=0
        while k<len(W) and W[k]['t0'] < true0: k+=1
        n=k; end=W[k]['t0'] if k<len(W) else true0+ n*0.35
        if n>0:
            span=max(0.3*n, end-true0); step=span/n
            for i in range(n): W[i]['t0']=round(true0+i*step,2); W[i]['t1']=round(true0+(i+1)*step-0.02,2)
        json.dump(W,open(fn,'w'),indent=0); print(part,'onset corrected: first word now',W[0]['t0'],'(vad',round(true0,2),') shifted',n,'words')
    else: print(part,'onset ok', W[0]['t0'] if W else None, 'vad', round(true0,2))
T=json.load(open('transcripts.json')); T[part]['vad_first']=round(true0,2); json.dump(T,open('transcripts.json','w'),indent=1)
