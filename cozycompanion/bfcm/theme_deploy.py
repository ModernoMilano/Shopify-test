"""Deploy the BFCM 2026 theme pieces (all date-gated; nothing shows outside Nov 20 - Nov 30 ET unless previewed).
  snippets/cc-bfcm.liquid        phase switch + top strip (rendered first thing in <body>)
  sections/cc-bfcm-hero.liquid   homepage hero, first section of templates/index.json
  snippets/cc-cart-perks.liquid  cart drawer: Black Friday tier progress (10/15/20% at $75/$150/$250) during the sale
Usage: theme_deploy.py [desktop_image_file_name mobile_image_file_name]   (Shopify Files names for the hero)
Preview: storefront ?ccbfcm=teaser|sale|cm ; cart tiers with cart attribute _ccbfcm=preview."""
import os, sys, json
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, S)
from lib import theme_file, put_theme_files
B = os.path.join(S, "bfcm", "theme"); BK = os.path.join(S, "theme-backup")

def backup(name):
    p = os.path.join(BK, name.replace("/", "__") + ".pre-bfcm")
    if not os.path.exists(p):
        open(p, "w").write(theme_file(name))
    return open(p).read()

files = {"snippets/cc-bfcm.liquid": open(os.path.join(B, "cc-bfcm.liquid")).read(),
         "sections/cc-bfcm-hero.liquid": open(os.path.join(B, "cc-bfcm-hero.liquid")).read()}

# layout: render the switch + strip before the header group
lay = backup("layout/theme.liquid")
anchor = '<div id="header-group">'
assert lay.count(anchor) == 1
files["layout/theme.liquid"] = lay.replace(anchor, "{% render 'cc-bfcm' %}\n    " + anchor)

# homepage: BFCM hero first
idx = backup("templates/index.json")
head, body = idx[: idx.find("{")], json.loads(idx[idx.find("{"):])
hero = body["sections"].get("bfcm_hero", {"type": "cc-bfcm-hero", "settings": {}})
# hero images are remembered in bfcm/theme/hero_settings.json (Shopify Files names):
#   theme_deploy.py <bfcm_desktop> <bfcm_mobile>        theme_deploy.py --dec <dec_desktop> <dec_mobile>
cfg_path = os.path.join(B, "hero_settings.json")
cfg = json.load(open(cfg_path)) if os.path.exists(cfg_path) else {}
a = sys.argv[1:]
if len(a) == 3 and a[0] == "--dec":
    cfg["image_desktop_dec"], cfg["image_mobile_dec"] = a[1], a[2]
elif len(a) == 2:
    cfg["image_desktop"], cfg["image_mobile"] = a[0], a[1]
json.dump(cfg, open(cfg_path, "w"), indent=1)
for k, v in cfg.items():
    hero["settings"][k] = f"shopify://shop_images/{v}"
body["sections"]["bfcm_hero"] = hero
body["order"] = ["bfcm_hero"] + [k for k in body["order"] if k != "bfcm_hero"]
files["templates/index.json"] = head + json.dumps(body, indent=2)

# cart drawer: tier progress during the sale (server clock; the cart is re-rendered on every change, so it is current)
perks = backup("snippets/cc-cart-perks.liquid")
old = """  <div class="cc-cart-top">
    {%- if cart.item_count == 1 -%}"""
new = """  <div class="cc-cart-top">
    {%- liquid
      # BFCM 2026: same bounds as the scheduled discounts (bfcm/discounts.py)
      assign cc_now = 'now' | date: '%s' | plus: 0
      assign cc_bf = false
      if cc_now >= 1795410000 and cc_now < 1796101200
        assign cc_bf = true
      endif
      if cart.attributes._ccbfcm == 'preview'
        assign cc_bf = true
      endif
      assign cc_sub = cart.items_subtotal_price
      assign cc_w = cc_sub | times: 100 | divided_by: 25000
      if cc_w > 100
        assign cc_w = 100
      endif
    -%}
    {%- if cc_bf and cart.item_count > 0 and cart.currency.iso_code != 'USD' -%}
      {%- comment -%} the tiers are set in USD; in another currency Shopify converts them, so no dollar maths here {%- endcomment -%}
      <p class="cc-cart-top__msg"><strong>Black Friday Week:</strong> save 10%, 15% or 20% on larger orders</p>
      <p class="cc-cart-top__note">Applied automatically at checkout &middot; Ends Nov 30</p>
    {%- elsif cc_bf and cart.item_count > 0 -%}
      {%- if cc_sub >= 25000 -%}
        <p class="cc-cart-top__msg">&#10003; <strong>20% off</strong> unlocked: our best Black Friday saving</p>
      {%- elsif cc_sub >= 15000 -%}
        <p class="cc-cart-top__msg">&#10003; 15% off unlocked. Add <strong>{{ 25000 | minus: cc_sub | money }}</strong> more for <strong>20% off</strong></p>
      {%- elsif cc_sub >= 7500 -%}
        <p class="cc-cart-top__msg">&#10003; 10% off unlocked. Add <strong>{{ 15000 | minus: cc_sub | money }}</strong> more for <strong>15% off</strong></p>
      {%- else -%}
        <p class="cc-cart-top__msg">Black Friday Week: add <strong>{{ 7500 | minus: cc_sub | money }}</strong> more to save <strong>10%</strong></p>
      {%- endif -%}
      <div class="cc-tiers" aria-hidden="true">
        <div class="cc-progress"><span style="width: {{ cc_w }}%"></span></div>
        <ol class="cc-tiers__marks">
          <li style="left: 30%"{% if cc_sub >= 7500 %} class="is-on"{% endif %}>10%<small>$75</small></li>
          <li style="left: 60%"{% if cc_sub >= 15000 %} class="is-on"{% endif %}>15%<small>$150</small></li>
          <li style="left: 100%"{% if cc_sub >= 25000 %} class="is-on"{% endif %}>20%<small>$250</small></li>
        </ol>
      </div>
      <p class="cc-cart-top__note">Applied automatically at checkout &middot; Ends Nov 30</p>
    {%- elsif cart.item_count == 1 -%}"""
assert perks.count(old) == 1, "cart perks anchor not found"
perks = perks.replace(old, new)
css_anchor = "  .cc-progress {"
assert perks.count(css_anchor) == 1
perks = perks.replace(css_anchor, """  .cc-tiers { position: relative; padding-bottom: 30px; margin: 4px 14px 0 4px; }
  .cc-tiers .cc-progress { height: 6px; }
  .cc-tiers__marks { list-style: none; margin: 0; padding: 0; }
  .cc-tiers__marks li { position: absolute; top: -3px; transform: translateX(-50%); display: flex; flex-direction: column;
    align-items: center; font-size: 0.68rem; font-weight: 500; line-height: 1.2; color: #8a817a; }
  .cc-tiers__marks li::before { content: ''; width: 12px; height: 12px; border-radius: 50%; background: #e3dbd2;
    border: 2px solid #fff; margin-bottom: 3px; }
  .cc-tiers__marks li.is-on { color: #b76e79; }
  .cc-tiers__marks li.is-on::before { background: #b76e79; }
  .cc-tiers__marks small { font-size: 0.62rem; font-weight: 400; opacity: 0.8; }
""" + css_anchor)
hol = "    {%- if today >= 1101 and today <= 1216 -%}"
assert perks.count(hol) == 1
perks = perks.replace(hol, "    {%- if cc_bf and cart.item_count > 0 -%}\n    {%- elsif today >= 1101 and today <= 1216 -%}")
files["snippets/cc-cart-perks.liquid"] = perks

put_theme_files(files)
print("deployed:", ", ".join(files))
