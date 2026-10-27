"""Branded CozyCompanion names for every product, plus full clean-up of the second Spocket batch.
New products (tag price-3x) are priced at 3x cost; reprice.py keeps them there.
Original data: products_snapshot.json / new_products_snapshot.json."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check

def d(lead, bullets, spec):
    return f"<p>{lead}</p><ul>" + "".join(f"<li>{b}</li>" for b in bullets) + f"</ul><p><small>{spec}</small></p>"

# current handle -> new branded title / handle (existing six keep their copy; only name + handle change)
RENAME = {
    "plush-heat-pad": ("Ember Heat Pad 60 × 30 cm", "ember-heat-pad"),
    "heklet-heated-sherpa-throw": ("Hearth Heated Sherpa Throw 180 × 130 cm", "hearth-heated-sherpa-throw"),
    "mitag-duo-smart-tag": ("Compass Smart Tag for Find My & Find Hub", "compass-smart-tag"),
    "heated-pet-pad": ("Nestle Heated Pet Pad", "nestle-heated-pet-pad"),
    "stainless-steel-pet-fountain": ("Brook Stainless Pet Fountain 2L / 4L", "brook-pet-fountain"),
    "automatic-pet-feeder-4l": ("Dine 4L Automatic Feeder", "dine-automatic-feeder"),
}

NEW = {
  "rojeco-2-in-1-smart-cat-toys-automatic-feather-fun-ball-toy-set-for": dict(
    title="Flutter 2-in-1 Cat Play Station", handle="flutter-cat-play-station", type="Cat Toy", template="pettech",
    tags=["play"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    highlights=["Pop-up feather and rolling ball", "Several speed and light modes", "Battery or cable powered"],
    seo="Flutter 2-in-1 interactive cat toy: a feather that pops out at random and a rolling ball, with several play modes.",
    html=d("Hunting instinct, satisfied: a feather that pops up where they least expect it.",
           ["Feather appears at random from 6 openings", "Rolling ball in the track for double the fun", "Fast, medium and smart play modes", "Replaceable feathers included"],
           "Power: 4 × AA (not included) or power cable"),
    options={"Color": ("Colour", {})}),
  "rojeco-automatic-cat-laser-toy-interactive-adjustable-mode-electric": dict(
    title="Spark Automatic Laser Cat Toy", handle="spark-laser-cat-toy", type="Cat Toy", template="pettech",
    tags=["play"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    highlights=["Plays on its own, 10 min every 2 h", "360° rotation, magnetic base", "Rechargeable via USB-C"],
    seo="Spark automatic laser cat toy with timed play sessions, 360° rotation, a magnetic base and a rechargeable USB-C battery.",
    html=d("Playtime that starts itself, even while you're out.",
           ["Random-moving laser dot for chase and pounce", "Auto play: 10 minutes every 2 hours", "Magnetic base, 360° rotation", "Very quiet operation"],
           "1000 mAh battery · USB-C · never shine the laser into eyes"),
    options={"Color": ("Colour", {}), "Ships From": ("Ships from", {})}),
  "extra-large-portable-pet-trolley-case-detachable-dog-trolley-case": dict(
    title="Voyage Rolling Pet Carrier XL", handle="voyage-rolling-pet-carrier", type="Pet Carrier", template="pettech",
    tags=["travel"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    highlights=["Wheels and telescopic handle", "Mesh windows and top opening", "Carries pets up to approx. 16 kg"],
    seo="Voyage XL rolling pet carrier with wheels, telescopic handle, mesh windows and a top opening. For cats and small dogs up to approx. 16 kg.",
    html=d("Travel together, comfortably and in style.",
           ["Detachable trolley with 4 wheels", "Mesh windows and curtains for calm and airflow", "Top and front openings, handy pockets", "Holds up to approx. 16 kg (35 lbs)"],
           "Approx. 60 × 39 × 44 cm · grey, black, blue or pink"),
    options={"Color": ("Colour", {})}),
  "dog-seat-cover-car-seat-cover-for-pets-waterproof-pet-seat-cover": dict(
    title="Roam Back Seat Dog Bed & Cover", handle="roam-back-seat-dog-bed", type="Car Seat Cover", template="pettech",
    tags=["travel"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    highlights=["Turns the back seat into a flat bed", "Waterproof, quilted surface", "Mesh window and door flaps"],
    seo="Roam back seat dog bed and car seat cover: a firm, flat, waterproof bed for the back seat with mesh window and door protection.",
    html=d("Road trips, sorted: a flat, cosy bed across the whole back seat.",
           ["Firm base bridges the footwell into one flat bed", "Waterproof quilted fabric protects your seats", "Side flaps protect doors; mesh window to see each other", "Pockets and harness openings"],
           "Fits most cars · approx. 112 cm wide · black or grey"),
    options={"Color": ("Colour", {}), "Ships From": ("Ships from", {})}),
}

COLS = {c["handle"]: c["id"] for c in gql("{collections(first:50){nodes{id handle}}}")["collections"]["nodes"]}

def prod(handle):
    return gql("query($h:String!){productByHandle(handle:$h){id options{id name optionValues{id name}}}}", {"h": handle})["productByHandle"]

for old, (title, handle) in RENAME.items():
    p = prod(old)
    if not p: continue
    check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){product{id} userErrors{field message}}}",
              {"p": {"id": p["id"], "title": title, "handle": handle, "redirectNewHandle": True,
                     "seo": {"title": f"{title} | CozyCompanion"}}})["productUpdate"], title)
    print("renamed:", title)

for old, c in NEW.items():
    p = prod(old) or prod(c["handle"])
    pid = p["id"]
    check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){product{id} userErrors{field message}}}",
        {"p": {"id": pid, "title": c["title"], "handle": c["handle"], "redirectNewHandle": True, "descriptionHtml": c["html"],
               "productType": c["type"], "templateSuffix": c["template"],
               "seo": {"title": f"{c['title']} | CozyCompanion", "description": c["seo"]}}})["productUpdate"], c["title"])
    check(gql("mutation($id:ID!,$t:[String!]!){tagsAdd(id:$id,tags:$t){userErrors{message}}}",
              {"id": pid, "t": c["tags"] + ["price-3x"]})["tagsAdd"], "tags")
    mf = [{"ownerId": pid, "namespace": "custom", "key": f"highlight_{i+1}", "type": "single_line_text_field", "value": h}
          for i, h in enumerate(c["highlights"])]
    check(gql("mutation($m:[MetafieldsSetInput!]!){metafieldsSet(metafields:$m){userErrors{field message}}}", {"m": mf})["metafieldsSet"], "mf")
    for opt_name, (new_name, values) in c["options"].items():
        o = next((o for o in prod(c["handle"])["options"] if o["name"] == opt_name), None)
        if not o: continue
        upd = [{"id": v["id"], "name": values[v["name"]]} for v in o["optionValues"] if v["name"] in values]
        check(gql("""mutation($pid:ID!,$o:OptionUpdateInput!,$v:[OptionValueUpdateInput!]){productOptionUpdate(productId:$pid,option:$o,optionValuesToUpdate:$v){userErrors{field message}}}""",
                  {"pid": pid, "o": {"id": o["id"], "name": new_name}, "v": upd})["productOptionUpdate"], f"{c['title']} {opt_name}")
    for h in c["cols"]:
        gql("mutation($id:ID!,$p:[ID!]!){collectionAddProducts(id:$id,productIds:$p){userErrors{message}}}", {"id": COLS[h], "p": [pid]})
    print("cleaned:", c["title"])
