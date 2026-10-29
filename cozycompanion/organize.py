"""Tidy the catalogue so collection pages read like a curated store, not an import feed.

- productType: one clean subtype per product (used by the 'Product type' filter), grouped under the six menu categories.
- Every collection: manual sort, grouped category -> subtype, premium first within a subtype. New products without a
  mapping fall back on their tags and land at the end of their category; re-run this after each import.
- Titles: drop specs (sizes, litres, compatibility) that belong in the description. SEO title follows.
- Tags: drop SEO keyword spam; keep the tags collections and scripts rely on.
- Shop All (smart-pet-tech, a manual collection): make sure every active product is in it.
Usage: python3 -I organize.py [--dry]"""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check

DRY = "--dry" in sys.argv
CATS = {  # category -> ordered subtypes -> first word of the product title
    "Sleep & Lounge": {"Beds": "Dream Haven Cocoon Billow Lounge Burrow Orbit",
                       "Blankets & Mats": "Ember Nestle Nook Cloud Snug",
                       "Cat Trees & Scratchers": "Perch Peak Fold",
                       "Pet Stairs": "Ascend"},
    "Dine & Drink": {"Smart Feeders": "Glance Murmur Dine",
                     "Water Fountains": "Brook",
                     "Bowls": "Purr Pace Tidy Cove",
                     "Puzzle Feeders & Lick Mats": "Forage Maze Quest Savor",
                     "Feeding Accessories": "Measure Slate"},
    "Play": {"Smart Toys": "Flutter Pounce Wiggle Spark Fetch Zoom",
             "Cat Toys": "Flit Plume Chase Chirp",
             "Dog Toys": "Buddy Glide Knot Gnaw Riddle Chomp"},
    "Wear & Walk": {"Coats & Apparel": "Frost Mistle Fin Drizzle Puddle Splash Knit Doze",
                    "Harnesses & Leashes": "Trail Stride Wander",
                    "Collars & Accessories": "Compass Dapper Beacon Bloom"},
    "Groom & Clean": {"Grooming": "Sweep Breeze Trim Polish Tame Lift",
                      "Litter & Hygiene": "Halo Fresh Sift"},
    "Travel": {"Carriers": "Voyage Jetset Cradle",
               "Car Travel": "Roam Ride"},
}
FALLBACK = [("beds-dens", "Sleep & Lounge"), ("feeding", "Dine & Drink"), ("hydration", "Dine & Drink"), ("play", "Play"),
            ("wear", "Wear & Walk"), ("walk", "Wear & Walk"), ("grooming", "Groom & Clean"),
            ("litter-hygiene", "Groom & Clean"), ("travel", "Travel")]
TITLES = {"Ember Heat Pad 24 × 12 in": "Ember Heat Pad",
          "Compass Smart Tag for Find My & Find Hub": "Compass Smart Pet Tag",
          "Brook Stainless Pet Fountain 2L / 4L": "Brook Stainless Pet Fountain",
          "Brook XL Cordless Fountain 7L": "Brook XL Cordless Fountain",
          "Dine 4L Automatic Feeder": "Dine Automatic Feeder",
          "Glance 4L Camera Feeder": "Glance Camera Feeder",
          "Murmur 3L Camera Feeder": "Murmur Camera Feeder",
          "Voyage Rolling Pet Carrier XL": "Voyage Rolling Pet Carrier",
          "Flutter 2-in-1 Cat Play Station": "Flutter Cat Play Station",
          "Ascend Acacia Pet Stairs & Ramp": "Ascend Pet Stairs & Ramp",
          "Frost Harness Winter Dog Jacket": "Frost Winter Dog Jacket",
          "Pounce Automatic Feather Cat Toy": "Pounce Feather Cat Toy",
          "Splash Quick-Dry Dog Bathrobe": "Splash Dog Bathrobe",
          "Roam Back Seat Dog Bed & Cover": "Roam Back Seat Dog Bed"}
KEEP_TAGS = set("dog cat play feeding hydration beds-dens wear walk travel smart grooming litter-hygiene upsell price-3x "
                "cc-ready fountain feeder camera-feeder smart-tag gps-safety heat-pad pet-heat-pad for-pets for-you weighted".split())

ORDER = {}   # first word -> (category index, subtype index, subtype name)
for ci, (cat, subs) in enumerate(CATS.items()):
    for si, (sub, words) in enumerate(subs.items()):
        for w in words.split():
            ORDER[w] = (ci, si, sub)

def products(query):
    out, after = [], None
    while True:
        r = gql("""query($q:String,$a:String){products(first:100,after:$a,query:$q){nodes{id title handle status productType tags
                   seo{title} priceRangeV2{maxVariantPrice{amount}}} pageInfo{hasNextPage endCursor}}}""", {"q": query, "a": after})["products"]
        out += r["nodes"]
        if not r["pageInfo"]["hasNextPage"]: return out
        after = r["pageInfo"]["endCursor"]

def category(p):
    word = p["title"].split()[0]
    if word in ORDER: return ORDER[word][:2]
    return next((list(CATS).index(c) for t, c in FALLBACK if t in p["tags"]), len(CATS)), 99

def rank(p, home=None):
    """home: the collection's own category, listed first (Play opens with toys, not the cat bed that is also in it)."""
    ci, si = category(p)
    return (p["status"] != "ACTIVE", ci != home, ci, si, -float(p["priceRangeV2"]["maxVariantPrice"]["amount"]), p["title"])

live = products("status:active")
unmapped = []
for p in live:
    upd = {}
    title = TITLES.get(p["title"], p["title"])
    if title != p["title"]:
        upd["title"] = title
        upd["seo"] = {"title": f"{title} | CozyCompanion"}
    word = title.split()[0]
    if word in ORDER:
        if p["productType"] != ORDER[word][2]: upd["productType"] = ORDER[word][2]
    else:
        unmapped.append(title)
    if upd:
        print(f"{p['title'][:42]:42} ->", ", ".join(f"{k}={v}" for k, v in upd.items() if k != "seo"))
        if not DRY:
            check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}",
                      {"p": {"id": p["id"], **upd}})["productUpdate"], p["handle"])
    junk = [t for t in p["tags"] if t not in KEEP_TAGS and not t.startswith("supplier-")]
    if junk:
        print(f"{p['handle'][:42]:42} -tags {len(junk)}")
        if not DRY:
            check(gql("mutation($id:ID!,$t:[String!]!){tagsRemove(id:$id,tags:$t){userErrors{message}}}", {"id": p["id"], "t": junk})["tagsRemove"], "tags")
if unmapped:
    print("not in the category map yet (sorted by their tags):", unmapped)

# Shop All is a manual collection: every live product belongs in it
shop_all = gql('{collectionByHandle(handle:"smart-pet-tech"){id}}')["collectionByHandle"]["id"]
inside = {p["id"] for p in products("collection_id:" + shop_all.split("/")[-1])}
missing = [p for p in live if p["id"] not in inside and {"dog", "cat"} & set(p["tags"])]   # pets only (Ember is a human heat pad)
if missing:
    print("adding to Shop All:", [p["title"] for p in missing])
    if not DRY:
        check(gql("mutation($id:ID!,$p:[ID!]!){collectionAddProducts(id:$id,productIds:$p){userErrors{message}}}",
                  {"id": shop_all, "p": [p["id"] for p in missing]})["collectionAddProducts"], "shop all")

# every collection: manual, grouped order
cols = gql("{collections(first:100){nodes{id handle sortOrder}}}")["collections"]["nodes"]
for c in cols:
    items = []
    after = None
    while True:
        r = gql("""query($id:ID!,$a:String){collection(id:$id){products(first:250,after:$a){nodes{id title status tags
                   priceRangeV2{maxVariantPrice{amount}}} pageInfo{hasNextPage endCursor}}}}""", {"id": c["id"], "a": after})["collection"]["products"]
        items += r["nodes"]
        if not r["pageInfo"]["hasNextPage"]: break
        after = r["pageInfo"]["endCursor"]
    if len(items) < 2: continue
    items = [{**p, "title": TITLES.get(p["title"], p["title"])} for p in items]
    counts = {}
    for p in items:
        if p["status"] == "ACTIVE": counts[category(p)[0]] = counts.get(category(p)[0], 0) + 1
    home = max(counts, key=counts.get) if counts and max(counts.values()) > len(items) / 2 else None
    want = sorted(items, key=lambda p: rank(p, home))
    print(f"{c['handle']:24} {len(items):3} products, first: {', '.join(p['title'].split()[0] for p in want[:6] if p['status'] == 'ACTIVE')}")
    if DRY: continue
    if c["sortOrder"] != "MANUAL":
        check(gql("mutation($c:CollectionInput!){collectionUpdate(input:$c){userErrors{field message}}}",
                  {"c": {"id": c["id"], "sortOrder": "MANUAL"}})["collectionUpdate"], c["handle"])
    moves = [{"id": p["id"], "newPosition": str(i)} for i, p in enumerate(want)]
    for i in range(0, len(moves), 250):
        check(gql("mutation($id:ID!,$m:[MoveInput!]!){collectionReorderProducts(id:$id,moves:$m){job{id} userErrors{field message}}}",
                  {"id": c["id"], "m": moves[i:i + 250]})["collectionReorderProducts"], c["handle"])
