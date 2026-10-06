# De ModernoMilano-norm voor Instagram

Elke contentplanning volgt deze norm. Hij staat ook in de code (`src/creative/plan.ts`, `shots.ts`, `prompt.ts`, `casting.ts`, `captions.ts`), zodat hij niet per ongeluk verdwijnt.

**Waar hij op rust** (details en bronnen in `creative-engine/research/2026-10-concurrenten.md`):

1. **Screenshots van het raster** van Brunello Cucinelli, Loro Piana en Boggi Milano, plus de eigen feed, op 6 oktober 2026. Elke tegel is door twee agents apart gecodeerd. Dit is het sterkste bewijs.
2. **Webonderzoek** naar de campagnes van 2025 en 2026 en de accountcijfers. De claims die in deze norm staan, zijn daarna apart nagecontroleerd.
3. **De huisregels van ModernoMilano**: alleen eigen kleding, geen accessoires.

Van Zegna is geen screenshot gezien. Wat over Zegna in deze norm staat, komt uit de gecontroleerde campagnes.

## 1. Ritme

| | Norm | Basis |
|---|---|---|
| Posts per week | **4**: zondag, maandag, woensdag, vrijdag | Eigen keuze. Geen enkel merk publiceert betrouwbare frequenties. Een vast ritme is belangrijker dan veel posten. |
| Lancering van een seizoen | Een week lang 5 posts | Loro Piana post rond lanceringen op opeenvolgende dagen. |
| Tijdstip | 19:30 (testwaarde) | Geen bron. Na 8 weken bijstellen met Instagram Insights. |
| Stories | 5 per week, in het Nederlands | Stories zijn voor verkoop: maten, levertijd, nieuwe kleuren en een productsticker. |

## 2. Hoofdstukken van 9 posts, gelezen in rijen van 3

Een seizoen is één hoofdstuk: één soort plek, één palet, één vast gezicht. Dat deden alle merken in de screenshots:
- **Cucinelli:** rij 1 en 2 zijn één shoot aan een zwarte kust en op een gletsjer.
- **Loro Piana:** negen opeenvolgende tegels zijn één studio-lookbook.
- **Boggi:** één rij is één reisverhaal.

| Rij | Post 1 | Post 2 | Post 3 |
|---|---|---|---|
| 1 | Opener, editorial (los beeld) | Product (carrousel) | Ambacht (carrousel) |
| 2 | Styling (carrousel) | Editorial (reel) | Loafers in beweging (reel) |
| 3 | Wereld (los beeld) | Styling (carrousel) | Editorial (reel) |

Elke rij heeft een man op een plek én een product dat scherp in beeld is.

## 3. Formaten

| Formaat | Per 9 posts | Concurrenten (screenshots) | Eigen feed (screenshot) |
|---|---|---|---|
| Carrousel | **4** (45%) | Loro Piana 67%, Boggi ±60%, Cucinelli 50% | 29% |
| Reel | **3** (33%) | Cucinelli 38%, Boggi 29%, Loro Piana 12% | 0% |
| Los beeld | **2** (22%) | Cucinelli 12%, Loro Piana 21%, Boggi ±4% | 71% |

De carrousels zijn vast opgebouwd:
- **Product:** studio ten voeten uit, halflang, stof van dichtbij.
- **Ambacht:** stof van dichtbij, alle kleuren gestapeld, schets.
- **Styling:** de look op locatie, dezelfde look in de studio, een detail uit dezelfde shoot, de flatlay met alle stukken.

**Reels** maakt de engine van een goedgekeurd beeld in 9:16, met Kling 3.0. Het beeld is het startframe, de beweging is rustig en er is geen geluid.
- Lengte: 6 tot 10 seconden per shot; voor 12 tot 20 seconden combineer je 2 of 3 shots.
- Muziek: één instrument of omgevingsgeluid, uit de Instagram-bibliotheek. Geen trending pop, geen voice-over.
- Geen tekst in beeld.

## 4. Beeldregels (bovenop `beeldregels.md`)

| Regel | Basis |
|---|---|
| Op locatie in natuurlijk licht. Hooguit 1 studiobeeld als hoofdbeeld per 9 posts. | Cucinelli en Boggi zitten bijna altijd op locatie. Loro Piana zet de studio in als lookbook-blok. |
| **Gedempte, filmische nabewerking**: koel en ontkleurd in de herfst en winter, warm gedempt in de zomer. Studio blijft natuurgetrouw. | Cucinelli: 12 van de 24 tegels koel ontkleurd. Zegna en Loro Piana Holiday 2025: "muted tones and soft focus". |
| **Zwart-wit portret** als vast beeldtype, ongeveer 1 per 9 posts. | Cucinelli: 7 van de 24 tegels zwart-wit, vooral close-portretten. |
| Wijd en dichtbij afwisselen: na hooguit 2 wijde beelden volgt een halflang beeld, een detail of een still life. | In alle drie de rasters. |
| Kijk weg van de camera in wijde beelden. Recht in de lens alleen bij een portret. | Cucinelli, en meestal ook Boggi. |
| Bewegen, niet poseren: lopen, een espresso, een kraag rechtzetten. | Zegna AW25: Mikkelsen loopt door Torino en neemt een espresso. Loro Piana FW26: kleding "in motion and in use". |
| Tonaal kleden, met hooguit één accentkleur per look (bijvoorbeeld Bordeaux). | Zegna SS26: "camel on camel, olive on khaki, sand on sand". Loro Piana zet in het lookbook per look één kleur in. |
| Minstens 1 op de 3 posts toont een gelaagde look: cardigan, vest of gilet over een polo of tee. | Cucinelli en Boggi tonen steeds laag over laag. |
| In een wijd landschap is de man minstens een kwart van de beeldhoogte. Het product moet herkenbaar blijven. | Eigen keuze: wij moeten verkopen, en hebben het bereik van de grote merken niet. |
| **Nooit** auto's, boten of andere merkobjecten. | In de rasters van Cucinelli en Loro Piana staan geen merkobjecten. In de eigen feed stonden een Mercedes, een Aston Martin en een Riva. |

## 5. Beeldtypes (`src/creative/shots.ts`)

| Pijler | Beeldtypes |
|---|---|
| Product | studio ten voeten uit, studio halflang, aan de hanger, loafers in beweging |
| Ambacht | stof van dichtbij, alle kleuren gestapeld, schets, still life |
| Styling | flatlay van de look (plus de carrouselbeelden hierboven) |
| Editorial | zwarte kust (herfst/winter), Milanese binnenplaats, stille architectuur, bibliotheek bij het vuur (herfst/winter), Italiaans dorp, balustrade aan het water, bewoond interieur, stenen kade (zomer) |
| Wereld | weids landschap, sneeuwveld (herfst/winter), eilandkust (zomer), espresso op het plein, portret in zwart-wit, twee generaties |

## 6. Casting (`src/creative/casting.ts`)

- **Eén vast hoofdgezicht per hoofdstuk**, 35 tot 55 jaar. Grijs haar of een grijze baard mag.
  - Basis: Zegna draagt elk seizoen met Mads Mikkelsen. Cucinelli zet ervaren modellen naast jonge; zijn Fall 2026-edit draait om Francisco Henriques.
- **Een tweede, jonger gezicht** (25 tot 35) alleen voor twee generaties of twee vrienden.
- **Alleen mannen.** We verkopen alleen herenkleding.
- Geen bekende gezichten en geen lookalikes: wij hebben geen ambassadeurs.
- Zodra je een gezicht kiest, wordt het een vast Higgsfield Element. Dan komt in elk beeld dezelfde man terug.

## 7. Captions (`src/creative/captions.ts`)

- **Engels** in de feed, Nederlands in Stories en DM's.
  - Basis: alle vier de merken posten Engels. Loro Piana opent met een kop als "A journey to the mountains." (Particl).
- **Opbouw:**
  1. Een kop van 3 tot 7 woorden, met een punt.
  2. Eén of twee zinnen over stof en moment.
  3. `Wearing:` met de exacte productnamen, alle stukken getagd.
  4. Hooguit 4 hashtags: `#ModernoMilano`, de seizoenstag (`#ModernoMilanoFW26`) en hooguit 2 uit de categorie.
- **Geen** emoji, geen uitroeptekens, geen korting of "shop now" in de feed.
- Geen claims die niet in de productdata staan.
- Geen campagnetitels of namen van de concurrenten.

Voorbeeld:

```text
Layers of quiet warmth.
A cashmere cardigan over a knit polo, one colour from collar to loafer.
Wearing: Milano Cashmere Vela in Rosso, Milano Cashmere Cortina Polo in Charcoal, Milano Cashmere Como Pant in Dark Grey, Milano Suede Loafers in Moro.

#ModernoMilano #ModernoMilanoFW26 #cashmere #quietluxury
```

## 8. Wat we meten

Vergelijk ons niet met de grote huizen: met miljoenen volgers liggen hun interactiecijfers laag. Ter vergelijking, interactie als (likes + reacties) gedeeld door volgers:
- Loro Piana: ongeveer 0,1%.
- Zegna: ongeveer 0,24 tot 0,33%.
- Boggi en Cucinelli: lage zekerheid.

| Wat | Startdoel |
|---|---|
| Interactie per post (likes + reacties) / volgers | minimaal 1,5%; 0,4% is de ondergrens |
| Bewaringen op craft- en stylingcarrousels | 1% van het bereik |
| Keren gedeeld per reel | 0,5% van het bereik |
| Kijktijd per reel | minstens de helft van de lengte |
| Sessies vanuit Instagram (Shopify) | elke maand meer dan de maand ervoor |
| Volgersgroei | minstens 2% per maand |
| Ritme | 100% van de geplande posts op tijd |

Zolang er geen Instagram-koppeling is, haal je elke eerste maandag van de maand de cijfers zelf uit Instagram Insights en Shopify Analytics. Na 8 weken worden de doelen bijgesteld op de eigen cijfers.
