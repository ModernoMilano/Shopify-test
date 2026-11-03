"""Product page template for the digital gift card (templates/product.giftcard.json): same layout as the default product
page, but no shipping/returns/care rows and no COZY15 line (discount codes never apply to gift cards); trust row and a
'How it works' row that fit a gift card."""
import json
from lib import gql, check, theme_file, put_theme_files
t = theme_file("templates/product.json"); head, j = t[:t.find("{")], json.loads(t[t.find("{"):])
d = j["sections"]["main"]["blocks"]["product-details"]
tr = d["blocks"]["trust"]["blocks"]
tr["t0"]["blocks"]["x"]["settings"]["text"] = "<p>Delivered instantly by email</p>"
tr["t1"]["blocks"]["x"]["settings"]["text"] = "<p>Never expires</p>"
d["blocks"].pop("offer", None)
d["block_order"] = [b for b in d["block_order"] if b != "offer"]
acc = d["blocks"]["info"]
for k in ("ship", "ret", "care"):
    acc["blocks"].pop(k, None)
how = json.loads(json.dumps(acc["blocks"]["help"]))
how["settings"]["heading"] = "How it works"
how["blocks"]["t"]["settings"]["text"] = ("<p>Choose an amount, then send it straight to their email (or to yours to print or forward), "
    "with an optional note and send date. They can spend it on anything at cozycompanion.us, in one or more orders.</p>")
acc["blocks"] = {"how": how, **{k: v for k, v in acc["blocks"].items()}}
acc["block_order"] = ["how"] + [b for b in acc.get("block_order", []) if b not in ("ship", "ret", "care", "how")]
put_theme_files({"templates/product.giftcard.json": head + json.dumps(j, indent=2)})
pid = gql('{products(first:1,query:"gift_card:true"){nodes{id}}}')["products"]["nodes"][0]["id"]
print(check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){product{templateSuffix} userErrors{field message}}}",
                {"p": {"id": pid, "templateSuffix": "giftcard"}})["productUpdate"]))
