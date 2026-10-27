#!/usr/bin/env python3
"""CozyCompanion Phase 1: collections + DRAFT products via the Admin API.

Usage:
  python3 cozycompanion/phase1.py --check   # step 1 only: token + shop check
  python3 cozycompanion/phase1.py           # check, then create/update (idempotent by handle)

Reads COZY_SHOPIFY_CLIENT_ID, COZY_SHOPIFY_CLIENT_SECRET, COZY_SHOPIFY_DOMAIN.
Never prints the token. Refuses to write unless the shop is CozyCompanion.
Products are always created as DRAFT; nothing is published or activated.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

EXPECTED_DOMAIN = "pj0q30-dd.myshopify.com"
API_VERSION = "2026-10"
CATALOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "catalog.json")


def die(msg):
    print(f"STOP: {msg}")
    sys.exit(1)


def env():
    names = ["COZY_SHOPIFY_CLIENT_ID", "COZY_SHOPIFY_CLIENT_SECRET", "COZY_SHOPIFY_DOMAIN"]
    missing = [n for n in names if not os.environ.get(n, "").strip()]
    if missing:
        die(f"missing env vars: {', '.join(missing)}")
    domain = os.environ["COZY_SHOPIFY_DOMAIN"].strip().removeprefix("https://").rstrip("/")
    if domain != EXPECTED_DOMAIN:
        die(f"COZY_SHOPIFY_DOMAIN is '{domain}', expected '{EXPECTED_DOMAIN}'")
    return domain, os.environ["COZY_SHOPIFY_CLIENT_ID"].strip(), os.environ["COZY_SHOPIFY_CLIENT_SECRET"].strip()


def get_token(domain, client_id, secret):
    body = urllib.parse.urlencode(
        {"grant_type": "client_credentials", "client_id": client_id, "client_secret": secret}
    ).encode()
    req = urllib.request.Request(
        f"https://{domain}/admin/oauth/access_token",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        die(f"token request failed: HTTP {e.code} (check client ID/secret and app installation)")
    if "access_token" not in data:
        die(f"no access_token in response (keys: {list(data)})")
    print(f"token ok (scopes: {data.get('scope', '?')})")
    return data["access_token"]


class Admin:
    def __init__(self, domain, token):
        self.url = f"https://{domain}/admin/api/{API_VERSION}/graphql.json"
        self.token = token

    def gql(self, query, variables=None):
        req = urllib.request.Request(
            self.url,
            data=json.dumps({"query": query, "variables": variables or {}}).encode(),
            headers={"Content-Type": "application/json", "X-Shopify-Access-Token": self.token},
        )
        try:
            with urllib.request.urlopen(req) as r:
                res = json.load(r)
        except urllib.error.HTTPError as e:
            die(f"GraphQL HTTP {e.code}: {e.read()[:300]!r}")
        if res.get("errors"):
            die(f"GraphQL errors: {json.dumps(res['errors'])[:500]}")
        return res["data"]


def user_errors(payload, what):
    errs = payload.get("userErrors") or []
    if errs:
        die(f"{what}: {errs}")


def check_shop(api):
    shop = api.gql("{ shop { name myshopifyDomain currencyCode } }")["shop"]
    print(f"shop: {shop['name']} | {shop['myshopifyDomain']} | currency {shop['currencyCode']}")
    if shop["myshopifyDomain"] != EXPECTED_DOMAIN:
        die("connected shop is not CozyCompanion, nothing written")
    if shop["currencyCode"] != "EUR":
        print(f"WARNING: store currency is {shop['currencyCode']}, prices in catalog are EUR")
    return shop


def ensure_collection(api, c):
    found = api.gql(
        "query($h:String!){ collectionByIdentifier(identifier:{handle:$h}){ id } }", {"h": c["handle"]}
    )["collectionByIdentifier"]
    if found:
        print(f"  = collection exists: {c['title']}")
        return found["id"]
    res = api.gql(
        """mutation($input: CollectionInput!){ collectionCreate(input:$input){
             collection{ id } userErrors{ field message } } }""",
        {"input": {"title": c["title"], "handle": c["handle"], "descriptionHtml": c["descriptionHtml"]}},
    )["collectionCreate"]
    user_errors(res, f"collectionCreate {c['title']}")
    print(f"  + collection created: {c['title']}")
    return res["collection"]["id"]


def ensure_product(api, p, vendor):
    found = api.gql(
        "query($h:String!){ productByIdentifier(identifier:{handle:$h}){ id status } }", {"h": p["handle"]}
    )["productByIdentifier"]
    if found:
        print(f"  = product exists ({found['status']}): {p['title']}")
        return found["id"]
    res = api.gql(
        """mutation($product: ProductCreateInput!){ productCreate(product:$product){
             product{ id variants(first:1){ nodes{ id } } } userErrors{ field message } } }""",
        {
            "product": {
                "title": p["title"],
                "handle": p["handle"],
                "descriptionHtml": p["descriptionHtml"],
                "vendor": vendor,
                "productType": p["productType"],
                "tags": p["tags"],
                "status": "DRAFT",
            }
        },
    )["productCreate"]
    user_errors(res, f"productCreate {p['title']}")
    pid = res["product"]["id"]
    vid = res["product"]["variants"]["nodes"][0]["id"]
    res = api.gql(
        """mutation($pid: ID!, $v: [ProductVariantsBulkInput!]!){
             productVariantsBulkUpdate(productId:$pid, variants:$v){ userErrors{ field message } } }""",
        {"pid": pid, "v": [{"id": vid, "price": p["price"], "taxable": True}]},
    )["productVariantsBulkUpdate"]
    user_errors(res, f"price {p['title']}")
    print(f"  + product created (DRAFT, EUR {p['price']}): {p['title']}")
    return pid


def summary(api):
    data = api.gql(
        """{ products(first:50, sortKey:TITLE){ nodes{ title status productType
               variants(first:1){ nodes{ price } } collections(first:10){ nodes{ title } } } }
             collections(first:50, sortKey:TITLE){ nodes{ title handle productsCount{ count } } } }"""
    )
    print("\nCollections:")
    for c in data["collections"]["nodes"]:
        print(f"  {c['title']:<22} {c['productsCount']['count']} products  (/{c['handle']})")
    print("\nProducts:")
    for p in data["products"]["nodes"]:
        price = p["variants"]["nodes"][0]["price"] if p["variants"]["nodes"] else "-"
        cols = ", ".join(c["title"] for c in p["collections"]["nodes"])
        print(f"  [{p['status']}] {p['title']:<42} EUR {price:>7}  | {cols}")


def main():
    domain, client_id, secret = env()
    api = Admin(domain, get_token(domain, client_id, secret))
    check_shop(api)
    if "--check" in sys.argv:
        print("check ok, nothing written (--check)")
        return

    catalog = json.load(open(CATALOG))
    print("\nCollections")
    col_ids = {c["handle"]: ensure_collection(api, c) for c in catalog["collections"]}

    print("\nProducts")
    members = {h: [] for h in col_ids}
    for p in catalog["products"]:
        pid = ensure_product(api, p, catalog["vendor"])
        for h in p["collections"]:
            members[h].append(pid)

    print("\nCollection membership")
    for h, pids in members.items():
        if not pids:
            print(f"  {h}: empty for now")
            continue
        res = api.gql(
            """mutation($id: ID!, $p: [ID!]!){ collectionAddProducts(id:$id, productIds:$p){
                 userErrors{ field message } } }""",
            {"id": col_ids[h], "p": pids},
        )["collectionAddProducts"]
        errs = [e for e in res["userErrors"] if "already" not in e["message"].lower()]
        if errs:
            die(f"collectionAddProducts {h}: {errs}")
        print(f"  {h}: {len(pids)} products")

    summary(api)


if __name__ == "__main__":
    main()
