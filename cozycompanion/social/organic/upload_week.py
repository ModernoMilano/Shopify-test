"""Upload the rendered sample week (social/organic/out/) to Shopify Files, one file at a time, and write social/organic_plan.json.
Reels -> generic FILE org_reel_<date>; stories -> IMAGE org_st_<date>_<am|mid|pm>; Facebook stills -> IMAGE org_still_<date>.
Already-registered names in files.json are skipped, so it is safe to re-run. Nothing is posted."""
import os, sys, json, time, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, S)
from lib import gql, check
OUT = os.path.join(HERE, "out"); REG = os.path.join(S, "files.json")
sys.path.insert(0, HERE)

def reg(): return json.load(open(REG))

def up_image(path, name, alt):
    if name not in reg():
        subprocess.run([sys.executable, os.path.join(S, "staged_one.py"), path, name, alt], check=True)
    return reg()[name]["url"].split("?")[0]

def up_video(path, name, alt):
    r = reg()
    if name in r: return r[name]["url"].split("?")[0]
    fn = f"cozycompanion-{name}.mp4"
    t = check(gql("""mutation($i:[StagedUploadInput!]!){stagedUploadsCreate(input:$i){stagedTargets{url resourceUrl parameters{name value}} userErrors{field message}}}""",
                  {"i": [{"filename": fn, "mimeType": "video/mp4", "httpMethod": "POST", "resource": "FILE", "fileSize": str(os.path.getsize(path))}]})["stagedUploadsCreate"])["stagedTargets"][0]
    args = ["curl", "-sS", "-f", "-o", "/dev/null", "-X", "POST", t["url"]]
    for p in t["parameters"]: args += ["-F", f"{p['name']}={p['value']}"]
    subprocess.run(args + ["-F", f"file=@{path};type=video/mp4"], check=True)
    fid = check(gql("""mutation($f:[FileCreateInput!]!){fileCreate(files:$f){files{id} userErrors{field message}}}""",
                    {"f": [{"originalSource": t["resourceUrl"], "contentType": "FILE", "filename": fn, "alt": alt}]})["fileCreate"])["files"][0]["id"]
    for _ in range(60):
        n = gql("query($id:ID!){node(id:$id){... on GenericFile{fileStatus url}}}", {"id": fid})["node"]
        if n["fileStatus"] in ("READY", "FAILED"): break
        time.sleep(3)
    if n["fileStatus"] != "READY": sys.exit(f"{name}: {n['fileStatus']}")
    r = reg(); r[name] = {"id": fid, "url": n["url"], "alt": alt}; json.dump(r, open(REG, "w"), indent=1)
    print(name, "uploaded"); return n["url"].split("?")[0]

if __name__ == "__main__":
    from build_week import STORIES
    STORY_TYPE = {"q": "question", "rate": "rate", "lr": "this_or_that"}
    caps = json.load(open(os.path.join(OUT, "captions.json")))
    plan = []
    for day in sorted(caps):
        c = caps[day]
        v = up_video(os.path.join(OUT, f"org_reel_{day}.mp4"), f"org_reel_{day}", f"CozyCompanion interaction reel {day}: {c['format']}")
        still = up_image(os.path.join(OUT, f"org_still_{day}.jpg"), f"org_still_{day}", f"CozyCompanion {c['format']} post {day}")
        plan.append({"date": day, "slot": "int", "type": "reel", "url": v, "instagram_caption": c["ig"], "facebook_caption": c["fb"],
                     "facebook_image": still, "format": c["format"]})
        for slot, it in zip(("am", "mid", "pm"), STORIES[day]):
            name = f"org_st_{day}_{slot}"
            u = up_image(os.path.join(OUT, name + ".jpg"), name, f"CozyCompanion {STORY_TYPE[it[0]]} story {day}")
            prompt = it[3] if it[0] == "q" else it[2]
            plan.append({"date": day, "slot": f"st_{slot}", "type": "story", "url": u, "instagram_caption": "", "facebook_caption": "",
                         "facebook_image": None, "format": STORY_TYPE[it[0]], "prompt": prompt})
    json.dump(plan, open(os.path.join(S, "social", "organic_plan.json"), "w"), indent=1, ensure_ascii=False)
    print("plan entries:", len(plan))
