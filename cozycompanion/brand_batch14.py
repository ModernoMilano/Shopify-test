"""Batch 14 (Zendrop): litter deodorizer, triangle cat scratchers, sherpa car booster seat.
Archived: a frilly pink tent with printed text, a tactical 'military' vest kit, a cat tunnel bed (overlaps Orbit),
and a back-seat car mat (overlaps Roam)."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
from brand_batch4 import d, prod
from brand_batch7 import run

ARCHIVE = {"removable-pet-tent-for-dogs-ideal-for-teddy-bears": "frilly tent with printed text",
           "dog-training-vest": "tactical/military look",
           "pet-supplies-cat-bed-cat-tent-cat-house": "overlaps Orbit",
           "anti-dirty-car-pet-mat": "overlaps Roam"}

NEW = {
  "smart-cat-litter-deodorizer": dict(title="Fresh Smart Litter Deodorizer", handle="fresh-smart-litter-deodorizer", type="Litter Accessory",
    tags=["litter-hygiene", "cat", "smart"], highlights=["Neutralizes litter box odors", "Runs automatically when needed", "USB rechargeable"],
    seo="Fresh smart litter deodorizer: a small rechargeable unit that neutralizes litter box odors automatically, with no sprays or scents.",
    html=d("A fresher litter corner, without sprays or perfume.", ["Mounts on or near the litter box", "Works automatically, no refills", "USB rechargeable battery"], "4000 or 5200 mAh · white"),
    options={"Color": ("Power", {"USB": "USB rechargeable"}), "Size": ("Battery", {"4000MAH": "4000 mAh", "5200MAH": "5200 mAh"})}),
  "cat-scratching-board-with-corrugated-paper-design": dict(title="Peak Triangle Cat Scratcher", handle="peak-triangle-cat-scratcher", type="Cat Furniture",
    tags=["play", "cat"], highlights=["Sculptural triangle shape", "Dense corrugated cardboard", "Scratch, climb and lounge"],
    seo="Peak triangle cat scratcher: a sculptural corrugated cardboard scratcher cats can scratch, climb and lounge on.",
    html=d("A scratcher that looks like a design object.", ["Triangular shape to scratch, climb and lounge", "Dense corrugated cardboard", "Saves your sofa and rugs"], "9.6 × 13.8 × 24.4 in · black"),
    options={"Color": ("Color", {"1": "Black"})}),
  "car-pet-basket-with-dog-cushion-and-pet-bed": dict(title="Ride Sherpa Car Booster Seat", handle="ride-sherpa-car-booster-seat", type="Pet Carrier",
    tags=["travel", "dog", "cat"], highlights=["Soft sherpa lining", "Raised so small pets can see out", "Seat strap and safety clip"],
    seo="Ride sherpa car booster seat: a raised, sherpa-lined car seat that keeps small dogs and cats cozy and secure on the road.",
    html=d("Small pet, big view, calm car rides.", ["Raised sides so small pets can look out", "Soft, removable sherpa cushion", "Straps to the car seat, with a harness clip", "Always use the safety clip with a harness"], "17.3 × 10.6 × 9 in · black or houndstooth"),
    options={"Color": ("Color", {"black": "Black", "Lattice": "Houndstooth"})}),
}

if __name__ == "__main__":
    for h, why in ARCHIVE.items():
        p = prod(h)
        if p:
            check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": {"id": p["id"], "status": "ARCHIVED"}})["productUpdate"], h)
            print("archived:", h[:60], "-", why)
    for old, c in NEW.items():
        run(old, c)
