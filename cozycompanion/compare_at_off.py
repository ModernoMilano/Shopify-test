"""Remove compare-at ("was") prices from the regular range (2026-11-05, owner: "doe wat jij denkt dat best is" after the
advice that sale prices on everything look like dropshipping). Saves every current compare-at price to
compare_at_backup_2026-11-05.json first; `--restore` puts them back. reprice.py no longer sets compare-at (COMPARE_AT = False).
Set prices ("Complete the set") and the BFCM cart tiers are real discounts and are not affected."""
import sys, json, os
from lib import gql, check
BK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "compare_at_backup_2026-11-05.json")
nodes, after = [], None
while True:
    r = gql("""query($a:String){products(first:100,after:$a,query:"-status:archived"){nodes{id title isGiftCard variants(first:100){nodes{id compareAtPrice}}}
               pageInfo{hasNextPage endCursor}}}""", {"a": after})["products"]
    nodes += r["nodes"]
    if not r["pageInfo"]["hasNextPage"]: break
    after = r["pageInfo"]["endCursor"]
if "--restore" in sys.argv:
    bk = json.load(open(BK)); n = 0
    for p in nodes:
        upd = [{"id": v["id"], "compareAtPrice": bk[v["id"]]} for v in p["variants"]["nodes"] if bk.get(v["id"])]
        if upd:
            check(gql("mutation($pid:ID!,$v:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$pid,variants:$v){userErrors{field message}}}", {"pid": p["id"], "v": upd})["productVariantsBulkUpdate"]); n += len(upd)
    print("restored", n); raise SystemExit
if not os.path.exists(BK):
    json.dump({v["id"]: v["compareAtPrice"] for p in nodes for v in p["variants"]["nodes"] if v["compareAtPrice"]}, open(BK, "w"), indent=0)
n = 0
for p in nodes:
    upd = [{"id": v["id"], "compareAtPrice": None} for v in p["variants"]["nodes"] if v["compareAtPrice"]]
    if upd:
        check(gql("mutation($pid:ID!,$v:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$pid,variants:$v){userErrors{field message}}}", {"pid": p["id"], "v": upd})["productVariantsBulkUpdate"], p["title"]); n += len(upd)
print("cleared compare-at on", n, "variants; backup:", BK)
