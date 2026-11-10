"""Download clips naar clips3/<name>.mp4 en maak strips. Gebruik: python3 dl3.py urls.json  (urls.json = {name: url})"""
import json, sys, subprocess, os
from concurrent.futures import ThreadPoolExecutor
U = json.load(open(sys.argv[1])); os.makedirs('clips3', exist_ok=True)
def get(item):
    name, url = item; out = f'clips3/{name}.mp4'
    if os.path.exists(out) and os.path.getsize(out) > 10000: return name, 'had'
    r = subprocess.run(['curl', '-sS', '-o', out, url]); return name, 'ok' if r.returncode == 0 else 'fail'
with ThreadPoolExecutor(6) as ex: res = list(ex.map(get, U.items()))
print(res)
subprocess.run(['python3', 'strip.py'] + [f'clips3/{n}.mp4' for n, _ in res])
