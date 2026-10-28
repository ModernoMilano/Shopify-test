"""Batch 4 (Zendrop imports): branded names, short copy, options, collections, highlights, SEO, price-3x.
Products stay DRAFT until gallery.py has put our own photos on them; then publish_ready() activates them."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check

def d(lead, bullets, spec):
    return f"<p>{lead}</p><ul>" + "".join(f"<li>{b}</li>" for b in bullets) + f"</ul><p><small>{spec}</small></p>"

NEW = {
  "waterproof-shaggy-pet-blanket": dict(
    title="Cloud Plush Pet Blanket", handle="cloud-plush-pet-blanket", type="Pet Blanket", template="pettech",
    tags=["beds-dens"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    highlights=["Faux fur top, sherpa underside", "Water-resistant", "4 sizes, 2 colors"],
    seo="Cloud plush pet blanket with a long-pile faux fur top and sherpa underside. Water-resistant, in 4 sizes and 2 colors.",
    html=d("Cloud-soft faux fur for naps on the couch, bed or back seat, and it keeps fur off what's underneath.",
           ["Long-pile faux fur top, fluffy sherpa underside", "Water-resistant to protect sofas and beds", "Lightweight and easy to throw anywhere", "Mocha or charcoal, sizes S to XL"],
           "Sizes S–XL · mocha or charcoal"),
    options={"Color": ("Color & size", {f"{c} {s}": f"{'Mocha' if c == 'Coffee' else 'Charcoal'} · {s}" for c in ("Coffee", "Gray") for s in ("S", "M", "L", "XL")})}),
  "self-heating-pet-bed": dict(
    title="Nook Self-Warming Pet Mat", handle="nook-self-warming-pet-mat", type="Pet Bed", template="pettech",
    tags=["beds-dens"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    highlights=["Reflects body heat, no power", "Soft velour, cotton filled", "Non-slip, machine washable"],
    seo="Nook self-warming pet mat: a heat-reflective layer returns your pet's body heat. No cord or electricity, soft velour, non-slip and machine washable.",
    html=d("Warmth without a cord: a heat-reflective layer sends your pet's own body heat back to them.",
           ["Heat-reflective insulating layer, no electricity needed", "Soft velour top with cotton filling", "Non-slip, water-resistant bottom", "Machine washable"],
           "Sizes S–XL · gray or caramel · safe to leave unattended"),
    options={"Color": ("Color", {"Grey": "Gray", "Brown": "Caramel"})}),
  "ceramic-cat-bowl-cat-bowl-cat-food-bowl-neck-guard-oblique-mouth-dog-bowl-pet-bowl": dict(
    title="Purr Tilted Ceramic Cat Bowl", handle="purr-tilted-ceramic-cat-bowl", type="Pet Bowl", template="pettech",
    tags=["feeding"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    highlights=["Raised and tilted for comfort", "Glossy, easy-clean ceramic", "Cute cat-ear design"],
    seo="Purr tilted ceramic cat bowl: a raised, tilted bowl that is easier on necks and whiskers, in glossy easy-clean ceramic.",
    html=d("A raised, tilted bowl that's easier on necks and whiskers at every meal.",
           ["Raised base and tilted rim for a more natural posture", "Wide, shallow bowl to avoid whisker fatigue", "Glossy ceramic, easy to clean and heavy enough not to slide", "Sweet cat-ear design"],
           "Ceramic · pink & blue or black & white"),
    options={"Color": ("Colors", {"Pink and Blue": "Pink & Blue", "Black and White": "Black & White"})}),
}

COLS = {c["handle"]: c["id"] for c in gql("{collections(first:50){nodes{id handle}}}")["collections"]["nodes"]}
prod = lambda h: gql("query($h:String!){productByHandle(handle:$h){id options{id name optionValues{id name}}}}", {"h": h})["productByHandle"]

if __name__ == "__main__":
    for old, c in NEW.items():
        p = prod(old) or prod(c["handle"]); pid = p["id"]
        check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}",
            {"p": {"id": pid, "title": c["title"], "handle": c["handle"], "redirectNewHandle": True, "descriptionHtml": c["html"],
                   "vendor": "CozyCompanion", "productType": c["type"], "templateSuffix": c["template"], "status": "DRAFT",
                   "seo": {"title": f"{c['title']} | CozyCompanion", "description": c["seo"]}}})["productUpdate"], c["title"])
        check(gql("mutation($id:ID!,$t:[String!]!){tagsAdd(id:$id,tags:$t){userErrors{message}}}", {"id": pid, "t": c["tags"] + ["price-3x", "supplier-zendrop"]})["tagsAdd"], "tags")
        mf = [{"ownerId": pid, "namespace": "custom", "key": f"highlight_{i+1}", "type": "single_line_text_field", "value": h} for i, h in enumerate(c["highlights"])]
        check(gql("mutation($m:[MetafieldsSetInput!]!){metafieldsSet(metafields:$m){userErrors{field message}}}", {"m": mf})["metafieldsSet"], "mf")
        for opt_name, (new_name, values) in c["options"].items():
            o = next((o for o in prod(c["handle"])["options"] if o["name"] == opt_name), None)
            if not o: continue
            upd = [{"id": v["id"], "name": values[v["name"]]} for v in o["optionValues"] if v["name"] in values]
            check(gql("mutation($pid:ID!,$o:OptionUpdateInput!,$v:[OptionValueUpdateInput!]){productOptionUpdate(productId:$pid,option:$o,optionValuesToUpdate:$v){userErrors{field message}}}",
                      {"pid": pid, "o": {"id": o["id"], "name": new_name}, "v": upd})["productOptionUpdate"], c["title"])
        for h in c["cols"]:
            gql("mutation($id:ID!,$p:[ID!]!){collectionAddProducts(id:$id,productIds:$p){userErrors{message}}}", {"id": COLS[h], "p": [pid]})
        print("branded:", c["title"])
