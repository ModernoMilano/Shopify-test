import sys, json, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import theme_file
for f in sys.argv[1:]:
    src = theme_file(f)
    m = re.search(r"\{%-?\s*schema\s*-?%\}(.*?)\{%-?\s*endschema\s*-?%\}", src, re.S)
    d = json.loads(m.group(1))
    print("=====", f, "blocks:", [b.get("type") for b in d.get("blocks", [])])
    for x in d.get("settings", []):
        if "id" in x:
            opts = [o["value"] for o in x.get("options", [])] if x.get("options") else ""
            print("  ", x["id"], x["type"], repr(x.get("default", ""))[:40], opts if opts else "", x.get("visible_if","")[:60] if x.get("visible_if") else "")
