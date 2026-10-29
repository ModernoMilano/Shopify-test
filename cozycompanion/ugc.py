"""'Life with CozyCompanion': candid, phone-style lifestyle photos of people at home with their pet and the product
(one per product, made with Nano Banana from our packshot). They are brand lifestyle photos, not customer photos:
the section never names people or calls them reviews. Stored in the product metafield custom.ugc_images and shown
by sections/cc-ugc.liquid at the bottom of every product page.
Usage: python3 -I ugc.py prompts            -> writes ugc_prompts.json (handle, ref url, prompt)
       python3 -I ugc.py attach <handle>... -> links uploaded u_<key> files to their products"""
import sys, os, json, ast
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check

STYLE = ("Authentic UGC-style smartphone photo, candid and natural, vertical 4:5 framing: {scene} The product is exactly "
         "the {what} from the reference image, clearly visible, accurate in shape, colour and details. Real lived-in home, "
         "natural window light, slight phone-camera softness, genuine warm happy expressions, not a studio shot, "
         "no text, no watermarks, no extra logos.")
SCENES = {
  "ember-heat-pad": "a smiling woman in a cozy knit sweater on her sofa with the heat pad across her lap and a small terrier curled up on it, mug of tea in hand.",
  "compass-smart-tag": "a laughing young man crouching on a park path, showing the smart tag on his beagle's collar to the camera.",
  "nestle-heated-pet-pad": "a happy older man on the living room floor stroking his senior greyhound sleeping on the heated pad.",
  "brook-pet-fountain": "a cheerful woman kneeling in her kitchen watching her tabby cat drink from the fountain, smiling at the camera.",
  "dine-automatic-feeder": "a woman in a work blazer at her front door grabbing her keys, smiling back at her cat waiting by the automatic feeder.",
  "haven-pet-den": "a happy couple sitting on their bedroom floor as their cat peeks out of the felt den between them.",
  "halo-self-cleaning-litter-box": "a relaxed young man in a modern laundry room giving a thumbs up next to the self-cleaning litter box, his cat sitting nearby.",
  "glance-camera-feeder": "a smiling woman kneeling beside the camera feeder in her kitchen, waving at its lens while her cat eats.",
  "murmur-camera-feeder": "a grinning teenage girl filming her two kittens eating from the camera feeder in a bright kitchen.",
  "brook-xl-cordless-fountain": "a man in a home office smiling at his husky drinking from the cordless fountain on the floor beside his desk.",
  "flutter-cat-play-station": "a delighted little girl on a rug watching her kitten bat at the play station, her mother smiling behind her.",
  "spark-laser-cat-toy": "a couple laughing on their sofa as their cat leaps after the laser dot from the toy on the coffee table.",
  "voyage-rolling-pet-carrier": "a stylish woman walking through a sunny airport terminal pulling the rolling carrier, her small dog looking out, both looking happy.",
  "roam-back-seat-dog-bed": "a smiling father opening the car's back door to show his golden retriever lying on the back seat dog bed.",
  "cloud-plush-pet-blanket": "a woman and her corgi snuggled together under the plush blanket on a sofa, both looking content.",
  "nook-self-warming-pet-mat": "a smiling man by a sunny window petting his cat curled on the self-warming mat.",
  "purr-tilted-ceramic-cat-bowl": "a young woman sitting on her kitchen floor smiling as her Siamese cat eats from the tilted ceramic bowl.",
  "orbit-felt-cat-tunnel-bed": "two laughing kids lying on the floor peeking at their cat inside the felt tunnel bed.",
  "lounge-plush-pet-sofa": "a happy woman on her own sofa smiling down at her Pomeranian lounging on the plush pet sofa next to it.",
  "pace-stainless-slow-feeder-bowl": "a smiling man in his kitchen putting the stainless slow feeder bowl down for his eager Labrador.",
  "quest-dog-puzzle-feeder": "a cheerful woman on the floor cheering on her border collie solving the puzzle feeder.",
  "stride-dog-harness-leash-set": "a smiling jogger in autumn leaves with her vizsla wearing the harness and leash set, mid-stride.",
  "wander-cat-harness-leash": "a delighted young man in a garden with his Bengal cat exploring the grass on the harness and leash.",
  "flit-flapping-bird-cat-toy": "a grandmother laughing in her armchair as her cat pounces on the flapping bird toy on the rug.",
  "zoom-self-rolling-cat-ball": "a young couple on a hallway floor laughing as their kitten chases the self-rolling ball.",
  "plume-feather-teaser-wand": "a smiling woman on a rug dangling the feather wand while her cat leaps for it.",
  "knot-tug-fetch-ball": "a laughing teenage boy in a backyard playing tug with his boxer using the tug and fetch ball.",
  "buddy-plush-dog-toy": "a smiling woman on a sofa while her puppy cuddles the plush toy beside her.",
  "forage-snuffle-mat": "a happy man sitting cross-legged on the floor watching his beagle sniff treats in the snuffle mat.",
  "knit-small-dog-sweater": "a smiling woman holding her chihuahua wearing the knit sweater close to her face on a city street in autumn.",
  "drizzle-dog-raincoat": "a cheerful man with an umbrella on a rainy sidewalk, his French bulldog in the raincoat beside him.",
  "cove-ceramic-cat-bowl": "a smiling woman setting the ceramic cat bowl on a kitchen floor mat for her ragdoll cat.",
  "chase-plush-prey-cat-toy": "a laughing young man on the floor as his cat wrestles the plush prey toys.",
  "fetch-automatic-ball-launcher": "a family laughing on their patio as their Jack Russell races after a ball shot from the launcher.",
  "glide-soft-dog-frisbee": "a smiling woman in a sunny park throwing the soft frisbee to her leaping Australian shepherd.",
  "gnaw-dental-chew-toy": "a happy man on a sofa watching his pit bull happily chewing the dental chew toy at his feet.",
  "puddle-suspender-dog-boots": "a laughing woman on a snowy sidewalk with her poodle wearing the suspender boots.",
  "frost-harness-winter-dog-jacket": "a smiling man in a winter coat on a snowy trail with his dog wearing the winter jacket.",
  "splash-quick-dry-dog-bathrobe": "a laughing mother and daughter in a bathroom drying their wet cockapoo wrapped in the bathrobe.",
  "snug-sherpa-pet-blanket": "a woman reading on her bed smiling at her cat kneading the sherpa blanket.",
  "doze-dog-pajamas": "a giggling couple on their bed with their dachshund wearing the pajamas between them.",
  "tidy-double-bowl-feeder": "a smiling woman pouring water into the double bowl feeder for her two kittens.",
  "riddle-treat-dispensing-ball": "a happy man in his living room watching his terrier nudge the treat dispensing ball.",
  "maze-puzzle-feeder-bowl": "a smiling woman filling the puzzle feeder bowl with kibble while her husky waits patiently.",
  "burrow-plush-pet-bed": "a young woman lying on the floor smiling at her cat cozy in the plush bed.",
  "fold-magnetic-cat-scratcher": "a grinning man on a rug as his kitten scratches and plays on the magnetic scratcher.",
  "chomp-rubber-treat-ball": "a happy woman in a garden tossing the rubber treat ball to her Labrador puppy.",
  "pounce-automatic-feather-cat-toy": "two friends laughing on a sofa as a cat pounces at the feather spinning from the toy.",
  "chirp-catnip-ball": "a smiling woman on the floor watching her cat roll around with the catnip balls.",
  "cradle-pet-sling-carrier": "a smiling woman at a farmers market carrying her small dog in the sling carrier.",
  "bloom-floral-cat-collar": "a happy young woman holding her white cat up to the camera, wearing the floral collar.",
  "mistle-knit-dog-hood": "a laughing man holding his small dog wearing the red knit hood in front of a decorated Christmas tree.",
  "trail-hands-free-dog-leash": "a smiling woman jogging along a lakeside path with her dog on the hands-free leash around her waist.",
  "dapper-gingham-bow-tie": "a grinning groom at a garden wedding kneeling beside his dog wearing the gingham bow tie.",
  "fin-dog-life-jacket": "a happy family on a wooden dock with their Labrador wearing the life jacket about to jump in a lake.",
  "sift-honeycomb-litter-mat": "a smiling woman in a tidy bathroom placing the honeycomb mat in front of the litter box, her cat watching.",
  "lift-pet-hair-remover-ball": "a cheerful man pulling a fresh, hair-free hoodie out of the dryer with the hair remover ball, his dog watching.",
  "polish-pet-nail-grinder": "a calm smiling woman on a sofa gently using the nail grinder on her relaxed dog's paw.",
  "savor-bone-lick-mat": "a happy woman on her bathroom floor as her dog licks the bone lick mat during bath time.",
  "measure-smart-scale-scoop": "a smiling man in his kitchen weighing kibble with the scale scoop while his dog watches.",
  "beacon-led-collar-light": "a laughing couple on an evening walk with their dog wearing the glowing LED collar light.",
  "tame-dematting-comb": "a smiling teen girl on a porch brushing her fluffy collie with the dematting comb.",
  "slate-silicone-feeding-mat": "a smiling woman setting her dog's bowls on the silicone feeding mat in a bright kitchen.",
  "wiggle-window-cat-teaser": "a delighted woman laughing beside a window as her cat paws at the window teaser stuck to the glass.",
  "jetset-soft-pet-carrier": "a smiling young man on a train holding the soft pet carrier on his lap with his cat peeking out.",
  "breeze-pet-grooming-dryer": "a happy woman in a laundry room drying her fluffy Samoyed with the grooming dryer.",
  "ascend-acacia-pet-stairs-ramp": "a smiling older woman on her bed welcoming her senior dachshund climbing the wooden pet stairs.",
  "dream-memory-foam-dog-bed": "a happy man sitting on the floor with his arm around his big Bernese mountain dog lying on the memory foam bed.",
  "billow-memory-foam-bolster-bed": "a smiling woman kneeling beside her golden retriever resting on the bolster bed in a sunny living room.",
  "perch-modern-cat-tree": "a laughing couple in a modern living room as their two cats lounge on the cat tree.",
  "sweep-grooming-vacuum-kit": "a smiling man grooming his calm husky with the vacuum kit, no loose hair on the floor.",
  "cocoon-deep-sleep-bed": "a happy young woman on her bedroom floor smiling at her puppy curled in the round deep sleep bed.",
  "trim-cordless-clipper-kit": "a smiling woman gently trimming her shih tzu's paws with the cordless clipper on a bathroom counter.",
  "fresh-smart-litter-deodorizer": "a cheerful man showing the litter deodorizer mounted by the litter box in a fresh, bright bathroom, cat nearby.",
  "peak-triangle-cat-scratcher": "a smiling woman on her rug as her cat stretches and scratches on the triangle scratcher.",
  "ride-sherpa-car-booster-seat": "a smiling woman in the driver's seat glancing back at her Maltese sitting in the sherpa car booster seat.",
  "pantry-pet-feeding-station": "a happy couple in their kitchen as their doodle eats from the feeding station's pull-out drawer.",
  "chester-tufted-dog-sofa": "a laughing woman on her living room sofa next to her Great Dane lounging on the tufted dog sofa.",
  "chaise-velvet-storage-pet-sofa": "a smiling young woman lifting the seat of the velvet chaise to put a toy away while her cat watches from the cushion.",
}

def gallery():
    src = open(os.path.join(S, "gallery.py")).read()
    return ast.literal_eval(src[src.index("GALLERIES = {") + len("GALLERIES = "): src.index("\n}\n", src.index("GALLERIES = {")) + 2])

def key(handle): return {"brook-xl-cordless-fountain": "brookxl"}.get(handle, handle.split("-")[0])

if __name__ == "__main__" and sys.argv[1:2] == ["prompts"]:
    reg = json.load(open(os.path.join(S, "files.json"))); G = gallery(); out = []
    for h, scene in SCENES.items():
        if h not in G or f"u_{key(h)}" in reg: continue
        title = gql('query($h:String!){productByHandle(handle:$h){title}}', {"h": h})["productByHandle"]["title"]
        out.append({"handle": h, "name": f"u_{key(h)}", "ref": reg[G[h][0]]["url"].split("?")[0],
                    "prompt": STYLE.format(scene=scene[0].upper() + scene[1:], what=title)})
    json.dump(out, open(os.path.join(S, "ugc_prompts.json"), "w"), indent=1)
    print(len(out), "prompts")

if __name__ == "__main__" and sys.argv[1:2] == ["attach"]:
    reg = json.load(open(os.path.join(S, "files.json")))
    if not gql('{metafieldDefinitions(first:1,ownerType:PRODUCT,namespace:"custom",key:"ugc_images"){nodes{id}}}')["metafieldDefinitions"]["nodes"]:
        check(gql("""mutation($d:MetafieldDefinitionInput!){metafieldDefinitionCreate(definition:$d){createdDefinition{id} userErrors{field message}}}""",
            {"d": {"name": "Lifestyle photos (Life with CozyCompanion)", "namespace": "custom", "key": "ugc_images", "ownerType": "PRODUCT",
                   "type": "list.file_reference", "access": {"storefront": "PUBLIC_READ"}}})["metafieldDefinitionCreate"], "definition")
    handles = sys.argv[2:] or list(SCENES)
    for h in handles:
        names = sorted(n for n in reg if n == f"u_{key(h)}" or n.startswith(f"u_{key(h)}_"))
        if not names: continue
        pid = gql('query($h:String!){productByHandle(handle:$h){id}}', {"h": h})["productByHandle"]["id"]
        check(gql("mutation($m:[MetafieldsSetInput!]!){metafieldsSet(metafields:$m){userErrors{field message}}}",
                  {"m": [{"ownerId": pid, "namespace": "custom", "key": "ugc_images", "type": "list.file_reference",
                          "value": json.dumps([reg[n]["id"] for n in names])}]})["metafieldsSet"], h)
        print("attached", h, names)
