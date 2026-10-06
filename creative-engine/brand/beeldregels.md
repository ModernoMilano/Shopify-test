# Beeldregels ModernoMilano

Deze regels gelden voor elk beeld dat de engine maakt. Ze staan ook in de code (`src/creative/prompt.ts` en `src/creative/qa.ts`), zodat ze niet vergeten kunnen worden.

## 1. Alleen ModernoMilano aan het lijf

- Elk zichtbaar kledingstuk en elke schoen is een **actief product** uit de winkel (`creative-engine/data/wardrobe.json`).
- Elk product gaat mee als **referentiefoto**, zodat het model het namaakt in de juiste kleur, het juiste breisel, de juiste kraag, knopen en zakken.
- Een look heeft precies één bovenstuk en één broek of short. Daarnaast mag er maximaal één tussenlaag (cardigan, gebreide gilet), één buitenlaag (blazer, jas, bodywarmer) en één paar loafers bij.
- **Geen loafers in de look, dan geen voeten in beeld.** Het beeld wordt dan op kniehoogte of hoger afgesneden.
- Loafers worden **zonder sokken** gedragen, met blote enkels.

## 2. Niets wat we niet verkopen

ModernoMilano verkoopt geen accessoires, dus ze komen nooit in beeld:

> horloge, armband, ring, ketting, oorbellen, riem, das, vlinderdas, pochet, sjaal, hoed, pet, muts, zonnebril, bril, tas, rugzak, aktetas, handschoenen, sneakers, boots, zichtbare sokken, een onderhemd dat uitsteekt, een jas of trui die niet in de referenties zit.

Ook nooit: logo's, labels, monogrammen, tekst, watermerken, tattoos, andere mensen op de achtergrond, vrouwen (we verkopen geen dameskleding), en **merktekens**: een klassieke auto of houten motorboot mag als decor (Zegna doet het in Venetië, en het staat in je eigen moodboard), maar altijd zonder embleem, logo of leesbaar kenteken, en nooit als hoofdonderwerp.

## 3. Clean look

| Wel | Niet |
|---|---|
| Rustige compositie, veel lege ruimte | Drukke achtergronden, winkelstraten, auto's |
| Zacht natuurlijk licht (raam, bewolkt, gouden uur) | Flitslicht, harde schaduwen, neon |
| Tonaal palet, maximaal drie kleurfamilies | Felle contrasten, patronen naast patronen |
| Echte huidstructuur, lichte filmkorrel | HDR, gladde CGI-huid, zware filters, vignet |
| Gedempte filmische nabewerking op locatie, zwart-wit voor portretten (Cucinelli) | Verzadigde blauwe luchten als standaard |
| Steen, travertin, kalkpleister, eiken, linnen | Plastic, glimmende oppervlakken, merkspullen |
| Model dat rustig en zelfverzekerd oogt | Overdreven poses, schreeuwerige expressies |

Toegestane rekwisieten (geen kleding): een espressokopje, een olijftak, een linnen stoel, een stenen balustrade. Maximaal één per beeld.

## 4. Casting

- Eén vast hoofdgezicht per hoofdstuk, 35 tot 55, grijs mag (Zegna met Mikkelsen, Cucinelli met ervaren modellen). Een tweede, jonger gezicht alleen voor twee mannen in beeld. Zie `src/creative/casting.ts`.
- Alleen mannen. Rustig en zelfverzekerd. Glimlachen mag (Cucinelli), staren in de verte ook (Zegna, Loro Piana). In wijde beelden kijkt hij weg van de camera.
- Geen sieraden, geen tattoos, geen zichtbare piercings, geen bekende gezichten of lookalikes.

## 5. Formaten

| Waar | Formaat |
|---|---|
| Instagram feed en carrousel | 4:5 (1080 × 1350) |
| Stories en reels | 9:16 (1080 × 1920), de kern binnen het 4:5-midden |
| Productpagina | 4:5 of 3:4 |

Tekst en logo komen er pas bij het posten op, nooit in het gegenereerde beeld.

## 6. Kwaliteitscontrole

Een beeld gaat pas naar jou als het deze vragen doorstaat (`QA_QUESTIONS` in `src/creative/qa.ts`):

1. Staat er een kledingstuk of schoen in beeld dat niet in de look zit?
2. Lijkt elk product op zijn productfoto (kleur, stof, kraag, knopen, zakken, lengte)?
3. Zie je een accessoire?
4. Zie je een logo, label of tekst?
5. Klopt het aantal personen (een hand telt als één), en is de achtergrond leeg?
6. Loafers zonder sokken, of voeten uit beeld als er geen loafers in de look zitten?
7. Is het clean?
8. Kloppen handen, vingers en gezicht?

Eén nee is afgekeurd. Dan wordt het beeld opnieuw gemaakt, niet bijgewerkt.
