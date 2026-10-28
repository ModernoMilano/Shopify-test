"""Batch 10 (Zendrop): food scale scoop, LED collar light, dematting comb, feeding mat, window cat teaser, soft carrier.
Archived: duplicates (second litter mat, second crinkle tunnel, scoop cup), cheap-looking clean-up items, a keychain with
profanity on it, rope toys with a 'Superman' variant (trademark), a 2-in-1 bottle with unclear variants, and two GPS trackers
that advertise GPRS/2G (switched off in the US)."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
from brand_batch4 import d, prod
from brand_batch7 import run

ARCHIVE = {
    "collapsible-silicone-pet-bowl-with-food-scoop-and-measuring-cup": "overlaps the scale scoop",
    "2-in-1-portable-pet-water-and-food-dispenser-with-collapsible-silicone-bowl": "unclear variants (cup only / no bowl / sets)",
    "hands-free-dog-waste-bag-dispenser-with-leash-clip": "cheap-looking",
    "dog-waste-disposal-bags-pack-of-dog-poop-bags": "consumable with foreign-language packaging",
    "new-interactive-cat-tunnel-with-crinkle-paper玩具": "cheap-looking",
    "durable-chew-rope-toy-for-dogs-cotton-knot-design": "'Superman' variant (trademark)",
    "double-layer-cat-litter-mat": "duplicate of Sift",
    "canvas-dog-poop-bag-keychain-with-carabiner-clip": "profanity printed on it",
    "pet-supplies-cat-crinkle-tunnel-foldable-cat-toy": "overlaps Orbit, messy variants",
    "foldable-pet-poop-bag-dispenser-with-travel-spoon": "cheap-looking, messy variants",
    "pet-collar-with-gps-tracker-and-locator": "GPRS/2G tracker, no US network",
    "pet-gps-tracker-for-dogs-anti-loss-tracking-device": "no network/app info; likely 2G",
}
CARRIER = {
    "* 1206 Standard Edition Small size light gray (free summer mat)": "Small · Light Gray",
    "* 1206 Standard Edition Small size dark gray (free summer mat)": "Small · Dark Gray",
    "* 0616 upgraded version Small size light gray (free summer mat)": "Small Plus · Light Gray",
    "* 0616 upgraded version small dark gray (free summer mat)": "Small Plus · Dark Gray",
    "* 0616 upgraded version large light gray (free summer mat)": "Large · Light Gray",
    "* 0616 upgraded version large dark gray (free summer mat)": "Large · Dark Gray",
}
NEW = {
  "smart-high-end-pet-food-measuring-scoop-for-cats-dogs": dict(title="Measure Smart Scale Scoop", handle="measure-smart-scale-scoop", type="Feeding Accessory",
    tags=["feeding", "smart", "dog", "cat"], highlights=["Digital scale in the handle", "Exact portions, every meal", "Easy-clean scoop"],
    seo="Measure smart scale scoop: a pet food scoop with a digital scale in the handle, for exact portions at every meal.",
    html=d("Exact portions, without the guesswork.", ["Digital scale with display in the handle", "Weigh as you scoop: no extra cups", "Detachable bowl for easy cleaning"], "White · kibble or treats"),
    options={}),
  "led-dog-collar-light-for-night-safety-and-visibility": dict(title="Beacon LED Collar Light", handle="beacon-led-collar-light", type="Dog Collar",
    tags=["walk", "dog"], highlights=["Clips onto any collar", "Bright, visible from afar", "Replaceable coin batteries"],
    seo="Beacon LED collar light: a small clip-on light that keeps your dog visible on evening and early-morning walks.",
    html=d("Easy to spot on every evening walk.", ["Clips onto most collars and harnesses", "Steady or flashing light", "Replaceable CR2032 batteries"], "White, green, red or blue"),
    options={}),
  "pet-dog-deshedding-comb-and-dematting-tool-for-large-breeds": dict(title="Tame Dematting Comb", handle="tame-dematting-comb", type="Grooming",
    tags=["grooming", "dog", "cat"], highlights=["Curved stainless blades", "Works through knots and mats", "Non-slip grip"],
    seo="Tame dematting comb: curved stainless steel blades that gently work through knots, mats and loose undercoat.",
    html=d("Knots and mats out, gently.", ["Curved stainless steel blades", "Comb in the direction of the coat, in short strokes", "Comfortable non-slip handle"], "Stainless steel · for medium and long coats"),
    options={}),
  "silicone-pet-food-mat-non-slip-waterproof-oilproof": dict(title="Slate Silicone Feeding Mat", handle="slate-silicone-feeding-mat", type="Feeding Accessory",
    tags=["feeding", "dog", "cat"], highlights=["Raised edge catches spills", "Non-slip, waterproof", "Wipe or rinse clean"],
    seo="Slate silicone feeding mat: a non-slip, waterproof mat with a raised edge that keeps bowls in place and floors clean.",
    html=d("A clean floor under every meal.", ["Raised edge keeps spills on the mat", "Non-slip silicone holds bowls in place", "Wipe clean or rinse under the tap"], "Gray · small or large"),
    options={"Color": ("Color", {"Grey": "Gray"})}),
  "smart-sensor-cat-teaser-toy": dict(title="Wiggle Window Cat Teaser", handle="wiggle-window-cat-teaser", type="Cat Toy",
    tags=["play", "cat", "smart"], highlights=["Sticks to windows and walls", "Light sensor starts and stops it", "USB rechargeable"],
    seo="Wiggle window cat teaser: a suction-mounted, rechargeable feather teaser that wakes up and wiggles when your cat comes near.",
    html=d("Play time, even when you're busy.", ["Suction cup sticks to windows, mirrors and smooth walls", "Light sensor starts and pauses play", "Spare tail included, USB rechargeable"], "15.7 in · white & green"),
    options={"Size": ("Size", {"40 x 8.5 x 9 CM": "15.7 in"})}),
  "large-foldable-pet-carrier-backpack-for-dogs-and-cats": dict(title="Jetset Soft Pet Carrier", handle="jetset-soft-pet-carrier", type="Pet Carrier",
    tags=["travel", "dog", "cat"], highlights=["Mesh windows on all sides", "Shoulder strap and top handles", "Includes a removable mat"],
    seo="Jetset soft pet carrier: a soft-sided carrier with mesh windows, a shoulder strap and a removable mat for cats and small dogs.",
    html=d("Vet visits, weekends away, the train into town.", ["Breathable mesh windows", "Padded shoulder strap and top handles", "Removable mat included", "Folds flat when not in use"], "Light or dark gray · Small, Small Plus or Large"),
    options={"Color": ("Size & Color", CARRIER)}),
}

if __name__ == "__main__":
    for h, why in ARCHIVE.items():
        p = prod(h)
        if p:
            check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": {"id": p["id"], "status": "ARCHIVED"}})["productUpdate"], h)
            print("archived:", h, "-", why)
    for old, c in NEW.items():
        run(old, c)
