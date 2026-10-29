"""Batch 18: a velvet chaise pet sofa with hidden storage.
Archived: five professional grooming tables (groomer equipment with lasso arms, not a home piece; near-duplicates of
each other) and a modern grey dog sofa (same size and role as Chester)."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
from brand_batch4 import d, prod
from brand_batch7 import run

TABLE = "professional grooming table (groomer equipment)"
ARCHIVE = {"large-46-inch-pet-dog-and-cat-grooming-table": TABLE,
           "professional-dog-pet-grooming-table-large-adjustable-heavy-duty-portable-with-armrests-and-lasso-grid-tray": TABLE,
           "large-pet-dog-and-cat-grooming-table-with-adjustable-arms-and-clips-large-heavy-animal-grooming-table-42-inches": TABLE,
           "large-pet-dog-and-cat-grooming-table-with-adjustable-arms-and-clips-large-heavy-duty-animal-grooming-table-42-inches": TABLE,
           "36-inch-professional-dog-pet-grooming-table-adjustable-heavy-duty-portable": TABLE,
           "pet-sofa-with-backrest-and-armrests-modern-rectangular-pet-sofa-suitable-for-medium-and-large-dogs-soft-cushion-comfortable-dog-sofa": "same size and role as Chester"}

NEW = {
  "luxury-small-dog-bed-with-hidden-storage": dict(title="Chaise Velvet Storage Pet Sofa", handle="chaise-velvet-storage-pet-sofa", type="Beds",
    tags=["beds-dens", "dog", "cat"], highlights=["Velvet chaise with a curved arm", "Lift-up seat hides 23 L of storage", "Thick 3 in quilted cushion"],
    seo="Chaise velvet storage pet sofa: a raised velvet chaise for cats and small dogs with a quilted 3 in cushion and hidden storage under the seat.",
    html=d("A little chaise longue, with room for their things underneath.", ["Soft velvet with a curved arm to lean on", "Thick 3 in quilted cushion", "Lift the seat: 23 L of hidden storage for toys and leashes", "Raised on four legs; simple assembly"], "30 × 17.75 × 16.25 in · gray · cats and small dogs up to 22 lb"),
    options={"Color": ("Color", {"Grey": "Gray"})}),
}

if __name__ == "__main__":
    for h, why in ARCHIVE.items():
        p = prod(h)
        if p:
            check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": {"id": p["id"], "status": "ARCHIVED"}})["productUpdate"], h)
            print("archived:", h[:60], "-", why)
    for old, c in NEW.items():
        run(old, c)
