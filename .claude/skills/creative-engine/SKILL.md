---
name: creative-engine
description: ModernoMilano creative engine. Use whenever the user asks for Instagram content, photos, videos, campaign images, a content plan or grid, product visuals, captions, or competitor analysis (Zegna, Loro Piana, Boggi Milano, Brunello Cucinelli) for modernomilano.com. Builds looks only from active Shopify products, generates images on Higgsfield with the real product photos as references and the one fixed ModernoMilano model as the only person, and rejects any image that shows clothing or accessories ModernoMilano does not sell.
---

# ModernoMilano creative engine

Antwoord de gebruiker in het Nederlands. Prompts voor het beeldmodel zijn Engels.

## Harde regels (nooit overslaan)

1. **Alleen eigen kleding.** Elk zichtbaar kledingstuk en elke schoen is een actief product uit `creative-engine/data/wardrobe.json`. Verzin nooit een product. Een look die je zelf samenstelt, controleer je met `validateLook()` (`src/creative/looks.ts`).
2. **Geen accessoires**, geen logo's, geen tekst. De lijst staat in `FORBIDDEN` (`src/creative/prompt.ts`) en zit in elke prompt. De enige uitzondering is het ingenaaide ModernoMilano-necklabel (`brand/beeldregels.md`, hoofdstuk 3).
3. **Referenties zijn altijd onze eigen productfoto's** (de URL's uit de garderobe). Gebruik nooit een beeld van een concurrent als input voor het beeldmodel: die zijn alleen voor analyse.
4. **Geen loafers in de look, dan geen voeten in beeld.** Loafers altijd zonder sokken.
5. **Elk beeld door de kwaliteitscontrole** (`QA_QUESTIONS` en `judge()` in `src/creative/qa.ts`) voordat je het als goed presenteert. Eén nee is afgekeurd.
6. **Publiceren of iets veranderen in Shopify, Instagram of advertenties** alleen na expliciete toestemming per actie.
7. **Eén vast model.** Elke persoon in elke foto en elke video is dezelfde man: het ModernoMilano-model. Zijn gegevens staan in `creative-engine/data/model.json` (bron van waarheid), de uitleg in `creative-engine/brand/model.md`. Nooit een andere man, nooit twee mannen in één beeld, geen tweede gezicht en geen wisselende casting. Op openbare plekken mogen alleen 2 of 3 verre voorbijgangers in beeld, klein en onscherp, met onleesbare gezichten. Vergelijk hem nooit met een bestaand persoon en noem geen namen. Zijn interne naam (`name` in model.json) komt nooit in een prompt of caption.

Lees bij twijfel `creative-engine/brand/norm.md` (de norm), `beeldregels.md`, `model.md`, `merk-dna.md` en `concurrenten.md`.

## Het vaste model op Higgsfield

Neem ids en Engelse tekstblokken altijd uit `creative-engine/data/model.json`, niet uit je geheugen.

**Foto met producten (de standaard)**

- `generate_image_batch` (of `generate_image`) met `model: "nano_banana_pro"`, `resolution: "4k"`, `aspect_ratio: "4:5"` (9:16 voor het startbeeld van een reel).
- `prompt`: de element-placeholder (`higgsfield.element_placeholder`, de vorm `<<<element_id>>>`) staat in de tekst als het onderwerp, bijvoorbeeld "`<<<…>>>` wearing the pieces in reference images #1-#3". Higgsfield voegt dan zelf zijn gezicht toe. Zet het element-id nooit in `medias`; de vorm `@naam` werkt niet.
- `medias`: de echte productfoto's als `{ value: media_id, role: "image_references" }`, maximaal 4 per beeld, in de volgorde van `references`. Bij een necklabelbeeld komen de 2 labelreferenties erbij.
- Vaste blokken uit `prompt` in model.json: `keep_en`, `light_default_en` (of een eigen lichtbron met richting), `expression_en`, `framing_en`, `realism_en`, en op openbare plekken `public_places_en`. Beschrijf zijn gezicht niet opnieuw in eigen woorden: dat vecht met het element. `identity_en` gebruik je alleen als het gezicht niet via het element of de Soul ID komt.
- Nieuwe opzet (ander model, ander aantal referenties)? Maak eerst één testbeeld en controleer dat "reference image #n" het juiste product pakt.

**Portret waar het gezicht centraal staat**

- `generate_image` met `model: "soul_2"`, `soul_id` uit `higgsfield.soul_id`, `quality: "2k"`, `aspect_ratio: "3:4"`. Daarna bijsnijden naar 4:5.
- Maximaal 1 productfoto: `medias: [{ role: "image", value: media_id }]`. Dus alleen voor eenvoudige outfits.
- Soul 2.0 negeert het element. Zet de placeholder er niet in.

**Video**

- Nooit video vanuit alleen tekst. Altijd image-to-video vanaf een goedgekeurde foto van hem.
- `generate_video` met `model: "seedance_2_0"`, `mode: "std"`, `resolution: "1080p"`, `duration: 5`, `aspect_ratio: "9:16"`, `generate_audio: false`, `medias: [{ role: "start_image", value: <job_id van de goedgekeurde foto> }]`, en de element-placeholder in de `prompt`, zodat zijn gezicht vast blijft.
- Kleine, natuurlijke beweging: lopen, een mouw rechttrekken, over het water kijken. Geen volledige hoofddraai en niets voor zijn gezicht.
- Terugval: `kling3_0` (`mode: "pro"`, `sound: "off"`, 5 seconden). Kling gebruikt het element alleen samen met een `start_image`.

**Als het element niet werkt** (status niet `completed`, of een model zonder elementsupport): zet 2 of 3 gezichtsfoto's (`higgsfield.face_refs`, eerst ref-1, ref-4 en ref-2) **als eerste** in `medias` en schrijf "the man in reference images #1-#3; use them only for his face and hair, ignore their clothing, light and setting". De productfoto's komen daarna. Meld het bij de oplevering.

## Echt, niet AI (sinds 8 oktober 2026)

De batch van 100 op 7 oktober oogde te AI. Daarom gelden deze regels voor elke prompt en elke batch.

**In de prompt**

- **Geen filmwoorden.** Geen Kodak, Portra, Vision3, "photographed on film", "film grain" of "still from a film". Die gaven nepranden en een korrellaag. Noem alleen camera en lens: "full-frame digital camera, 85mm f/1.8" (of 135mm f/2). Korrel en kleur komen er in de nabewerking bij.
- **Eén lichtbron die je kunt aanwijzen**, met richting, en het licht op hem klopt met de achtergrond. Standaard is `light_default_en`. 's Avonds noem je de bron op zijn gezicht: "lit only by the warm window on his left". Zijn gewicht staat op één been, met een echte schaduw waar hij staat.
- **Mond dicht, blik langs de camera** (`expression_en`). Nooit "laughs" of "smiling", geen tandenlach, niet recht in de lens poseren.
- **Standaard waist-up of driekwart**, uit het midden, van opzij, over de schouder of van achteren, met iets zachts op de voorgrond (`framing_en`). Ten voeten uit hooguit 2 op de 10 beelden. Nooit "walks towards the camera", nooit gecentreerd en symmetrisch.
- **Leven in de verte.** Op straat, aan de kanalen en op stations: 2 of 3 verre voorbijgangers, klein en onscherp (`public_places_en`). Winkelborden alleen ver weg en onleesbaar. Schrijf niet "nobody else": dat geeft een steriele stad.
- **Huid** volgens `realism_en`. Niet "visible pores", "asymmetric face" of "not a model": dat gaf opgeplakte puistjes en vecht met zijn vaste gezicht. Geen "luxury", "clean" of "perfect".
- Licht, uitsnede en uitdrukking vooraan in de prompt, de kledingregels erachter.
- Still life: "slightly rumpled, not pressed, one sleeve falling loose". Necklabel: "small, curving with the collar, partly shaded". Loafers: "a mirrored left and right pair".

**Plekken en licht per set**

- Milaan in de meerderheid: straten, Navigli, daken, binnenruimtes. Eén plek is hooguit ongeveer 15% van een set, ook het Comomeer.
- Hooguit 1 zonsondergang of blauw uur per 10 beelden. Ook bewolkt of een grijze ochtend.
- Gedempt, zachte contrasten, de achtergrond iets donkerder dan hij. Standaard warm; in herfst en winter mag de nabewerking koeler (norm, hoofdstuk 4). Geen HDR, geen teal-en-oranje.

**Per batch**

- Maximaal 12 beelden per batch. Eerst de kwaliteitscontrole, dan pas de volgende batch. Maak liever 2 of 3 varianten van een shot en houd de beste: 30 sterke beelden zijn beter dan 100 matige.
- 4k voor elk beeld met een persoon. 2k mag voor sfeerbeelden zonder mensen.
- Zijn gezicht is in het eindbestand minstens ongeveer 500 px breed. Kleiner is afgekeurd.
- Elk beeld met een gezicht leg je naast ref-1 en ref-4 (`creative-engine/brand/assets/model/`). Is het niet duidelijk dezelfde man, dan is het afgekeurd.
- Gebruik `output/2026-10-07-100-gevarieerd/shots100.py` niet als sjabloon. De tien wisselende mannen (`MEN`) en de filmwoorden in `REAL` en `LOOK` zijn precies wat misging.

## Werkwijze

### 1. Garderobe verversen (als `generatedAt` in wardrobe.json ouder is dan 7 dagen, of na een nieuwe drop)

- Haal alle actieve producten op met de Shopify-connector: `graphql_query` met de query uit `src/creative/catalog-query.ts` (`first: 50`, doorpagineren met `after` tot `hasNextPage` false is). De resultaten zijn groot en worden als bestand opgeslagen; voeg de pagina's samen met `jq -s '[.[].data.products.nodes[]]' p*.json > all.json`.
- `npm run creative:wardrobe -- --from all.json`. Meldt het script producten die het niet kon indelen, voeg dan een regel toe aan `LINE_RULES` in `src/creative/wardrobe.ts` en een test.
- Bestsellers: `run-analytics-query` met `FROM sales SHOW net_items_sold GROUP BY product_title SINCE -60d UNTIL today ORDER BY net_items_sold DESC LIMIT 40` en zet de titels in `creative-engine/data/bestsellers.json`.

### 2. Concurrenten (maandelijks, of als de gebruiker screenshots stuurt)

- **Screenshots van het raster** (de Windsor-koppeling lukt de gebruiker niet; dit is de hoofdroute): laat elke tegel door twee onafhankelijke agents coderen (formaat via het icoon rechtsboven, soort beeld, kader, nabewerking, personen, accessoires, logo's, merkobjecten) en vergelijk hun uitkomsten. Zie `creative-engine/research/data/2026-10-raster.json` voor het formaat.
- **Webonderzoek** alleen via de zoekmachine (WebFetch en Instagram zijn geblokkeerd). Elke claim die in de norm komt, apart laten controleren; cijfers van analysesites spreken elkaar vaak tegen.
- Lukt de Windsor-connector `instagram_public` toch (`get_connectors`): velden via `get_fields`, data via `get_data`, omzetten met `fromWindsorRow()` en samenvatten met `summarize()` (`src/creative/competitors.ts`).
- Schrijf `creative-engine/research/<jaar>-<maand>-concurrenten.md` met telling en bronnen, en werk `brand/norm.md` en zo nodig `CHAPTER` in `src/creative/plan.ts` en `SHOTS` in `src/creative/shots.ts` bij. Casting van concurrenten neem je niet over: wij hebben één vast model.

### 3. Plan maken

- `npm run creative:plan -- --posts 9 --start JJJJ-MM-DD [--seed N] [--anchor <handle>]...`
  - Een hoofdstuk is 9 posts: 4 carrousels, 3 reels, 2 losse beelden, gelezen in rijen van 3 (`CHAPTER` in `plan.ts`). Postdagen: zondag, maandag, woensdag en vrijdag.
  - `--anchor`: producten die er zeker in moeten (nieuwe drop, voorraad, campagne). Herhaalbaar.
  - Er valt niets te casten: elke persoon in het plan is het vaste model. Staat er in een oud plan nog een tweede man of het beeldtype "two-generations", maak dat beeld dan met alleen hem, of sla het over.
- Lees `creative-engine/output/plan-<start>.md` en laat de gebruiker de looks zien (titels, prijs, link) voordat je gaat genereren, tenzij hij al heeft gezegd dat je direct mag beginnen.

### 4. Genereren op Higgsfield

- Beelden (`frames[].request`):
  1. Elke referentie-URL importeren met `media_import_url`. Kijk eerst in `creative-engine/data/higgsfield-media.json`: daar staan al geïmporteerde foto's met hun `media_id`. Nieuwe ids voeg je daaraan toe.
  2. Neem de `prompt` uit het plan over. Bij een beeld met een persoon controleer je dat de element-placeholder erin staat (anders zet je hem bij het onderwerp) en dat er geen filmwoorden in staan. Volg verder "Het vaste model op Higgsfield": `nano_banana_pro`, `resolution: "4k"`, `aspect_ratio` uit de request, en `medias` als `{ value: media_id, role: "image_references" }` **in dezelfde volgorde als `references`** (de prompt verwijst naar "reference image #n"), maximaal 4 productfoto's.
  3. Beelden zonder persoon: `nano_banana_pro`, 2k mag, zonder placeholder.
  4. `generate_image_batch` met maximaal 12 beelden per keer. Daarna eerst stap 5, dan pas de volgende batch.
  5. Wachten met `jobs_wait`, tonen met `show_generation_by_ids`. Wordt die uitvoer te groot, zet de links (`results.rawUrl`) dan in een tabel zoals `creative-engine/output/2026-10-06-testbeelden.md`.
- Reels (`video`): pas nadat het 9:16-beeld van die post is goedgekeurd. Volg "Video" hierboven: `seedance_2_0`, 5 seconden, 1080p, het goedgekeurde beeld als `start_image` en de placeholder in de prompt. Neem de beweging uit `video.prompt` over; noemt het plan nog `kling3_0` of een andere lengte, gebruik dan toch Seedance 2.0 en 5 seconden. Muziek komt er pas bij het posten op, uit de Instagram-bibliotheek.
- Kosten: rond 2 credits per beeld in 2k (oktober 2026); 4k en video kosten meer. Vraag `get_cost` bij 4k, video en batches, en vraag toestemming boven de 50 credits, tenzij de gebruiker al een aantal heeft genoemd.
- Higgsfield meldt de jobs als `nano_banana_2`, ook als `nano_banana_pro` is gevraagd. Meld dat als de kwaliteit tegenvalt.
- Geen project aanmaken tenzij `get_preferences` dat zegt of de gebruiker erom vraagt.

### 4b. Filmische serie (de stijl die de eigenaar wil, 6 oktober 2026)

De eigenaar vond de eerste 20 beelden "te AI, geen creativiteit". Wat hij wel wil: de manier van fotograferen van de Zegna-campagne in Venetië en van zijn eigen moodboard, en ook beelden **zonder kleding die over Milaan of het moderne Milaan gaan**. Staat er een persoon in beeld, dan is dat altijd het vaste model (harde regel 7). Werkwijze:

- Een serie van 10: ongeveer 4 sfeerbeelden van Milaan zonder mensen of kleding (Torre Velasca, de koepel van de Galleria, espresso aan de bar, een trappenhuis) en 6 productbeelden: van achteren, een detail met een hand, een gestapelde still life, een kledingstuk in ochtendlicht, een avondscène, een buitenscène (Comomeer, met een houten boot zonder merkteken).
- Prompts als een brief voor een cameraman: camera en lens, één lichtbron met richting, een echt moment, de uitsnede. Geen filmsoorten (zie "Echt, niet AI"). Geen trefwoorden als "luxury", "clean" of "perfect". Wat niet mag: kort en positief ("bare hands and wrists"). Een lange lijst met verboden voorwerpen roept die voorwerpen juist op (in de eerste set kwam er zo een ring in beeld).
- Bouwen: `python3 -I scripts/creative/cinematic_prompts.py <shots.json> <built.json>` (voorbeeld: `creative-engine/output/2026-10-06-zegna-stijl/shots.json`). Het script voegt de kledingregels en de referenties toe; shots zonder handles worden sfeerbeelden zonder kleding. Controleer in de uitvoer dat elk shot met een persoon het vaste model gebruikt en geen filmwoorden bevat.
- Bekende fouten:
  - De Torino-blazer wordt enkelrijs en geweven getekend. Schrijf "DOUBLE-BREASTED, knitted, not woven" uit en zet de Shopify-foto van de blazer aan een model als eerste productreferentie. Het gezicht komt van het element, niet van die foto.
  - Bij een zittende man komen de voeten met sokken in beeld. Laat het beeld dan op halve dij eindigen.
  - Trappenhuizen krijgen een onmogelijk perspectief. Laat ze van onder naar het daklicht fotograferen, met één verdwijnpunt.

### 5. Kwaliteitscontrole

- **Bekijken via de Higgsfield-sandbox**: in deze omgeving is de beeldhost geblokkeerd, maar `sandbox_exec` heeft internet. Download daar de resultaten en de productfoto's (cdn.shopify.com), maak er thumbnails van (640x800, JPEG) plus uitvergrote uitsneden van handen, polsen, voeten en kraag, en geef ze mee in `image_paths` (maximaal 4 per keer, samen 512 KB of minder). Zet variabelen met `;` en niet met `&&` als je curls op de achtergrond draait. Lukt dat ook niet, zeg dat eerlijk en presenteer een beeld nooit als goedgekeurd.
- **Dezelfde man?** Geef bij elk beeld met een gezicht het beeld, een uitsnede van het gezicht, ref-1 en ref-4 samen mee. Vergelijk wenkbrauwen, ogen, kaak, lippen, haar (kleur, lengte, naar achteren gekamd), leeftijd en postuur, en loop `must_not_en` uit model.json na. Meet ook de breedte van het gezicht: minstens ongeveer 500 px.
- **Op 100%** bekijken: huid, breisel, achtergrond, raamreflecties, schaal, voeten, en alle vier de hoeken (filmranden).
- Laat bij een serie ook twee onafhankelijke controleurs kijken (workflow): één op de kleding- en accessoireregels, één op AI-fouten en echtheid (anatomie, perspectief, tekst, randen, licht dat niet klopt, een ander gezicht).
- Beantwoord per beeld `QA_QUESTIONS`, vul een `Observation` in en gebruik `judge()`.
- Reels: dezelfde gezichtsvraag op het begin, het midden en het einde. Verandert zijn gezicht, dan is de reel afgekeurd.
- Afgekeurd: opnieuw genereren (maximaal 3 keer per beeld) met de prompt plus één extra zin die het probleem benoemt, bijvoorbeeld "His wrists are bare: no watch, no bracelet." Niet retoucheren of bijwerken.

### 6. Opleveren

- **De foto's**: de eigenaar wil één download met alleen de foto's, geen documenten en geen losse downloads. Maak in de Higgsfield-sandbox van de goedgekeurde beelden JPEG's op volle grootte (quality 95), genummerd met een Nederlandse titel ("01 Van achteren in het atrium.jpg"). Zet ze in één zip en vraag een upload-URL aan met `media_upload` (een zip is een "general file"). Upload in dezelfde sandbox-opdracht met `curl -X PUT -H 'Content-Type: application/octet-stream' -H 'If-None-Match: *'`, bevestig met `media_confirm` (type `file`) en controleer dat de link HTTP 200 geeft. Geef die ene link. In Google Drive kan Claude geen fotobestanden zetten, alleen documenten.

- Per goedgekeurde post: datum, pijler, formaat, de producten (titel en link, voor product-tags) en de caption volgens `norm.md` hoofdstuk 7. Het plan heeft al een `caption` met de `wearing`-regel en de hashtags; schrijf de kop (3 tot 7 woorden met een punt) en één of twee zinnen. Engels, geen emoji, geen uitroeptekens, geen "shop now", alleen claims uit de productdata.
- Publiceren via Windsor (`instagram`, actie voor een beeldpost) alleen na toestemming per post.

## Bestanden

| Pad | Wat |
|---|---|
| `creative-engine/data/model.json` | **Het vaste model**: element, Soul ID, gezichtsfoto's met media-ids, Engelse promptblokken en regels. Bron van waarheid |
| `creative-engine/brand/model.md` | Uitleg bij het model: wie hij is, waaraan je hem herkent, hoe hij in beeld komt |
| `creative-engine/brand/assets/model/` | De referentiefoto's ref-1 t/m ref-4 |
| `src/creative/wardrobe.ts` | Shopify-product naar garderobe-item (zone, kleur, seizoen, referentiefoto's) |
| `src/creative/looks.ts` | Looks samenstellen en controleren, huislooks |
| `src/creative/shots.ts` | De beeldtypes (studio, architectuur, zwarte kust, sneeuwveld, schets, hanger, flatlay...) met nabewerking en beweging voor reels |
| `src/creative/casting.ts` | Het vaste model in de engine, uit `data/model.json` |
| `src/creative/captions.ts` | Captionopzet: productregel, hashtags, toonregels |
| `src/creative/prompt.ts` | Prompt + referenties, verboden items, clean look |
| `src/creative/qa.ts` | Kwaliteitscontrole |
| `src/creative/competitors.ts` | Concurrentieposts omzetten en samenvatten |
| `src/creative/plan.ts` | Hoofdstukken van 9 posts volgens de norm, met reels en captionopzet |
| `creative-engine/data/` | Garderobe, bestsellers, Higgsfield-media-ids, het model |
| `creative-engine/output/` | Gegenereerde plannen |
| `creative-engine/research/` | Concurrentie-analyses met bronnen en ruwe data |

Tests: `npx vitest run src/creative`. Typecheck: `npm run lint`.
