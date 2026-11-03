"""Render social/calendar.json as a review page (social/kalender_november.html) for the owner's approval."""
import sys, os, json, html, datetime
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, S)
from lib import gql
DEC = len(sys.argv) > 1 and sys.argv[1] == "dec"   # calendar_html.py dec -> December calendar
C = json.load(open(os.path.join(S, "social", "calendar_dec.json" if DEC else "calendar.json")))
MONTH = "December" if DEC else "November"
titles = {}
for c in C:
    for h in c["products"]:
        if h not in titles:
            p = gql('query($h:String!){productByHandle(handle:$h){title}}', {"h": h})["productByHandle"]
            titles[h] = p["title"] if p else h
NL_DAY = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"]
NL_THEME = {"product_spotlight": "Product in de spotlight", "care_tip": "Verzorgingstip", "life_with": "Life with (baasje + dier)",
            "collection_carousel": "Carrousel (3 beelden)", "playful": "Grappig", "gift_idea": "Cadeau-idee", "brand_story": "Merkverhaal",
            "gift_guide": "Cadeaugids (carrousel)"}
SPECIAL = {"2026-11-24": "Thanksgiving-tip", "2026-11-26": "Thanksgiving", "2026-11-27": "Black Friday",
           "2026-11-28": "Small Business Saturday", "2026-11-30": "Cyber Monday",
           "2026-12-01": "Giving Tuesday", "2026-12-05": "Laatste bestelling voor kerst", "2026-12-21": "Winterzonnewende",
           "2026-12-24": "Kerstavond", "2026-12-25": "Kerst", "2026-12-26": "Boxing Day", "2026-12-31": "Oudejaarsavond"}
e = html.escape
cards, week = [], None
for c in C:
    d = datetime.date.fromisoformat(c["date"])
    wk = d.isocalendar()[1]
    if wk != week:
        week = wk; cards.append(f'<h2>Week {wk}</h2>')
    badges = f'<span class="b">{e(NL_THEME[c["theme"]])}</span>'
    if c["date"] in SPECIAL: badges += f'<span class="b hol">{e(SPECIAL[c["date"]])}</span>'
    if c.get("reel"): badges += '<span class="b reel">Reel</span>'
    if "COZY15" in c["caption"]: badges += '<span class="b code">COZY15</span>'
    if c.get("needs_owner_approval"): badges += '<span class="b hol">Akkoord nodig: cadeaubon bestaat nog niet</span>'
    prods = " · ".join(e(titles[h]) for h in c["products"]) or ("CozyCompanion gift card" if c.get("gift_card") else "")
    reel = f'<p class="k">Reel (6–8 sec.)</p><p>{e(c["reel"])}</p>' if c.get("reel") else ""
    a = c.get("assets", {})
    thumbs = "".join(f'<a href="{e(u)}" target="_blank"><img src="{e(u)}" class="t45" alt=""></a>' for u in a.get("feed", []))
    if a.get("story"): thumbs += f'<a href="{e(a["story"])}" target="_blank"><img src="{e(a["story"])}" class="t916" alt=""></a>'
    if a.get("reel"): thumbs += f'<video src="{e(a["reel"])}" class="t916" controls muted playsinline preload="metadata"></video>'
    thumbs = f'<div class="thumbs">{thumbs}</div>' if thumbs else '<p class="todo">Beelden volgen</p>'
    cards.append(f'''<article class="card"><header><div class="date">{NL_DAY[d.weekday()]} {d.day} {"dec" if DEC else "nov"}</div><div>{badges}</div></header>
<p class="prod">{prods}</p>{thumbs}
<div class="grid"><div><p class="k">Beeld (Nano Banana)</p><p>{e(c["scene"])}</p>{reel}
<p class="k">Story</p><p class="story">“{e(c["story_text"])}”</p></div>
<div><p class="k">Caption</p><p class="cap">{e(c["caption"]).replace(chr(10), "<br>")}</p><p class="tags">{e(c["tags"])}</p></div></div></article>''')
page = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Content calendar {MONTH}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant:wght@500;600&family=Jost:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{--char:#1a1a1a;--rose:#b76e79;--cream:#f5f1ed;--sand:#ebe3da}}
body{{margin:0;background:var(--cream);color:var(--char);font-family:Jost,Arial,sans-serif;font-size:15px;line-height:1.5}}
.wrap{{max-width:1000px;margin:0 auto;padding:28px 16px 60px}}
h1{{font-family:Cormorant,serif;font-weight:500;font-size:40px;margin:0}} .sub{{opacity:.75;margin:6px 0 20px}}
.sum{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin-bottom:10px}}
.sum div{{background:#fff;border:1px solid var(--sand);padding:12px 14px}} .sum b{{display:block;font-family:Cormorant,serif;font-size:26px;font-weight:600}}
h2{{font-family:Cormorant,serif;font-weight:500;font-size:28px;margin:34px 0 12px;border-bottom:1px solid var(--sand);padding-bottom:6px}}
.card{{background:#fff;border:1px solid var(--sand);padding:16px 18px;margin-bottom:12px}}
.card header{{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center}}
.date{{font-family:Cormorant,serif;font-size:22px;font-weight:600}}
.b{{display:inline-block;font-size:11px;letter-spacing:.06em;text-transform:uppercase;background:var(--sand);padding:3px 8px;margin:2px 0 2px 4px}}
.b.reel{{background:var(--char);color:var(--cream)}} .b.hol{{background:var(--rose);color:#fff}} .b.code{{background:#e9f1ea;color:#3d6b48}}
.prod{{font-weight:500;margin:6px 0 10px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px}} @media(max-width:700px){{.grid{{grid-template-columns:1fr}}}}
.k{{margin:8px 0 2px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--rose)}} p{{margin:0 0 6px}}
.thumbs{{display:flex;gap:8px;overflow-x:auto;margin:4px 0 12px}} .thumbs img,.thumbs video{{display:block;border:1px solid var(--sand)}}
.t45{{height:250px;aspect-ratio:4/5;object-fit:cover}} .t916{{height:250px;aspect-ratio:9/16;object-fit:cover}} .todo{{font-size:12px;opacity:.6}}
.cap{{background:var(--cream);padding:10px 12px}} .tags{{font-size:12.5px;color:#5b6b8c}} .story{{font-family:Cormorant,serif;font-size:19px}}
</style></head><body><div class="wrap">
<h1>Content calendar · {MONTH} 2026</h1>
<p class="sub">@cozycompanion.usa + Facebook-pagina · elke dag 16:43 NL-tijd (11:43 New York) · alle beelden nieuw met Nano Banana 2.1, video's met Seedance 2.0, elk beeld door de strenge QA-check</p>
<div class="sum"><div><b>29</b>feed-posts</div><div><b>29</b>stories</div><div><b>12</b>Reels</div><div><b>~525</b>credits / maand</div></div>
{"".join(cards)}
</div></body></html>'''
open(os.path.join(S, "social", "kalender_december.html" if DEC else "kalender_november.html"), "w").write(page)
print("ok")
