"""TikTok planner page for the Chrome extension (owner 2026-11-08: "chrome extensie ... alles inplannen op tiktok").
Reads social/tiktok_plan.json + the rendered media in social/organic/out/tt and writes social/tiktok_planner_w<N>.html:
one card per post (P01..P35, in posting order) with Dutch date/time, caption (copy button), media preview, plus
"download week/day" buttons that zip the published media in the browser (Artifact `downloads` capability).
It also writes the Artifact `files` mapping in batches under 60 MB (one publish carries at most 64 MB) to
social/organic/out/planner_batches.json. Usage: python3 social/organic/make_tiktok_planner.py [week] [planner_url]"""
import os, sys, json, html, datetime as dt
S = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEEK = sys.argv[1] if len(sys.argv) > 1 else "1"
URL = sys.argv[2] if len(sys.argv) > 2 else "(de link van deze planner-pagina)"
MEDIA = os.path.join(S, "social", "organic", "out", "tt")
plan = sorted(json.load(open(os.path.join(S, "social", "tiktok_plan.json"))), key=lambda e: e["post_at_nl"])
DAYS = ["ma", "di", "wo", "do", "vr", "za", "zo"]
DAYS_LONG = ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"]
MONTHS = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
ZIPDIR = f"CozyCompanion-TikTok-week{WEEK}"

posts, files = [], {}
for i, e in enumerate(plan, 1):
    pid = f"P{i:02d}"
    t = dt.datetime.strptime(e["post_at_nl"], "%Y-%m-%d %H:%M")
    base = f"tt_{e['date']}_{e['slot']}"
    stamp = t.strftime("%Y-%m-%d_%H-%M")
    if e["type"] == "photo":
        media = []
        for n in range(1, len(e["slides"]) + 1):
            src = f"{base}_s{n}.jpg"
            media.append({"path": f"m/{src}", "zip": f"{pid}_{stamp}_foto-{n}.jpg"})
    else:
        media = [{"path": f"m/{base}.mp4", "zip": f"{pid}_{stamp}_video.mp4"}]
    for m in media:
        src = os.path.join(MEDIA, m["path"][2:]); assert os.path.exists(src), src
        files[m["path"]] = src
        m["size"] = os.path.getsize(src)
    d0 = dt.date.fromisoformat(e.get("us_date", e["date"]))   # the US day the post goes out
    night = t.date() != d0
    posts.append({
        "id": pid, "type": e["type"], "format": e["format"].removeprefix("Carousel · "), "caption": e["description"],
        "day": d0.isoformat(), "dayLabel": f"{DAYS_LONG[d0.weekday()]} {d0.day} {MONTHS[d0.month - 1]}",
        "when": f"{DAYS[t.weekday()]} {t.day} {MONTHS[t.month - 1]} · {t:%H:%M}",
        "date": t.strftime("%d-%m-%Y"), "time": t.strftime("%H:%M"), "et": e["post_at_et"][11:],
        "night": night, "media": media,
    })

total = sum(m["size"] for p in posts for m in p["media"])
# publish batches (< 60 MB each)
batches, cur, size = [], {}, 0
for k, v in files.items():
    s = os.path.getsize(v)
    if cur and size + s > 60e6: batches.append(cur); cur, size = {}, 0
    cur[k] = v; size += s
if cur: batches.append(cur)
json.dump(batches, open(os.path.join(S, "social", "organic", "out", "planner_batches.json"), "w"), indent=1)

first, last = posts[0]["day"], posts[-1]["day"]
fd, ld = dt.date.fromisoformat(first), dt.date.fromisoformat(last)
RANGE = f"{fd.day}–{ld.day} {MONTHS[ld.month - 1]}"
n_photo = sum(p["type"] == "photo" for p in posts); n_video = len(posts) - n_photo

PROMPT = f"""Plan 35 TikTok-posts in voor mijn account @cozycompanion.us via TikTok Studio op de website. Post niets direct: alles wordt ingepland.

Alle posts, captions, datums en tijden staan op deze planner-pagina: {URL}
De bestanden staan op mijn computer in de map Downloads/{ZIPDIR} (de uitgepakte zip van die pagina). Elke bestandsnaam begint met het postnummer (P01 t/m P35).

Doe per post, in volgorde P01 t/m P35:
1. Open https://www.tiktok.com/tiktokstudio/upload. Controleer dat het ingelogde account cozycompanion.us is. Is het een ander account, stop dan en vraag het mij.
2. Upload de bestanden van die post. Video: het bestand P##_..._video.mp4. Foto-carrousel: alle bestanden P##_..._foto-1.jpg, foto-2.jpg, enz. samen, in de volgorde 1, 2, 3. Lukt het niet om zelf het bestand te kiezen in het bestandvenster, vraag mij dan welk bestand ik moet aanklikken en wacht tot ik dat gedaan heb.
3. Wacht tot de upload klaar is.
4. Beschrijving: wis de tekst die er al staat en plak de caption van die post precies zoals op de planner, met emoji's en hashtags. Verschijnt er een lijstje met hashtag-suggesties, druk dan op Escape en kies er geen.
5. Cover: laat de standaardcover staan.
6. Wie kan dit bekijken: Iedereen. Reacties, Duet en Stitch: aan (voor zover TikTok die opties toont).
7. Inhoud van de post bekendmaken (Disclose post content): aan, en kies Je eigen merk (Your brand).
8. Onder Meer opties (Show more): AI-gegenereerde inhoud (AI-generated content) aan.
9. Wanneer posten: kies Plannen (Schedule) en vul de datum en tijd in die op de planner bij die post staan. Dat is Nederlandse tijd, dezelfde tijdzone als deze computer. Posts om 00:00 en 02:00 staan op de planner al op de juiste (volgende) datum.
10. Klik op Plannen en controleer daarna dat de post zichtbaar is bij Berichten (Posts) onder Gepland (Scheduled), met de juiste datum en tijd.

Regels:
- Kies nooit Nu posten (Post now). Alleen inplannen.
- Kijk vóór je begint bij Berichten (Posts) → Gepland (Scheduled) welke posts al ingepland staan, en sla die over, zodat er niets dubbel komt (handig als je eerder bent gestopt).
- Ligt de tijd van een post minder dan 30 minuten in de toekomst of al in het verleden, sla hem dan over en noteer hem.
- Wijzig niets aan het profiel, de instellingen of bestaande posts, en start geen betaalde promotie.
- Krijg je een foutmelding, captcha of verificatie, stop dan en vertel het mij.
- Kan een foto-carrousel niet via de website worden ingepland, sla die post over en ga door met de volgende.

Geef mij aan het eind een tabel P01 t/m P35 met: status (gepland, of overgeslagen met de reden) en de datum en tijd zoals ingepland."""

SETTINGS = [("Wie kan dit bekijken", "Iedereen"), ("Reacties · Duet · Stitch", "aan"),
            ("Post bekendmaken", "Je eigen merk"), ("AI-gegenereerde inhoud", "aan"),
            ("Wanneer", "Plannen, datum en tijd van de post")]

data = json.dumps({"posts": posts, "zipdir": ZIPDIR}, ensure_ascii=False).replace("</", "<\\/")
days = []
for p in posts:
    if not days or days[-1][0] != p["day"]: days.append((p["day"], p["dayLabel"], []))
    days[-1][2].append(p)

def esc(s): return html.escape(s, quote=True)
def card(p):
    if p["type"] == "photo":
        thumbs = "".join(f'<img loading="lazy" src="{esc(m["path"])}" alt="Slide {n}" width="90" height="160">'
                         for n, m in enumerate(p["media"], 1))
        media = f'<div class="strip" tabindex="0" aria-label="{len(p["media"])} slides">{thumbs}</div>'
        kind = f'Foto-carrousel · {len(p["media"])} slides'
    else:
        media = f'<video class="vid" src="{esc(p["media"][0]["path"])}#t=0.6" preload="metadata" controls playsinline muted></video>'
        kind = "Video"
    night = '<span class="night">nacht</span>' if p["night"] else ""
    fn = ", ".join(m["zip"] for m in p["media"]) if len(p["media"]) < 3 else f'{p["media"][0]["zip"]} … foto-{len(p["media"])}.jpg'
    return f"""<article class="post" id="{p['id']}">
  <div class="media">{media}</div>
  <div class="body">
    <div class="meta"><span class="pid">{p['id']}</span><span class="when">{esc(p['when'])}</span>{night}<span class="et">{p['et']} ET</span></div>
    <p class="kind">{kind} <span class="fmt">{esc(p['format'])}</span></p>
    <dl class="facts"><div><dt>Datum</dt><dd>{p['date']}</dd></div><div><dt>Tijd (NL)</dt><dd>{p['time']}</dd></div></dl>
    <pre class="cap" id="cap-{p['id']}">{esc(p['caption'])}</pre>
    <div class="row"><button class="btn ghost" data-copy="cap-{p['id']}" type="button" id="copy-{p['id']}">Kopieer caption</button>
    <span class="file">{esc(fn)}</span></div>
  </div>
</article>"""

day_html = "".join(f"""<section class="day" aria-labelledby="h-{d}">
  <header class="dayhead"><h2 id="h-{d}">{esc(lbl)}</h2>
  <button class="btn ghost small" type="button" data-day="{d}" id="dl-{d}">Download deze dag</button></header>
  {''.join(card(p) for p in ps)}
</section>""" for d, lbl, ps in days)

settings_html = "".join(f"<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>" for a, b in SETTINGS)

page = f"""<title>TikTok Week {WEEK} Planner</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Jost:wght@400;500&family=JetBrains+Mono:wght@400&display=swap">
<style>
/* Layout: a single schedule column, one card per post in posting order, grouped by the US day it belongs to */
:root {{
  --bg: #f6f3f0; --surface: #ffffff; --ink: #1d1a1b; --muted: #6f6669; --line: #e4dcd8;
  --accent: #a85f6a; --accent-ink: #ffffff; --night: #3b4a6b; --chip: #efe7e4;
  --display: 'Cormorant Garamond', 'Iowan Old Style', Georgia, serif;
  --body: 'Jost', 'Avenir Next', 'Segoe UI', system-ui, sans-serif;
  --mono: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #171415; --surface: #221e1f; --ink: #f1ebe8; --muted: #a99ea1; --line: #3a3335;
  --accent: #d58f9a; --accent-ink: #1d1a1b; --night: #9db0d9; --chip: #2e2829; color-scheme: dark }} }}
:root[data-theme="dark"] {{
  --bg: #171415; --surface: #221e1f; --ink: #f1ebe8; --muted: #a99ea1; --line: #3a3335;
  --accent: #d58f9a; --accent-ink: #1d1a1b; --night: #9db0d9; --chip: #2e2829; color-scheme: dark }}
body {{ background: var(--bg); color: var(--ink); font: 15px/1.55 var(--body); }}
.wrap {{ max-width: 860px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 28px 64px; display: grid; gap: 28px; }}
h1 {{ font: 600 clamp(2rem, 6vw, 2.9rem)/1.05 var(--display); margin: 0; text-wrap: balance; letter-spacing: -0.01em; }}
h2 {{ font: 600 1.55rem/1.2 var(--display); margin: 0; }} h2::first-letter {{ text-transform: uppercase; }}
h3 {{ font: 500 0.72rem/1.3 var(--body); text-transform: uppercase; letter-spacing: 0.14em; color: var(--muted); margin: 0; }}
.eyebrow {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.16em; color: var(--accent); margin: 0 0 8px; }}
.lede {{ color: var(--muted); margin: 10px 0 0; max-width: 60ch; }}
.panel {{ background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 18px; display: grid; gap: 14px; }}
.steps {{ margin: 0; padding-left: 1.3em; display: grid; gap: 6px; }}
.btn {{ font: 500 0.8rem/1 var(--body); letter-spacing: 0.08em; text-transform: uppercase; border-radius: 3px;
  padding: 13px 18px; border: 1px solid var(--accent); background: var(--accent); color: var(--accent-ink); cursor: pointer; }}
.btn:hover {{ filter: brightness(1.06); }} .btn:disabled {{ opacity: 0.55; cursor: progress; }}
.btn:focus-visible, .strip:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
.btn.ghost {{ background: transparent; color: var(--accent); }} .btn.small {{ padding: 9px 12px; font-size: 0.7rem; }}
.row {{ display: flex; flex-wrap: wrap; align-items: center; gap: 10px 14px; }}
.status {{ font-size: 0.9rem; color: var(--muted); min-height: 1.4em; margin: 0; }}
.facts {{ display: flex; flex-wrap: wrap; gap: 8px 22px; margin: 0; }}
.facts div {{ display: grid; gap: 1px; }} dt {{ font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.12em; color: var(--muted); }}
dd {{ margin: 0; font-variant-numeric: tabular-nums; }}
.settings {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px 18px; margin: 0; }}
.prompt {{ font: 0.78rem/1.55 var(--mono); white-space: pre-wrap; background: var(--chip); border-radius: 4px; padding: 14px;
  margin: 0; max-height: 300px; overflow: auto; }}
.day {{ display: grid; gap: 12px; }}
.dayhead {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: end; gap: 10px;
  border-bottom: 1px solid var(--line); padding-bottom: 8px; }}
.post {{ display: grid; grid-template-columns: 132px 1fr; gap: 16px; background: var(--surface); border: 1px solid var(--line);
  border-radius: 6px; padding: 14px; scroll-margin-top: 16px; }}
.media {{ min-width: 0; }}
.vid {{ width: 132px; aspect-ratio: 9 / 16; max-width: 100%; border-radius: 4px; background: var(--chip); display: block; object-fit: cover; }}
.strip {{ display: flex; gap: 6px; overflow-x: auto; width: 132px; max-width: 100%; scroll-snap-type: x mandatory; border-radius: 4px; }}
.strip img {{ width: 132px; height: auto; aspect-ratio: 9 / 16; object-fit: cover; flex: 0 0 auto; scroll-snap-align: start;
  border-radius: 4px; background: var(--chip); }}
.body {{ min-width: 0; display: grid; gap: 8px; align-content: start; }}
.meta {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 10px; }}
.pid {{ font: 500 0.75rem/1 var(--mono); background: var(--ink); color: var(--bg); padding: 4px 6px; border-radius: 3px; }}
.when {{ font-weight: 500; font-variant-numeric: tabular-nums; }}
.night {{ font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--night); border: 1px solid var(--night);
  border-radius: 999px; padding: 2px 7px; }}
.et {{ font: 0.74rem var(--mono); color: var(--muted); }}
.kind {{ margin: 0; font-size: 0.88rem; }} .fmt {{ color: var(--muted); }}
.cap {{ font: 0.86rem/1.5 var(--body); white-space: pre-wrap; margin: 0; background: var(--chip); padding: 10px 12px; border-radius: 4px; }}
.file {{ font: 0.7rem var(--mono); color: var(--muted); overflow-wrap: anywhere; min-width: 0; }}
.note {{ font-size: 0.86rem; color: var(--muted); margin: 0; }}
@media (max-width: 520px) {{ .post {{ grid-template-columns: 96px 1fr; gap: 12px; }} .vid, .strip, .strip img {{ width: 96px; }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ scroll-behavior: auto !important; }} }}
</style>
<div class="wrap">
<header>
  <p class="eyebrow">CozyCompanion · @cozycompanion.us</p>
  <h1>TikTok week {WEEK} · {RANGE}</h1>
  <p class="lede">{len(posts)} posts ({n_video} video's, {n_photo} foto-carrousels), 5 per dag op de beste tijden voor Amerika. Alle tijden zijn Nederlandse tijd; ET is de tijd aan de Amerikaanse oostkust.</p>
</header>

<section class="panel" aria-labelledby="h-how">
  <h3 id="h-how">Zo plan je de week in</h3>
  <ol class="steps">
    <li>Download de hele week hieronder en pak de zip uit in je map Downloads. Dan staat alles in <b>Downloads/{ZIPDIR}</b>.</li>
    <li>Open TikTok Studio in Chrome en log in als cozycompanion.us.</li>
    <li>Kopieer de prompt hieronder en geef hem aan de Chrome-extensie. Die plant alle {len(posts)} posts in.</li>
  </ol>
  <div class="row"><button class="btn" type="button" id="dl-all">Download hele week (.zip, {total / 1e6:.0f} MB)</button></div>
  <p class="status" id="status" role="status" aria-live="polite"></p>
</section>

<section class="panel" aria-labelledby="h-prompt">
  <div class="row" style="justify-content:space-between"><h3 id="h-prompt">Prompt voor de Chrome-extensie</h3>
  <button class="btn ghost small" type="button" data-copy="prompt" id="copy-prompt">Kopieer prompt</button></div>
  <pre class="prompt" id="prompt">{esc(PROMPT)}</pre>
</section>

<section class="panel" aria-labelledby="h-set">
  <h3 id="h-set">Instellingen voor elke post</h3>
  <dl class="settings">{settings_html}</dl>
  <p class="note">Tip: geef je sterkste video's later in de app nog een trending geluid. Dat is de grootste hefboom voor bereik op TikTok.</p>
</section>

{day_html}
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script id="plan" type="application/json">{data}</script>
<script>
(function () {{
  var PLAN = JSON.parse(document.getElementById('plan').textContent);
  var statusEl = document.getElementById('status');
  function say(t) {{ statusEl.textContent = t; }}
  document.addEventListener('click', function (ev) {{
    var b = ev.target.closest('[data-copy]'); if (!b) return;
    var el = document.getElementById(b.getAttribute('data-copy')); var txt = el.textContent;
    var done = function () {{ var o = b.textContent; b.textContent = 'Gekopieerd'; setTimeout(function () {{ b.textContent = o; }}, 1400); }};
    var fallback = function () {{ var r = document.createRange(); r.selectNodeContents(el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = 'Geselecteerd: Ctrl/Cmd+C'; }};
    try {{ navigator.clipboard.writeText(txt).then(done, fallback); }} catch (e) {{ fallback(); }}
  }});
  var dlP = (window.claude && window.claude.use) ? window.claude.use('downloads') : Promise.resolve(null);
  var buttons = [document.getElementById('dl-all')].concat([].slice.call(document.querySelectorAll('[data-day]')));
  dlP.then(function (d) {{
    if (!d) {{ buttons.forEach(function (b) {{ b.disabled = true; }});
      say('Downloaden werkt alleen als je deze pagina op claude.ai opent.'); }}
  }});
  function planText(posts) {{
    return posts.map(function (p) {{
      return p.id + '  ' + p.date + '  ' + p.time + ' (NL)  ' + (p.type === 'photo' ? 'foto-carrousel' : 'video') + '\\n' +
        p.media.map(function (m) {{ return '  ' + m.zip; }}).join('\\n') + '\\n\\n' + p.caption + '\\n\\n----------\\n';
    }}).join('\\n');
  }}
  async function build(posts, name, btn) {{
    var d = await dlP; if (!d) return;
    if (typeof JSZip === 'undefined') {{ say('De zip-module is niet geladen. Herlaad de pagina en probeer opnieuw.'); return; }}
    buttons.forEach(function (b) {{ b.disabled = true; }});
    try {{
      var zip = new JSZip(), dir = zip.folder(PLAN.zipdir);
      var list = []; posts.forEach(function (p) {{ p.media.forEach(function (m) {{ list.push(m); }}); }});
      for (var i = 0; i < list.length; i++) {{
        say('Bestanden ophalen: ' + (i + 1) + ' van ' + list.length);
        var r = await fetch(list[i].path); if (!r.ok) throw new Error(list[i].path + ' (' + r.status + ')');
        dir.file(list[i].zip, await r.blob());
      }}
      dir.file('planning.txt', planText(posts));
      say('Zip maken…');
      var blob = await zip.generateAsync({{ type: 'blob', compression: 'STORE' }});
      say('Bevestig het opslaan in het venster.');
      await d.save({{ filename: name, data: blob }});
      say('Opgeslagen: ' + name + '. Pak hem uit in je map Downloads.');
    }} catch (e) {{
      var c = e && e.code;
      say(c === 'declined' ? 'Opslaan geannuleerd. Klik opnieuw als je de zip toch wilt.' :
          c === 'rate_limited' ? 'Er staat al een opslaan-venster open. Rond dat eerst af.' :
          'Downloaden lukte niet: ' + ((e && e.message) || e) + '. Probeer het opnieuw.');
    }} finally {{ buttons.forEach(function (b) {{ b.disabled = false; }}); }}
  }}
  document.getElementById('dl-all').addEventListener('click', function () {{ build(PLAN.posts, PLAN.zipdir + '.zip', this); }});
  [].slice.call(document.querySelectorAll('[data-day]')).forEach(function (b) {{
    b.addEventListener('click', function () {{ var day = b.getAttribute('data-day');
      build(PLAN.posts.filter(function (p) {{ return p.day === day; }}), PLAN.zipdir + '_' + day + '.zip', b); }});
  }});
}})();
</script>
"""
out = os.path.join(S, "social", f"tiktok_planner_w{WEEK}.html")
open(out, "w").write(page)
print(out, f"{len(page) / 1e3:.0f} kB", "posts", len(posts), "files", len(files), f"{total / 1e6:.0f} MB", "batches", [len(b) for b in batches])
