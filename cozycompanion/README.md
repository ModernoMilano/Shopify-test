# CozyCompanion store tooling

Scripts used to build and maintain the CozyCompanion Shopify store (`pj0q30-dd.myshopify.com`) through the Admin GraphQL API.

Credentials come from the environment (`COZY_SHOPIFY_CLIENT_ID`, `COZY_SHOPIFY_CLIENT_SECRET`, `COZY_SHOPIFY_DOMAIN`).
Get a 24h token into `tok.json` (git-ignored) before running anything except `reprice.py`, which fetches its own:

```bash
curl -s -X POST "https://$COZY_SHOPIFY_DOMAIN/admin/oauth/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=$COZY_SHOPIFY_CLIENT_ID&client_secret=$COZY_SHOPIFY_CLIENT_SECRET" > cozycompanion/tok.json
```

| Script | What it does |
|---|---|
| `reprice.py [--dry-run]` | Pricing rule: every single-item order keeps €15 profit after €30 ad spend, VAT, payment fees and shipping (`ADS`, `MARGIN` at the top); rounded up to x4.95/x9.95; equal prices for look-alike variants; never lowers a price |
| `spocket_cleanup.py` | Titles, copy, options, prices and collections for the first six Spocket imports |
| `product_templates.py` | `product.blanket` / `product.pettech` page templates (story, how it works, FAQ) |
| `homepage.py`, `headfoot.py`, `theme_settings.py`, `product_tpl.py` | Horizon theme: homepage, header/footer, brand settings, default product page |
| `cc-cart-perks.liquid` | Cart drawer extras (bundle progress, delivery note, upsells, USPs) |
| `pages.py`, `menus.py`, `subcollections.py`, `discounts.py` | Pages & policies, navigation, smart collections, discounts |
| `upload.py`, `staged.py` | Upload images to Shopify Files (`files.json` maps names to file IDs) |

`theme-backup/` holds the original Horizon files the theme scripts start from. `products_snapshot.json` is the raw Spocket import before cleanup.
