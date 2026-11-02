"""Product cards: replace the "Sale" badge with the real discount percentage.

Per variant: (compare_at - price) * 100 / compare_at, rounded down (integer cents), so the badge never overstates.
All on-sale variants equal -> "-36%"; variants differ -> "Up to -40%" (the largest).
Patches blocks/_product-card-gallery.liquid (original kept in theme-backup/)."""
import os
from lib import theme_file, put_theme_files, S

F = "blocks/_product-card-gallery.liquid"
bak = os.path.join(S, "theme-backup", "blocks___product-card-gallery.liquid")
if not os.path.exists(bak):
    open(bak, "w").write(theme_file(F))
src = open(bak).read()

OLD = """          {%- elsif product.compare_at_price > product.price -%}
            {{ 'content.product_badge_sale' | t }}
          {%- endif -%}"""
NEW = """          {%- elsif product.compare_at_price > product.price -%}
            {%- liquid
              # CozyCompanion: show the discount percentage instead of "Sale"
              assign cc_max = 0
              assign cc_min = 100
              for v in product.variants
                if v.compare_at_price > v.price
                  assign cc_off = v.compare_at_price | minus: v.price | times: 100 | divided_by: v.compare_at_price
                  if cc_off > cc_max
                    assign cc_max = cc_off
                  endif
                  if cc_off < cc_min
                    assign cc_min = cc_off
                  endif
                endif
              endfor
            -%}
            {%- if cc_max > 0 -%}
              <span class="cc-badge-pct">{% if cc_min != cc_max %}Up to {% endif %}-{{ cc_max }}%</span>
            {%- else -%}
              {{ 'content.product_badge_sale' | t }}
            {%- endif -%}
          {%- endif -%}"""
assert src.count(OLD) == 1
put_theme_files({F: src.replace(OLD, NEW)})
print("patched", F)
