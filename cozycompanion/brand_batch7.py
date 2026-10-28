"""Batch 7 (Zendrop): toys, bowls, apparel, beds. Same flow as brand_batch6.
Also: Dart Speedy Tail Cat Ball is the same item as Zoom (same cost, colors) -> archived;
Fetch launcher keeps only the US-plug machine and a mini-ball refill."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
from brand_batch4 import d, COLS, prod

C3 = ["smart-pet-tech", "holiday-gift-guide", "bundle-deals"]
GRAY = {"Grey": "Gray"}
NEW = {
  "cove-ceramic-pet-bowl": dict(title="Cove Ceramic Cat Bowl", handle="cove-ceramic-cat-bowl", type="Pet Bowl",
    tags=["feeding"], highlights=["Glazed ceramic, easy to clean", "Cute cat-face design", "For food or water"],
    seo="Cove ceramic cat bowl: a glazed ceramic pet bowl with a cute cat face and ear-shaped rim, for food or water.",
    html=d("A little ceramic bowl that makes every meal cuter.", ["Glazed ceramic, easy to wipe clean", "Ear-shaped rim for easy lifting", "Use it for food or water"], "Ceramic · gray cat face"),
    options={"Color": ("Color", GRAY)}),
  "chase-mouse-bird-cat-toy": dict(title="Chase Plush Prey Cat Toy", handle="chase-plush-prey-cat-toy", type="Cat Toy",
    tags=["play"], highlights=["9 plush prey characters", "Made to spark the hunt", "Soft and light to bat around"],
    seo="Chase plush prey cat toy: soft bird, mouse, bee, ladybug and hedgehog toys made to bring out your cat's hunting instinct.",
    html=d("Little plush prey for big hunting instincts.", ["Designed to mimic the sounds and moves of prey", "Soft, lightweight and easy to bat", "Pick from 9 characters"], "Plush · bird, mouse, bee, ladybug, hedgehog and more"),
    options={"Color": ("Style", {"Long billed bird": "Long-Billed Bird", "Beetle": "Ladybug", "Blue parrot": "Blue Parrot",
                                 "Little bird": "Little Bird", "Red parrot": "Red Parrot"})}),
  "fetch-automatic-ball-launcher": dict(title="Fetch Automatic Ball Launcher", handle="fetch-automatic-ball-launcher", type="Dog Toy",
    tags=["play"], highlights=["3 distances: 10, 20 or 30 ft", "Uses 2 in mini tennis balls", "3 balls and US adapter included"],
    seo="Fetch automatic dog ball launcher: launches 2 in mini tennis balls 10, 20 or 30 ft. Includes 3 balls and a US adapter.",
    html=d("Endless fetch, even when your arm needs a break.", ["Launches mini balls 10, 20 or 30 ft", "Set the distance with one button on the back", "Includes 3 mini tennis balls, US adapter and manual", "Best for small and medium dogs"], "Launcher for 2 in balls · US plug"),
    options={"Color": ("Choose", {"US": "Launcher (US plug)", "Diameter 5cm 6pcs": "Refill: 6 mini balls"})}),
  "glide-soft-dog-frisbee": dict(title="Glide Soft Dog Frisbee", handle="glide-soft-dog-frisbee", type="Dog Toy",
    tags=["play"], highlights=["Soft, flexible rubber", "7.5 in, only 4.3 oz", "Floppy, easy to catch"],
    seo="Glide soft dog frisbee: a flexible 7.5 in rubber flying disc that's light, easy to catch and gentle to carry.",
    html=d("A flying disc that's soft enough to catch and carry all afternoon.", ["Flexible TPR rubber", "Light and easy to throw", "Great for fetch and training"], "7.5 in · 4.3 oz · purple"),
    options={"Size": ("Size", {"Large": "7.5 in"})}),
  "gnaw-dental-chew-toy": dict(title="Gnaw Dental Chew Toy", handle="gnaw-dental-chew-toy", type="Dog Toy",
    tags=["play"], highlights=["Ridged texture to chew on", "7.4 in, for small dogs", "Tough and easy to rinse"],
    seo="Gnaw dental chew toy: a ridged 7.4 in chew toy for small dogs and teething puppies.",
    html=d("Something satisfying to chew on (that isn't your shoes).", ["Ridged, textured surface", "Sized for small dogs and puppies", "Rinse clean after play"], "7.4 in · orange"),
    options={"Size": ("Size", {"200*70*70(1mm)": "7.4 in"})}),
  "puddle-waterproof-dog-boots": dict(title="Puddle Suspender Dog Boots", handle="puddle-suspender-dog-boots", type="Dog Apparel",
    tags=["travel"], highlights=["Suspender straps keep them on", "Water-repellent, wipe clean", "Adjustable, sizes S to 2XL"],
    seo="Puddle suspender dog boots: water-repellent boot leggings with adjustable straps that keep them on through mud and rain.",
    html=d("Muddy walks, clean paws: boots that actually stay on.", ["Suspender straps over the back hold all four boots up", "Water-repellent, wipe-clean fabric", "Adjustable buckles for a snug fit"], "Black · sizes S–2XL"),
    options={"Color": ("Size", {"Black-S": "S", "Black-M": "M", "Black-L": "L", "Black-XL": "XL", "Black-XXL": "2XL"})}),
  "frost-quilted-dog-jacket": dict(title="Frost Harness Winter Dog Jacket", handle="frost-harness-winter-dog-jacket", type="Dog Apparel",
    tags=["travel"], highlights=["Built-in harness with leash ring", "Padded, fleece-lined collar", "Reflective straps, S to 4XL"],
    seo="Frost winter dog jacket: a padded, water-repellent coat with a built-in harness, fleece collar and reflective straps.",
    html=d("Warm coat and harness in one, so winter walks are quick to start.", ["Padded body with a fleece-lined collar", "Built-in harness with leash ring", "Reflective straps for darker evenings", "Zip closure"], "6 colors · sizes S–4XL"),
    options={"Color": ("Color", {"Blue": "Navy", "Purple": "Wine", "Silver Grey": "Silver Gray"})}),
  "splash-quick-dry-pet-bathrobe": dict(title="Splash Quick-Dry Dog Bathrobe", handle="splash-quick-dry-dog-bathrobe", type="Dog Apparel",
    tags=["travel"], highlights=["Absorbent microfiber", "Hook-and-loop closure", "Sizes XS to 3XL"],
    seo="Splash quick-dry dog bathrobe: an absorbent microfiber robe for after baths, rain and swims, with an adjustable fit.",
    html=d("Bath, rain or swim: wrap them up and skip the wet-dog shake.", ["Ultra-absorbent microfiber", "Adjustable neck and belly closure", "Keeps them warm while they dry"], "7 colors · sizes XS–3XL"),
    options={"Color": ("Color", GRAY)}),
  "snug-sherpa-pet-blanket": dict(title="Snug Sherpa Pet Blanket", handle="snug-sherpa-pet-blanket", type="Pet Blanket",
    tags=["beds-dens"], highlights=["Plush sherpa on one side", "Soft flannel on the other", "Sizes XS to XL"],
    seo="Snug sherpa pet blanket: plush sherpa on one side and soft flannel on the other, in 4 colors and 5 sizes.",
    html=d("Their own cozy layer for the crate, the bed or your couch.", ["Plush sherpa on one side", "Smooth, soft flannel on the other", "From crate size to couch size"], "XS 20×28 in · S 28×39 in · M 39×57 in · L 57×65 in · XL 57×85 in"),
    options={"Color": ("Color", GRAY)}),
  "doze-dog-pajamas": dict(title="Doze Dog Pajamas", handle="doze-dog-pajamas", type="Dog Apparel",
    tags=["beds-dens"], highlights=["Soft cotton one-piece", "Button front, easy on", "Sizes XS to XL"],
    seo="Doze dog pajamas: a soft cotton four-leg onesie with a button front, in palm print or pink, sizes XS to XL.",
    html=d("For chilly nights and lazy mornings on the couch.", ["Soft cotton, four-leg fit", "Button front for easy dressing", "Palm print or pink"], "Cotton · sizes XS–XL"),
    options={"Color": ("Color", {"Leaves": "Palm Print"})}),
  "tidy-bone-silicone-bowl-mat": dict(title="Tidy Double Bowl Feeder", handle="tidy-double-bowl-feeder", type="Pet Bowl",
    tags=["feeding"], highlights=["Two stainless steel bowls", "Non-slip silicone base", "Catches spills, wipes clean"],
    seo="Tidy double bowl feeder: two stainless steel bowls set in a non-slip, bone-shaped silicone mat that catches spills.",
    html=d("Food and water side by side, and the floor stays clean.", ["Two removable stainless steel bowls", "Non-slip, food-grade silicone mat", "Raised rim catches spills"], "S 13.5×8 in, 2×5 oz · M 17.2×9 in, 2×12 oz"),
    options={"Color": ("Color", GRAY)}),
  "riddle-treat-dispensing-ball": dict(title="Riddle Treat Dispensing Ball", handle="riddle-treat-dispensing-ball", type="Dog Toy",
    tags=["play", "feeding"], highlights=["Fill with kibble or treats", "Wobbles and spins as they play", "Slows down fast eaters"],
    seo="Riddle treat dispensing ball: a wobbling puzzle toy that releases kibble or treats as your dog plays.",
    html=d("Turn dinner into a game they have to solve.", ["Fill with kibble or small treats", "Wobbles and spins to release food", "Slows down fast eaters"], "Lake blue or yellow"),
    options={}),
  "maze-puzzle-feeder-bowl": dict(title="Maze Puzzle Feeder Bowl", handle="maze-puzzle-feeder-bowl", type="Pet Bowl",
    tags=["feeding", "play"], highlights=["Sliding puzzle lids", "Slows down fast eaters", "9.4 in, easy to clean"],
    seo="Maze puzzle feeder bowl: sliding lids and hidden pockets turn mealtime into a brain game and slow down fast eaters.",
    html=d("Mealtime becomes a brain game.", ["Sliding lids and hidden pockets", "Turns a 2-minute meal into a longer one", "Non-slip base"], "9.4 in wide · 1.1 in high"),
    options={"Color": ("Color", {"Food bowl": "Classic"})}),
  "burrow-cozy-cat-bed": dict(title="Burrow Plush Pet Bed", handle="burrow-plush-pet-bed", type="Pet Bed",
    tags=["beds-dens"], highlights=["Plush bolster sides", "Thick, warm cushion", "Sizes S to 2XL"],
    seo="Burrow plush pet bed: a thick, warm bed with soft raised sides for cats and dogs, in 3 colors and 5 sizes.",
    html=d("Soft sides to lean on and a thick cushion to sink into.", ["Plush, raised bolster sides", "Thick, warm cushion", "For cats and small to medium dogs"], "S 18×12 in · M 20×16 in · L 24×18 in · XL 28×20 in · 2XL 31×24 in"),
    options={"Color": ("Color", {"Light Gray Thick Warm": "Gray", "Light Green Thick Warm": "Sage", "Light Pink Thick Warm": "Blush"})}),
  "fold-magnetic-cat-scratcher": dict(title="Fold Magnetic Cat Scratcher", handle="fold-magnetic-cat-scratcher", type="Cat Toy",
    tags=["play"], highlights=["Folds into a ring with magnets", "Corrugated cardboard to scratch", "Bell ball for extra play"],
    seo="Fold magnetic cat scratcher: an accordion cardboard scratcher that clicks into a ring, with a bell ball to chase.",
    html=d("A scratcher that changes shape, so they never get bored of it.", ["Accordion cardboard folds open or clicks into a ring", "Satisfying corrugated scratching surface", "Bell ball to bat inside"], "Corrugated cardboard"),
    options={"Color": ("Color", {"Organ Cat Scratch Board": "Classic"})}),
  "chomp-rubber-treat-ball": dict(title="Chomp Rubber Treat Ball", handle="chomp-rubber-treat-ball", type="Dog Toy",
    tags=["play", "feeding"], highlights=["Natural rubber, for chewers", "Hide treats inside", "Bounces and wobbles"],
    seo="Chomp rubber treat ball: a natural rubber chew toy that hides treats and bounces unpredictably.",
    html=d("Chew it, chase it, work out the treat.", ["Natural rubber, made for chewing", "Stuff treats inside", "Saturn shape bounces in odd directions"], "6 in · blue or gray"),
    options={"Color": ("Color", {"blue": "Blue", "grey": "Gray"})}),
  "glow-led-dog-collar": dict(title="Glow LED Dog Collar", handle="glow-led-dog-collar", type="Dog Collar",
    tags=["travel", "gps-safety"], highlights=["Glows for night walks", "USB rechargeable", "Several colors"],
    seo="Glow LED dog collar: a USB rechargeable light-up collar that keeps your dog visible on night walks.",
    html=d("Be seen on every evening walk.", ["Bright LED glow, visible from all sides", "USB rechargeable", "Light and comfortable"], "TPU + ABS"),
    options={"Color": ("Color", {"Grey": "Gray", "New Blue": "Blue", "New Green": "Green", "New Red": "Red"})}),
}

def run(old, c):
    p = prod(old) or prod(c["handle"]); pid = p["id"]
    check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}",
        {"p": {"id": pid, "title": c["title"], "handle": c["handle"], "redirectNewHandle": True, "descriptionHtml": c["html"],
               "vendor": "CozyCompanion", "productType": c["type"], "templateSuffix": "pettech", "status": "DRAFT",
               "seo": {"title": f"{c['title']} | CozyCompanion", "description": c["seo"]}}})["productUpdate"], c["title"])
    check(gql("mutation($id:ID!,$t:[String!]!){tagsAdd(id:$id,tags:$t){userErrors{message}}}", {"id": pid, "t": c["tags"] + ["price-3x", "supplier-zendrop"]})["tagsAdd"], "tags")
    mf = [{"ownerId": pid, "namespace": "custom", "key": f"highlight_{i+1}", "type": "single_line_text_field", "value": h} for i, h in enumerate(c["highlights"])]
    check(gql("mutation($m:[MetafieldsSetInput!]!){metafieldsSet(metafields:$m){userErrors{field message}}}", {"m": mf})["metafieldsSet"], "mf")
    for opt_name, (new_name, values) in c["options"].items():
        o = next((o for o in prod(c["handle"])["options"] if o["name"] == opt_name), None)
        if not o: continue
        upd = [{"id": v["id"], "name": values[v["name"]]} for v in o["optionValues"] if v["name"] in values and values[v["name"]] != v["name"]]
        check(gql("mutation($pid:ID!,$o:OptionUpdateInput!,$v:[OptionValueUpdateInput!]){productOptionUpdate(productId:$pid,option:$o,optionValuesToUpdate:$v){userErrors{field message}}}",
                  {"pid": pid, "o": {"id": o["id"], "name": new_name}, "v": upd})["productOptionUpdate"], c["title"])
    for h in C3:
        gql("mutation($id:ID!,$p:[ID!]!){collectionAddProducts(id:$id,productIds:$p){userErrors{message}}}", {"id": COLS[h], "p": [pid]})
    print("branded:", c["title"])

def trim_fetch():
    """US store: drop the AU/UK/EU/CH plugs, the odd bowl bundle, the big set and the 36-ball pack."""
    p = gql('{productByHandle(handle:"fetch-automatic-ball-launcher"){id variants(first:20){nodes{id title}}}}')["productByHandle"]
    drop = [v["id"] for v in p["variants"]["nodes"] if v["title"] in ("AU", "UK", "EU", "CH", "Machine US w/ Blue Bowel", "Set", "Diameter 5cm 36pcs")]
    if drop:
        check(gql("mutation($p:ID!,$v:[ID!]!){productVariantsBulkDelete(productId:$p,variantsIds:$v){userErrors{field message}}}", {"p": p["id"], "v": drop})["productVariantsBulkDelete"], "fetch")
        print("fetch: removed", len(drop), "non-US variants")

if __name__ == "__main__":
    dart = prod("dart-speedy-tail-cat-ball")
    if dart:
        check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}", {"p": {"id": dart["id"], "status": "ARCHIVED"}})["productUpdate"], "dart")
        print("archived: Dart (same item as Zoom)")
    trim_fetch()
    for old, c in NEW.items():
        run(old, c)
