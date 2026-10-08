# ModernoMilano creative engine

Maakt Instagram-content in de stijl van Zegna, Loro Piana, Brunello Cucinelli en Boggi Milano, met **uitsluitend kleding uit de eigen winkel**.

```text
Shopify (232 actieve producten) ──► garderobe ──► looks ──► plan (norm) ──► prompt + productfoto's ──► Higgsfield ──► kwaliteitscontrole ──► jij
                                       ▲            ▲            ▲                                          │
Bestsellers (ShopifyQL) ───────────────┘            │            │                                          └──► reel (Seedance, vanaf het goedgekeurde beeld)
Merk-DNA, paletten, vast model ─────────────────────┘            │
Concurrenten (screenshots + gecontroleerd webonderzoek) ─────────┘
```

## Gebruiken

Vraag het aan Claude in deze repo, bijvoorbeeld:

- "Maak een raster van 9 posts voor volgende week."
- "Maak 4 beelden van de nieuwe Torino blazer."
- "Hier zijn nieuwe screenshots van de concurrenten, werk de norm bij."

Claude volgt dan de skill in `.claude/skills/creative-engine/SKILL.md`.

Zelf draaien kan ook:

```bash
npm run creative:wardrobe -- --from export.json   # garderobe opnieuw opbouwen
npm run creative:plan -- --posts 9 --start 2026-10-11 --seed 2 --anchor milano-cashmere-torino-blazer-perla
npx vitest run src/creative                       # de regels testen
```

Voorbeeldplan (18 posts, 2 hoofdstukken): `output/plan-2026-10-11.md`. De 20 testbeelden van 6 oktober staan in `output/2026-10-06-testbeelden.md`.

## Bestanden

| Pad | Wat |
|---|---|
| `brand/norm.md` | **De norm**: ritme, hoofdstukken van 9, formaten, beeldtypes, het vaste model, captions, KPI's |
| `brand/beeldregels.md` | Wat nooit in beeld mag, clean look en echt beeld, het vaste model, kwaliteitscontrole |
| `brand/model.md` | **Het vaste model**: wie hij is, waaraan je hem herkent, hoe hij in beeld komt |
| `brand/assets/model/` | De referentiefoto's van het model (ref-1 t/m ref-4) |
| `brand/merk-dna.md` | Wat we verkopen, bestsellers, paletten, toon |
| `brand/concurrenten.md` | Per merk: overnemen en niet overnemen |
| `research/2026-10-concurrenten.md` | Het onderzoek met telling en bronnen; ruwe data in `research/data/` |
| `data/wardrobe.json` | De garderobe (alle actieve producten) |
| `data/bestsellers.json` | Bestsellers van de laatste 60 dagen |
| `data/higgsfield-media.json` | Higgsfield-ids van al geïmporteerde productfoto's (hergebruik) |
| `data/model.json` | Het model voor de engine: element, Soul ID, gezichtsfoto's en de Engelse promptblokken. Bron van waarheid |

## Hoe de regel "alleen eigen kleding" wordt bewaakt

1. **Garderobe**: alleen actieve producten, ingedeeld naar zone (top, tussenlaag, buitenlaag, broek, schoen). Sets worden opgesplitst in hun stukken.
2. **Looks**: precies één top en één broek, hooguit één tussenlaag, één buitenlaag en één paar loafers. Eén palet, hooguit drie kleurfamilies en tonaal gekozen loafers. Zonder loafers geen voeten in beeld.
3. **Prompt**: elk zichtbaar product gaat mee als referentiefoto. De prompt zegt "alleen deze stukken en niets anders" en noemt elk verboden item: horloge, riem, sjaal, bril, tas, sokken, logo's, auto's, boten, vrouwen, omstanders. Bij halflange beelden gaan de loafers niet mee, omdat de voeten dan buiten beeld vallen.
4. **Kwaliteitscontrole**: elk beeld wordt beoordeeld. Eén afwijking en het wordt opnieuw gemaakt.

Alle vier staan in code met tests (`src/creative/`), zodat de regels niet per ongeluk verdwijnen.

## Het vaste model

Sinds 8 oktober 2026 staat in elke foto en elke video dezelfde man. Nooit een ander model, nooit twee mannen in één beeld. Wie hij is en hoe hij in beeld komt: `brand/model.md`. De ids en promptblokken staan in `data/model.json`.

## Wat er nog nodig is

| Wat | Waarom | Wie |
|---|---|---|
| **De 20 testbeelden beoordelen** | Claude kan ze vanuit deze omgeving niet openen. Jouw oordeel per beeld (goed, afkeuren, waarom) bepaalt wat er aan de prompts verandert | Jij |
| **De originele foto's van het model in hoge resolutie** | De vier referenties zijn kleine schermafbeeldingen (208 tot 348 px breed). Liefst 5 tot 20 foto's van minstens 1024 px: van voren, driekwart, profiel, neutraal en lachend, in verschillend licht. Daarmee worden de Soul ID en het element opnieuw gemaakt en wordt zijn gezicht scherper | Jij |
| **Echte productfoto's** (plat of op paspop: voor, achter, detail) | Veel productfoto's zijn zelf AI-beelden. Het model maakt na wat het ziet: hoe echter de referentie, hoe trouwer het product | Jij of een fotograaf |
| Netwerktoegang voor `cdn.shopify.com`, `d8j0ntlcm91z4.cloudfront.net` en `d2ol7oe51mr4n9.cloudfront.net` | Daarna controleert Claude elk beeld zelf voordat jij het ziet | Jij, in de instellingen van de omgeving |
| **Elke maand screenshots** van de vier rasters (en Zegna, die nog ontbreekt) | De Windsor-koppeling lukt niet. Met screenshots wordt de norm elke maand bijgewerkt met echte beelden | Jij, 5 minuten per maand |
| Cijfers uit Instagram Insights, elke eerste maandag van de maand | Meten of de norm werkt (zie `norm.md`, hoofdstuk 8) | Jij |
| Budget aan credits per maand | Ongeveer 2 credits per beeld in 2k; beelden met het model zijn 4k en kosten meer. Een hoofdstuk van 9 posts is zo'n 20 beelden plus 3 reels | Jij |

## Gevonden in de winkel

- **Milano Onice Set**: de omschrijving is die van de Azzurro Set (Reverso Gilet, Bergamo Polo), terwijl de set een Torino blazer en Cortina polo bevat.
- **Milano Cashmere Lounge Set** zwart, grijs en navy: de omschrijving is die van de Two-Tone set. Beige heeft geen omschrijving, net als de Classic Milano Essential Sets.
- Typfouten in titels: "POSINTANO" (Positano), "LINNEN" (linen).
- Shopify-categorieën zijn niet consequent (dezelfde polo staat als Polos en als Sweaters; de Avorio Set als Shoes). De engine gebruikt daarom de titel.
