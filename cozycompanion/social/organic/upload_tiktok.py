"""Upload the rendered TikTok week (social/organic/out/tt/, see build_tiktok.py) to Shopify Files one file at a time and write
social/tiktok_plan.json. Videos -> generic FILE tt_<date>_<slot>; carousel slides -> IMAGE tt_<date>_<slot>_s<n>.
Names already in files.json are skipped, so it is safe to re-run. Nothing is posted."""
import os, sys, json, datetime
from zoneinfo import ZoneInfo
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from upload_week import up_video, up_image

OUT = os.path.join(HERE, "out", "tt")
store = lambda u, img=False: "https://cozycompanion.us/cdn/shop/files/" + u.split("/files/")[-1].split("?")[0] + ("?format=jpg" if img else "")

posts = json.load(open(os.path.join(OUT, "posts.json")))
plan = []
for name in sorted(posts):
    p = posts[name]
    e = {"date": p["date"], "slot": p["slot"], "type": p["type"], "format": p["format"]}
    if p["type"] == "video":
        e["url"] = store(up_video(os.path.join(OUT, p["files"][0]), name, f"CozyCompanion TikTok {p['date']} slot {p['slot']}: {p['format']}"))
    else:
        e["slides"] = [store(up_image(os.path.join(OUT, f), f"{name}_s{i + 1}", f"CozyCompanion TikTok carousel {p['date']} slot {p['slot']} slide {i + 1}"), True)
                       for i, f in enumerate(p["files"])]
        e["url"] = e["slides"][0]
    # slots 4-5 (00:00 / 02:00 NL) are the US evening of `date`, so they fall on the NEXT Amsterdam calendar day
    hh, mm = map(int, p["recommended_post_time_nl"].split(":"))
    nl = datetime.datetime.fromisoformat(p["date"]).replace(hour=hh, minute=mm, tzinfo=ZoneInfo("Europe/Amsterdam"))
    if p["slot"] >= 4: nl += datetime.timedelta(days=1)
    e.update(title=p["title"], description=p["description"], recommended_post_time_nl=p["recommended_post_time_nl"],
             post_at_nl=nl.strftime("%Y-%m-%d %H:%M"), post_at_et=nl.astimezone(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M"))
    plan.append(e); print("ok", name, flush=True)
json.dump(plan, open(os.path.join(S, "social", "tiktok_plan.json"), "w"), indent=1, ensure_ascii=False)
print("plan entries:", len(plan))
