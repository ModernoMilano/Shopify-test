---
name: creative-engine
description: ModernoMilano creative engine. Use whenever the user asks for Instagram content, photos, campaign images, a content plan or grid, product visuals, captions, or competitor analysis (Zegna, Loro Piana, Boggi Milano, Brunello Cucinelli) for modernomilano.com. Builds looks only from active Shopify products, generates images on Higgsfield with the real product photos as references, and rejects any image that shows clothing or accessories ModernoMilano does not sell.
---

# ModernoMilano creative engine

Antwoord de gebruiker in het Nederlands. Prompts voor het beeldmodel zijn Engels.

## Harde regels (nooit overslaan)

1. **Alleen eigen kleding.** Elk zichtbaar kledingstuk en elke schoen is een actief product uit `creative-engine/data/wardrobe.json`. Verzin nooit een product. Een look die je zelf samenstelt, controleer je met `validateLook()` (`src/creative/looks.ts`).
2. **Geen accessoires**, geen logo's, geen tekst, niemand op de achtergrond. De lijst staat in `FORBIDDEN` (`src/creative/prompt.ts`) en zit in elke prompt.
3. **Referenties zijn altijd onze eigen productfoto's** (de URL's uit de garderobe). Gebruik nooit een beeld van een concurrent als input voor het beeldmodel: die zijn alleen voor analyse.
4. **Geen loafers in de look, dan geen voeten in beeld.** Loafers altijd zonder sokken.
5. **Elk beeld door de kwaliteitscontrole** (`QA_QUESTIONS` en `judge()` in `src/creative/qa.ts`) voordat je het als goed presenteert. Eén nee is afgekeurd.
6. **Publiceren of iets veranderen in Shopify, Instagram of advertenties** alleen na expliciete toestemming per actie.

Lees bij twijfel `creative-engine/brand/norm.md` (de norm), `beeldregels.md`, `merk-dna.md` en `concurrenten.md`.

## Werkwijze

### 1. Garderobe verversen (als `generatedAt` in wardrobe.json ouder is dan 7 dagen, of na een nieuwe drop)

- Haal alle actieve producten op met de Shopify-connector: `graphql_query` met de query uit `src/creative/catalog-query.ts` (`first: 50`, doorpagineren met `after` tot `hasNextPage` false is). De resultaten zijn groot en worden als bestand opgeslagen; voeg de pagina's samen met `jq -s '[.[].data.products.nodes[]]' p*.json > all.json`.
- `npm run creative:wardrobe -- --from all.json`. Meldt het script producten die het niet kon indelen, voeg dan een regel toe aan `LINE_RULES` in `src/creative/wardrobe.ts` en een test.
- Bestsellers: `run-analytics-query` met `FROM sales SHOW net_items_sold GROUP BY product_title SINCE -60d UNTIL today ORDER BY net_items_sold DESC LIMIT 40` en zet de titels in `creative-engine/data/bestsellers.json`.

### 2. Concurrenten (maandelijks, of als de gebruiker screenshots stuurt)

- **Screenshots van het raster** (de Windsor-koppeling lukt de gebruiker niet; dit is de hoofdroute): laat elke tegel door twee onafhankelijke agents coderen (formaat via het icoon rechtsboven, soort beeld, kader, nabewerking, personen, accessoires, logo's, merkobjecten) en vergelijk hun uitkomsten. Zie `creative-engine/research/data/2026-10-raster.json` voor het formaat.
- **Webonderzoek** alleen via de zoekmachine (WebFetch en Instagram zijn geblokkeerd). Elke claim die in de norm komt, apart laten controleren; cijfers van analysesites spreken elkaar vaak tegen.
- Lukt de Windsor-connector `instagram_public` toch (`get_connectors`): velden via `get_fields`, data via `get_data`, omzetten met `fromWindsorRow()` en samenvatten met `summarize()` (`src/creative/competitors.ts`).
- Schrijf `creative-engine/research/<jaar>-<maand>-concurrenten.md` met telling en bronnen, en werk `brand/norm.md` en zo nodig `CHAPTER` in `src/creative/plan.ts` en `SHOTS` in `src/creative/shots.ts` bij.

### 3. Plan maken

- `npm run creative:plan -- --posts 9 --start JJJJ-MM-DD [--seed N] [--anchor <handle>]... [--casting "<<<element_id>>>"]`
  - Een hoofdstuk is 9 posts: 4 carrousels, 3 reels, 2 losse beelden, gelezen in rijen van 3 (`CHAPTER` in `plan.ts`). Postdagen: zondag, maandag, woensdag en vrijdag.
  - `--anchor`: producten die er zeker in moeten (nieuwe drop, voorraad, campagne). Herhaalbaar.
  - `--casting`: het vaste gezicht. Staat er een Higgsfield Element-id in `creative-engine/data/models.json`, gebruik dan `<<<element_id>>>`. Zonder casting kiest de seed een gezicht uit `FACES` (`casting.ts`); houd binnen een hoofdstuk dezelfde seed aan.
- Lees `creative-engine/output/plan-<start>.md` en laat de gebruiker de looks zien (titels, prijs, link) voordat je gaat genereren, tenzij hij al heeft gezegd dat je direct mag beginnen.

### 4. Genereren op Higgsfield

- Beelden (`frames[].request`):
  1. Elke referentie-URL importeren met `media_import_url`. Kijk eerst in `creative-engine/data/higgsfield-media.json`: daar staan al geïmporteerde foto's met hun `media_id`. Nieuwe ids voeg je daaraan toe.
  2. `generate_image_batch` (tot 12 per keer) met `model: "nano_banana_pro"`, `aspect_ratio` en `resolution` uit de request, de `prompt` ongewijzigd, en `medias` als `{ value: media_id, role: "image_references" }` **in dezelfde volgorde als `references`** (de prompt verwijst naar "reference image #n").
  3. Wachten met `jobs_wait`, tonen met `show_generation_by_ids`. Wordt die uitvoer te groot, zet de links (`results.rawUrl`) dan in een tabel zoals `creative-engine/output/2026-10-06-testbeelden.md`.
- Reels (`video`): pas nadat het eerste beeld van die post is goedgekeurd. `generate_video` met `model: "kling3_0"`, het goedgekeurde beeld als `start_image`, `duration`, `mode: "pro"`, `sound: "off"` en de `prompt` uit `video`. Muziek komt er pas bij het posten op, uit de Instagram-bibliotheek.
- Kosten: rond 2 credits per beeld (oktober 2026). Vraag `get_cost` bij video en grote batches, en vraag toestemming boven de 50 credits, tenzij de gebruiker al een aantal heeft genoemd.
- Higgsfield meldt de jobs als `nano_banana_2`, ook als `nano_banana_pro` is gevraagd. Meld dat als de kwaliteit tegenvalt.
- Geen project aanmaken tenzij `get_preferences` dat zegt of de gebruiker erom vraagt.

### 4b. Filmische serie (de stijl die de eigenaar wil, 6 oktober 2026)

De eigenaar vond de eerste 20 beelden "te AI, geen creativiteit". Wat hij wel wil: de manier van fotograferen van Zegna (Mikkelsen-campagne, Venetië) en zijn eigen moodboard, **niet een vast model**, en ook beelden **zonder kleding die over Milaan of het moderne Milaan gaan**. Werkwijze:

- Een serie van 10: ongeveer 4 sfeerbeelden van Milaan zonder mensen of kleding (Torre Velasca, de koepel van de Galleria, espresso aan de bar, een trappenhuis) en 6 productbeelden: van achteren, een detail met een hand, een gestapelde still life, een kledingstuk in ochtendlicht, een avondscène, een buitenscène (Comomeer, met een houten boot zonder merkteken).
- Prompts als een brief voor een cameraman: lens, filmsoort (Kodak Vision3 500T, Portra), één lichtbron met richting, een echt moment, de uitsnede. Geen trefwoorden als "luxury", "clean" of "perfect". Wat niet mag: kort en positief ("bare hands and wrists"). Een lange lijst met verboden voorwerpen roept die voorwerpen juist op (in de eerste set kwam er zo een ring in beeld).
- Bouwen: `python3 -I scripts/creative/cinematic_prompts.py <shots.json> <built.json>` (voorbeeld: `creative-engine/output/2026-10-06-zegna-stijl/shots.json`). Het script voegt de kledingregels en de referenties toe; shots zonder handles worden sfeerbeelden zonder kleding.
- Bekende fouten:
  - De Torino-blazer wordt enkelrijs en geweven getekend. Schrijf "DOUBLE-BREASTED, knitted, not woven" uit en geef de modelfoto als eerste referentie.
  - Bij een zittende man komen de voeten met sokken in beeld. Laat het beeld dan op halve dij eindigen.
  - Trappenhuizen krijgen een onmogelijk perspectief. Laat ze van onder naar het daklicht fotograferen, met één verdwijnpunt.

### 5. Kwaliteitscontrole

- **Bekijken via de Higgsfield-sandbox**: in deze omgeving is de beeldhost geblokkeerd, maar `sandbox_exec` heeft internet. Download daar de resultaten en de productfoto's (cdn.shopify.com), maak er thumbnails van (640x800, JPEG) plus uitvergrote uitsneden van handen, polsen, voeten en kraag, en geef ze mee in `image_paths` (maximaal 4 per keer, samen 512 KB of minder). Zet variabelen met `;` en niet met `&&` als je curls op de achtergrond draait. Lukt dat ook niet, zeg dat eerlijk en presenteer een beeld nooit als goedgekeurd.
- Laat bij een serie ook twee onafhankelijke controleurs kijken (workflow): één op de kleding- en accessoireregels, één op AI-fouten (anatomie, perspectief, tekst, randen).
- Beantwoord per beeld `QA_QUESTIONS`, vul een `Observation` in en gebruik `judge()`.
- Afgekeurd: opnieuw genereren (maximaal 3 keer per beeld) met de prompt plus één extra zin die het probleem benoemt, bijvoorbeeld "His wrists are bare: no watch, no bracelet." Niet retoucheren of bijwerken.

### 6. Opleveren

- **De foto's**: de eigenaar wil één download met alleen de foto's, geen documenten en geen losse downloads. Maak in de Higgsfield-sandbox van de goedgekeurde beelden JPEG's op volle grootte (quality 95), genummerd met een Nederlandse titel ("01 Van achteren in het atrium.jpg"). Zet ze in één zip en vraag een upload-URL aan met `media_upload` (een zip is een "general file"). Upload in dezelfde sandbox-opdracht met `curl -X PUT -H 'Content-Type: application/octet-stream' -H 'If-None-Match: *'`, bevestig met `media_confirm` (type `file`) en controleer dat de link HTTP 200 geeft. Geef die ene link. In Google Drive kan Claude geen fotobestanden zetten, alleen documenten.

- Per goedgekeurde post: datum, pijler, formaat, de producten (titel en link, voor product-tags) en de caption volgens `norm.md` hoofdstuk 7. Het plan heeft al een `caption` met de `wearing`-regel en de hashtags; schrijf de kop (3 tot 7 woorden met een punt) en één of twee zinnen. Engels, geen emoji, geen uitroeptekens, geen "shop now", alleen claims uit de productdata.
- Publiceren via Windsor (`instagram`, actie voor een beeldpost) alleen na toestemming per post.

## Bestanden

| Pad | Wat |
|---|---|
| `src/creative/wardrobe.ts` | Shopify-product naar garderobe-item (zone, kleur, seizoen, referentiefoto's) |
| `src/creative/looks.ts` | Looks samenstellen en controleren, huislooks |
| `src/creative/shots.ts` | De beeldtypes (studio, architectuur, zwarte kust, sneeuwveld, schets, hanger, flatlay...) met nabewerking en beweging voor reels |
| `src/creative/casting.ts` | Vaste gezichten per hoofdstuk |
| `src/creative/captions.ts` | Captionopzet: productregel, hashtags, toonregels |
| `src/creative/prompt.ts` | Prompt + referenties, verboden items, clean look |
| `src/creative/qa.ts` | Kwaliteitscontrole |
| `src/creative/competitors.ts` | Concurrentieposts omzetten en samenvatten |
| `src/creative/plan.ts` | Hoofdstukken van 9 posts volgens de norm, met reels en captionopzet |
| `creative-engine/data/` | Garderobe, bestsellers, vaste modellen |
| `creative-engine/output/` | Gegenereerde plannen |
| `creative-engine/research/` | Concurrentie-analyses met bronnen en ruwe data |

Tests: `npx vitest run src/creative`. Typecheck: `npm run lint`.
