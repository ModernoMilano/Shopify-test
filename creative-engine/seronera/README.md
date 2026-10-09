# Seronera creative engine

Makes Meta ads for seronera.shop where **one image works in both 9:16 and 1:1**, with nothing important in the dead zones.

## How it works

1. **Background** (Higgsfield `generate_image`, model `nano_banana_pro`, 9:16, 2k, real product photo as reference). The prompt puts the product in a fixed band and leaves the top empty for text. No text in the image. See `backgrounds.json`.
2. **Check** the backgrounds with `qa.py` (guides: green = key area, red = 1:1 crop).
3. **Render** (`render.js`, Playwright): logo, headline and subline on exact pixel coordinates, in the site fonts (Trirong Light / Quattrocento Sans) and brand colours (`brand.json`). Copy per ad lives in `ads.json`.
4. **Checks**: every text box inside the safe area, minimum gap above the product, fonts and logo loaded (`render.js`), WCAG contrast measured on the real background (`contrast.py`), 1:1 pixel-identical to the 9:16 crop (`verify.py`).

## Geometry (1080x1920)

| | 9:16 coordinates |
|---|---|
| 1:1 crop | x 0-1080, y 219-1299 |
| Key area (text, logo, product) | x 65-1015, y 284-1234 |
| Reels/Stories UI (kept clear) | top 0-270, bottom 1248-1920, sides 65 px, right-hand buttons x 960+ at y 800-1500 |

## Running

The container blocks seronera.shop and the Higgsfield CDN, so the scripts run in the Higgsfield sandbox (`sandbox_exec`):

```bash
bash setup.sh   # fonts, logo, backgrounds -> bgx/ (1080x1920)
bash build.sh   # render -> contrast -> 1:1 crops + previews -> verify (must say ALL PASS)
```

`render.js`, `contrast.py`, `post.py`, `verify.py` and `qa.py` are the exact versions that produced batch 1 (ALL PASS). `setup.sh` and `build.sh` bundle the same steps and have not yet been run as one whole from scratch.

## Upload to Meta

One ad with placement asset customization: Feed gets `_1x1.png`, Stories and Reels get `_9x16.png`. Turn off the Advantage+ creative enhancements (expand image, adjust aspect ratio, overlays). Meta adds the CTA button itself.

## Batch 1 (2026-10-06)

9 ads (3x Backstrap Belt Black €199, 3x Belt Cognac €149, 3x iPhone 17 Pro Max case €149), 24 Higgsfield credits (12 backgrounds at 2 credits, 3 of them redone).
Download: https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/99004c4a-4f67-4c96-8b2a-813dfb04ab02.zip

## Batch 2 (2026-10-06): one file per ad

From batch 2 on, every ad is **one 9:16 file** (1080x1920) that you upload as-is. Meta then crops the middle out of it for the feed:

| Format | Visible part of the 9:16 |
|---|---|
| Reels/Stories | everything, minus the UI: y 270-1248 is free |
| Feed 1:1 (Meta centre crop) | y 420-1500 |
| Feed 4:5 (Meta centre crop) | y 285-1635 |
| **Free in all three** | **x 65-1015, y 440-1230** |

Layout: logo + headline (Trirong 72 px) + rule + subline in y 456-678, product from y ~720 to at most 1230. A soft gradient behind the text (it ends where the product starts) when the background is too busy. Checks are the same as batch 1 (safe zone, gap to the product, WCAG contrast per line). For the batch 2 settings: `batch2/ads.json`, `batch2/backgrounds.json`. Differences from `render.js`: SAFE y 440-1230, block top 456, headline 72 px, `white-space: nowrap`, scrim from y 300 to `productTop`.

Product too big in the AI image? Generate at 1:1 with the product in the lower-middle and empty space at the top, then `outpaint_image` to 9:16 (2 credits). Outpainting first to a larger 1:1 (e.g. 3000x3000) zooms out further.

6 ads (3x iPad cover €250, 3x luggage tag €35). Cost about 42 credits (including discarded attempts).
Download: https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/3dd4ddb5-951f-4abf-a2cb-961b51140805.zip

## Whole collection: catalogue, logo and creative bank (2026-10-09)

- **`catalog.json`**: the 7 product lines from seronera.shop (master products and collections): price, colours, sizes, models, description, a reference photo per colour, and the claims the site makes (CITES certified, free shipping over €100, shipped from EU with duties & taxes included, farm since 1997 on the Sabie River, gives back to South African communities). Watch the iPhone price: the main page says €150 for hornback, the older per-colour pages say €149.
- **`assets/logo_black.png`, `assets/logo_white.png`**: the logo as transparent PNG, 920x172 (twice as sharp as the site version).
- **`creative-bank/<line>.json`**: per line, 5 angles (hook, primary text short and long, headline, description, CTA), 6 on-image headline/subline pairs and 4 ready scene prompts (method `1:1+outpaint` or `9:16`, theme dark/light).
  - Written by one agent per line, then fact-checked against the catalogue and checked on format by two separate reviewers.
  - Character limits recounted independently: primary short ≤220, long ≤500, headline ≤40, description ≤30, on-image headline ≤22 with a full stop, subline ≤32 with the price.
  - 38 phrasings that two lines shared have been made unique, so no on-image headline appears twice.
- **`creative-bank/_cross-check.json`**: those replacements plus a launch plan: first the men's belt, iPhone case and luggage tag, one ad set per line, 4 creatives each, broad targeting, evaluate after 7 days.

### Making a new ad from the bank
1. Pick a `scene` from `creative-bank/<line>.json` and the matching `on_image[pairs_with_on_image]`.
2. Import the reference photo for that colour (`catalog.json` → `heroImages`) with `media_import_url` (append `?format=png`).
3. Generate with `nano_banana_pro` (2k, `image_references`), then for `1:1+outpaint` run `outpaint_image` 9:16 2048x3641. Check with guides that the product starts below y ~720 of 1920.
4. Render the text with the batch 2/3 renderer (SAFE x 65-1015, y 440-1230) and let the contrast check decide whether a scrim is needed.
5. Take the primary text, headline and description from the angle that fits the on-image headline.

Notes from practice:
- AI video looks fake fast and garbles the SERONERA engraving on the buckle. For Reels, use real footage and put only text and an end card on it.
- Ask for the product small in frame, otherwise the AI makes it too big.
- Subline casing doesn't matter: the renderer always sets the subline in capitals.

## Batch 3 (2026-10-09)
5 ads: women's belt red and pink (€100), men's belt green (€149), hornback cognac (€199), key ring cognac (€25). One 9:16 file per ad, all checks pass, 20 credits. Settings in `batch3/`.
Download: https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/715c6075-413f-4b79-a279-27f9f972d04d.zip
