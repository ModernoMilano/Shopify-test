"""Collection pages: CozyCompanion header with category chips (cc-collection-nav) above the product grid."""
import sys, os, json, re
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import theme_file, put_theme_files

raw = theme_file("templates/collection.json")
header = re.match(r"\s*/\*.*?\*/\s*", raw, flags=re.S)
d = json.loads(raw[header.end() if header else 0:])
d["sections"] = {k: v for k, v in d["sections"].items() if k != "section"}
d["sections"]["cc_nav"] = {"type": "cc-collection-nav", "settings": {}}
d["order"] = ["cc_nav"] + [k for k in d["order"] if k not in ("section", "cc_nav")]
main = d["sections"]["main"]
main["settings"].update({"columns_gap_horizontal": 16, "columns_gap_vertical": 32, "padding-block-start": 8})
print(put_theme_files({"sections/cc-collection-nav.liquid": open(os.path.join(S, "cc-collection-nav.liquid")).read(),
                       "templates/collection.json": (header.group(0) if header else "") + json.dumps(d, indent=2)}))
