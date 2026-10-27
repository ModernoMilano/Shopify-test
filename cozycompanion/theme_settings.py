import sys, json, re, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import put_theme_files
raw = open(os.path.join(S, "theme-backup", "config__settings_data.json")).read()
data = json.loads(raw[raw.index("*/") + 2:])
c = data["current"]
CHAR, ROSE, CREAM, LINE = "#1a1a1a", "#b76e79", "#f5f1ed", "#e3dbd2"
c["color_palette"] = {"background": CREAM, "foreground": CHAR, "color1": ROSE, "color2": LINE}
c.update({
    "type_heading_font": sys.argv[1], "type_accent_font": sys.argv[1],
    "type_body_font": sys.argv[2], "type_subheading_font": sys.argv[3],
    "type_size_paragraph": "16", "type_line_height_paragraph": "body-loose",
    "type_size_h1": "56", "type_size_h2": "44", "type_size_h3": "32", "type_size_h4": "24",
    "type_font_h4": "heading", "type_case_h5": "uppercase", "type_letter_spacing_h5": "heading-loose",
    "type_case_h6": "uppercase", "type_letter_spacing_h6": "heading-loose",
    "page_width": "normal",
    "card_hover_effect": "subtle-zoom", "page_transition_enabled": False,
    "badge_position": "top-left", "badge_corner_radius": 0,
    "badge_sale_background_color": ROSE, "badge_sale_text_color": "#ffffff",
    "badge_sold_out_background_color": LINE, "badge_text_transform": "uppercase",
    "palette_primary_button_background": CHAR, "palette_primary_button_text": CREAM,
    "palette_primary_button_border": CHAR, "button_border_radius_primary": 0,
    "palette_secondary_button_background": "rgba(0,0,0,0)", "palette_secondary_button_text": CHAR,
    "palette_secondary_button_border": CHAR, "button_border_radius_secondary": 0,
    "button_text_case_primary": "uppercase", "button_text_case_secondary": "uppercase",
    "inputs_border_radius": 0, "popover_border_radius": 0, "card_corner_radius": 0,
    "variant_button_radius": 0, "cart_type": "drawer", "auto_open_cart_drawer": True,
    "show_add_discount_code": True, "show_accelerated_checkout_buttons": True,
    "currency_code_enabled_product_cards": False, "currency_code_enabled_product_pages": False,
    "empty_cart_button_link": "shopify://collections/cozy-heated-blankets",
    "drawer_border_color": LINE, "popover_border_color": LINE, "palette_input_border": LINE,
    "logo_height": 36, "logo_height_mobile": 28,
    "logo": "shopify://shop_images/cozycompanion-logo-dark.png", "logo_inverse": "shopify://shop_images/cozycompanion-logo-light.png",
})
if len(sys.argv) > 4: c["favicon"] = sys.argv[4]
out = raw[: raw.index("*/") + 2] + "\n" + json.dumps(data, indent=2)
print(put_theme_files({"config/settings_data.json": out}))
