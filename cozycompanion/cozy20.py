"""COZY20 launch-week code (owner, 2026-11-04: "doe dan cozy20 voor de aankomende dagen"): 20% off, once per customer,
until Wed Nov 11 23:59 ET, combines with nothing (like COZY15). Gift cards are never discounted by Shopify."""
from lib import gql, check
import datetime
ex = gql('{codeDiscountNodeByCode(code:"COZY20"){id}}')["codeDiscountNodeByCode"]
if ex: print("exists", ex["id"]); raise SystemExit
now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
r = gql("""mutation($d:DiscountCodeBasicInput!){discountCodeBasicCreate(basicCodeDiscount:$d){codeDiscountNode{id codeDiscount{... on DiscountCodeBasic{title status startsAt endsAt}}} userErrors{field message}}}""",
        {"d": {"title": "COZY20 launch week: 20% off your first order", "code": "COZY20", "startsAt": now, "endsAt": "2026-11-12T04:59:59Z",
               "customerSelection": {"all": True}, "appliesOncePerCustomer": True,
               "customerGets": {"value": {"percentage": 0.20}, "items": {"all": True}},
               "combinesWith": {"orderDiscounts": False, "productDiscounts": False, "shippingDiscounts": True}}})
print(check(r["discountCodeBasicCreate"])["codeDiscountNode"])
