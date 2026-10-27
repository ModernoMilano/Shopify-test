"""Clean up the six Spocket imports: honest titles/copy, tidy options, profitable prices, collections.
Original data is backed up in products_snapshot.json."""
import sys, os, json
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check

P = {p["handle"]: p for p in json.load(open(os.path.join(S, "products_snapshot.json"))) if p["vendor"] != "CozyCompanion"}

def ul(items):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

PRODUCTS = {
  "portable-heated-blanket-10w-super-soft-fast-heating-electric-plush": dict(
    handle="plush-heat-pad", title="Plush Heat Pad 60 × 30 cm", type="Heat Pad", template="blanket",
    tags=["for-you", "heat-pad"], cols=["cozy-heated-blankets", "holiday-gift-guide", "bundle-deals"],
    tagline="Targeted warmth for your lap, back and shoulders.",
    highlights=["Soft, thick flannel", "Warms up in about 15 minutes", "Overheating protection"],
    seo="A plush 60 × 30 cm heat pad in soft flannel with a detachable controller and overheating protection. Cosy warmth for lap, back or shoulders.",
    html="<p><strong>Small in size, big on comfort.</strong></p>"
         "<p>Drape this plush heat pad over your lap while you read, tuck it behind your back on the sofa or lay it across your shoulders after a long day. Thick, skin-friendly flannel and gentle heat turn any chair into your coziest spot.</p>"
         + ul(["<strong>Soft, thick flannel</strong> &ndash; velvety on the skin and pleasantly substantial.",
               "<strong>Fast, even warmth</strong> &ndash; comfortably warm in about 15 minutes.",
               "<strong>Detachable controller &amp; long cord</strong> &ndash; flexible to use, easy to care for.",
               "<strong>Overheating protection</strong> &ndash; built-in safety for worry-free comfort."])
         + "<p><strong>Size:</strong> approx. 60 × 30 cm &middot; <strong>Power:</strong> 10 W</p>",
    prices={"*": "44.95"}, rename_option={"Color": ("Colour", {"Gray": "Grey"})}),

  "electric-blanket-heklet-innovagoods-white-grey-130-x-180-cm-160-w": dict(
    handle="heklet-heated-sherpa-throw", title="Heklet Heated Sherpa Throw 180 × 130 cm", type="Heated Blanket", template="blanket",
    tags=["for-you", "heated-throw", "ships-from-eu"], cols=["cozy-heated-blankets", "holiday-gift-guide", "bundle-deals"],
    tagline="Velvet on one side, sherpa on the other. Warmth on both.",
    highlights=["9 temperature settings", "Timer with automatic switch-off", "Reversible velvet & sherpa"],
    seo="Reversible heated throw (180 × 130 cm) with velvety top, sherpa reverse, 9 heat settings, timer and automatic switch-off. Ships from the EU.",
    html="<p><strong>Your evening ritual, beautifully upgraded.</strong></p>"
         "<p>One side is velvety soft, the other a cloud of warm sherpa fleece. Wrap yourself up on the sofa, lay it over the bed or keep it close while working from home, then choose exactly how warm you'd like it to be.</p>"
         + ul(["<strong>9 temperature settings</strong> &ndash; from a gentle glow to deep warmth (up to approx. 47&nbsp;&deg;C).",
               "<strong>Timer &amp; automatic switch-off</strong> &ndash; 9 time intervals, so you can drift off without a second thought.",
               "<strong>Reversible design</strong> &ndash; velvety on one side, fleecy sherpa on the other.",
               "<strong>Easy care</strong> &ndash; detach the cable and wash by hand or in the machine.",
               "<strong>Ships from our European warehouse</strong> for quick delivery."])
         + "<p><strong>Size:</strong> 180 × 130 cm &middot; <strong>Power:</strong> 160 W &middot; <strong>Includes:</strong> remote control with removable cable</p>",
    prices={"*": "79.95"}),

  "both-for-ios-android-mili-mitag-duo-item-finder-global-gps-tracking": dict(
    handle="mitag-duo-smart-tag", title="MiTag Duo Smart Tag for Collars & Keys", type="Smart Tag", template="pettech",
    tags=["gps-safety", "smart-tag"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    tagline="Works with Apple Find My or Google Find Hub.",
    highlights=["Apple Find My or Google Find Hub", "Play a sound to find it nearby", "IP65 water-resistant"],
    seo="MiTag Duo smart tag for collars, keys and bags. Works with Apple Find My or Google Find Hub, plays a sound and is IP65 water-resistant.",
    html="<p><strong>A little peace of mind on their collar, your keys or your bag.</strong></p>"
         "<p>MiTag Duo uses the Apple Find My or Google Find Hub network to show where it was last seen, and plays a sound when it's nearby. Clip it to a collar with the leather case, or to your keys and bags.</p>"
         + ul(["<strong>Apple Find My or Google Find Hub</strong> &ndash; pair with one platform at a time; reset to switch.",
               "<strong>Play sound to find</strong> &ndash; locate it quickly around the house or garden.",
               "<strong>IP65 water-resistant</strong> &ndash; ready for rain and muddy walks.",
               "<strong>Optional leather case</strong> with keyring to attach it securely."])
         + "<p><strong>Good to know:</strong> MiTag is a Bluetooth smart tag, not a GPS tracker. Its location updates when a nearby phone in the Find My or Find Hub network passes by, so it works best in populated areas. Not compatible with Huawei phones.</p>",
    prices={"BLACK-1PCS": "24.95", "WHITE-1PCS": "24.95", "BLACK-2PCS": "39.95", "*": "29.95"},
    rename_option={"Color": ("Style", {
        "Black-black case": "Black tag · black leather case", "Black-blue case": "Black tag · blue leather case",
        "Black-2PCS": "2 black tags", "Black-white case": "Black tag · white leather case",
        "White-white case": "White tag · white leather case", "White-black case": "White tag · black leather case",
        "Black-brow case": "Black tag · brown leather case", "White-white paw": "White tag · white paw case",
        "Black-1PCS": "1 black tag", "White-1PCS": "1 white tag", "Black -red case": "Black tag · red leather case"})}),

  "winter-pet-heating-blanket-waterproof-wearable-wear-resistant": dict(
    handle="heated-pet-pad", title="Heated Pet Pad · Waterproof & Bite-Safe", type="Pet Heated Pad", template="blanket",
    tags=["for-pets", "pet-heat-pad"], cols=["cozy-heated-blankets", "smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    tagline="A warm place of their own, gentle on paws and fur.",
    highlights=["3 temperature levels (approx. 35–44 °C)", "Waterproof, stain-resistant fabric", "Anti-bite cable protection"],
    seo="Heated pet pad with 3 temperature levels, waterproof stain-resistant fabric and anti-bite cable. In 45 × 45 or 50 × 70 cm, EU or US plug.",
    html="<p><strong>Because they deserve to be cosy, too.</strong></p>"
         "<p>Senior pets, small breeds and short-coated companions feel the cold first. This heated pad gives them a warm, comfortable spot that heats evenly, never too hot, just right for long naps.</p>"
         + ul(["<strong>3 temperature levels</strong> &ndash; approx. 35&ndash;44&nbsp;&deg;C (95&ndash;112&nbsp;&deg;F) for gentle warmth.",
               "<strong>Even heating</strong> &ndash; evenly spaced heating wires for consistent comfort.",
               "<strong>Waterproof &amp; stain-resistant</strong> &ndash; durable PU Oxford fabric; simply wipe it dry.",
               "<strong>Anti-bite tube</strong> &ndash; protects the cable from curious teeth."])
         + "<p><strong>Sizes:</strong> 45 × 45 cm or 50 × 70 cm &middot; <strong>Power:</strong> 20 W &middot; <strong>Cord:</strong> approx. 147 cm &middot; Choose the <strong>EU</strong> or <strong>US</strong> plug for your country.</p>"
         + "<p>Always supervise pets who like to chew, and make sure your pet can move off the pad if they get too warm.</p>",
    prices={"45CMX45CM": "39.95", "50CMX70CM": "54.95"}, restructure_pad=True),

  "rojeco-stainless-steel-cat-water-fountain-filters-2l-automatic-pet": dict(
    handle="stainless-steel-pet-fountain", title="Stainless Steel Pet Fountain · 2L or 4L", type="Pet Water Fountain", template="pettech",
    tags=["hydration", "fountain"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    tagline="Fresh, filtered, flowing water, in polished stainless steel.",
    highlights=["304 stainless steel", "Ultra-quiet (under 20 dB)", "Dual filtration: carbon + sponge"],
    seo="Stainless steel pet water fountain (2L or 4L) with dual carbon and sponge filtration, ultra-quiet pump and dishwasher-safe parts.",
    html="<p><strong>Fresh water, beautifully kept.</strong></p>"
         "<p>Cats and dogs are naturally drawn to moving water. This fountain keeps it circulating and filtered in a polished 304 stainless-steel bowl that's hygienic, easy to clean and handsome enough for any kitchen.</p>"
         + ul(["<strong>304 stainless steel</strong> &ndash; rust-proof and helps reduce bacterial growth.",
               "<strong>Dual filtration</strong> &ndash; activated carbon filter and pre-filter sponge for cleaner water.",
               "<strong>Ultra-quiet pump</strong> &ndash; under 20 dB, so it won't disturb your evening.",
               "<strong>Water-level window</strong> &ndash; see at a glance when it's time to top up.",
               "<strong>Easy to clean</strong> &ndash; stainless tray and tank are dishwasher safe."])
         + "<p><strong>Capacity:</strong> 2L (about 1&ndash;2 weeks for one adult cat) or 4L &middot; Replace the filter every 2&ndash;4 weeks &middot; <strong>Power:</strong> USB cable included, wall adapter not included.</p>",
    prices={"NEW4L1FILTER-NOPLUG": "69.95", "NEW4L5FILTERS-NOPLUG": "79.95", "NEW4L9FILTERS-NOPLUG": "89.95",
            "NOADAPTER-NOPLUG": "59.95", "9PCSFILTERSET-NOPLUG": "69.95", "17PCSFILTERSET-NOPLUG": "79.95"},
    rename_option={"Color": ("Size & filters", {
        "New 4L 1 Filter": "4L · 1 filter set", "New 4L 5 Filters": "4L · 5 filter sets", "New 4L 9 Filters": "4L · 9 filter sets",
        "No Adapter": "2L · 1 filter set", "9PCS Filter Set": "2L · 9 filter sets", "17PCS Filter Set": "2L · 17 filter sets"}),
        "Voltage/Plug Type": ("Power", {"No plug": "USB (wall adapter not included)"})}),

  "nityers-4l-automatic-cat-feeder-smart-pet-food-dispenser-with-key": dict(
    handle="automatic-pet-feeder-4l", title="4L Automatic Pet Feeder · Stainless Steel Bowl", type="Smart Pet Feeder", template="pettech",
    tags=["feeding", "feeder"], cols=["smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
    tagline="Up to six perfectly timed meals a day, no Wi-Fi needed.",
    highlights=["1–6 scheduled meals per day", "Food-grade stainless steel bowl", "Triple-seal lid keeps kibble fresh"],
    seo="4L automatic pet feeder with 1–6 timed meals a day, portion control, stainless steel bowl and triple-seal freshness lid. No Wi-Fi or app needed.",
    html="<p><strong>Mealtime on time, every time.</strong></p>"
         "<p>Set the schedule once with the simple LCD buttons and your companion's meals are served on time, whether you're working late or away for the weekend. No Wi-Fi, no app, no connection hassle.</p>"
         + ul(["<strong>1&ndash;6 meals a day</strong> &ndash; with customisable portion sizes for a healthy routine.",
               "<strong>Generous 4L capacity</strong> &ndash; ideal for busy weeks and short trips.",
               "<strong>Food-grade stainless steel bowl</strong> &ndash; hygienic and easy to clean.",
               "<strong>Stays fresh</strong> &ndash; soft rubber rotor, triple-seal lid and desiccant box.",
               "<strong>Anti-clog &amp; paw-proof</strong> &ndash; handles dry kibble from 2&ndash;15 mm; the locking lid keeps curious paws out.",
               "<strong>Dual power</strong> &ndash; mains adapter included; optional 3 &times; D batteries (not included) as backup."])
         + "<p><strong>In the box:</strong> feeder, stainless steel bowl, power adapter &amp; cable, user manual &middot; Dry food only.</p>",
    prices={"*": "89.95"},
    rename_option={"Color": ("Colour", {"White Timed Feeder": "White", "Black Timed Feeder": "Black"}),
                   "Volume": ("Bowl", {"ABS SUS": "Stainless steel"})}),
}

COLS = {c["handle"]: c["id"] for c in gql("{collections(first:50){nodes{id handle}}}")["collections"]["nodes"]}

def options(pid):
    return gql("query($id:ID!){product(id:$id){options{id name optionValues{id name}} variants(first:50){nodes{id sku selectedOptions{name value}}}}}",
               {"id": pid})["product"]

for old_handle, c in PRODUCTS.items():
    p = P[old_handle]; pid = p["id"]
    # 1. Core product fields
    check(gql("""mutation($p:ProductUpdateInput!){productUpdate(product:$p){product{id} userErrors{field message}}}""",
        {"p": {"id": pid, "title": c["title"], "handle": c["handle"], "redirectNewHandle": True, "descriptionHtml": c["html"],
               "productType": c["type"], "templateSuffix": c["template"],
               "seo": {"title": f"{c['title']} | CozyCompanion", "description": c["seo"]}}})["productUpdate"], c["title"])
    check(gql("mutation($id:ID!,$t:[String!]!){tagsAdd(id:$id,tags:$t){userErrors{message}}}", {"id": pid, "t": c["tags"]})["tagsAdd"], "tags")
    mf = [{"ownerId": pid, "namespace": "custom", "key": "tagline", "type": "single_line_text_field", "value": c["tagline"]}]
    mf += [{"ownerId": pid, "namespace": "custom", "key": f"highlight_{i+1}", "type": "single_line_text_field", "value": h}
           for i, h in enumerate(c["highlights"])]
    check(gql("mutation($m:[MetafieldsSetInput!]!){metafieldsSet(metafields:$m){userErrors{field message}}}", {"m": mf})["metafieldsSet"], "mf")

    # 2. Option names / values
    for opt_name, (new_name, values) in c.get("rename_option", {}).items():
        o = next(o for o in options(pid)["options"] if o["name"] == opt_name)
        upd = [{"id": v["id"], "name": values[v["name"]]} for v in o["optionValues"] if v["name"] in values]
        check(gql("""mutation($pid:ID!,$o:OptionUpdateInput!,$v:[OptionValueUpdateInput!]){productOptionUpdate(productId:$pid,option:$o,optionValuesToUpdate:$v){userErrors{field message}}}""",
                  {"pid": pid, "o": {"id": o["id"], "name": new_name}, "v": upd})["productOptionUpdate"], f"{c['title']} {opt_name}")

    if c.get("restructure_pad"):
        prod = options(pid)
        o2 = next(o for o in prod["options"] if o["name"] == "Color")
        check(gql("""mutation($pid:ID!,$o:OptionUpdateInput!){productOptionUpdate(productId:$pid,option:$o){userErrors{field message}}}""",
                  {"pid": pid, "o": {"id": o2["id"], "name": "Style"}})["productOptionUpdate"], "pad option")
        size = lambda sku: "45 × 45 cm" if sku.startswith("45CM") or "-45CMX45CM-" in sku else "50 × 70 cm"
        def style(sku):
            pat = "Rose" if "ROSE" in sku else "Paws"
            plug = "US plug" if "US" in sku.split("-")[0] + sku.split("-")[1] else "EU plug"
            return f"{pat} · {plug}"
        upd = [{"id": v["id"], "optionValues": [{"optionName": "Size", "name": size(v["sku"])}, {"optionName": "Style", "name": style(v["sku"])}]}
               for v in prod["variants"]["nodes"]]
        for u, v in zip(upd, prod["variants"]["nodes"]):
            print("   ", v["sku"], "->", [x["name"] for x in u["optionValues"]])
        check(gql("""mutation($pid:ID!,$v:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$pid,variants:$v){userErrors{field message}}}""",
                  {"pid": pid, "v": upd})["productVariantsBulkUpdate"], "pad variants")

    # 3. Prices (no compare-at: no fake "was" prices)
    vs = options(pid)["variants"]["nodes"]
    def price_for(sku):
        if sku in c["prices"]: return c["prices"][sku]
        for k, val in c["prices"].items():
            if k != "*" and k in sku: return val
        return c["prices"]["*"]
    upd = [{"id": v["id"], "price": price_for(v["sku"]), "compareAtPrice": None} for v in vs]
    check(gql("""mutation($pid:ID!,$v:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$pid,variants:$v){userErrors{field message}}}""",
              {"pid": pid, "v": upd})["productVariantsBulkUpdate"], "prices")

    # 4. Manual collections
    for h in c["cols"]:
        r = gql("mutation($id:ID!,$p:[ID!]!){collectionAddProducts(id:$id,productIds:$p){userErrors{message}}}", {"id": COLS[h], "p": [pid]})["collectionAddProducts"]
        if r["userErrors"] and "already" not in str(r["userErrors"]).lower(): print("   col", h, r["userErrors"])
    print("done:", c["title"])
