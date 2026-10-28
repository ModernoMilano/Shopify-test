"""Batch 6 (Zendrop): harnesses, toys, snuffle mat, sweater, raincoat. Same flow as brand_batch4."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
from brand_batch4 import d, COLS, prod

C3 = ["smart-pet-tech", "holiday-gift-guide", "bundle-deals"]
NEW = {
  "adjustable-dog-harness-leash-set": dict(title="Stride Dog Harness & Leash Set", handle="stride-dog-harness-leash-set", type="Dog Harness",
    tags=["travel"], cols=C3, highlights=["Harness and leash in one set", "Adjustable, sizes XS to XL", "Padded, breathable fit"],
    seo="Stride dog harness and leash set: an adjustable, padded no-fuss harness with a matching leash, in sizes XS to XL.",
    html=d("Everything you need for the daily walk: a comfy harness with a matching leash.", ["Adjustable straps for a secure, snug fit", "Breathable padded mesh", "Sturdy clip ring and matching leash", "Sizes XS to XL, many colors"], "Nylon · sizes XS–XL"),
    options={"Size": ("Size", {"Small": "S", "Medium": "M", "Large": "L"}), "Color": ("Color", {"Gray": "Gray", "Rose Red": "Raspberry", "Camouflage": "Camo"})}),
  "cat-harness-with-adjustable-leash-and-collar": dict(title="Wander Cat Harness & Leash", handle="wander-cat-harness-leash", type="Cat Harness",
    tags=["travel"], cols=C3, highlights=["Escape-resistant vest fit", "Soft breathable mesh", "Leash included"],
    seo="Wander cat harness and leash: a soft, breathable vest harness with an adjustable fit and matching leash for safe outdoor adventures.",
    html=d("Safe little adventures outdoors, in a vest they'll barely notice.", ["Soft, breathable double-layer mesh", "Adjustable straps and secure buckles", "Matching leash included", "Sizes S to L"], "Polyester mesh · sizes S–L"),
    options={}),
  "flapping-bird-cat-toy-usb-rechargeable": dict(title="Flit Flapping Bird Cat Toy", handle="flit-flapping-bird-cat-toy", type="Cat Toy",
    tags=["play"], cols=C3, highlights=["Flaps like a real bird", "Activates on touch", "USB rechargeable"],
    seo="Flit flapping bird cat toy: a realistic bird that flaps its wings on touch to trigger your cat's hunting instinct. USB rechargeable.",
    html=d("A bird that flaps back: the toy that wakes up every cat's inner hunter.", ["Realistic flapping wings and chirp", "Starts moving when your cat touches it", "Soft, safe plush body", "USB rechargeable, no batteries"], "Approx. 6.7 in · USB rechargeable"),
    options={"Color": ("Style", {"Picture Style": "Sparrow"}), "Size": ("Size", {"17cm": "6.7 in"})}),
  "interactive-indoor-cat-ball-toy": dict(title="Zoom Self-Rolling Cat Ball", handle="zoom-self-rolling-cat-ball", type="Cat Toy",
    tags=["play"], cols=C3, highlights=["Rolls and turns on its own", "Two speed modes", "USB rechargeable"],
    seo="Zoom self-rolling cat ball: rolls randomly with two speed modes to keep indoor cats moving. USB rechargeable.",
    html=d("A ball that runs away, so your cat finally gets a workout.", ["Random rolling and turning, avoids obstacles", "Two speed modes", "Durable shell for hard floors and rugs", "USB rechargeable"], "USB rechargeable · blue or orange"),
    options={}),
  "diy-colorful-feather-cat-teaser-wand-for-pets": dict(title="Plume Feather Teaser Wand", handle="plume-feather-teaser-wand", type="Cat Toy",
    tags=["play"], cols=C3, highlights=["Natural pheasant feathers", "Flexible wand", "Bonding playtime"],
    seo="Plume feather teaser wand with natural pheasant feathers for interactive play and bonding with your cat.",
    html=d("The classic for a reason: flick, swoop and watch them pounce.", ["Natural pheasant feather topper", "Flexible wand for realistic movement", "Builds bonding through play", "Feather colors vary"], "Feather colors vary"),
    options={"Color": ("Color", {"Random Color": "Assorted"})}),
  "dog-toy-tug-rope-toy-training-ball": dict(title="Knot Tug & Fetch Ball", handle="knot-tug-fetch-ball", type="Dog Toy",
    tags=["play"], cols=C3, highlights=["Tug, fetch and chew", "Durable TPR rubber", "Great for training"],
    seo="Knot tug and fetch ball: a durable TPR rubber ball on a rope for tug of war, fetch and training.",
    html=d("One toy, three games: tug, fetch and chew.", ["Durable, flexible TPR rubber", "Rope handle for tug of war and long throws", "Textured surface", "Great for training rewards"], "TPR rubber · rope handle"),
    options={"Color": ("Color", {"Default": "Classic"})}),
  "soft-plush-dog-toy": dict(title="Buddy Plush Dog Toy", handle="buddy-plush-dog-toy", type="Plush Toy",
    tags=["play"], cols=C3, highlights=["Lifelike breed designs", "Super-soft short plush", "Huggable gift"],
    seo="Buddy plush dog toy: lifelike, super-soft plush dogs in nine breeds. A huggable gift for dog lovers.",
    html=d("A lifelike plush pup to hug, gift or keep on the shelf.", ["Nine lifelike breeds", "Super-soft short plush", "Filled with soft PP cotton", "A sweet gift for dog lovers"], "Plush · not a chew toy"),
    options={"Color": ("Breed", {"Wales": "Corgi", "Bernard": "St. Bernard", "Hiromi": "Pomeranian"}), "Size": ("Size", {"Standard": "One size"})}),
  "dog-snuffle-mat-for-pet-enrichment-and-training": dict(title="Forage Snuffle Mat", handle="forage-snuffle-mat", type="Dog Toy",
    tags=["play", "feeding"], cols=C3, highlights=["Sniff-and-find enrichment", "Slows down eating", "Machine washable"],
    seo="Forage snuffle mat: hide kibble and treats in soft fabric folds so dogs can sniff, search and slow down.",
    html=d("Ten minutes of sniffing beats a long walk for a tired, happy dog.", ["Hide kibble and treats in soft folds and pockets", "Natural foraging calms and focuses", "Slows down fast eaters", "Non-slip base, machine washable"], "Fleece and felt · non-slip base"),
    options={}),
  "small-dog-sweater": dict(title="Knit Small Dog Sweater", handle="knit-small-dog-sweater", type="Dog Apparel",
    tags=["travel"], cols=C3, highlights=["Soft stretch knit", "Warm without overheating", "Sizes XS to XL"],
    seo="Knit small dog sweater: soft, stretchy knit that keeps small dogs warm on chilly walks, in sizes XS to XL.",
    html=d("A cozy knit for chilly walks and drafty evenings.", ["Soft, stretchy knit for a snug fit", "Warm but breathable", "Easy to pull on", "For small dogs, sizes XS to XL"], "Knit · sizes XS–XL"),
    options={"Size": ("Size", {"Small": "S", "Medium": "M", "Large": "L"})}),
  "all-weather-dog-raincoat": dict(title="Drizzle Dog Raincoat", handle="drizzle-dog-raincoat", type="Dog Apparel",
    tags=["travel"], cols=C3, highlights=["Waterproof, full coverage", "Adjustable fit", "Lightweight"],
    seo="Drizzle dog raincoat: waterproof, full-coverage and lightweight, with an adjustable fit for rainy walks.",
    html=d("Rainy walks, dry dog: full coverage that's easy to slip on.", ["Waterproof material", "Full body coverage with hood", "Adjustable for a secure fit", "Lightweight and packable"], "Sizes S–2XL · yellow, raspberry or lagoon blue"),
    options={"Color": ("Color", {"Rose Red": "Raspberry", "Lagoon Blue": "Lagoon"}), "Size": ("Size", {"Small": "S", "Medium": "M", "Large": "L", "X Large": "XL", "2X Large": "2XL"})}),
}

def fix_sweater():
    p = gql('{productByHandle(handle:"small-dog-sweater"){id options{id name optionValues{id name hasVariants}} variants(first:20){nodes{id selectedOptions{name value}}}}}')["productByHandle"]
    if not p: return
    o = next(o for o in p["options"] if o["name"] == "Color")
    moves = [{"id": v["id"], "optionValues": [{"optionName": "Color", "name": "n/a"}, {"optionName": "Size", "name": v["selectedOptions"][1]["value"]}]}
             for v in p["variants"]["nodes"] if v["selectedOptions"][0]["value"] != "n/a"]
    if moves: check(gql("mutation($p:ID!,$v:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$p,variants:$v){userErrors{field message}}}", {"p": p["id"], "v": moves})["productVariantsBulkUpdate"], "sweater move")
    o = gql('{productByHandle(handle:"small-dog-sweater"){options{id name optionValues{id name hasVariants}}}}')["productByHandle"]["options"][0]
    dead = [v["id"] for v in o["optionValues"] if not v["hasVariants"]]
    keep = [{"id": v["id"], "name": "Classic"} for v in o["optionValues"] if v["hasVariants"]]
    check(gql("mutation($pid:ID!,$o:OptionUpdateInput!,$v:[OptionValueUpdateInput!],$d:[ID!]){productOptionUpdate(productId:$pid,option:$o,optionValuesToUpdate:$v,optionValuesToDelete:$d){userErrors{field message}}}",
              {"pid": p["id"], "o": {"id": o["id"], "name": "Color"}, "v": keep, "d": dead})["productOptionUpdate"], "sweater option")

if __name__ == "__main__":
    fix_sweater()
    steam = prod("steam-pet-brush")
    if steam:  # ships with a tea-tree-oil 'essence': tea tree oil is toxic to cats, so we don't sell it
        check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": {"id": steam["id"], "status": "ARCHIVED"}})["productUpdate"], "steam")
        print("archived: Steam Pet Brush (tea tree oil essence)")
    for old, c in NEW.items():
        p = prod(old) or prod(c["handle"]); pid = p["id"]
        check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}",
            {"p": {"id": pid, "title": c["title"], "handle": c["handle"], "redirectNewHandle": True, "descriptionHtml": c["html"],
                   "vendor": "CozyCompanion", "productType": c["type"], "templateSuffix": "pettech", "status": "DRAFT",
                   "seo": {"title": f"{c['title']} | CozyCompanion", "description": c["seo"]}}})["productUpdate"], c["title"])
        check(gql("mutation($id:ID!,$t:[String!]!){tagsAdd(id:$id,tags:$t){userErrors{message}}}", {"id": pid, "t": c["tags"] + ["price-3x", "supplier-zendrop"]})["tagsAdd"], "tags")
        mf = [{"ownerId": pid, "namespace": "custom", "key": f"highlight_{i+1}", "type": "single_line_text_field", "value": h} for i, h in enumerate(c["highlights"])]
        check(gql("mutation($m:[MetafieldsSetInput!]!){metafieldsSet(metafields:$m){userErrors{field message}}}", {"m": mf})["metafieldsSet"], "mf")
        for opt_name, (new_name, values) in c["options"].items():
            o = next((o for o in prod(c["handle"])["options"] if o["name"] == opt_name), None)
            if not o: continue
            upd = [{"id": v["id"], "name": values[v["name"]]} for v in o["optionValues"] if v["name"] in values and values[v["name"]] != v["name"]]
            check(gql("mutation($pid:ID!,$o:OptionUpdateInput!,$v:[OptionValueUpdateInput!]){productOptionUpdate(productId:$pid,option:$o,optionValuesToUpdate:$v){userErrors{field message}}}",
                      {"pid": pid, "o": {"id": o["id"], "name": new_name}, "v": upd})["productOptionUpdate"], c["title"])
        for h in c["cols"]:
            gql("mutation($id:ID!,$p:[ID!]!){collectionAddProducts(id:$id,productIds:$p){userErrors{message}}}", {"id": COLS[h], "p": [pid]})
        print("branded:", c["title"])
