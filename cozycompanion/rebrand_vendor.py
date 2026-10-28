"""Show CozyCompanion as the brand everywhere: vendor -> CozyCompanion (supplier kept as a tag
supplier-<name> for reprice.py), old supplier names out of photo alt texts, tidy titles."""
import sys, os, re
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check

TITLES = {"haven-pet-den": "Haven Pet Den"}
ALT_FIX = [("Plush Heat Pad", "Ember Heat Pad"), ("Heklet heated sherpa throw", "Hearth Heated Sherpa Throw"),
           ("MiTag Duo", "Compass Smart Tag"), ("heated pet pad", "Nestle Heated Pet Pad"),
           ("stainless steel pet fountain", "Brook Stainless Pet Fountain"), ("4L automatic pet feeder", "Dine 4L Automatic Feeder")]

ps = gql('{products(first:100, query:"-status:archived"){nodes{id handle title vendor media(first:50){nodes{id alt}}}}}')["products"]["nodes"]
for p in ps:
    upd = {"id": p["id"]}
    if p["vendor"] != "CozyCompanion":
        check(gql("mutation($id:ID!,$t:[String!]!){tagsAdd(id:$id,tags:$t){userErrors{message}}}",
                  {"id": p["id"], "t": ["supplier-" + re.sub(r"\W+", "-", p["vendor"].lower())]})["tagsAdd"], "tag")
        upd["vendor"] = "CozyCompanion"
    if p["handle"] in TITLES:
        upd["title"] = TITLES[p["handle"]]; upd["seo"] = {"title": f"{TITLES[p['handle']]} | CozyCompanion"}
    if len(upd) > 1:
        check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){product{id} userErrors{field message}}}", {"p": upd})["productUpdate"], p["title"])
    media = []
    for m in p["media"]["nodes"]:
        alt = m["alt"] or ""
        new = alt
        for a, b in ALT_FIX: new = new.replace(a, b)
        new = new.replace("CozyCompanion Ember", "Ember").replace("CozyCompanion Hearth", "Hearth").replace("CozyCompanion Nestle", "Nestle").replace("CozyCompanion Brook", "Brook").replace("CozyCompanion Dine", "Dine")
        if new != alt: media.append({"id": m["id"], "alt": new})
    if media:
        check(gql("mutation($pid:ID!,$m:[UpdateMediaInput!]!){productUpdateMedia(productId:$pid,media:$m){mediaUserErrors{field message}}}",
                  {"pid": p["id"], "m": media})["productUpdateMedia"] | {"userErrors": []}, "alt")
    print(f"{p['title'][:40]:40} vendor {p['vendor']} -> CozyCompanion, {len(media)} alt fixed")
