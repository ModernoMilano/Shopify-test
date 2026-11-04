"""Cart buttons in the CozyCompanion style (owner, 2026-11-03: "de knoppen in de cart ... zien er standaard uit").
Checkout: charcoal, lock icon, "Secure checkout · $total", rose-gold on hover. Express buttons are off in the cart
(owner 2026-11-04: calmer cart; they still show in checkout); a compact USP row sits right under the checkout button. Patches snippets/cart-summary.liquid (original kept in
theme-backup/snippets__cart-summary.liquid.orig)."""
import os
from lib import theme_file, put_theme_files, S

F = "snippets/cart-summary.liquid"
bak = os.path.join(S, "theme-backup", "snippets__cart-summary.liquid.orig")
if not os.path.exists(bak):
    open(bak, "w").write(theme_file(F))
src = open(bak).read()

OLD_BTN = """    <span class="button-text">
      {{ 'content.checkout' | t }}
    </span>
  </button>"""
NEW_BTN = """    <span class="button-text cc-checkout__text">
      <svg class="cc-checkout__lock" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="4.5" y="10.5" width="15" height="10" rx="1.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/></svg>
      <span>Secure checkout</span>
      {%- if cart != empty -%}<span class="cc-checkout__sep" aria-hidden="true"></span><span class="cc-checkout__total">{{ cart.total_price | money }}</span>{%- endif -%}
    </span>
  </button>"""
assert src.count(OLD_BTN) == 1, "checkout button anchor"
src = src.replace(OLD_BTN, NEW_BTN)

OLD_EXP = """      {{ content_for_additional_checkout_buttons }}
    </div>
  {% endif %}"""
NEW_EXP = """      {{ content_for_additional_checkout_buttons }}
    </div>
  {% endif %}
  {%- if cart != empty -%}
    <ul class="cc-ctas-usps" role="list">
      <li>{% render 'cc-icon', name: 'truck' %}<span>Free shipping &middot; 3&ndash;5 days</span></li>
      <li>{% render 'cc-icon', name: 'return' %}<span>30-day returns</span></li>
      <li>{% render 'cc-icon', name: 'lock' %}<span>Secure checkout</span></li>
    </ul>
  {%- endif -%}"""
assert src.count(OLD_EXP) == 1, "express anchor"
src = src.replace(OLD_EXP, NEW_EXP)

STYLE = """
<style>
  /* CozyCompanion cart buttons */
  .cart__ctas { gap: 10px; }
  .cart__ctas .cart__checkout-button.button {
    height: 56px; min-height: 56px; border-radius: 2px; border: 0; background: #1a1a1a; color: #f5f1ed;
    box-shadow: 0 10px 24px -14px rgba(26, 26, 26, 0.55); transition: background 0.25s ease, transform 0.15s ease;
    font-family: var(--font-body--family, 'Jost', sans-serif);
  }
  .cart__ctas .cart__checkout-button.button:hover:not([disabled]) { background: #b76e79; }
  .cart__ctas .cart__checkout-button.button:active:not([disabled]) { transform: translateY(1px); }
  .cc-checkout__text { display: inline-flex; align-items: center; justify-content: center; gap: 10px;
    font-size: 0.78rem; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; line-height: 1; }
  .cc-checkout__lock { flex: 0 0 auto; margin-top: -2px; }
  .cc-checkout__sep { width: 1px; height: 14px; background: rgba(245, 241, 237, 0.4); }
  .cc-checkout__total { letter-spacing: 0.06em; font-weight: 400; }
  .cart__ctas .additional-checkout-buttons { display: grid; gap: 8px; }
  .cc-express__label { margin: 2px 0 0; display: flex; align-items: center; gap: 12px; font-size: 0.66rem;
    letter-spacing: 0.16em; text-transform: uppercase; color: rgba(26, 26, 26, 0.55); }
  .cc-express__label::before, .cc-express__label::after { content: ''; flex: 1; height: 1px; background: #e3dbd2; }
  .cart__ctas shopify-accelerated-checkout-cart {
    --shopify-accelerated-checkout-button-block-size: 48px;
    --shopify-accelerated-checkout-button-border-radius: 2px;
    --shopify-accelerated-checkout-row-gap: 8px;
  }
  .cc-ctas-usps { list-style: none; margin: 2px 0 0; padding: 0; display: flex; justify-content: space-between; gap: 6px; }
  .cc-ctas-usps li { display: flex; align-items: center; gap: 5px; font-size: 0.7rem; line-height: 1.2; color: rgba(26, 26, 26, 0.85); }
  .cc-ctas-usps svg { width: 15px; height: 15px; flex: 0 0 auto; color: #b76e79; }
  @media (max-width: 749px) {
    .cart__ctas .cart__checkout-button.button { height: 54px; min-height: 54px; }
    .cc-checkout__text { font-size: 0.74rem; letter-spacing: 0.14em; gap: 8px; }
  }
</style>
"""
src = src.replace("{% stylesheet %}", STYLE + "\n{% stylesheet %}", 1)
put_theme_files({F: src})
print("patched", F)
