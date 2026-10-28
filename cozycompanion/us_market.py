"""Switch CozyCompanion to a US-facing store: US spelling, imperial sizes, US shipping copy,
US-plug / US-warehouse variants only. Store currency, tax-inclusive pricing and units are
changed by the owner in Shopify admin (not available through the API).
Usage: us_market.py [--dry-run]"""
import sys, os, re
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check, theme_file, put_theme_files
DRY = "--dry-run" in sys.argv

SPELL = [(r"\bcosy\b", "cozy"), (r"\bCosy\b", "Cozy"), (r"\bcosier\b", "cozier"), (r"\bgrey\b", "gray"), (r"\bGrey\b", "Gray"),
         (r"\bcolours?\b", lambda m: m.group(0).replace("colour", "color")), (r"\bColour", "Color"),
         (r"\bfavourite", "favorite"), (r"\bpersonalis", "personaliz")]
def us(t):
    for a, b in SPELL: t = re.sub(a, b, t)
    return t

# product handle -> exact text replacements (after spelling), new highlights, title
PRODUCTS = {
  "ember-heat-pad": dict(title="Ember Heat Pad 24 × 12 in", rep=[("60 × 30 cm · 10 W", "24 × 12 in (60 × 30 cm) · 10 W")]),
  "nestle-heated-pet-pad": dict(rep=[("3 levels, approx. 35–44 °C", "3 heat levels, approx. 95–111 °F"), ("<li>EU or US plug</li>", "<li>US plug, 5 ft cord</li>"),
        ("45 × 45 or 50 × 70 cm · 20 W · cord approx. 147 cm", "18 × 18 in or 20 × 28 in · 20 W")]),
  "brook-pet-fountain": dict(rep=[("2L or 4L · USB cable included", "2L (68 oz) or 4L (135 oz) · USB cable included")]),
  "dine-automatic-feeder": dict(rep=[("4L · dry kibble 2–15 mm", "4L (17 cups) · dry kibble up to 0.6 in")]),
  "haven-pet-den": dict(rep=[("washable at 30 °C", "machine washable cold (86 °F)"), ("approx. 60 × 63 × 45 cm", "approx. 24 × 25 × 18 in")]),
  "halo-self-cleaning-litter-box": dict(rep=[("cats of 1.5–8 kg", "cats from 3.3 to 17.6 lb")]),
  "glance-camera-feeder": dict(rep=[("approx. 32 × 19 × 28 cm", "approx. 12.6 × 7.5 × 11 in")]),
  "murmur-camera-feeder": dict(rep=[("<li>Kibble from 3–13 mm</li>", "<li>Kibble from 0.1 to 0.5 in</li>"),
        ("3L · EU adapter and 1.5 m USB cable included", "3L (13 cups) · USB powered, 5 ft USB cable included")]),
  "brook-xl-cordless-fountain": dict(rep=[("7L: refill", "7L (1.8 gal): refill")]),
  "voyage-rolling-pet-carrier": dict(rep=[("Holds up to approx. 16 kg (35 lbs)", "Holds pets up to approx. 35 lb"),
        ("Approx. 60 × 39 × 44 cm", "Approx. 23.6 × 15.4 × 17.3 in")],
        highlights={3: "Carries pets up to approx. 35 lb"}),
  "roam-back-seat-dog-bed": dict(rep=[("approx. 112 cm wide", "approx. 44 in wide")]),
}
# option value renames (after spelling)
VALUES = {"45 × 45 cm": "18 × 18 in", "50 × 70 cm": "20 × 28 in", "Rose · US plug": "Rose", "Paws · US plug": "Paws",
          "China Mainland": "International warehouse"}
# variants a US customer must not be able to buy
DROP = {"nestle-heated-pet-pad": lambda t: "EU plug" in t,
        "halo-self-cleaning-litter-box": lambda t: "United Kingdom" in t or "Germany" in t}
# EU-only products: 230 V plug, ships from an EU warehouse
DRAFT = ["hearth-heated-sherpa-throw"]

ps = gql('{products(first:100, query:"-status:archived"){nodes{id handle title status descriptionHtml '
         'options{id name optionValues{id name}} variants(first:50){nodes{id title}} '
         'metafields(first:5, namespace:"custom"){nodes{key value}}}}}')["products"]["nodes"]
for p in ps:
    h, pid, log = p["handle"], p["id"], []
    if h in DRAFT:
        if p["status"] != "DRAFT":
            log.append("-> DRAFT (EU-only)")
            if not DRY: check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}",
                                  {"p": {"id": pid, "status": "DRAFT"}})["productUpdate"], h)
        print(p["title"], log); continue
    cfg = PRODUCTS.get(h, {})
    upd = {"id": pid}
    html = us(p["descriptionHtml"])
    for a, b in cfg.get("rep", []):
        if a not in html and b not in html: print(f"  ! {h}: '{a}' not found")
        html = html.replace(a, b)
    if html != p["descriptionHtml"]: upd["descriptionHtml"] = html; log.append("description")
    title = cfg.get("title", us(p["title"]))
    if title != p["title"]:
        upd["title"] = title; upd["seo"] = {"title": f"{title} | CozyCompanion"}; log.append(f"title {title}")
    if len(upd) > 1 and not DRY:
        check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": upd})["productUpdate"], h)
    # highlights
    mf = []
    for m in p["metafields"]["nodes"]:
        k = int(m["key"].split("_")[-1]) if m["key"].startswith("highlight_") else None
        if k is None: continue
        v = cfg.get("highlights", {}).get(k, us(m["value"]))
        if v != m["value"]:
            mf.append({"ownerId": pid, "namespace": "custom", "key": m["key"], "type": "single_line_text_field", "value": v})
    if mf:
        log.append(f"{len(mf)} highlights")
        if not DRY: check(gql("mutation($m:[MetafieldsSetInput!]!){metafieldsSet(metafields:$m){userErrors{field message}}}", {"m": mf})["metafieldsSet"], h)
    # drop variants that don't work in the US
    if h in DROP:
        gone = [v["id"] for v in p["variants"]["nodes"] if DROP[h](v["title"])]
        if gone:
            log.append(f"removed {len(gone)} non-US variants")
            if not DRY: check(gql("mutation($pid:ID!,$v:[ID!]!){productVariantsBulkDelete(productId:$pid,variantsIds:$v){userErrors{field message}}}",
                                  {"pid": pid, "v": gone})["productVariantsBulkDelete"], h)
    # option names and values
    if not DRY and h in DROP:
        p["options"] = gql("query($id:ID!){product(id:$id){options{id name optionValues{id name}}}}", {"id": pid})["product"]["options"]
    for o in p["options"]:
        name = us(o["name"]).replace("Ships From", "Ships from")
        vals = [{"id": v["id"], "name": VALUES.get(us(v["name"]), us(v["name"]))} for v in o["optionValues"]
                if VALUES.get(us(v["name"]), us(v["name"])) != v["name"]]
        if name != o["name"] or vals:
            log.append(f"option {name} {[v['name'] for v in vals]}")
            if not DRY:
                r = gql("mutation($pid:ID!,$o:OptionUpdateInput!,$v:[OptionValueUpdateInput!]){productOptionUpdate(productId:$pid,option:$o,optionValuesToUpdate:$v){userErrors{field message}}}",
                        {"pid": pid, "o": {"id": o["id"], "name": name}, "v": vals})["productOptionUpdate"]
                if r["userErrors"]: print("  !", h, r["userErrors"])
    print(p["title"], log)

# collections
for c in gql("{collections(first:50){nodes{id handle title descriptionHtml}}}")["collections"]["nodes"]:
    t, d = us(c["title"]).replace("€", "$"), us(c["descriptionHtml"] or "").replace("€", "$")
    if (t, d) != (c["title"], c["descriptionHtml"] or ""):
        print("collection", c["handle"], t)
        if not DRY: check(gql("mutation($c:CollectionInput!){collectionUpdate(input:$c){userErrors{field message}}}",
                              {"c": {"id": c["id"], "title": t, "descriptionHtml": d}})["collectionUpdate"], c["handle"])

# theme copy
SHIP_OLD = "Dispatched in 1&ndash;3 business days, tracked worldwide. EU delivery 3&ndash;8 business days."
SHIP_NEW = "Dispatched in 1&ndash;3 business days with tracking. Delivery across the US in 5&ndash;12 business days."
THEME_REP = {
  "templates/product.blanket.json": [(SHIP_OLD, SHIP_NEW)],
  "templates/product.pettech.json": [(SHIP_OLD, SHIP_NEW)],
  "templates/product.json": [("shipped worldwide with tracking on every order: 3&ndash;8 business days within the EU, 7&ndash;15 business days to the rest of the world.",
                              "shipped with tracking on every order: delivery across the US in 5&ndash;12 business days.")],
  "templates/index.json": [],
  "snippets/cc-cart-perks.liquid": [("order by <strong>8 December</strong> for the best chance of EU delivery before Christmas.",
                                     "order by <strong>December 5</strong> for the best chance of delivery before Christmas.")],
}
out = {}
for f, reps in THEME_REP.items():
    t = theme_file(f); n = t
    for a, b in reps:
        if a not in n: print(f"  ! {f}: text not found")
        n = n.replace(a, b)
    n = us(n)
    if n != t: out[f] = n; print("theme", f)
if out and not DRY: put_theme_files(out)
