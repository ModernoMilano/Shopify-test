# Contact sheet of raw backgrounds with guides: green = key area, red = 1:1 crop, yellow = text/product/CTA bands.
import sys
from PIL import Image, ImageDraw
def norm(p):
    im=Image.open(p).convert('RGB'); w,h=im.size
    s=max(1080/w,1920/h); im=im.resize((round(w*s),round(h*s)),Image.LANCZOS)
    W,H=im.size; l=(W-1080)//2; t=(H-1920)//2
    return im.crop((l,t,l+1080,t+1920))
def guide(im):
    im=im.copy(); d=ImageDraw.Draw(im)
    d.rectangle((65,284,1015,1234),outline=(0,255,0),width=6)
    d.rectangle((2,219,1078,1299),outline=(255,0,0),width=4)
    for y in (519,1049): d.line((0,y,1080,y),fill=(255,255,0),width=3)
    return im
if __name__ == '__main__':
    out, ids = sys.argv[1], sys.argv[2:]
    thumbs=[]
    for n in ids:
        g=guide(norm(f'bg/{n}.png')).resize((270,480),Image.LANCZOS)
        ImageDraw.Draw(g).text((8,6),n,fill=(255,255,255))
        thumbs.append(g)
    sheet=Image.new('RGB',(274*len(thumbs),480),'black')
    for i,t in enumerate(thumbs): sheet.paste(t,(i*274,0))
    sheet.save(out,quality=82)
