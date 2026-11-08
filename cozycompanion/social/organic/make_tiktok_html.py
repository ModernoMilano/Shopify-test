"""social/tiktok_week.html: Dutch, mobile-friendly review page for the TikTok week (reads social/tiktok_plan.json)."""
import os, json, html, datetime
S = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
plan = json.load(open(os.path.join(S, "social", "tiktok_plan.json")))
DAYS = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"]
KIND = {"Interaction": "Interactie", "Product": "Product", "POV": "POV (herkenbaar)", "Cozy aesthetic": "Sfeer", "List": "Tips",
        "Stitch bait": "Stitch-uitnodiging", "Quiz": "Quiz met aftellen", "Carousel": "Fotocarrousel"}
WHY = {"Interaction": "Vraagt in de eerste seconde om een keuze of cijfer: reageren kost één tik, dus veel comments.",
       "Product": "Eén product in gebruik, met feiten uit de productpagina en de vraag of hun huisdier het zou gebruiken.",
       "POV": "Herkenbaar en grappig: mensen taggen vrienden met precies zo'n huisdier (bereik naar nieuwe mensen).",
       "Cozy aesthetic": "Rustig en mooi: wordt bewaard en vaak opnieuw bekeken (kijktijd), zonder te verkopen.",
       "List": "Nuttige tips worden bewaard en gedeeld; bewaren telt zwaar mee bij TikTok.",
       "Stitch bait": "Nodigt uit om onze video te 'stitchen' met hun eigen huisdier: elke stitch toont ons account aan hun volgers.",
       "Quiz": "Aftellen en een onthulling houden mensen tot het einde kijken; daarna raden ze in de comments.",
       "Carousel": "Fotomodus: mensen swipen door alle foto's (kijktijd) en reageren met een nummer of keuze."}
e = html.escape
when = lambda t, d: f"{t}" + (f" <small>(nacht na {d.day} nov)</small>" if t in ("00:00", "02:00") else "")
cards, n_v, n_p = [], 0, 0
for day in sorted({p["date"] for p in plan}):
    d = datetime.date.fromisoformat(day); rows = []
    for p in sorted((p for p in plan if p["date"] == day), key=lambda p: p["slot"]):
        kind = p["format"].split(" · ")[0]; sub = p["format"].split(" · ", 1)[1]
        if p["type"] == "video":
            n_v += 1
            media = f'<video class="vid" controls playsinline preload="metadata" src="{p["url"]}"></video>'
        else:
            n_p += 1
            media = '<div class="row">' + "".join(f'<a href="{u}" target="_blank"><img loading="lazy" src="{u}&width=540" alt="slide {i + 1}"></a>'
                                                  for i, u in enumerate(p["slides"])) + f'</div><p class="hint">{len(p["slides"])} foto\'s · swipe →</p>'
        rows.append(f'''<div class="post"><div class="meta"><span class="t">{when(p["recommended_post_time_nl"], d)}</span>
<span class="b {"v" if p["type"] == "video" else "p"}">{"Video" if p["type"] == "video" else "Foto's"}</span><span class="b">{KIND.get(kind, kind)}</span>
<div class="sub">{e(sub)}</div></div>{media}
<p class="k">Waarom</p><p>{WHY.get(kind, "")}</p>
<p class="k">Titel</p><div class="cap">{e(p["title"])}</div>
<p class="k">Beschrijving <button onclick="navigator.clipboard.writeText(this.parentNode.nextElementSibling.innerText)">kopieer</button></p>
<div class="cap">{e(p["description"]).replace(chr(10), "<br>")}</div></div>''')
    cards.append(f'<section class="day"><h2>{DAYS[d.weekday()]} {d.day} november</h2><div class="posts">{"".join(rows)}</div></section>')
page = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TikTok-week 9–15 nov</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant:wght@500;600&family=Jost:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{--char:#1a1a1a;--rose:#b76e79;--cream:#f5f1ed;--sand:#ebe3da}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--cream);color:var(--char);font-family:Jost,Arial,sans-serif;font-size:15px;line-height:1.5}}
.wrap{{max-width:1180px;margin:0 auto;padding:28px 16px 60px}}
h1{{font-family:Cormorant,serif;font-weight:500;font-size:38px;margin:0;line-height:1.1}} .lead{{opacity:.8;margin:8px 0 18px}}
h2{{font-family:Cormorant,serif;font-weight:600;font-size:28px;margin:30px 0 10px}}
.sum{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}}
.sum div{{background:#fff;border:1px solid var(--sand);padding:12px 14px}} .sum b{{display:block;font-family:Cormorant,serif;font-size:26px;font-weight:600}}
.note{{background:#fff;border-left:3px solid var(--rose);padding:12px 16px;margin:16px 0}} .note li{{margin:3px 0}}
.posts{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}}
.post{{background:#fff;border:1px solid var(--sand);padding:14px;min-width:0}}
.meta{{margin-bottom:8px}} .t{{font-family:Cormorant,serif;font-size:22px;font-weight:600;margin-right:6px}} .t small{{font-family:Jost;font-size:12px;opacity:.7;font-weight:400}}
.sub{{font-size:13px;opacity:.8;margin-top:2px}}
.b{{display:inline-block;font-size:11px;letter-spacing:.06em;text-transform:uppercase;background:var(--sand);padding:3px 8px;margin:2px 4px 2px 0}}
.b.v{{background:var(--char);color:var(--cream)}} .b.p{{background:var(--rose);color:#fff}}
.vid{{width:100%;max-width:300px;aspect-ratio:9/16;background:#000;display:block;margin:0 auto}}
.row{{display:flex;gap:6px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;padding-bottom:4px}}
.row a{{flex:0 0 72%;max-width:240px;scroll-snap-align:start}} .row img{{width:100%;aspect-ratio:9/16;object-fit:cover;display:block;border:1px solid var(--sand)}}
.hint{{font-size:12px;opacity:.65;margin:4px 0 0}}
.k{{margin:10px 0 3px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--rose)}} p{{margin:0 0 6px}}
.k button{{font:inherit;font-size:10px;letter-spacing:.1em;border:1px solid var(--rose);background:none;color:var(--rose);padding:1px 6px;margin-left:6px;cursor:pointer}}
.cap{{background:var(--cream);padding:9px 11px;font-size:13.5px;overflow-wrap:anywhere}}
</style></head><body><div class="wrap">
<h1>TikTok-week · 9–15 november</h1>
<p class="lead">5 posts per dag op @cozycompanion.us: een mix van video's, fotocarrousels en interactie. Alles gemaakt van bestaande, goedgekeurde beelden (0 credits). Nog niets gepost.</p>
<div class="sum"><div><b>{len(plan)}</b>posts</div><div><b>{n_v}</b>video's</div><div><b>{n_p}</b>fotocarrousels</div><div><b>5</b>per dag</div><div><b>0</b>credits</div></div>
<div class="note"><b>Zo posten we</b><ul>
<li>Tijden zijn Nederlandse tijd: 15:00, 18:00, 21:00, 00:00 en 02:00 (= 9:00, 12:00, 15:00, 18:00 en 20:00 in New York, wanneer Amerikanen scrollen).</li>
<li>TikTok laat elke post pas live gaan als jij op <b>Post</b> tikt in het formulier dat ik klaarzet. Je kunt ook een dag in één keer als concept (drafts) laten klaarzetten en ze zelf inplannen in de TikTok-app.</li>
<li>Kies in het formulier een trending geluid (de video's hebben alleen een rustige achtergrond) en zet het label <b>AI-gegenereerd</b> en <b>Je merk</b> aan.</li>
<li>Geen prijzen, geen reviews, geen kortingscodes. Elke post vraagt om één actie: een nummer, een kant kiezen, stitchen of bewaren.</li>
<li>Reageer het eerste uur op comments (met een vraag terug): dat is de grootste duw voor bereik.</li></ul></div>
{"".join(cards)}
</div></body></html>'''
open(os.path.join(S, "social", "tiktok_week.html"), "w").write(page)
print("written social/tiktok_week.html")
