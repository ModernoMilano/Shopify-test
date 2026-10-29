"""Product highlights with matching icons instead of check boxes.

Each of the three highlights (custom.highlight_1..3) gets an icon key in custom.highlight_icon_1..3, picked from its
wording (first matching rule wins, 'paw' as fallback). The theme block blocks/cc-highlights.liquid renders the rows;
snippets/cc-icon.liquid holds the line icons (24px grid, round strokes, drawn in the brand rose).
Usage: python3 -I highlight_icons.py [--preview out.html]   (preview: writes an HTML page instead of saving)"""
import sys, os, re, json
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check, put_theme_files

ICONS = {  # inner SVG, viewBox 0 0 24 24
  "moon": '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z"/>',
  "droplet": '<path d="M12 3.5s-6 6.6-6 10.5a6 6 0 0 0 12 0c0-3.9-6-10.5-6-10.5Z"/><path d="M9.5 15a2.5 2.5 0 0 0 2.5 2.5"/>',
  "wash": '<path d="M4 9h16l-1.5 10.5h-13Z"/><path d="M7 13.5c1.2 0 1.2 1 2.5 1s1.3-1 2.5-1 1.2 1 2.5 1 1.3-1 2.5-1"/><path d="M8 6.5c.8-.8.8-1.7 0-2.5M12 6.5c.8-.8.8-1.7 0-2.5M16 6.5c.8-.8.8-1.7 0-2.5"/>',
  "bolt": '<path d="M13 3 5.5 13.5H12L11 21l7.5-10.5H12Z"/>',
  "app": '<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 18.5h2"/><path d="M9.8 9.2a3.2 3.2 0 0 1 4.4 0M8.4 7.6a5.2 5.2 0 0 1 7.2 0"/><circle cx="12" cy="11.2" r=".6"/>',
  "camera": '<path d="M3.5 8.5A1.5 1.5 0 0 1 5 7h2.5L9 5h6l1.5 2H19a1.5 1.5 0 0 1 1.5 1.5v9A1.5 1.5 0 0 1 19 19H5a1.5 1.5 0 0 1-1.5-1.5Z"/><circle cx="12" cy="13" r="3.5"/>',
  "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
  "shield": '<path d="M12 3 5 6v5.5c0 4.4 3 8 7 9.5 4-1.5 7-5.1 7-9.5V6Z"/><path d="m9 12 2 2 4-4"/>',
  "feather": '<path d="M20 4c-7 0-12 5-12 12v4"/><path d="M8 16c5 0 9-2.5 10.5-7"/><path d="M8 12c3 0 6-1.5 8-4"/>',
  "layers": '<path d="m12 3.5 8.5 4.5-8.5 4.5L3.5 8Z"/><path d="m3.5 12 8.5 4.5 8.5-4.5"/><path d="m3.5 16 8.5 4.5 8.5-4.5"/>',
  "paw": '<path d="M12 12.5c-2.8 0-5.5 3.2-5.5 5.4 0 1.6 1.3 2.4 2.8 2.1 1.1-.2 1.8-.6 2.7-.6s1.6.4 2.7.6c1.5.3 2.8-.5 2.8-2.1 0-2.2-2.7-5.4-5.5-5.4Z"/><ellipse cx="5.8" cy="10" rx="1.9" ry="2.3"/><ellipse cx="9.6" cy="5.7" rx="1.9" ry="2.3"/><ellipse cx="14.4" cy="5.7" rx="1.9" ry="2.3"/><ellipse cx="18.2" cy="10" rx="1.9" ry="2.3"/>',
  "sparkle": '<path d="M12 3.5c.6 4 1.5 5 5.5 5.5-4 .6-4.9 1.5-5.5 5.5-.6-4-1.5-4.9-5.5-5.5 4-.5 4.9-1.5 5.5-5.5Z"/><path d="M18 15c.3 1.7.8 2.2 2.5 2.5-1.7.3-2.2.8-2.5 2.5-.3-1.7-.8-2.2-2.5-2.5 1.7-.3 2.2-.8 2.5-2.5Z"/>',
  "ruler": '<path d="m3.5 15.5 12-12 5 5-12 12Z"/><path d="m7 12 2 2M9.5 9.5l1.5 1.5M12 7l2 2M14.5 4.5 16 6"/>',
  "flame": '<path d="M12 21a6 6 0 0 0 6-6c0-4-3-6-4-10-2 2-2.5 4-2.5 5.5C10 9.5 9 8.5 9 7c-2 2-3 4.5-3 8a6 6 0 0 0 6 6Z"/>',
  "snowflake": '<path d="M12 3v18M4.2 7.5l15.6 9M4.2 16.5l15.6-9"/><path d="m9.5 4.5 2.5 2 2.5-2M9.5 19.5l2.5-2 2.5 2"/>',
  "umbrella": '<path d="M3 12a9 9 0 0 1 18 0Z"/><path d="M12 12v6.5a2 2 0 0 1-4 0"/><path d="M12 3v.5"/>',
  "eye": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z"/><circle cx="12" cy="12" r="3"/>',
  "wind": '<path d="M3 9h11a3 3 0 1 0-3-3"/><path d="M3 15h15a3 3 0 1 1-3 3"/><path d="M3 12h7"/>',
  "leaf": '<path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15"/><path d="M5 19c3-4 6-7 10-9"/>',
  "scissors": '<circle cx="6" cy="7" r="2.5"/><circle cx="6" cy="17" r="2.5"/><path d="M8.2 8.3 20 18M8.2 15.7 20 6"/>',
  "bowl": '<path d="M3 11h18a9 9 0 0 1-18 0Z"/><path d="M8 7.5c1-.8 2-.8 3 0M13 6c1-.8 2-.8 3 0"/>',
  "quiet": '<path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4Z"/><path d="m16 9.5 5 5M21 9.5l-5 5"/>',
  "box": '<path d="M3.5 7.5 12 3.5l8.5 4v9L12 20.5l-8.5-4Z"/><path d="M3.5 7.5 12 11.5l8.5-4M12 11.5v9"/>',
  "car": '<path d="M4 16.5V12l2-5h12l2 5v4.5"/><path d="M3 12h18v4.5H3Z"/><circle cx="7.5" cy="17.5" r="1.5"/><circle cx="16.5" cy="17.5" r="1.5"/>',
  "plane": '<path d="M21 4 3 11l7 2.5L12.5 21 21 4Z"/><path d="m10 13.5 4-4"/>',
  "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>',
  "heart": '<path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7.4 4.3 4.3 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10Z"/>',
  "home": '<path d="M3.5 11 12 4l8.5 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/>',
  "hand": '<path d="M8 12V6a1.5 1.5 0 0 1 3 0v5M11 11V4.5a1.5 1.5 0 0 1 3 0V11M14 11V6a1.5 1.5 0 0 1 3 0v7c0 4-2.5 7-6.5 7S5 17 4.5 14l-1-3.5a1.4 1.4 0 0 1 2.6-1L8 13"/>',
  "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
  "grip": '<rect x="4" y="6" width="16" height="12" rx="3"/><path d="M8 10v4M12 10v4M16 10v4"/>',
  "star": '<path d="m12 3.5 2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.8l-5.2 2.8 1-5.8-4.3-4.1 5.9-.9Z"/>',
}
RULES = [  # (regex on the highlight text, icon); first match wins
  (r"camera|video|\bhd\b|watch .* live", "camera"),
  (r"\bapp\b|wi-?fi|smart|find my|nearby|sound", "app"),
  (r"overheat|protection|escape|(?<!water-)resistant|buoyan|grab handle|anti-bite", "shield"),
  (r"airflow|negative ions|static", "wind"),
  (r"heat|warm|thermal|temperature", "flame"),
  (r"recharge|usb|batter|cordless|charging|powered", "bolt"),
  (r"timer|schedul|automatic|auto[- ]|portion|minutes|on its own|random", "clock"),
  (r"quiet|silent|low[- ]noise", "quiet"),
  (r"winter|cold|insulat|snow|fleece", "snowflake"),
  (r"removable cover|wash|dishwasher|wipe|clean|rinse|reusable|hair off|lint|traps litter|catches spills|spill", "wash"),
  (r"\brain|waterproof|water-?resistant|water-repellent|splash|puddle", "umbrella"),
  (r"absorb|microfiber|towel", "droplet"),
  (r"fountain|water|drink|hydrat|filt", "droplet"),
  (r"memory foam|orthopedic|gel", "layers"),
  (r"plush|soft|sherpa|velvet|velour|fluffy|cozy|faux fur|felt|knit|flannel|cotton|lightweight|smooth", "feather"),
  (r"thick|padding|padded|cushion|bolster|support", "layers"),
  (r"back seat|car\b|booster|road", "car"),
  (r"sleep|nap|rest|calm|bed\b|lounge", "moon"),
  (r"breathable|mesh|\bair|dry", "wind"),
  (r"reflective|\bled\b|\blight\b|glow|visible|see each other|sensor", "eye"),
  (r"clipper|trim|groom|\bcomb|brush|nail|dematt|grind|blade|knot|\bmats\b|tangle|shed", "scissors"),
  (r"feed|bowl|meal|kibble|food|treat|slow|lick|snuffle|dinner|eaters", "bowl"),
  (r"travel|carrier|airline|trip|wheel", "plane"),
  (r"leash|harness|walk|collar|lead\b", "link"),
  (r"closure|hook-and-loop|buckle|magnet|lock|clasp|snap", "lock"),
  (r"hands-free|easy|one hand|simple|quick|touch|handle|strap|handheld|catch", "hand"),
  (r"storage|store|hidden|fold|compact|organi[sz]|pouch|pocket|steps|ramp", "box"),
  (r"non-slip|anti-slip|grip|stays put|suction|sticks", "grip"),
  (r"safe|secure|non-toxic|bpa|durable|chew|tough|sturdy|strong|rubber|\blb\b", "shield"),
  (r"size|adjustable|\bfit\b|\bxs\b|\d+(\.\d+)?\s?(in|ft|oz)\b", "ruler"),
  (r"floral|print|pattern|gingham|style|black|white|gr[ae]y|violet|colou?r|rose gold|silver|finish|design|sculpt|modern|elegant|look|tufted|chesterfield|chaise|lifelike", "sparkle"),
  (r"sofa|couch|den\b|hideaway|hide|tunnel|cave|house|tree|perch|lookout|climb", "home"),
  (r"wood|acacia|ceramic|natural|bamboo|stainless|eco|cardboard", "leaf"),
  (r"comfort|tilt|raised|love|bond|together|gift|huggable", "heart"),
  (r"catnip|play|toy|chase|fetch|pounce|interactive|enrich|puzzle|game|ball|bird|feather|hunt|bat\b", "paw"),
]

OVERRIDES = {  # exact highlight text -> icon, where the wording fools the rules
  "4 weight sensors for safety": "shield", "Quiet, scratch-resistant felt": "quiet", "Feather pops out at random": "paw",
  "Folds into a ring with magnets": "box", "Clips and vacuums in one go": "scissors", "Hair goes straight into the bin": "wash",
  "Neutralizes litter box odors": "leaf", "Tilt-out bin hides the food": "box", "Shelf and hooks for leashes and treats": "box",
  "Hammocks, hideaway and lookout": "home", "Scratch, climb and lounge": "home", "Digital scale in the handle": "ruler",
  "Raised so small pets can see out": "eye", "Seat strap and safety clip": "lock", "Covers head and ears": "snowflake",
}

def pick(text):
    if text in OVERRIDES: return OVERRIDES[text]
    t = (text or "").lower()
    return next((ic for rx, ic in RULES if re.search(rx, t)), "paw")

SNIPPET = ("{%- comment -%} CozyCompanion line icons (highlight_icons.py). Usage: {% render 'cc-icon', name: 'moon' %} {%- endcomment -%}\n"
           '<svg class="cc-icon" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.75" '
           'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
           "{%- case name -%}" + "".join(f"{{%- when '{k}' -%}}{v}" for k, v in ICONS.items() if k != "paw") +
           "{%- else -%}" + ICONS["paw"] + "{%- endcase -%}</svg>\n")

BLOCK = """{%- comment -%}
  CozyCompanion highlights: the product's three highlights (custom.highlight_1..3), each with its own line icon
  (custom.highlight_icon_1..3, set by highlight_icons.py) in a soft sand circle.
{%- endcomment -%}
{%- assign p = closest.product -%}
<ul class="cc-hl" role="list" {{ block.shopify_attributes }}>
  {%- for i in (1..3) -%}
    {%- assign k = 'highlight_' | append: i -%}
    {%- assign ik = 'highlight_icon_' | append: i -%}
    {%- assign t = p.metafields.custom[k].value -%}
    {%- if t != blank -%}
      <li class="cc-hl__row">
        <span class="cc-hl__icon">{% render 'cc-icon', name: p.metafields.custom[ik].value %}</span>
        <span class="cc-hl__text">{{ t | escape }}</span>
      </li>
    {%- endif -%}
  {%- endfor -%}
</ul>
<style>
  .cc-hl { list-style: none; margin: 4px 0; padding: 0; display: grid; gap: 12px; }
  .cc-hl__row { display: flex; align-items: center; gap: 14px; }
  .cc-hl__icon { flex: 0 0 40px; width: 40px; height: 40px; border-radius: 50%; background: #ebe3da; color: #b76e79;
    display: inline-flex; align-items: center; justify-content: center; }
  .cc-hl__icon .cc-icon { width: 22px; height: 22px; }
  .cc-hl__text { font-size: 1rem; line-height: 1.35; }
</style>

{% schema %}
{ "name": "CC highlights", "tag": null, "settings": [], "presets": [{ "name": "CC highlights" }] }
{% endschema %}
"""

def products():
    out, after = [], None
    while True:
        r = gql("""query($a:String){products(first:100,after:$a,query:"-status:archived"){nodes{id handle
                   h1: metafield(namespace:"custom",key:"highlight_1"){value} h2: metafield(namespace:"custom",key:"highlight_2"){value}
                   h3: metafield(namespace:"custom",key:"highlight_3"){value}} pageInfo{hasNextPage endCursor}}}""", {"a": after})["products"]
        out += r["nodes"]
        if not r["pageInfo"]["hasNextPage"]: return out
        after = r["pageInfo"]["endCursor"]

if __name__ == "__main__":
    P = products()
    if "--preview" in sys.argv:
        out = sys.argv[sys.argv.index("--preview") + 1]
        rows = []
        for p in P:
            cells = "".join(f'<div class="r"><span class="i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS[pick((p[h] or {}).get("value"))]}</svg></span>{(p[h] or {}).get("value", "")}<em>{pick((p[h] or {}).get("value"))}</em></div>' for h in ("h1", "h2", "h3"))
            rows.append(f'<div class="p"><b>{p["handle"]}</b>{cells}</div>')
        open(out, "w").write("""<html><head><style>body{font-family:Jost,Arial;background:#f5f1ed;margin:16px;display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.p{background:#fff;padding:10px;font-size:12px}.p b{display:block;margin-bottom:6px;font-size:11px;color:#888}.r{display:flex;align-items:center;gap:8px;margin:5px 0}
.i{width:30px;height:30px;border-radius:50%;background:#ebe3da;color:#b76e79;display:inline-flex;align-items:center;justify-content:center;flex:none}.i svg{width:17px;height:17px}
em{margin-left:auto;color:#bbb;font-size:10px}</style></head><body>""" + "".join(rows) + "</body></html>")
        print("preview:", out, len(P), "products")
        sys.exit()
    print(put_theme_files({"snippets/cc-icon.liquid": SNIPPET, "blocks/cc-highlights.liquid": BLOCK}))
    mf = []
    for p in P:
        for n, h in enumerate(("h1", "h2", "h3"), 1):
            if p[h]:
                mf.append({"ownerId": p["id"], "namespace": "custom", "key": f"highlight_icon_{n}", "type": "single_line_text_field", "value": pick(p[h]["value"])})
    for i in range(0, len(mf), 25):
        check(gql("mutation($m:[MetafieldsSetInput!]!){metafieldsSet(metafields:$m){userErrors{field message}}}", {"m": mf[i:i + 25]})["metafieldsSet"], "icons")
    print("icons set:", len(mf))
