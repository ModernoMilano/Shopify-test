"""Turn AD_COPY.md + the uploaded ad images into launch_spec.json: the exact Meta objects to create
(campaign 120246807406500609 already exists, paused). Setup mirrors the ModernoMilano CBO campaigns."""
import json, os, re
A = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://cozycompanion.us"
reg = json.load(open(os.path.join(A, "..", "files.json")))
md = open(os.path.join(A, "AD_COPY.md")).read()
HANDLES = {"nestle": "nestle-heated-pet-pad", "roam": "roam-back-seat-dog-bed", "glance": "glance-camera-feeder"}
TARGETING = {"age_min": 18, "age_max": 65,
             "geo_locations": {"countries": ["US"], "location_types": ["home", "recent"]},
             "targeting_automation": {"advantage_audience": 1},
             "publisher_platforms": ["facebook", "instagram"],
             "facebook_positions": ["feed", "story", "facebook_reels", "profile_feed"],
             "instagram_positions": ["stream", "story", "reels", "profile_feed"],
             "device_platforms": ["mobile", "desktop"]}
# Advantage+ creative: everything off except visual touch-ups
OFF = ["text_optimizations", "inline_comment", "enhance_cta", "add_text_overlay", "image_animation", "music",
       "image_templates", "image_uncrop", "product_extensions", "site_extensions", "description_automation",
       "text_translation", "reveal_details_over_time", "show_summary", "show_destination_blurbs"]
ON = ["image_touchups", "image_brightness_and_contrast"]
DOF = {"creative_features_spec": {**{k: {"enroll_status": "OPT_OUT"} for k in OFF}, **{k: {"enroll_status": "OPT_IN"} for k in ON}}}
ads = []
for m in re.finditer(r"### (\w+): angle: (.+?)\n\*\*Primary text\*\*\n(.*?)\n\*\*Headline\*\* (.+?)\n\*\*Description\*\* (.+?)\n", md, re.S):
    aid, angle, text, head, desc = m.groups()
    prod = aid.split("_")[0]
    ads.append({"name": f"{prod.upper()} | {aid} | {angle}", "product": prod,
                "image_url": reg[f"ad_final_{aid}"]["url"].split("?")[0],
                "message": text.strip(), "headline": head.strip(), "description": desc.strip(),
                "link": f"{DOMAIN}/products/{HANDLES[prod]}",
                "url_tags": f"utm_source=meta&utm_medium=paid&utm_campaign=cc_usa_launch&utm_content={aid}",
                "call_to_action_type": "SHOP_NOW"})
spec = {"account": "4581064878797741", "campaign_id": "120246807406500609",
        "adsets": {p: {"name": f"USA | {p.upper()} | Advantage+ | VALUE", "optimization_goal": "VALUE",
                       "billing_event": "IMPRESSIONS", "targeting": TARGETING,
                       "promoted_object": {"pixel_id": "<COZY_PIXEL_ID>", "custom_event_type": "PURCHASE"}} for p in HANDLES},
        "degrees_of_freedom_spec": DOF, "page_id": "<COZY_PAGE_ID>", "ads": ads}
json.dump(spec, open(os.path.join(A, "launch_spec.json"), "w"), indent=1, ensure_ascii=False)
print(len(ads), "ads", [a["name"] for a in ads][:3])
