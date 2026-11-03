"""Bring finished Nano Banana results into Shopify Files and build the feed (4:5) / story (9:16) versions for QA.
  process.py <plan_index> <result_url> [attempt]   -> results.json[key] = {url, preview, raw, attempt, qa: "pending"}
  process.py --accept key[,key...]                 -> marks pass and writes the assets into social/calendar_dec.json
  process.py --reject key[,key...]                 -> marks fail (kept out of the calendar)
Run strictly one at a time (files.json has a single writer)."""
import json, os, sys, subprocess
D = os.path.dirname(os.path.abspath(__file__)); SOC = os.path.dirname(D); S = os.path.dirname(SOC)
sys.path.insert(0, SOC); sys.path.insert(0, S)
R = os.path.join(D, "results.json")
res = json.load(open(R)) if os.path.exists(R) else {}
P = json.load(open(os.path.join(D, "plan.json")))
CAL = os.path.join(SOC, "calendar_dec.json")

def save(): json.dump(res, open(R, "w"), indent=1)

if sys.argv[1] in ("--accept", "--reject"):
    keys = sys.argv[2].split(",")
    for k in keys: res[k]["qa"] = "pass" if sys.argv[1] == "--accept" else "fail"
    save()
    if sys.argv[1] == "--accept":
        cal = json.load(open(CAL))
        for c in cal:
            d = c["date"]; a = c.setdefault("assets", {})
            feed = sorted([(v["n"], v["url"]) for k, v in res.items() if v["qa"] == "pass" and v["date"] == d and v["kind"] == "feed"])
            if feed: a["feed"] = [u for _, u in feed]
            st = [v for k, v in res.items() if v["qa"] == "pass" and v["date"] == d and v["kind"] == "story"]
            if st: a["story"] = st[0]["url"]; a["story_raw"] = st[0].get("raw")
        json.dump(cal, open(CAL, "w"), indent=1, ensure_ascii=False)
    print("ok", sys.argv[1], keys); sys.exit()

import social_post as sp
i, url = int(sys.argv[1]), sys.argv[2]; att = int(sys.argv[3]) if len(sys.argv) > 3 else 1
p = P[i]; key = p["key"]; name = key if att == 1 else f"{key}_v{att}"
if p["kind"] == "feed":
    out = sp.finish(url, name)
else:
    text = next(c["story_text"] for c in json.load(open(CAL)) if c["date"] == p["date"])
    out = sp.story(url, name, text)
raw = sp.reg()[f"{name}_raw"]["url"].split("?")[0]
res[key] = {"date": p["date"], "kind": p["kind"], "n": p["n"], "url": out["public_url"], "preview": out["preview"], "raw": raw,
            "attempt": att, "qa": "pending"}
save(); print(key, out["preview"])
