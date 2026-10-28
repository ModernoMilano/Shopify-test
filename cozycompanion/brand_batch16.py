"""Batch 16 (Zendrop): nothing new worth adding. Archived: a flat grey memory foam mat with German-language supplier
photos and conflicting sizes (near-duplicate of Dream), and a grey sofa bed (near-duplicate of Billow; its beige twin
was archived in batch 15)."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
from brand_batch4 import prod

ARCHIVE = {"dog-mat-for-pets-comfortable-and-cozy-design": "near-duplicate of Dream",
           "sofa-dog-bed": "near-duplicate of Billow"}
for h, why in ARCHIVE.items():
    p = prod(h)
    if p:
        check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": {"id": p["id"], "status": "ARCHIVED"}})["productUpdate"], h)
        print("archived:", h[:60], "-", why)
