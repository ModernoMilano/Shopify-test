# 10 sfeerbeelden voor social media, 7 oktober 2026

Feedback van de eigenaar op de 50 productfoto's: te veel productshots, meer sfeer en gevoel voor social media. Focus op de collecties Reverso / Bundle & Save, Cashmere Sets, Cashmere Tops en Milano Sets (alleen de lounge sets en de Imperial set). Prompts en refs: `shots10.py` (bouwt `built10.json`). Model: `nano_banana_pro` (Higgsfield meldt `nano_banana_2`), 4:5, 2k.

**Download (zip met 10 JPEG's, 14 MB):** https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/c671d657-c466-46b3-bcd2-6264b1d91c9f.zip

| # | Titel | Collectie | Producten | Pogingen | Bestand (Higgsfield) |
|---|---|---|---|---|---|
| 1 | Arcadenhof op het blauwe uur | Bundle & Save | Reverso Nero Set, Suede Loafers Nero | 1 | `hf_20261007_195056_dcf67723-17fb-4fa4-9c63-0753b091a5c1.png` |
| 2 | Achterbank bij nacht | Bundle & Save | Reverso Midnight Set | 1 | `hf_20261007_195055_6fe3da96-bc6c-410d-8fca-987888665834.png` |
| 3 | Penthouse met skyline | Bundle & Save | Cashmere Onyx Set | 1 | `hf_20261007_195057_61ac121b-f969-4727-8369-825d83885cf0.png` |
| 4 | Zondagochtend in het park | Milano Sets | Exclusive Milano Lounge Set Navy, Puro tee, Suede Loafer Notte | 2 | `hf_20261007_195353_1848b73a-d725-4d95-9d75-543124eb3c5b.png` |
| 5 | Espresso aan de bar | Milano Sets | Imperial Milano Zip Set Brown, Puro tee | 1 | `hf_20261007_195056_9ee7eca6-65ab-4fb9-ab5c-91aa403904d1.png` |
| 6 | Bij het haardvuur | Cashmere Sets | Knitted Two-Tone Cashmere Set Navy, Puro tee | 1 | `hf_20261007_195056_1dc7cacf-a6c2-4e1d-bc1f-f7de69602ead.png` |
| 7 | Mist op het Comomeer | Cashmere Sets | Morbido Relaxed Set Beige, Suede Loafer Sabbia | 1 | `hf_20261007_195056_300312ff-555f-47a3-944d-d7f0e14785b1.png` |
| 8 | Blauw uur aan de Navigli | Cashmere Tops | Bellagio Ivory, Sartoriale Pant Charcoal | 1 | `hf_20261007_195056_63315ac8-c688-4ec9-847d-33ef7cfc950a.png` |
| 9 | In de oude tram | Cashmere Tops | Camicia Oliva, Puro tee, Atelier Trouser Beige | 1 | `hf_20261007_195056_d7c73885-8e73-4b7f-b95d-b927f5c85202.png` |
| 10 | Op de fiets langs het kanaal | Bundle & Save | Milano Oliva Set, Suede Loafers Moro | 1 | `hf_20261007_195056_e273fe57-2c03-479b-bd35-d2d554eb4dcc.png` |

Nabewerking: bij 8 twee wazige figuurtjes op de achtergrond weggeretoucheerd, bij 5 een smalle filmrand weggesneden. Foto 4 is opnieuw gemaakt omdat de Notte-loafers eerst donkere zolen hadden. Het echte product heeft een witte zool.

Werkwijze om toestemmingsvragen te beperken: de 18 nieuwe productfoto's zijn in drie sandbox-blokken via één `media_upload` en één `media_confirm` naar Higgsfield gezet, in plaats van 18 losse `media_import_url`-aanroepen. Alle tien beelden zijn in één batch gegenereerd.
