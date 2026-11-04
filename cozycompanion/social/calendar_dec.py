"""December 2026 content calendar, "The Cozy Season" (drafted for the owner's approval). Writes social/calendar_dec.json
with the same structure as calendar.json (November): date, theme, products, scene, caption, tags, story_text, reel, assets.
Look: warm cream/oak/linen interiors, soft candle and tree lights, cream & rose-gold ornaments and ribbon, a sprig of
evergreen, snowy windows. Quiet luxury, never kitsch or a red/green overload.
Rules (social/QA.md): only verified product facts (product highlights), no prices, no reviews or invented quotes,
COZY15 at most twice a week and never Dec 24-26, delivery wording "best chance of delivery", never "guaranteed".
Gift-card days (12-17, 12-23) link the digital gift card product (created 2026-11-04, approved by the owner)."""
import json, os
H_DOG = "#dogsofinstagram #doglife #dogmom #doglover #puppylove"
H_CAT = "#catsofinstagram #catlife #catmom #catlover #kittylove"
H_PET = "#petsofinstagram #petlover #dogsandcats #furbaby"
H_HOME = "#cozyhome #slowliving #homedecor #petfriendlyhome"
H_XMAS = "#holidaygifts #giftideas #christmaswithpets"
LINK = "Shop via the link in bio 🐾"
COZY15 = "New here? Take 15% off your first order with code COZY15."
LOOK = ("Cozy-season palette: warm cream, oak and linen tones, soft warm light, small touches of cream and rose-gold "
        "ornaments or ribbon and a sprig of evergreen where natural, quiet luxury, never kitsch")
C = [
 dict(date="2026-12-01", theme="brand_story", products=["snug-sherpa-pet-blanket"],
      scene="A grey-muzzled senior rescue dog wrapped in the Snug sherpa blanket, resting by a frosty window in a calm cream living room, soft morning light.",
      caption="It's Giving Tuesday. 🤍\n\nSo many shelter pets are waiting for a warm spot this winter. If you can, donate, volunteer, foster or adopt at a shelter near you. Every bit of kindness counts.\n\nTag a shelter you love below. 👇",
      tags=f"{H_DOG} #givingtuesday #adoptdontshop #rescuedog #seniordog #fosteringsaveslives"),
 dict(date="2026-12-02", theme="gift_guide", products=["roam-back-seat-dog-bed", "buddy-plush-dog-toy", "trail-hands-free-dog-leash"],
      scene="Three gift-guide images in one cozy-season palette: a golden retriever relaxing on the Roam bed across a car's back seat with a wrapped gift; a puppy hugging the Buddy plush by a softly lit tree; a woman walking her dog on the Trail hands-free leash on a snowy path.",
      caption=f"Gift guide: for the dog who has everything. 🎁\n\n1. Roam: turns the back seat into a flat, waterproof bed\n2. Buddy: a super-soft plush in lifelike breed designs\n3. Trail: a hands-free leash with a zip pouch and reflective stitching\n\n{COZY15} {LINK}",
      tags=f"{H_DOG} {H_XMAS} #giftsfordogs #dogmomgift"),
 dict(date="2026-12-03", theme="gift_guide", products=["purr-tilted-ceramic-cat-bowl", "flutter-cat-play-station", "orbit-felt-cat-tunnel-bed"],
      scene="Three gift-guide images in one cozy-season palette: a Siamese eating from the tilted Purr bowl beside a ribbon-tied gift; a kitten pouncing at the Flutter play station near the tree; a cat peeking out of the Orbit felt tunnel bed.",
      caption=f"Gift guide: for the cat who rules the house. 👑\n\n1. Purr: a raised, tilted ceramic bowl for comfy dinners\n2. Flutter: a pop-up feather and rolling ball with several modes\n3. Orbit: a felt bed and tunnel in one\n\n{LINK}",
      tags=f"{H_CAT} {H_XMAS} #giftsforcats #catdad"),
 dict(date="2026-12-04", theme="playful", products=["frost-harness-winter-dog-jacket"],
      scene="A happy border collie in the padded Frost winter jacket bounding through fresh snow in a quiet snowy garden, soft winter light.",
      caption="Snow day? They're dressed for it. ❄️\n\nFrost has a built-in harness with a leash ring, a padded fleece-lined collar and reflective straps.\n\nOrdering gifts? Order by December 16 for delivery before Christmas.\n\n" + LINK,
      tags=f"{H_DOG} #snowdog #winterwalk #dogcoat #dogsinclothes #holidayseason"),
 dict(date="2026-12-05", theme="gift_idea", products=["cloud-plush-pet-blanket"],
      scene="A wrapped gift under a softly lit Christmas tree, its paper folded back to show the Cloud faux fur blanket, a curious cat sniffing it.",
      caption=f"Gift it today, under the tree in 3–5 business days. 🎄\n\nCloud makes it easy: faux fur on top, sherpa underneath, water-resistant. 4 sizes, 2 colors.\n\n{COZY15} {LINK}",
      tags=f"{H_CAT} {H_XMAS} #lastminutegifts #petblanket"),
 dict(date="2026-12-06", theme="brand_story", products=["chaise-velvet-storage-pet-sofa"],
      scene="A dog resting elegantly on the velvet Chaise pet sofa beside a softly lit Christmas tree in a calm cream living room, lots of quiet space.",
      caption="Slow Sunday, tree lights on. 🕯️\n\nChaise is a velvet chaise with a curved arm, a thick quilted cushion and a lift-up seat that hides their toys.\n\n" + LINK,
      tags=f"{H_DOG} #sundaymood {H_HOME} #interiordesign"),
 dict(date="2026-12-07", theme="care_tip", products=["savor-bone-lick-mat"],
      scene="A dog happily licking the Savor bone lick mat on a kitchen floor, a festive dinner table softly blurred in the background.",
      caption="Holiday tip: keep the table scraps for the humans. 🍽️\n\nChocolate, grapes and raisins, onions and xylitol (in some sweets and peanut butters) are dangerous for dogs. Give them their own treat instead: a spoon of plain pumpkin on Savor keeps them busy and calm.\n\n" + LINK,
      tags=f"{H_DOG} #dogsafety #petcare #holidaytips #lickmat #dogtips"),
 dict(date="2026-12-08", theme="gift_idea", products=["chirp-catnip-ball", "beacon-led-collar-light", "bloom-floral-cat-collar"],
      scene="Three stocking-stuffer images in one palette: a kitten batting the Chirp catnip ball out of a cream stocking; the Beacon light glowing on a dog's collar on an evening walk; a cat wearing the Bloom floral collar by the tree.",
      caption=f"Stocking stuffers they'll actually use. 🧦\n\n1. Chirp: a refillable catnip ball, easy to bat\n2. Beacon: an LED light that clips onto any collar\n3. Bloom: a floral cat collar with a little bell\n\n{COZY15} {LINK}",
      tags=f"{H_PET} {H_XMAS} #stockingstuffers #cattoys"),
 dict(date="2026-12-09", theme="life_with", products=["lounge-plush-pet-sofa"],
      scene="Candid phone-style photo: a woman sitting on the floor wrapping gifts with rose-gold ribbon while her cat lounges on the plush Lounge pet sofa, watching closely.",
      caption="Gift-wrapping supervisor, reporting for duty. 🎀\n\nLounge is a real little sofa for them, in fluffy plush with bolster arms and a removable cushion.\n\n" + LINK,
      tags=f"{H_CAT} #giftwrapping #catsofig #petsofa {H_HOME}"),
 dict(date="2026-12-10", theme="product_spotlight", products=["glance-camera-feeder"],
      scene="A cat eating from the Glance camera feeder in a calm kitchen with a small decorated tree, the camera lens facing the viewer, morning light.",
      caption=f"Travelling for the holidays? 🧳\n\nGlance serves their meals on schedule via the app, and the HD camera lets you check in anytime.\n\n{COZY15} {LINK}",
      tags=f"{H_CAT} #smarthome #petcamera #holidaytravel {H_PET}"),
 dict(date="2026-12-11", theme="playful", products=["perch-modern-cat-tree"],
      scene="A Bengal cat lounging proudly on the Perch modern cat tree right next to a decorated Christmas tree, ornaments untouched, warm evening light.",
      caption="The only tree they're allowed to climb. 🎄😼\n\nPerch has hammocks, a hideaway and a lookout, sisal scratching posts and a sturdy metal frame.\n\n" + LINK,
      tags=f"{H_CAT} #funnycats #cattree #christmascat {H_HOME}"),
 dict(date="2026-12-12", theme="gift_idea", products=["burrow-plush-pet-bed", "snug-sherpa-pet-blanket", "doze-dog-pajamas"],
      scene="Three images of The Cozy Nap Set in one palette: a puppy curled in the Burrow plush bed; the Snug sherpa blanket draped over the bed with a sleepy dog; a dog in the Doze cotton pajamas by the tree.",
      caption="Meet The Cozy Nap Set. 💤\n\n1. Burrow: a plush bolster bed with a thick, warm cushion\n2. Snug: plush sherpa on one side, soft flannel on the other\n3. Doze: soft cotton pajamas with a button front\n\nPut all three in your cart and 20% comes off the set automatically.\n\n" + LINK,
      tags=f"{H_DOG} {H_XMAS} #dogbed #dogpajamas #napqueen"),
 dict(date="2026-12-13", theme="brand_story", products=["cocoon-deep-sleep-bed"],
      scene="A dog deeply asleep in the round Cocoon bed beside a glowing fireplace, a cream knit throw and a few rose-gold ornaments nearby, calm and warm.",
      caption="Fire on. Phone off. Dog asleep. 🔥\n\nCocoon has a thick raised round bolster to sink into and a removable, washable cover.\n\n" + LINK,
      tags=f"{H_DOG} #sundaymood #dogbed #fireplace {H_HOME}"),
 dict(date="2026-12-14", theme="care_tip", products=["puddle-suspender-dog-boots"],
      scene="A poodle in the Puddle suspender boots stepping through a snowy, salted sidewalk at dusk, warm shop lights behind.",
      caption="Winter paw tip: salt and ice are rough on paws. 🐾\n\nWipe their paws with a warm cloth after every walk and check between the pads. Boots help: Puddle has suspender straps that keep them on, and a water-repellent, wipe-clean finish.\n\n" + LINK,
      tags=f"{H_DOG} #pawcare #wintertips #dogboots #petcare #winterwalk"),
 dict(date="2026-12-15", theme="product_spotlight", products=["ascend-acacia-pet-stairs-ramp"],
      scene="A senior dachshund calmly walking up the acacia Ascend stairs onto a cozy sofa decorated with a holiday throw, tree lights behind.",
      caption=f"Everyone gets a seat on the sofa this season. 🛋️\n\nAscend has 4 steps that fold into a ramp, in solid acacia wood, for pets up to 110 lb.\n\n{COZY15} {LINK}",
      tags=f"{H_DOG} #seniordog #petstairs #dachshund {H_HOME}"),
 dict(date="2026-12-16", theme="life_with", products=["ride-sherpa-car-booster-seat"],
      scene="A happy Maltese sitting in the Ride sherpa booster seat on the front passenger seat of a cream-leather car, snowy trees and string lights blurred through the side window. No driver hands, no steering wheel in focus.",
      caption="Driving home for Christmas. 🚗\n\nToday is the last day to order for delivery before Christmas.\n\nRide has a soft sherpa lining, raises small pets so they can see out, and has a seat strap and safety clip.\n\n" + LINK,
      tags=f"{H_DOG} #roadtripwithdog #holidaytravel #smalldog #maltese"),
 dict(date="2026-12-17", theme="gift_idea", products=["digital-gift-card"], gift_card=True,
      scene="An elegant blank cream gift card with a rose-gold edge resting on dark velvet, a dog's nose curiously sniffing it, a sprig of evergreen and soft candle light. The card itself has no text.",
      caption="Not sure what to get them? 💌\n\nGive the CozyCompanion gift card: delivered by email instantly, so they can pick the piece they love.\n\n" + LINK,
      tags=f"{H_PET} {H_XMAS} #giftcard #lastminutegifts"),
 dict(date="2026-12-18", theme="playful", products=["plume-feather-teaser-wand"],
      scene="A tabby cat leaping to bat the Plume feather teaser wand in front of a decorated Christmas tree, the ornaments staying on the tree, warm evening light.",
      caption="The feathers are the only thing that flies this season. 🪶😹\n\nPlume has natural pheasant feathers on a flexible wand, made for playtime together.\n\n" + LINK,
      tags=f"{H_CAT} #funnycats #cattoys #christmascat #catplay"),
 dict(date="2026-12-19", theme="collection_carousel", products=["nook-self-warming-pet-mat", "nestle-heated-pet-pad", "billow-memory-foam-bolster-bed"],
      scene="Three cozy-night-in images in one palette: a cat curled on the Nook mat by a frosty window; a dog stretched on the Nestle heated pad on the sofa; a dog asleep in the Billow bolster bed with candle light.",
      caption=f"Cozy night in. 🕯️\n\n1. Nook: reflects their own body heat, no power needed\n2. Nestle: 3 warmth levels and an anti-bite cable\n3. Billow: a supportive memory foam base with soft bolsters\n\n{COZY15} {LINK}",
      tags=f"{H_PET} #cozynight #winternights #petbed {H_HOME}"),
 dict(date="2026-12-20", theme="brand_story", products=["haven-pet-den"],
      scene="A white cat resting inside the felt Haven den, a snowy window behind it and soft fairy lights, calm and quiet.",
      caption="Snow outside. Their own den inside. ❄️\n\nHaven is a bed and a den in one, in quiet, scratch-resistant felt with a washable cover.\n\n" + LINK,
      tags=f"{H_CAT} #snowday #catden {H_HOME}"),
 dict(date="2026-12-21", theme="product_spotlight", products=["billow-memory-foam-bolster-bed"],
      scene="A dog sleeping in the Billow memory foam bolster bed at dusk, a window showing early winter darkness and snow, a lamp and candles glowing.",
      caption="The longest night deserves the coziest bed. 🌙\n\nBillow has a supportive memory foam base, soft woven bolsters and a removable, washable cover.\n\n" + LINK,
      tags=f"{H_DOG} #wintersolstice #dogbed #memoryfoam {H_HOME}"),
 dict(date="2026-12-22", theme="care_tip", products=["burrow-plush-pet-bed"],
      scene="A small dog resting peacefully in the Burrow plush bed in a quiet bedroom, a holiday party softly blurred through the open door.",
      caption="Holiday guests tip: give them a quiet retreat. 🤫\n\nSet up their bed in a calm room away from the party, with water and a favorite toy, and let them choose when to say hello. Burrow's plush bolster sides make it feel like a safe nest.\n\n" + LINK,
      tags=f"{H_PET} #petcare #holidaytips #calmdog #dogbed"),
 dict(date="2026-12-23", theme="gift_idea", products=["digital-gift-card"], gift_card=True,
      scene="A blank cream gift card with a rose-gold edge tucked into a cream knit stocking hanging by the fireplace, a cat looking up at it. The card itself has no text.",
      caption="Last-minute? Still lovely. 🎄\n\nThe CozyCompanion gift card is delivered by email instantly, perfect for the pet lover on your list.\n\n" + LINK,
      tags=f"{H_PET} {H_XMAS} #giftcard #lastminutegifts"),
 dict(date="2026-12-24", theme="life_with", products=["doze-dog-pajamas"],
      scene="Christmas Eve: a dog in the Doze cotton pajamas sitting by the softly lit tree, a family on the sofa softly out of focus behind.",
      caption="Christmas Eve, pajamas on. 🎄\n\nFrom all of us at CozyCompanion: we hope your home is warm and full tonight.",
      tags=f"{H_DOG} #christmaseve #dogpajamas #christmaswithpets #familytime"),
 dict(date="2026-12-25", theme="playful", products=["buddy-plush-dog-toy"],
      scene="Christmas morning: a puppy pulling a Buddy plush toy out of an opened cream gift box with rose-gold ribbon, beside the tree.",
      caption="Merry Christmas from CozyCompanion. 🤍\n\nMay your day be full of wagging tails and happy purrs.",
      tags=f"{H_DOG} #merrychristmas #christmasmorning #puppylove #christmaswithpets"),
 dict(date="2026-12-26", theme="playful", products=["nook-self-warming-pet-mat"],
      scene="A cat fast asleep on the Nook self-warming mat surrounded by crumpled wrapping paper and loose ribbon, morning-after calm.",
      caption="Boxing Day mood. 😴\n\nNook reflects their own body heat back to them, no power needed, in soft velour.\n\n" + LINK,
      tags=f"{H_CAT} #boxingday #sleepycat #catnap {H_HOME}"),
 dict(date="2026-12-27", theme="care_tip", products=["quest-dog-puzzle-feeder"],
      scene="A border collie working out the Quest puzzle feeder on a living-room rug, new toys in a basket beside it.",
      caption="Post-holiday tip: rotate the new toys. 🧩\n\nPut half away and swap them each week so everything feels new again. Add a brain game too: Quest turns treats into a puzzle with slides, flips and hidden pockets.\n\n" + LINK,
      tags=f"{H_DOG} #enrichment #dogpuzzle #dogtips #smartdog"),
 dict(date="2026-12-28", theme="product_spotlight", products=["halo-self-cleaning-litter-box"],
      scene="A cat stepping out of the white Halo self-cleaning litter box in a bright, minimal bathroom, calm morning light.",
      caption=f"New year, no more scooping. ✨\n\nHalo cleans itself after every visit, has 4 weight sensors for safety and app control.\n\n{COZY15} {LINK}",
      tags=f"{H_CAT} #smarthome #litterbox #newyear #catcare"),
 dict(date="2026-12-29", theme="life_with", products=["stride-dog-harness-leash-set"],
      scene="Candid photo of a man walking his dog on the Stride harness and leash along a snowy street at dusk, warm window lights glowing.",
      caption="Winter dusk walks, our favorite kind. 🌆\n\nStride is a padded, breathable harness and leash set, adjustable from XS to XL.\n\n" + LINK,
      tags=f"{H_DOG} #dogwalk #winterwalk #dusk #doglife"),
 dict(date="2026-12-30", theme="collection_carousel", products=["tame-dematting-comb", "breeze-pet-grooming-dryer", "pace-stainless-slow-feeder-bowl"],
      scene="Three new-routine images in one bright cream palette: a long-haired cat being gently combed with Tame; a doodle being dried with the Breeze dryer after a bath; a dog eating calmly from the Pace slow feeder bowl.",
      caption=f"New year, new routines. 🗓️\n\n1. Tame: a dematting comb that works through knots\n2. Breeze: a grooming dryer with adjustable airflow and heat\n3. Pace: a stainless slow feeder for fast eaters\n\n{COZY15} {LINK}",
      tags=f"{H_PET} #newyearnewyou #petgrooming #slowfeeder #petcare"),
 dict(date="2026-12-31", theme="care_tip", products=["haven-pet-den"],
      scene="A cat calm and safe inside the felt Haven den in a cozy room with curtains closed, soft lamp light, New Year's Eve.",
      caption="Fireworks tonight? Keep them calm. 🎆\n\nStay home with them if you can, close the curtains, play calm music and give them a den to hide in, like Haven. Happy New Year from CozyCompanion. 🤍",
      tags=f"{H_PET} #newyearseve #fireworks #petsafety #calmpets"),
]
STORY = {
 "2026-12-01": "Giving Tuesday", "2026-12-02": "For the good boy", "2026-12-03": "For the real boss",
 "2026-12-04": "Order by Dec 16", "2026-12-05": "Delivered in 3–5 days", "2026-12-06": "Slow Sunday",
 "2026-12-07": "Skip the scraps", "2026-12-08": "Stocking stuffers", "2026-12-09": "Wrapping supervisor",
 "2026-12-10": "Away? Still fed", "2026-12-11": "Their own tree", "2026-12-12": "The Cozy Nap Set",
 "2026-12-13": "Fire on, phone off", "2026-12-14": "Paws first", "2026-12-15": "A seat for everyone",
 "2026-12-16": "Driving home", "2026-12-17": "Give the gift card", "2026-12-18": "Feathers fly",
 "2026-12-19": "Cozy night in", "2026-12-20": "Snow outside", "2026-12-21": "The longest night",
 "2026-12-22": "A quiet retreat", "2026-12-23": "Still lovely", "2026-12-24": "Pajamas on",
 "2026-12-25": "Merry Christmas", "2026-12-26": "Boxing Day mood", "2026-12-27": "New toys, fresh again",
 "2026-12-28": "No more scooping", "2026-12-29": "Dusk walks", "2026-12-30": "New routines",
 "2026-12-31": "Happy New Year",
}
REEL = {
 "2026-12-04": "The dog bounds happily through the fresh snow toward the camera, snowflakes falling softly.",
 "2026-12-18": "The cat leaps and bats the feather wand, lands softly, tail flicking; the tree ornaments stay still.",
 "2026-12-25": "The puppy tugs the plush toy out of the gift box and shakes it playfully, tail wagging.",
}
for c in C:
    c["story_text"] = STORY[c["date"]]
    c["reel"] = REEL.get(c["date"])
    c["look"] = LOOK

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calendar_dec.json")
    old = {c["date"]: c.get("assets") for c in json.load(open(out))} if os.path.exists(out) else {}
    for c in C:
        if old.get(c["date"]): c["assets"] = old[c["date"]]
    json.dump(C, open(out, "w"), indent=1, ensure_ascii=False)
    print(len(C), "posts")
