"""Daily organic post for Instagram (@cozycompanion.usa) and the CozyCompanion Facebook Page.
Every post gets NEW imagery made with Nano Banana (our packshot as the product reference), checked against
social/QA.md before anything is published.

  python3 -I social/social_post.py prepare [--theme NAME] [--date YYYY-MM-DD]
      Picks today's theme (weekday rhythm) and a product (or, on carousel days, a collection) not posted in the
      last 30 days. Prints a JSON brief: theme, product facts, link, packshot reference URL(s) and a scene idea.
  python3 -I social/social_post.py finish <image_result_url> <name>
      Brings a finished Nano Banana image into Shopify Files, crops it to Instagram's 4:5 (1080x1350 JPEG),
      uploads that and prints {"public_url", "preview"}; open the preview for the QA check.
  python3 -I social/social_post.py log '<json>'
      Appends what was published (date, theme, handle, image names, post ids) to social/log.json.

Rules: no prices (they change), no reviews, ratings or invented customer stories, only real products."""
import sys, os, io, json, random, datetime, ssl, subprocess, urllib.request
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, S)
from lib import gql, DOMAIN
from PIL import Image

LOG = os.path.join(S, "social", "log.json")
TMP = os.path.join(S, "social", ".tmp"); os.makedirs(TMP, exist_ok=True)
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
THEMES = {0: "product_spotlight", 1: "care_tip", 2: "life_with", 3: "collection_carousel",
          4: "playful", 5: "gift_idea", 6: "brand_story"}
SCENES = {
  "product_spotlight": "editorial still life of the product on a warm cream set with soft daylight, the pet resting beside it, magazine quality",
  "care_tip": "the pet in a calm real-home moment that illustrates a care tip around the product (comfort, hydration, grooming, enrichment, walks)",
  "life_with": "candid phone-style lifestyle photo of a happy owner and pet at home with the product, natural light, genuine joy",
  "collection_carousel": "one clean editorial image per product: product with the pet, same cream/oak/linen palette so the carousel feels like one set",
  "playful": "funny, relatable pet moment with the product (a mischievous look, stealing the spot, zoomies); optional short handwritten note in the scene with correctly spelled English",
  "gift_idea": "cozy seasonal gifting scene: the product wrapped or beside a ribbon and a winter-holiday setting, pet curious about it",
  "brand_story": "quiet, premium brand photo: product in a beautiful interior, pet asleep or relaxed, lots of calm space",
}
COLLECTIONS = ["beds-dens", "smart-feeding", "play-enrichment", "wear-walk", "groom-clean", "pet-travel", "cats", "dogs"]

def reg(): return json.load(open(os.path.join(S, "files.json")))
def log(): return json.load(open(LOG)) if os.path.exists(LOG) else []

def gallery():
    import ast
    src = open(os.path.join(S, "gallery.py")).read()
    return ast.literal_eval(src[src.index("GALLERIES = {") + len("GALLERIES = "): src.index("\n}\n", src.index("GALLERIES = {")) + 2])

def products():
    out, after = [], None
    while True:
        r = gql("""query($a:String){products(first:100,after:$a,query:"status:active tag:cc-ready"){nodes{handle title productType tags
                   h1: metafield(namespace:"custom",key:"highlight_1"){value} h2: metafield(namespace:"custom",key:"highlight_2"){value}
                   h3: metafield(namespace:"custom",key:"highlight_3"){value} collections(first:10){nodes{handle}}}
                   pageInfo{hasNextPage endCursor}}}""", {"a": after})["products"]
        out += r["nodes"]
        if not r["pageInfo"]["hasNextPage"]: return out
        after = r["pageInfo"]["endCursor"]

def facts(p, G, rg):
    return {"handle": p["handle"], "title": p["title"], "type": p["productType"],
            "pet": [t for t in ("dog", "cat") if t in p["tags"]],
            "highlights": [(p[h] or {}).get("value") for h in ("h1", "h2", "h3") if p[h]],
            "link": f"https://cozycompanion.us/products/{p['handle']}",
            "reference_url": rg[G[p["handle"]][0]]["url"].split("?")[0]}

def prepare(theme=None, date=None):
    day = datetime.date.fromisoformat(date) if date else datetime.date.today()
    theme = theme or THEMES[day.weekday()]
    rg, G = reg(), gallery()
    cut = (day - datetime.timedelta(days=30)).isoformat()
    used = {h for e in log() if e.get("date", "") >= cut for h in ([e.get("handle")] + e.get("products", []))}
    P = [p for p in products() if p["handle"] in G and "for-you" not in p["tags"]]
    fresh = [p for p in P if p["handle"] not in used] or P
    random.seed(day.isoformat())
    brief = {"date": day.isoformat(), "theme": theme, "scene_idea": SCENES[theme], "name_prefix": f"s_{day.isoformat()}"}
    if theme == "collection_carousel":
        recent_cols = {e.get("handle") for e in log()[-21:]}
        col = random.choice([c for c in COLLECTIONS if c not in recent_cols] or COLLECTIONS)
        c = gql('query($h:String!){collectionByHandle(handle:$h){title description}}', {"h": col})["collectionByHandle"]
        members = [p for p in fresh if any(x["handle"] == col for x in p["collections"]["nodes"])] or \
                  [p for p in P if any(x["handle"] == col for x in p["collections"]["nodes"])]
        picks = random.sample(members, min(3, len(members)))
        brief.update(handle=col, title=c["title"], about=c["description"], link=f"https://cozycompanion.us/collections/{col}",
                     products=[facts(p, G, rg) for p in picks])
        return brief
    if theme == "gift_idea":
        fresh = [p for p in fresh if any(c["handle"] == "holiday-gift-guide" for c in p["collections"]["nodes"])] or fresh
    brief.update(product=facts(random.choice(fresh), G, rg))
    return brief

def finish(result_url, name):
    """Image result -> Shopify Files (raw) -> 4:5 1080x1350 JPEG -> Shopify Files; returns public URL + local preview."""
    p = subprocess.run([sys.executable, "-I", os.path.join(S, "upload.py")], input=f"{name}_raw {result_url}|CozyCompanion social {name}\n",
                       text=True, capture_output=True)
    if f"{name}_raw" not in reg(): sys.exit("upload failed: " + p.stdout[-300:] + p.stderr[-300:])
    u = f"https://{DOMAIN}/cdn/shop/files/" + reg()[f"{name}_raw"]["url"].split("/files/")[-1].split("?")[0]
    im = Image.open(io.BytesIO(urllib.request.urlopen(u, context=CTX).read())).convert("RGB")
    w, h = im.size; tw = min(w, round(h * 4 / 5)); th = round(tw * 5 / 4)
    im = im.crop(((w - tw) // 2, (h - th) // 2, (w - tw) // 2 + tw, (h - th) // 2 + th)).resize((1080, 1350), Image.LANCZOS)
    path = os.path.join(TMP, f"{name}.jpg"); im.save(path, "JPEG", quality=90)
    subprocess.run([sys.executable, "-I", os.path.join(S, "staged_one.py"), path, name, f"CozyCompanion social {name}"],
                   check=True, capture_output=True)
    return {"public_url": reg()[name]["url"].split("?")[0], "preview": path}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "prepare"
    if cmd == "prepare":
        a = sys.argv[2:]
        print(json.dumps(prepare(a[a.index("--theme") + 1] if "--theme" in a else None,
                                 a[a.index("--date") + 1] if "--date" in a else None), indent=1))
    elif cmd == "finish":
        print(json.dumps(finish(sys.argv[2], sys.argv[3])))
    elif cmd == "log":
        entries = log(); entries.append(json.loads(sys.argv[2])); json.dump(entries, open(LOG, "w"), indent=1)
        print("logged", len(entries))
