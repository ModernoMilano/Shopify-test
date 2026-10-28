import sys, json, os, copy
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import put_theme_files
CHAR, ROSE, CREAM, SAND = "#1a1a1a", "#b76e79", "#f5f1ed", "#ebe3da"
img = lambda k: f"shopify://shop_images/cozycompanion-{k}.png"
raw = open(os.path.join(S, "theme-backup", "templates__index.json")).read()
HEADER = raw[: raw.index("*/") + 2]
orig = json.loads(raw[raw.index("*/") + 2:])

def text(t, preset="rte", color="", width="fit-content", align="left", max_width="normal", pad_bottom=0):
    s = {"text": t, "type_preset": preset, "width": width, "alignment": align, "max_width": max_width,
         "padding-block-end": pad_bottom}
    if color: s["text_color"] = color
    return {"type": "text", "settings": s, "blocks": {}}

def button(label, link, style="button", **kw):
    s = {"label": label, "link": link, "style_class": style}; s.update(kw)
    return {"type": "button", "settings": s, "blocks": {}}

def blocks(*pairs):
    return {k: v for k, v in pairs}, [k for k, _ in pairs]

sections, order = {}, []
def add(key, sec):
    sections[key] = sec; order.append(key)

# 1. Hero
b, o = blocks(
    ("eyebrow", text("<p>Luxury comfort for you &amp; your companions</p>", "h6", CREAM)),
    ("heading", text("<h1>Warmth, thoughtfully designed.</h1>", "h1", CREAM, max_width="narrow")),
    ("sub", text("<p>Heated blankets and smart pet essentials, made for long evenings in and the ones who share them.</p>", "paragraph", CREAM, max_width="narrow", pad_bottom=8)),
    ("ctas", {"type": "group", "settings": {"content_direction": "row", "vertical_on_mobile": False, "gap": 10, "width": "fill"},
              "blocks": {"a": button("Shop blankets", "shopify://collections/cozy-heated-blankets", "button-custom",
                                     custom_button_background=CREAM, custom_button_text=CHAR, custom_button_border=CREAM),
                         "b": button("Pet tech", "shopify://collections/smart-pet-tech", "button-custom",
                                     custom_button_background="rgba(0,0,0,0)", custom_button_text=CREAM, custom_button_border=CREAM)},
              "block_order": ["a", "b"]}),
)
add("hero", {"type": "hero", "blocks": b, "block_order": o, "settings": {
    "media_type_1": "image", "image_1": img("hero"), "content_direction": "column",
    "custom_mobile_media": True, "media_type_1_mobile": "image", "image_1_mobile": img("hero_m"),
    "horizontal_alignment_flex_direction_column": "flex-start", "vertical_alignment_flex_direction_column": "center",
    "gap": 20, "section_width": "full-width", "section_height": "large",
    "toggle_overlay": True, "overlay_style": "gradient", "gradient_direction": "to top", "overlay_color": "#1a1a1a8c",
    "padding-block-start": 64, "padding-block-end": 64}})

# 2. Trust marquee
mq = {}
mo = []
for i, (icon, t) in enumerate([("truck", "Tracked shipping around the world"), ("return", "30-day happiness guarantee"),
                                ("lock", "Secure checkout"), ("heart", "15% off your first order: COZY15")]):
    mq[f"i{i}"] = {"type": "icon", "settings": {"icon": icon, "width": 18, "icon_color": ROSE}, "blocks": {}}
    mq[f"t{i}"] = {"type": "text", "settings": {"text": f"<p>{t}</p>", "type_preset": "custom", "font": "var(--font-body--family)",
                                                 "font_size": "0.875rem", "case": "uppercase", "letter_spacing": "loose",
                                                 "wrap": "nowrap", "text_color": CREAM}, "blocks": {}}
    mo += [f"i{i}", f"t{i}"]
add("trust", {"type": "marquee", "blocks": mq, "block_order": mo,
              "settings": {"background_color": CHAR, "padding-block-start": 14, "padding-block-end": 14, "gap_between_elements": 28}})

# 3. Collections
add("collections", {"type": "collection-list", "blocks": {
    "header": {"type": "group", "settings": {"gap": 8, "padding-block-end": 16, "horizontal_alignment_flex_direction_column": "center"},
               "blocks": {"eyebrow": text("<p>The CozyCompanion edit</p>", "h6", ROSE),
                          "h": text("<h2>Shop by ritual</h2>", "h2")},
               "block_order": ["eyebrow", "h"]},
    "static-collection-card": {"type": "_collection-card", "static": True,
        "settings": {"horizontal_alignment": "flex-start", "vertical_alignment": "flex-end", "placement": "on_image"},
        "blocks": {"collection-card-image": {"type": "_collection-card-image", "static": True, "settings": {"image_ratio": "portrait"}},
                   "collection-title": {"type": "collection-title", "settings": {"type_preset": "h5", "background": True,
                        "background_color": CREAM, "padding-block-start": 8, "padding-block-end": 8,
                        "padding-inline-start": 14, "padding-inline-end": 14}}},
        "block_order": ["collection-title"]}},
    "block_order": ["header"],
    "settings": {"collection_list": ["cozy-heated-blankets", "smart-pet-tech", "holiday-gift-guide", "bundle-deals"],
                 "layout_type": "grid", "columns": 4, "mobile_columns": "2", "columns_gap": 12, "rows_gap": 12,
                 "carousel_on_mobile": True, "mobile_card_size": "60cqw",
                 "section_width": "page-width", "background_color": CREAM,
                 "padding-block-start": 56, "padding-block-end": 40}})

# 4/7. Product lists (reuse the theme's own product-list structure)
pl = orig["sections"]["product_list_fa6P9H"]
def product_list(handle, title, eyebrow, bg):
    s = copy.deepcopy(pl)
    s["settings"].update({"collection": handle, "max_products": 4, "columns": 4, "background_color": bg,
                          "padding-block-start": 40, "padding-block-end": 40, "carousel_on_mobile": True, "mobile_card_size": "60cqw"})
    hdr = s["blocks"]["static-header"]["blocks"]
    hdr["product_list_text_YFtzcL"]["settings"].update({"text": f"<h2>{title}</h2>", "type_preset": "h3"})
    hdr["product_list_button_MWeP9V"]["settings"]["label"] = "View all"
    gal = s["blocks"]["static-product-card"]["blocks"]["product_card_gallery_677WP3"]["settings"]
    gal["image_ratio"] = "square"
    return s
add("blankets", product_list("cozy-heated-blankets", "Cozy heated blankets", "", CREAM))

# 5. Brand story
def editorial(image, pos, eyebrow, heading, body, label, link, bg):
    return {"type": "media-with-content", "settings": {"media_position": pos, "media_width": "medium",
            "media_height": "60svh", "section_width": "full-width", "background_color": bg},
        "blocks": {
            "media": {"type": "_media-without-appearance", "static": True, "settings": {"media_type": "image", "image": img(image)}, "blocks": {}},
            "content": {"type": "_content-without-appearance", "static": True,
                        "settings": {"horizontal_alignment_flex_direction_column": "flex-start",
                                     "vertical_alignment_flex_direction_column": "center", "gap": 20},
                        "blocks": {"eyebrow": text(f"<p>{eyebrow}</p>", "h6", ROSE),
                                   "heading": text(f"<h2>{heading}</h2>", "h2", max_width="narrow"),
                                   "body": text(body, "rte", max_width="narrow"),
                                   "cta": button(label, link, "button-secondary")},
                        "block_order": ["eyebrow", "heading", "body", "cta"]}}}
add("story", editorial("l7", "left", "Chapter II &middot; The evening ritual", "The art of slowing down.",
    "<p>CozyCompanion began with a simple idea: the best moments at home are the quiet ones. A warm blanket, a soft light, a companion curled up beside you.</p><p>We curate pieces that make those moments easier to come by: gentle warmth for chilly evenings and smart essentials that care for your pets, even when you can't be there.</p>",
    "Discover our story", "shopify://pages/about", SAND))

# 6. Value props (two rows of two, so phones get a compact 2x2 grid)
def vp_item(icon, h, t):
    return {"type": "group", "settings": {"gap": 8, "horizontal_alignment_flex_direction_column": "center", "width": "fill"},
            "blocks": {"icon": {"type": "icon", "settings": {"icon": icon, "width": 28, "icon_color": ROSE}, "blocks": {}},
                       "h": text(f"<h3>{h}</h3>", "h6", align="center", width="100%"),
                       "t": text(f"<p>{t}</p>", "rte", align="center", width="100%", max_width="narrow")},
            "block_order": ["icon", "h", "t"]}
ITEMS = [("fire", "Adjustable warmth", "From a soft glow to deep, soothing heat."),
         ("paw_print", "Made for pets too", "Fed, hydrated, warm and close."),
         ("return", "30-day guarantee", "Not in love? Return it, no fuss."),
         ("plane", "Shipped worldwide", "Tracked delivery on every order.")]
rows = {}
for r in range(2):
    rows[f"row{r}"] = {"type": "group", "settings": {"content_direction": "row", "vertical_on_mobile": False, "gap": 16,
                       "horizontal_alignment": "space-between", "vertical_alignment": "flex-start", "width": "fill"},
                       "blocks": {f"v{k}": vp_item(*ITEMS[r * 2 + k]) for k in range(2)}, "block_order": ["v0", "v1"]}
add("promise", {"type": "section", "blocks": {"head": text("<h2>The CozyCompanion promise</h2>", "h3", width="100%", align="center"), **rows},
    "block_order": ["head", "row0", "row1"], "settings": {
    "content_direction": "column", "gap": 28, "section_width": "page-width", "background_color": CREAM,
    "horizontal_alignment_flex_direction_column": "center", "padding-block-start": 56, "padding-block-end": 56}})

add("chapter2", editorial("s_morning", "right", "Chapter I &middot; Care, even when you're away", "Peace of mind, quietly automated.",
    "<p>Long day at work? Dinner is served on time, fresh water keeps flowing, and a quick glance at your phone shows they're fine.</p><p>Our smart pet essentials take care of the routine, so the time you spend together is simply time together.</p>",
    "Explore smart pet tech", "shopify://collections/smart-pet-tech", CREAM))
add("pettech", product_list("smart-pet-tech", "Smart pet tech", "", CREAM))
add("chapter3", editorial("s_bond", "left", "Chapter III &middot; Warm hearts, warm paws", "Because they deserve to be cozy, too.",
    "<p>Senior dogs, small breeds and short-coated cats feel the cold first. A gentle, washable heated blanket gives them a warm place that's entirely their own, right beside yours.</p>",
    "Shop heated blankets for pets", "shopify://collections/heated-blankets-for-pets", SAND))

# 8. Holiday
add("holiday", editorial("holiday", "right", "Holiday Gift Guide", "Gifts that feel like a hug.",
    "<p>Warmth for the people you love and quiet comfort for the pets who complete the picture. Explore our most giftable pieces, all ready to be wrapped.</p>",
    "Shop the gift guide", "shopify://collections/holiday-gift-guide", CHAR))
c = sections["holiday"]["blocks"]["content"]["blocks"]
for k in ("heading", "body"): c[k]["settings"]["text_color"] = CREAM
c["cta"] = button("Shop the gift guide", "shopify://collections/holiday-gift-guide", "button-custom",
                  custom_button_background=ROSE, custom_button_text="#ffffff", custom_button_border=ROSE)

# 9. Newsletter
add("newsletter", {"type": "section", "settings": {"content_direction": "column", "gap": 16,
    "horizontal_alignment_flex_direction_column": "center", "section_width": "page-width", "background_color": SAND,
    "padding-block-start": 56, "padding-block-end": 56},
    "blocks": {"eyebrow": text("<p>Join the Cozy Circle</p>", "h6", ROSE, width="100%", align="center"),
               "h": text("<h2>15% off your first order.</h2>", "h2", width="100%", align="center"),
               "t": text("<p>Be the first to hear about new arrivals, seasonal edits and members-only offers. Use code <strong>COZY15</strong> at checkout.</p>", "rte", width="100%", align="center", max_width="narrow"),
               "signup": {"type": "email-signup", "settings": {"width": "fill", "heading": "",
                          "label": "Join", "style_class": "button"}, "blocks": {}}},
    "block_order": ["eyebrow", "h", "t", "signup"]})

# Story flow: hook -> chapter -> shop it, three times, then browse, promise, gifting, sign-up
order[:] = ["hero", "trust", "chapter2", "pettech", "story", "blankets", "chapter3",
            "collections", "promise", "holiday", "newsletter"]
out = HEADER + "\n" + json.dumps({"sections": sections, "order": order}, indent=2)
open(os.path.join(S, "index.new.json"), "w").write(out)
print(put_theme_files({"templates/index.json": out}))
