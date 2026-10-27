import json, os, ssl, sys, time, urllib.request
S = os.path.dirname(os.path.abspath(__file__))
DOMAIN = os.environ["COZY_SHOPIFY_DOMAIN"]
TOKEN = json.load(open(os.path.join(S, "tok.json")))["access_token"]
URL = f"https://{DOMAIN}/admin/api/2026-10/graphql.json"
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
THEME = "gid://shopify/OnlineStoreTheme/210861556042"

def gql(query, variables=None):
    req = urllib.request.Request(URL, data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    out = json.load(urllib.request.urlopen(req, context=CTX))
    if out.get("errors"):
        sys.exit(f"GraphQL error: {out['errors']}")
    return out["data"]

def check(payload, name=""):
    errs = payload.get("userErrors")
    if errs:
        sys.exit(f"{name}: {errs}")
    return payload

def theme_file(name):
    d = gql("""query($id:ID!,$f:[String!]){ theme(id:$id){ files(filenames:$f){ nodes{ filename body{ ... on OnlineStoreThemeFileBodyText{content} } } } } }""",
            {"id": THEME, "f": [name]})
    return d["theme"]["files"]["nodes"][0]["body"]["content"]

def put_theme_files(files):
    r = gql("""mutation($id:ID!,$files:[OnlineStoreThemeFilesUpsertFileInput!]!){ themeFilesUpsert(themeId:$id, files:$files){
              upsertedThemeFiles{filename} userErrors{field message code filename} } }""",
            {"id": THEME, "files": [{"filename": k, "body": {"type": "TEXT", "value": v}} for k, v in files.items()]})
    return check(r["themeFilesUpsert"], "themeFilesUpsert")

def product_ids():
    return {p["title"]: p["id"] for p in gql("{ products(first:50){nodes{id title}} }")["products"]["nodes"]}
