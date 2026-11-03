"""Cart drawer fix (2026-11-03): the product lines were squeezed to ~0px because the sticky summary at the bottom held the
upsell carousel + totals + buttons + trust row, so shoppers could not see what was in their cart.
Now: product lines first, then the upsells and trust row, all in one scrolling area; only totals + checkout stay sticky.
Patches snippets/cart-drawer.liquid (original kept in theme-backup/snippets__cart-drawer.liquid.orig)."""
import os
from lib import theme_file, put_theme_files, S

F = "snippets/cart-drawer.liquid"
bak = os.path.join(S, "theme-backup", "snippets__cart-drawer.liquid.orig")
if not os.path.exists(bak):
    open(bak, "w").write(theme_file(F))
src = open(bak).read()

OLD = """                <scroll-hint class="cart-drawer__items">
                  {% render 'cc-cart-perks', part: 'top' %}
                  {% render 'cart-products', context: 'drawer' %}
                </scroll-hint>

                <div class="cart-drawer__summary">
                  {% render 'cc-cart-perks', part: 'upsells' %}
                  {% render 'cart-summary', section_id: 'cart-drawer-section' %}
                  {% render 'cc-cart-perks', part: 'bottom' %}
                </div>"""
NEW = """                <scroll-hint class="cart-drawer__items">
                  {% render 'cc-cart-perks', part: 'top' %}
                  {% render 'cart-products', context: 'drawer' %}
                  <div class="cc-cart-extras">
                    {% render 'cc-cart-perks', part: 'upsells' %}
                    {% render 'cc-cart-perks', part: 'bottom' %}
                  </div>
                </scroll-hint>

                <div class="cart-drawer__summary">
                  {% render 'cart-summary', section_id: 'cart-drawer-section' %}
                </div>"""
assert src.count(OLD) == 1, "drawer anchor not found"
src = src.replace(OLD, NEW)

CSS = """
  /* CozyCompanion: one scrolling area (lines, upsells, trust row); only totals + checkout stay sticky */
  .cart-drawer__content .cart-drawer__items { flex: 1 0 auto; overflow: visible; }
  .cc-cart-extras { margin-top: var(--gap-xl, 24px); padding-bottom: 8px; }
  .cc-cart-extras .cc-upsells { margin-block-end: 8px; }
{% endstylesheet %}"""
assert src.count("{% endstylesheet %}") == 1
src = src.replace("{% endstylesheet %}", CSS)
put_theme_files({F: src})
print("patched", F)
