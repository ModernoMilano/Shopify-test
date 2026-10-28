"""Batch 9 (Zendrop): litter mat, hair remover ball, nail grinder, lick mat, plus a new Groom & Clean collection.
Archived: a human hair brush (description is for wigs/scalp, not pets) and a $1.31 'smart' ball (likely shell only; overlaps Zoom)."""
import sys, os, json
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
from brand_batch4 import d, prod
from brand_batch7 import run

ARCHIVE = {"4-in-1-self-cleaning-anti-static-hair-brush-with-massage-and-lifting-function": "human hair brush",
           "wear-resistant-smart-pet-teaser-toy": "$1.31 ball, likely shell only; overlaps Zoom"}

NEW = {
  "paw-clean-honeycomb-litter-mat": dict(title="Sift Honeycomb Litter Mat", handle="sift-honeycomb-litter-mat", type="Litter Mat",
    tags=["litter-hygiene", "cat"], highlights=["Honeycomb top traps litter", "Waterproof bottom layer", "5 sizes, S to XXL"],
    seo="Sift honeycomb litter mat: a double-layer mat that traps scattered litter so you can pour it straight back into the box.",
    html=d("Litter stays by the box, not all over the house.", ["Honeycomb top layer catches litter from paws", "Waterproof bottom layer", "Fold it and pour litter back into the box", "Soft on paws, easy to rinse"], "S 12×12 in · M 12×18 in · L 16×20 in · XL 16×24 in · XXL 24×35 in"),
    options={"Color": ("Color", {"Grey": "Gray"}),
             "Size": ("Size", {"S.30.30cm": "S", "M.30.45cm": "M", "L.40.50cm": "L", "XL.40.60CM": "XL", "XLL.60.90cm": "XXL"})}),
  "reusable-pet-hair-lint-roller-ball": dict(title="Lift Pet Hair Remover Ball", handle="lift-pet-hair-remover-ball", type="Grooming",
    tags=["grooming", "dog", "cat"], highlights=["Lifts pet hair off fabric", "Reusable, rinse and go", "Rose gold or silver"],
    seo="Lift pet hair remover ball: a reusable roller ball that lifts dog and cat hair off sofas, clothes and car seats.",
    html=d("Pet hair off the sofa in a few strokes.", ["Roll over sofas, clothes, beds and car seats", "Reusable: rinse and let it dry", "Comes with a protective cover"], "About 2.8 in · rose gold or silver"),
    options={"Color": ("Color", {"New Rose Gold": "Rose Gold", "Liquid Silver": "Silver"})}),
  "rechargeable-electric-pet-nail-grinder": dict(title="Polish Pet Nail Grinder", handle="polish-pet-nail-grinder", type="Grooming",
    tags=["grooming", "dog", "cat"], highlights=["2 speeds, quiet motor", "Diamond grinding head", "USB rechargeable"],
    seo="Polish pet nail grinder: a quiet, USB rechargeable nail grinder with two speeds and a diamond head for dogs and cats.",
    html=d("Smooth, rounded nails without the clipper stress.", ["Two speeds: 5,000 and 7,000 RPM", "Diamond grinding head", "USB rechargeable, about 4 hours of use", "Go slowly and take breaks with nervous pets"], "5.4 × 1.3 in · white"),
    options={"Color": ("Color", {})}),
  "bone-silicone-licking-dog-slow-food-mat": dict(title="Savor Bone Lick Mat", handle="savor-bone-lick-mat", type="Lick Mat",
    tags=["feeding", "play", "dog"], highlights=["Spread with treats or wet food", "Suction cups hold it in place", "Calming licking activity"],
    seo="Savor bone lick mat: a silicone lick mat for peanut butter, yogurt or wet food that turns treat time into a calming activity.",
    html=d("A calm, happy few minutes, every time.", ["Spread peanut butter, yogurt or wet food", "Textured surface slows them down", "Suction cups hold it to the floor or tub", "Food-grade silicone, easy to rinse"], "5 colors"),
    options={}),
}

def tidy_options():
    p = gql('{productByHandle(handle:"paw-clean-honeycomb-litter-mat"){id variants(first:20){nodes{id title}}}}')["productByHandle"]
    if p:   # odd variant: 'New Grey' only in S, at XXL cost
        drop = [v["id"] for v in p["variants"]["nodes"] if v["title"].startswith("New Grey")]
        if drop:
            check(gql("mutation($p:ID!,$v:[ID!]!){productVariantsBulkDelete(productId:$p,variantsIds:$v){userErrors{field message}}}", {"p": p["id"], "v": drop})["productVariantsBulkDelete"], "sift")
    p = gql('{productByHandle(handle:"reusable-pet-hair-lint-roller-ball"){id options{id name}}}')["productByHandle"]
    if p:   # each colour comes in one size only, so the size option adds nothing
        o = next((o for o in p["options"] if o["name"] == "Size"), None)
        if o:
            check(gql("mutation($p:ID!,$o:[ID!]!){productOptionsDelete(productId:$p,options:$o,strategy:POSITION){userErrors{field message}}}", {"p": p["id"], "o": [o["id"]]})["productOptionsDelete"], "lift")

def groom_collection():
    reg = json.load(open(os.path.join(S, "files.json")))
    existing = {c["handle"]: c["id"] for c in gql("{collections(first:50){nodes{id handle}}}")["collections"]["nodes"]}
    desc = "Brushes, grinders and clean-up helpers for a tidy home and a well-groomed pet."
    inp = {"title": "Groom & Clean", "descriptionHtml": f"<p>{desc}</p>", "image": {"src": reg["z_lift_sofa"]["url"], "altText": reg["z_lift_sofa"]["alt"]},
           "seo": {"title": "Groom & Clean | CozyCompanion", "description": desc},
           "ruleSet": {"appliedDisjunctively": True, "rules": [{"column": "TAG", "relation": "EQUALS", "condition": t} for t in ("grooming", "litter-hygiene")]}}
    if "groom-clean" in existing:
        inp["id"] = existing["groom-clean"]; r = gql("mutation($i:CollectionInput!){collectionUpdate(input:$i){collection{id} userErrors{message}}}", {"i": inp})["collectionUpdate"]
    else:
        inp["handle"] = "groom-clean"; r = gql("mutation($i:CollectionInput!){collectionCreate(input:$i){collection{id} userErrors{message}}}", {"i": inp})["collectionCreate"]
    cid = check(r, "groom-clean")["collection"]["id"]
    check(gql("mutation($id:ID!,$p:[PublicationInput!]!){publishablePublish(id:$id,input:$p){userErrors{message}}}",
              {"id": cid, "p": [{"publicationId": "gid://shopify/Publication/379832926538"}]})["publishablePublish"], "groom-clean")
    print("collection ok: groom-clean")

if __name__ == "__main__":
    for h, why in ARCHIVE.items():
        p = prod(h)
        if p:
            check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": {"id": p["id"], "status": "ARCHIVED"}})["productUpdate"], h)
            print("archived:", h, "-", why)
    tidy_options()
    for old, c in NEW.items():
        run(old, c)
    groom_collection()
