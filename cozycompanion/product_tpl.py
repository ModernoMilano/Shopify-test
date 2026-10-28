import sys, json, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import put_theme_files
ROSE, LINE = "#b76e79", "#e3dbd2"
r = open(os.path.join(S, "theme-backup", "templates__product.json")).read(); i = r.index("*/") + 2
d = json.loads(r[i:])
main = d["sections"]["main"]
det = main["blocks"]["product-details"]
B = det["blocks"]

def text(t, preset="rte", **kw):
    s = {"text": t, "type_preset": preset, "width": "100%"}; s.update(kw)
    return {"type": "text", "settings": s, "blocks": {}}

# Eyebrow above title + subtle "tax included" line
hdr = B["group_icgrde"]
hdr["blocks"]["eyebrow"] = text("<p>CozyCompanion</p>", "h6", text_color=ROSE)
hdr["block_order"] = ["eyebrow", "text_xrnftG", "price_tVjtKg"]
hdr["blocks"]["price_tVjtKg"]["settings"]["show_tax_info"] = True

# Trust row under the buy buttons
trust, order = {}, []
for k, (icon, t) in enumerate([("truck", "Tracked shipping around the world"), ("return", "30-day happiness guarantee"),
                               ("lock", "Secure, encrypted checkout")]):
    trust[f"t{k}"] = {"type": "group", "settings": {"content_direction": "row", "vertical_on_mobile": False, "gap": 10,
                      "vertical_alignment": "center", "width": "fill"},
                      "blocks": {"i": {"type": "icon", "settings": {"icon": icon, "width": 20, "icon_color": ROSE}, "blocks": {}},
                                 "x": text(f"<p>{t}</p>", "paragraph", width="fit-content")},
                      "block_order": ["i", "x"]}
    order.append(f"t{k}")
B["trust"] = {"type": "group", "settings": {"content_direction": "column", "gap": 10, "width": "fill",
              "padding-block-start": 4, "padding-block-end": 4}, "blocks": trust, "block_order": order}

# Offer nudge
B["offer"] = text("<p>New here? Enjoy <strong>15% off your first order</strong> with code <strong>COZY15</strong>.</p>",
                  "paragraph", background=True, background_color="#efe4e1", corner_radius=0,
                  **{"padding-block-start": 12, "padding-block-end": 12, "padding-inline-start": 16, "padding-inline-end": 16})

# Accordion: shipping / returns / care
def row(h, icon, body, open_=False):
    return {"type": "_accordion-row", "settings": {"heading": h, "icon": icon, "open_by_default": open_},
            "blocks": {"t": text(body)}, "block_order": ["t"]}
B["info"] = {"type": "accordion", "settings": {"icon": "plus", "dividers": True, "divider_color": LINE, "type_preset": "h6"},
    "blocks": {
        "ship": row("Shipping", "truck", "<p>Prepared within 1&ndash;3 business days and shipped with tracking on every order: delivery across the US in 5&ndash;12 business days. <a href=\"/pages/shipping\">Shipping details</a></p>"),
        "ret": row("30-day returns", "return", "<p>Not completely in love? Return it unused within 30 days of delivery. <a href=\"/pages/returns\">How returns work</a></p>"),
        "care": row("Care & safe use", "washing", "<p>Always follow the care label and the instructions included with your product. For heated blankets, disconnect the controller before washing and never use the blanket folded while it's switched on.</p>"),
        "help": row("Questions?", "chat_bubble", "<p>We're happy to help. <a href=\"/pages/contact\">Send us a message</a> and we'll reply within 1&ndash;2 business days, or browse our <a href=\"/pages/faq\">FAQ</a>.</p>"),
    }, "block_order": ["ship", "ret", "care", "help"]}

det["block_order"] = ["group_icgrde", "divider_VJhene", "variant_picker_R3rGDr", "buy_buttons_eYQEYi",
                      "offer", "trust", "text_aEtTtq", "info"]
main["blocks"].pop("disclosures_g9mWze", None)
main["block_order"] = []
# Owner's choice: no Shop Pay / "More payment options" buttons on the product page
B["buy_buttons_eYQEYi"]["blocks"]["accelerated-checkout"]["disabled"] = True
main["blocks"]["media-gallery"]["settings"].update({"media_presentation": "carousel", "aspect_ratio": "square",
                                                    "media_fit": "cover", "large_first_image": True})
rec = d["sections"]["product_recommendations_qggXJq"]
rec["blocks"]["text_cbcgyb"]["settings"]["text"] = "<h3>Pairs well with</h3>"
print(put_theme_files({"templates/product.json": r[:i] + "\n" + json.dumps(d, indent=2)}))
