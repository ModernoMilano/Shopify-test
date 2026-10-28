"""'Complete the set' bundles: each set gets 20% off automatically when all its pieces are in the cart.
Shows on every member's product page via the cc-bundle theme block (metafields custom.bundle_products / bundle_name).
Only price-3x products (3x cost + shipping) are bundled, so 20% off still leaves a healthy margin.
Shopify allows 25 active automatic discounts; 23 sets + 'Bundle & Save' = 24."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check

PCT = 0.20
SETS = [
    ("The Evening Walk", ["stride-dog-harness-leash-set", "beacon-led-collar-light"]),
    ("The Winter Walk", ["frost-harness-winter-dog-jacket", "mistle-knit-dog-hood", "puddle-suspender-dog-boots"]),
    ("The Rainy Day Set", ["drizzle-dog-raincoat", "puddle-suspender-dog-boots", "splash-quick-dry-dog-bathrobe"]),
    ("The Cozy Nap Set", ["burrow-plush-pet-bed", "snug-sherpa-pet-blanket", "doze-dog-pajamas"]),
    ("The Big Dog Sleep Set", ["dream-memory-foam-dog-bed", "snug-sherpa-pet-blanket"]),
    ("The Lounge Set", ["lounge-plush-pet-sofa", "cloud-plush-pet-blanket"]),
    ("The Den Set", ["haven-pet-den", "nook-self-warming-pet-mat"]),
    ("The Cat Play Set", ["pounce-automatic-feather-cat-toy", "chirp-catnip-ball", "plume-feather-teaser-wand"]),
    ("The Window Watch Set", ["wiggle-window-cat-teaser", "flit-flapping-bird-cat-toy", "chase-plush-prey-cat-toy"]),
    ("The Indoor Hunt Set", ["spark-laser-cat-toy", "flutter-cat-play-station", "zoom-self-rolling-cat-ball"]),
    ("The Scratch & Rest Set", ["fold-magnetic-cat-scratcher", "orbit-felt-cat-tunnel-bed"]),
    ("The Brain Games Set", ["riddle-treat-dispensing-ball", "savor-bone-lick-mat", "maze-puzzle-feeder-bowl"]),
    ("The Fetch Set", ["fetch-automatic-ball-launcher", "glide-soft-dog-frisbee", "knot-tug-fetch-ball"]),
    ("The Chew Set", ["gnaw-dental-chew-toy", "chomp-rubber-treat-ball", "buddy-plush-dog-toy"]),
    ("The Snuffle Set", ["forage-snuffle-mat", "quest-dog-puzzle-feeder"]),
    ("The Cat Dining Set", ["purr-tilted-ceramic-cat-bowl", "cove-ceramic-cat-bowl", "slate-silicone-feeding-mat"]),
    ("The Dog Dining Set", ["pace-stainless-slow-feeder-bowl", "tidy-double-bowl-feeder", "measure-smart-scale-scoop"]),
    ("The Grooming Kit", ["tame-dematting-comb", "polish-pet-nail-grinder", "lift-pet-hair-remover-ball"]),
    ("The Bath Day Set", ["breeze-pet-grooming-dryer", "splash-quick-dry-dog-bathrobe"]),
    ("The Cat Travel Set", ["jetset-soft-pet-carrier", "wander-cat-harness-leash", "bloom-floral-cat-collar"]),
    ("The Little One Set", ["cradle-pet-sling-carrier", "dapper-gingham-bow-tie", "knit-small-dog-sweater"]),
    ("The Road Trip Set", ["roam-back-seat-dog-bed", "ascend-acacia-pet-stairs-ramp"]),
    ("The Clean Litter Set", ["halo-self-cleaning-litter-box", "sift-honeycomb-litter-mat"]),
]
START = "2026-10-28T00:00:00Z"

def ensure_definitions():
    for key, name, typ in (("bundle_products", "Bundle products", "list.product_reference"), ("bundle_name", "Bundle name", "single_line_text_field")):
        r = gql("""mutation($d:MetafieldDefinitionInput!){metafieldDefinitionCreate(definition:$d){createdDefinition{id} userErrors{code message}}}""",
                {"d": {"name": name, "namespace": "custom", "key": key, "type": typ, "ownerType": "PRODUCT", "access": {"storefront": "PUBLIC_READ"}}})["metafieldDefinitionCreate"]
        errs = [e for e in r["userErrors"] if e["code"] != "TAKEN"]
        if errs: sys.exit(f"definition {key}: {errs}")

def ids_for(handles):
    out = {}
    for h in handles:
        p = gql("query($h:String!){productByHandle(handle:$h){id status tags}}", {"h": h})["productByHandle"]
        if not p: sys.exit(f"missing product: {h}")
        if "price-3x" not in p["tags"]: sys.exit(f"not price-3x, would lose margin: {h}")
        out[h] = p["id"]
    return out

if __name__ == "__main__":
    ensure_definitions()
    ids = ids_for({h for _, hs in SETS for h in hs})
    # each product page shows the first set it belongs to
    shown = {}
    for name, hs in SETS:
        for h in hs: shown.setdefault(h, (name, hs))
    mf = []
    for h, (name, hs) in shown.items():
        mf.append({"ownerId": ids[h], "namespace": "custom", "key": "bundle_name", "type": "single_line_text_field", "value": name})
        mf.append({"ownerId": ids[h], "namespace": "custom", "key": "bundle_products", "type": "list.product_reference",
                   "value": __import__("json").dumps([ids[x] for x in hs if x != h])})
    for i in range(0, len(mf), 25):
        check(gql("mutation($m:[MetafieldsSetInput!]!){metafieldsSet(metafields:$m){userErrors{field message}}}", {"m": mf[i:i + 25]})["metafieldsSet"], "bundle metafields")
    print("metafields set on", len(shown), "products")
    existing = {n["discount"]["title"]: n["id"] for n in gql("{discountNodes(first:50){nodes{id discount{... on DiscountAutomaticBasic{title}}}}}")["discountNodes"]["nodes"] if n["discount"].get("title")}
    for name, hs in SETS:
        title = f"{name}: {int(PCT * 100)}% off the set"
        d = {"title": title, "startsAt": START,
             "minimumRequirement": {"quantity": {"greaterThanOrEqualToQuantity": str(len(hs))}},
             "customerGets": {"value": {"percentage": PCT}, "items": {"products": {"productsToAdd": [ids[h] for h in hs]}}},
             "combinesWith": {"productDiscounts": False, "orderDiscounts": False, "shippingDiscounts": True}}
        if title in existing:
            r = gql("mutation($id:ID!,$d:DiscountAutomaticBasicInput!){discountAutomaticBasicUpdate(id:$id,automaticBasicDiscount:$d){userErrors{field message}}}",
                    {"id": existing[title], "d": d})["discountAutomaticBasicUpdate"]
        else:
            r = gql("mutation($d:DiscountAutomaticBasicInput!){discountAutomaticBasicCreate(automaticBasicDiscount:$d){userErrors{field message}}}", {"d": d})["discountAutomaticBasicCreate"]
        check(r, title); print("discount ok:", title)
