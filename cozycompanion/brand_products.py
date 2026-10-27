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
  "rexproduct-petpocket-dog-kennel-size-m-light-gray-with-gray": dict(
    title="Haven Pet Den · Size M", handle="haven-pet-den", type="Pet Bed", template="pettech",
    tags=["beds-dens", "for-pets-living"], cols=["holiday-gift-guide", "bundle-deals"],
    highlights=["Bed and den in one", "Quiet, scratch-resistant felt", "Washable cover, non-slip base"],
    seo="Haven Pet Den: a foldable Scandinavian-style bed and den for cats and small dogs, made in Poland from recycled, Oeko-Tex certified materials.",
    html=d("A calm, cosy hideaway that looks beautiful in any room.",
           ["Felt shell softens noise for a calmer rest", "Bite-, tear- and scratch-resistant", "Removable cover, washable at 30 °C", "Oeko-Tex 100 & GRS certified, made in Poland"],
           "Size M: approx. 60 × 63 × 45 cm · foldable · light grey"),
    options={}),
  "doel-2026-upgrade-automatic-smart-litter-box-self-cleaning-cat-litter": dict(
    title="Halo Self-Cleaning Litter Box", handle="halo-self-cleaning-litter-box", type="Litter Box", template="pettech",
    tags=["litter-hygiene"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    highlights=["Cleans itself after every visit", "4 weight sensors for safety", "App control via 2.4 GHz Wi-Fi"],
    seo="Halo self-cleaning cat litter box with weight sensors, app control and a spacious 65L drum. For cats from 1.5 to 8 kg.",
    html=d("Less scooping, a fresher home and more time together.",
           ["Automatic cleaning after each visit", "4 gravity sensors pause the drum when a cat is near", "Spacious 65L drum for cats of 1.5–8 kg", "App control and schedules (2.4 GHz Wi-Fi)"],
           "For cats older than 6 months · clumping litter only (bentonite, mineral, mixed, small tofu) · place on a flat, hard floor"),
    options={"Color": ("Colour", {"WHITE": "White"}), "Ships From": ("Ships from", {})}),
  "4l-with-hd-camera-automatic-pet-feeder-cat-and-dog-food-automatic": dict(
    title="Glance 4L Camera Feeder", handle="glance-camera-feeder", type="Smart Pet Feeder", template="pettech",
    tags=["feeding", "camera-feeder"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    highlights=["HD camera to check in anytime", "Scheduled meals via the app", "One or two stainless bowls"],
    seo="Glance 4L automatic pet feeder with HD camera, app-scheduled meals and stainless steel bowls. Single or double bowl, in white or black.",
    html=d("See them, feed them and stay close, wherever your day takes you.",
           ["HD camera with live view in the app", "Timed, portioned meals", "Double bowl option for two pets", "Dual power: adapter plus battery backup"],
           "4L visible food container · approx. 32 × 19 × 28 cm · stainless steel bowls"),
    options={"Color": ("Style", {"Double Meal Black": "Black · 2 bowls", "Single Meal White": "White · 1 bowl",
                                 "Double Meal White": "White · 2 bowls", "Single Meal Black": "Black · 1 bowl"}),
             "Volume": ("Capacity", {})}),
  "rojeco-automatic-cat-feeder-with-camera-video-cat-food-dispenser-pet": dict(
    title="Murmur 3L Camera Feeder", handle="murmur-camera-feeder", type="Smart Pet Feeder", template="pettech",
    tags=["feeding", "camera-feeder"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    highlights=["Live video and two-way voice", "Record a 10-second meal call", "Up to 8 meals a day"],
    seo="Murmur 3L camera pet feeder with live video, two-way voice, a recorded meal call and up to 8 scheduled meals a day.",
    html=d("Call them to dinner in your own voice, even from the office.",
           ["Live video with 115° wide-angle view", "Two-way voice and a 10 s recorded meal call", "Up to 8 meals a day, 1–20 portions each", "Kibble from 3–13 mm"],
           "3L · EU adapter and 1.5 m USB cable included"),
    options={"Color": ("Version", {"3L Camera Version": "3L · camera"})}),
  "7l-stainless-steel-wireless-recharging-sensor-cat-water-fountain-auto": dict(
    title="Brook XL Cordless Fountain 7L", handle="brook-xl-cordless-fountain", type="Pet Water Fountain", template="pettech",
    tags=["hydration", "fountain"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    highlights=["Cordless: 4000 mAh battery", "Sensor, timer or constant flow", "Large 7L stainless bowl"],
    seo="Brook XL cordless stainless steel pet fountain: 7L capacity, 4000 mAh battery and sensor, timer or constant flow modes.",
    html=d("Fresh running water anywhere, no cable in sight.",
           ["4000 mAh battery, place it anywhere", "3 modes: sensor, timer or constant (when plugged in)", "Shallow 1\" tray suits how dogs lap", "7L: refill about once a week"],
           "Stainless steel · up to 50 days standby in timer mode · choose with or without spare filters"),
    options={"Color": ("Filters", {"OnLy Pet Water": "Fountain only", "Pet Water 3Chips": "+ 3 spare filters",
                                   "Pet Water 6Chips": "+ 6 spare filters", "Pet Water 12Chips": "+ 12 spare filters"})}),
}

COLS = {c["handle"]: c["id"] for c in gql("{collections(first:50){nodes{id handle}}}")["collections"]["nodes"]}

def prod(handle):
    return gql("query($h:String!){productByHandle(handle:$h){id options{id name optionValues{id name}}}}", {"h": handle})["productByHandle"]

for old, (title, handle) in RENAME.items():
    p = prod(old)
    if not p: print("skip (already renamed?)", old); continue
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
