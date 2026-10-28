"""Batch 8 (Zendrop): carrier, collars, leash, hood, bow tie, life jacket, two cat toys. Same flow as brand_batch7.
Archived (not a fit for a high-end pet store): duplicates, a children's panda toy, a cartoon-character plush
(copyrighted character), a novelty propeller cap and a $0.29 vinyl squeaker."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
from brand_batch4 import d, prod
from brand_batch7 import run

ARCHIVE = {"pet-backpack": "same sling as Cradle", "dog-life-jacket-pet-swimwear-for-safety": "second life jacket (keep Fin)",
           "plush-toy-set-silly-cat-vs-fat-cat-characters": "cartoon character plush for children",
           "pet-propeller-hat": "novelty cap", "cute-panda-plush-toy-with-music-and-lights": "children's toy",
           "dog-toy-interactive-squeaky-dumbbell-for-puppies": "$0.29 vinyl squeaker"}

NEW = {
  "electric-cat-toy": dict(title="Pounce Automatic Feather Cat Toy", handle="pounce-automatic-feather-cat-toy", type="Cat Toy",
    tags=["play", "cat", "smart"], highlights=["Feather pops out at random", "Keeps indoor cats moving", "Black or violet"],
    seo="Pounce automatic feather cat toy: a feather darts in and out of its holes at random to wake up your cat's hunting instinct.",
    html=d("A feather that never plays the same way twice.", ["Feather pops in and out of the holes at random", "Gets indoor cats moving and pouncing", "Sturdy base that stays put"], "Black or violet"),
    options={"Color": ("Color", {})}),
  "interactive-plush-electric-catnip-ball-toy-for-kittens": dict(title="Chirp Catnip Ball", handle="chirp-catnip-ball", type="Cat Toy",
    tags=["play", "cat"], highlights=["Refillable with catnip", "Plush or smooth foam", "2 in, easy to bat"],
    seo="Chirp catnip ball: a small 2 in ball with a refillable catnip chamber, in soft plush or smooth foam.",
    html=d("A little ball that cats can't leave alone.", ["Open the lid and add catnip", "Small and light to bat and chase", "Soft plush or smooth foam finish"], "2 in · pink, blue or yellow"),
    options={"Color": ("Style", {"Plush material PINK": "Plush Pink", "Plush material Blue": "Plush Blue", "Plush material Yellow": "Plush Yellow",
                                 "EVA Blue": "Smooth Blue", "EVA Yellow": "Smooth Yellow", "EVA Pink": "Smooth Pink"})}),
  "mesh-pet-sling-carrier-bag": dict(title="Cradle Pet Sling Carrier", handle="cradle-pet-sling-carrier", type="Pet Carrier",
    tags=["travel", "dog", "cat"], highlights=["Hands-free, worn across the body", "Breathable mesh", "Up to 6.6 lb (S) or 13 lb (L)"],
    seo="Cradle pet sling carrier: a breathable mesh sling for small dogs and cats, worn across the body for hands-free outings.",
    html=d("Keep them close on busy streets and quick errands.", ["Worn across the body, hands-free", "Breathable mesh with drawstring opening", "Padded shoulder strap"], "S up to 6.6 lb · L up to 13 lb · 7 colors"),
    options={"Size": ("Size", {"Small": "S", "Large": "L"})}),
  "adjustable-cat-collar-with-bell-ucc-055": dict(title="Bloom Floral Cat Collar", handle="bloom-floral-cat-collar", type="Cat Collar",
    tags=["walk", "cat"], highlights=["Bohemian floral print", "Metal buckle and little bell", "Sizes XS to XL"],
    seo="Bloom floral cat collar: a soft polyester collar with a bohemian floral print, metal buckle and bell.",
    html=d("A little color for the most stylish cat in the house.", ["Soft polyester with a floral print", "Adjustable metal buckle", "Small bell included"], "Red floral · sizes XS–XL"),
    options={}),
  "woolen-pet-hat-for-autumn-winter": dict(title="Mistle Knit Dog Hood", handle="mistle-knit-dog-hood", type="Dog Apparel",
    tags=["wear", "dog"], highlights=["Soft ribbed knit", "Covers head and ears", "Sizes S to XL"],
    seo="Mistle knit dog hood: a soft ribbed-knit hood with pompom that keeps ears warm on chilly walks.",
    html=d("Warm ears on winter walks (and very cute holiday photos).", ["Soft, stretchy ribbed knit", "Covers head, ears and neck", "Pompom on top"], "Red · sizes S–XL"),
    options={}),
  "hands-free-reflective-dog-leash": dict(title="Trail Hands-Free Dog Leash", handle="trail-hands-free-dog-leash", type="Dog Leash",
    tags=["walk", "dog"], highlights=["Waist belt with zip pouch", "Stretchy bungee leash", "Reflective stitching"],
    seo="Trail hands-free dog leash: a waist belt with zip pouch and a reflective bungee leash for runs and long walks.",
    html=d("Run, hike or walk with both hands free.", ["Adjustable waist belt with zip pouch", "Bungee section absorbs sudden pulls", "Reflective details for low light"], "Nylon · 6 colors"),
    options={"Color": ("Color", {"Lake Water Green Color Suit": "Lake Green", "Fluorescent Green Suit": "Neon Green", "Purple Suit": "Purple",
                                 "Rose Red Suit": "Rose", "Red Suit": "Red", "Dream Blue Suit": "Blue"})}),
  "pet-accessories-bow-tie-dog-collar-decoration": dict(title="Dapper Gingham Bow Tie", handle="dapper-gingham-bow-tie", type="Dog Accessory",
    tags=["wear", "dog"], highlights=["Slides onto any collar", "Blue gingham cotton look", "Sizes XS to XL"],
    seo="Dapper gingham bow tie for dogs: a blue gingham bow that slides onto your dog's collar for photos, parties and every day.",
    html=d("The finishing touch for every good boy and girl.", ["Slides onto most collars", "Blue gingham bow", "Sizes for small to large dogs"], "Polyester · sizes XS–XL"),
    options={}),
  "dog-life-jacket-for-pet-swimming": dict(title="Fin Dog Life Jacket", handle="fin-dog-life-jacket", type="Dog Apparel",
    tags=["wear", "travel", "dog"], highlights=["Buoyant vest with grab handle", "Adjustable buckle straps", "Shark fin or mermaid style"],
    seo="Fin dog life jacket: a buoyant swim vest with grab handle and adjustable straps, in a shark-fin or mermaid design.",
    html=d("Beach days, boat days, pool days.", ["Buoyant panels around chest and belly", "Top grab handle to lift them out", "Adjustable quick-release buckles", "Always supervise your dog in and around water"], "Gray shark or pink mermaid · S–L"),
    options={"Color": ("Style", {"Dark brow": "Shark Gray", "Pink": "Mermaid Pink"})}),
}

if __name__ == "__main__":
    for h, why in ARCHIVE.items():
        p = prod(h)
        if p:
            check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": {"id": p["id"], "status": "ARCHIVED"}})["productUpdate"], h)
            print("archived:", h, "-", why)
    for old, c in NEW.items():
        run(old, c)
