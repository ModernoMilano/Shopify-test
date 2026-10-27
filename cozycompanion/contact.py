import json, sys, io, ssl, urllib.request, os
from PIL import Image
S = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(S, "files.json")))
names = sys.argv[2:]; out = sys.argv[1]
ctx = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
W = 420; cols = 3
ims = []
for n in names:
    u = "https://" + os.environ["COZY_SHOPIFY_DOMAIN"] + "/cdn/shop/files/" + reg[n]["url"].split("/files/")[-1].split("?")[0] + "?width=600"
    im = Image.open(io.BytesIO(urllib.request.urlopen(u, context=ctx).read())).convert("RGB")
    im.thumbnail((W, W)); ims.append(im)
rows = (len(ims) + cols - 1) // cols
c = Image.new("RGB", (W * cols, W * rows), "white")
for k, im in enumerate(ims): c.paste(im, ((k % cols) * W, (k // cols) * W))
c.save(out, quality=85)
