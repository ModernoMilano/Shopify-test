"""Replace each product's gallery with our own square photos (supplier images removed) and
point variants at the matching photo. Portrait (4:5) shots are cropped to 1:1 first.
Usage: gallery.py"""
import sys, os, io, json, time, ssl, subprocess, urllib.request
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from PIL import Image
from lib import gql, check, DOMAIN

reg = json.load(open(os.path.join(S, "files.json")))
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

GALLERIES = {
    "plush-heat-pad": ["b_pad", "g_hp_colors2", "n_pad_life", "g_hp_shoulders", "g_hp_detail"],
    "heklet-heated-sherpa-throw": ["b_throw", "g_th_detail", "n_throw_life", "g_th_bed", "g_th_flat2"],
    "mitag-duo-smart-tag": ["b_tag", "g_mt_lineup", "g_mt_two2", "n_tag_life", "g_mt_keys"],
    "heated-pet-pad": ["b_petpad", "g_pp_rose", "n_petpad_life", "g_pp_dog", "g_pp_detail"],
    "stainless-steel-pet-fountain": ["b_fountain", "b_fountain4l", "g_ft_detail", "n_fountain_life", "g_ft_dog", "g_ft_parts"],
    "automatic-pet-feeder-4l": ["b_feeder", "b_feederblack", "g_fd_duo", "n_feeder_life", "g_fd_dog", "g_fd_detail"],
}
# variant option value (substring) -> photo shown when that variant is picked
VARIANT_MEDIA = {
    "plush-heat-pad": {"Grey": "b_pad", "Yellow": "g_hp_colors2", "Green": "g_hp_colors2", "Blue": "g_hp_colors2"},
    "heated-pet-pad": {"Rose": "g_pp_rose", "Paws": "b_petpad"},
    "stainless-steel-pet-fountain": {"4L": "b_fountain4l", "2L": "b_fountain"},
    "automatic-pet-feeder-4l": {"White": "b_feeder", "Black": "b_feederblack"},
    "mitag-duo-smart-tag": {"2 black": "g_mt_two2", "brown": "b_tag", "case": "g_mt_lineup", "1 ": "g_mt_two2"},
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
    names = [make_square(n) for n in names]
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
            if key: items.append({"variantId": v["id"], "mediaIds": [reg[make_square(vm[key])]["id"]]})
        if items:
            r = gql("mutation($pid:ID!,$v:[ProductVariantAppendMediaInput!]!){productVariantAppendMedia(productId:$pid,variantMedia:$v){userErrors{field message}}}",
                    {"pid": p["id"], "v": items})["productVariantAppendMedia"]
            if r["userErrors"]: print("   variant media:", r["userErrors"])
    time.sleep(2)
    now = gql("query($h:String!){productByHandle(handle:$h){media(first:100){nodes{id}}}}", {"h": handle})["productByHandle"]["media"]["nodes"]
    print(f"{handle}: {len(now)} photos, exactly ours in order: {[m['id'] for m in now] == want}")
json.dump(reg, open(os.path.join(S, "files.json"), "w"), indent=1)
