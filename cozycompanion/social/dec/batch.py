import json, sys
P = json.load(open('plan.json')); a, b = int(sys.argv[1]), int(sys.argv[2])
only = set(sys.argv[3].split(',')) if len(sys.argv) > 3 else None
out = []
for i in range(a, min(b, len(P))):
    p = P[i]
    if only and p['key'] not in only: continue
    r = {'index': i, 'params': {'model': 'nano_banana_2_1', 'resolution': '2k', 'aspect_ratio': p['aspect'], 'thinking_level': 'high', 'prompt': p.get('prompt2') or p['prompt']}}
    if p['media']: r['params']['medias'] = [{'value': p['media'], 'role': 'image_references'}]
    out.append(r)
print(json.dumps(out, ensure_ascii=False))
