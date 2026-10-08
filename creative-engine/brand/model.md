# Het model van ModernoMilano: Luca

Sinds 8 oktober 2026 staat er in alle content één en dezelfde man: in elke foto en in elke video. Er komt nooit een ander model in beeld, en nooit twee mannen tegelijk. De naam Luca is alleen intern, om naar hem te verwijzen.

De gegevens die de engine gebruikt staan in `creative-engine/data/model.json`. Dat bestand is de bron van waarheid; dit document legt het uit.

## Wie hij is

Luca is midden twintig en heeft:

- donker kastanjebruin haar, bovenop lang en vol, naar achteren gekamd vanaf een zachte scheiding rechts, zodat er een golf over zijn linkerslaap valt;
- dikke, donkere, bijna rechte wenkbrauwen, laag boven diepliggende hazelbruine ogen;
- een brede kaak met scherpe hoeken en een brede, vierkante kin;
- volle lippen, waarvan de onderlip iets naar voren staat;
- een vage stoppelbaard en een atletisch postuur met brede schouders.

Hij kijkt rustig en serieus, meestal langs de camera. Hij lacht nooit breeduit.

Referentiefoto's (van de eigenaar): `brand/assets/model/ref-1.jpg` t/m `ref-4.jpg`.

| Foto | Wat je ziet |
|---|---|
| ref-1 | vooraanzicht, zittend op een dak in Milaan |
| ref-2 | close-up driekwart, Navigli (haar hier anders gekamd, niet de standaard) |
| ref-3 | van achteren/opzij, kijkt omlaag; laat de echte haarkleur zien |
| ref-4 | driekwart, lopend op een brug |

## Waaraan je hem herkent

1. **Wenkbrauwen**: laag, dik, donker en bijna recht, vlak boven de ogen. Ze zijn nooit gebogen of opgetrokken.
2. **Ogen**: diepliggend onder een duidelijke wenkbrauwboog, met zware oogleden en hazelbruine irissen. In de zon lijken ze lichter (amber), maar ze zijn nooit blauw of grijs.
3. **Gezicht**: rechthoekig, met een brede kaak met scherpe hoeken onder de oren en een brede, vierkante kin.
4. **Mond**: volle lippen, de onderlip voller en iets naar voren, met de mondhoeken neutraal tot iets omlaag.
5. **Neus**: recht en vrij lang, smal bovenaan, met een ronde punt.
6. **Haar**: donker kastanjebruin en alleen in direct zonlicht warmer. Het is bovenop lang, omhoog en naar achteren gekamd met een zachte golf over de linkerslaap. De zijkanten zijn vol en gaan over de bovenkant van de oren naar achteren. Hij heeft geen fade en geen undercut.
7. **Huid en postuur**: lichte, warme huid met een vage stoppelbaard, een lange nek en brede, ontspannen schouders.

## Wat nooit mag

Hij krijgt nooit:

- een baard, sik of snor;
- een leeftijd boven de dertig, of grijs haar;
- blauwe of grijze ogen;
- een smalle V-kaak of puntige kin;
- hoge of gebogen wenkbrauwen;
- blond, rood of zwart haar, een fade, wet-look gel of een middenscheiding met gordijntjes.

Verder nooit een brede tandenlach, en nooit een andere man of twee mannen in één beeld. Hij lijkt niet op een acteur of bekend persoon, en we vergelijken hem ook met niemand.

## Hoe hij in beeld komt

### Foto's met producten (de standaard)

- **Model**: Nano Banana Pro, 4K, 4:5.
- **Prompt**: zet het element `<<<4c170ca1-19b2-49db-b217-d1c6e0b543e7>>>` erin. Higgsfield voegt dan zelf zijn gezicht toe.
- **Productfoto's**: de echte foto's als `image_references`, maximaal 4 per beeld.
- **Vaste tekstblokken** uit `model.json` → `prompt`: `keep_en`, `realism_en`, `light_default_en`, `expression_en` en `framing_en`.

### Portret- en sfeerfoto's waar het gezicht centraal staat

- **Model**: Soul 2.0 met Soul ID `9047016d-76a7-454b-bc9b-c2268778f00a` (`soul_2`), 2K, 3:4. Daarna bijsnijden naar 4:5.
- **Waarom**: dit geeft de echtste huid en het vaste gezicht.
- **Beperking**: er past maar één productfoto per beeld bij. Gebruik het dus voor eenvoudige outfits.

### Video

Maak nooit video vanuit alleen tekst. Begin altijd met een goedgekeurde foto van hem:

- **Model**: Seedance 2.0, 5 seconden, 1080p.
- **Startbeeld**: `start_image` is die foto.
- **Prompt**: het element in de prompt, zodat het gezicht vast blijft.
- **Beweging**: rustig en natuurlijk, zoals lopen, een mouw rechttrekken of over het water kijken. Geen volledige hoofddraai en niets voor zijn gezicht.

### Altijd

- Maximaal 12 beelden per batch, daarna eerst controleren.
- In elk beeld met een gezicht is dat gezicht minstens ongeveer 500 px breed.
- **Controle**: leg elk beeld naast ref-1 en ref-4. Is het niet duidelijk dezelfde man, dan wordt het afgekeurd.

## Waarom zo (lessen uit de batch van 100)

De batch van 100 oogde te AI. De oorzaken:

- tien wisselende verzonnen mannen in plaats van één gezicht;
- kleine gezichten in beelden van top tot teen;
- geforceerde lachjes en catalogusposes recht op de camera af;
- lege, steriele straten;
- licht op de man dat niet klopte met de achtergrond;
- filmrol-woorden in de prompt, die nepranden gaven.

De tekstblokken in `model.json` draaien dat allemaal om: één gezicht, waist-up, rustige gesloten mond, één lichtbron die je kunt aanwijzen, wat leven in de verte en geen filmrandjes.

## Hoe het personage gebouwd is

1. De vier foto's van de eigenaar zijn klein (200–350 px breed). Ze zijn opgeschaald naar 4K, en daarna is gecontroleerd dat het gezicht niet veranderde.
2. Van drie daarvan (ref-1, ref-4, ref-2) is het Higgsfield-element `modernomilano-model` gemaakt.
3. Met dat element zijn 8 neutrale portretten gemaakt (voor, driekwart, profiel, verschillende lichtsituaties). 7 kwamen overeen en zijn goedgekeurd.
4. Op de 4 foto's en die 7 portretten is de Soul ID "ModernoMilano Luca" getraind (Soul 2.0, 25 credits).

## Wat het nog beter maakt

De originele, grote bestanden van de vier foto's zouden het gezicht nog scherper vastleggen. Nog beter zijn 5 tot 20 foto's van minstens 1024 px: van voren, driekwart, profiel, neutraal en lachend, in verschillend licht. Met zulke foto's trainen we de Soul ID opnieuw en vervangen we het element.

## Onzeker (op deze kleine foto's niet goed te zien)

- De exacte oogkleur: hazelbruin, in de zon amber.
- Het profiel van de neus en hoe ver de kin naar voren komt; er is geen zuiver profiel.
- Lengte en lichaam onder de borst. Bij foto's van top tot teen houden we lange benen en een platte buik aan.
- Hoe dicht de stoppels zijn. We houden altijd dezelfde lichte schaduw aan.
