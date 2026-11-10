import sys, subprocess, os
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]).decode().strip())
times=[]; t=1.0
while t < dur-0.2:
    times.append(t); t+=2.0
frames=[]
for i,t in enumerate(times):
    fn=f'{out}/f{i:03d}.jpg'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t:.2f}','-i',src,'-frames:v','1','-vf','scale=288:512',fn],check=True)
    frames.append((t,fn))
try:
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',16)
except Exception:
    font=ImageFont.load_default()
for s in range(0,len(frames),4):
    g=frames[s:s+4]; im=Image.new('RGB',(288*len(g),512)); d=ImageDraw.Draw(im)
    for j,(t,fn) in enumerate(g):
        im.paste(Image.open(fn),(j*288,0))
        d.rectangle([j*288,0,j*288+58,20],fill=(0,0,0)); d.text((j*288+4,2),f'{t:.0f}s',fill=(255,255,0),font=font)
    name=f'{out}/strip{s//4+1:02d}_{g[0][0]:.0f}s-{g[-1][0]:.0f}s.jpg'
    im.save(name,quality=62,optimize=True); print(name,os.path.getsize(name))
print('frames',len(frames),'dur',round(dur,2),'klaar')
