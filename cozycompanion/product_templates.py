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
    d = copy.deepcopy(base)
    main = d["sections"]["main"]
    det = main["blocks"]["product-details"]; B = det["blocks"]

    # Tagline under the title, highlights under the price
    B["tagline"] = text("<p><em>{{ closest.product.metafields.custom.tagline.value }}</em></p>", "h5",
                        **{"padding-block-start": 0, "padding-block-end": 0})
    hl = {f"h{k}": row("check_box", "<p>{{ closest.product.metafields.custom.highlight_%d.value }}</p>" % k) for k in (1, 2, 3)}
    B["highlights"] = {"type": "group", "settings": {"gap": 8, "width": "fill"}, "blocks": hl, "block_order": list(hl)}
    # Social proof that is always true: star rating straight from the review app's standard
    # reviews.rating metafield (renders nothing until real reviews exist), accepted payment
    # methods, and the guarantee as a seal.
    hdr = B["group_icgrde"]
    hdr["blocks"]["stars"] = {"type": "review", "settings": {"stars_style": "shaded", "show_number": True,
                              "text_color": ROSE, "width": "fit-content"}, "blocks": {}}
    hdr["block_order"] = [k for k in hdr["block_order"] if k != "stars"]
    hdr["block_order"].insert(hdr["block_order"].index("text_xrnftG") + 1, "stars")
    B["payments"] = {"type": "payment-icons", "settings": {"horizontal_alignment": "flex-start", "gap": 8}, "blocks": {}}
    B["promise"] = {"type": "group", "settings": {"content_direction": "row", "vertical_on_mobile": False, "gap": 14,
                    "vertical_alignment": "center", "width": "fill", "background_color": SAND,
                    "padding-block-start": 14, "padding-block-end": 14, "padding-inline-start": 16, "padding-inline-end": 16},
                    "blocks": {"i": icon("heart", 28),
                               "t": text("<p><strong>The CozyCompanion promise</strong><br>Not completely in love? Return it within 30 days for a full refund of the purchase price.</p>",
                                         "paragraph", width="fit-content")},
                    "block_order": ["i", "t"]}
    det["block_order"] = ["group_icgrde", "tagline", "highlights", "divider_VJhene", "variant_picker_R3rGDr",
                          "buy_buttons_eYQEYi", "payments", "offer", "trust", "promise", "text_aEtTtq", "info"]
    main["blocks"]["media-gallery"]["settings"].update({"media_presentation": "grid", "media_columns": "two",
        "large_first_image": True, "aspect_ratio": "square", "media_fit": "cover", "image_gap": 6})

    if kind == "blanket":
        story = ("l7", "The evening ritual", "Warmth that invites you to slow down.",
                 "<p>Draw the curtains, dim the lights and let gentle warmth do the rest. Our blankets are made for the quiet hours: a good book, a slow film, a companion curled up beside you.</p>")
        steps = [("fire", "1. Unfold &amp; connect", "Spread it over your bed or sofa and connect the controller."),
                 ("lightning_bolt", "2. Choose your warmth", "Pick the setting that feels just right, from a soft glow to deep heat."),
                 ("heart", "3. Unwind", "Let the day melt away. Switch off whenever you're done.")]
        faq = [("How do I wash it?", "<p>Always follow the care label. Disconnect the controller and cable first; many of our blankets can be machine washed on a gentle, cool cycle.</p>"),
               ("Is it safe to use every evening?", "<p>Our blankets are made for everyday comfort. Follow the included instructions, don't use the blanket folded or bunched while it's on, and switch it off when you're done.</p>"),
               ("Does it work outside the EU?", "<p>Check the plug type before ordering: mains-powered blankets come with the plug noted on the product listing. USB blankets work anywhere with a USB power source.</p>"),
               ("What if it's not right for me?", "<p>You have 30 days to return it unused under our happiness guarantee. <a href=\"/pages/returns\">How returns work</a></p>")]
        story_bg = SAND
    else:
        story = ("s_morning", "Care, even when you're away", "Peace of mind, quietly automated.",
                 "<p>Busy mornings, long days, unexpected delays: our smart essentials keep your companion's routine calm and consistent, so you can focus on the moments you spend together.</p>")
        steps = [("box", "1. Unbox &amp; place", "Find a calm spot at home, or clip it to their collar."),
                 ("stopwatch", "2. Set it up", "Follow the included guide; most setups take just a few minutes."),
                 ("paw_print", "3. Relax", "Their routine runs itself; check in whenever you like.")]
        faq = [("Do I need an app?", "<p>It depends on the device: the description above tells you exactly how it's set up. Some work entirely with buttons, others connect to an app on your phone.</p>"),
               ("Is it suitable for cats and dogs?", "<p>Yes, our pet tech is designed for cats and dogs. Check the size and capacity on the product page to match your companion.</p>"),
               ("How is it powered?", "<p>Power details, including what's in the box, are listed in the description above and in the included instructions.</p>"),
               ("What if it's not right for us?", "<p>You have 30 days to return it unused under our happiness guarantee. <a href=\"/pages/returns\">How returns work</a></p>")]
        story_bg = SAND

    sections, order = dict(d["sections"]), list(d["order"])
    # Story block
    sections["story"] = {"type": "media-with-content", "settings": {"media_position": "left", "media_width": "medium",
        "media_height": "60svh", "section_width": "full-width", "background_color": story_bg},
        "blocks": {"media": {"type": "_media-without-appearance", "static": True, "settings": {"media_type": "image", "image": img(story[0])}, "blocks": {}},
                   "content": {"type": "_content-without-appearance", "static": True,
                               "settings": {"horizontal_alignment_flex_direction_column": "flex-start", "vertical_alignment_flex_direction_column": "center", "gap": 18},
                               "blocks": {"e": text(f"<p>{story[1]}</p>", "h6", text_color=ROSE, width="fit-content"),
                                          "h": text(f"<h2>{story[2]}</h2>", "h3", max_width="narrow", width="fit-content"),
                                          "b": text(story[3], "rte", max_width="narrow", width="fit-content")},
                               "block_order": ["e", "h", "b"]}}}
    # How it works
    st = {}
    for k, (ic, h, t) in enumerate(steps):
        st[f"s{k}"] = {"type": "group", "settings": {"gap": 8, "horizontal_alignment_flex_direction_column": "center", "width": "fill"},
                       "blocks": {"i": icon(ic, 28), "h": text(f"<h3>{h}</h3>", "h6", alignment="center"),
                                  "t": text(f"<p>{t}</p>", "rte", alignment="center", max_width="narrow")},
                       "block_order": ["i", "h", "t"]}
    sections["how"] = {"type": "section", "settings": {"content_direction": "column", "gap": 28, "section_width": "page-width",
        "horizontal_alignment_flex_direction_column": "center", "background_color": CREAM,
        "padding-block-start": 56, "padding-block-end": 40},
        "blocks": {"head": text("<h2>How it works</h2>", "h3", alignment="center"),
                   "steps": {"type": "group", "settings": {"content_direction": "row", "vertical_on_mobile": True, "gap": 24,
                             "horizontal_alignment": "space-between", "vertical_alignment": "flex-start", "width": "fill"},
                             "blocks": st, "block_order": list(st)}},
        "block_order": ["head", "steps"]}
    # FAQ
    sections["faq"] = {"type": "section", "settings": {"content_direction": "column", "gap": 20, "section_width": "page-width",
        "background_color": CREAM, "padding-block-start": 24, "padding-block-end": 56},
        "blocks": {"head": text("<h2>Good to know</h2>", "h3", alignment="center"), "acc": accordion(faq)},
        "block_order": ["head", "acc"]}
    rec = [k for k in order if k.startswith("product_recommendations")]
    order = ["main", "story", "how", "faq"] + rec
    d["sections"], d["order"] = sections, order
    return HEADER + "\n" + json.dumps(d, indent=2)

print(put_theme_files({"templates/product.blanket.json": build("blanket"),
                       "templates/product.pettech.json": build("pettech")}))
