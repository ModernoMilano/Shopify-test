import sys, json, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import put_theme_files
CHAR, ROSE, CREAM = "#1a1a1a", "#b76e79", "#f5f1ed"
def load(f):
    r = open(os.path.join(S, "theme-backup", f)).read(); i = r.index("*/") + 2
    return r[:i], json.loads(r[i:])

# Header
hh, h = load("sections__header-group.json")
ann = h["sections"]["header_announcements_9jGBFp"]
msgs = ["Join the Cozy Circle: 15% off your first order with code COZY15",
        "30-day happiness guarantee on every order",
        "Free tracked shipping on orders over $150"]
links = ["shopify://collections/smart-pet-tech", "shopify://pages/returns", "shopify://pages/shipping"]
ann["blocks"] = {f"a{i}": {"type": "_announcement", "settings": {"text": m, "link": l, "font_size": "0.75rem",
                 "case": "uppercase", "letter_spacing": "loose", "text_color": CREAM}, "blocks": {}}
                 for i, (m, l) in enumerate(zip(msgs, links))}
ann["block_order"] = ["a0", "a1", "a2"]
ann["settings"].update({"background_color": CHAR, "divider_width": 0, "speed": 5,
                        "padding-block-start": 10, "padding-block-end": 10})
hs = h["sections"]["header_section"]
hs["settings"].update({"logo_position": "center", "menu_position": "left", "show_language": False,
                       "show_country": False, "background_color_top": CREAM, "text_color_top": CHAR,
                       "divider_width": 1, "divider_color": "#e3dbd2", "enable_sticky_header": "scroll-up"})
hs["blocks"]["header-menu"]["settings"].update({"menu_style": "collection_images", "type_case_primary_link": "uppercase",
    "type_font_primary_size": "0.75rem", "background_color": CREAM, "drawer_dividers": True,
    "drawer_accordion": True, "drawer_accordion_expand_first": True, "menu_font_style": "regular"})

# Footer
fh, f = load("sections__footer-group.json")
def text(t, preset="rte", color=CREAM, width="100%"):
    return {"type": "text", "settings": {"text": t, "type_preset": preset, "text_color": color, "width": width}, "blocks": {}}
def menu(handle, heading):
    return {"type": "menu", "settings": {"menu": handle, "heading": heading, "heading_preset": "h6", "link_preset": "paragraph",
            "text_color": CREAM, "menu_spacing": 10, "show_as_accordion": False}, "blocks": {}}
foot = f["sections"]["footer_m9NzUG"]
foot["blocks"] = {
    "brand": {"type": "group", "settings": {"gap": 14, "width": "fill"}, "blocks": {
        "name": {"type": "logo", "settings": {"inverse": True, "unit": "pixel", "pixel_height": 32}, "blocks": {}},
        "about": text("<p>Luxury comfort for you and your companions. Heated blankets and smart pet essentials, thoughtfully curated for the quiet moments at home.</p><p>Questions? <a href=\"mailto:cozycompanion.us@gmail.com\">cozycompanion.us@gmail.com</a></p>"),
        "signup_h": text("<p><strong>Join the Cozy Circle</strong> and get 15% off your first order with code COZY15.</p>"),
        "signup": {"type": "email-signup", "settings": {"width": "fill", "heading": "", "input_style": "custom",
                   "input_background_color": CREAM, "input_text_color": CHAR, "style_class": "button-custom",
                   "custom_button_background": ROSE, "custom_button_text": "#ffffff", "custom_button_border": ROSE,
                   "display_type": "text", "label": "Join"}, "blocks": {}},
        "payments": {"type": "payment-icons", "settings": {"horizontal_alignment": "flex-start", "gap": 8}, "blocks": {}}},
        "block_order": ["name", "about", "signup_h", "signup", "payments"]},
    "shop": menu("footer-shop", "Shop"),
    "help": menu("footer", "Customer care"),
    "legal": menu("footer-legal", "Legal"),
}
foot["block_order"] = ["brand", "shop", "help", "legal"]
foot["settings"].update({"background_color": CHAR, "gap": 48, "padding-block-start": 72, "padding-block-end": 48})

util = f["sections"]["footer_utilities_jLGE8U"]
util["blocks"] = {
    "copyright": {"type": "footer-copyright", "settings": {"show_powered_by": False, "font_size": "0.75rem", "text_color": CREAM}, "blocks": {}},
}
util["block_order"] = ["copyright"]
util["settings"].update({"background_color": CHAR, "divider_color": "#3a3a3a"})

print(put_theme_files({"sections/header-group.json": hh + "\n" + json.dumps(h, indent=2),
                       "sections/footer-group.json": fh + "\n" + json.dumps(f, indent=2)}))
