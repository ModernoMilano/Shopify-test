"""Batch 15 (Zendrop): nothing new worth adding. Archived: a tactical harness kit (military look), a grey bolster bed
(near-duplicate of Dream), a beige boucle sofa bed (near-duplicate of Billow), a round cat bed with no supplier photos."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
from brand_batch4 import prod

ARCHIVE = {"dog-training-harness-set": "tactical/military look",
           "waterproof-dog-kennel": "near-duplicate of Dream",
           "rectangular-dog-sofa-bed-pet-nest-kennel-beige": "near-duplicate of Billow",
           "solid-color-plush-round-cat-bed-soft-pet-nest-for-cats": "no supplier photos"}
for h, why in ARCHIVE.items():
    p = prod(h)
    if p:
        check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": {"id": p["id"], "status": "ARCHIVED"}})["productUpdate"], h)
        print("archived:", h[:60], "-", why)
