import sys, json, io, ssl, urllib.request, os
sys.path.insert(0, "/home/user/Shopify-test/cozycompanion")
from lib import DOMAIN
from PIL import Image, ImageDraw
reg = json.load(open("/home/user/Shopify-test/cozycompanion/files.json"))
C = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
names, out = sys.argv[2:], sys.argv[1]
th = []
for n in names:
    u = f"https://{DOMAIN}/cdn/shop/files/" + reg[n]["url"].split("/files/")[-1].split("?")[0]
    im = Image.open(io.BytesIO(urllib.request.urlopen(u, context=C).read())).convert("RGB")
    im.save(f"/home/user/Shopify-test/cozycompanion/ads/v2/raw_{n}.jpg", quality=95)
    w, h = im.size; d = ImageDraw.Draw(im); t = (h - w) // 2
    d.rectangle((0, t, w - 1, t + w), outline=(255, 0, 0), width=6)  # 1:1 crop area
    im.thumbnail((500, 900)); th.append(im)
g = Image.new("RGB", (510 * len(th), 900), "white")
for i, im in enumerate(th): g.paste(im, (i * 510, 0))
g.save(out, quality=88)
