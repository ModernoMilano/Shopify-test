"""CozyCompanion pricing rule. Raises any variant priced below target; never lowers a price.

Products tagged price-3x are priced at 3x (cost + SHIP_3X shipping), at least FLOOR, rounded up to a clean price (nice()). All others:
every single-item order must leave MARGIN profit after ADS ad spend per purchase:
  price / 1.21 (VAT) - (2.9% + 0.30 payment fee) - cost - shipping - ADS >= MARGIN
  target = (cost + shipping + 0.30 + ADS + MARGIN) / (1/1.21 - 0.029), rounded UP to a x4.95 / x9.95 price
  shipping estimate: EU warehouse (Bigbuy) 5, ships from US 8, otherwise 4
Usage: reprice.py [--dry-run]
"""
import sys, os, json, math, subprocess
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)

# fresh token every run (tokens last 24h)
subprocess.run(["curl", "-sf", "--retry", "4", "--retry-all-errors", "--retry-delay", "5", "-X", "POST", f"https://{os.environ['COZY_SHOPIFY_DOMAIN']}/admin/oauth/access_token",
                "-H", "Content-Type: application/x-www-form-urlencoded", "-o", os.path.join(S, "tok.new"),
                "-d", f"grant_type=client_credentials&client_id={os.environ['COZY_SHOPIFY_CLIENT_ID']}&client_secret={os.environ['COZY_SHOPIFY_CLIENT_SECRET']}"], check=True)
os.replace(os.path.join(S, "tok.new"), os.path.join(S, "tok.json"))
from lib import gql, check

DRY = "--dry-run" in sys.argv

def nice(x):
    """Owner's rule: clean whole-dollar prices, always rounded UP so the margin never shrinks.
    Under $100 they end in 5 or 9 (15, 19, 25, 29 ... 95, 99); from $100 they end in 9 (109, 119 ...)."""
    n = math.ceil(x - 1e-9)
    while not ((n < 100 and n % 10 in (5, 9)) or (n >= 100 and n % 10 == 9)):
        n += 1
    return float(n)
charm = nice

def nice_down(x):
    """Largest clean price at or below x (used to tidy prices that may only go down a little)."""
    n = math.floor(x + 1e-9)
    while not ((n < 100 and n % 10 in (5, 9)) or (n >= 100 and n % 10 == 9)):
        n -= 1
    return float(n)

ADS = 30.0      # ad spend per purchase (EUR), set by the owner
MARGIN = 15.0   # profit left per single-item order after ads
NET = 1 / 1.21 - 0.029

def target_price(cost, ship):
    return charm((cost + ship + 0.30 + ADS + MARGIN) / NET)

SHIP_3X = 4.0   # Zendrop shipping per item, counted into cost before tripling (owner's rule)
FLOOR = 15.0    # nothing in a high-end store sells for less

def triple(cost):
    """Products tagged price-3x: 3x (cost + shipping), never below FLOOR, rounded up to a clean price."""
    return max(FLOOR, nice((cost + SHIP_3X) * 3))

def shipping(vendor, sku, options, tags=()):
    text = (sku or "") + " ".join(options)
    if vendor.lower() == "bigbuy" or "supplier-bigbuy" in tags: return 5.0
    if "UNITED STATES" in text.upper() or "UNITEDSTATES" in text.upper(): return 8.0
    return 4.0

assert gql("{shop{myshopifyDomain}}")["shop"]["myshopifyDomain"] == "pj0q30-dd.myshopify.com"
nodes, after = [], None
while True:   # the catalog is past 100 products, so page through all of it
    page = gql("""query($a:String){ products(first:100, after:$a, query:"-status:archived"){ nodes{ id title vendor tags
      variants(first:100){nodes{id title sku price selectedOptions{value} inventoryItem{unitCost{amount}}}} } pageInfo{hasNextPage endCursor} } }""", {"a": after})["products"]
    nodes += page["nodes"]
    if not page["pageInfo"]["hasNextPage"]: break
    after = page["pageInfo"]["endCursor"]
d = {"products": {"nodes": nodes}}
changes = 0
def group_key(p, v):
    """Variants that look the same to a shopper share one price: same first option when there are
    several options, or same kind (with/without case, 1 vs 2 pieces) for single-option products."""
    vals = [o["value"] for o in v["selectedOptions"]]
    if len(vals) > 1: return vals[0]
    t = vals[0].lower()
    if "2 " in t or "2pcs" in t: return "multi"
    return "case" if "case" in t else "single"

for p in d["products"]["nodes"]:
    upd = []
    targets = {}
    if "price-3x" in p["tags"] or "cc-ready" not in p["tags"]:  # new imports default to the 3x rule
        # exact rule: each variant 3x its own cost; variants within EUR 5 of each other (e.g. colours)
        # share the highest of those prices. Set exactly, so a too-high price is corrected too.
        vs = [v for v in p["variants"]["nodes"] if v["inventoryItem"]["unitCost"]]
        raw = {v["id"]: triple(float(v["inventoryItem"]["unitCost"]["amount"])) for v in vs}
        for v in vs:
            target = max(t for t in raw.values() if abs(t - raw[v["id"]]) < 5)
            if abs(float(v["price"]) - target) > 0.001:
                upd.append({"id": v["id"], "price": f"{target:.2f}"})
                print(f"  {p['title'][:45]:45} | {v['title'][:30]:30} €{float(v['price']):6.2f} -> €{target:6.2f} (3x cost+ship €{float(v['inventoryItem']['unitCost']['amount']):.2f})")
        if upd and not DRY:
            check(gql("mutation($pid:ID!,$v:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$pid,variants:$v){userErrors{field message}}}",
                      {"pid": p["id"], "v": upd})["productVariantsBulkUpdate"], p["title"])
        changes += len(upd)
        continue
    floors = {}
    for v in p["variants"]["nodes"]:
        uc = v["inventoryItem"]["unitCost"]
        if uc:
            cost = float(uc["amount"])
            t = target_price(cost, shipping(p["vendor"], v["sku"], [o["value"] for o in v["selectedOptions"]], p["tags"]))
            k = group_key(p, v); floors[k] = max(floors.get(k, 0), t)
    for v in p["variants"]["nodes"]:
        uc = v["inventoryItem"]["unitCost"]
        if not uc: print(f"  ! no cost on {p['title']} / {v['title']}: skipped"); continue
        cost, price, floor = float(uc["amount"]), float(v["price"]), floors[group_key(p, v)]
        if price < floor:
            target = floor   # already a clean price (target_price rounds up with nice())
        elif nice_down(price) != price and nice_down(price) >= floor:
            # tidy an untidy price DOWN, never up: live ads quote these prices
            target = nice_down(price)
        else:
            continue
        upd.append({"id": v["id"], "price": f"{target:.2f}"})
        print(f"  {p['title'][:45]:45} | {v['title'][:30]:30} €{price:6.2f} -> €{target:6.2f} (cost €{cost:.2f})")
    if upd and not DRY:
        check(gql("mutation($pid:ID!,$v:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$pid,variants:$v){userErrors{field message}}}",
                  {"pid": p["id"], "v": upd})["productVariantsBulkUpdate"], p["title"])
    changes += len(upd)
print(f"{'would change' if DRY else 'changed'} {changes} variant prices")
