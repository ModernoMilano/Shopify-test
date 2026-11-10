"""Hele keten voor een nieuwe take: analyze -> align -> linecheck -> fixonset -> monotoon maken -> joinplan -> join2 ->
tighten -> tijdlijn (absolute tijden) -> mp3 -> kopie naar ~/tb/rapvid.
Gebruik: python3 chain.py PREFIX P1 P2 ... [--tails 1.0,1.0,1.0,3.5] [--bpm 90] [--skip-analyze]
Verwacht per deel <P>.mp3 en lyr_<P>.txt (alleen regels, geen tags)."""
import sys, json, subprocess, re, os, shutil
args = sys.argv[1:]
tails = [1.0]; bpm = 90.0; skip = False
if '--tails' in args: i = args.index('--tails'); tails = [float(x) for x in args[i+1].split(',')]; del args[i:i+2]
if '--bpm' in args: i = args.index('--bpm'); bpm = float(args[i+1]); del args[i:i+2]
if '--skip-analyze' in args: args.remove('--skip-analyze'); skip = True
noonset=[]; firstfix={}; onsetat={}
if '--onsetat' in args: i=args.index('--onsetat'); onsetat={kv.split('=')[0]: float(kv.split('=')[1]) for kv in args[i+1].split(',')}; del args[i:i+2]
if '--noonset' in args: i=args.index('--noonset'); noonset=args[i+1].split(','); del args[i:i+2]
if '--firstfix' in args: i=args.index('--firstfix'); firstfix={kv.split('=')[0]: float(kv.split('=')[1]) for kv in args[i+1].split(',')}; del args[i:i+2]
prefix, parts = args[0], args[1:]
if len(tails) < len(parts): tails = tails + [tails[-1]] * (len(parts) - len(tails))
def run(cmd, log=None):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if log: open(log, 'a').write(r.stdout + r.stderr)
    return r.stdout + r.stderr
lc = f'linecheck_{prefix}.log'; open(lc, 'w').close()
for p in parts:
    if not skip or not os.path.exists(f'done_{p}.flag'): run(f'python3 analyze.py {p}', f'analyze_{p}.log')
    run(f'python3 align.py {p} lyr_{p}.txt', f'align_{prefix}.log')
    open(lc, 'a').write(f'== {p}\n'); run(f'python3 linecheck.py {p} lyr_{p}.txt', lc)
    if p in onsetat: run(f'python3 fixonset.py {p} {onsetat[p]}', f'onset_{prefix}.log')
    elif p not in noonset: run(f'python3 fixonset.py {p}', f'onset_{prefix}.log')
    else: open(f'onset_{prefix}.log','a').write(f'{p} onset fix skipped\n')
    W = json.load(open(f'words_{p}.json'))
    for a, b in zip(W, W[1:]):  # monotoon: een woord begint nooit voor het einde van het vorige
        if b['t0'] < a['t1']: b['t0'] = round(a['t1'], 2)
        if b['t1'] < b['t0'] + 0.12: b['t1'] = round(b['t0'] + 0.12, 2)
    json.dump(W, open(f'words_{p}.json', 'w'), indent=0)
plan = {"xfade": 0.35, "swell": 1.2, "parts": []}
for p, tail in zip(parts, tails):
    W = json.load(open(f'words_{p}.json'))
    plan['parts'].append({"wav": p + ".wav", "mp3": p + ".mp3", "first": firstfix.get(p, W[0]['t0']), "last": W[-1]['t1'], "lead": 0.3, "tail": tail})
json.dump(plan, open(f'joinplan_{prefix}.json', 'w'), indent=1)
jl = run(f'python3 join2.py joinplan_{prefix}.json song_{prefix}_raw.wav'); open(f'join_{prefix}.log', 'w').write(jl)
cuts = {}
for m in re.finditer(r'(\S+)\.mp3 tempo ([\d.]+) cut ([\d.]+) ([\d.]+) len ([\d.]+)', jl):
    cuts[m.group(1)] = (float(m.group(3)), float(m.group(4)), float(m.group(5)))
xf = plan['xfade']; words = []; lines = []; off = 0.0
for k, p in enumerate(parts):
    t0, t1, ln = cuts[p]
    W = json.load(open(f'words_{p}.json'))
    for w in W: words.append({"w": w['w'], "t0": round(w['t0'] - t0 + off, 2), "t1": round(w['t1'] - t0 + off, 2), "part": p})
    off += ln - xf
json.dump(words, open(f'timeline_words_{prefix}_raw.json', 'w'))
tl = run(f'python3 tighten.py song_{prefix}_raw.wav timeline_words_{prefix}_raw.json song_{prefix}.wav {bpm} 1.6 1.0')
open(f'join_{prefix}.log', 'a').write(tl)
C = json.load(open(f'song_{prefix}.wav.cuts.json'))
def remap(t):
    d = 0.0
    for c in C:
        if t >= c['end']: d += c['end'] - c['start']
        elif t > c['start']: d += t - c['start']
    return round(t - d, 2)
for w in words: w['t0'], w['t1'] = remap(w['t0']), remap(w['t1'])
json.dump(words, open(f'timeline_words_{prefix}.json', 'w'))
# regels: in volgorde van de lyr-bestanden, woordaantal per regel
wi = 0; n = 0
for p in parts:
    for line in [l for l in open(f'lyr_{p}.txt').read().splitlines() if l.strip()]:
        cnt = len([t for t in re.findall(r"[A-Za-z0-9'’]+[.,:!?]*", line) if re.sub(r"[^a-z0-9']", '', t.lower())])
        ws = words[wi:wi + cnt]; wi += cnt; n += 1
        lines.append({"n": n, "t0": ws[0]['t0'], "t1": ws[-1]['t1'], "text": line, "part": p})
json.dump(lines, open(f'timeline_lines_{prefix}.json', 'w'))
run(f'ffmpeg -loglevel error -y -i song_{prefix}.wav -c:a libmp3lame -b:a 256k song_{prefix}.mp3')
for f in [f'song_{prefix}.mp3', f'timeline_words_{prefix}.json', f'timeline_lines_{prefix}.json']: shutil.copy(f, os.path.expanduser('~/tb/rapvid/'))
dur = run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 song_{prefix}.wav').strip()
print('JOIN:', jl.strip().replace('\n', ' | ')); print('TIGHTEN:', tl.strip()); print('DURATION', dur, 'lines', n, 'words', len(words), 'consumed', wi)
print('LAST LINE', lines[-1])
open(f'done_{prefix}.flag', 'w').write('ok')
