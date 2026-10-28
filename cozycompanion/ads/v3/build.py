"""Collection ads v3: one ad per collection page, each about that page. Writes v3/create_params.json."""
import json
reg = json.load(open("/home/user/Shopify-test/cozycompanion/files.json"))
v2 = json.load(open("/home/user/Shopify-test/cozycompanion/ads/v2/create_params.json"))[0]["creative"]
ADSET = "120246810964710609"
ADS = [
 ("wear-walk", "C1 sorry_wear", "Sorry, not sorry. 🧥\nQuilted jackets, knit hoods, paw boots and hands-free leashes: the Wear & Walk edit has everything for cold-weather walks in one place.\nTake 15% off your first order with code COZY15.",
  "The Wear & Walk edit", "Jackets, boots, harnesses & leashes"),
 ("beds-dens", "C2 nap_sleep", "They're not getting up. 😴\nMemory foam, soft bolsters and deep round nests for the long afternoon nap. Shop the Sleep & Lounge edit: beds, dens and cat trees for dogs and cats.\n15% off your first order with code COZY15.",
  "They're not getting up.", "Beds, dens & cat trees"),
 ("cats", "C3 notes_cats", "She has a list. ✔️\nWindow teasers, designer scratchers, catnip and a cat tree that actually looks good in your living room. It's all in the For Cats edit.\n15% off your first order: COZY15.",
  "Everything she'll claim as hers", "Toys, scratchers, beds & trees"),
 ("groom-clean", "C4 spa_groom", "Spa day, without the appointment. 🛁\nVacuum grooming kits, quiet cordless clippers, nail grinders and hair removers: the Groom & Clean edit keeps coats tidy and hair off your floor.\nTake 15% off your first order with code COZY15.",
  "Spa day. At home.", "Grooming & cleaning essentials"),
 ("smart-feeding", "C5 note_dine", "Dinner, but make it a game. 🐾\nPuzzle feeders, lick mats and treat balls slow down fast eaters and keep busy minds happy. Explore the Dine & Drink edit, from bowls to fountains.\n15% off your first order with code COZY15.",
  "Dinner, slowed down.", "Bowls, feeders & fountains"),
 ("pet-travel", "C6 packed_travel", "Packed for two. 🚙\nCarriers, car booster seats and folding pet stairs for weekend trips with your favorite co-pilot. Shop the Travel edit.\nTracked shipping and 30-day returns. 15% off your first order: COZY15.",
  "Packed for two.", "Carriers, car seats & stairs"),
]
out = []
for handle, name, msg, head, desc in ADS:
    if f"v3f_{handle}" not in reg: continue
    tag = "v3_" + name.split()[1]
    link = f"https://cozycompanion.us/collections/{handle}"
    out.append({"adset_id": ADSET, "name": f"COLLECTIONS | v3 {name}", "status": "active", "creative": {
        "name": tag, "url_tags": f"utm_source=meta&utm_medium=paid&utm_campaign=cc_usa_launch&utm_content={tag}",
        "degrees_of_freedom_spec": v2["degrees_of_freedom_spec"],
        "object_story_spec": {"page_id": "1411553698703314", "link_data": {
            "link": link, "picture": reg[f"v3f_{handle}"]["url"].split("?")[0], "message": msg, "name": head,
            "description": desc, "call_to_action": {"type": "SHOP_NOW", "value": {"link": link}}}}}})
json.dump(out, open("/home/user/Shopify-test/cozycompanion/ads/v3/create_params.json", "w"), indent=1, ensure_ascii=False)
print(len(out), [o["name"] for o in out])
