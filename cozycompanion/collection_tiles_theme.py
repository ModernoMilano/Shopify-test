"""Theme side of the collection-page redesign: lifestyle tiles in the grid after every EVERY products, two product
columns on desktop, and the CozyCompanion USP row under the grid. Patches sections/main-collection.liquid from the
untouched copy in theme-backup/, so it can be re-run safely."""
import sys, os, json, re
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import theme_file, put_theme_files

EVERY = 6   # a tile after every 6 products: 3 rows of 2 on desktop and mobile
src = open(os.path.join(S, "theme-backup/sections__main-collection.liquid")).read()
loop_end = """              %}
            </li>
          {% endfor %}"""
assert loop_end in src
src = src.replace(loop_end, """              %}
            </li>
            {%- comment -%} CozyCompanion: lifestyle tile after every __EVERY__ products (collection_tiles_theme.py) {%- endcomment -%}
            {%- liquid
              assign cc_n = paginate.current_offset | plus: forloop.index
              assign cc_mod = cc_n | modulo: __EVERY__
              if cc_mod == 0 and forloop.last == false
                assign cc_k = cc_n | divided_by: __EVERY__ | minus: 1
                render 'cc-collection-tile', collection: collection, k: cc_k
              endif
            -%}
          {% endfor %}""".replace("__EVERY__", str(EVERY)))
style = """
{% style %}
  /* CozyCompanion: two products side by side on desktop, a calmer centred grid, full-row lifestyle tiles */
  @media screen and (min-width: 750px) {
    .product-grid--{{ section.id }}.product-grid--grid { --product-grid-columns-desktop: repeat(2, minmax(0, 1fr)); max-width: 1080px; margin-inline: auto; }
  }
  .product-grid--{{ section.id }} .cc-tile { grid-column: 1 / -1; margin-block: 8px; }
  .cc-tile__link { position: relative; display: block; overflow: hidden; color: #f5f1ed; text-decoration: none; background: #ebe3da; }
  .cc-tile__img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; transition: transform .8s ease; }
  .cc-tile__link:hover .cc-tile__img { transform: scale(1.02); }
  .cc-tile__cap { position: absolute; left: 0; right: 0; bottom: 0; padding: 48px 28px 24px; display: grid; gap: 4px;
    background: linear-gradient(to top, rgba(26,26,26,.55), rgba(26,26,26,0)); }
  .cc-tile__eyebrow { font-size: .7rem; letter-spacing: .16em; text-transform: uppercase; opacity: .9; }
  .cc-tile__title { font-family: var(--font-heading--family); font-size: clamp(1.4rem, 3vw, 2.2rem); line-height: 1.1; }
  .cc-tile__cta { font-size: .8rem; letter-spacing: .08em; text-transform: uppercase; margin-top: 4px; }
  @media screen and (max-width: 749px) {
    .cc-tile__img { aspect-ratio: 4 / 3; }
    .cc-tile__cap { padding: 36px 16px 16px; }
  }
{% endstyle %}
"""
src = src.replace("{% render 'collection-wrapper-styles' %}", "{% render 'collection-wrapper-styles' %}\n" + style, 1)

raw = theme_file("templates/collection.json")
header = re.match(r"\s*/\*.*?\*/\s*", raw, flags=re.S)
d = json.loads(raw[header.end() if header else 0:])
d["sections"]["main"]["blocks"]["filters"]["settings"]["enable_grid_density"] = False   # keep the 2-column layout
usps = [("truck", "Tracked shipping", "Every order ships with tracking."),
        ("return", "30-day returns", "Not right? Send it back within 30 days."),
        ("lock", "Secure checkout", "Encrypted payments, all major cards."),
        ("paw", "Chosen with care", "Pieces we'd want in our own home.")]
d["sections"]["cc_usps"] = {"type": "cc-usps", "settings": {},
    "blocks": {f"u{i}": {"type": "usp", "settings": {"icon": ic, "title": t, "text": x}} for i, (ic, t, x) in enumerate(usps)},
    "block_order": [f"u{i}" for i in range(len(usps))]}
d["order"] = [k for k in d["order"] if k != "cc_usps"] + ["cc_usps"]
print(put_theme_files({
    "snippets/cc-collection-tile.liquid": open(os.path.join(S, "cc-collection-tile.liquid")).read(),
    "sections/cc-usps.liquid": open(os.path.join(S, "cc-usps.liquid")).read(),
    "sections/main-collection.liquid": src,
}))
print(put_theme_files({"templates/collection.json": (header.group(0) if header else "") + json.dumps(d, indent=2)}))
