"""Product pages: remove the 'run from overseas' signals (owner approved 2026-11-05).
1. Trust row: 'Tracked worldwide' / 'Tracked shipping around the world' (plane) -> 'Free shipping · 3–5 days' (truck)
2. "Duties and taxes included" is not shown to US visitors (tax-info snippet + price block; other markets keep it)
3. Payment icons: only the methods US shoppers know (Amex, Apple Pay, Google Pay, Mastercard, PayPal, Shop Pay, Visa)
4. Highlights in °C -> °F (product metafields custom.highlight_1..3)
5. The generic story banner (the human heated-blanket / Aussie-dog image) is switched off on product pages
Originals in theme-backup/*.pre-pdp-trust."""
import os, json, re
from lib import gql, check, theme_file, put_theme_files, THEME, S

def backup(name):
    p = os.path.join(S, "theme-backup", name.replace("/", "__") + ".pre-pdp-trust")
    if not os.path.exists(p):
        open(p, "w").write(theme_file(name))
    return open(p).read()

files = {}
# 1 + 5: product templates
names = [n["filename"] for n in gql('query($id:ID!){theme(id:$id){files(first:50,filenames:["templates/product*.json"]){nodes{filename}}}}',
                                    {"id": THEME})["theme"]["files"]["nodes"]]
def walk(blocks):
    n = 0
    for b in (blocks or {}).values():
        kids = b.get("blocks") or {}
        texts = [k for k in kids.values() if k.get("type") == "text"]
        if any(re.search(r"Tracked (worldwide|shipping around the world)", t.get("settings", {}).get("text", "")) for t in texts):
            for k in kids.values():
                if k.get("type") == "text": k["settings"]["text"] = "<p>Free shipping</p>"
                if k.get("type") == "icon": k["settings"]["icon"] = "truck"
            n += 1
        n += walk(kids)
    return n
for name in names:
    if name.endswith("giftcard.json"): continue
    t = backup(name); head, j = t[:t.find("{")], json.loads(t[t.find("{"):])
    changed = sum(walk(sec.get("blocks")) for sec in j["sections"].values())
    if "story" in j["sections"]:
        j["sections"]["story"]["disabled"] = True; changed += 1
    if changed: files[name] = head + json.dumps(j, indent=2)
    print(name, "changes:", changed)

# 2: tax/duties line hidden for US visitors
t = backup("snippets/tax-info.liquid")
assert t.count("<small>") == 1 and t.count("</small>") == 1
files["snippets/tax-info.liquid"] = (t.replace("<small>", "{%- unless localization.country.iso_code == 'US' -%}\n<small>")
                                      .replace("</small>", "</small>\n{%- endunless -%}"))
# 3: payment icons US shoppers know
t = backup("blocks/payment-icons.liquid")
old = """    {%- for type in shop.enabled_payment_types -%}
      <li class="payment-icons__item">
        {{ type | payment_type_svg_tag: class: 'icon icon--full-color' }}
      </li>
    {%- endfor -%}"""
assert t.count(old) == 1, "payment icons anchor"
files["blocks/payment-icons.liquid"] = t.replace(old, """    {%- assign cc_keep = 'american_express,apple_pay,google_pay,master,paypal,shopify_pay,visa' | split: ',' -%}
    {%- for type in shop.enabled_payment_types -%}
      {%- unless cc_keep contains type -%}{%- continue -%}{%- endunless -%}
      <li class="payment-icons__item">
        {{ type | payment_type_svg_tag: class: 'icon icon--full-color' }}
      </li>
    {%- endfor -%}""")
put_theme_files(files); print("theme:", list(files))

# 4: °C highlights -> °F
def c2f(m):
    a, b = int(m.group(1)), int(m.group(2))
    return f"{round(a * 9 / 5 + 32)}–{round(b * 9 / 5 + 32)} °F"
after, mf = None, []
while True:
    r = gql("""query($a:String){products(first:100,after:$a,query:"status:active"){nodes{id title
               h1: metafield(namespace:"custom",key:"highlight_1"){value} h2: metafield(namespace:"custom",key:"highlight_2"){value}
               h3: metafield(namespace:"custom",key:"highlight_3"){value}} pageInfo{hasNextPage endCursor}}}""", {"a": after})["products"]
    for p in r["nodes"]:
        for i, h in ((1, "h1"), (2, "h2"), (3, "h3")):
            v = (p[h] or {}).get("value") or ""
            if "°C" in v or "℃" in v:
                nv = re.sub(r"(\d+)\s*[–-]\s*(\d+)\s*(°C|℃)", c2f, v)
                nv = re.sub(r"(\d+)\s*(°C|℃)", lambda m: f"{round(int(m.group(1)) * 9 / 5 + 32)} °F", nv)
                print(f"  {p['title'][:34]:34} {v!r} -> {nv!r}")
                mf.append({"ownerId": p["id"], "namespace": "custom", "key": f"highlight_{i}", "type": "single_line_text_field", "value": nv})
    if not r["pageInfo"]["hasNextPage"]: break
    after = r["pageInfo"]["endCursor"]
if mf:
    check(gql("mutation($m:[MetafieldsSetInput!]!){metafieldsSet(metafields:$m){userErrors{field message}}}", {"m": mf})["metafieldsSet"])
print("highlights fixed:", len(mf))
