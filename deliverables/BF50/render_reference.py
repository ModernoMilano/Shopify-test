from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageStat
import numpy as np, sys
F='/home/user/bw/f/'; W,H=2160,3840; SQ0,SQ1=840,3000
CREAM=(240,232,220); SUBC=(214,206,195); INK=(24,20,17); MUTE=(92,84,76)
O='/home/user/bw/bf50/out/'; S='/home/user/bw/bf50/src/'
_fc={}
def font(name,size,axes):
    k=(name,size,tuple(axes))
    if k not in _fc:
        f=ImageFont.truetype(F+name+'.ttf',size); f.set_variation_by_axes(list(axes)); _fc[k]=f
    return _fc[k]
def ITAL(s): return font('CormorantItalic',s,[400])
def CORM(s): return font('CormorantGaramond',s,[500])
def INTER(s,w=400): return font('Inter',s,[min(32,max(14,s//2)),w])
def MONT(s,w=800): return font('Montserrat',s,[w])
def tlen(s,f,tr=0):
    d=ImageDraw.Draw(Image.new('L',(1,1)))
    return d.textlength(s,font=f)+(tr*(len(s)-1) if tr else 0)
def dt(im,s,cx,y,f,fill,tr=0):
    d=ImageDraw.Draw(im); x=cx-tlen(s,f,tr)/2
    if not tr: d.text((x,y),s,font=f,fill=fill); return
    for c in s: d.text((x,y),c,font=f,fill=fill); x+=d.textlength(c,font=f)+tr
def logo_img(w,col):
    a=Image.open('/home/user/bw/logo/logo_inv.png').convert('RGBA'); a=a.crop(a.getchannel('A').getbbox())
    r=w/a.size[0]; a=a.resize((w,int(a.size[1]*r)),Image.LANCZOS)
    c=Image.new('RGBA',a.size,col+(0,)); c.putalpha(a.getchannel('A')); return c
def src(n): return ImageOps.fit(Image.open(S+'%s.png'%n).convert('RGB'),(W,H),Image.LANCZOS)
def lum(im,box): return ImageStat.Stat(im.convert('L').crop(box)).mean[0]
def place(im,s=1.0,dy=0,k=0.92,vig=True):
    """shrink the photo onto its own (dark or light) border colour with a soft feather; dy in fraction of H"""
    rgb=im.convert('RGB')
    if s>=0.999 and dy==0: out=rgb
    else:
        w,h=int(W*s),int(H*s); sm=rgb.resize((w,h),Image.LANCZOS); a=np.asarray(rgb).astype(float)
        border=np.concatenate([a[:40].reshape(-1,3),a[-40:].reshape(-1,3),a[:,:40].reshape(-1,3),a[:,-40:].reshape(-1,3)])
        col=tuple(int(v*k) for v in np.median(border,0))
        out=Image.new('RGB',(W,H),col); top=(H-h)//2+int(H*dy); l=(W-w)//2
        m=Image.new('L',(w,h),0); d=ImageDraw.Draw(m); fe=260
        for i in range(fe): d.rectangle([i,i,w-1-i,h-1-i],outline=int(255*(i/fe)**1.5))
        d.rectangle([fe,fe,w-1-fe,h-1-fe],fill=255); out.paste(sm,(l,top),m)
    if vig:
        yy,xx=np.mgrid[0:H,0:W]; r=np.sqrt(((xx-W/2)/(W*0.62))**2+((yy-H*0.42)/(H*0.55))**2)
        v=np.clip(1-0.5*np.clip(r-0.6,0,1)**1.4,0.4,1)[...,None]
        out=Image.fromarray((np.asarray(out).astype(float)*v).astype(np.uint8))
    return out
def top(im,label,col,y0=SQ0+28,lw=600):
    lg=logo_img(lw,col); im.alpha_composite(lg,(W//2-lg.size[0]//2,y0)); y=y0+lg.size[1]+30
    if label: dt(im,label,W//2,y,INTER(36,600),col,tr=int(36*0.42)); y+=46
    return y
def bottom(im,head,sub,btn,col,subc,btncol,btntxt,style='ital',bottom=SQ1-40):
    if style=='bold':
        hs=170; hf=MONT(hs); tr=int(hs*0.04)
        while max(tlen(l,hf,tr) for l in head)>1840: hs-=8; hf=MONT(hs); tr=int(hs*0.04)
        lh=int(hs*1.08)
    else:
        hs=200; hf=ITAL(hs); tr=0
        while max(tlen(l,hf) for l in head)>1820: hs-=8; hf=ITAL(hs)
        lh=int(hs*1.0)
    sf=INTER(52,400); slh=int(52*1.45); bf=INTER(42,700); btr=int(42*0.32); bh=148
    hh=lh*len(head)+int(hs*0.2); sh=slh*len(sub); g1=26; g2=58 if btn else 0
    total=hh+g1+sh+g2+(bh if btn else 0); y=bottom-total; t=y
    for l in head: dt(im,l,W//2,y,hf,col,tr=tr); y+=lh
    y+=int(hs*0.2)+g1
    for l in sub: dt(im,l,W//2,y,sf,subc); y+=slh
    if btn:
        y+=g2; bw=int(tlen(btn,bf,btr))+192; x0=W//2-bw//2
        ImageDraw.Draw(im).rectangle([x0,y,x0+bw,y+bh],fill=btncol)
        a,dsc=bf.getmetrics(); dt(im,btn,W//2,y+(bh-(a+dsc))//2+4,bf,btntxt,tr=btr)
    return t
def ugc(im,lines,y=SQ0+30):
    f=INTER(84,600); lh=112; pad=40
    ww=max(tlen(l,f) for l in lines)+2*pad+20; hh=lh*len(lines)+2*pad-10
    box=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(box).rounded_rectangle([W//2-ww/2,y,W//2+ww/2,y+hh],radius=26,fill=(255,255,255,240)); im.alpha_composite(box)
    yy=y+pad-6
    for l in lines: dt(im,l,W//2,yy,f,(17,17,17)); yy+=lh
def save(im,name):
    rgb=im.convert('RGB'); s=rgb.resize((1080,1920),Image.LANCZOS)
    s.save(O+'MM_BF_%s_916.jpg'%name,quality=95); s.crop((0,420,1080,1500)).save(O+'MM_BF_%s_11.jpg'%name,quality=95); return s
def render(n,name,mode,head=None,sub=(),btn=None,label=None,s=1.0,dy=0,style='ital',caption=None,vig=None):
    dark = mode=='dark'
    im=place(src(n),s,dy,vig=(dark if vig is None else vig)).convert('RGBA')
    if mode=='clean': return save(im,name)
    if mode=='logo':
        c=CREAM if lum(im,(700,SQ0+40,1460,SQ0+200))<130 else INK; top(im,None,c,lw=420); return save(im,name)
    if mode=='ugc': ugc(im,caption); return save(im,name)
    col,subc,bc,bt=(CREAM,SUBC,CREAM,INK) if dark else (INK,MUTE,INK,CREAM)
    top(im,label,col); bottom(im,head,list(sub),btn,col,subc,bc,bt,style=style)
    return save(im,name)
