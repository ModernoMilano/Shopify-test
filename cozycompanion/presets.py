import sys, json, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import theme_file
f = sys.argv[1]
src = theme_file(f)
m = re.search(r"\{%-?\s*schema\s*-?%\}(.*?)\{%-?\s*endschema\s*-?%\}", src, re.S)
d = json.loads(m.group(1))
for p in d.get("presets", [])[: int(sys.argv[2]) if len(sys.argv) > 2 else 1]:
    print(json.dumps(p, indent=0)[:6000])
