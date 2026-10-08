---
name: creative-engine
description: ModernoMilano creative engine. Use whenever the user asks for Instagram content, photos, videos, campaign images, a content plan or grid, product visuals, captions, or competitor analysis (Zegna, Loro Piana, Boggi Milano, Brunello Cucinelli) for modernomilano.com. Builds looks only from active Shopify products, generates images on Higgsfield with the real product photos as references and the one fixed ModernoMilano model as the only person, and rejects any image that shows clothing or accessories ModernoMilano does not sell.
---

# ModernoMilano creative engine

Antwoord de gebruiker in het Nederlands. Prompts voor het beeldmodel zijn Engels.

**Geen meerkeuzevragen** (eigenaar, 8 oktober 2026). Stel de eigenaar geen vragen met opties en een aanbevolen keuze. Kies zelf de optie die je zou aanbevelen, voer die uit en meld in één zin wat je koos en waarom. Dit verandert niets aan de toestemming per actie voor publiceren in Shopify, Instagram of advertenties (harde regel 6), en niets aan een budget dat de eigenaar heeft genoemd.

## Harde regels (nooit overslaan)

1. **Alleen eigen kleding.** Elk zichtbaar kledingstuk en elke schoen is een actief product uit `creative-engine/data/wardrobe.json`. Verzin nooit een product. Een look die je zelf samenstelt, controleer je met `validateLook()` (`src/creative/looks.ts`).
2. **Geen accessoires**, geen logo's, geen tekst. De lijst staat in `FORBIDDEN` (`src/creative/prompt.ts`) en zit in elke prompt. De enige uitzondering is het ingenaaide ModernoMilano-necklabel (`brand/beeldregels.md`, hoofdstuk 3).
3. **Referenties zijn altijd onze eigen productfoto's** (de URL's uit de garderobe). Gebruik nooit een beeld van een concurrent als input voor het beeldmodel: die zijn alleen voor analyse.
4. **Geen loafers in de look, dan geen voeten in beeld.** Loafers altijd zonder sokken.
5. **Elk beeld door de kwaliteitscontrole** (`QA_QUESTIONS` en `judge()` in `src/creative/qa.ts`) voordat je het als goed presenteert. Eén nee is afgekeurd.
6. **Publiceren of iets veranderen in Shopify, Instagram of advertenties** alleen na expliciete toestemming per actie.
7. **Eén vast model.** Elke persoon in elke foto en elke video is dezelfde man: het ModernoMilano-model. Zijn gegevens staan in `creative-engine/data/model.json` (bron van waarheid), de uitleg in `creative-engine/brand/model.md`. Nooit een andere man, nooit twee mannen in één beeld, geen tweede gezicht en geen wisselende casting. Op openbare plekken mogen alleen 2 of 3 verre voorbijgangers in beeld, klein en onscherp, met onleesbare gezichten; die tellen niet als tweede man. Vergelijk hem nooit met een bestaand persoon en noem geen namen. Zijn interne naam (`name` in model.json) komt nooit in een prompt of caption.

Lees bij twijfel `creative-engine/brand/norm.md` (de norm), `beeldregels.md`, `model.md`, `merk-dna.md` en `concurrenten.md`.

## Het vaste model op Higgsfield

Neem ids en Engelse tekstblokken altijd uit `creative-engine/data/model.json`, niet uit je geheugen.

**Foto met producten (de standaard)**

- `generate_image_batch` (of `generate_image`) met `model: "nano_banana_pro"`, `resolution: "4k"`, `aspect_ratio: "4:5"` (9:16 voor het startbeeld van een reel).
- `prompt`: de element-placeholder (`higgsfield.element_placeholder`, de vorm `<<<element_id>>>`) staat in de tekst als het onderwerp, bijvoorbeeld "`<<<…>>>` wearing the pieces in reference images #1-#3". Higgsfield voegt dan zelf zijn gezicht toe. Zet het element-id nooit in `medias`; de vorm `@naam` werkt niet.
- `medias`: exact de lijst `references` uit het plan, in die volgorde, als `{ value: media_id, role: "image_references" }`. Dat zijn alleen productfoto's (#1 tot en met #n): geen gezichtsfoto's, want het element brengt zijn gezicht. Maximaal 4 per beeld; alleen een look van 5 stukken krijgt er 5, één per stuk. Haal niets weg en voeg niets toe: de prompt telt met die nummers. Bij een necklabelbeeld komen de 2 labelreferenties erachter.
- Vaste blokken uit `prompt` in model.json: `keep_en`, `light_default_en` (of een eigen lichtbron met richting), `expression_en`, `framing_en` (niet bij ten voeten uit en niet in de studio), `realism_en`, en op openbare plekken `public_places_en`. Beschrijf zijn gezicht niet in eigen woorden en gebruik `identity_en` niet: dat vecht met het element. `identity_en` hoort alleen bij de terugval zonder element (hieronder).
- De nummering met element plus referenties is nog niet getest: maak vóór de eerste batch één testbeeld en controleer dat "reference image #n" het juiste stuk pakt. Doe dat ook bij een nieuwe opzet (ander beeldmodel, ander aantal referenties).

**Portret waar het gezicht centraal staat** (`rules.image_model_portrait` in model.json)

- Alleen voor losse, snelle sfeerportretten buiten het plan. De beelden in het plan (ook `bw-portrait` en `studio-portrait`) blijven `nano_banana_pro` met het element.
- `generate_image` met `model: "soul_2"`, `soul_id` uit `higgsfield.soul_id`, `quality: "2k"`, `aspect_ratio: "3:4"`. Daarna bijsnijden naar 4:5.
- Geen productfoto in `medias`: Soul gebruikt een beeld met `role: "image"` als basis en maakt dan die productfoto na, zonder hem (getest 8 oktober). De kleding staat dus alleen in de tekst en wordt bij benadering; gebruik het alleen voor eenvoudige outfits en keur de kleding streng.
- Prompt: `realism_en`, één lichtbron, `expression_en` en `framing_en`. Niet `keep_en` (dat verwijst naar referentiebeelden), geen placeholder (Soul 2.0 negeert het element) en geen "#n".

**Video (alleen Seedance 2.5, besluit van de eigenaar op 8 oktober 2026)**

Seedance 2.5 is duur, dus elke clip moet in één keer goed zijn. Werk daarom altijd zo:

1. **Startbeeld.** Alleen een 9:16-beeld dat beide controles heeft doorstaan zonder uitzondering of eigen oordeel. Gebruik 4K. Bij een clip zonder hoofd staat de bovenrand in het beeld zelf al op de hals. Gaat de kin er toch in, snijd dan het startbeeld bij (9:16 behouden) en upload het; snijd nooit achteraf in de video. Geen voorbijgangers die dichtbij genoeg zijn om te bewegen.
2. **Vooraf nalopen.** Laat de prompt en het startbeeld door een aparte agent controleren tegen deze regels, voordat er een credit wordt uitgegeven.
3. **Concept.** Roep `generate_video` aan met deze instellingen:
   - `model: "seedance_2_5"`, `mode: "omni_reference"`, `resolution: "1080p"`, `bitrate_mode: "high"`, `duration: 5` (4 voor een clip die in een montage wordt geknipt, zoals de reels van `output/2026-10-08-reels-focus`), `aspect_ratio: "9:16"`, `generate_audio: false`, `draft: true` (480p, rond 15 credits; bij 4 seconden 12);
   - in `medias` eerst `{ role: "start_image", value: <job_id of media_id van het startbeeld> }`;
   - is zijn gezicht in beeld, dan daarna de 4K-gezichtsfoto's uit `higgsfield.video_face_refs` (ref-1 en ref-4, de `upscale_job_id`) als `{ role: "image_references" }`.

   Seedance 2.5 negeert het element. Zet de placeholder dus niet in de prompt: de prompt noemt hem "the man in the start frame and in the reference images". Krijg je een `preset_recommendation`, herhaal de aanroep dan met `declined_preset_id`.
4. **Controle.** Controleer het concept beeld voor beeld (elke 0,25 seconde) met de twee controleurs. Kijk naar het gezicht, de kleding, handen en voeten, of er mensen in elkaar overlopen, en of er tekst in beeld komt.
5. **Afmaken.** Vraag met `get_cost` op wat afmaken kost, en maak alleen een goedgekeurd concept af met `draft_job_id`, in 1080p (een volledige clip in 1080p is rond 60 credits). Controleer het eindresultaat nog één keer.
6. **Eén video tegelijk.** Mislukken twee concepten van dezelfde video, stop dan en overleg met de eigenaar, in plaats van door te gaan met credits uitgeven.
7. **Beweging.** Kleine, echte bewegingen: wind in het haar en het breisel, ademhalen, een mouw rechttrekken, één blik opzij, of de camera die langzaam dichterbij komt. Laat hem niet langs dingen lopen terwijl hij ze aanraakt, geen hoofddraai van meer dan 45 graden, niets voor zijn gezicht, en geen nieuwe mensen. Bij een detail blijft zijn gezicht de hele clip uit beeld.
8. **Ander model in het plan.** Noemt een plan of een oud bestand een ander videomodel (Kling, Seedance 2.0), gebruik dan toch Seedance 2.5.

**Als het element niet werkt** (status niet `completed`, of een model zonder elementsupport): maak het plan opnieuw met `--face-refs` (de filmische serie ook, zie 4b). Dan staan ref-1, ref-4 en ref-2 (`higgsfield.face_ref_order`) als #1-#3 **vooraan** in `references`, met de 4K-versie (`upscale_job_id`) als `value`, en de productfoto's daarna. De prompt zegt dan "the man in reference images #1-#3" met `identity_en`, zonder placeholder. Ref-3 (van achteren) gaat niet mee. Meld het bij de oplevering.

## Echt, niet AI (sinds 8 oktober 2026)

De batch van 100 op 7 oktober oogde te AI. Daarom gelden deze regels voor elke prompt en elke batch.

**In de prompt**

- **Geen filmwoorden.** Geen Kodak, Portra, Fuji, Vision3, "film" (ook niet "film photograph" of "35mm film"), "grain" of "halation". Die gaven nepranden en een korrellaag; de code en het script weigeren ze. Noem alleen camera en lens: "full-frame digital camera, 85mm f/1.8" (of 135mm f/2). Voeg voorlopig ook achteraf geen korrel of LUT toe: lever de beelden zoals het beeldmodel ze maakt.
- **Eén lichtbron die je kunt aanwijzen**, met richting, en het licht op hem klopt met de achtergrond. Standaard is `light_default_en`. 's Avonds noem je de bron op zijn gezicht: "lit only by the warm window on his left". Zijn gewicht staat op één been, met een echte schaduw waar hij staat.
- **Mond dicht, blik langs de camera** (`expression_en`). Nooit "laughs" of "smiling", geen tandenlach, niet recht in de lens poseren.
- **Standaard waist-up of driekwart**, uit het midden, van opzij, over de schouder of van achteren, met iets zachts op de voorgrond (`framing_en`). Ten voeten uit hooguit 2 op de 10 beelden: de studioslide van de productcarrousel en wijde locatiebeelden waarin hij van achteren of opzij staat (het plan houdt dat bij). Nooit "walks towards the camera", nooit gecentreerd en symmetrisch.
- **Leven in de verte.** Op straat, aan de kanalen, op pleinen en op stations: 2 of 3 verre voorbijgangers, klein en onscherp (`public_places_en`), en iets van leven, zoals een geparkeerde fiets of een krijtbord van opzij. Winkelborden alleen ver weg en onleesbaar. Schrijf op openbare plekken niet "nobody else": dat geeft een steriele stad. In de shotlijst heet zo'n plek `publicPlace`.
- **Huid** volgens `realism_en`. Niet "visible pores", "asymmetric face" of "not a model": dat gaf opgeplakte puistjes en vecht met zijn vaste gezicht. Geen "luxury", "clean" of "perfect".
- Licht, uitsnede en uitdrukking vooraan in de prompt, de kledingregels erachter.
- Still life: "slightly rumpled, not pressed, one sleeve falling loose". Necklabel: "small, curving with the collar, partly shaded". Loafers: "a mirrored left and right pair".

**Plekken en licht per set** (een set is één batch of losse serie van hooguit 12 beelden, zoals in 4b; het contentplan volgt de hoofdstukken van de norm)

- Milaan in de meerderheid: straten, Navigli, daken, binnenruimtes. Eén plek is hooguit ongeveer 15% van een set, ook het Comomeer.
- Hooguit 1 zonsondergang of blauw uur per 10 beelden. Ook bewolkt of een grijze ochtend.
- Gedempt, zachte contrasten, de achtergrond iets donkerder dan hij. Standaard warm; in herfst en winter mag de nabewerking koeler (norm, hoofdstuk 4). Geen HDR, geen teal-en-oranje.

**Per batch**

- Maximaal 12 beelden per batch. Eerst de kwaliteitscontrole, dan pas de volgende batch. Maak liever 2 of 3 varianten van een shot en houd de beste: 30 sterke beelden zijn beter dan 100 matige.
- 4k voor elk beeld met een persoon (Soul 2.0-portretten: 2k, het maximum van dat model). 2k mag voor sfeerbeelden zonder mensen.
- Zijn gezicht is in het eindbestand minstens ongeveer 500 px breed. Kleiner is afgekeurd. Dat geldt alleen voor foto's waarin zijn gezicht herkenbaar in beeld is. In wijde beelden (landschap, sneeuwveld, kust) staat hij van achteren of opzij en is zijn gezicht niet te lezen; dan is de vraag n.v.t. (`faceVisible: false`, `sameModel: null`). Bij een reel vraag je alleen of het dezelfde man is, niet de 500 px.
- Elk beeld waarin zijn gezicht herkenbaar is, leg je naast ref-1 en ref-4 (`creative-engine/brand/assets/model/`). Is het niet duidelijk dezelfde man, dan is het afgekeurd.
- Stijlvoorbeelden uit de batch van 100 (`output/2026-10-07-100-gevarieerd/final100.tsv`): zo wel P28, P31, P26, P05 en P07; zo niet P24, P19, P12, P18, P33 en P04.
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
  - `--face-refs`: alleen als het element niet werkt (zie "Als het element niet werkt").
  - Er valt niets te casten: elke persoon in het plan is het vaste model.
  - Plannen van vóór 8 oktober 2026 niet oplappen (andere man, filmwoorden, oude referenties): maak ze opnieuw met `npm run creative:plan`.
- Lees `creative-engine/output/plan-<start>.md` en laat de gebruiker de looks zien (titels, prijs, link) voordat je gaat genereren, tenzij hij al heeft gezegd dat je direct mag beginnen.

### 4. Genereren op Higgsfield

- Beelden (`frames[].request`):
  1. Elke productfoto-URL importeren met `media_import_url`. Kijk eerst in `creative-engine/data/higgsfield-media.json`: daar staan al geïmporteerde foto's met hun `media_id`. Nieuwe ids voeg je daaraan toe. Gezichtsfoto's (alleen bij `--face-refs`) hebben hun id al in de request (`mediaId`, de 4K-versie): niet importeren.
  2. Neem de `prompt` uit het plan ongewijzigd over. Bij een beeld met een persoon staat de element-placeholder erin en staan er geen filmwoorden in; staat er toch een gezichtsbeschrijving of een tweede man in, maak het plan dan opnieuw. Volg verder "Het vaste model op Higgsfield": `nano_banana_pro`, `resolution: "4k"`, `aspect_ratio` uit de request, en `medias` als `{ value: media_id, role: "image_references" }` **in precies de volgorde van `references`** (de prompt verwijst naar "reference image #n").
  3. Beelden zonder persoon: `nano_banana_pro`, 2k mag, zonder placeholder.
  4. `generate_image_batch` met maximaal 12 beelden per keer. Daarna eerst stap 5, dan pas de volgende batch.
  5. Wachten met `jobs_wait`, tonen met `show_generation_by_ids`. Wordt die uitvoer te groot, zet de links (`results.rawUrl`) dan in een tabel zoals `creative-engine/output/2026-10-06-testbeelden.md`.
- Reels (`video`): pas nadat het 9:16-beeld van die post is goedgekeurd. Het plan geeft `seedance_2_5` met `omni_reference`, 1080p, 5 seconden, 9:16 en zonder geluid. Het goedgekeurde beeld is de `start_image`, en als zijn gezicht in beeld is staan de gezichtsfoto's in `video.faceRefs`. Neem `video.prompt` ongewijzigd over en volg de stappen onder "Video": eerst een concept, dan de controle, dan afmaken. Noemt een oud plan Kling of Seedance 2.0, gebruik dan toch Seedance 2.5. Eén reel is voorlopig één clip van 5 seconden. Muziek komt er pas bij het posten op, uit de Instagram-bibliotheek.
- Kosten: rond 2 credits per beeld in 2k (oktober 2026); 4k en video kosten meer. Vraag `get_cost` bij 4k, video en batches, en vraag toestemming boven de 50 credits, tenzij de gebruiker al een aantal heeft genoemd.
- Higgsfield meldt de jobs als `nano_banana_2`, ook als `nano_banana_pro` is gevraagd. Meld dat als de kwaliteit tegenvalt.
- Geen project aanmaken tenzij `get_preferences` dat zegt of de gebruiker erom vraagt.

### 4b. Filmische serie (de stijl die de eigenaar wil, 6 oktober 2026)

De eigenaar vond de eerste 20 beelden "te AI, geen creativiteit". Wat hij wel wil: de manier van fotograferen van de Zegna-campagne in Venetië en van zijn eigen moodboard, en ook beelden **zonder kleding die over Milaan of het moderne Milaan gaan**. Staat er een persoon in beeld, dan is dat altijd het vaste model (harde regel 7). Werkwijze:

- Een serie van 10: ongeveer 4 sfeerbeelden van Milaan zonder mensen of kleding (Torre Velasca, de koepel van de Galleria, espresso aan de bar, een trappenhuis) en 6 productbeelden: van achteren, een detail met een hand, een gestapelde still life, een kledingstuk in ochtendlicht, een avondscène, een buitenscène (Comomeer, met een houten boot zonder merkteken).
- Prompts als een brief voor een cameraman: camera en lens, één lichtbron met richting, een echt moment, de uitsnede. Geen filmsoorten (zie "Echt, niet AI"). Geen trefwoorden als "luxury", "clean" of "perfect". Wat niet mag: kort en positief ("bare hands and wrists"). Een lange lijst met verboden voorwerpen roept die voorwerpen juist op (in de eerste set kwam er zo een ring in beeld).
- Bouwen: `python3 -I scripts/creative/cinematic_prompts.py <shots.json> <built.json>` (voorbeeld van de vorm: `creative-engine/output/2026-10-06-zegna-stijl/shots.json`; de teksten daarin zijn van vóór 8 oktober, met filmwoorden en een andere man: niet overnemen, het script weigert ze). Het script voegt het element, de kledingregels en de referenties toe; shots zonder handles worden sfeerbeelden zonder kleding. Zet `"public": true` bij een openbare plek en geef een detail altijd een eigen `light`. Beschrijf zijn gezicht of haar niet en noem geen tweede persoon: het script stopt dan. `--face-refs` alleen als het element niet werkt.
- Bekende fouten:
  - De Torino-blazer wordt enkelrijs en geweven getekend. Schrijf "DOUBLE-BREASTED, knitted, not woven" uit en zet de Shopify-foto van de blazer aan een model als eerste productreferentie. Het gezicht komt van het element, niet van die foto.
  - Bij een zittende man komen de voeten met sokken in beeld. Laat het beeld dan op halve dij eindigen.
  - Trappenhuizen krijgen een onmogelijk perspectief. Laat ze van onder naar het daklicht fotograferen, met één verdwijnpunt.

### 5. Kwaliteitscontrole

- **Bekijken via de Higgsfield-sandbox**: in deze omgeving is de beeldhost geblokkeerd, maar `sandbox_exec` heeft internet. Download daar de resultaten en de productfoto's (cdn.shopify.com), maak er thumbnails van (640x800, JPEG) plus uitvergrote uitsneden van handen, polsen, voeten en kraag, en geef ze mee in `image_paths` (maximaal 4 per keer, samen 512 KB of minder). Zet variabelen met `;` en niet met `&&` als je curls op de achtergrond draait. Lukt dat ook niet, zeg dat eerlijk en presenteer een beeld nooit als goedgekeurd.
- **Dezelfde man?** Geef bij elk beeld waarin zijn gezicht herkenbaar is (`faceVisible`) het beeld, een uitsnede van het gezicht, ref-1 en ref-4 samen mee. Vergelijk wenkbrauwen, ogen, kaak, lippen, haar (kleur, lengte, naar achteren gekamd), leeftijd en postuur, en loop `must_not_en` uit model.json na. Meet ook de breedte van het gezicht in px (`faceWidthPx`): minstens ongeveer 500 px. Zonder meting of vergelijking keurt `judge()` het af.
- **Op 100%** bekijken: huid, breisel, achtergrond, raamreflecties, schaal, voeten, en alle vier de hoeken (filmranden).
- Laat bij een serie ook twee onafhankelijke controleurs kijken (workflow): één op de kleding- en accessoireregels, één op AI-fouten en echtheid (anatomie, perspectief, tekst, randen, licht dat niet klopt, een ander gezicht).
- Beantwoord per beeld `QA_QUESTIONS`, vul een `Observation` in en gebruik `judge()`.
- Reels: de gezichtsvraag op elk beeld, elke 0,25 seconde, niet alleen op het begin, het midden en het einde (de 500 px gelden niet). Verandert zijn gezicht, zijn haar of de kleding, lopen mensen op de achtergrond in elkaar over, of komt er tekst in beeld, dan is de reel afgekeurd. Bij een concept gaat er dan niets naar 1080p.
- Afgekeurd: opnieuw genereren (maximaal 3 keer per beeld) met de prompt plus één extra zin die het probleem benoemt, bijvoorbeeld "His wrists are bare: no watch, no bracelet." Een afgekeurd beeld retoucheer je niet en werk je niet bij: je maakt het opnieuw.

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
