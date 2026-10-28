import sys, json, os, copy
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import put_theme_files, theme_file

CHAR, ROSE, CREAM, SAND, LINE = "#1a1a1a", "#b76e79", "#f5f1ed", "#ebe3da", "#e3dbd2"
img = lambda k: f"shopify://shop_images/cozycompanion-{k}.png"
raw = theme_file("templates/product.json")
i = raw.index("*/") + 2
base = json.loads(raw[i:])
HEADER = raw[:i]

def text(t, preset="rte", **kw):
    s = {"text": t, "type_preset": preset, "width": "100%"}; s.update(kw)
    return {"type": "text", "settings": s, "blocks": {}}

def icon(name, w=20):
    return {"type": "icon", "settings": {"icon": name, "width": w, "icon_color": ROSE}, "blocks": {}}

def row(icon_name, t):
    return {"type": "group", "settings": {"content_direction": "row", "vertical_on_mobile": False, "gap": 10,
            "vertical_alignment": "center", "width": "fill"},
            "blocks": {"i": icon(icon_name, 18), "x": text(t, "paragraph", width="fit-content")}, "block_order": ["i", "x"]}

def accordion(rows):
    blocks, order = {}, []
    for k, (h, body) in enumerate(rows):
        blocks[f"r{k}"] = {"type": "_accordion-row", "settings": {"heading": h},
                           "blocks": {"t": text(body)}, "block_order": ["t"]}
        order.append(f"r{k}")
    return {"type": "accordion", "settings": {"icon": "plus", "dividers": True, "divider_color": LINE, "type_preset": "h6"},
            "blocks": blocks, "block_order": order}

def build(kind):
    """Tight product page: title, stars, price, 3 highlights, options, add to cart, one trust row,
    payment icons, then everything else folded into an accordion. Below: one short story band and
    recommendations."""
    d = copy.deepcopy(base)
    main = d["sections"]["main"]
    det = main["blocks"]["product-details"]; B = det["blocks"]

    # Header: title, stars (only render once a review app has real ratings), price
    hdr = B["group_icgrde"]
    hdr["blocks"]["stars"] = {"type": "review", "settings": {"stars_style": "shaded", "show_number": True,
                              "text_color": ROSE, "width": "fit-content"}, "blocks": {}}
    hdr["block_order"] = ["text_xrnftG", "stars", "price_tVjtKg"]
    hdr["blocks"] = {k: v for k, v in hdr["blocks"].items() if k in hdr["block_order"]}
    hdr["settings"]["gap"] = 8

    hl = {f"h{k}": row("check_box", "<p>{{ closest.product.metafields.custom.highlight_%d.value }}</p>" % k) for k in (1, 2, 3)}
    B["highlights"] = {"type": "group", "settings": {"gap": 6, "width": "fill"}, "blocks": hl, "block_order": list(hl)}

    # Owner's choice: no Shop Pay / "More payment options" buttons on the product page
    B["buy_buttons_eYQEYi"]["blocks"]["accelerated-checkout"]["disabled"] = True

    # One compact trust row instead of stacked lines
    tr = {}
    for k, (ic, t) in enumerate([("plane", "Tracked worldwide"), ("return", "30-day returns"), ("lock", "Secure checkout")]):
        tr[f"t{k}"] = {"type": "group", "settings": {"gap": 6, "horizontal_alignment_flex_direction_column": "center", "width": "fill"},
                       "blocks": {"i": icon(ic, 20), "x": text(f"<p>{t}</p>", "custom", font_size="0.75rem", alignment="center")},
                       "block_order": ["i", "x"]}
    B["trust"] = {"type": "group", "settings": {"content_direction": "row", "vertical_on_mobile": False, "gap": 8,
                  "horizontal_alignment": "space-between", "vertical_alignment": "flex-start", "width": "fill",
                  "padding-block-start": 4, "padding-block-end": 4}, "blocks": tr, "block_order": list(tr)}
    B.pop("payments", None)   # owner's choice: no payment icons anywhere

    care = ("<p>Follow the care label and included instructions. Disconnect the controller before washing; "
            "never use it folded while switched on.</p>") if kind == "blanket" else \
           ("<p>Setup and power details are in the description and the included guide. Clean regularly with a soft cloth.</p>")
    B["info"] = accordion([
        ("Description", "{{ closest.product.description }}"),
        ("Shipping", "<p>Dispatched in 1&ndash;3 business days with tracking. Delivery across the US in 5&ndash;12 business days. <a href=\"/pages/shipping\">Details</a></p>"),
        ("30-day returns", "<p>Not in love? Return it unused within 30 days for a full refund. <a href=\"/pages/returns\">How it works</a></p>"),
        ("Care &amp; safety" if kind == "blanket" else "Setup &amp; care", care),
    ])
    B["info"]["blocks"]["r0"]["settings"]["open_by_default"] = True
    for k in ("tagline", "offer", "promise", "text_aEtTtq"):
        B.pop(k, None)
    det["settings"]["gap"] = 20
    det["block_order"] = ["group_icgrde", "highlights", "variant_picker_R3rGDr", "buy_buttons_eYQEYi",
                          "trust", "info"]
    det["blocks"] = {k: v for k, v in B.items() if k in det["block_order"]}
    # Photos are 2:3: one large photo with thumbnails underneath, on desktop and mobile
    main["blocks"]["media-gallery"]["settings"].update({"media_presentation": "carousel", "aspect_ratio": "adapt",
        "media_fit": "cover", "slideshow_controls_style": "thumbnails", "thumbnail_position": "bottom",
        "thumbnail_width": 72, "thumbnail_radius": 0, "slideshow_mobile_controls_style": "thumbnails",
        "icons_style": "chevron", "constrain_to_viewport": True, "zoom": True})

    if kind == "blanket":
        story = ("l7", "The evening ritual", "Warmth that invites you to slow down.")
    else:
        story = ("s_morning", "Care, even when you're away", "Peace of mind, quietly automated.")
    sections = {k: v for k, v in d["sections"].items() if k not in ("story", "how", "faq")}
    sections["story"] = {"type": "media-with-content", "settings": {"media_position": "left", "media_width": "medium",
        "media_height": "50svh", "section_width": "full-width", "background_color": SAND},
        "blocks": {"media": {"type": "_media-without-appearance", "static": True, "settings": {"media_type": "image", "image": img(story[0])}, "blocks": {}},
                   "content": {"type": "_content-without-appearance", "static": True,
                               "settings": {"horizontal_alignment_flex_direction_column": "flex-start", "vertical_alignment_flex_direction_column": "center", "gap": 12},
                               "blocks": {"e": text(f"<p>{story[1]}</p>", "h6", text_color=ROSE, width="fit-content"),
                                          "h": text(f"<h2>{story[2]}</h2>", "h3", max_width="narrow", width="fit-content")},
                               "block_order": ["e", "h"]}}}
    rec = [k for k in d["order"] if k.startswith("product_recommendations")]
    d["sections"], d["order"] = sections, ["main"] + rec + ["story"]
    return HEADER + "\n" + json.dumps(d, indent=2)

print(put_theme_files({"templates/product.blanket.json": build("blanket"),
                       "templates/product.pettech.json": build("pettech")}))
