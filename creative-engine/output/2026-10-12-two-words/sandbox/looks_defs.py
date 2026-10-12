# Oude-camerafilters als ffmpeg-filterketens: naam -> (titel, uitleg, keten). Dezelfde keten voor stills en video.
# Cinestill: de gloed (halation) wordt in gbrp gemengd; in yuv420p of rgb24 kleurt blend=screen de chroma magenta.
LOOKS = {
 "kodachrome": ("Kodachrome 64", "warm, rijk rood, diepe zwarten, fijne korrel",
   "curves=r='0/0 0.25/0.22 0.5/0.53 0.75/0.8 1/1':g='0/0 0.25/0.23 0.5/0.5 0.75/0.76 1/1':b='0/0.03 0.25/0.22 0.5/0.46 0.75/0.72 1/0.95',"
   "colorbalance=rs=0.06:bs=-0.07:rm=0.04:bm=-0.04:rh=0.03:bh=-0.02,eq=saturation=1.22:contrast=1.1,noise=c0s=7:c0f=t+u,vignette=PI/4.8"),
 "portra": ("Portra 400", "zacht, warme huid, opgelichte zwarten, pastel",
   "curves=all='0/0.07 0.25/0.28 0.5/0.53 0.75/0.77 1/0.96',colorbalance=rs=0.07:gs=0.03:bs=-0.07:rm=0.03:bm=-0.03:rh=0.04:bh=-0.04,"
   "eq=saturation=0.88:contrast=0.95,noise=c0s=11:c0f=t+u,vignette=PI/5.5"),
 "cinestill": ("Cinestill 800T", "nachtfilm: koele schaduwen, warme lichten met gloed",
   "split=2[base][hl];[hl]lutyuv=y='clip((val-185)*4,0,255)':u=128:v=128,gblur=sigma=18,colorchannelmixer=rr=1:gg=0.45:bb=0.2,format=gbrp[glow];"
   "[base]format=gbrp[b];[b][glow]blend=all_mode=screen:all_opacity=0.55,format=yuv420p,colorbalance=rs=-0.04:bs=0.07:rh=0.06:bh=-0.06,eq=saturation=1.05,noise=c0s=13:c0f=t+u,vignette=PI/5"),
 "16mm": ("16 mm Ektachrome", "documentaire 16 mm: zichtbare korrel, iets zachter, koeler groen",
   "gblur=sigma=0.7,curves=all='0/0.02 0.3/0.26 0.7/0.74 1/0.98',colorbalance=gs=0.03:bm=-0.02:rh=0.02,eq=contrast=1.05,noise=c0s=20:c0f=t+u,vignette=PI/4.5"),
 "faded": ("Verbleekte print", "jaren-70 afdruk: opgelicht, warm, gedempt, vergeelde lichten",
   "curves=all='0/0.08 0.5/0.5 1/0.94',colorbalance=rs=0.02:gs=0.04:bs=-0.06:rh=0.06:gh=0.03:bh=-0.08,eq=saturation=0.8,noise=c0s=9:c0f=t+u,vignette=PI/5"),
 "trix": ("Tri-X 400 zwart-wit", "contrastrijk zwart-wit met korrel",
   "hue=s=0,curves=all='0/0 0.25/0.21 0.75/0.8 1/1',noise=c0s=16:c0f=t+u,vignette=PI/5"),
}
