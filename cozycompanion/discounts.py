import sys, os
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
d = gql("{ discountNodes(first:20){nodes{id discount{__typename ... on DiscountCodeBasic{title} ... on DiscountAutomaticBasic{title}}}} collections(first:20){nodes{id handle}} }")
titles = {n["discount"].get("title") for n in d["discountNodes"]["nodes"]}
col = {c["handle"]: c["id"] for c in d["collections"]["nodes"]}
START = "2026-10-27T00:00:00Z"
if "COZY15" not in titles:
    r = gql("""mutation($d:DiscountCodeBasicInput!){discountCodeBasicCreate(basicCodeDiscount:$d){codeDiscountNode{id} userErrors{field message}}}""",
        {"d": {"title": "COZY15", "code": "COZY15", "startsAt": START, "appliesOncePerCustomer": True,
               "context": {"all": "ALL"},
               "customerGets": {"value": {"percentage": 0.15}, "items": {"all": True}},
               "combinesWith": {"productDiscounts": False, "orderDiscounts": False, "shippingDiscounts": True}}})["discountCodeBasicCreate"]
    check(r, "COZY15"); print("created COZY15")
else:
    print("COZY15 exists")
T = "Bundle & Save: 10% off 2+ pieces"
if T not in titles:
    r = gql("""mutation($d:DiscountAutomaticBasicInput!){discountAutomaticBasicCreate(automaticBasicDiscount:$d){automaticDiscountNode{id} userErrors{field message}}}""",
        {"d": {"title": T, "startsAt": START,
               "minimumRequirement": {"quantity": {"greaterThanOrEqualToQuantity": "2"}},
               "customerGets": {"value": {"percentage": 0.10}, "items": {"collections": {"add": [col["bundle-deals"]]}}},
               "combinesWith": {"productDiscounts": False, "orderDiscounts": False, "shippingDiscounts": True}}})["discountAutomaticBasicCreate"]
    check(r, T); print("created", T)
