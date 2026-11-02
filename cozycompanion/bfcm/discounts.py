"""BFCM 2026 tiered automatic discounts (owner approved offer A on 2026-11-02).
10% off $75+, 15% off $150+, 20% off $250+; live Mon Nov 23 00:00 ET - Mon Nov 30 23:59 ET.
Automatic discounts that don't combine: Shopify applies the one that saves the customer the most."""
import os, sys
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, S)
from lib import gql, check
START, END = "2026-11-23T05:00:00Z", "2026-12-01T04:59:59Z"
TIERS = [(0.10, 75), (0.15, 150), (0.20, 250)]
existing = {n["discount"].get("title") for n in gql("{discountNodes(first:100){nodes{discount{... on DiscountAutomaticBasic{title}}}}}")["discountNodes"]["nodes"]}
for pct, minimum in TIERS:
    title = f"Black Friday Week: {int(pct*100)}% off ${minimum}+"
    if title in existing: print("exists:", title); continue
    r = gql("""mutation($d:DiscountAutomaticBasicInput!){discountAutomaticBasicCreate(automaticBasicDiscount:$d){
               automaticDiscountNode{id automaticDiscount{... on DiscountAutomaticBasic{title status startsAt endsAt}}} userErrors{field message}}}""",
            {"d": {"title": title, "startsAt": START, "endsAt": END,
                   "minimumRequirement": {"subtotal": {"greaterThanOrEqualToSubtotal": str(minimum)}},
                   "customerGets": {"value": {"percentage": pct}, "items": {"all": True}},
                   "combinesWith": {"orderDiscounts": False, "productDiscounts": False, "shippingDiscounts": True}}})
    print(check(r["discountAutomaticBasicCreate"])["automaticDiscountNode"])
