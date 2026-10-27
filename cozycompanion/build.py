import json, os, ssl, sys, urllib.request

S = os.path.dirname(os.path.abspath(__file__))
DOMAIN = os.environ["COZY_SHOPIFY_DOMAIN"]
TOKEN = json.load(open(os.path.join(S, "tok.json")))["access_token"]
URL = f"https://{DOMAIN}/admin/api/2026-10/graphql.json"
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")


def gql(query, variables=None):
    req = urllib.request.Request(URL, data=json.dumps({"query": query, "variables": variables or {}}).encode(),
                                 headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN})
    out = json.load(urllib.request.urlopen(req, context=CTX))
    if out.get("errors"):
        sys.exit(f"GraphQL error: {out['errors']}")
    return out["data"]


def check(payload, name):
    errs = payload.get("userErrors")
    if errs:
        sys.exit(f"{name}: {errs}")
    return payload


assert gql("{ shop { myshopifyDomain } }")["shop"]["myshopifyDomain"] == "pj0q30-dd.myshopify.com"

COLLECTIONS = {
    "Smart Pet Tech": {
        "handle": "smart-pet-tech",
        "html": "<p>Thoughtfully engineered technology for the companions who share your home. Feed, hydrate and keep watch over them with quiet, elegant devices designed to bring you peace of mind &mdash; wherever the day takes you.</p>",
        "seo": "Smart pet feeders, cameras, GPS trackers and water fountains, chosen for design, reliability and peace of mind.",
    },
    "Cozy Heated Blankets": {
        "handle": "cozy-heated-blankets",
        "html": "<p>Soft, enveloping warmth for long evenings in. Our heated blankets pair plush, touch-soft fabrics with gentle, adjustable heat &mdash; for you, for the ones you share the sofa with, and for your four-legged companions.</p>",
        "seo": "Luxuriously soft heated and weighted blankets with adjustable warmth, for people and pets.",
    },
    "Bundle Deals": {
        "handle": "bundle-deals",
        "html": "<p>Curated pairings that belong together &mdash; considered sets for a warmer, more connected home, offered at a gentler price.</p>",
        "seo": "Curated CozyCompanion sets of pet tech and heated blankets at special bundle pricing.",
    },
    "Holiday Gift Guide": {
        "handle": "holiday-gift-guide",
        "html": "<p>Gifts that say <em>I thought of you</em>. Our edit of the season's most giftable pieces &mdash; warmth for the people you love and quiet comfort for the pets who complete the picture.</p>",
        "seo": "The CozyCompanion holiday gift guide: luxury pet tech and heated blankets for everyone you love.",
    },
}

GIFT = ["Holiday Gift Guide"]
PRODUCTS = [
    {
        "title": "Smart Pet Feeder Camera 1080P HD", "price": "184.99", "type": "Smart Pet Feeder",
        "cols": ["Smart Pet Tech"] + GIFT, "tags": ["pet-tech", "feeder", "camera", "gift"],
        "seo": "See, hear and feed your pet from anywhere with a 1080P HD camera feeder — scheduled meals and peace of mind in one elegant device.",
        "html": """<p><strong>Mealtime, beautifully handled &mdash; even when you're away.</strong></p>
<p>The Smart Pet Feeder Camera brings you home in an instant. Look in through crisp 1080P HD video, check that dinner has been served, and enjoy a quiet moment together from wherever your day takes you.</p>
<ul>
<li><strong>1080P HD view</strong> &ndash; a clear window into your home, right from your phone.</li>
<li><strong>Scheduled, portioned meals</strong> &ndash; a calm, consistent routine your companion can count on.</li>
<li><strong>Peace of mind on long days</strong> &ndash; no more rushing home to fill the bowl.</li>
<li><strong>Refined design</strong> &ndash; understated lines that sit gracefully in any interior.</li>
</ul>
<p>Thoughtful care, quietly automated.</p>""",
    },
    {
        "title": "Automatic Pet Feeder Smart Sensor", "price": "184.53", "type": "Smart Pet Feeder",
        "cols": ["Smart Pet Tech"], "tags": ["pet-tech", "feeder", "sensor"],
        "seo": "A smart-sensor automatic pet feeder for perfectly timed, portion-controlled meals — calm routines and effortless care.",
        "html": """<p><strong>Effortless nourishment, precisely timed.</strong></p>
<p>Designed for households that value calm routines, the Automatic Pet Feeder with Smart Sensor serves measured meals on schedule &mdash; so your companion is cared for, every single time.</p>
<ul>
<li><strong>Smart sensor technology</strong> &ndash; responsive, reliable dispensing you can trust.</li>
<li><strong>Portion control</strong> &ndash; supports a healthy weight with consistent servings.</li>
<li><strong>A steady rhythm</strong> &ndash; regular mealtimes help pets feel settled and secure.</li>
<li><strong>Minimal footprint</strong> &ndash; a clean, modern silhouette for elegant spaces.</li>
</ul>
<p>Less to remember. More time to simply enjoy each other.</p>""",
    },
    {
        "title": "Smart Mini GPS Pet Tracker", "price": "59.99", "type": "Pet GPS Tracker",
        "cols": ["Smart Pet Tech"] + GIFT, "tags": ["pet-tech", "gps", "tracker", "gift"],
        "seo": "A lightweight smart mini GPS tracker that clips to any collar — know where your pet is and enjoy every adventure with confidence.",
        "html": """<p><strong>Freedom for them. Reassurance for you.</strong></p>
<p>Small enough to forget it's there, smart enough to matter when it counts. The Smart Mini GPS Pet Tracker attaches discreetly to your companion's collar, keeping their whereabouts close at hand on your phone.</p>
<ul>
<li><strong>Real-time location</strong> &ndash; find your companion quickly, wherever they wander.</li>
<li><strong>Featherlight and discreet</strong> &ndash; comfortable for daily wear, for cats and dogs alike.</li>
<li><strong>Confident adventures</strong> &ndash; open fields, new trails and city walks, all with peace of mind.</li>
<li><strong>A considered gift</strong> &ndash; for every pet parent who worries a little.</li>
</ul>
<p>Because the ones we love should always find their way home.</p>""",
    },
    {
        "title": "Premium Pet Water Fountain 68oz", "price": "44.99", "type": "Pet Water Fountain",
        "cols": ["Smart Pet Tech"], "tags": ["pet-tech", "fountain", "hydration"],
        "seo": "A 68oz (approx. 2L) premium pet water fountain with continuously flowing, filtered water that invites pets to drink more.",
        "html": """<p><strong>Fresh, flowing water &mdash; an everyday luxury.</strong></p>
<p>Pets are naturally drawn to moving water. The Premium Pet Water Fountain keeps a generous 68oz (approx. 2L) circulating and filtered, gently encouraging your companion to drink more throughout the day.</p>
<ul>
<li><strong>Continuously circulating water</strong> &ndash; fresher and more inviting than a still bowl.</li>
<li><strong>Filtered for purity</strong> &ndash; helps keep hair and debris out of every sip.</li>
<li><strong>Generous 68oz capacity</strong> &ndash; fewer refills, even in multi-pet homes.</li>
<li><strong>Quiet and refined</strong> &ndash; a calm presence in the kitchen or living room.</li>
</ul>
<p>Good hydration, elegantly encouraged.</p>""",
    },
    {
        "title": "Laura Hill Electric Heated Blanket Double", "price": "46.88", "type": "Heated Blanket",
        "cols": ["Cozy Heated Blankets"] + GIFT, "tags": ["heated-blanket", "double", "gift"],
        "seo": "The Laura Hill double electric heated blanket: plush, even warmth with adjustable settings for cosy nights for two.",
        "html": """<p><strong>Warmth made for two.</strong></p>
<p>Slip into an evening of soft, even warmth. The Laura Hill Electric Heated Blanket is generously sized for a double bed or a shared sofa, wrapping you in gentle heat on the coldest nights of the year.</p>
<ul>
<li><strong>Double size</strong> &ndash; ample coverage for couples, or for curling up alone in style.</li>
<li><strong>Adjustable warmth</strong> &ndash; choose the comfort level that feels just right.</li>
<li><strong>Plush, soft-touch finish</strong> &ndash; as indulgent to hold as it is to sleep under.</li>
<li><strong>Warm the person, not the house</strong> &ndash; a cosy, considered way to stay comfortable through winter.</li>
</ul>
<p>Long evenings in have never felt so inviting.</p>""",
    },
    {
        "title": "USB Powered Heated Blanket 3 Settings", "price": "36.99", "type": "Heated Blanket",
        "cols": ["Cozy Heated Blankets"] + GIFT, "tags": ["heated-blanket", "usb", "portable", "gift"],
        "seo": "A USB-powered heated blanket with 3 warmth settings — portable, plush comfort for the desk, sofa, car or travel.",
        "html": """<p><strong>Your personal warmth, wherever you settle.</strong></p>
<p>Powered by USB, this soft heated blanket goes where you go &mdash; the home office, the reading chair, the car or a chilly evening on the terrace. Simply connect to a power bank or USB adapter and unwind.</p>
<ul>
<li><strong>3 heat settings</strong> &ndash; from a gentle glow to deep, comforting warmth.</li>
<li><strong>USB powered</strong> &ndash; works with power banks, laptops and wall adapters.</li>
<li><strong>Lightweight and portable</strong> &ndash; folds easily for travel and everyday use.</li>
<li><strong>A thoughtful gift</strong> &ndash; for anyone who always feels the cold.</li>
</ul>
<p>Small comforts, beautifully portable.</p>""",
    },
    {
        "title": "Weighted Heated Blanket 9kg", "price": "109.99", "type": "Weighted Blanket",
        "cols": ["Cozy Heated Blankets"] + GIFT, "tags": ["heated-blanket", "weighted", "relaxation", "gift"],
        "seo": "A 9kg weighted heated blanket that combines calming, even pressure with soothing warmth for deeper relaxation.",
        "html": """<p><strong>The feeling of being held &mdash; with warmth to match.</strong></p>
<p>Our Weighted Heated Blanket brings together two of life's quiet comforts: the calming, evenly distributed pressure of a 9kg weighted blanket and the soothing embrace of gentle heat. It's an invitation to slow down, breathe and truly unwind.</p>
<ul>
<li><strong>9kg evenly distributed weight</strong> &ndash; a grounding, cocooning sensation.</li>
<li><strong>Soothing adjustable heat</strong> &ndash; melts away the chill of a long day.</li>
<li><strong>Designed for deep relaxation</strong> &ndash; your new evening ritual on the sofa or in bed.</li>
<li><strong>Luxurious soft-touch cover</strong> &ndash; indulgent against the skin.</li>
</ul>
<p>Rest, reimagined.</p>""",
    },
    {
        "title": "Pet-Specific Heated Blanket Washable", "price": "45.99", "type": "Pet Heated Blanket",
        "cols": ["Cozy Heated Blankets", "Smart Pet Tech"] + GIFT, "tags": ["heated-blanket", "pet", "washable", "gift"],
        "seo": "A washable heated blanket designed for pets — gentle, cosy warmth for cats and dogs, especially seniors and short-coated breeds.",
        "html": """<p><strong>Because they deserve to be cosy, too.</strong></p>
<p>Made especially for our four-legged companions, this heated blanket offers gentle, comforting warmth for naps, long nights and chilly mornings &mdash; a quiet luxury that senior pets, small breeds and short-coated companions particularly appreciate.</p>
<ul>
<li><strong>Designed for pets</strong> &ndash; soothing warmth tailored to curl-up comfort.</li>
<li><strong>Washable</strong> &ndash; easy to keep fresh, clean and inviting.</li>
<li><strong>Soft, plush surface</strong> &ndash; a favourite spot they'll return to again and again.</li>
<li><strong>Fits their space</strong> &ndash; on the bed, in the crate or by your side on the sofa.</li>
</ul>
<p>Warm hearts, warm paws.</p>""",
    },
]

# --- Collections (manual, unpublished until launch) ---
existing = {c["title"]: c["id"] for c in gql("{ collections(first:50){nodes{id title}} }")["collections"]["nodes"]}
col_ids = {}
for title, c in COLLECTIONS.items():
    if title in existing:
        col_ids[title] = existing[title]
        print(f"collection exists: {title}")
        continue
    r = check(gql("""mutation($input: CollectionInput!){ collectionCreate(input:$input){ collection{id handle} userErrors{field message} } }""",
                  {"input": {"title": title, "handle": c["handle"], "descriptionHtml": c["html"],
                             "seo": {"title": f"{title} | CozyCompanion", "description": c["seo"]}}})["collectionCreate"], title)
    col_ids[title] = r["collection"]["id"]
    print(f"collection created: {title}")

# --- Products (DRAFT) ---
existing_p = {p["title"]: p["id"] for p in gql("{ products(first:100){nodes{id title}} }")["products"]["nodes"]}
for p in PRODUCTS:
    if p["title"] in existing_p:
        print(f"product exists: {p['title']}")
        continue
    r = check(gql("""mutation($product: ProductCreateInput!){ productCreate(product:$product){
                product{ id variants(first:1){nodes{id}} } userErrors{field message} } }""",
                  {"product": {"title": p["title"], "descriptionHtml": p["html"], "vendor": "CozyCompanion",
                               "productType": p["type"], "tags": p["tags"], "status": "DRAFT",
                               "collectionsToJoin": [col_ids[c] for c in p["cols"]],
                               "seo": {"title": f"{p['title']} | CozyCompanion", "description": p["seo"]}}})["productCreate"], p["title"])
    pid = r["product"]["id"]
    vid = r["product"]["variants"]["nodes"][0]["id"]
    check(gql("""mutation($pid: ID!, $v: [ProductVariantsBulkInput!]!){ productVariantsBulkUpdate(productId:$pid, variants:$v){
                userErrors{field message} } }""",
              {"pid": pid, "v": [{"id": vid, "price": p["price"], "taxable": True,
                                  "inventoryItem": {"tracked": False, "requiresShipping": True}}]})["productVariantsBulkUpdate"], p["title"])
    print(f"product created (DRAFT): {p['title']} €{p['price']}")
