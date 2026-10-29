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

def build(kind, size_guide=None):
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
    # owner's choice: payment icons only here, right under the buy button (not in cart or footer)
    B["payments"] = {"type": "payment-icons", "settings": {"horizontal_alignment": "center", "gap": 6}, "blocks": {}}
    B["bundle"] = {"type": "cc-bundle", "settings": {}, "blocks": {}}   # 'Complete the set' -20% (bundles.py)

    care = ("<p>Follow the care label and included instructions. Disconnect the controller before washing; "
            "never use it folded while switched on.</p>") if kind == "blanket" else \
           ("<p>Setup and power details are in the description and the included guide. Clean regularly with a soft cloth.</p>")
    help_line = "<p>Not sure? Email us at <a href=\"mailto:cozycompanion.us@gmail.com\">cozycompanion.us@gmail.com</a> and we'll help you choose.</p>"
    guides = {
        "apparel": ("<p>Measure your pet's neck, chest (the widest part, just behind the front legs) and back length "
                    "(base of the neck to base of the tail) with a soft tape. Compare with the sizes on this page; between two sizes, choose the larger one.</p>" + help_line),
        "bed": ("<p>Measure your pet lying stretched out, nose to tail, and add 6&ndash;10 in. Curlers can go a size smaller, "
                "stretchers a size bigger. Compare with the sizes on this page.</p>" + help_line),
    }
    faq = ("<p><strong>When will my order arrive?</strong><br>Orders are prepared in 1&ndash;3 business days and delivered across the US in 5&ndash;12 business days, with tracking.</p>"
           "<p><strong>What if it doesn't fit or they don't love it?</strong><br>Return it unused within 30 days for a full refund under our happiness guarantee.</p>"
           "<p><strong>Is it suitable for my dog or cat?</strong><br>Check the sizes and details above. Always supervise pets with new toys and accessories at first.</p>"
           "<p><strong>Do you have a welcome offer?</strong><br>Yes: join the Cozy Circle and get 15% off your first order with code COZY15.</p>")
    rows = [("Description", "{{ closest.product.description }}")]
    if size_guide: rows.append(("Size &amp; fit", guides[size_guide]))   # only on products that come in sizes
    B["info"] = accordion(rows + [
        ("Shipping", "<p>Dispatched in 1&ndash;3 business days with tracking. Delivery across the US in 5&ndash;12 business days. Free tracked shipping on orders over $150. <a href=\"/pages/shipping\">Details</a></p>"),
        ("30-day returns", "<p>Not in love? Return it unused within 30 days for a full refund. <a href=\"/pages/returns\">How it works</a></p>"),
        ("Care &amp; safety" if kind == "blanket" else "Setup &amp; care", care),
        ("FAQ", faq),
    ])
    B["info"]["blocks"]["r0"]["settings"]["open_by_default"] = True
    for k in ("tagline", "offer", "promise", "text_aEtTtq"):
        B.pop(k, None)
    det["settings"]["gap"] = 20
    det["block_order"] = ["group_icgrde", "highlights", "variant_picker_R3rGDr", "buy_buttons_eYQEYi",
                          "payments", "trust", "bundle", "info"]
    det["blocks"] = {k: v for k, v in B.items() if k in det["block_order"]}
    # Photos are 2:3: one large photo with thumbnails underneath, on desktop and mobile
    main["blocks"]["media-gallery"]["settings"].update({"media_presentation": "carousel", "aspect_ratio": "adapt",
        "media_fit": "cover", "slideshow_controls_style": "thumbnails", "thumbnail_position": "bottom",
        "thumbnail_width": 72, "thumbnail_radius": 0, "slideshow_mobile_controls_style": "thumbnails",
        "icons_style": "chevron", "constrain_to_viewport": True, "zoom": True})

    if kind == "blanket":
        story = ("l7", "The evening ritual", "Warmth that invites you to slow down.")
    else:
        story = ("h3_story", "The CozyCompanion promise", "Considered essentials, chosen with care.")
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
    main["settings"]["enable_sticky_add_to_cart"] = True   # buy button follows on scroll (mobile especially)
    for k in rec:   # 'Pairs well with': more products, swipeable
        d["sections"][k]["settings"].update({"layout_type": "carousel", "max_products": 10, "columns": 4,
                                             "carousel_on_mobile": True, "mobile_columns": "2"})
    sections["community"] = {"type": "cc-community", "settings": {"heading": "From our community", "max_items": 8}}   # hidden until real entries exist
    d["sections"], d["order"] = sections, ["main", "community"] + rec + ["story"]
    return (HEADER + "\n" + json.dumps(d, indent=2)).replace("You may also like ", "Pairs well with").replace("<h3>Complete the ritual</h3>", "<h3>Pairs well with</h3>")

print(put_theme_files({"templates/product.blanket.json": build("blanket"),
                       "templates/product.pettech.json": build("pettech"),
                       "templates/product.apparel.json": build("pettech", "apparel"),
                       "templates/product.bed.json": build("pettech", "bed")}))

# Which template each product uses: a size guide only where the product actually comes in sizes
from lib import gql, check
after = None
while True:
    r = gql("""query($a:String){products(first:100,after:$a,query:"-status:archived"){nodes{id handle tags templateSuffix
               options{name optionValues{name}}} pageInfo{hasNextPage endCursor}}}""", {"a": after})["products"]
    for p in r["nodes"]:
        if p["templateSuffix"] == "blanket": continue
        sized = any(o["name"].lower().startswith("size") and len(o["optionValues"]) > 1 for o in p["options"])
        tags = set(p["tags"])
        want = ("apparel" if sized and tags & {"wear", "walk"} else
                "bed" if sized and "beds-dens" in tags else "pettech")
        if p["templateSuffix"] != want:
            check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){userErrors{field message}}}",
                      {"p": {"id": p["id"], "templateSuffix": want}})["productUpdate"], p["handle"])
            print(f"  {p['handle']}: {p['templateSuffix']} -> {want}")
    if not r["pageInfo"]["hasNextPage"]: break
    after = r["pageInfo"]["endCursor"]
