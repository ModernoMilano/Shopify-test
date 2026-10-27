# usage: upload.py <name> <url> [alt]  ... reads lines "name url|alt" from stdin
import sys, json, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import gql, check, S
reg_path = os.path.join(S, "files.json")
reg = json.load(open(reg_path)) if os.path.exists(reg_path) else {}
items = []
for line in sys.stdin:
    if not line.strip(): continue
    name, rest = line.strip().split(" ", 1)
    url, alt = rest.split("|", 1)
    if name in reg: continue
    items.append((name, url, alt))
if items:
    r = check(gql("""mutation($f:[FileCreateInput!]!){ fileCreate(files:$f){ files{ id } userErrors{field message} } }""",
          {"f": [{"originalSource": u, "alt": a, "contentType": "IMAGE", "filename": f"cozycompanion-{n}.png"} for n, u, a in items]})["fileCreate"])
    for (n, u, a), f in zip(items, r["files"]):
        reg[n] = {"id": f["id"], "alt": a}
# resolve CDN urls
for _ in range(30):
    pending = [n for n, v in reg.items() if not v.get("url")]
    if not pending: break
    d = gql("query($ids:[ID!]!){ nodes(ids:$ids){ ... on MediaImage{ id fileStatus image{url width height} } } }", {"ids": [reg[n]["id"] for n in pending]})
    for n, node in zip(pending, d["nodes"]):
        if node["fileStatus"] == "READY":
            reg[n]["url"] = node["image"]["url"]; reg[n]["size"] = [node["image"]["width"], node["image"]["height"]]
        elif node["fileStatus"] == "FAILED":
            print("FAILED", n); reg[n]["url"] = "FAILED"
    time.sleep(3)
json.dump(reg, open(reg_path, "w"), indent=1)
for n, v in reg.items(): print(n, v.get("size"), v.get("url", "pending")[:90])
