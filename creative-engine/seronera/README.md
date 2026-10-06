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
