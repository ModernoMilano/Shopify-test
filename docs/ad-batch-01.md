# Ad-batch 01: tien ads gebouwd op de bewezen winnaars

Gemaakt 2026-10-12 uit de creative engine (`docs/creative-insights.md`, 767 ads, € 104.559 spend). Elke ad kopieert
de structuur van een winnaar (product, beeldtype, kop, body) en varieert één ding, zodat we leren wat de winst veroorzaakt.
Alleen eigen kleding uit de Shopify-catalogus, logo via de merkkit. Beelden gegenereerd met Higgsfield Ads Studio op basis
van de productpagina's (foto's van de site als referentie).

## Aanpak

1. **Winnaar kiezen**: concepten met oordeel "winnaar" (minimaal € 300 spend, 5 aankopen, ROAS boven 2,0).
2. **Product op voorraad of dropship**: jackets, cashmere sets en polo's worden niet op voorraad bijgehouden (dropship, altijd te koop); sets, vests, tees en broeken hebben echte voorraad.
3. **Copy uit de bibliotheek**: alleen koppen en bodies die zelf al bewezen zijn, hoogstens met een ander product ingevuld.
4. **Eén variabele per ad**: ander product, andere kleur, of kop met of zonder korting. Niet alles tegelijk veranderen.
5. **Formaat 3:4** (dichtst bij de 4:5-feedpost waar de winnaars in draaiden), logo klein in de hoek, geen tekst over het gezicht.

## De tien ads

| # | Gebouwd op (winnaar, ROAS) | Product | Beeld | Kop | Body | Markt om te testen |
|---|---|---|---|---|---|---|
| 1 | MM_Bestseller_Jacket_Studio_01 (2,59x, € 18k) | Signature Reversible Jacket navy | Studio, model, egale achtergrond, product groot in beeld, geen tekst in beeld | Timeless Style. Modern Essence. | This is what timeless actually looks like. Italian-inspired craftsmanship, cut for the way you live now. Discover the pieces built to outlast every trend. | Worldwide |
| 2 | Jacket studio + Bundle Up (2,45x) | Signature Reversible Jacket black | Studio, jacket open over tee met bijpassende broek: complete look | Bundle Up, Save More | Built for wherever the day takes you. Pair it with the rest of the edit and save when you bundle. | Worldwide, UK/IE |
| 3 | MM_Cashmere_Tracksuit_Travel_01 (2,38x, € 7k) | Cashmere Lounge Set beige | Reizen/lounge-setting, zittend, zachte stof zichtbaar | Cashmere Tracksuits Now On Sale | Luxuriously soft. Effortlessly refined. Designed to move with you. Our bestselling cashmere tracksuit is now on sale, comfort and elevated style for wherever life takes you. | UK/IE, DE/AT |
| 4 | 15-8 BATCH 2 (2,67x) | Cashmere Lounge Set navy | Herfst buiten, koude ochtend, close-up van de knit | Cashmere Collection, 50% Off | The cold is coming. Our cashmere collection is 50% off, pure cashmere, refined for autumn, made to last well beyond one season. | Worldwide |
| 5 | Photo-Closeup-Polo-Beach (2,24x, € 15k) | Portofino Polo stone beige | Close-up op het strand, kraag en stof scherp, gezicht half | Timeless Style. Modern Essence. | (zelfde body als ad 1) | UK/IE, DE/AT |
| 6 | UGC_BundleSave_Beige_Static_v1 (2,77x, € 8k) | Knitted Vest beige + Mercer Tee wit + Signature Trousers beige | UGC-stijl, telefoonfoto, spiegel of straat, hele outfit | We did the matching for you | Tired of guessing what goes with what? Every ModernoMilano set is already put together for you. | Worldwide, USA |
| 7 | Lounge-set Video Ad 2 (3,19x) | Exclusive Milano Lounge Set beige | Thuis, ontspannen, set compleet zichtbaar | Up To 50% OFF – Limited Stock | A style worth coming back to. Discover the Milano Lounge Set — refined, comfortable, and designed for effortless everyday wear. ✅Premium tracked worldwide delivery. ✅30-day money-back guarantee. ✅Wear now, pay later with Klarna. | Worldwide |
| 8 | BUNDLE AD 8 (2,66x) | Exclusive Milano Lounge Set black | Flatlay of model, zwart op lichte achtergrond | Stop Buying Pieces. Start Buying Looks. | Stop buying pieces, start buying looks. Our black set takes the guesswork out of getting dressed, effortless and ready in one go. | UK/IE |
| 9 | BUNDLE AD 4 (3,08x) | Imperial Milano Zip Set gray | Model, set compleet, prijsanker in de kop | More Pieces. One Price. | More pieces, one price, zero compromise on quality. Our grey zip set brings together everything you need for a complete, versatile wardrobe. | UK/IE, DE/AT |
| 10 | UNBOXING (2,91x) | Reverso Gilet navy | Verpakking open, gilet gevouwen in de doos, logo op de doos | Luxury, Delivered Properly. | Every ModernoMilano piece arrives the way it deserves to. Folded, boxed, and ready to give or keep. This is the Reverso, in our signature packaging. | Worldwide |

## Testplan

- Eén nieuwe ABO-campagne "CE | Batch 01 | Worldwide", 10 adsets van € 30 tot € 40 per dag, Advantage+ audience, zelfde landingspagina als het product.
- 4 dagen niet aanraken. Daarna: CPA boven € 110 of 0 aankopen bij € 120 spend → uit. ROAS boven 2,0 bij minimaal € 150 spend → budget +20% per 3 dagen (protocol), en de ad als kopie in de scaling-campagne.
- De creative engine haalt de cijfers automatisch op; na een week staat elk van deze ads met oordeel op `/creatives`.

## Wat we leren per ad

- 1 vs 2: werkt de jacket beter alleen (hero) of als complete look?
- 3 vs 4: cashmere met "now on sale" of met "50% off, the cold is coming"?
- 7 vs 8 vs 9: dezelfde set-belofte in drie koppen (korting + garanties, "looks", "one price").
- 5: is de polo-close-up herhaalbaar met een ander polo-product?
- 6: is de UGC-stijl herhaalbaar met een andere set?
- 10: werkt unboxing met een ander product dan de Bellagio?
