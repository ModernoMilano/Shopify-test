"""CozyCompanion pricing rule. Raises any variant priced below target; never lowers a price.

target = cost x multiplier + estimated shipping, rounded UP to a .95 price ending in 4.95 / 9.95
  multiplier: cost < 15 -> 3.0 | < 30 -> 2.6 | < 60 -> 2.3 | otherwise 2.0
  shipping estimate: EU warehouse (Bigbuy) 5, ships from US 8, otherwise 4
Usage: reprice.py [--dry-run]
"""
import sys, os, json, math, subprocess
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)

# fresh token every run (tokens last 24h)
subprocess.run(["curl", "-s", "-X", "POST", f"https://{os.environ['COZY_SHOPIFY_DOMAIN']}/admin/oauth/access_token",
                "-H", "Content-Type: application/x-www-form-urlencoded", "-o", os.path.join(S, "tok.json"),
                "-d", f"grant_type=client_credentials&client_id={os.environ['COZY_SHOPIFY_CLIENT_ID']}&client_secret={os.environ['COZY_SHOPIFY_CLIENT_SECRET']}"], check=True)
from lib import gql, check

DRY = "--dry-run" in sys.argv

def multiplier(cost):
    return 3.0 if cost < 15 else 2.6 if cost < 30 else 2.3 if cost < 60 else 2.0

def shipping(vendor, sku, options):
    text = (sku or "") + " ".join(options)
    if vendor.lower() == "bigbuy": return 5.0
    if "UNITED STATES" in text.upper() or "UNITEDSTATES" in text.upper(): return 8.0
    return 4.0

def charm(x):
    return math.ceil((x + 0.05) / 5) * 5 - 0.05   # 41.2 -> 44.95, 45.0 -> 49.95

assert gql("{shop{myshopifyDomain}}")["shop"]["myshopifyDomain"] == "pj0q30-dd.myshopify.com"
d = gql("""{ products(first:100, query:"-status:archived"){ nodes{ id title vendor tags
  variants(first:100){nodes{id title sku price selectedOptions{value} inventoryItem{unitCost{amount}}}} } } }""")
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
    for v in p["variants"]["nodes"]:
        uc = v["inventoryItem"]["unitCost"]
        if uc:
            cost = float(uc["amount"])
            t = charm(cost * multiplier(cost) + shipping(p["vendor"], v["sku"], [o["value"] for o in v["selectedOptions"]]))
            k = group_key(p, v); targets[k] = max(targets.get(k, 0), t, float(v["price"]))
    for v in p["variants"]["nodes"]:
        uc = v["inventoryItem"]["unitCost"]
        if not uc: print(f"  ! no cost on {p['title']} / {v['title']}: skipped"); continue
        cost = float(uc["amount"])
        target = targets[group_key(p, v)]
        if float(v["price"]) < target:
            upd.append({"id": v["id"], "price": f"{target:.2f}"})
            print(f"  {p['title'][:45]:45} | {v['title'][:30]:30} €{float(v['price']):6.2f} -> €{target:6.2f} (cost €{cost:.2f})")
    if upd and not DRY:
        check(gql("mutation($pid:ID!,$v:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$pid,variants:$v){userErrors{field message}}}",
                  {"pid": p["id"], "v": upd})["productVariantsBulkUpdate"], p["title"])
    changes += len(upd)
print(f"{'would change' if DRY else 'changed'} {changes} variant prices")
