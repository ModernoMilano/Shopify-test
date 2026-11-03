"""CozyCompanion Q4 2026 plan for the owner: strategy, phases, budget, guardrails and the full posting calendar
(Nov 3 - Dec 31) with every visual. Sources: social/calendar.json (November), bfcm/social_plan.json + bfcm/assets.json
(Nov 20-30, replaces the November entries for those days), social/calendar_dec.json (December).
Writes q4/q4_plan.html."""
import json, os, html, datetime as dt
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda p: json.load(open(os.path.join(S, p))) if os.path.exists(os.path.join(S, p)) else None
E = html.escape

PHASES = [
    ("f1", "2026-11-03", "2026-11-19", "1 · Data & conversie", "#6f8f7a"),
    ("f2", "2026-11-20", "2026-11-22", "2 · BFCM teaser", "#8a6d7a"),
    ("f3", "2026-11-23", "2026-11-30", "3 · Black Friday Week", "#1a1a1a"),
    ("f4", "2026-12-01", "2026-12-05", "4 · Cadeauseizoen", "#b76e79"),
    ("f5", "2026-12-06", "2026-12-23", "5 · Last-minute cadeaus", "#a5835a"),
    ("f6", "2026-12-24", "2026-12-31", "6 · Kerst & Nieuwjaar", "#5d6b7a"),
]
def phase(d):
    for p in PHASES:
        if p[1] <= d <= p[2]: return p
    return PHASES[0]

nov = {d["date"]: d for d in (J("social/calendar.json") or [])}
dec = {d["date"]: d for d in (J("social/calendar_dec.json") or [])}
bplan = J("bfcm/social_plan.json") or []
bassets = J("bfcm/assets.json") or {}
bstories = {}
for s in bassets.get("stories", []):
    bstories.setdefault(s["date"], []).append(s)
log = {e["date"] for e in (J("social/log.json") or [])}

def thumb(u, w=320):
    if not u: return ""
    base = u.split("?")[0]
    if base.endswith((".mp4", ".mov")):
        return f'<video src="{E(base)}" muted playsinline controls preload="metadata"></video>'
    return f'<img loading="lazy" src="{E(base)}?width={w}" alt="">'

def first_line(c):
    return E((c or "").strip().split("\n")[0])

def day_items(d):
    """[(slot label, kind, [urls], caption)] for one day."""
    out = []
    if "2026-11-20" <= d <= "2026-11-30":
        for p in sorted([p for p in bplan if p["date"] == d], key=lambda p: p["slot"]):
            out.append((("11:43 ET" if p["slot"] == "am" else "19:13 ET"), {"image": "Post", "carousel": "Carrousel", "reel": "Reel"}.get(p["type"], p["type"]), p["assets"], p["caption"]))
        st = sorted(bstories.get(d, []), key=lambda s: ["am", "mid", "pm"].index(s["slot"]) if s["slot"] in ("am", "mid", "pm") else 9)
        if st: out.append(("3× per dag", "Stories", [s["url"] for s in st], ""))
        return out
    src = nov.get(d) or dec.get(d)
    if not src: return out
    a = src.get("assets") or {}
    if a.get("reel"):
        out.append(("11:43 ET", "Reel", [a["reel"]], src.get("caption", "")))
    elif a.get("feed"):
        out.append(("11:43 ET", "Carrousel" if len(a["feed"]) > 1 else "Post", a["feed"], src.get("caption", "")))
    elif src.get("caption"):
        out.append(("11:43 ET", "Post", [], src.get("caption", "")))
    if a.get("story"):
        out.append(("11:43 ET", "Story", [a["story"]], src.get("story_text", "")))
    return out

days, d = [], dt.date(2026, 11, 3)
while d <= dt.date(2026, 12, 31):
    days.append(d.isoformat()); d += dt.timedelta(days=1)

NL_DAY = ["ma", "di", "wo", "do", "vr", "za", "zo"]
NL_MON = {11: "nov", 12: "dec"}
SPECIAL = {"2026-11-23": "Sale start", "2026-11-26": "Thanksgiving", "2026-11-27": "Black Friday", "2026-11-30": "Cyber Monday",
           "2026-12-01": "Giving Tuesday", "2026-12-05": "Laatste besteldag voor kerst", "2026-12-21": "Kortste dag",
           "2026-12-24": "Kerstavond", "2026-12-25": "Kerst", "2026-12-31": "Oudjaar"}

cal = []
for ds in days:
    y, m, dd = map(int, ds.split("-")); wd = dt.date(y, m, dd).weekday()
    ph = phase(ds); items = day_items(ds)
    rows = []
    for slot, kind, urls, cap in items:
        thumbs = "".join(f'<div class="t">{thumb(u)}</div>' for u in urls)
        rows.append(f'<div class="it k-{E(kind.lower())}"><div class="ih"><span class="k">{E(kind)}</span><span class="s">{E(slot)}</span></div>'
                    f'<div class="ts{" many" if len(urls) > 1 else ""}">{thumbs or "<div class=pending>Beeld wordt gemaakt</div>"}</div>'
                    f'{f"<p class=cap>{first_line(cap)}</p>" if cap else ""}</div>')
    if not rows:
        rows.append('<div class="it"><div class="pending">December-beelden worden gemaakt en verschijnen hier zodra ze door de controle zijn</div></div>')
    flag = SPECIAL.get(ds, "")
    done = ' <span class="done">✓ gepost</span>' if ds in log else ""
    if ds in dec and dec[ds].get("needs_owner_approval"):
        flag = (flag + " · " if flag else "") + "cadeaubon: jouw akkoord nodig"
    cal.append(f'<article class="day" style="--ph:{ph[4]}" id="d{ds}"><header><b>{NL_DAY[wd]} {dd} {NL_MON[m]}</b>'
               f'<span class="ph">{E(ph[3])}</span>{f"<span class=fl>{E(flag)}</span>" if flag else ""}{done}</header>{"".join(rows)}</article>')

STRATEGY = """
<section class="card lead">
  <h2>Het plan in één zin</h2>
  <p>Eerst de winkel laten converteren (november), dan Black Friday Week maximaal benutten, en in december verkopen als <b>hét cadeau-adres voor dieren en hun mensen</b>, tot de laatste besteldag. Daarna rustig en warm afsluiten.</p>
</section>

<section class="card">
  <h2>Doelen &amp; hoe ik meet</h2>
  <table>
    <tr><th>Wat</th><th>Doel</th><th>Nu</th></tr>
    <tr><td>Eerste verkopen</td><td>vóór Black Friday</td><td>0</td></tr>
    <tr><td>Winkelwagen → afrekenen</td><td>≥ 35%</td><td>±10–15% (ads, 2–3 nov)</td></tr>
    <tr><td>Bezoek → bestelling</td><td>≥ 1%</td><td>0%</td></tr>
    <tr><td>Kosten per verkoop (ads)</td><td>≤ €30 (november ≤ €45 voor data)</td><td>nog geen verkoop</td></tr>
    <tr><td>Black Friday Week ROAS</td><td>≥ 1,5</td><td>–</td></tr>
  </table>
  <p class="note">Elke maandag om 10:00 (NL) krijg je van mij een kort rapport: omzet, ads, wat werkte, wat ik heb aangepast.</p>
</section>

<section class="card">
  <h2>De 6 fases</h2>
  <div class="phases">
    <div class="pc" style="--ph:#6f8f7a"><h3>1 · Data &amp; conversie</h3><p class="d">3 – 19 november</p>
      <ul><li><b>Doel:</b> eerste verkopen en het lek tussen winkelwagen en afrekenen dichten.</li>
      <li><b>Aanbod:</b> tijdelijk lagere prijzen, sets 20% korting, COZY15 voor nieuwe klanten.</li>
      <li><b>Ads:</b> WINNERS (±€35/dag). Elke maandag en donderdag stuur ik bij: budget naar de beste advertentie en plek, verliezers uit.</li>
      <li><b>Social:</b> elke dag 1 post + 1 story, 11 reels (goedgekeurde novemberkalender).</li>
      <li><b>Website:</b> winkelwagen gerepareerd ✓. Verzendkosten duidelijker maken en "International warehouse" vervangen (wacht op jou).</li></ul></div>
    <div class="pc" style="--ph:#8a6d7a"><h3>2 · BFCM teaser</h3><p class="d">20 – 22 november</p>
      <ul><li><b>Doel:</b> spanning opbouwen en een warm publiek verzamelen.</li>
      <li><b>Website:</b> zwarte aankondigingsbalk en homepage-banner "starts Monday" (gaan automatisch aan).</li>
      <li><b>Social:</b> aftellen: 1 post + 3 stories per dag.</li>
      <li><b>Ads:</b> WINNERS loopt door. Ik bouw doelgroepen van video-kijkers, bezoekers en winkelwagens.</li></ul></div>
    <div class="pc" style="--ph:#1a1a1a"><h3>3 · Black Friday Week</h3><p class="d">23 – 30 november</p>
      <ul><li><b>Aanbod:</b> 10% vanaf $75 · 15% vanaf $150 · 20% vanaf $250, automatisch (staat ingepland ✓).</li>
      <li><b>Ads:</b> aparte BFCM-groep met 4 advertenties en 2 reels, plus retargeting van winkelwagens. Fase 2 + 3 samen: €500–1000.</li>
      <li><b>Social:</b> 1–2 posts + 3 stories per dag: launch, Black Friday, "last 48 hours", Cyber Monday "ends tonight".</li>
      <li><b>Website:</b> banner, balk en een voortgangsbalk naar de volgende korting in de winkelwagen ✓.</li></ul></div>
    <div class="pc" style="--ph:#b76e79"><h3>4 · Cadeauseizoen</h3><p class="d">1 – 5 december</p>
      <ul><li><b>Doel:</b> cadeaus verkopen vóór de laatste besteldag (5 dec).</li>
      <li><b>Aanbod:</b> cadeaugidsen (hond, kat, stocking stuffers) en sets 20%. Geen nieuwe korting nodig.</li>
      <li><b>Ads:</b> cadeau-advertenties naar de Holiday Gift Guide en retargeting (±€40/dag).</li>
      <li><b>Website:</b> balk "Order by Dec 5 for the best chance of Christmas delivery".</li></ul></div>
    <div class="pc" style="--ph:#a5835a"><h3>5 · Last-minute cadeaus</h3><p class="d">6 – 23 december</p>
      <ul><li><b>Probleem:</b> pakketjes komen niet meer op tijd.</li>
      <li><b>Oplossing:</b> een <b>digitale cadeaubon</b>, direct per e-mail (moet jij goedkeuren; ik maak hem aan).</li>
      <li><b>Ads:</b> lager (±€25/dag): cadeaubon + retargeting.</li>
      <li><b>Social:</b> sfeer, zorgtips (feestdagen, winterpootjes), sets.</li></ul></div>
    <div class="pc" style="--ph:#5d6b7a"><h3>6 · Kerst &amp; Nieuwjaar</h3><p class="d">24 – 31 december</p>
      <ul><li><b>Doel:</b> merk en sympathie, niet verkopen.</li>
      <li><b>Ads:</b> pauze 24–26 dec, daarna ±€10/dag.</li>
      <li><b>Social:</b> kerstochtend-reel, rust tussen het pakpapier, vuurwerktips op oudjaar, een warm "Happy New Year".</li></ul></div>
  </div>
</section>

<section class="card">
  <h2>Budget (voorstel)</h2>
  <table>
    <tr><th>Fase</th><th>Per dag</th><th>Totaal</th></tr>
    <tr><td>1 · Data &amp; conversie (17 dagen)</td><td>±€35</td><td>±€600</td></tr>
    <tr><td>2 + 3 · BFCM (11 dagen)</td><td>€45–90</td><td>€500–1000 (jouw keuze)</td></tr>
    <tr><td>4 · Cadeauseizoen (5 dagen)</td><td>±€40</td><td>±€200</td></tr>
    <tr><td>5 · Last-minute (18 dagen)</td><td>±€25</td><td>±€450</td></tr>
    <tr><td>6 · Kerst &amp; Nieuwjaar</td><td>€0–10</td><td>±€50</td></tr>
    <tr><th>Q4 totaal</th><th></th><th>±€1.800 – 2.300</th></tr>
  </table>
  <p class="note">Werkt iets uitzonderlijk goed (kosten per verkoop ruim onder doel), dan vraag ik je eerst voordat ik boven het fasebudget ga.</p>
</section>

<section class="card">
  <h2>Wat ik zelf doe, en wat ik eerst aan jou vraag</h2>
  <div class="two">
    <div><h3>Ik doe zelf</h3><ul>
      <li>Elke dag posten en stories plaatsen volgens deze kalender (alleen goedgekeurde beelden).</li>
      <li>Ads bijsturen binnen het fasebudget: verliezers pauzeren, budget ±25% verschuiven, advertenties uit de goedgekeurde set wisselen.</li>
      <li>Website op het juiste moment omschakelen (balk, banner, winkelwagen per fase).</li>
      <li>Fouten op de site direct oplossen.</li>
      <li>Elke maandag een rapport.</li></ul></div>
    <div><h3>Ik vraag eerst</h3><ul>
      <li>Prijzen veranderen.</li>
      <li>Nieuwe kortingen of codes.</li>
      <li>Meer uitgeven dan het fasebudget.</li>
      <li>Nieuwe producten, de cadeaubon.</li>
      <li>Nieuwe beelden die niet in deze kalender staan.</li>
      <li>Alles wat juridisch of beleid raakt (verzending, retour, privacy).</li></ul></div>
  </div>
</section>

<section class="card">
  <h2>Postschema</h2>
  <table>
    <tr><th>Wanneer</th><th>Wat</th><th>Tijd (VS-oostkust)</th><th>Tijd (NL)</th></tr>
    <tr><td>Elke dag</td><td>Post of reel + story (Instagram + Facebook)</td><td>11:43</td><td>17:43</td></tr>
    <tr><td>20 – 30 nov</td><td>Extra stories</td><td>14:43 en 19:13</td><td>20:43 en 01:13</td></tr>
    <tr><td>Drukke BFCM-dagen</td><td>Tweede post</td><td>19:13</td><td>01:13</td></tr>
  </table>
</section>

<section class="card">
  <h2>Nog van jou nodig</h2>
  <ol>
    <li><b>Akkoord op dit plan</b> (en daarmee op alle beelden in de kalender hieronder).</li>
    <li>Prijzen: laag houden t/m 30 november (advies) of 20 november terug?</li>
    <li>Digitale cadeaubon aanmaken voor december: ja/nee?</li>
    <li>Verzendkosten en gratis-verzendgrens (nu $150).</li>
    <li>"International warehouse" vervangen door een levertermijn.</li>
    <li>Lokale valuta aanzetten (de Chrome-extensie-opdracht).</li>
  </ol>
</section>
"""

legend = "".join(f'<span class="lg" style="--ph:{p[4]}">{E(p[3])} <small>{p[1][8:]}/{p[1][5:7]}–{p[2][8:]}/{p[2][5:7]}</small></span>' for p in PHASES)
doc = f"""<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CozyCompanion Q4 plan</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant:wght@500;600&family=Jost:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{--char:#1a1a1a;--rose:#b76e79;--cream:#f5f1ed;--sand:#ebe3da}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--cream);color:var(--char);font:15px/1.55 Jost,Arial,sans-serif}}
.wrap{{max-width:1100px;margin:0 auto;padding:28px 16px 80px}}
h1{{font:500 44px/1.05 Cormorant,serif;margin:0}} .sub{{opacity:.75;margin:8px 0 24px}}
h2{{font:500 28px/1.15 Cormorant,serif;margin:0 0 12px}} h3{{font:600 20px/1.2 Cormorant,serif;margin:0 0 6px}}
.card{{background:#fff;border:1px solid var(--sand);padding:20px 22px;margin:0 0 16px}} .lead{{background:var(--char);color:var(--cream);border:0}}
.lead b{{color:#d9a3ab}} table{{width:100%;border-collapse:collapse;font-size:14px}} th,td{{text-align:left;padding:8px 6px;border-bottom:1px solid var(--sand);vertical-align:top}}
.note{{font-size:13px;opacity:.75;margin:10px 0 0}} .phases{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}}
.pc{{border-top:4px solid var(--ph);background:var(--cream);padding:14px 16px}} .pc .d{{margin:0 0 8px;font-size:13px;opacity:.7}} .pc ul{{margin:0;padding-left:18px}} .pc li{{margin:4px 0}}
.two{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}} .two ul{{margin:0;padding-left:18px}}
.legend{{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 18px}} .lg{{border-left:4px solid var(--ph);background:#fff;padding:4px 10px;font-size:13px}}
.cal{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}}
.day{{background:#fff;border:1px solid var(--sand);border-top:4px solid var(--ph);padding:10px 12px;min-width:0}}
.day header{{display:flex;flex-wrap:wrap;gap:6px;align-items:baseline;margin-bottom:8px}} .day header b{{font:600 19px Cormorant,serif}}
.ph{{font-size:11px;opacity:.6}} .fl{{font-size:11px;background:var(--rose);color:#fff;padding:1px 6px}} .done{{font-size:11px;color:#3d7a52}}
.it{{margin:8px 0 0}} .ih{{display:flex;justify-content:space-between;font-size:11px;letter-spacing:.08em;text-transform:uppercase}} .k{{color:var(--rose)}} .s{{opacity:.6}}
.ts{{display:grid;grid-template-columns:1fr;gap:4px;margin-top:4px}} .ts.many{{grid-template-columns:repeat(3,1fr)}}
.t img,.t video{{width:100%;display:block;background:var(--sand);aspect-ratio:4/5;object-fit:cover}}
.ts.many .t img,.ts.many .t video{{aspect-ratio:9/16}}
.k-story .ts{{grid-template-columns:1fr}} .k-story .t{{width:58%;margin:0 auto}} .k-story .t img,.k-stories .t img{{aspect-ratio:9/16}}
.k-reel .t video{{aspect-ratio:9/16;width:72%;margin:0 auto}}
.cap{{margin:6px 0 0;font-size:13px;line-height:1.4}} .pending{{font-size:12px;opacity:.6;padding:14px;background:var(--cream);text-align:center}}
@media (max-width:600px){{h1{{font-size:34px}} .cal{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">
<h1>CozyCompanion · Q4 plan</h1>
<p class="sub">3 november – 31 december 2026 · strategie, fases, budget en elke post met beeld. Na jouw akkoord voer ik dit zelf uit.</p>
{STRATEGY}
<section class="card"><h2>Kalender met alle beelden</h2>
<p class="note" style="margin:0 0 6px">Elke dag: wat er wanneer online gaat. Tik op een reel om hem af te spelen. Kleur = fase.</p>
<div class="legend">{legend}</div>
<div class="cal">{"".join(cal)}</div></section>
</div></body></html>"""
os.makedirs(os.path.join(S, "q4"), exist_ok=True)
open(os.path.join(S, "q4", "q4_plan.html"), "w").write(doc)
print("wrote q4/q4_plan.html", len(days), "days,", sum(1 for d in days if day_items(d)), "with content")
