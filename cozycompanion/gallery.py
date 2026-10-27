"""Replace each product's gallery with our own 2:3 photos (supplier images removed) and
point variants at the matching photo.
Usage: gallery.py"""
import sys, os, io, json, time, ssl, subprocess, urllib.request
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from PIL import Image
from lib import gql, check, DOMAIN

reg = json.load(open(os.path.join(S, "files.json")))
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

GALLERIES = {
    "ember-heat-pad": ["b_pad_23", "g_hp_colors2_23", "n_pad_life_23", "g_hp_shoulders_23", "g_hp_detail_23"],
    "hearth-heated-sherpa-throw": ["b_throw_23b", "g_th_detail_23", "n_throw_life_23", "g_th_bed_23", "g_th_flat2_23"],
    "compass-smart-tag": ["b_tag_23", "g_mt_lineup_23", "g_mt_two2_23", "n_tag_life_23", "g_mt_keys_23"],
    "nestle-heated-pet-pad": ["b_petpad_23", "g_pp_rose_23", "n_petpad_life_23", "g_pp_dog_23", "g_pp_detail_23c"],
    "brook-pet-fountain": ["b_fountain_23", "b_fountain4l_23", "g_ft_detail_23c", "n_fountain_life_23", "g_ft_dog_23", "g_ft_parts_23"],
    "dine-automatic-feeder": ["b_feeder_23", "b_feederblack_23", "g_fd_duo_23", "n_feeder_life_23", "g_fd_dog_23", "g_fd_detail_23c"],
    "haven-pet-den": ["x_den_pack", "x_den_front", "x_den_dog", "x_den_cat"],
    "halo-self-cleaning-litter-box": ["x_halo_pack", "x_halo_detail", "x_halo_life", "x_halo_bath"],
    "glance-camera-feeder": ["x_glance_white", "x_glance_black", "x_glance_detail", "x_glance_life", "x_glance_blacklife"],
    "murmur-camera-feeder": ["x_murmur_pack", "x_murmur_detail", "x_murmur_life", "x_murmur_kitten"],
    "brook-xl-cordless-fountain": ["x_brookxl_pack", "x_brookxl_filters", "x_brookxl_detail", "x_brookxl_dog", "x_brookxl_cat"],
}
# variant option value (substring) -> photo shown when that variant is picked
VARIANT_MEDIA = {
    "ember-heat-pad": {"Grey": "b_pad_23", "Yellow": "g_hp_colors2_23", "Green": "g_hp_colors2_23", "Blue": "g_hp_colors2_23"},
    "nestle-heated-pet-pad": {"Rose": "g_pp_rose_23", "Paws": "b_petpad_23"},
    "brook-pet-fountain": {"4L": "b_fountain4l_23", "2L": "b_fountain_23"},
    "dine-automatic-feeder": {"White": "b_feeder_23", "Black": "b_feederblack_23"},
    "glance-camera-feeder": {"White": "x_glance_white", "Black": "x_glance_black"},
    "brook-xl-cordless-fountain": {"only": "x_brookxl_pack", "filters": "x_brookxl_filters"},
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

for handle, names in GALLERIES.items():
    want = [reg[n]["id"] for n in names]
    p = gql("query($h:String!){productByHandle(handle:$h){id media(first:100){nodes{id}}}}", {"h": handle})["productByHandle"]
    have = [m["id"] for m in p["media"]["nodes"]]
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
