"""Sort size option values small -> large on every active product (owner: Burrow showed S after XL)."""
import sys, re
from lib import gql, check
RANK = ["XXS", "XS", "S", "M", "L", "XL", "2XL", "XXL", "3XL", "XXXL", "4XL", "5XL"]
def key(v):
    t = v.upper().strip()
    m = re.match(r"^(XXS|XS|S|M|L|XL|2XL|XXL|3XL|XXXL|4XL|5XL)\b", t)
    if m: return (0, RANK.index(m.group(1)), tuple(float(x) for x in re.findall(r"\d+(?:\.\d+)?", t[len(m.group(1)):])))
    n = re.findall(r"\d+(?:\.\d+)?", t)
    if n: return (1, 0, tuple(float(x) for x in n))
    return None
DRY = "--dry-run" in sys.argv
after, fixed = None, 0
while True:
    r = gql("""query($a:String){products(first:100,after:$a,query:"status:active"){nodes{id title options{name optionValues{name}}}
               pageInfo{hasNextPage endCursor}}}""", {"a": after})["products"]
    for p in r["nodes"]:
        opts = [{"name": o["name"], "values": [v["name"] for v in o["optionValues"]]} for o in p["options"]]
        changed = False
        for o in opts:
            if not re.search(r"size|maat", o["name"], re.I): continue
            ks = [key(v) for v in o["values"]]
            if None in ks: continue
            want = [v for _, v in sorted(zip(ks, o["values"]), key=lambda x: x[0])]
            if want != o["values"]:
                print(f"{p['title'][:40]:40} {o['name']}: {o['values']} -> {want}"); o["values"] = want; changed = True
        if changed and not DRY:
            check(gql("""mutation($id:ID!,$o:[OptionReorderInput!]!){productOptionsReorder(productId:$id,options:$o){userErrors{field message}}}""",
                      {"id": p["id"], "o": [{"name": o["name"], "values": [{"name": v} for v in o["values"]]} for o in opts]})["productOptionsReorder"], p["title"])
            fixed += 1
    if not r["pageInfo"]["hasNextPage"]: break
    after = r["pageInfo"]["endCursor"]
print(("would fix" if DRY else "fixed"), fixed, "products")
