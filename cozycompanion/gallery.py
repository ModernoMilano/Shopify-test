"""Replace each product's gallery with our own 2:3 photos (supplier images removed) and
point variants at the matching photo.
Usage: gallery.py [handle ...]   (no handles = all products)"""
import sys, os, io, json, time, ssl, subprocess, urllib.request
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from PIL import Image
from lib import gql, check, DOMAIN

reg = json.load(open(os.path.join(S, "files.json")))
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

GALLERIES = {
    "ember-heat-pad": ["b_pad_23", "g_hp_colors2_23", "n_pad_life_23", "g_hp_shoulders_23", "g_hp_detail_23"],
    "hearth-heated-sherpa-throw": ["b_throw_23b", "g_th_detail_23", "n_throw_life_23", "g_th_bed_23", "g_th_flat2_23"],
    "cloud-plush-pet-blanket": {"Charcoal": "z_cloud_pack", "Mocha": "z_cloud_dog"},
    "nook-self-warming-pet-mat": {"Gray": "z_nook_pack", "Caramel": "z_nook_cat"},
    "purr-tilted-ceramic-cat-bowl": {"Pink": "z_purr_pack", "Black": "z_purr_colors"},
    "orbit-felt-cat-tunnel-bed": {"Charcoal": "z_orbit_pack", "Blush": "z_orbit_colors", "Sky Blue": "z_orbit_colors", "Light Gray": "z_orbit_colors", "Pebble": "z_orbit_colors"},
    "lounge-plush-pet-sofa": {"Cream": "z_lounge_pack", "Blush": "z_lounge_colors", "Mocha": "z_lounge_dog"},
    "compass-smart-tag": ["b_tag_23", "g_mt_lineup_23", "g_mt_two2_23", "n_tag_life_23", "g_mt_keys_23"],
    "nestle-heated-pet-pad": ["b_petpad_23", "g_pp_rose_23", "n_petpad_life_23", "g_pp_dog_23", "g_pp_detail_23c"],
    "brook-pet-fountain": ["b_fountain_23", "b_fountain4l_23", "g_ft_detail_23c", "n_fountain_life_23", "g_ft_dog_23", "g_ft_parts_23"],
    "dine-automatic-feeder": ["b_feeder_23", "b_feederblack_23", "g_fd_duo_23", "n_feeder_life_23", "g_fd_dog_23", "g_fd_detail_23c"],
    "haven-pet-den": ["x_den_pack", "x_den_front", "x_den_dog", "x_den_cat"],
    "halo-self-cleaning-litter-box": ["x_halo_pack", "x_halo_detail", "x_halo_life", "x_halo_bath"],
    "glance-camera-feeder": ["x_glance_white", "x_glance_black", "x_glance_detail", "x_glance_life", "x_glance_blacklife"],
    "murmur-camera-feeder": ["x_murmur_pack", "x_murmur_detail", "x_murmur_life", "x_murmur_kitten"],
    "brook-xl-cordless-fountain": ["x_brookxl_pack", "x_brookxl_filters", "x_brookxl_detail", "x_brookxl_dog", "x_brookxl_cat"],
    "flutter-cat-play-station": ["y_flutter_pack", "y_flutter_detail", "y_flutter_life"],
    "spark-laser-cat-toy": ["y_spark_pack", "y_spark_detail", "y_spark_life"],
    "voyage-rolling-pet-carrier": ["y_voyage_pack", "y_voyage_colors", "y_voyage_life"],
    "roam-back-seat-dog-bed": ["y_roam_hero_c", "y_roam_pack", "y_roam_detail", "y_roam_life"],
    "cloud-plush-pet-blanket": ["z_cloud_pack", "z_cloud_colors", "z_cloud_detail", "z_cloud_cat", "z_cloud_dog"],
    "nook-self-warming-pet-mat": ["z_nook_pack", "z_nook_colors", "z_nook_detail", "z_nook_crate", "z_nook_cat"],
    "purr-tilted-ceramic-cat-bowl": ["z_purr_pack", "z_purr_colors", "z_purr_cat"],
    "orbit-felt-cat-tunnel-bed": ["z_orbit_pack", "z_orbit_colors", "z_orbit_kitten", "z_orbit_sleep"],
    "lounge-plush-pet-sofa": ["z_lounge_pack", "z_lounge_colors", "z_lounge_cat", "z_lounge_dog"],
    "pace-stainless-slow-feeder-bowl": ["z_pace_pack", "z_pace_kibble", "z_pace_dog"],
    "quest-dog-puzzle-feeder": ["z_quest_pack", "z_quest_detail", "z_quest_dog"],
    "stride-dog-harness-leash-set": ["z_stride_pack", "z_stride_walk"],
    "wander-cat-harness-leash": ["z_wander_pack", "z_wander_walk"],
    "flit-flapping-bird-cat-toy": ["z_flit_pack", "z_flit_play"],
    "zoom-self-rolling-cat-ball": ["z_zoom_pack", "z_zoom_play"],
    "plume-feather-teaser-wand": ["z_plume_pack", "z_plume_play"],
    "knot-tug-fetch-ball": ["z_knot_pack", "z_knot_play"],
    "buddy-plush-dog-toy": ["z_buddy_pack", "z_buddy_life"],
    "forage-snuffle-mat": ["z_forage_pack", "z_forage_dog"],
    "knit-small-dog-sweater": ["z_knit_pack", "z_knit_poodle"],
    "drizzle-dog-raincoat": ["z_drizzle_pack", "z_drizzle_walk"],
    "cove-ceramic-cat-bowl": ["z_cove_pack", "z_cove_cat"],
    "chase-plush-prey-cat-toy": ["z_chase_pack", "z_chase_cat"],
    "fetch-automatic-ball-launcher": ["z_fetch_pack", "z_fetch_dog"],
    "glide-soft-dog-frisbee": ["z_glide_pack", "z_glide_dog"],
    "gnaw-dental-chew-toy": ["z_gnaw_pack", "z_gnaw_puppy"],
    "puddle-suspender-dog-boots": ["z_puddle_pack", "z_puddle_walk"],
    "frost-harness-winter-dog-jacket": ["z_frost_pack", "z_frost_snow"],
    "splash-quick-dry-dog-bathrobe": ["z_splash_pack", "z_splash_dog"],
    "snug-sherpa-pet-blanket": ["z_snug_pack", "z_snug_dog"],
    "doze-dog-pajamas": ["z_doze_pack", "z_doze_dog"],
    "tidy-double-bowl-feeder": ["z_tidy_pack", "z_tidy_dog"],
    "riddle-treat-dispensing-ball": ["z_riddle_pack", "z_riddle_dog"],
    "maze-puzzle-feeder-bowl": ["z_maze_pack", "z_maze_dog"],
    "burrow-plush-pet-bed": ["z_burrow_pack", "z_burrow_cat"],
    "fold-magnetic-cat-scratcher": ["z_fold_pack", "z_fold_cat"],
    "chomp-rubber-treat-ball": ["z_chomp_pack", "z_chomp_dog"],
    "pounce-automatic-feather-cat-toy": ["z_pounce_pack", "z_pounce_cat"],
    "chirp-catnip-ball": ["z_chirp_pack", "z_chirp_kitten"],
    "cradle-pet-sling-carrier": ["z_cradle_pack", "z_cradle_walk"],
    "bloom-floral-cat-collar": ["z_bloom_pack", "z_bloom_cat"],
    "mistle-knit-dog-hood": ["z_mistle_pack", "z_mistle_dog"],
    "trail-hands-free-dog-leash": ["z_trail_pack", "z_trail_run"],
    "dapper-gingham-bow-tie": ["z_dapper_pack", "z_dapper_dog"],
    "fin-dog-life-jacket": ["z_fin_pack", "z_fin_swim"],
}
# many colors/breeds and we only shot one: keep the supplier's variant photos after ours
KEEP_VARIANT_PHOTOS = {"stride-dog-harness-leash-set", "zoom-self-rolling-cat-ball", "buddy-plush-dog-toy", "drizzle-dog-raincoat",
                       "chase-plush-prey-cat-toy", "fetch-automatic-ball-launcher", "frost-harness-winter-dog-jacket", "splash-quick-dry-dog-bathrobe",
                       "snug-sherpa-pet-blanket", "doze-dog-pajamas", "tidy-double-bowl-feeder", "riddle-treat-dispensing-ball",
                       "burrow-plush-pet-bed", "chomp-rubber-treat-ball", "pounce-automatic-feather-cat-toy", "chirp-catnip-ball",
                       "cradle-pet-sling-carrier", "trail-hands-free-dog-leash", "fin-dog-life-jacket"}
# variant option value (substring) -> photo shown when that variant is picked
VARIANT_MEDIA = {
    "ember-heat-pad": {"Gray": "b_pad_23", "Yellow": "g_hp_colors2_23", "Green": "g_hp_colors2_23", "Blue": "g_hp_colors2_23"},
    "nestle-heated-pet-pad": {"Rose": "g_pp_rose_23", "Paws": "b_petpad_23"},
    "brook-pet-fountain": {"4L": "b_fountain4l_23", "2L": "b_fountain_23"},
    "dine-automatic-feeder": {"White": "b_feeder_23", "Black": "b_feederblack_23"},
    "glance-camera-feeder": {"White": "x_glance_white", "Black": "x_glance_black"},
    "brook-xl-cordless-fountain": {"only": "x_brookxl_pack", "filters": "x_brookxl_filters"},
    "voyage-rolling-pet-carrier": {"Gray": "y_voyage_pack", "Black": "y_voyage_colors", "Blue": "y_voyage_colors", "Pink": "y_voyage_colors"},
    "cloud-plush-pet-blanket": {"Charcoal": "z_cloud_pack", "Mocha": "z_cloud_dog"},
    "nook-self-warming-pet-mat": {"Gray": "z_nook_pack", "Caramel": "z_nook_cat"},
    "purr-tilted-ceramic-cat-bowl": {"Pink": "z_purr_pack", "Black": "z_purr_colors"},
    "orbit-felt-cat-tunnel-bed": {"Charcoal": "z_orbit_pack", "Blush": "z_orbit_colors", "Sky Blue": "z_orbit_colors", "Light Gray": "z_orbit_colors", "Pebble": "z_orbit_colors"},
    "lounge-plush-pet-sofa": {"Cream": "z_lounge_pack", "Blush": "z_lounge_colors", "Mocha": "z_lounge_dog"},
    "compass-smart-tag": {"2 black": "g_mt_two2_23", "brown": "b_tag_23", "case": "g_mt_lineup_23", "1 ": "g_mt_two2_23"},
}

def fetch(name):
    u = f"https://{DOMAIN}/cdn/shop/files/" + reg[name]["url"].split("/files/")[-1].split("?")[0]
    return Image.open(io.BytesIO(urllib.request.urlopen(u, context=CTX).read())).convert("RGB")

def make_square(name):
    """Return the registry name of a 2000x2000 version of this photo, creating it if needed."""
    w, h = reg[name]["size"]
    if w == h: return name
    sq = name + "_sq"
    if sq in reg and reg[sq].get("url"): return sq
    im = fetch(name); w, h = im.size; side = min(w, h)
    top = int((h - side) * 0.4)   # keep a little more of the top than the bottom
    im = im.crop(((w - side) // 2, top, (w - side) // 2 + side, top + side)).resize((2000, 2000), Image.LANCZOS)
    path = os.path.join(S, f"{sq}.jpg"); im.save(path, quality=92)
    out = subprocess.run([sys.executable, "-I", os.path.join(S, "staged_one.py"), path, sq, reg[name]["alt"]], capture_output=True, text=True)
    if out.returncode: sys.exit(out.stderr)
    os.remove(path)
    reg.update(json.load(open(os.path.join(S, "files.json"))))
    return sq

ONLY = sys.argv[1:]
for handle, names in GALLERIES.items():
    if ONLY and handle not in ONLY: continue
    want = [reg[n]["id"] for n in names]
    p = gql("query($h:String!){productByHandle(handle:$h){id media(first:100){nodes{id}}}}", {"h": handle})["productByHandle"]
    have = [m["id"] for m in p["media"]["nodes"]]
    per_color = {}   # first option value (color/style) -> the one supplier photo we keep for it
    if handle in KEEP_VARIANT_PHOTOS:
        kv = gql("query($h:String!){productByHandle(handle:$h){variants(first:100){nodes{id selectedOptions{value} media(first:1){nodes{id}}}}}}", {"h": handle})["productByHandle"]["variants"]["nodes"]
        for v in kv:
            mid = next(iter(m["id"] for m in v["media"]["nodes"]), None)
            per_color.setdefault(v["selectedOptions"][0]["value"], mid) if mid else None
        want += [m for m in dict.fromkeys(per_color.values()) if m not in want]
    for fid in want:
        if fid not in have:
            check(gql("mutation($f:[FileUpdateInput!]!){fileUpdate(files:$f){userErrors{field message}}}",
                      {"f": [{"id": fid, "referencesToAdd": [p["id"]]}]})["fileUpdate"], handle)
    extra = [m for m in have if m not in want]
    if extra:
        check(gql("mutation($pid:ID!,$m:[ID!]!){productDeleteMedia(productId:$pid,mediaIds:$m){mediaUserErrors{field message}}}",
                  {"pid": p["id"], "m": extra})["productDeleteMedia"] | {"userErrors": []}, handle)
    time.sleep(3)
    check(gql("mutation($id:ID!,$m:[MoveInput!]!){productReorderMedia(id:$id,moves:$m){userErrors{field message}}}",
              {"id": p["id"], "m": [{"id": fid, "newPosition": str(i)} for i, fid in enumerate(want)]})["productReorderMedia"], handle)
    if per_color:   # sizes of the same color all point at that color's one photo
        items = [{"variantId": v["id"], "mediaIds": [per_color[v["selectedOptions"][0]["value"]]]} for v in kv
                 if per_color.get(v["selectedOptions"][0]["value"]) and per_color[v["selectedOptions"][0]["value"]] not in [m["id"] for m in v["media"]["nodes"]]]
        if items:
            r = gql("mutation($pid:ID!,$v:[ProductVariantAppendMediaInput!]!){productVariantAppendMedia(productId:$pid,variantMedia:$v){userErrors{field message}}}",
                    {"pid": p["id"], "v": items})["productVariantAppendMedia"]
            if r["userErrors"]: print("   variant media:", r["userErrors"])
    # variant photos
    vm = VARIANT_MEDIA.get(handle)
    if vm:
        vs = gql("query($h:String!){productByHandle(handle:$h){variants(first:50){nodes{id title}}}}", {"h": handle})["productByHandle"]["variants"]["nodes"]
        items = []
        for v in vs:
            key = next((k for k in vm if k.lower() in v["title"].lower()), None)
            if key: items.append({"variantId": v["id"], "mediaIds": [reg[vm[key]]["id"]]})
        if items:
            r = gql("mutation($pid:ID!,$v:[ProductVariantAppendMediaInput!]!){productVariantAppendMedia(productId:$pid,variantMedia:$v){userErrors{field message}}}",
                    {"pid": p["id"], "v": items})["productVariantAppendMedia"]
            if r["userErrors"]: print("   variant media:", r["userErrors"])
    time.sleep(2)
    now = gql("query($h:String!){productByHandle(handle:$h){media(first:100){nodes{id}}}}", {"h": handle})["productByHandle"]["media"]["nodes"]
    print(f"{handle}: {len(now)} photos, exactly ours in order: {[m['id'] for m in now] == want}")
json.dump(reg, open(os.path.join(S, "files.json"), "w"), indent=1)
