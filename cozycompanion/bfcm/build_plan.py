"""Builds bfcm/assets.json and bfcm/social_plan.json from files.json (uploaded creatives) and social/calendar.json (existing reels).

Captions follow social/QA.md and bfcm/BRIEF.md:
- English, hook, 1–3 short lines, CTA, 8–12 hashtags;
- no product prices (they change), only the tier thresholds;
- no fake scarcity, no reviews.
"""
import os, json
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = json.load(open(os.path.join(S, "files.json")))
CAL = {d["date"]: d for d in json.load(open(os.path.join(S, "social", "calendar.json")))}
EDIT = "https://cozycompanion.us/collections/black-friday-edit"
P = lambda h: f"https://cozycompanion.us/products/{h}"

def url(name):
    u = REG.get(name, {}).get("url")
    return u.split("?")[0] if u and u.startswith("https") else None

TIERS = "Save 10% on orders $75+, 15% on $150+ and 20% on $250+. Applied automatically at checkout, no code needed."
TAGS_DOG = "#dogsofinstagram #doglife #dogmom #doglover #blackfriday #blackfridayweek #giftsfordogs #petgifts #cozyhome #luxurypets"
TAGS_CAT = "#catsofinstagram #catlife #catmom #catlover #blackfriday #blackfridayweek #giftsforcats #petgifts #cozyhome #luxurypets"
TAGS_PET = "#dogsofinstagram #catsofinstagram #petlover #blackfriday #blackfridayweek #cybermonday #petgifts #holidaygifts #cozyhome #luxurypets"

CLEAN = {"A1_45": "bfcm_A1_45", "A1_916": "bfcm_A1_916", "A2_45": "bfcm_A2_45", "A2_916": "bfcm_A2_916", "A3_45": "bfcm_A3_45",
         "A3_916": "bfcm_A3_916", "A4_45": "bfcm_A4_45_v2", "A4_916": "bfcm_A4_916_v2", "P1": "bfcm_P1", "P3a": "bfcm_P3a_v2",
         "P3b": "bfcm_P3b", "P3c": "bfcm_P3c_v2", "P4a": "bfcm_P4a_v2", "P4b": "bfcm_P4b", "P4c": "bfcm_P4c", "P5": "bfcm_P5",
         "P6a": "bfcm_P6a", "P6b": "bfcm_P6b", "P6c": "bfcm_P6c", "P7": "bfcm_P7", "P8": "bfcm_P8", "P9": "bfcm_P9", "P10": "bfcm_P10",
         "SB1": "bfcm_SB1", "SB2": "bfcm_SB2", "SB3": "bfcm_SB3", "SB4": "bfcm_SB4", "SB5": "bfcm_SB5", "SB6": "bfcm_SB6",
         "W1": "bfcm_W1", "W2": "bfcm_W2", "W3": "bfcm_W3"}
FINAL = {"A1_45": "bfcm_out_ad_A1_45", "A1_916": "bfcm_out_ad_A1_916", "A2_45": "bfcm_out_ad_A2_45", "A2_916": "bfcm_out_ad_A2_916",
         "A3_45": "bfcm_out_ad_A3_45", "A3_916": "bfcm_out_ad_A3_916", "A4_45": "bfcm_out_ad_A4_45", "A4_916": "bfcm_out_ad_A4_916",
         "P1": "bfcm_out_feed_P1", "P2a": "bfcm_out_feed_P2a", "P5": "bfcm_out_feed_P5", "P8": "bfcm_out_feed_P8",
         "P9": "bfcm_out_feed_P9", "P10": "bfcm_out_feed_P10"}
PRODUCT = {"W1": "chaise-velvet-storage-pet-sofa", "W2": "chaise-velvet-storage-pet-sofa", "W3": "chester-tufted-dog-sofa",
           "A1": "nestle-heated-pet-pad", "A2": "dine-automatic-feeder", "A3": "chester-tufted-dog-sofa", "A4": "perch-modern-cat-tree",
           "P3a": "chester-tufted-dog-sofa", "P3b": "dream-memory-foam-dog-bed", "P3c": "frost-harness-winter-dog-jacket",
           "P4a": "perch-modern-cat-tree", "P4b": "haven-pet-den", "P4c": "pounce-automatic-feather-cat-toy", "P5": "chaise-velvet-storage-pet-sofa",
           "P6a": "snug-sherpa-pet-blanket", "P6b": "nestle-heated-pet-pad", "P6c": "peak-triangle-cat-scratcher", "P7": "haven-pet-den",
           "P8": "dream-memory-foam-dog-bed", "P9": "burrow-plush-pet-bed"}
ATTEMPTS = {"A4_45": 2, "A4_916": 2, "P3a": 2, "P3c": 2, "P4a": 2}
ASPECT = lambda k: "16:9" if k == "W1" else "21:9" if k == "W3" else "9:16" if k.endswith("916") or k.startswith("SB") else "4:5"

def F(k): return url(FINAL[k]) if k in FINAL else None
def C(k): return url(CLEAN[k])
def img(k): return F(k) or C(k)
def reel(date): return CAL[date]["assets"]["reel"].split("?")[0]

PLAN = [
 {"date": "2026-11-20", "slot": "am", "type": "reel", "assets": [reel("2026-11-20")], "facebook_link": P("splash-quick-dry-dog-bathrobe"),
  "caption": "Fresh from the bath and fully in their feelings. \U0001f6c1\n\nSomething cozy is coming: Black Friday Week starts Monday, November 23.\n\nTurn on notifications so you don't miss it \U0001f514",
  "tags": TAGS_DOG},
 {"date": "2026-11-21", "slot": "am", "type": "image", "assets": [img("P1")], "facebook_link": EDIT,
  "caption": "Unwrapping soon. \U0001f381\n\nBlack Friday Week starts Monday, November 23. " + TIERS + "\n\nStart your wishlist via the link in bio \U0001f43e",
  "tags": TAGS_PET},
 {"date": "2026-11-22", "slot": "am", "type": "reel", "assets": [reel("2026-11-22")], "facebook_link": P("ascend-acacia-pet-stairs-ramp"),
  "caption": "Every step, their way. \U0001f43e\n\nAscend helps senior and small pets reach their favorite spot. Black Friday Week starts tomorrow.\n\n" + TIERS,
  "tags": TAGS_DOG},
 {"date": "2026-11-23", "slot": "am", "type": "carousel", "assets": [img("P2a"), C("A3_45"), C("A4_45")], "facebook_link": EDIT,
  "caption": "Black Friday, the cozy way. ✨\n\nBlack Friday Week is here, November 23 – 30.\n" + TIERS + "\n\nShop the edit via the link in bio \U0001f43e",
  "tags": TAGS_PET},
 {"date": "2026-11-23", "slot": "pm", "type": "reel", "assets": [url("bfcm_R1")], "facebook_link": P("nestle-heated-pet-pad"),
  "caption": "They stole your spot. Make it official. \U0001f6cb️\n\nNestle is a heated pad that turns any seat into their favorite one.\n\n" + TIERS + "\n\nShop via the link in bio \U0001f43e",
  "tags": TAGS_DOG},
 {"date": "2026-11-24", "slot": "am", "type": "reel", "assets": [reel("2026-11-24")], "facebook_link": P("savor-bone-lick-mat"),
  "caption": "Slow down, savor it. \U0001f9b4\n\nA lick mat turns treat time into calm time. It's Black Friday Week at CozyCompanion.\n\n" + TIERS,
  "tags": TAGS_DOG},
 {"date": "2026-11-25", "slot": "am", "type": "carousel", "assets": [C("P3a"), C("P3b"), C("P3c")], "facebook_link": EDIT,
  "caption": "Gift guide: for the dog who has everything. \U0001f381\n\n1. Chester: a tufted sofa made for their naps\n2. Dream: memory foam with a bolster for their head\n3. Frost: a padded winter jacket with a built-in harness\n\n" + TIERS + "\n\nShop via the link in bio \U0001f43e",
  "tags": TAGS_DOG},
 {"date": "2026-11-25", "slot": "pm", "type": "carousel", "assets": [C("P4a"), C("P4b"), C("P4c")], "facebook_link": EDIT,
  "caption": "Gift guide: for the cat who rules the house. \U0001f451\n\n1. Perch: a modern cat tree with a den, hammock and ramps\n2. Haven: a felt den for serious naps\n3. Pounce: an automatic feather toy for indoor hunters\n\n" + TIERS + "\n\nShop via the link in bio \U0001f43e",
  "tags": TAGS_CAT},
 {"date": "2026-11-26", "slot": "am", "type": "reel", "assets": [reel("2026-11-26")], "facebook_link": P("burrow-plush-pet-bed"),
  "caption": "Thankful for naps like these. \U0001f9e1\n\nHappy Thanksgiving from our pack to yours. Black Friday Week runs through Monday.\n\n" + TIERS,
  "tags": TAGS_PET},
 {"date": "2026-11-27", "slot": "am", "type": "image", "assets": [img("P5")], "facebook_link": EDIT,
  "caption": "Black Friday is here. ✨\n\n" + TIERS + "\n\nShop the Black Friday Edit via the link in bio \U0001f43e",
  "tags": TAGS_PET},
 {"date": "2026-11-27", "slot": "pm", "type": "reel", "assets": [url("bfcm_R2")], "facebook_link": P("chester-tufted-dog-sofa"),
  "caption": "Their own sofa. Finally. \U0001f6cb️\n\nChester is a tufted dog sofa that looks as good as yours.\n\n" + TIERS + "\n\nShop via the link in bio \U0001f43e",
  "tags": TAGS_DOG},
 {"date": "2026-11-28", "slot": "am", "type": "carousel", "assets": [C("P6a"), C("P6b"), C("P6c")], "facebook_link": EDIT,
  "caption": "Little luxuries they'll love. \U0001f381\n\n1. Snug: a soft sherpa blanket\n2. Nestle: a heated pad for chilly nights\n3. Peak: a triangle scratcher that saves your sofa\n\n" + TIERS + "\n\nShop via the link in bio \U0001f43e",
  "tags": TAGS_PET},
 {"date": "2026-11-28", "slot": "pm", "type": "image", "assets": [C("P7")], "facebook_link": P("haven-pet-den"),
  "caption": "Weekend plans: none. \U0001f634\n\nHaven is a felt den made for long naps. Black Friday Week ends Monday at 11:59 pm ET.\n\n" + TIERS,
  "tags": TAGS_CAT},
 {"date": "2026-11-29", "slot": "am", "type": "reel", "assets": [reel("2026-11-29")], "facebook_link": P("peak-triangle-cat-scratcher"),
  "caption": "Sunday stretch. \U0001f408\n\nPeak gives them the perfect scratching angle (and saves your sofa).\n\n" + TIERS,
  "tags": TAGS_CAT},
 {"date": "2026-11-29", "slot": "pm", "type": "image", "assets": [img("P8")], "facebook_link": EDIT,
  "caption": "Black Friday Week ends Monday at 11:59 pm ET. \U0001f319\n\n" + TIERS + "\n\nShop via the link in bio \U0001f43e",
  "tags": TAGS_PET},
 {"date": "2026-11-30", "slot": "am", "type": "image", "assets": [img("P9")], "facebook_link": EDIT,
  "caption": "Cyber Monday. Last chance. \U0001f4bb\n\nBlack Friday Week ends tonight at 11:59 pm ET.\n" + TIERS + "\n\nShop via the link in bio \U0001f43e",
  "tags": TAGS_PET},
 {"date": "2026-11-30", "slot": "pm", "type": "image", "assets": [img("P10")], "facebook_link": EDIT,
  "caption": "Ends tonight. ✨\n\nBlack Friday Week closes at 11:59 pm ET. " + TIERS + "\n\nThank you for an amazing week \U0001f43e",
  "tags": TAGS_PET},
]

STORY_TEXT = {}
def stories():
    from importlib.machinery import SourceFileLoader
    mo = SourceFileLoader("mo", os.path.join(S, "bfcm", "make_overlays.py")).load_module()
    out = []
    for date, slot, _fn in mo.STORIES:
        n = f"bfcm_out_story_{date[5:]}_{slot}"
        if url(n + "_v2"): n += "_v2"
        out.append({"date": date, "slot": slot, "url": url(n), "name": n})
    return out

if __name__ == "__main__":
    assets = {}
    for k in sorted(set(CLEAN) | set(FINAL)):
        base = k.split("_")[0] if k[0] == "A" else k
        assets[k] = {"clean": C(k) if k in CLEAN else None, "final": F(k), "aspect": ASPECT(k),
                     "product": PRODUCT.get(base) or PRODUCT.get(k), "qa": "pass", "attempts": ATTEMPTS.get(k, 1)}
    assets["P2b"] = {"clean": C("A3_45"), "final": None, "aspect": "4:5", "product": PRODUCT["A3"], "qa": "pass", "attempts": 1, "note": "same photo as A3_45"}
    assets["P2c"] = {"clean": C("A4_45"), "final": None, "aspect": "4:5", "product": PRODUCT["A4"], "qa": "pass", "attempts": 2, "note": "same photo as A4_45"}
    st = stories()
    res = {"assets": assets, "stories": st, "reels": {"R1": url("bfcm_R1"), "R2": url("bfcm_R2")}}
    missing = [k for k, v in assets.items() if not (v["clean"] or v["final"])] + [s["name"] for s in st if not s["url"]]
    missing += [k for k, v in res["reels"].items() if not v]
    missing += [f"plan {p['date']} {p['slot']}" for p in PLAN if not all(p["assets"])]
    json.dump(res, open(os.path.join(S, "bfcm", "assets.json"), "w"), indent=1)
    for p in PLAN:
        if "link in bio" not in p["caption"] and p["date"] != "2026-11-20":
            p["caption"] += "\n\nShop via the link in bio \U0001f43e"
    json.dump(PLAN, open(os.path.join(S, "bfcm", "social_plan.json"), "w"), indent=1, ensure_ascii=False)
    print("missing:", missing)
