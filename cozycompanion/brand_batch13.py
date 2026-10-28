"""Batch 13 (Zendrop): grooming vacuum kit, deep-sleep donut bed, cordless clipper kit.
Archived: denim harness (another brand's woven label on it), a washable kennel bed (overlaps Burrow),
an RC cat car with no supplier photos, and a pink cat sofa (overlaps Lounge)."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
from brand_batch4 import d, prod
from brand_batch7 import run

ARCHIVE = {"luxury-lightweight-dog-harness-and-leash-set": "another brand's label on the harness",
           "removable-washable-dog-kennel": "overlaps Burrow",
           "smart-cat-toy": "no supplier photos",
           "four-season-soft-cat-nest-warm-washable-pet-bed": "overlaps Lounge"}

NEW = {
  "pet-grooming-kit": dict(title="Sweep Grooming Vacuum Kit", handle="sweep-grooming-vacuum-kit", type="Grooming",
    tags=["grooming", "dog", "cat", "smart"], highlights=["Clips and vacuums in one go", "5 grooming attachments", "Hair goes straight into the bin"],
    seo="Sweep grooming vacuum kit: clipper, brushes and comb guides that vacuum loose hair as you groom, so it never lands on the floor.",
    html=d("Groom at home without hair all over the floor.", ["Clipper and brushes connect to a quiet vacuum", "Loose hair goes straight into the dust bin", "4 comb guides for different coat lengths", "Introduce it slowly, on the lowest setting"], "5-piece set · US plug"),
    options={"Color": ("Set", {"5piece set": "5-piece set"}), "Size": ("Plug", {"US": "US plug", "UK": "UK plug"})}),
  "thick-dog-bed": dict(title="Cocoon Deep Sleep Bed", handle="cocoon-deep-sleep-bed", type="Pet Bed",
    tags=["beds-dens", "dog", "cat"], highlights=["Thick, raised round bolster", "Removable, washable cover", "Soft velvet or flannel finish"],
    seo="Cocoon deep sleep bed: a thick round bed with a raised bolster and a removable, washable cover for dogs and cats.",
    html=d("A deep, round nest they can curl up in.", ["Thick raised bolster all around", "Soft velvet or flannel finish", "Cover removes for washing"], "M or L · 4 finishes"),
    options={"Color": ("Finish", {"Deep Sleep Nest": "Classic Nest", "Deep Sleep Dark Grey Velvet": "Dark Gray Velvet",
                                  "Deep Sleep Beige Velvet": "Beige Velvet", "Deep Sleep Flannel Blanket": "Flannel"})}),
  "4x-professional-cordless-pet-clippers-grooming-trimmer-ki": dict(title="Trim Cordless Clipper Kit", handle="trim-cordless-clipper-kit", type="Grooming",
    tags=["grooming", "dog", "cat"], highlights=["4-in-1 heads: body, paws, face, nails", "Cordless and rechargeable", "Comb guides included"],
    seo="Trim cordless clipper kit: a quiet 4-in-1 rechargeable pet trimmer with heads for body, paws, face and nails.",
    html=d("Tidy paws, faces and coats between groomer visits.", ["4 interchangeable heads", "Cordless, USB rechargeable", "Comb guides for an even length", "Quiet motor for nervous pets"], "Mint green"),
    options={}),
}

def us_only():
    p = gql('{productByHandle(handle:"pet-grooming-kit"){id variants(first:10){nodes{id title}}}}')["productByHandle"]
    if p:
        drop = [v["id"] for v in p["variants"]["nodes"] if "UK" in v["title"]]
        if drop:
            check(gql("mutation($p:ID!,$v:[ID!]!){productVariantsBulkDelete(productId:$p,variantsIds:$v){userErrors{field message}}}", {"p": p["id"], "v": drop})["productVariantsBulkDelete"], "sweep")

if __name__ == "__main__":
    for h, why in ARCHIVE.items():
        p = prod(h)
        if p:
            check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": {"id": p["id"], "status": "ARCHIVED"}})["productUpdate"], h)
            print("archived:", h[:60], "-", why)
    us_only()
    for old, c in NEW.items():
        run(old, c)
