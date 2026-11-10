"""Montageplan voor tekst v3: regel -> keyframe (shots_v3_map), shottijden uit timeline_lines_Z.json, cliplengte 3/4/5 s
(nooit korter dan het shot), hergebruik van bestaande clips in clips2/ als ze lang genoeg zijn.
Gebruik: python3 plan_v3.py timeline_lines_Z.json keyframes.json -> schrijft plan_v3_full.json en clip_requests_v3.json"""
import json, sys, os, subprocess
SEQ = ['K44','K02','K03','K35','K25', 'K08','K17','K07','K09','K10','K11','K13','K14','K15','K12','K06',
 'K18','K05','K19r','K20','K21r','K22','K23','K25b','K26','K33r','K27r','K32','K28','K29',
 'K01','K30','K24','K38','K25','K38b','K42','K43','K41','K14','K36','K37','K17','K34','K40','K01','K39','K45',
 'K46r','K47','K31','K56','K48','K50','K51','K53','K54','K55','K52','K58','K59']
L = json.load(open(sys.argv[1])); ids = json.load(open(sys.argv[2]))
assert len(SEQ) == len(L), (len(SEQ), len(L))
def idfor(k): return ids.get(k)
# te lange shots (> 5 s): splitsen in twee keyframes, of (zonder split) afkappen op 5,0 s en het volgende shot eerder laten beginnen
SPLIT = {11: ['K11','K16'], 12: ['K13','K04'], 13: ['K14','K05']}
end_t = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','song_Z.mp3'],capture_output=True,text=True).stdout or 203)
shots = []
for i, l in enumerate(L):
    t0 = l['t0'] if i > 0 else 0.0
    t1 = L[i+1]['t0'] if i+1 < len(L) else l['t1']
    shots.append([l['n'], SEQ[i], round(t0,2), round(t1,2)])
# te lange shots (> 5 s) splitsen: de eerste 5 s op de keyframe, de rest op de volgende shot naar voren halen is niet mogelijk,
# dus hier worden ze gemeld en krijgt het shot een tweede clip van hetzelfde keyframe met andere offset (zelfde clip twee keer kan niet: lengte).
fixed = []
for idx, s in enumerate(shots):
    n, k, t0, t1 = s
    if t1 - t0 > 5.0:
        if n in SPLIT:
            a, b = SPLIT[n]; mid = round(t0 + 3.0, 2)
            fixed.append([n, a, t0, mid]); fixed.append([n, b, mid, t1]); print('SPLIT', n, a, b, t0, mid, t1)
        else:
            cap = round(t0 + 5.0, 2); fixed.append([n, k, t0, cap])
            if idx + 1 < len(shots): shots[idx+1][2] = cap
            print('CAP', n, k, t0, cap, '(next starts earlier)')
    else: fixed.append(s)
shots = fixed
# eindbeeld K60 na de laatste regel
if shots[-1][1] != 'K60': shots.append([60, 'K60', shots[-1][3], round(end_t,2)])
def clip_len(d): return 3 if d <= 2.9 else (4 if d <= 3.9 else 5)
reqs = []; plan_shots = []; reuse = []
used = {}
for n, k, t0, t1 in shots:
    d = t1 - t0; cl = clip_len(d)
    name = k if k not in used else f'{k}_{used[k]+1}'
    used[k] = used.get(k, 0) + 1
    existing = f'clips2/{k}.mp4'
    have = None
    if os.path.exists(existing) and used[k] == 1:
        dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',existing],capture_output=True,text=True).stdout or 0)
        if dur >= d - 0.02: have = existing; reuse.append((n, k, round(d,2), round(dur,2)))
    if have: plan_shots.append({"clip": have, "t0": t0, "t1": t1})
    else:
        plan_shots.append({"clip": f"clips3/{name}.mp4", "t0": t0, "t1": t1})
        reqs.append({"name": name, "key": k, "line": n, "dur": cl, "shot": round(d,2), "start_image": idfor(k)})
for s in plan_shots:
    if 'K59' in s['clip'] or 'K60' in s['clip']: s['overlay'] = 'end_overlay.png'
json.dump({"audio":"song_Z.mp3","words":"timeline_words_Z.json","end_hold":True,"end_t":round(end_t,2),"shots":plan_shots}, open('plan_v3_full.json','w'), indent=1)
json.dump(reqs, open('clip_requests_v3.json','w'), indent=1)
print('shots', len(plan_shots), 'reuse', len(reuse), 'new clips', len(reqs), 'new clip seconds', sum(r['dur'] for r in reqs))
for r in reuse: print('  reuse', r)
