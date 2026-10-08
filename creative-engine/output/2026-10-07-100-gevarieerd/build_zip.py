"""Bouwt de zip met de 100 gevarieerde beelden uit final100.tsv (draait in de Higgsfield-sandbox).

Verwacht de bron-PNG's in src/<id>.png. Retouches: P11 (twee wazige figuren achtergrond),
(v2: randdetectie herkent nu ook afgeronde filmhoeken en witte printranden)
A24 (klein embleem op de auto), O03 en A25 (bovenrand bijgesneden, 4:5 behouden), plus randen <40px.
"""
import os, zipfile, numpy as np
from PIL import Image, ImageDraw, ImageFilter
def heal(g, cx, cy, rx, ry, pad=80, seed=7):
    a=np.asarray(g).astype(np.float32)
    x0,y0,x1,y1=max(cx-rx-pad,0),max(cy-ry-pad,0),min(cx+rx+pad,a.shape[1]),min(cy+ry+pad,a.shape[0])
    win=a[y0:y1,x0:x1].copy()
    m=Image.new('L',(x1-x0,y1-y0),0); ImageDraw.Draw(m).ellipse((cx-rx-x0,cy-ry-y0,cx+rx-x0,cy+ry-y0),fill=255)
    M=np.asarray(m)>0; f=win.copy(); f[M]=win[~M].mean(0)
    for _ in range(2500):
        avg=(np.roll(f,1,0)+np.roll(f,-1,0)+np.roll(f,1,1)+np.roll(f,-1,1))/4; f[M]=avg[M]
    hp=win-np.asarray(Image.fromarray(win.astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(np.float32)
    sd=hp[~M].std(); rng=np.random.default_rng(seed)
    noise=np.asarray(Image.fromarray(np.clip(rng.normal(128,sd*1.2,f.shape[:2]),0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32)-128
    f=f+noise[...,None]; soft=(np.asarray(m.filter(ImageFilter.GaussianBlur(6))).astype(np.float32)/255)[...,None]
    a[y0:y1,x0:x1]=win*(1-soft)+f*soft
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def border(g, cap=0.035):
    """Filmrand per kant (t, b, l, r) in px. Alleen een kant waarvan de buitenste 3 lijnen voor minstens 60%
    bijna zwart (<22) of bijna wit (>246) zijn telt als rand; dan naar binnen tot die kleur onder 1% van de
    lijn zakt (zo gaan ook golvende, afgeronde filmhoeken mee), maximaal cap van de afmeting, plus 6 px."""
    a=np.asarray(g.convert('L')).astype(np.int16); h,w=a.shape
    out=[]
    for get,n in [(lambda i:a[i],h),(lambda i:a[h-1-i],h),(lambda i:a[:,i],w),(lambda i:a[:,w-1-i],w)]:
        k=0
        for m in (lambda x:x<22, lambda x:x>246):
            if min(m(get(j)).mean() for j in range(3))>=0.6:
                lim=int(n*cap); k=0
                while k<lim and m(get(k)).mean()>=0.01: k+=1
                k+=6; break
        out.append(k)
    return tuple(out)
def fit(g,x0,y0,x1,y1,W,H):
    cw,ch=x1-x0,y1-y0
    if cw/ch>W/H: nw=round(ch*W/H); x0+=(cw-nw)//2; x1=x0+nw
    else: nh=round(cw*H/W); y0+=(ch-nh)//2; y1=y0+nh
    return g.crop((x0,y0,x1,y1)).resize((W,H),Image.LANCZOS)
DIR='ModernoMilano 100 beelden'; os.makedirs(DIR,exist_ok=True); os.makedirs('prev',exist_ok=True); log=[]
thumbs=[]; cropped=[]
for line in open('final100.tsv', encoding='utf-8'):
    n,i,title,fn=line.rstrip('\n').split('\t'); n=int(n)
    g=Image.open(f'src/{i}.png').convert('RGB'); W,H=g.size
    if i=='P11': g=heal(g,80,760,72,78); g.crop((0,600,400,950)).save('prev/P11.jpg',quality=80)
    if i=='A24': g=heal(g,1401,1819,16,14,pad=40); g.crop((1300,1740,1500,1900)).resize((400,320)).save('prev/A24.jpg',quality=80)
    if i=='O03': g=fit(g,int(W*.03),int(H*.06),W-int(W*.03),H,W,H); log.append('O03 crop top')
    if i=='A25': g=fit(g,158,196,W,H,W,H); g.crop((0,0,600,400)).save('prev/A25.jpg',quality=80); log.append('A25 crop')
    t,b,l,r=border(g)
    if t or b or l or r:
        before=g.resize((150,186))
        g=fit(g,l,t,W-r,H-b,W,H); log.append(f'{i}: rand t{t} b{b} l{l} r{r}')
        cropped.append((i,before,g.resize((150,186))))
    g.save(f'{DIR}/{n:03d} {title}.jpg',quality=95); thumbs.append(g.resize((150,186)))
grid=Image.new('RGB',(1500,1860),'white')
for k,t in enumerate(thumbs): grid.paste(t,((k%10)*150,(k//10)*186))
grid.save('prev/grid.jpg',quality=55)
if cropped:
    cols=8; rows=(len(cropped)+3)//4
    sheet=Image.new('RGB',(cols*150,rows*200),'white'); d=ImageDraw.Draw(sheet)
    for k,(i,bf,af) in enumerate(cropped):
        x=(k%4)*300; y=(k//4)*200
        sheet.paste(bf,(x,y+12)); sheet.paste(af,(x+150,y+12)); d.text((x+2,y),f'{i} voor / na',fill='black')
    sheet.save('prev/cropped.jpg',quality=60)
with zipfile.ZipFile('out.zip','w',zipfile.ZIP_STORED) as z:
    for f in sorted(os.listdir(DIR)): z.write(f'{DIR}/{f}',f'{DIR}/{f}')
print('\n'.join(log)); print(len(os.listdir(DIR)),'files'); print('MB',round(os.path.getsize('out.zip')/1e6,1))
