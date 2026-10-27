"""Short product descriptions: one line, max four bullets, one spec line."""
import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
def d(lead, bullets, spec):
    return f"<p>{lead}</p><ul>" + "".join(f"<li>{b}</li>" for b in bullets) + f"</ul><p><small>{spec}</small></p>"
COPY = {
 "plush-heat-pad": d("Targeted warmth for your lap, back or shoulders.",
    ["Thick, velvety flannel", "Warm in about 15 minutes", "Detachable controller, long cord", "Overheating protection"],
    "60 × 30 cm · 10 W"),
 "heklet-heated-sherpa-throw": d("Velvet on one side, sherpa on the other, warmth on both.",
    ["9 heat settings, up to approx. 47 °C", "Timer with auto switch-off", "Machine washable (cable detached)", "Ships from our EU warehouse"],
    "180 × 130 cm · 160 W · remote included"),
 "mitag-duo-smart-tag": d("Find collars, keys and bags with Apple Find My or Google Find Hub.",
    ["Works with iPhone or Android (one at a time)", "Play a sound to find it nearby", "IP65 water-resistant", "Optional leather case with keyring"],
    "Bluetooth smart tag, not GPS: location updates via nearby phones in the network. Not for Huawei."),
 "heated-pet-pad": d("A warm spot of their own, gentle on paws and fur.",
    ["3 levels, approx. 35–44 °C", "Waterproof, stain-resistant fabric", "Anti-bite cable protection", "EU or US plug"],
    "45 × 45 or 50 × 70 cm · 20 W · cord approx. 147 cm"),
 "stainless-steel-pet-fountain": d("Fresh, filtered, flowing water in polished stainless steel.",
    ["304 stainless steel", "Carbon + sponge filtration", "Ultra-quiet, under 20 dB", "Dishwasher-safe tray and tank"],
    "2L or 4L · USB cable included, wall adapter not included · filter every 2–4 weeks"),
 "automatic-pet-feeder-4l": d("Up to six meals a day, on time, no Wi-Fi needed.",
    ["1–6 portioned meals per day", "Stainless steel bowl", "Triple-seal lid keeps kibble fresh", "Paw-proof locking lid"],
    "4L · dry kibble 2–15 mm · adapter included, 3 × D batteries optional (not included)"),
}
for h, html in COPY.items():
    p = gql("query($h:String!){productByHandle(handle:$h){id}}", {"h": h})["productByHandle"]
    check(gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){product{id} userErrors{field message}}}",
              {"p": {"id": p["id"], "descriptionHtml": html}})["productUpdate"], h)
    print("ok", h)
