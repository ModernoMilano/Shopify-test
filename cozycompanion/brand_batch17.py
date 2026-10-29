"""Batch 17: a pantry-style feeding station cabinet and a tufted Chesterfield dog sofa.
Archived: the grey feeding station (same cabinet in another colour; one listing keeps the shop tidy)."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
from brand_batch4 import d, prod
from brand_batch7 import run

ARCHIVE = {"pet-feeder-stations-lockers-dog-food-storage-containers": "same cabinet as Pantry, in grey"}

NEW = {
  "pet-feeder-station-lockers": dict(title="Pantry Pet Feeding Station", handle="pantry-pet-feeding-station", type="Feeding Stations",
    tags=["feeding", "dog"], highlights=["Raised stainless bowls in a pull-out drawer", "Tilt-out bin hides the food", "Shelf and hooks for leashes and treats"],
    seo="Pantry pet feeding station: a white cabinet with raised stainless steel bowls in a pull-out drawer, a tilt-out food bin, shelf and hooks.",
    html=d("A tidy feeding corner that looks like furniture.", ["Raised stainless steel bowls slide out at mealtime, then tuck away", "Tilt-out cabinet hides kibble and treats", "Open shelf, countertop and 3 hooks for leashes and harnesses", "Doubles as a side table; assembly required"], "24 × 14 × 32.25 in · white · countertop holds 44 lb"),
    options={}),
  "elegant-rectangular-pet-bed-for-medium-and-large-dogs": dict(title="Chester Tufted Dog Sofa", handle="chester-tufted-dog-sofa", type="Beds",
    tags=["beds-dens", "dog"], highlights=["Tufted Chesterfield-style sofa", "Raised off the floor, thick padding", "Removable, washable cover"],
    seo="Chester tufted dog sofa: a raised Chesterfield-style sofa bed with thick padding and a removable, washable cover for medium and large dogs.",
    html=d("Their own sofa, so yours stays theirs a little less.", ["Tufted Chesterfield-style back and rolled arms", "Raised base with thick, supportive padding", "Cover removes for machine washing", "Sized for medium and large dogs"], "40 × 23 × 14 in · beige · holds up to 250 lb"),
    options={}),
}

if __name__ == "__main__":
    for h, why in ARCHIVE.items():
        p = prod(h)
        if p:
            check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": {"id": p["id"], "status": "ARCHIVED"}})["productUpdate"], h)
            print("archived:", h[:60], "-", why)
    for old, c in NEW.items():
        run(old, c)
