"""Brand the Shopify cookie banner: upload snippets/cc-privacy-banner.liquid and render it in the layout
(right after the signup popup). Safe to re-run."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import theme_file, put_theme_files

lay = theme_file("layout/theme.liquid")
if "cc-privacy-banner" not in lay:
    assert "{% render 'cc-signup-popup' %}" in lay
    lay = lay.replace("{% render 'cc-signup-popup' %}", "{% render 'cc-signup-popup' %}\n    {% render 'cc-privacy-banner' %}", 1)
print(put_theme_files({"snippets/cc-privacy-banner.liquid": open(os.path.join(S, "cc-privacy-banner.liquid")).read()}))
print(put_theme_files({"layout/theme.liquid": lay}))
