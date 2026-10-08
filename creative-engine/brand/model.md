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

Verder nooit een brede tandenlach, en nooit een andere man of twee mannen in één beeld. Verre, onscherpe voorbijgangers op een openbare plek tellen niet mee. Hij lijkt niet op een acteur of bekend persoon, en we vergelijken hem ook met niemand.

## Hoe hij in beeld komt

### Foto's met producten (de standaard)

- **Model**: Nano Banana Pro, 4K, 4:5.
- **Prompt**: zet het element `<<<4c170ca1-19b2-49db-b217-d1c6e0b543e7>>>` erin. Higgsfield voegt dan zelf zijn gezicht toe.
- **Referenties**: alleen de echte productfoto's als `image_references`, maximaal 4 per beeld (een look van 5 stukken: één per stuk). Geen gezichtsfoto's: het element brengt zijn gezicht.
- **Vaste tekstblokken** uit `model.json` → `prompt`: `keep_en`, `realism_en`, `light_default_en`, `expression_en` en `framing_en`, en op openbare plekken `public_places_en`. Niet `identity_en`: een gezicht in woorden vecht met het element.
- **Eerst testen**: de nummering met element plus productfoto's is nog niet getest. Maak vóór de eerste batch één testbeeld en controleer dat "reference image #n" het juiste stuk pakt.
- **Terugval zonder element**: ref-1, ref-4 en ref-2 in 4K (`face_ref_order`) als eerste referenties (#1-#3), dan de producten, met `identity_en` en zonder placeholder. Ref-3 gaat niet mee: van achteren zegt hij te weinig over zijn gezicht.

### Portret- en sfeerfoto's waar het gezicht centraal staat

- **Model**: Soul 2.0 met Soul ID `9047016d-76a7-454b-bc9b-c2268778f00a` (`soul_2`), 2K, 3:4. Daarna bijsnijden naar 4:5.
- **Waarom**: dit geeft de echtste huid.
- **Beperking**: zonder productfoto. Soul gebruikt een meegegeven foto als basis en maakt dan die productfoto na, zonder hem (getest 8 oktober). De kleding staat dus alleen in de tekst en klopt maar bij benadering, en zijn gezicht lijkt minder dan met het element. Alleen voor snelle sfeerportretten buiten het plan, met een eenvoudige outfit.

### Video

Maak nooit video vanuit alleen tekst. Begin altijd met een goedgekeurde foto van hem:

- **Model**: Kling 3.0 (`mode: "pro"`, zonder geluid), 5 seconden, 9:16. Seedance 2.0 kan ook, maar kost ongeveer vijf keer zoveel.
- **Startbeeld**: `start_image` is die foto, in 9:16.
- **Prompt**: het element in de prompt, zodat het gezicht vast blijft. Kling gebruikt het element alleen samen met dat startbeeld.
- **Beweging**: rustig en natuurlijk, zoals lopen, een mouw rechttrekken of over het water kijken. Geen volledige hoofddraai en niets voor zijn gezicht.

### Altijd

- Maximaal 12 beelden per batch, daarna eerst controleren.
- In elk beeld met een gezicht is dat gezicht minstens ongeveer 500 px breed. Dat geldt alleen voor foto's waarin zijn gezicht herkenbaar in beeld is. In wijde beelden (landschap, sneeuwveld, kust) staat hij van achteren of opzij en is zijn gezicht niet te lezen; dan vervalt deze regel. Bij een reel ook.
- **Controle**: leg elk beeld waarin zijn gezicht herkenbaar is naast ref-1 en ref-4. Is het niet duidelijk dezelfde man, dan wordt het afgekeurd.

## Waarom zo (lessen uit de batch van 100)

De batch van 100 oogde te AI. De oorzaken:

- tien wisselende verzonnen mannen in plaats van één gezicht;
- kleine gezichten in beelden van top tot teen;
- geforceerde lachjes en catalogusposes recht op de camera af;
- lege, steriele straten;
- licht op de man dat niet klopte met de achtergrond;
- filmrol-woorden in de prompt, die nepranden gaven.

De tekstblokken in `model.json` draaien dat allemaal om: één gezicht, waist-up, rustige gesloten mond, één lichtbron die je kunt aanwijzen, wat leven in de verte en geen filmrandjes.

## Lessen uit de set van 25 (8 oktober)

- **Haar:** het element maakt zijn haar in de nek vaak iets langer dan op de referentiefoto's. Dat is geen reden om af te keuren. Wel afkeuren: een lok over het voorhoofd, een andere kleur, een baard of een ander gezicht.
- **Haarregel:** "kort in de nek" in de prompt gaf soms een fade of pompadour. Gebruik de haarregel uit `output/2026-10-08-luca-25/shots.py` (`ID_LINE`).
- **Stukken die het beeldmodel slecht tekent** (kies ze niet voor een hoofdrol of video):
  - de Sartoriale-broek: krijgt een gulp en een omslag;
  - het Imperial-jack: wordt een trainingsjack;
  - de Midnight-set: de twee lagen vloeien in elkaar over;
  - de Tabacco-set;
  - het navy Lounge-vest: krijgt steekzakken.
- **Stukken die het wel betrouwbaar tekent:** Onyx, Bellagio, de Lido- en Bergamo-polo's, de Signature-broek en de loafers.
- **Wit T-shirt:** een wit crew-neck T-shirt onder een jas is een eigen product (Puro Supima) en mag.
- **Video zonder hoofd:** het model zet de kin toch in beeld. Snijd het startbeeld bovenaan 160 tot 200 px bij, met 9:16 behouden, en de video zelf 150 px.
- **Bewegen in video:** geen grote hoofddraai, want het haar vervormt. Versmelten voorbijgangers op de achtergrond, knip de clip dan voor dat moment af.
- **Resolutie:** 2K is genoeg voor Instagram (1080 px breed) en kost de helft van 4K.

## Hoe het personage gebouwd is

1. De vier foto's van de eigenaar zijn klein (200–350 px breed). Ze zijn opgeschaald naar 4K, en daarna is gecontroleerd dat het gezicht niet veranderde. In `model.json` is `media_id` de import van het kleine origineel en `upscale_job_id` de 4K-versie.
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
