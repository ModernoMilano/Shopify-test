"""Builds bfcm/overzicht.html (owner review page, Dutch UI) from bfcm/assets.json and bfcm/social_plan.json."""
import os, json, html, datetime
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(open(os.path.join(S, "bfcm", "assets.json")))
PLAN = json.load(open(os.path.join(S, "bfcm", "social_plan.json")))
E = html.escape
DAYS = ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"]
SLOT = {"am": "ochtend", "mid": "middag", "pm": "avond"}
TYPE = {"image": "Foto", "carousel": "Carrousel", "reel": "Reel"}

def media(u, cls=""):
    if u.endswith(".mp4"):
        return f'<video class="{cls}" src="{E(u)}" controls muted playsinline preload="metadata"></video>'
    return f'<a href="{E(u)}" target="_blank" rel="noopener"><img class="{cls}" src="{E(u)}" loading="lazy" alt=""></a>'

def nl_date(d):
    dt = datetime.date.fromisoformat(d); return f"{DAYS[dt.weekday()]} {dt.day} november"

def phase(d):
    return "Teaser" if d < "2026-11-23" else "Cyber Monday" if d == "2026-11-30" else "Black Friday" if d == "2026-11-27" else "Thanksgiving" if d == "2026-11-26" else "Black Friday Week"

a = A["assets"]
web = "".join(f'<figure>{media(a[k]["clean"], "w")}<figcaption>{t}</figcaption></figure>' for k, t in
              (("W1", "Homepage-banner desktop (16:9). De tekst komt er in het thema overheen, links."),
               ("W2", "Homepage-banner mobiel (4:5). Tekst bovenin."),
               ("W3", "Banner collectie “The Black Friday Edit” (21:9). Tekst in het midden.")))
ads = ""
for k, name in (("A1", "Nestle · “they stole your spot” (BFCM-versie van de winnaar)"), ("A2", "Dine automatische voerbak"),
                ("A3", "Chester hondenbank"), ("A4", "Perch kattenboom")):
    ads += (f'<div class="card"><h3>{E(name)}</h3><div class="pair">'
            f'<figure>{media(a[k + "_45"]["final"], "f45")}<figcaption>Feed 4:5</figcaption></figure>'
            f'<figure>{media(a[k + "_916"]["final"], "f916")}<figcaption>Stories/Reels 9:16</figcaption></figure></div></div>')
reels = "".join(f'<figure>{media(u, "f916")}<figcaption>{E(t)}</figcaption></figure>' for u, t in
                ((A["reels"]["R1"], "R1 · Nestle (ads + organisch 23 nov)"), (A["reels"]["R2"], "R2 · Chester (ads + organisch 27 nov)")))

days = ""
for d in sorted({p["date"] for p in PLAN} | {s["date"] for s in A["stories"]}):
    posts = ""
    for p in [p for p in PLAN if p["date"] == d]:
        imgs = "".join(media(u, "f45" if p["type"] != "reel" else "f916") for u in p["assets"])
        posts += (f'<div class="post"><div class="meta"><span class="b">{SLOT[p["slot"]]}</span><span class="b dark">{TYPE[p["type"]]}</span></div>'
                  f'<div class="imgs">{imgs}</div><p class="cap">{E(p["caption"]).replace(chr(10), "<br>")}</p>'
                  f'<p class="tags">{E(p["tags"])}</p><p class="fb">Facebook-link: <a href="{E(p["facebook_link"])}">{E(p["facebook_link"])}</a></p></div>')
    st = "".join(f'<figure>{media(s["url"], "st")}<figcaption>{SLOT[s["slot"]]}</figcaption></figure>' for s in A["stories"] if s["date"] == d)
    days += (f'<section class="day"><h3>{nl_date(d)} <span class="ph">{phase(d)}</span></h3>{posts}'
             f'<h4>Stories (3)</h4><div class="stories">{st}</div></section>')

page = f"""<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BFCM Black Velvet Edit</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant:wght@500;600&family=Jost:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{--char:#1a1a1a;--rose:#b76e79;--cream:#f5f1ed;--sand:#ebe3da}}
body{{margin:0;background:var(--cream);color:var(--char);font-family:Jost,Arial,sans-serif;font-size:15px;line-height:1.5}}
.wrap{{max-width:1100px;margin:0 auto;padding:28px 16px 70px}}
header{{background:var(--char);color:var(--cream);padding:34px 16px}} header .in{{max-width:1100px;margin:0 auto}}
.eb{{color:#d9a3ab;letter-spacing:.2em;text-transform:uppercase;font-size:12px}}
h1{{font-family:Cormorant,serif;font-weight:500;font-size:44px;margin:6px 0}} header p{{opacity:.8;margin:4px 0}}
h2{{font-family:Cormorant,serif;font-weight:500;font-size:32px;margin:40px 0 12px;border-bottom:1px solid var(--sand);padding-bottom:6px}}
h3{{font-family:Cormorant,serif;font-weight:600;font-size:24px;margin:0 0 10px}} h4{{margin:14px 0 8px;font-weight:500}}
.sum{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin-top:18px}}
.sum div{{background:rgba(245,241,237,.08);border:1px solid rgba(183,110,121,.4);padding:12px 14px}}
.sum b{{display:block;font-family:Cormorant,serif;font-size:24px;font-weight:600;color:#fff}}
figure{{margin:0}} figcaption{{font-size:13px;opacity:.75;margin-top:4px}}
img,video{{display:block;max-width:100%;border:1px solid var(--sand);background:#111}}
.grid{{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}}
.w{{width:100%}} .card,.day{{background:#fff;border:1px solid var(--sand);padding:16px;margin-bottom:14px}}
.pair{{display:flex;gap:12px;flex-wrap:wrap}} .f45{{width:240px}} .f916{{width:200px}} .st{{width:150px}}
.post{{border-top:1px solid var(--sand);padding:12px 0}} .imgs{{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}}
.cap{{white-space:normal;margin:6px 0}} .tags{{color:var(--rose);font-size:13px;margin:4px 0}} .fb{{font-size:13px;opacity:.75;margin:0;word-break:break-all}}
.b{{display:inline-block;font-size:11px;letter-spacing:.06em;text-transform:uppercase;background:var(--sand);padding:3px 8px;margin-right:4px}}
.b.dark{{background:var(--char);color:var(--cream)}} .ph{{font-family:Jost;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--rose);margin-left:8px}}
.stories{{display:flex;gap:8px;flex-wrap:wrap}} .note{{background:#fff;border-left:3px solid var(--rose);padding:12px 14px;margin:12px 0}}
@media (max-width:600px){{.f45{{width:46%}} .f916{{width:46%}} .st{{width:31%}} h1{{font-size:34px}}}}
</style></head><body>
<header><div class="in"><div class="eb">CozyCompanion · Black Friday Week 2026</div><h1>The Black Velvet Edit</h1>
<p>Alle beelden voor BFCM, ter goedkeuring. Er staat nog niets live.</p>
<div class="sum"><div><b>10% · 15% · 20%</b>vanaf $75 · $150 · $250, automatisch</div>
<div><b>20 – 22 nov</b>teaser</div><div><b>23 – 30 nov</b>Black Friday Week (t/m ma 23:59 ET)</div>
<div><b>{len(PLAN)} posts · {len(A["stories"])} stories</b>Instagram + Facebook, 11 dagen</div></div></div></header>
<div class="wrap">
<div class="note">Alle foto's zijn nieuw gemaakt met Nano Banana, met jullie echte productfoto als voorbeeld, en elk beeld is streng gecontroleerd (product, dieren, labels). Teksten zijn er daarna zelf op gezet, dus altijd goed gespeld. In de teksten staan geen productprijzen, alleen de kortingstrappen.</div>
<h2>Website</h2><div class="grid">{web}</div>
<h2>Ads (vanaf 23 november)</h2>{ads}
<h2>Reels</h2><div class="pair">{reels}</div>
<h2>Organisch: Instagram + Facebook</h2>
<p>Elke dag een feedpost (op 23, 25, 27, 28, 29 en 30 nov twee) en 3 stories. De reels van 20, 22, 24, 26 en 29 nov zijn de al goedgekeurde reels, met een nieuwe BFCM-tekst.</p>
{days}
</div></body></html>"""
open(os.path.join(S, "bfcm", "overzicht.html"), "w").write(page)
print("ok", len(page))
