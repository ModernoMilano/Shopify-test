"""Frees 2 of Shopify's 25 automatic-discount slots for the BFCM tiers (owner approved 2026-11-02) by merging two pairs of
related 'Complete the set' discounts into one discount each. Same 20% and the same minimum quantity; every product keeps the
set shown on its page, and customers can now also mix pieces across the two merged sets (only ever more generous).
  The Winter Walk (3) + The Rainy Day Set (3)  -> one discount, min 3 of: frost, mistle, puddle, drizzle, splash
  The Lounge Set (2) + The Den Set (2)         -> one discount, min 2 of: lounge, cloud, haven, nook"""
import os, sys
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, S)
from lib import gql, check
P = "gid://shopify/DiscountAutomaticNode/"
MERGES = [(P + "2099217498442", P + "2099217531210", "The Winter Walk & Rainy Day Sets: 20% off"),
          (P + "2099217629514", P + "2099217662282", "The Lounge & Den Sets: 20% off")]

def products(node):
    r = gql("""query($id:ID!){automaticDiscountNode(id:$id){automaticDiscount{... on DiscountAutomaticBasic{title
               customerGets{items{... on DiscountProducts{products(first:20){nodes{id handle}}}}}}}}}""", {"id": node})
    d = r["automaticDiscountNode"]
    return None if d is None else [p["id"] for p in d["automaticDiscount"]["customerGets"]["items"]["products"]["nodes"]]

for keep, drop, title in MERGES:
    extra = products(drop)
    if extra is None:
        print("already merged:", title); continue
    have = products(keep); add = [p for p in extra if p not in have]
    r = gql("""mutation($id:ID!,$d:DiscountAutomaticBasicInput!){discountAutomaticBasicUpdate(id:$id,automaticBasicDiscount:$d){
               automaticDiscountNode{automaticDiscount{... on DiscountAutomaticBasic{title}}} userErrors{field message}}}""",
            {"id": keep, "d": {"title": title, "customerGets": {"items": {"products": {"productsToAdd": add}}}}})
    print(check(r["discountAutomaticBasicUpdate"]))
    print(check(gql("mutation($id:ID!){discountAutomaticDelete(id:$id){deletedAutomaticDiscountId userErrors{field message}}}",
                    {"id": drop})["discountAutomaticDelete"]))
