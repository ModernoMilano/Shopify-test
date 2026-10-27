import sys, os, json, time, subprocess
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
paths = sys.argv[1:]
r = check(gql("""mutation($i:[StagedUploadInput!]!){stagedUploadsCreate(input:$i){stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}""",
    {"i": [{"filename": os.path.basename(p), "mimeType": "image/png", "httpMethod": "POST", "resource": "IMAGE",
            "fileSize": str(os.path.getsize(p))} for p in paths]})["stagedUploadsCreate"])
srcs = []
for p, t in zip(paths, r["stagedTargets"]):
    cmd = ["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", t["url"]]
    for prm in t["parameters"]: cmd += ["-F", f"{prm['name']}={prm['value']}"]
    cmd += ["-F", f"file=@{p}"]
    code = subprocess.run(cmd, capture_output=True, text=True); print(os.path.basename(p), "upload http", code.stdout, code.stderr[:200])
    srcs.append(t["resourceUrl"])
f = check(gql("""mutation($f:[FileCreateInput!]!){fileCreate(files:$f){files{id} userErrors{field message}}}""",
    {"f": [{"originalSource": s, "contentType": "IMAGE", "alt": "CozyCompanion logo", "filename": "cozycompanion-" + os.path.basename(p)} for p, s in zip(paths, srcs)]})["fileCreate"])
ids = [x["id"] for x in f["files"]]
for _ in range(20):
    nodes = gql("query($ids:[ID!]!){nodes(ids:$ids){... on MediaImage{fileStatus image{url}}}}", {"ids": ids})["nodes"]
    if all(n["fileStatus"] in ("READY", "FAILED") for n in nodes): break
    time.sleep(3)
for p, n in zip(paths, nodes): print(os.path.basename(p), n["fileStatus"], (n.get("image") or {}).get("url"))
