import json, sys
P = json.load(open('plan.json'))
out = []
for i in map(int, sys.argv[1].split(',')):
    p = P[i]
    r = {'index': i, 'params': {'model': 'nano_banana_2_1', 'resolution': '2k', 'aspect_ratio': p['aspect'], 'thinking_level': 'high', 'prompt': p.get('prompt2') or p['prompt']}}
    if p['media']: r['params']['medias'] = [{'value': p['media'], 'role': 'image_references'}]
    out.append(r)
print(json.dumps(out, ensure_ascii=False))
