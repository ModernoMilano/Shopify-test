"""Keep fresh imports off the storefront: every non-archived product without `cc-ready` becomes DRAFT
and gets `price-3x`, so it is priced at 3x cost and only goes live once branded and photographed."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
for p in gql('{products(first:100, query:"-status:archived -tag:cc-ready"){nodes{id title status tags}}}')["products"]["nodes"]:
    if "price-3x" not in p["tags"]:
        check(gql("mutation($id:ID!,$t:[String!]!){tagsAdd(id:$id,tags:$t){userErrors{message}}}", {"id": p["id"], "t": ["price-3x"]})["tagsAdd"], p["title"])
    if p["status"] == "ACTIVE":
        check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": {"id": p["id"], "status": "DRAFT"}})["productUpdate"], p["title"])
        print("held:", p["title"])
