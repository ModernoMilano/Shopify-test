"""Generation plan for the December calendar: one Nano Banana request per feed image (4:5) and per story (9:16).
Writes social/dec/plan.json: [{key, date, kind, n, aspect, handle, prompt, media}]."""
import json, os, sys
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(D))
from calendar_dec import C, LOOK
MEDIA = json.load(open(os.path.join(D, "media.json")))
TITLE = {
 "snug-sherpa-pet-blanket": "Snug Sherpa Pet Blanket", "roam-back-seat-dog-bed": "Roam Back Seat Dog Bed",
 "buddy-plush-dog-toy": "Buddy Plush Dog Toy", "trail-hands-free-dog-leash": "Trail Hands-Free Dog Leash",
 "purr-tilted-ceramic-cat-bowl": "Purr Tilted Ceramic Cat Bowl", "flutter-cat-play-station": "Flutter Cat Play Station",
 "orbit-felt-cat-tunnel-bed": "Orbit Felt Cat Tunnel Bed", "frost-harness-winter-dog-jacket": "Frost Winter Dog Jacket",
 "cloud-plush-pet-blanket": "Cloud Plush Pet Blanket", "chaise-velvet-storage-pet-sofa": "Chaise Velvet Storage Pet Sofa",
 "savor-bone-lick-mat": "Savor Bone Lick Mat", "chirp-catnip-ball": "Chirp Catnip Ball",
 "beacon-led-collar-light": "Beacon LED Collar Light", "bloom-floral-cat-collar": "Bloom Floral Cat Collar",
 "lounge-plush-pet-sofa": "Lounge Plush Pet Sofa", "glance-camera-feeder": "Glance Camera Feeder",
 "perch-modern-cat-tree": "Perch Modern Cat Tree", "burrow-plush-pet-bed": "Burrow Plush Pet Bed",
 "doze-dog-pajamas": "Doze Dog Pajamas", "cocoon-deep-sleep-bed": "Cocoon Deep Sleep Bed",
 "puddle-suspender-dog-boots": "Puddle Suspender Dog Boots", "ascend-acacia-pet-stairs-ramp": "Ascend Pet Stairs & Ramp",
 "ride-sherpa-car-booster-seat": "Ride Sherpa Car Booster Seat", "plume-feather-teaser-wand": "Plume Feather Teaser Wand",
 "nook-self-warming-pet-mat": "Nook Self-Warming Pet Mat", "nestle-heated-pet-pad": "Nestle Heated Pet Pad",
 "billow-memory-foam-bolster-bed": "Billow Memory Foam Bolster Bed", "haven-pet-den": "Haven Pet Den",
 "quest-dog-puzzle-feeder": "Quest Dog Puzzle Feeder", "halo-self-cleaning-litter-box": "Halo Self-Cleaning Litter Box",
 "stride-dog-harness-leash-set": "Stride Dog Harness & Leash Set", "tame-dematting-comb": "Tame Dematting Comb",
 "breeze-pet-grooming-dryer": "Breeze Pet Grooming Dryer", "pace-stainless-slow-feeder-bowl": "Pace Stainless Slow Feeder Bowl",
}
# carousel days: one scene per product, same palette
CAROUSEL = {
 "2026-12-02": ["A golden retriever relaxing on the Roam back seat dog bed spread across a car's back seat, a small wrapped gift with rose-gold ribbon beside it, snowy trees through the window.",
                "A puppy hugging the Buddy plush dog toy on a cream rug beside a softly lit Christmas tree.",
                "A woman walking her dog on the Trail hands-free leash clipped around her waist, on a snowy park path at golden hour."],
 "2026-12-03": ["A Siamese cat eating from the Purr tilted ceramic cat bowl on a cream kitchen floor, a ribbon-tied gift beside it.",
                "A kitten pouncing at the feather of the Flutter cat play station on a rug near a softly lit Christmas tree.",
                "A cat peeking out of the Orbit felt cat tunnel bed in a calm living room with a sprig of evergreen and soft lights."],
 "2026-12-08": ["A kitten batting the Chirp catnip ball out of a cream knit stocking on a rug by the fireplace.",
                "A dog on an evening winter walk, the Beacon LED collar light glowing on its collar, soft bokeh street lights behind.",
                "A cat wearing the Bloom floral cat collar with its little bell, sitting by a softly lit Christmas tree."],
 "2026-12-12": ["A puppy curled up asleep in the Burrow plush pet bed in a calm cream bedroom with soft tree lights.",
                "The Snug sherpa pet blanket draped over a pet bed with a sleepy dog snuggled into it, cozy evening light.",
                "A small dog wearing the Doze cotton dog pajamas sitting by a softly lit Christmas tree."],
 "2026-12-19": ["A cat curled up on the Nook self-warming pet mat by a frosty window, soft evening lamp light.",
                "A dog stretched out comfortably on the Nestle heated pet pad on a cream sofa, a knit throw and candle light.",
                "A dog asleep in the Billow memory foam bolster bed, candles glowing softly in the background."],
 "2026-12-30": ["A long-haired cat being gently combed with the Tame dematting comb, a calm bright cream room.",
                "A doodle being dried with the Breeze pet grooming dryer after a bath, towel nearby, bright clean bathroom.",
                "A dog eating calmly from the Pace stainless slow feeder bowl on a light oak kitchen floor."],
}
TAIL = ("{look}, natural light, shallow depth of field, sharp focus on the pet and the product. "
        "Photorealistic, natural anatomy. No text, letters, labels, logos or watermarks anywhere in the image.")
def feed_prompt(scene, handle):
    ref = f" The {TITLE[handle]} must match the reference image exactly in shape, color, materials and details." if handle else ""
    return f"Photorealistic premium editorial social media photo, vertical 4:5. {scene}{ref} " + TAIL.format(look=LOOK)
def story_prompt(scene, handle):
    ref = f" The {TITLE[handle]} must match the reference image exactly in shape, color, materials and details." if handle else ""
    return (f"Photorealistic premium editorial vertical 9:16 photo for an Instagram story. {scene}{ref} "
            "Compose it vertically: the pet and the product centred in the middle of the frame, a calm uncluttered top 15% "
            "and a calm floor, rug or wall in the bottom 25% (text will be added there). " + TAIL.format(look=LOOK))
P = []
for c in C:
    d = c["date"]; hs = c["products"]
    if d in CAROUSEL:
        for n, (h, sc) in enumerate(zip(hs, CAROUSEL[d])):
            P.append(dict(key=f"f_{d}_{n}", date=d, kind="feed", n=n, aspect="4:5", handle=h, prompt=feed_prompt(sc, h), media=MEDIA[h]))
        P.append(dict(key=f"st_{d}", date=d, kind="story", n=0, aspect="9:16", handle=hs[0], prompt=story_prompt(CAROUSEL[d][0], hs[0]), media=MEDIA[hs[0]]))
    else:
        h = hs[0] if hs else None
        P.append(dict(key=f"f_{d}_0", date=d, kind="feed", n=0, aspect="4:5", handle=h, prompt=feed_prompt(c["scene"], h), media=MEDIA.get(h)))
        P.append(dict(key=f"st_{d}", date=d, kind="story", n=0, aspect="9:16", handle=h, prompt=story_prompt(c["scene"], h), media=MEDIA.get(h)))
json.dump(P, open(os.path.join(D, "plan.json"), "w"), indent=1, ensure_ascii=False)
print(len(P), "images")
