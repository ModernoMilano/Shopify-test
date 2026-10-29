"""Collection-page lifestyle tiles: wide editorial photos of a pet using a piece from that collection, shown across the
full grid after every few products (snippets/cc-collection-tile.liquid, called from sections/main-collection.liquid).

Photos are made with Nano Banana 2.1 (16:9, packshot as reference), uploaded as t_<collection>_<n>, and linked per
collection through two metafields that stay in step: custom.lifestyle_images (files) and custom.lifestyle_products.
Collections without their own set (Shop All, gifts, smart home...) borrow a mix from the category collections.
Usage: python3 -I collection_tiles.py prompts   -> tiles_prompts.json (name, product handle, packshot url, prompt)
       python3 -I collection_tiles.py attach    -> sets the metafields on every collection"""
import sys, os, json, ast
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check

STYLE = ("Premium editorial lifestyle photograph, wide 16:9 framing with the subject in the centre third so it can also be "
         "cropped to 4:3: {scene} The product is exactly the {what} from the reference image, clearly visible and accurate in "
         "shape, colour and details. The pet is the hero: natural, relaxed and happy. Quiet-luxury home in warm cream, oak and "
         "linen tones, soft natural window light, shallow depth of field, no people (at most a hand), no text, no watermark.")
TILES = {
  "beds-dens": [("chester-tufted-dog-sofa", "a Great Dane stretched out asleep on the tufted dog sofa beside a marble fireplace."),
                ("perch-modern-cat-tree", "a Bengal cat lounging in the top hammock of the cat tree by a tall sunny window."),
                ("cocoon-deep-sleep-bed", "a golden puppy curled up deep asleep in the round deep sleep bed on a wool rug.")],
  "smart-feeding": [("glance-camera-feeder", "a grey British shorthair cat eating from the camera feeder in a bright kitchen."),
                    ("brook-pet-fountain", "a tabby cat drinking from the stainless pet fountain, a few drops in the air."),
                    ("pantry-pet-feeding-station", "a cream labradoodle eating from the pull-out drawer of the white feeding station.")],
  "play-enrichment": [("fetch-automatic-ball-launcher", "a Jack Russell terrier mid-leap chasing a ball just launched from the ball launcher on a sunny lawn."),
                      ("wiggle-window-cat-teaser", "a ginger cat on its hind legs pawing at the window teaser stuck to the glass."),
                      ("forage-snuffle-mat", "a beagle with its nose buried in the snuffle mat on a living room floor.")],
  "wear-walk": [("frost-harness-winter-dog-jacket", "a border collie in the winter jacket trotting through fresh snow in a forest."),
                ("drizzle-dog-raincoat", "a French bulldog in the raincoat on a wet city sidewalk with reflections."),
                ("trail-hands-free-dog-leash", "a golden retriever on the hands-free leash trotting along a lakeside path at golden hour.")],
  "groom-clean": [("breeze-pet-grooming-dryer", "a fluffy white Samoyed sitting calmly while the grooming dryer's nozzle gently blows its coat."),
                  ("halo-self-cleaning-litter-box", "a sleek black cat stepping out of the self-cleaning litter box in a bright modern laundry room."),
                  ("splash-quick-dry-dog-bathrobe", "a cockapoo wrapped in the quick-dry dog bathrobe after a bath, on a fluffy bath mat.")],
  "pet-travel": [("voyage-rolling-pet-carrier", "a small Pomeranian peeking out of the rolling pet carrier in a sunlit airport terminal."),
                 ("ride-sherpa-car-booster-seat", "a Maltese sitting in the sherpa car booster seat looking out of the car window."),
                 ("roam-back-seat-dog-bed", "a golden retriever lying on the back seat dog bed of an SUV, door open to a meadow.")],
  "dogs": [("dream-memory-foam-dog-bed", "a Bernese mountain dog sleeping on the memory foam dog bed in a cozy living room."),
           ("quest-dog-puzzle-feeder", "an Australian shepherd solving the puzzle feeder on a kitchen floor."),
           ("stride-dog-harness-leash-set", "a vizsla in the harness and leash set walking through autumn leaves.")],
  "cats": [("haven-pet-den", "a cat peeking out of the felt pet den on a sunny bedroom floor."),
           ("orbit-felt-cat-tunnel-bed", "a kitten tumbling out of the felt tunnel bed on a cream rug."),
           ("pounce-automatic-feather-cat-toy", "a Siamese cat leaping at the feather from the automatic feather toy.")],
}
BORROW = {  # collections without their own photos: round-robin from these sets
  "smart-pet-tech": list(TILES), "holiday-gift-guide": list(TILES), "bundle-deals": list(TILES),
  "gifts-under-50": ["play-enrichment", "wear-walk", "cats", "dogs"], "smart-home": ["smart-feeding", "play-enrichment", "groom-clean"],
  "litter-hygiene": ["groom-clean"], "hydration": ["smart-feeding"], "gps-safety": ["wear-walk"],
}

def gallery():
    src = open(os.path.join(S, "gallery.py")).read()
    return ast.literal_eval(src[src.index("GALLERIES = {") + len("GALLERIES = "): src.index("\n}\n", src.index("GALLERIES = {")) + 2])

if __name__ == "__main__" and sys.argv[1:2] == ["prompts"]:
    reg = json.load(open(os.path.join(S, "files.json"))); G = gallery(); out = []
    for col, items in TILES.items():
        for n, (h, scene) in enumerate(items, 1):
            name = f"t_{col}_{n}"
            if name in reg: continue
            title = gql('query($h:String!){productByHandle(handle:$h){title}}', {"h": h})["productByHandle"]["title"]
            out.append({"name": name, "product": h, "ref": reg[G[h][0]]["url"].split("?")[0],
                        "prompt": STYLE.format(scene=scene[0].upper() + scene[1:], what=title)})
    json.dump(out, open(os.path.join(S, "tiles_prompts.json"), "w"), indent=1)
    print(len(out), "prompts")

if __name__ == "__main__" and sys.argv[1:2] == ["attach"]:
    reg = json.load(open(os.path.join(S, "files.json")))
    for key, typ, name in (("lifestyle_images", "list.file_reference", "Collection lifestyle photos"),
                           ("lifestyle_products", "list.product_reference", "Collection lifestyle products")):
        if not gql('query($k:String!){metafieldDefinitions(first:1,ownerType:COLLECTION,namespace:"custom",key:$k){nodes{id}}}', {"k": key})["metafieldDefinitions"]["nodes"]:
            check(gql("""mutation($d:MetafieldDefinitionInput!){metafieldDefinitionCreate(definition:$d){createdDefinition{id} userErrors{field message}}}""",
                {"d": {"name": name, "namespace": "custom", "key": key, "ownerType": "COLLECTION", "type": typ,
                       "access": {"storefront": "PUBLIC_READ"}}})["metafieldDefinitionCreate"], key)
    pid = {}
    def product_id(h):
        if h not in pid: pid[h] = gql('query($h:String!){productByHandle(handle:$h){id}}', {"h": h})["productByHandle"]["id"]
        return pid[h]
    sets = {col: [(reg[f"t_{col}_{n}"]["id"], h) for n, (h, _) in enumerate(items, 1) if f"t_{col}_{n}" in reg] for col, items in TILES.items()}
    plan = dict(sets)
    for col, sources in BORROW.items():   # interleave: 1st of each source, then 2nd of each...
        plan[col] = [s for i in range(3) for src in sources for s in sets.get(src, [])[i:i + 1]]
    for col, items in plan.items():
        c = gql('query($h:String!){collectionByHandle(handle:$h){id}}', {"h": col})["collectionByHandle"]
        if not c or not items: continue
        check(gql("mutation($m:[MetafieldsSetInput!]!){metafieldsSet(metafields:$m){userErrors{field message}}}", {"m": [
            {"ownerId": c["id"], "namespace": "custom", "key": "lifestyle_images", "type": "list.file_reference", "value": json.dumps([f for f, _ in items])},
            {"ownerId": c["id"], "namespace": "custom", "key": "lifestyle_products", "type": "list.product_reference", "value": json.dumps([product_id(h) for _, h in items])}]})["metafieldsSet"], col)
        print(f"{col:22} {len(items)} photos")
