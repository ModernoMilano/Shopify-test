import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check, product_ids
# title: (template, tagline, [highlights]) - only features we actually know from the supplier listing
CONTENT = {
    "Smart Pet Feeder Camera 1080P HD": ("pettech", "Mealtime, beautifully handled, even when you're away.",
        ["1080P HD camera view of home", "Scheduled, portioned meals", "Refined design for elegant interiors"]),
    "Automatic Pet Feeder Smart Sensor": ("pettech", "Effortless nourishment, precisely timed.",
        ["Smart sensor dispensing", "Portion control for a healthy routine", "Minimal, modern silhouette"]),
    "Smart Mini GPS Pet Tracker": ("pettech", "Freedom for them. Reassurance for you.",
        ["Location tracking on your phone", "Featherlight, clips to any collar", "For cats and dogs alike"]),
    "Premium Pet Water Fountain 68oz": ("pettech", "Fresh, flowing water, an everyday luxury.",
        ["Generous 68oz (approx. 2L) capacity", "Circulating, filtered water", "Encourages pets to drink more"]),
    "Laura Hill Electric Heated Blanket Double": ("blanket", "Warmth made for two.",
        ["Double size for bed or sofa", "Adjustable warmth settings", "Plush, soft-touch finish"]),
    "USB Powered Heated Blanket 3 Settings": ("blanket", "Your personal warmth, wherever you settle.",
        ["3 heat settings", "USB powered: power bank, laptop or adapter", "Lightweight and easy to take along"]),
    "Weighted Heated Blanket 9kg": ("blanket", "The feeling of being held, with warmth to match.",
        ["9kg evenly distributed weight", "Soothing, adjustable heat", "Designed for deep relaxation"]),
    "Pet-Specific Heated Blanket Washable": ("blanket", "Because they deserve to be cosy, too.",
        ["Designed especially for pets", "Washable for easy care", "Soft, plush curl-up surface"]),
}
ids = product_ids()
for title, (tpl, tag, hl) in CONTENT.items():
    pid = ids[title]
    check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){product{id} userErrors{field message}}}",
              {"p": {"id": pid, "templateSuffix": tpl}})["productUpdate"], title)
    mf = [{"ownerId": pid, "namespace": "custom", "key": "tagline", "type": "single_line_text_field", "value": tag}]
    mf += [{"ownerId": pid, "namespace": "custom", "key": f"highlight_{i+1}", "type": "single_line_text_field", "value": h} for i, h in enumerate(hl)]
    check(gql("mutation($m:[MetafieldsSetInput!]!){metafieldsSet(metafields:$m){userErrors{field message}}}", {"m": mf})["metafieldsSet"], title)
    print("ok", tpl, title)
