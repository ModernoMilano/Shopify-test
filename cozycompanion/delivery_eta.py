"""Replace the bare 'Ships from: International warehouse / United States' line with an honest delivery estimate
(owner, 2026-11-03: "idk what you think" -> my advice). Numbers come from /pages/shipping: dispatch 1-3 business days,
then 3-7 (US warehouse) or 7-12 (international warehouses) business days => 4-10 / 8-15 business days in total.
Product page: "Estimated delivery: Nov 10 – Nov 17" (dates computed in the visitor's browser, weekends skipped).
Cart: the 'Ships from' value is no longer listed. Originals kept in theme-backup/*.orig."""
import os
from lib import theme_file, put_theme_files, S

def base(name):
    p = os.path.join(S, "theme-backup", name.replace("/", "__") + ".orig")
    if not os.path.exists(p):
        open(p, "w").write(theme_file(name))
    return open(p).read()

files = {}
# --- product page variant picker
F = "snippets/variant-main-picker.liquid"; src = base(F)
OLD = """        {%- if product_option.values.size == 1 and variant_style != 'swatch' -%}
          <div
            class="variant-option"
            data-testid="variant-option-single"
          >"""
NEW = """        {%- if product_option.name == 'Ships from' and product_option.values.size == 1 -%}
          {%- liquid
            if product_option.selected_value == 'United States'
              assign cc_eta_min = 4
              assign cc_eta_max = 10
            else
              assign cc_eta_min = 8
              assign cc_eta_max = 15
            endif
          -%}
          <div class="variant-option cc-eta" data-cc-eta="{{ cc_eta_min }},{{ cc_eta_max }}">
            <svg class="cc-eta__icon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6.5h11v9H3z"/><path d="M14 9.5h3.5l3 3v3H14z"/><circle cx="7" cy="17.5" r="1.6"/><circle cx="17" cy="17.5" r="1.6"/></svg>
            <span>Estimated delivery: <b class="cc-eta__dates">{{ cc_eta_min }}&ndash;{{ cc_eta_max }} business days</b> <span class="cc-eta__note">&middot; tracked</span></span>
          </div>
          <script>
            (function () {
              function add(d, n) { d = new Date(d); while (n > 0) { d.setDate(d.getDate() + 1); var w = d.getDay(); if (w !== 0 && w !== 6) n--; } return d; }
              var f = { month: 'short', day: 'numeric' };
              document.querySelectorAll('.cc-eta[data-cc-eta]:not([data-done])').forEach(function (el) {
                var r = el.getAttribute('data-cc-eta').split(','), now = new Date();
                var a = add(now, +r[0]).toLocaleDateString('en-US', f), b = add(now, +r[1]).toLocaleDateString('en-US', f);
                el.querySelector('.cc-eta__dates').textContent = a + ' \\u2013 ' + b; el.setAttribute('data-done', '1');
              });
            })();
          </script>
          <style>
            .cc-eta { display: flex; align-items: center; gap: 10px; padding: 12px 14px; background: #ebe3da; font-size: 0.9rem; line-height: 1.35; }
            .cc-eta__icon { color: #b76e79; flex: 0 0 auto; }
            .cc-eta b { font-weight: 500; }
            .cc-eta__note { opacity: 0.7; }
          </style>
        {%- elsif product_option.values.size == 1 and variant_style != 'swatch' -%}
          <div
            class="variant-option"
            data-testid="variant-option-single"
          >"""
assert src.count(OLD) == 1, "picker anchor"
files[F] = src.replace(OLD, NEW)

# --- cart line items
F2 = "snippets/cart-products.liquid"; src2 = base(F2)
OLD2 = """                          {%- for option in item.options_with_values -%}
                            <div class="cart-items__variant">
                              <dt class="visually-hidden">{{ option.name }}:</dt>
                              <dd>
                                {{- option.value -}}
                                {%- if forloop.last != true %},&nbsp;{% endif -%}
                              </dd>
                            </div>
                          {%- endfor -%}"""
NEW2 = """                          {%- for option in item.options_with_values -%}
                            {%- if option.name == 'Ships from' -%}{%- continue -%}{%- endif -%}
                            <div class="cart-items__variant cc-variant">
                              <dt class="visually-hidden">{{ option.name }}:</dt>
                              <dd>
                                {{- option.value -}}
                              </dd>
                            </div>
                          {%- endfor -%}"""
assert src2.count(OLD2) == 1, "cart anchor"
src2 = src2.replace(OLD2, NEW2)
src2 = src2.replace("{% stylesheet %}", "<style>.cc-variant:not(:last-child) dd::after { content: ','; }</style>\n{% stylesheet %}", 1)
files[F2] = src2
put_theme_files(files)
print("patched", ", ".join(files))
