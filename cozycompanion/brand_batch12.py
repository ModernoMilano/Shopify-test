"""Batch 12 (Zendrop): memory foam bolster bed and a modern cat tree.
Archived: electronic pet fence (shock/static collar system), a car sofa (overlaps Roam), FetchPro (duplicate of Fetch),
a cutesy cat-house bed with messy variants, a U-sofa and a large dog dryer with no supplier photos (dryer duplicates Breeze),
a bulky plastic airline crate, and a grooming vacuum kit printed with another brand's name."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
from brand_batch4 import d, prod
from brand_batch7 import run

ARCHIVE = {
    "rechargeable-waterproof-pet-fence-receiver-new-wireless-model": "electronic fence / static collar",
    "removable-washable-warm-pet-sofa": "car sofa, overlaps Roam",
    "fetchpro-automatic-dog-ball-launcher": "duplicate of Fetch",
    "pet-bed": "cutesy cat-house, messy variants",
    "removable-washable-u-shaped-pet-sofa": "no supplier photos",
    "high-power-pet-blow-dryer-for-large-dogs": "no photos; duplicate of Breeze",
    "pet-air-travel-box": "bulky plastic airline crate",
    "5-in-1-pet-grooming-vacuum-kit": "another brand's name printed on the product",
}
NEW = {
  "waterproof-memory-foam-dog-kennel": dict(title="Billow Memory Foam Bolster Bed", handle="billow-memory-foam-bolster-bed", type="Pet Bed",
    tags=["beds-dens", "dog", "cat"], highlights=["Supportive memory foam base", "Soft woven bolster sides", "Removable, washable cover"],
    seo="Billow memory foam bolster bed: a supportive memory foam base with soft woven bolsters and a removable, waterproof-lined cover.",
    html=d("A calm, supportive place to sink into.", ["Memory foam base eases pressure on joints", "Soft woven-yarn bolsters to lean on", "Waterproof layer under a removable cover"], "Milky white · M, L or XL"),
    options={"Color": ("Color", {"Milky White": "Milk White"})}),
  "multi-functional-cat-tree-with-sisal-rope-and-bed": dict(title="Perch Modern Cat Tree", handle="perch-modern-cat-tree", type="Cat Furniture",
    tags=["beds-dens", "play", "cat"], highlights=["Hammocks, hideaway and lookout", "Sisal scratching posts", "Sturdy metal frame"],
    seo="Perch modern cat tree: a sturdy metal-frame cat tree with hammocks, a domed hideaway and sisal scratching posts. 42 in tall.",
    html=d("A modern climbing tree that looks good in your living room.", ["Fabric hammocks and a domed hideaway", "Sisal-wrapped posts for scratching", "Sturdy black metal frame"], "42 × 47 × 31 in · smoke gray or leopard"),
    options={"Color": ("Color", {"Smoke gray": "Smoke Gray", "Leopard print": "Leopard"})}),
}

if __name__ == "__main__":
    for h, why in ARCHIVE.items():
        p = prod(h)
        if p:
            check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": {"id": p["id"], "status": "ARCHIVED"}})["productUpdate"], h)
            print("archived:", h[:60], "-", why)
    for old, c in NEW.items():
        run(old, c)
