import json, os, ssl, sys, time, urllib.request, urllib.error
S = os.path.dirname(os.path.abspath(__file__))
DOMAIN = os.environ["COZY_SHOPIFY_DOMAIN"]
TOKEN = json.load(open(os.path.join(S, "tok.json")))["access_token"]
URL = f"https://{DOMAIN}/admin/api/2026-10/graphql.json"
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
THEME = "gid://shopify/OnlineStoreTheme/210861556042"

def refresh_token():
    """client_credentials tokens last 24h: fetch a fresh one into tok.json (secrets stay in the environment)."""
    global TOKEN
    import subprocess
    subprocess.run(["curl", "-sf", "--retry", "3", "-X", "POST", f"https://{DOMAIN}/admin/oauth/access_token",
                    "-H", "Content-Type: application/x-www-form-urlencoded", "-o", os.path.join(S, "tok.json"),
                    "--data-urlencode", "grant_type=client_credentials",
                    "--data-urlencode", f"client_id={os.environ['COZY_SHOPIFY_CLIENT_ID']}",
                    "--data-urlencode", f"client_secret={os.environ['COZY_SHOPIFY_CLIENT_SECRET']}"], check=True)
    TOKEN = json.load(open(os.path.join(S, "tok.json")))["access_token"]

def gql(query, variables=None, _retry=True):
    req = urllib.request.Request(URL, data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    try:
        out = json.load(urllib.request.urlopen(req, context=CTX))
    except urllib.error.HTTPError as e:
        if e.code == 401 and _retry:
            refresh_token(); return gql(query, variables, _retry=False)
        raise
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
