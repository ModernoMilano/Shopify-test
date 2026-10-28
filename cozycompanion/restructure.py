"""High-end pet store: shop by category (Sleep, Dine, Play, Wear & Walk, Travel, Smart Home) and by pet (Dogs, Cats).
Heated blankets leave the menu and homepage. Collection images are our branded editorial shots (m_*)."""
import sys, os, json
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
reg = json.load(open(os.path.join(S, "files.json")))
PUB = "gid://shopify/Publication/379832926538"

# 1. Tags: who it's for (dog / cat) and the new wear / walk / smart groups. Apparel leaves 'travel'.
DOG, CAT, BOTH = ["dog"], ["cat"], ["dog", "cat"]
TAGS = {
    "Brook": BOTH + ["smart"], "Brook XL": BOTH + ["smart"], "Dine": BOTH + ["smart"], "Glance": BOTH + ["smart"],
    "Murmur": BOTH + ["smart"], "Compass": BOTH + ["smart"], "Halo": CAT + ["smart"], "Spark": CAT + ["smart"],
    "Fetch": DOG + ["smart"], "Nestle": BOTH + ["smart"], "Zoom": CAT + ["smart"],
    "Haven": BOTH, "Cloud": BOTH, "Nook": BOTH, "Lounge": BOTH, "Snug": BOTH, "Burrow": BOTH, "Tidy": BOTH, "Voyage": BOTH,
    "Roam": DOG, "Knot": DOG, "Buddy": DOG, "Forage": DOG, "Quest": DOG, "Pace": DOG, "Glide": DOG, "Gnaw": DOG,
    "Riddle": DOG, "Chomp": DOG, "Maze": DOG,
    "Purr": CAT, "Cove": CAT, "Orbit": CAT, "Flutter": CAT, "Flit": CAT, "Plume": CAT, "Chase": CAT, "Fold": CAT,
    "Knit": DOG + ["wear"], "Drizzle": DOG + ["wear"], "Puddle": DOG + ["wear"], "Frost": DOG + ["wear"],
    "Splash": DOG + ["wear"], "Doze": DOG + ["wear"],
    "Stride": DOG + ["walk"], "Wander": CAT + ["walk"], "Glow": DOG + ["walk"],
}
NOT_TRAVEL = {"Knit", "Drizzle", "Puddle", "Frost", "Splash", "Doze", "Stride", "Wander"}

def retag():
    for p in gql('{products(first:150, query:"-status:archived"){nodes{id title tags}}}')["products"]["nodes"]:
        word = p["title"].split()[0] if not p["title"].startswith("Brook XL") else "Brook XL"
        if word not in TAGS: continue
        add = [t for t in TAGS[word] if t not in p["tags"]]
        if add:
            check(gql("mutation($id:ID!,$t:[String!]!){tagsAdd(id:$id,tags:$t){userErrors{message}}}", {"id": p["id"], "t": add})["tagsAdd"], p["title"])
        if word in NOT_TRAVEL and "travel" in p["tags"]:
            check(gql("mutation($id:ID!,$t:[String!]!){tagsRemove(id:$id,tags:$t){userErrors{message}}}", {"id": p["id"], "t": ["travel"]})["tagsRemove"], p["title"])
    print("tags ok")

# 2. Collections
tag = lambda *ts: [{"column": "TAG", "relation": "EQUALS", "condition": t} for t in ts]
COLS = [  # handle, title, rules (None = manual), image, description
    ("smart-pet-tech", "Shop All", None, "m_all", "Considered essentials for the dogs and cats we share our homes with."),
    ("dogs", "For Dogs", tag("dog"), "m_dogs", "Beds, bowls, coats and play for the dogs who make a house a home."),
    ("cats", "For Cats", tag("cat"), "m_cats", "Quiet comforts and clever play for discerning cats."),
    ("beds-dens", "Sleep & Lounge", tag("beds-dens"), "m_sleep", "Plush beds, dens and blankets for long, deep naps."),
    ("smart-feeding", "Dine & Drink", tag("feeding", "hydration"), "m_dine", "Bowls, puzzle feeders and fountains that make every meal better."),
    ("play-enrichment", "Play", tag("play"), "m_play", "Toys that keep curious minds and busy paws happy."),
    ("wear-walk", "Wear & Walk", tag("wear", "walk"), "m_wear", "Coats, harnesses and walking gear, made for every weather."),
    ("pet-travel", "Travel", tag("travel"), "y_roam_life", "Carriers and car comfort for every adventure together."),
    ("smart-home", "Smart Home", tag("smart"), "h2_morning", "Feeders, fountains and trackers that care for them while you're away."),
    ("holiday-gift-guide", "Holiday Gift Guide", None, "m_gifts", "Thoughtful gifts for the pets (and pet people) you love."),
]
def collections():
    existing = {c["handle"]: c["id"] for c in gql("{collections(first:50){nodes{id handle}}}")["collections"]["nodes"]}
    for handle, title, rules, img, desc in COLS:
        inp = {"title": title, "descriptionHtml": f"<p>{desc}</p>",
               "image": {"src": reg[img]["url"], "altText": reg[img]["alt"]},
               "seo": {"title": f"{title} | CozyCompanion", "description": desc}}
        if rules: inp["ruleSet"] = {"appliedDisjunctively": len(rules) > 1, "rules": rules}
        if handle in existing:
            inp["id"] = existing[handle]
            r = gql("mutation($i:CollectionInput!){collectionUpdate(input:$i){collection{id} userErrors{message}}}", {"i": inp})["collectionUpdate"]
        else:
            inp["handle"] = handle
            r = gql("mutation($i:CollectionInput!){collectionCreate(input:$i){collection{id} userErrors{message}}}", {"i": inp})["collectionCreate"]
        cid = check(r, handle)["collection"]["id"]
        check(gql("mutation($id:ID!,$p:[PublicationInput!]!){publishablePublish(id:$id,input:$p){userErrors{message}}}", {"id": cid, "p": [{"publicationId": PUB}]})["publishablePublish"], handle)
        print("collection ok:", handle, "-", title)

# 3. Menus: Shop (by category) / Dogs / Cats / Gifts / Our Story. Heated blankets are no longer a headline.
def menus():
    d = gql("{ collections(first:50){nodes{id handle}} pages(first:30){nodes{id handle}} menus(first:20){nodes{id handle}} }")
    col = {c["handle"]: c["id"] for c in d["collections"]["nodes"]}
    pg = {p["handle"]: p["id"] for p in d["pages"]["nodes"]}
    ids = {m["handle"]: m["id"] for m in d["menus"]["nodes"]}
    C = lambda t, h, items=None: {"title": t, "type": "COLLECTION", "resourceId": col[h], "items": items or []}
    P = lambda t, h: {"title": t, "type": "PAGE", "resourceId": pg[h], "items": []}
    MENUS = {
        "main-menu": ("Main menu", [
            C("Shop", "smart-pet-tech", [
                C("Sleep & Lounge", "beds-dens"), C("Dine & Drink", "smart-feeding"), C("Play", "play-enrichment"),
                C("Wear & Walk", "wear-walk"), C("Groom & Clean", "groom-clean"), C("Travel", "pet-travel"), C("Smart Home", "smart-home"), C("Shop all", "smart-pet-tech")]),
            C("Dogs", "dogs"), C("Cats", "cats"),
            C("Gifts", "holiday-gift-guide", [
                C("Holiday Gift Guide", "holiday-gift-guide"), C("Gifts under $50", "gifts-under-50"), C("Bundle & Save 10%", "bundle-deals")]),
            P("Our Story", "about")]),
        "footer-shop": ("Shop", [C("For Dogs", "dogs"), C("For Cats", "cats"), C("Sleep & Lounge", "beds-dens"),
                                 C("Dine & Drink", "smart-feeding"), C("Play", "play-enrichment"), C("Wear & Walk", "wear-walk"),
                                 C("Gift Guide", "holiday-gift-guide"), P("Our Story", "about")]),
    }
    for handle, (title, items) in MENUS.items():
        r = gql("mutation($id:ID!,$t:String!,$h:String,$i:[MenuItemUpdateInput!]!){menuUpdate(id:$id,title:$t,handle:$h,items:$i){menu{handle} userErrors{field message}}}",
                {"id": ids[handle], "t": title, "h": handle, "i": items})["menuUpdate"]
        check(r, handle); print("menu ok:", handle)

if __name__ == "__main__":
    retag(); collections(); menus()
