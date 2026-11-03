"""CozyCompanion digital gift card (owner approved 2026-11-03, for the December last-minute phase).
Shopify gift card product: delivered by email, no shipping. Face values $25 / $50 / $75 / $100 / $150 (USD; Shopify converts
for other markets). Never repriced and never given a compare-at price (reprice.py skips gift cards).
Image: the approved December gift-card visual (calendar_dec 12-17). Published on the Online Store."""
import json, os
from lib import gql, check, S

AMOUNTS = [25, 50, 75, 100, 150]
TITLE = "CozyCompanion Digital Gift Card"
HANDLE = "digital-gift-card"
DESC = ("<p>The easiest gift for every pet person: a CozyCompanion digital gift card, sent by email with your note. "
        "No shipping, no waiting, and they choose what their dog or cat will love.</p>"
        "<ul><li>Delivered instantly by email after checkout</li><li>Never expires</li>"
        "<li>Use it on anything in the store, in one or more orders</li></ul>")

ex = gql("query($h:String!){productByHandle(handle:$h){id}}", {"h": HANDLE})["productByHandle"]
if not ex:   # created by hand in the admin ("Add gift card product"): adopt it
    found = gql('{products(first:5,query:"gift_card:true"){nodes{id title}}}')["products"]["nodes"]
    ex = found[0] if found else None
if ex:
    pid = ex["id"]; print("exists", pid)
    check(gql("""mutation($p:ProductUpdateInput!){productUpdate(product:$p){product{id handle} userErrors{field message}}}""",
              {"p": {"id": pid, "title": TITLE, "handle": HANDLE, "descriptionHtml": DESC, "vendor": "CozyCompanion",
                     "productType": "Gift Card", "tags": ["gift-card", "holiday-gift-guide"], "status": "ACTIVE"}})["productUpdate"])
    vs = gql("query($id:ID!){product(id:$id){variants(first:20){nodes{title price}}}}", {"id": pid})["product"]["variants"]["nodes"]
    print("variants:", [(v["title"], v["price"]) for v in vs])
else:
    r = gql("""mutation($p:ProductCreateInput!){productCreate(product:$p){product{id variants(first:5){nodes{id}}} userErrors{field message}}}""",
            {"p": {"title": TITLE, "handle": HANDLE, "descriptionHtml": DESC, "giftCard": True, "vendor": "CozyCompanion",
                   "productType": "Gift Card", "tags": ["gift-card", "holiday-gift-guide"], "status": "ACTIVE",
                   "productOptions": [{"name": "Amount", "values": [{"name": f"${a}"} for a in AMOUNTS]}]}})
    prod = check(r["productCreate"])["product"]; pid = prod["id"]; print("created", pid)
    r = gql("""mutation($pid:ID!,$v:[ProductVariantsBulkInput!]!){productVariantsBulkCreate(productId:$pid,variants:$v,strategy:REMOVE_STANDALONE_VARIANT){
               productVariants{id title price} userErrors{field message}}}""",
            {"pid": pid, "v": [{"price": f"{a:.2f}", "optionValues": [{"optionName": "Amount", "name": f"${a}"}],
                                "inventoryPolicy": "CONTINUE"} for a in AMOUNTS]})
    print([(v["title"], v["price"]) for v in check(r["productVariantsBulkCreate"])["productVariants"]])

cal = {d["date"]: d for d in json.load(open(os.path.join(S, "social", "calendar_dec.json")))}
imgs = [u.split("?")[0] for u in (cal["2026-12-17"]["assets"]["feed"] + cal["2026-12-23"]["assets"]["feed"])]
have = gql("query($id:ID!){product(id:$id){media(first:5){nodes{id}}}}", {"id": pid})["product"]["media"]["nodes"]
if not have:
    r = gql("""mutation($id:ID!,$m:[CreateMediaInput!]!){productCreateMedia(productId:$id,media:$m){media{id} mediaUserErrors{field message}}}""",
            {"id": pid, "m": [{"originalSource": u, "mediaContentType": "IMAGE", "alt": "CozyCompanion digital gift card"} for u in imgs]})
    print("media", r["productCreateMedia"]["mediaUserErrors"] or "ok")
pubs = gql("{publications(first:20){nodes{id name}}}")["publications"]["nodes"]
online = [p["id"] for p in pubs if p["name"] == "Online Store"]
print(check(gql("mutation($id:ID!,$p:[PublicationInput!]!){publishablePublish(id:$id,input:$p){userErrors{field message}}}",
                {"id": pid, "p": [{"publicationId": online[0]}]})["publishablePublish"]))
gg = gql('{collectionByHandle(handle:"holiday-gift-guide"){id ruleSet{appliedDisjunctively}}}')["collectionByHandle"]
if gg and not gg["ruleSet"]:
    print("gift guide:", gql("mutation($id:ID!,$p:[ID!]!){collectionAddProducts(id:$id,productIds:$p){userErrors{message}}}",
                             {"id": gg["id"], "p": [pid]})["collectionAddProducts"]["userErrors"] or "added")
