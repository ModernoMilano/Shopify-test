"""'The Black Friday Edit' collection (BFCM 2026): the pieces from the approved BFCM ads, posts and gift guides,
banner W3. Manual order; published on the Online Store."""
import os, sys, json
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, S)
from lib import gql, check
HANDLES = ["chaise-velvet-storage-pet-sofa", "chester-tufted-dog-sofa", "nestle-heated-pet-pad", "dine-automatic-feeder",
           "perch-modern-cat-tree", "dream-memory-foam-dog-bed", "haven-pet-den", "frost-harness-winter-dog-jacket",
           "pounce-automatic-feather-cat-toy", "snug-sherpa-pet-blanket", "peak-triangle-cat-scratcher", "burrow-plush-pet-bed",
           "glance-camera-feeder", "cocoon-deep-sleep-bed", "brook-xl-cordless-fountain", "halo-self-cleaning-litter-box"]
reg = json.load(open(os.path.join(S, "files.json")))
ids = []
for h in HANDLES:
    p = gql("query($h:String!){productByHandle(handle:$h){id status}}", {"h": h})["productByHandle"]
    if p and p["status"] == "ACTIVE": ids.append(p["id"])
    else: print("skip", h)
desc = ("<p>Black Friday Week, the cozy way: save 10% on orders $75+, 15% on $150+ and 20% on $250+, applied automatically "
        "at checkout. November 23–30.</p>")
ex = gql('{collectionByHandle(handle:"black-friday-edit"){id}}')["collectionByHandle"]
if ex:
    cid = ex["id"]; print("exists", cid)
else:
    r = gql("""mutation($c:CollectionInput!){collectionCreate(input:$c){collection{id handle} userErrors{field message}}}""",
            {"c": {"title": "The Black Friday Edit", "handle": "black-friday-edit", "descriptionHtml": desc, "sortOrder": "MANUAL",
                   "image": {"src": reg["bfcm_W3"]["url"].split("?")[0], "altText": "A dog on the Chester tufted sofa between wrapped gifts"},
                   "products": ids}})
    cid = check(r["collectionCreate"])["collection"]["id"]; print("created", cid)
pubs = gql("{publications(first:20){nodes{id name}}}")["publications"]["nodes"]
online = [p["id"] for p in pubs if p["name"] == "Online Store"]
print(check(gql("mutation($id:ID!,$p:[PublicationInput!]!){publishablePublish(id:$id,input:$p){userErrors{field message}}}",
                {"id": cid, "p": [{"publicationId": online[0]}]})["publishablePublish"]))
