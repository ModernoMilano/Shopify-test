"""Batch 5 (Zendrop): Orbit, Lounge, Pace, Quest. Same flow as brand_batch4 (draft, 3x, copy, options, collections)."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
from brand_batch4 import d, COLS, prod

NEW = {
  "donut-cat-bed-tunnel": dict(
    title="Orbit Felt Cat Tunnel Bed", handle="orbit-felt-cat-tunnel-bed", type="Cat Bed", template="pettech",
    tags=["beds-dens", "play"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    highlights=["Bed and tunnel in one", "Sturdy felt, zips apart", "Fits cats up to approx. 15 lb"],
    seo="Orbit felt cat tunnel bed: a cozy donut bed and play tunnel in one. Sturdy felt that zips apart into two halves for cleaning.",
    html=d("A cozy hideaway and a play tunnel in one: cats nap in it, then race through it.",
           ["Donut shape with two openings to hide, pounce and sleep", "Sturdy felt keeps its shape", "Zips apart into two halves, easy to clean", "Calm, neutral colors that suit your home"],
           "M approx. 20 × 20 × 9 in · L approx. 24 × 24 × 11 in · felt"),
    options={"Color": ("Color", {"Pink": "Blush", "Dark Grey": "Charcoal", "Light Grey": "Light Gray", "New Light Grey": "Pebble Gray"}),
             "Size": ("Size", {"50x50x23cm": "M · 20 in", "60x60x27cm": "L · 24 in", "50 * 50 * 20": "M · 20 in (low)"})}),
  "luxury-plush-cat-bed": dict(
    title="Lounge Plush Pet Sofa", handle="lounge-plush-pet-sofa", type="Pet Bed", template="pettech",
    tags=["beds-dens"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    highlights=["A real little sofa for them", "Fluffy plush with bolster arms", "Removable cushion"],
    seo="Lounge plush pet sofa for cats and small dogs: fluffy plush, supportive bolster arms and a removable cushion.",
    html=d("Their own little sofa, so yours stays theirs a little less.",
           ["Fluffy plush with supportive bolster arms and back", "Soft removable cushion", "Non-slip base", "For cats and small dogs"],
           "M approx. 22 × 15 in · L 26 × 18 in · XL 30 × 20 in · 2XL 35 × 22 in"),
    options={}),
  "stainless-steel-pet-slow-feeder": dict(
    title="Pace Stainless Slow Feeder Bowl", handle="pace-stainless-slow-feeder-bowl", type="Pet Bowl", template="pettech",
    tags=["feeding"], cols=["smart-pet-tech", "bundle-deals"],
    highlights=["Slows down fast eaters", "Food-grade stainless steel", "Dishwasher-friendly"],
    seo="Pace stainless steel slow feeder bowl: raised ridges slow down fast eaters. Durable, hygienic and easy to clean.",
    html=d("Raised ridges turn gulping into a calmer, slower meal.",
           ["Ridged maze slows down fast eaters", "Durable, hygienic stainless steel", "Wide base that's hard to tip", "Easy to clean, dishwasher-friendly"],
           "Stainless steel · for dogs and cats"),
    options={"Size": ("Size", {"SL1002": "One size"})}),
  "interactive-slow-feeder-puzzle-toy-for-dogs": dict(
    title="Quest Dog Puzzle Feeder", handle="quest-dog-puzzle-feeder", type="Dog Toy", template="pettech",
    tags=["feeding", "play"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    highlights=["Turns treats into a game", "Slides, flips and hidden pockets", "Non-slip base"],
    seo="Quest dog puzzle feeder: an interactive treat puzzle with sliders, flips and hidden pockets that keeps dogs busy and slows eating.",
    html=d("Turn snack time into brain time: sliders, flips and hidden pockets keep them busy.",
           ["Hide kibble or treats in sliders and pockets", "Mental enrichment that eases boredom", "Slows down fast eaters", "Non-slip base, easy to rinse"],
           "Several levels and sizes · BPA-free plastic"),
    options={"Color": ("Level", {"New  SL2": "Level 2 · S", "ML2": "Level 2 · M", "SL3": "Level 3 · S", "ML3": "Level 3 · M", "LL3": "Level 3 · L"})}),
}

def clean_lounge():
    """Drop multi-packs and merge duplicate color names into Blush / Mocha / Cream."""
    p = gql('{productByHandle(handle:"luxury-plush-cat-bed"){id variants(first:60){nodes{id selectedOptions{name value}}}}}')["productByHandle"]
    if not p: return
    gone = [v["id"] for v in p["variants"]["nodes"] if "PC)" in v["selectedOptions"][0]["value"] and "(1PC)" not in v["selectedOptions"][0]["value"]]
    if gone: check(gql("mutation($p:ID!,$v:[ID!]!){productVariantsBulkDelete(productId:$p,variantsIds:$v){userErrors{message}}}", {"p": p["id"], "v": gone})["productVariantsBulkDelete"], "del")
    NAME = lambda s: "Blush" if "Cherry" in s else "Mocha" if "Mousse" in s else "Cream" if "Beige" in s else s
    o = gql('{productByHandle(handle:"luxury-plush-cat-bed"){options{id name optionValues{id name}}}}')["productByHandle"]["options"][0]
    keep = {}
    for v in o["optionValues"]:
        n = NAME(v["name"])
        if n not in keep: keep[n] = v
    check(gql("mutation($pid:ID!,$o:OptionUpdateInput!,$v:[OptionValueUpdateInput!]){productOptionUpdate(productId:$pid,option:$o,optionValuesToUpdate:$v){userErrors{field message}}}",
              {"pid": p["id"], "o": {"id": o["id"], "name": "Color"}, "v": [{"id": v["id"], "name": n} for n, v in keep.items()]})["productOptionUpdate"], "rename")
    vs = gql('{productByHandle(handle:"luxury-plush-cat-bed"){variants(first:60){nodes{id selectedOptions{name value}}}}}')["productByHandle"]["variants"]["nodes"]
    moves = [{"id": v["id"], "optionValues": [{"optionName": "Color", "name": NAME(v["selectedOptions"][0]["value"])}, {"optionName": "Size", "name": v["selectedOptions"][1]["value"]}]}
             for v in vs if NAME(v["selectedOptions"][0]["value"]) != v["selectedOptions"][0]["value"]]
    if moves: check(gql("mutation($p:ID!,$v:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$p,variants:$v){userErrors{field message}}}", {"p": p["id"], "v": moves})["productVariantsBulkUpdate"], "move")
    o = gql('{productByHandle(handle:"luxury-plush-cat-bed"){options{id optionValues{id name hasVariants}}}}')["productByHandle"]["options"][0]
    dead = [v["id"] for v in o["optionValues"] if not v["hasVariants"]]
    if dead: check(gql("mutation($pid:ID!,$o:OptionUpdateInput!,$d:[ID!]){productOptionUpdate(productId:$pid,option:$o,optionValuesToDelete:$d){userErrors{field message}}}",
                       {"pid": p["id"], "o": {"id": o["id"]}, "d": dead})["productOptionUpdate"], "cleanup")

if __name__ == "__main__":
    clean_lounge()
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
