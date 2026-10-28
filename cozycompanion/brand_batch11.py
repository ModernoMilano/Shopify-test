"""Batch 11 (Zendrop): grooming dryer, wooden pet stairs/ramp, memory foam bolster bed.
Archived: a TK911 GPS tracker (2G network, switched off in the US), a checkered carrier (overlaps Jetset/Cradle),
a second set of grey wooden stairs (duplicate of Ascend)."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
from brand_batch4 import d, prod
from brand_batch7 import run

ARCHIVE = {"new-design-wifi-waterproof-mini-gps-tracker-for-pets": "TK911, 2G network",
           "checkered-pet-carrier-backpack-for-dogs-and-cats": "overlaps Jetset / Cradle",
           "wood-pet-stairs-pet-steps-foldable-3-levels-dog-stairs-ramp-perfect-for-beds-and-cars-portable-dog-cat-ladder-up-to-110-pounds": "duplicate of Ascend"}

NEW = {
  "smart-negative-ion-pet-hair-dryer": dict(title="Breeze Pet Grooming Dryer", handle="breeze-pet-grooming-dryer", type="Grooming",
    tags=["grooming", "dog", "cat", "smart"], highlights=["Adjustable airflow and heat", "Negative ions reduce static", "Hose and handheld nozzle"],
    seo="Breeze pet grooming dryer: a hose dryer with adjustable airflow and negative ions to dry your dog's coat faster after baths.",
    html=d("Bath day, without the long damp wait.", ["Adjustable airflow and temperature", "Negative ions help reduce static and frizz", "Flexible hose with handheld nozzle", "Start on low and keep the nozzle moving"], "US plug · white"),
    options={"Color": ("Plug", {"Blower US": "US plug"})}),
  "wooden-foldable-4-storey-pet-stairs-and-ramps": dict(title="Ascend Acacia Pet Stairs & Ramp", handle="ascend-acacia-pet-stairs-ramp", type="Pet Furniture",
    tags=["beds-dens", "travel", "dog", "cat"], highlights=["4 steps that fold into a ramp", "Solid acacia wood", "Holds pets up to 110 lb"],
    seo="Ascend acacia pet stairs & ramp: four carpeted steps that convert into a ramp, for beds, sofas and cars. Holds up to 110 lb.",
    html=d("A gentle way up to the bed, the sofa or the car.", ["4 carpeted steps convert into a ramp", "Solid acacia wood frame", "Non-slip treads for sure footing", "Folds flat to store or travel"], "Acacia wood · up to 110 lb · folded 40.7 × 19.7 × 4 in"),
    options={"Size": ("Finish", {"Acacia wood": "Acacia"})}),
  "large-dog-bed-with-pillows": dict(title="Dream Memory Foam Dog Bed", handle="dream-memory-foam-dog-bed", type="Pet Bed",
    tags=["beds-dens", "dog"], highlights=["7.9 in gel memory foam", "Bolster pillow for their head", "Removable cover, waterproof liner"],
    seo="Dream memory foam dog bed: 7.9 in gel memory foam with a bolster pillow, removable flannel cover and waterproof liner. 46 × 29 in.",
    html=d("Deep, supportive sleep for big dogs.", ["7.9 in thick gel memory foam", "Bolster pillow to rest their head", "Soft flannel cover, removable for washing", "Waterproof inner liner and non-slip base"], "46 × 29 × 7.9 in · blue or brown"),
    options={"Size": ("Color", {"BrownFabric": "Brown Flannel"})}),
}

if __name__ == "__main__":
    for h, why in ARCHIVE.items():
        p = prod(h)
        if p:
            check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": {"id": p["id"], "status": "ARCHIVED"}})["productUpdate"], h)
            print("archived:", h[:60], "-", why)
    for old, c in NEW.items():
        run(old, c)
