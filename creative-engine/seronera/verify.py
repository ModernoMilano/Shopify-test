# Final gate: sizes, 1:1 pixel-identical to the 9:16 crop, safe-zone report clean, contrast passes.
import json, numpy as np
from PIL import Image
rep={r['id']:r for r in json.load(open('out/report.json'))}
con={i:r for i,r in json.load(open('out/contrast.json'))}
allok=True
for n in sorted(rep):
    a=Image.open(f'out/seronera_ad{n}_9x16.png'); b=Image.open(f'out/seronera_ad{n}_1x1.png')
    A=np.asarray(a.convert('RGB')); B=np.asarray(b.convert('RGB'))
    exact=a.size==(1080,1920) and b.size==(1080,1080) and np.array_equal(A[219:1299],B)
    safe=not rep[n]['issues']; c=all(v['ok'] for v in con[n].values())
    allok&=exact and safe and c
    print(f"ad{n}: 1:1 == crop(y219) pixel-identical: {exact} | safe-zone issues: {rep[n]['issues'] or 'none'} | contrast headline {con[n]['headline']['worst5']:.2f} sub {con[n]['sub']['worst5']:.2f} -> {'PASS' if exact and safe and c else 'FAIL'}")
print('ALL PASS' if allok else 'SOME FAIL')
