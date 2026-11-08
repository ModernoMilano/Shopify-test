"""social/organic_week.html: Dutch review page for the interactive sample week (reads social/organic_plan.json)."""
import os, json, html, datetime
S = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
plan = json.load(open(os.path.join(S, "social", "organic_plan.json")))
DAYS = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"]
NL_FMT = {"This or that": "Dit of dat", "Rate this nap": "Geef een cijfer", "POV": "POV (herkenbaar)", "Which one is your pet": "Welke is jouw huisdier?",
          "Caption this": "Bedenk een caption", "Guess": "Raad het product", "Team dog or team cat": "Team hond of team kat"}
ST_NL = {"question": "Vraag", "rate": "Cijfer 1–10", "this_or_that": "Links of rechts"}
WHY = {"This or that": "Iedereen heeft een mening: 1 of 2 typen kost één seconde, dus veel reacties.",
       "Rate this nap": "Cijfers geven is laagdrempelig; mensen reageren om het 'eerlijke' cijfer te geven.",
       "POV": "Herkenbaar en grappig: mensen taggen een vriend die precies dit heeft (bereik naar nieuwe accounts).",
       "Which one is your pet": "Mensen herkennen hun eigen dier en reageren met een nummer, vaak met een verhaal erbij.",
       "Caption this": "Een wedstrijdje (beste caption in onze story) geeft lange, grappige reacties.",
       "Guess": "Nieuwsgierigheid houdt mensen tot het einde kijken (kijktijd) en de onthulling laat een product zien zonder te verkopen.",
       "Team dog or team cat": "De klassieker: iedereen kiest kant, ook mensen zonder huisdier."}
e = html.escape
cards = []
for day in sorted({p["date"] for p in plan}):
    d = datetime.date.fromisoformat(day); items = [p for p in plan if p["date"] == day]
    r = next(p for p in items if p["slot"] == "int"); st = [p for p in items if p["type"] == "story"]
    stories = "".join(f'<figure><a href="{p["url"]}" target="_blank"><img class="t916" loading="lazy" src="{p["url"]}?width=400" alt=""></a>'
                      f'<figcaption><b>{["Ochtend", "Middag", "Avond"][i]}</b> · {ST_NL[p["format"]]}<br>{e(p["prompt"])}</figcaption></figure>' for i, p in enumerate(st))
    cards.append(f'''<article class="card"><header><div class="date">{DAYS[d.weekday()]} {d.day} nov</div><div><span class="b reel">Reel</span><span class="b">{NL_FMT[r["format"]]}</span></div></header>
<div class="grid"><div><video class="vid" controls playsinline preload="metadata" poster="{r["facebook_image"]}?width=540" src="{r["url"]}"></video></div>
<div><p class="k">Waarom dit werkt</p><p>{WHY[r["format"]]}</p>
<p class="k">Instagram-caption</p><div class="cap">{e(r["instagram_caption"]).replace(chr(10), "<br>")}</div>
<p class="k">Facebook-tekst (met stilstaand beeld)</p><div class="cap">{e(r["facebook_caption"])}</div></div></div>
<p class="k">3 stories (antwoord via DM)</p><div class="thumbs">{stories}</div></article>''')
page = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Interactieweek 9–15 nov</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant:wght@500;600&family=Jost:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{--char:#1a1a1a;--rose:#b76e79;--cream:#f5f1ed;--sand:#ebe3da}}
body{{margin:0;background:var(--cream);color:var(--char);font-family:Jost,Arial,sans-serif;font-size:15px;line-height:1.5}}
.wrap{{max-width:1000px;margin:0 auto;padding:28px 16px 60px}}
h1{{font-family:Cormorant,serif;font-weight:500;font-size:38px;margin:0;line-height:1.1}} .sub{{opacity:.75;margin:8px 0 18px}}
.sum{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:8px}}
.sum div{{background:#fff;border:1px solid var(--sand);padding:12px 14px}} .sum b{{display:block;font-family:Cormorant,serif;font-size:26px;font-weight:600}}
.note{{background:#fff;border-left:3px solid var(--rose);padding:12px 14px;margin:14px 0 22px}} .note li{{margin:3px 0}}
.card{{background:#fff;border:1px solid var(--sand);padding:16px 18px;margin-bottom:14px}}
.card header{{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:10px}}
.date{{font-family:Cormorant,serif;font-size:24px;font-weight:600}}
.b{{display:inline-block;font-size:11px;letter-spacing:.06em;text-transform:uppercase;background:var(--sand);padding:3px 8px;margin:2px 0 2px 4px}}
.b.reel{{background:var(--char);color:var(--cream)}}
.grid{{display:grid;grid-template-columns:300px 1fr;gap:20px}} @media(max-width:700px){{.grid{{grid-template-columns:1fr}}}}
.vid{{width:100%;max-width:300px;aspect-ratio:9/16;background:#000;display:block;margin:0 auto}}
.k{{margin:10px 0 3px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--rose)}} p{{margin:0 0 6px}}
.cap{{background:var(--cream);padding:10px 12px;font-size:14px}}
.thumbs{{display:flex;gap:10px;overflow-x:auto;padding-bottom:6px}} figure{{margin:0;flex:0 0 150px}} figcaption{{font-size:12.5px;margin-top:4px;line-height:1.35}}
.t916{{width:150px;aspect-ratio:9/16;object-fit:cover;display:block;border:1px solid var(--sand)}}
</style></head><body><div class="wrap">
<h1>Interactieweek · 9–15 november</h1>
<p class="sub">Proefweek om organisch te groeien: elke dag één extra Reel die vraagt om een reactie (21:13 NL-tijd / 15:13 New York) plus 3 stories die om een antwoord vragen. Nog niets gepost: dit is ter goedkeuring.</p>
<div class="sum"><div><b>7</b>interactie-Reels</div><div><b>21</b>vraag-stories</div><div><b>0</b>credits (bestaande beelden)</div><div><b>7</b>formats</div></div>
<div class="note"><b>Hoe het werkt</b><ul>
<li>Elke Reel stelt in de eerste seconde een vraag en eindigt met een duidelijke opdracht ("Comment 1 or 2 👇"). Reacties en shares laten Instagram de video aan meer mensen tonen.</li>
<li>Stickers (poll, slider) kunnen niet via de koppeling, daarom vragen de stories om een antwoord via DM: ook dat telt voor het algoritme.</li>
<li>Geen prijzen, geen reviews, geen korting: het gaat puur om interactie. De gewone dagelijkse post blijft gewoon doorlopen.</li>
<li>Het werkt alleen als we snel terugreageren op elke comment en DM (het liefst binnen het eerste uur).</li></ul></div>
{"".join(cards)}
</div></body></html>'''
open(os.path.join(S, "social", "organic_week.html"), "w").write(page)
print("written social/organic_week.html")
