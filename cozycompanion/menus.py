import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
d = gql("{ collections(first:20){nodes{id handle}} pages(first:30){nodes{id handle}} menus(first:20){nodes{id handle}} }")
col = {c["handle"]: c["id"] for c in d["collections"]["nodes"]}
pg = {p["handle"]: p["id"] for p in d["pages"]["nodes"]}
menus = {m["handle"]: m["id"] for m in d["menus"]["nodes"]}
C = lambda t, h, items=None: {"title": t, "type": "COLLECTION", "resourceId": col[h], "items": items or []}
P = lambda t, h: {"title": t, "type": "PAGE", "resourceId": pg[h], "items": []}
MENUS = {
    "main-menu": ("Main menu", [
        C("Heated Blankets", "cozy-heated-blankets", [
            C("For You", "heated-blankets-for-you"), C("For Your Pet", "heated-blankets-for-pets"),
            C("Weighted Comfort", "weighted-comfort"), C("Shop all blankets", "cozy-heated-blankets")]),
        C("Smart Pet Tech", "smart-pet-tech", [
            C("Smart Feeding", "smart-feeding"), C("Hydration", "hydration"),
            C("GPS & Safety", "gps-safety"), C("Shop all pet tech", "smart-pet-tech")]),
        C("Gifts", "holiday-gift-guide", [
            C("Holiday Gift Guide", "holiday-gift-guide"),
            C("Bundle & Save 10%", "bundle-deals")]),
        P("Our Story", "about"),
        {"title": "Help", "type": "PAGE", "resourceId": pg["faq"], "items": [
            P("FAQ", "faq"), P("Shipping", "shipping"), P("Returns", "returns"), P("Contact us", "contact")]}]),
    "footer": ("Help", [P("FAQ", "faq"), P("Shipping", "shipping"), P("Returns & Refunds", "returns"), P("Contact us", "contact")]),
    "footer-shop": ("Shop", [C("Heated Blankets", "cozy-heated-blankets"), C("Smart Pet Tech", "smart-pet-tech"),
                             C("Holiday Gift Guide", "holiday-gift-guide"), C("Bundle Deals", "bundle-deals"), P("Our Story", "about")]),
    "footer-legal": ("Legal", [P("Privacy Policy", "privacy-policy"), P("Terms of Service", "terms-of-service"),
                               P("Returns & Refunds", "returns"), P("Legal Notice", "legal-notice")]),
}
for handle, (title, items) in MENUS.items():
    if handle in menus:
        r = gql("mutation($id:ID!,$t:String!,$h:String,$i:[MenuItemUpdateInput!]!){menuUpdate(id:$id,title:$t,handle:$h,items:$i){menu{handle} userErrors{field message}}}",
                {"id": menus[handle], "t": title, "h": handle, "i": items})["menuUpdate"]
    else:
        r = gql("mutation($t:String!,$h:String!,$i:[MenuItemCreateInput!]!){menuCreate(title:$t,handle:$h,items:$i){menu{handle} userErrors{field message}}}",
                {"t": title, "h": handle, "i": items})["menuCreate"]
    check(r, handle); print("menu ok:", handle)
