"""Download Shopify-hosted generations and build a QA sheet: generation (big) next to the product packshot.
usage: qa_view.py <files.json name>:<packshot handle or -> ...   -> prints sheet path(s)"""
import sys, os, io, json, ssl, urllib.request
from PIL import Image, ImageDraw
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = "/tmp/claude-0/-home-user-Shopify-test/7ae2a11e-4ae5-5a99-ac75-b7957d6a039d/scratchpad/bfcm"
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt"); D = os.environ["COZY_SHOPIFY_DOMAIN"]
reg = json.load(open(os.path.join(S, "files.json")))
def get(name):
    path = f"{P}/{name}.png"
    if not os.path.exists(path):
        f = reg[name]["url"].split("/files/")[-1].split("?")[0]
        open(path, "wb").write(urllib.request.urlopen(f"https://{D}/cdn/shop/files/{f}", context=CTX).read())
    return path
for arg in sys.argv[1:]:
    name, pack = arg.split(":")
    im = Image.open(get(name)).convert("RGB"); im.thumbnail((1100, 1100))
    W = im.width + (360 if pack != "-" else 0); g = Image.new("RGB", (W, max(im.height, 380)), "white"); g.paste(im, (0, 0))
    if pack != "-":
        pk = Image.open(f"{P}/pack_{pack}.jpg").convert("RGB"); pk.thumbnail((350, 350)); g.paste(pk, (im.width + 5, 0))
    ImageDraw.Draw(g).text((6, 6), name, fill="red")
    out = f"{P}/qa_{name}.jpg"; g.save(out, quality=88); print(out)
