# ModernoMilano creative engine

Maakt Instagram-content in de stijl van Zegna, Loro Piana, Brunello Cucinelli en Boggi Milano, met **uitsluitend kleding uit de eigen winkel**.

```text
Shopify (232 actieve producten) ──► garderobe ──► looks ──► shots ──► prompt + productfoto's ──► Higgsfield ──► kwaliteitscontrole ──► jij
                                       ▲            ▲         ▲
Bestsellers (ShopifyQL) ───────────────┘            │         │
Merk-DNA en paletten ───────────────────────────────┘         │
Concurrenten op Instagram (Windsor.ai) ───────────────────────┘
```

## Gebruiken

Vraag het aan Claude in deze repo, bijvoorbeeld:

- "Maak een raster van 9 posts voor volgende week."
- "Maak 4 beelden van de nieuwe Torino blazer, studio en architectuur."
- "Wat posten de concurrenten deze maand en wat betekent dat voor ons?"

Claude volgt dan de skill in `.claude/skills/creative-engine/SKILL.md`.

Zelf draaien kan ook:

```bash
npm run creative:wardrobe -- --from export.json   # garderobe opnieuw opbouwen
npm run creative:plan -- --posts 9 --start 2026-10-12 --anchor milano-cashmere-torino-blazer-perla
npx vitest run src/creative                       # de regels testen
```

Een voorbeeldplan staat in `output/plan-2026-10-12.md`.

## Hoe de regel "alleen eigen kleding" wordt bewaakt

1. **Garderobe**: alleen actieve producten, ingedeeld naar zone (top, tussenlaag, buitenlaag, broek, schoen). Sets worden opgesplitst in hun stukken.
2. **Looks**: precies één top en één broek, hooguit één tussenlaag, één buitenlaag en één paar loafers. Eén palet, maximaal drie kleurfamilies. Zonder loafers geen voeten in beeld.
3. **Prompt**: elk product gaat mee als referentiefoto. De prompt zegt "alleen deze stukken en niets anders" en noemt elk verboden item (horloge, riem, sjaal, bril, tas, sokken, logo's...).
4. **Kwaliteitscontrole**: elk beeld wordt beoordeeld. Eén afwijking en het wordt opnieuw gemaakt.

Alle vier staan in code met tests (`src/creative/`), zodat de regels niet per ongeluk verdwijnen.

## Eerste test

Op 6 oktober 2026 is één testbeeld gemaakt op Higgsfield (Nano Banana Pro, 4:5, 2k, 2 credits): Torino Blazer Tortora, Cashmere Camicia Sabbia, Sartoriale Pant Espresso en Suede Loafers Moro in de studio. Job `31ef523d-5f1c-408d-b51a-f881a0f253fd`. Higgsfield meldt de job als `nano_banana_2`, terwijl er `nano_banana_pro` gevraagd is. Vergelijk bij twijfel de kwaliteit van beide.

## Wat er nog nodig is

| Wat | Waarom | Wie |
|---|---|---|
| Windsor.ai **Instagram Public** koppelen en de vier handles toevoegen | Echte posts, likes en reacties van de concurrenten, maandelijks | Jij, via de link die Claude geeft |
| Windsor.ai **Instagram** (eigen account) koppelen | Meten wat bij ons werkt, en later posten vanuit Claude | Jij |
| Netwerktoegang in de cloudomgeving voor `cdn.shopify.com`, `d8j0ntlcm91z4.cloudfront.net` en `d2ol7oe51mr4n9.cloudfront.net` | Zonder deze toegang kan Claude de gemaakte beelden niet zelf bekijken en dus niet zelf controleren | Jij, in de instellingen van de omgeving |
| **Echte productfoto's** (plat of op paspop: voor, achter, detail) | Veel huidige productfoto's zijn zelf al AI-beelden. Het model maakt na wat het ziet: hoe echter de referentie, hoe trouwer het product | Jij of de fotograaf |
| **Vaste gezichten** van het merk kiezen | Herkenbaarheid zoals bij de grote merken; wordt een Higgsfield Element dat in elke prompt meegaat | Samen: Claude maakt voorstellen, jij kiest |
| **Taal van de captions** (Engels, Nederlands of beide) en de markten | Toon en woordkeuze | Jij |
| **Hoeveel posts per week** en welke dagen | Ritme in het plan (nu ma, wo, vr) | Jij |
| **Budget aan credits** per maand | Rond 2 credits per beeld, plus herkansingen | Jij |

## Gevonden in de winkel

- **Milano Onice Set**: de omschrijving is die van de Azzurro Set (Reverso Gilet, Bergamo Polo), terwijl de set een Torino blazer en Cortina polo bevat.
- **Milano Cashmere Lounge Set** zwart, grijs en navy: de omschrijving is die van de Two-Tone set. Beige heeft geen omschrijving, net als de Classic Milano Essential Sets.
- Typfouten in titels: "POSINTANO" (Positano), "LINNEN" (linen).
- Shopify-categorieën zijn niet consequent (dezelfde polo staat als Polos en als Sweaters; de Avorio Set als Shoes). De engine gebruikt daarom de titel.
