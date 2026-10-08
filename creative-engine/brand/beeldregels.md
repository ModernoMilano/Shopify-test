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

Ook nooit: logo's, labels, monogrammen, tekst (met één uitzondering: het ModernoMilano-necklabel, zie hieronder), watermerken, tattoos, andere mensen die je echt ziet (op openbare plekken mogen alleen 2 of 3 verre voorbijgangers, zie hoofdstuk 3), vrouwen (we verkopen geen dameskleding), en **merktekens**: een klassieke auto of houten motorboot mag als decor (Zegna doet het in Venetië, en het staat in je eigen moodboard), maar altijd zonder embleem, logo of leesbaar kenteken, en nooit als hoofdonderwerp.

## 3. Clean look en echt beeld

| Wel | Niet |
|---|---|
| Rustige compositie, uit het midden, iets zachts op de voorgrond | Drukke achtergronden, winkelstraten, auto's, maar ook lege, steriele straten; gecentreerde, symmetrische plaatjes |
| Eén lichtbron die je kunt aanwijzen (lage zon, raam, lamp), en het licht op hem klopt met de achtergrond | Flitslicht, harde schaduwen, neon, een onzichtbare softbox op zijn gezicht |
| Tonaal palet, maximaal drie kleurfamilies | Felle contrasten, patronen naast patronen |
| Echte huid: mat, fijne structuur, een vage stoppelbaard | HDR, gladde CGI-huid, wasglans, opgeplakte poriën of puistjes, zware filters, vignet |
| Stof met zichtbaar breisel en zachte plooien bij ellebogen en taille | Breisel als vilt, perfect geperste of gespiegelde vouwen |
| Gedempte nabewerking met zachte contrasten (warm of koel per seizoen, zie de norm), zwart-wit voor portretten (Cucinelli). Korrel komt er pas in de nabewerking bij | Verzadigde blauwe luchten als standaard, teal-en-oranje, filmranden |
| Steen, travertin, kalkpleister, eiken, linnen | Plastic, glimmende oppervlakken, merkspullen |
| Model dat rustig en zelfverzekerd oogt: mond dicht, blik langs de camera | Tandenlach, recht in de lens poseren, overdreven poses |

**Echt, niet AI.** De batch van 100 (7 oktober) oogde te AI. Sindsdien:

- **Geen filmwoorden in de prompt**: geen Kodak, Portra, Vision3, "on film" of "film grain". Die gaven nepranden en een korrellaag. Alleen camera en lens.
- **Uitsnede**: standaard tot de taille of driekwart, van opzij, over de schouder of van achteren. Ten voeten uit hooguit 2 op de 10 beelden.
- **Gezicht groot genoeg**: elk beeld met een persoon in 4k, en zijn gezicht is minstens ongeveer 500 px breed.
- **Openbare plekken** (straat, kanaal, station): 2 of 3 verre voorbijgangers, klein en onscherp, gezichten onleesbaar. Winkelborden alleen ver weg en onleesbaar.
- **Plekken en licht**: Milaan in de meerderheid. Eén plek hooguit ongeveer 15% van een set, ook het Comomeer. Hooguit 1 zonsondergang of blauw uur per 10 beelden, en ook bewolkte of grijze ochtenden.
- **Kleine batches**: hooguit 12 beelden, dan eerst controleren.

De Engelse tekstblokken hiervoor staan in `creative-engine/data/model.json` (`realism_en`, `light_default_en`, `expression_en`, `framing_en`, `public_places_en`).

**Uitzondering: het necklabel.** Sinds 7 oktober mag het eigen ModernoMilano-label in beeld, ingenaaid binnenin de nek: ivoor satijn, fijne stiklijn langs de randen, korte kanten omgevouwen en vastgestikt, met het zwarte script-logo 'ModernoMilano' en verder niets (geen maatlabel). Referenties: `brand/assets/necklabel.jpg` en het logo. Altijd rechtop en correct gespeld; een verkeerd gespeld of los, onleesbaar label is afkeur.

Toegestane rekwisieten (geen kleding): een espressokopje, een olijftak, een linnen stoel, een stenen balustrade. Maximaal één per beeld.

## 4. Casting: één vast model

- Sinds 8 oktober staat in **alle** foto's en video's dezelfde man: het ModernoMilano-model. Wie hij is en hoe hij in beeld komt: [`model.md`](model.md). De gegevens voor de engine staan in `creative-engine/data/model.json`.
- Nooit een andere man, nooit twee mannen in één beeld, geen tweede gezicht.
- Hetzelfde gezicht, haar, leeftijd en postuur in elk beeld. In wijde beelden mag hij van opzij of van achteren te zien zijn. Is zijn gezicht zichtbaar, dan klopt het met de referentiefoto's (`brand/assets/model/ref-1.jpg` t/m `ref-4.jpg`).
- Alleen mannen. Rustig en zelfverzekerd, mond dicht, blik meestal langs de camera. Hooguit een lichte glimlach met gesloten mond, nooit een tandenlach.
- Geen sieraden, geen tattoos, geen zichtbare piercings. Hij lijkt niet op een bekend persoon en we vergelijken hem met niemand.

## 5. Formaten

| Waar | Formaat |
|---|---|
| Instagram feed en carrousel | 4:5 (1080 × 1350) |
| Stories en reels | 9:16 (1080 × 1920), de kern binnen het 4:5-midden |
| Productpagina | 4:5 of 3:4 |

Tekst en logo komen er pas bij het posten op, nooit in het gegenereerde beeld. Het ingenaaide necklabel is de enige uitzondering.

## 6. Kwaliteitscontrole

Een beeld gaat pas naar jou als het deze vragen doorstaat (`QA_QUESTIONS` in `src/creative/qa.ts`):

1. Staat er een kledingstuk of schoen in beeld dat niet in de look zit?
2. Lijkt elk product op zijn productfoto (kleur, stof, kraag, knopen, zakken, lengte)?
3. Zie je een accessoire?
4. Zie je een logo, label of tekst, anders dan het correct gespelde ModernoMilano-necklabel?
5. Klopt het aantal personen (een hand telt als één): alleen hij, of niemand bij een still life? Voorbijgangers alleen ver weg, klein en onscherp, op een openbare plek.
6. Loafers zonder sokken, of voeten uit beeld als er geen loafers in de look zitten?
7. Is het clean, en klopt het licht op hem met de achtergrond?
8. Kloppen handen, vingers en gezicht?
9. **Is het dezelfde man als op ref-1 en ref-4?** Leg ze naast elkaar: wenkbrauwen, ogen, kaak, lippen, haar, leeftijd en postuur. Is zijn gezicht minstens ongeveer 500 px breed?
10. Ziet het eruit als een echte foto: huid zonder wasglans of opgeplakte poriën, stof met echt breisel en plooien, mond dicht, geen filmranden in de hoeken?

Eén nee is afgekeurd. Dan wordt het beeld opnieuw gemaakt, niet bijgewerkt. Bij een reel stel je vraag 9 op het begin, het midden en het einde: verandert zijn gezicht, dan is de reel afgekeurd.
