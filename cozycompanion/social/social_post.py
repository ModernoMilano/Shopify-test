"""Daily organic post for Instagram (@cozycompanion.usa) and the CozyCompanion Facebook Page.
Every post gets NEW imagery made with Nano Banana (our packshot as the product reference), checked against
social/QA.md before anything is published.

  python3 -I social/social_post.py prepare [--theme NAME] [--date YYYY-MM-DD]
      Picks today's theme (weekday rhythm) and a product (or, on carousel days, a collection) not posted in the
      last 30 days. Prints a JSON brief: theme, product facts, link, packshot reference URL(s) and a scene idea.
  python3 -I social/social_post.py finish <image_result_url> <name>
      Brings a finished Nano Banana image into Shopify Files, crops it to Instagram's 4:5 (1080x1350 JPEG),
      uploads that and prints {"public_url", "preview"}; open the preview for the QA check.
  python3 -I social/social_post.py story <image_result_url> <name> "<text>"
      9:16 story: brand overlay (line + LINK IN BIO + wordmark), 1080x1920 JPEG in Shopify Files; prints URL + preview.
  python3 -I social/social_post.py video <video_result_url> <name>
      Reel MP4 into Shopify Files; prints the public URL, a frame sheet for QA and the audio levels.
  python3 -I social/social_post.py day [YYYY-MM-DD] [--slot am|mid|pm]
      The owner-approved calendar entry for that day (default: today, US Eastern), ready to publish: Instagram
      caption, Facebook caption (with product links), feed/story/reel URLs, and whether it was already posted.
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

FONT = os.path.join(S, "ads", "fonts")
CREAM, ROSE, CHAR = (245, 241, 237), (183, 110, 121), (26, 26, 26)

def _raw(result_url, name):
    p = subprocess.run([sys.executable, "-I", os.path.join(S, "upload.py")], input=f"{name}_raw {result_url}|CozyCompanion social {name}\n",
                       text=True, capture_output=True)
    if f"{name}_raw" not in reg(): sys.exit("upload failed: " + p.stdout[-300:] + p.stderr[-300:])
    u = f"https://{DOMAIN}/cdn/shop/files/" + reg()[f"{name}_raw"]["url"].split("/files/")[-1].split("?")[0]
    return Image.open(io.BytesIO(urllib.request.urlopen(u, context=CTX).read())).convert("RGB")

def story(result_url, name, text):
    """9:16 Nano Banana image -> 1080x1920 story with a soft bottom gradient, the brand line in Cormorant,
    'link in bio' in Jost and the small wordmark on top. Returns public URL + local preview."""
    from PIL import ImageDraw, ImageFont
    im = _raw(result_url, name)
    w, h = im.size; th = round(w * 16 / 9)
    if th > h: tw = round(h * 9 / 16); im = im.crop(((w - tw) // 2, 0, (w - tw) // 2 + tw, h))
    else: im = im.crop((0, (h - th) // 2, w, (h - th) // 2 + th))
    im = im.resize((1080, 1920), Image.LANCZOS).convert("RGBA")
    grad = Image.new("L", (1, 1920))
    for y in range(1920): grad.putpixel((0, y), int(170 * max(0, (y - 1180) / 740) ** 1.4))
    shade = Image.new("RGBA", (1080, 1920), CHAR + (0,)); shade.putalpha(grad.resize((1080, 1920)))
    im = Image.alpha_composite(im, shade)
    d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype(os.path.join(FONT, "Cormorant-500.ttf"), 92)
    f2 = ImageFont.truetype(os.path.join(FONT, "Jost-500.ttf"), 30)
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=f1) > 900 and cur: lines.append(cur); cur = wd
        else: cur = t
    lines.append(cur)
    y = 1700 - len(lines) * 100
    for ln in lines:
        d.text(((1080 - d.textlength(ln, font=f1)) / 2, y), ln, font=f1, fill=CREAM + (255,)); y += 100
    tag = "LINK IN BIO"
    sp = 6; tw = sum(d.textlength(c, font=f2) for c in tag) + sp * (len(tag) - 1); x = (1080 - tw) / 2
    for c in tag: d.text((x, y + 24), c, font=f2, fill=CREAM + (230,)); x += d.textlength(c, font=f2) + sp
    logo = Image.open(os.path.join(S, "logo", "logo-light.png")).convert("RGBA"); logo = logo.crop(logo.getbbox())
    logo = Image.merge("RGBA", (*[Image.new("L", logo.size, v) for v in CREAM], logo.getchannel("A")))   # solid cream: rose letters vanish on mid tones
    lw = 300; logo = logo.resize((lw, round(lw * logo.height / logo.width)), Image.LANCZOS)
    top = Image.new("L", (1, 340)); [top.putpixel((0, yy), int(175 * (1 - yy / 340) ** 1.2)) for yy in range(340)]
    tshade = Image.new("RGBA", (1080, 340), CHAR + (0,)); tshade.putalpha(top.resize((1080, 340)))
    im.alpha_composite(tshade, (0, 0)); im.alpha_composite(logo, ((1080 - lw) // 2, 110))
    path = os.path.join(TMP, f"{name}.jpg"); im.convert("RGB").save(path, "JPEG", quality=90)
    subprocess.run([sys.executable, "-I", os.path.join(S, "staged_one.py"), path, name, f"CozyCompanion story {name}"],
                   check=True, capture_output=True)
    return {"public_url": reg()[name]["url"].split("?")[0], "preview": path}

def video(result_url, name):
    """Finished Seedance video -> Shopify Files (public MP4 URL) + local copy and QA frames (8 stills, audio levels)."""
    from lib import check
    # Shopify only takes external URLs for images and generic files (a VIDEO must be staged), and this sandbox can't
    # fetch the generator's CDN itself, so the MP4 is stored as a generic file: a public cdn.shopify.com .mp4 URL.
    f = check(gql("mutation($f:[FileCreateInput!]!){fileCreate(files:$f){files{id} userErrors{field message}}}",
                  {"f": [{"originalSource": result_url, "contentType": "FILE", "alt": f"CozyCompanion reel {name}", "filename": f"cozycompanion-{name}.mp4"}]})["fileCreate"])["files"][0]["id"]
    import time
    for _ in range(60):
        n = gql("query($id:ID!){node(id:$id){... on GenericFile{fileStatus url mimeType}}}", {"id": f})["node"]
        if n["fileStatus"] in ("READY", "FAILED"): break
        time.sleep(5)
    if n["fileStatus"] != "READY": sys.exit(f"video upload {n['fileStatus']}")
    url = n["url"]
    data = urllib.request.urlopen(f"https://{DOMAIN}/cdn/shop/files/" + url.split("/files/")[-1].split("?")[0], context=CTX).read()
    mp4 = os.path.join(TMP, f"{name}.mp4"); open(mp4, "wb").write(data)
    sheet = os.path.join(TMP, f"{name}_frames.jpg")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-vf", "fps=8/6,scale=270:-1,tile=4x2", "-frames:v", "1", sheet], check=False)
    vol = subprocess.run(["ffmpeg", "-i", mp4, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    levels = {k: v for k, v in (l.split("] ")[-1].split(": ") for l in vol.splitlines() if "_volume" in l)}
    reg_ = reg(); reg_[name] = {"id": f, "url": url, "alt": f"CozyCompanion reel {name}"}
    json.dump(reg_, open(os.path.join(S, "files.json"), "w"), indent=1)
    return {"public_url": url, "local": mp4, "frames": sheet, "audio": levels}

def _titles(handles):
    t = {}
    for h in handles:
        r = gql("query($h:String!){productByHandle(handle:$h){title status}}", {"h": h})["productByHandle"]
        t[h] = r and r["status"] == "ACTIVE" and r["title"]
    return t

def _pub(u):
    """Media URL for Instagram/Facebook: the store's own domain. Since 2026-11-05 Instagram rejects fetches from
    cdn.shopify.com ("Only photo or video can be accepted"), while https://cozycompanion.us/cdn/shop/files/... works."""
    if not u: return u
    import re
    m = re.match(r"https://cdn\.shopify\.com/s/files/1/\d+/\d+/\d+/files/([^?]+)", u)
    return f"https://cozycompanion.us/cdn/shop/files/{m.group(1)}" if m else u

def _pubify(d):
    for k in ("story", "reel", "facebook_image"):
        if d.get(k): d[k] = _pub(d[k])
    if d.get("feed"): d["feed"] = [_pub(u) for u in d["feed"]]
    return d

def _approved(flag):
    """Owner approvals are recorded as files: bfcm/APPROVED (BFCM plan), q4/APPROVED (December calendar)."""
    return os.path.exists(os.path.join(S, flag))

def day(date=None, slot="am"):
    """Owner-approved post(s) for one day and slot ('am' 11:43 ET, 'mid' 14:43 ET, 'pm' 19:13 ET), as ready-to-send
    payloads. Sources: social/calendar.json (Nov), bfcm/social_plan.json + bfcm/assets.json stories (Nov 20-30, only
    once bfcm/APPROVED exists), social/calendar_dec.json (Dec, only once q4/APPROVED exists)."""
    if not date:
        date = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=5)).date().isoformat()
    done = [e for e in log() if e.get("date") == date and e.get("slot", "am") == slot]
    base = {"date": date, "slot": slot, "already_posted": bool(done)}
    if "2026-11-20" <= date <= "2026-11-30" and _approved("bfcm/APPROVED"):
        plan = [p for p in json.load(open(os.path.join(S, "bfcm", "social_plan.json"))) if p["date"] == date and p["slot"] == slot]
        stories = [x["url"] for x in json.load(open(os.path.join(S, "bfcm", "assets.json"))).get("stories", [])
                   if x["date"] == date and x["slot"] == slot]
        if not plan and not stories: return {**base, "error": "nothing planned for this slot"}
        out = {**base, "source": "bfcm", "story": stories[0] if stories else None, "feed": [], "reel": None}
        if plan:
            p = plan[0]; h = p["facebook_link"].split("/products/")[-1] if "/products/" in p["facebook_link"] else None
            t = _titles([h]) if h else {}
            body = p["caption"].replace("Shop via the link in bio", "Shop now").replace(" via the link in bio", "").rstrip()
            out.update({"type": p["type"], "inactive_products": [k for k, v in t.items() if not v],
                        "instagram_caption": p["caption"].rstrip() + "\n\n" + p["tags"],
                        "facebook_caption": body + "\n\n" + p["facebook_link"] + "\n\n" + " ".join(p["tags"].split()[:5]),
                        "facebook_image": next((u for u in p["assets"] if not u.split("?")[0].endswith(".mp4")), None)})
            if not out["facebook_image"]:   # reel days: Facebook gets that day's approved November photo (or the story)
                novc = {d["date"]: d for d in json.load(open(os.path.join(S, "social", "calendar.json")))}
                out["facebook_image"] = ((novc.get(date, {}).get("assets") or {}).get("feed") or [out["story"]])[0]
            if p["type"] == "reel": out["reel"] = p["assets"][0]
            else: out["feed"] = p["assets"]
        return out
    if slot != "am": return {**base, "error": "nothing planned for this slot"}
    src = "social/calendar.json" if date < "2026-12-01" else "social/calendar_dec.json"
    if src.endswith("_dec.json") and not _approved("q4/APPROVED"):
        return {**base, "error": "December calendar not approved by the owner yet"}
    path = os.path.join(S, src)
    cal = {d["date"]: d for d in json.load(open(path))} if os.path.exists(path) else {}
    if date not in cal: return {**base, "error": "no calendar entry for this date"}
    d = cal[date]; a = d.get("assets") or {}
    if d.get("needs_owner_approval"): return {**base, "error": "entry needs owner approval: " + d["needs_owner_approval"]}
    titles = _titles(d["products"])
    links = [f"{(titles[h] or h).split(' ')[0]}: https://cozycompanion.us/products/{h}" for h in d["products"] if titles[h]]
    fb_tags = " ".join(d["tags"].split()[:5])
    fb_body = d["caption"].replace("Shop via the link in bio", "Shop now").replace(" via the link in bio", "").rstrip()
    return {**base, "source": src, "theme": d["theme"], "products": d["products"], "inactive_products": [h for h in d["products"] if not titles[h]],
            "instagram_caption": d["caption"].rstrip() + "\n\n" + d["tags"],
            "facebook_caption": fb_body + "\n\n" + "\n".join(links) + "\n\n" + fb_tags,
            "feed": a.get("feed") or [], "story": a.get("story"), "reel": a.get("reel"), "reel_planned": bool(d.get("reel")),
            "facebook_image": (a.get("feed") or [None])[0]}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "prepare"
    if cmd == "prepare":
        a = sys.argv[2:]
        print(json.dumps(prepare(a[a.index("--theme") + 1] if "--theme" in a else None,
                                 a[a.index("--date") + 1] if "--date" in a else None), indent=1))
    elif cmd == "finish":
        print(json.dumps(finish(sys.argv[2], sys.argv[3])))
    elif cmd == "story":
        print(json.dumps(story(sys.argv[2], sys.argv[3], sys.argv[4])))
    elif cmd == "video":
        print(json.dumps(video(sys.argv[2], sys.argv[3])))
    elif cmd == "day":
        a = sys.argv[2:]; sl = a[a.index("--slot") + 1] if "--slot" in a else "am"
        dd = next((x for x in a if x[:4].isdigit()), None)
        print(json.dumps(_pubify(day(dd, sl)), indent=1, ensure_ascii=False))
    elif cmd == "log":
        entries = log(); entries.append(json.loads(sys.argv[2])); json.dump(entries, open(LOG, "w"), indent=1)
        print("logged", len(entries))
