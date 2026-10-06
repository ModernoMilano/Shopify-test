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

Lees bij twijfel `creative-engine/brand/beeldregels.md`, `merk-dna.md` en `concurrenten.md`.

## Werkwijze

### 1. Garderobe verversen (als `generatedAt` in wardrobe.json ouder is dan 7 dagen, of na een nieuwe drop)

- Haal alle actieve producten op met de Shopify-connector: `graphql_query` met de query uit `src/creative/catalog-query.ts` (`first: 50`, doorpagineren met `after` tot `hasNextPage` false is). De resultaten zijn groot en worden als bestand opgeslagen; voeg de pagina's samen met `jq -s '[.[].data.products.nodes[]]' p*.json > all.json`.
- `npm run creative:wardrobe -- --from all.json`. Meldt het script producten die het niet kon indelen, voeg dan een regel toe aan `LINE_RULES` in `src/creative/wardrobe.ts` en een test.
- Bestsellers: `run-analytics-query` met `FROM sales SHOW net_items_sold GROUP BY product_title SINCE -60d UNTIL today ORDER BY net_items_sold DESC LIMIT 40` en zet de titels in `creative-engine/data/bestsellers.json`.

### 2. Concurrenten (maandelijks, of als de gebruiker erom vraagt)

- Windsor.ai-connector `instagram_public`. Controleer met `get_connectors` of hij gekoppeld is; zo niet, geef de gebruiker de link uit `get_connector_connect_info` en ga verder met de basisanalyse in `concurrenten.md`.
- Velden opzoeken met `get_fields` (nooit raden), dan `get_data` voor de laatste 30 dagen van de vier accounts uit `COMPETITORS` in `src/creative/competitors.ts`.
- Rijen omzetten met `fromWindsorRow()`, samenvatten met `summarize()`. Ontbreekt een veldnaam in `fromWindsorRow`, vul hem aan.
- Schrijf `creative-engine/research/<jaar>-<maand>.md`: per account de cijfers, de top 5 posts met link, en drie concrete conclusies voor ons volgende raster (welke shots, welk formaat, welke dagen). Pas zo nodig `MIX` in `src/creative/plan.ts` aan.

### 3. Plan maken

- `npm run creative:plan -- --posts 9 --start JJJJ-MM-DD [--seed N] [--anchor <handle>]...`
  - `--anchor`: producten die er zeker in moeten (nieuwe drop, voorraad, campagne). Herhaalbaar.
  - Andere `--seed` geeft een ander plan met dezelfde regels.
- Lees `creative-engine/output/plan-<start>.md` en laat de gebruiker de looks zien (titels, prijs, link) voordat je gaat genereren, tenzij hij al heeft gezegd dat je direct mag beginnen.

### 4. Genereren op Higgsfield

- Per beeld in het plan (`frames[].request`):
  1. Elke referentie-URL importeren met `media_import_url` (onthoud de `media_id` per URL in deze sessie, importeer niet twee keer).
  2. `generate_image` (of `generate_image_batch` bij meerdere beelden) met `model: "nano_banana_pro"`, `aspect_ratio` en `resolution` uit de request, de `prompt` ongewijzigd, en `medias` als `{ value: media_id, role: "image_references" }` **in dezelfde volgorde als `references`** (de prompt verwijst naar "reference image #n").
  3. Wachten met `jobs_wait`, tonen met één `show_generation_by_ids`.
- Kosten: rond 2 credits per beeld (oktober 2026). Vraag `get_cost` bij grote batches en vraag toestemming boven de 50 credits.
- Geen project aanmaken tenzij `get_preferences` dat zegt of de gebruiker erom vraagt.
- Vaste modellen: staat er een Higgsfield Element-id in `creative-engine/data/models.json`, zet dan `<<<element_id>>>` in de casting (`--casting` of `buildPrompt(..., { casting })`).

### 5. Kwaliteitscontrole

- Download elk resultaat en bekijk het met de Read-tool. Lukt downloaden niet (netwerk geblokkeerd), zeg dat eerlijk en vraag de gebruiker de beelden zelf te controleren met de vragen uit `QA_QUESTIONS`. Presenteer een beeld dan nooit als goedgekeurd.
- Beantwoord per beeld `QA_QUESTIONS`, vul een `Observation` in en gebruik `judge()`.
- Afgekeurd: opnieuw genereren (maximaal 3 keer per beeld) met de prompt plus één extra zin die het probleem benoemt, bijvoorbeeld "His wrists are bare: no watch, no bracelet." Niet retoucheren of bijwerken.

### 6. Opleveren

- Per goedgekeurd beeld: datum, pijler, de producten (titel en link, voor product-tags) en een caption in de merktoon (`merk-dna.md`): rustig, kort, materiaal en gevoel, geen hype, hooguit één emoji.
- Publiceren via Windsor (`instagram`, actie voor een beeldpost) alleen na toestemming per post.

## Bestanden

| Pad | Wat |
|---|---|
| `src/creative/wardrobe.ts` | Shopify-product naar garderobe-item (zone, kleur, seizoen, referentiefoto's) |
| `src/creative/looks.ts` | Looks samenstellen en controleren, huislooks |
| `src/creative/shots.ts` | De beeldtypes (studio, architectuur, landschap, dorp, macro...) |
| `src/creative/prompt.ts` | Prompt + referenties, verboden items, clean look |
| `src/creative/qa.ts` | Kwaliteitscontrole |
| `src/creative/competitors.ts` | Concurrentieposts omzetten en samenvatten |
| `src/creative/plan.ts` | Contentplan met mix en data |
| `creative-engine/data/` | Garderobe, bestsellers, vaste modellen |
| `creative-engine/output/` | Gegenereerde plannen |
| `creative-engine/research/` | Maandelijkse concurrentie-analyses |

Tests: `npx vitest run src/creative`. Typecheck: `npm run lint`.
