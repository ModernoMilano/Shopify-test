"""QA sheet: packshot next to each preview. qa_sheet.py key[,key...] out.jpg"""
import json, os, sys, io, ssl, urllib.request
D = os.path.dirname(os.path.abspath(__file__)); SOC = os.path.dirname(D); S = os.path.dirname(SOC)
sys.path.insert(0, S)
from lib import DOMAIN
from PIL import Image, ImageDraw
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
res = json.load(open(os.path.join(D, "results.json"))); P = {p["key"]: p for p in json.load(open(os.path.join(D, "plan.json")))}
PACK = {}
for l in open("/tmp/claude-0/-home-user-Shopify-test/7ae2a11e-4ae5-5a99-ac75-b7957d6a039d/scratchpad/dec_packshots.txt"):
    d, h, u = l.split(); PACK[h] = u
cache = os.path.join(SOC, ".tmp", "packs"); os.makedirs(cache, exist_ok=True)
def pack(h):
    if not h: return Image.new("RGB", (300, 300), "white")
    f = os.path.join(cache, h + ".png")
    if not os.path.exists(f):
        u = f"https://{DOMAIN}/cdn/shop/files/" + PACK[h].split("/files/")[-1]
        open(f, "wb").write(urllib.request.urlopen(u, context=CTX).read())
    im = Image.open(f).convert("RGB"); im.thumbnail((300, 300)); return im
keys = sys.argv[1].split(","); H = 760
tiles = []
for k in keys:
    r = res[k]; pv = Image.open(r["preview"]).convert("RGB"); pv = pv.resize((round(pv.width * H / pv.height), H))
    pk = pack(P[k]["handle"])
    t = Image.new("RGB", (pv.width + 310, H + 30), "white"); t.paste(pv, (0, 30)); t.paste(pk, (pv.width + 5, 30))
    ImageDraw.Draw(t).text((5, 5), f"{k} (try {r['attempt']})", fill="red"); tiles.append(t)
W = sum(t.width for t in tiles); g = Image.new("RGB", (W, H + 30), "white"); x = 0
for t in tiles: g.paste(t, (x, 0)); x += t.width
g.save(sys.argv[2], quality=85); print(sys.argv[2], g.size)
