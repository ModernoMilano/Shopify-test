"""Make every scheduled reel Instagram-proof (2026-11-06: Instagram rejected r_2026-11-06_v2 with container status ERROR).
The Seedance MP4s have the moov atom at the END (no fast start) and 32 kHz audio. Re-mux: video stream copied unchanged,
audio AAC 48 kHz 128k, +faststart. Uploaded as a generic FILE named <old>_ig; every reference in social/calendar.json,
social/calendar_dec.json, bfcm/social_plan.json and bfcm/assets.json is switched to the new URL."""
import os, sys, json, re, time, subprocess, urllib.request, ssl
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, S)
from lib import gql, check, DOMAIN
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
TMP = os.path.join(S, "social", ".tmp", "ig"); os.makedirs(TMP, exist_ok=True)
SRC = ["social/calendar.json", "social/calendar_dec.json", "bfcm/social_plan.json", "bfcm/assets.json"]
urls = set()
for f in SRC:
    urls |= set(re.findall(r"https://cdn\.shopify\.com/[^\"]+?\.mp4", open(os.path.join(S, f)).read()))
reg = json.load(open(os.path.join(S, "files.json")))
mapping = {}
for u in sorted(urls):
    name = u.split("/files/")[-1].split("?")[0]            # cozycompanion-r_2026-11-06_v2.mp4
    if name.endswith("_ig.mp4"): continue
    base = name[len("cozycompanion-"):-4] + "_ig"
    if base in reg:
        mapping[u] = reg[base]["url"].split("?")[0]; print("have", base); continue
    src, dst = os.path.join(TMP, name), os.path.join(TMP, base + ".mp4")
    open(src, "wb").write(urllib.request.urlopen(f"https://{DOMAIN}/cdn/shop/files/{name}", context=CTX).read())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-c:v", "copy", "-c:a", "aac", "-ar", "48000", "-b:a", "128k",
                    "-movflags", "+faststart", dst], check=True)
    fn = f"cozycompanion-{base}.mp4"
    t = check(gql("""mutation($i:[StagedUploadInput!]!){stagedUploadsCreate(input:$i){stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}""",
                  {"i": [{"filename": fn, "mimeType": "video/mp4", "httpMethod": "POST", "resource": "FILE", "fileSize": str(os.path.getsize(dst))}]})["stagedUploadsCreate"])["stagedTargets"][0]
    args = ["curl", "-sS", "-f", "-X", "POST", t["url"]]
    for p in t["parameters"]: args += ["-F", f"{p['name']}={p['value']}"]
    subprocess.run(args + ["-F", f"file=@{dst};type=video/mp4"], check=True, capture_output=True)
    fid = check(gql("""mutation($f:[FileCreateInput!]!){fileCreate(files:$f){files{id} userErrors{field message}}}""",
                    {"f": [{"originalSource": t["resourceUrl"], "contentType": "FILE", "filename": fn, "alt": f"CozyCompanion reel {base}"}]})["fileCreate"])["files"][0]["id"]
    for _ in range(60):
        n = gql("query($id:ID!){node(id:$id){... on GenericFile{fileStatus url}}}", {"id": fid})["node"]
        if n["fileStatus"] in ("READY", "FAILED"): break
        time.sleep(3)
    if n["fileStatus"] != "READY": sys.exit(f"{base}: {n['fileStatus']}")
    reg[base] = {"id": fid, "url": n["url"], "alt": f"CozyCompanion reel {base}"}
    json.dump(reg, open(os.path.join(S, "files.json"), "w"), indent=1)
    mapping[u] = n["url"].split("?")[0]; print("uploaded", base)
for f in SRC:
    p = os.path.join(S, f); s = open(p).read(); s2 = s
    for a, b in mapping.items(): s2 = s2.replace(a, b)
    if s2 != s: open(p, "w").write(s2); print("updated", f)
print("reels fixed:", len(mapping))
