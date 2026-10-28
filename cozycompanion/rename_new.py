"""Give fresh supplier imports a CozyCompanion name (one evocative word + what it is). Keeps them DRAFT."""
import sys, os, re
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, check
NAMES = {
  "16147904790858": "Frost Quilted Dog Jacket",
  "16147905216842": "Splash Quick-Dry Pet Bathrobe",
  "16147906003274": "Snug Sherpa Pet Blanket",
  "16147906560330": "Doze Dog Pajamas",
  "16147908362570": "Tidy Bone Silicone Bowl Mat",
  "16147910820170": "Riddle Treat Dispensing Ball",
  "16147910918474": "Maze Puzzle Feeder Bowl",
  "16147912098122": "Burrow Cozy Cat Bed",
  "16147912196426": "Fold Magnetic Cat Scratcher",
  "16147912229194": "Dart Speedy Tail Cat Ball",
  "16147913277770": "Chomp Rubber Treat Ball",
}
ONLY = sys.argv[1:]
for pid, title in NAMES.items():
    if ONLY and pid not in ONLY: continue
    handle = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    r = gql("""mutation($p:ProductUpdateInput!){productUpdate(product:$p){product{title handle} userErrors{field message}}}""",
            {"p": {"id": f"gid://shopify/Product/{pid}", "title": title, "handle": handle, "redirectNewHandle": True,
                   "vendor": "CozyCompanion", "status": "DRAFT"}})
    check(r, "productUpdate"); print(r["productUpdate"]["product"])
