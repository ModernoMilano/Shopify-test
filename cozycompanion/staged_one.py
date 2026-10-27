"""Upload one local image to Shopify Files and record it in files.json. Usage: staged_one.py <path> <name> <alt>"""
import sys, os, json, time, subprocess, mimetypes
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
path, name, alt = sys.argv[1:4]
mime = mimetypes.guess_type(path)[0] or "image/jpeg"
t = check(gql("""mutation($i:[StagedUploadInput!]!){stagedUploadsCreate(input:$i){stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}""",
    {"i": [{"filename": f"cozycompanion-{name}{os.path.splitext(path)[1]}", "mimeType": mime, "httpMethod": "POST", "resource": "IMAGE",
            "fileSize": str(os.path.getsize(path))}]})["stagedUploadsCreate"])["stagedTargets"][0]
cmd = ["curl", "-sS", "-f", "-o", "/dev/null", "-X", "POST", t["url"]]
for p in t["parameters"]: cmd += ["-F", f"{p['name']}={p['value']}"]
subprocess.run(cmd + ["-F", f"file=@{path}"], check=True)
fid = check(gql("mutation($f:[FileCreateInput!]!){fileCreate(files:$f){files{id} userErrors{field message}}}",
    {"f": [{"originalSource": t["resourceUrl"], "contentType": "IMAGE", "alt": alt, "filename": f"cozycompanion-{name}{os.path.splitext(path)[1]}"}]})["fileCreate"])["files"][0]["id"]
for _ in range(30):
    n = gql("query($id:ID!){node(id:$id){... on MediaImage{fileStatus image{url width height}}}}", {"id": fid})["node"]
    if n["fileStatus"] in ("READY", "FAILED"): break
    time.sleep(2)
if n["fileStatus"] != "READY": sys.exit(f"upload failed: {name}")
reg_path = os.path.join(S, "files.json"); reg = json.load(open(reg_path))
reg[name] = {"id": fid, "alt": alt, "url": n["image"]["url"], "size": [n["image"]["width"], n["image"]["height"]]}
json.dump(reg, open(reg_path, "w"), indent=1)
print(name, reg[name]["size"])
