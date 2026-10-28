"""Owner's choice: no payment icons anywhere (cart drawer, product pages, footer)."""
import sys, os, json, re
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import theme_file, put_theme_files

def strip_blocks(node):
    """Remove every payment-icons block from a section/block tree; return how many were removed."""
    n = 0
    for key in ("sections", "blocks"):
        kids = node.get(key)
        if not isinstance(kids, dict): continue
        for bid in [b for b, v in kids.items() if v.get("type") == "payment-icons" or "payment" in v.get("type", "") and "icons" in v.get("type", "")]:
            del kids[bid]; n += 1
            for o in ("order", "block_order"):
                if bid in node.get(o, []): node[o].remove(bid)
        for v in kids.values(): n += strip_blocks(v)
    s = node.get("settings", {})
    for k in [k for k in s if "payment" in k and isinstance(s[k], bool)]:
        if s[k]: s[k] = False; n += 1
    return n

files = {}
for name in ("sections/footer-group.json", "templates/product.blanket.json", "templates/product.pettech.json"):
    raw = theme_file(name)
    head = re.match(r"\s*/\*.*?\*/\s*", raw, re.S)
    data = json.loads(raw[head.end():] if head else raw)
    n = strip_blocks(data)
    print(name, "removed:", n)
    if n: files[name] = (head.group(0) if head else "") + json.dumps(data, indent=2)
files.update(json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {})
print(put_theme_files(files))
