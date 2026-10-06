# WCAG contrast of each text line against the real background behind it (worst 5% of pixels).
import json, numpy as np
from PIL import Image
ads={a['id']:a for a in json.load(open('ads.json'))}
rep=json.load(open('out/report.json'))
def lum(rgb):
    c=np.asarray(rgb,dtype=float)/255; c=np.where(c<=0.03928,c/12.92,((c+0.055)/1.055)**2.4)
    return 0.2126*c[...,0]+0.7152*c[...,1]+0.0722*c[...,2]
def hx(h): return [int(h[i:i+2],16) for i in (1,3,5)]
def cr(a,b): a,b=max(a,b),min(a,b); return (a+0.05)/(b+0.05)
out=[]
for r in rep:
    a=ads[r['id']]; dark=a['theme']=='dark'
    bg=np.asarray(Image.open(f"chk/bgonly_{a['id']}.png").convert('RGB'))
    cols={'headline':'#EFECEC' if dark else '#252525','sub':a.get('subColor',('#C8AE78' if dark else '#4A4436'))}
    res={}
    for k,need in (('headline',3.0),('sub',4.5)):
        x0,y0,x1,y1=[int(round(v)) for v in r['parts'][k]]
        L=lum(bg[y0:y1,x0:x1]).ravel(); t=lum(np.array(hx(cols[k])))
        # worst case: text darker than bg -> darkest 5% of bg pixels; text lighter -> brightest 5%
        worst=np.percentile(L,5) if t<np.median(L) else np.percentile(L,95)
        c_med=cr(t,np.median(L)); c_w=cr(t,worst)
        res[k]={'median':round(c_med,2),'worst5':round(c_w,2),'need':need,'ok':bool(c_w>=need)}
    out.append((r['id'],res))
    print(r['id'],{k:(v['median'],v['worst5'],'OK' if v['ok'] else 'FAIL<%s'%v['need']) for k,v in res.items()})
json.dump(out,open('out/contrast.json','w'),indent=1)
