import sys, os, json
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check, product_ids
reg = json.load(open(os.path.join(S, "files.json")))
PUB = "gid://shopify/Publication/379832926538"
# 1. Tags that drive the smart sub-collections
TAGS = {
    "Smart Pet Feeder Camera 1080P HD": ["feeding"],
    "Automatic Pet Feeder Smart Sensor": ["feeding"],
    "Smart Mini GPS Pet Tracker": ["gps-safety"],
    "Premium Pet Water Fountain 68oz": ["hydration"],
    "Laura Hill Electric Heated Blanket Double": ["for-you"],
    "USB Powered Heated Blanket 3 Settings": ["for-you"],
    "Weighted Heated Blanket 9kg": ["for-you", "weighted"],
    "Pet-Specific Heated Blanket Washable": ["for-pets"],
}
ids = product_ids()
for title, tags in TAGS.items():
    check(gql("mutation($id:ID!,$t:[String!]!){tagsAdd(id:$id,tags:$t){userErrors{message}}}", {"id": ids[title], "t": tags})["tagsAdd"], title)
print("tags ok")
# 2. Smart collections
COLS = [
    ("Heated Blankets for You", "heated-blankets-for-you", "for-you", "l5",
     "Plush, adjustable warmth for cosy nights in, from double-bed comfort to portable USB throws."),
    ("Heated Blankets for Pets", "heated-blankets-for-pets", "for-pets", "l8",
     "Gentle, washable warmth made for curl-up naps, especially loved by senior pets and short-coated companions."),
    ("Weighted Comfort", "weighted-comfort", "weighted", "l7",
     "The calming embrace of evenly distributed weight, paired with soothing warmth."),
    ("Smart Feeding", "smart-feeding", "feeding", "l1",
     "Scheduled, portioned meals and a window into home, so mealtime is handled even when you're away."),
    ("Hydration", "hydration", "hydration", "l4",
     "Fresh, flowing, filtered water that gently encourages your companion to drink more."),
    ("GPS & Safety", "gps-safety", "gps-safety", "l3",
     "Featherlight trackers for confident adventures and peace of mind wherever they wander."),
]
existing = {c["handle"]: c["id"] for c in gql("{collections(first:50){nodes{id handle}}}")["collections"]["nodes"]}
def ensure(title, handle, rules, img, desc):
    inp = {"title": title, "handle": handle, "descriptionHtml": f"<p>{desc}</p>",
           "image": {"src": reg[img]["url"], "altText": reg[img]["alt"]},
           "seo": {"title": f"{title} | CozyCompanion", "description": desc},
           "ruleSet": {"appliedDisjunctively": False, "rules": rules}}
    if handle in existing:
        inp["id"] = existing[handle]; inp.pop("handle")
        r = gql("mutation($i:CollectionInput!){collectionUpdate(input:$i){collection{id} userErrors{message}}}", {"i": inp})["collectionUpdate"]
    else:
        r = gql("mutation($i:CollectionInput!){collectionCreate(input:$i){collection{id} userErrors{message}}}", {"i": inp})["collectionCreate"]
    cid = check(r, handle)["collection"]["id"]
    check(gql("mutation($id:ID!,$p:[PublicationInput!]!){publishablePublish(id:$id,input:$p){userErrors{message}}}", {"id": cid, "p": [{"publicationId": PUB}]})["publishablePublish"], handle)
    print("collection ok:", handle)
for title, handle, tag, img, desc in COLS:
    ensure(title, handle, [{"column": "TAG", "relation": "EQUALS", "condition": tag}], img, desc)
ensure("Gifts under €50", "gifts-under-50", [{"column": "VARIANT_PRICE", "relation": "LESS_THAN", "condition": "50"}], "holiday",
       "Thoughtful, beautifully cosy gifts under €50, for the people and pets you love.")
