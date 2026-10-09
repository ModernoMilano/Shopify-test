# Reels op de focuscollecties (8 oktober 2026)

Het plan, de vier reels met kosten, staat in `PLAN.md`. Daarvan is reel 1 als proef gemaakt. De eigenaar koos die proef en de kleur Bordeaux & Crema.

## Reel 1: "One gilet. Two looks." (proef)

Opgeleverd als één zip: `ModernoMilano-Reverso-reel-proef.zip` (14 MB). Daarin zitten de reel (10,2 s, 1080×1920, 24 fps, H.264, zonder geluid) en `Cover.jpg`.

Link: https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/3abe9bed-d509-4ff1-9b9f-24841462f77f.zip

| Bestand | Wat |
|---|---|
| `reel1.py` | Opdrachten voor de stills (Nano Banana Pro) en voor Seedance 2.5 (concept en afmaken) |
| `reel1-edit.json` | De montage: bronnen, snedes en tekst |
| `montage.py` | Monteert in de Higgsfield-sandbox: harde snedes, schreefletter (Cormorant Garamond 600), geen korrel of LUT |

### Bronnen

| Id | Job | Controle |
|---|---|---|
| Startbeeld A, bordeaux buiten (A2) | `152dd083-0cc3-4090-8a01-32f57da326dc` | beide controles goed |
| Startbeeld B, crème buiten (bewerking van A2) | `c1eafea8-f9c7-452e-b730-bc21046660a3` | beide goed |
| Macro van de kraag (MAC2) | `3ebfcafa-ecd3-4ec6-b8ac-c227ff9c9f45` | beide goed (poging 2) |
| Clip A, concept 480p | `11f863d7-65bd-499f-bd33-e265c88d9afb` | beide goed |
| Clip A, 1080p | `ce33bccd-7116-42eb-adec-c37c04c07106` | beide goed |
| Clip B, concept 480p | `d2ced65d-f25f-4724-aa40-2b49829203db` | beide goed |
| Clip B, 1080p | `79e050f8-2f40-43a2-b79a-4395db8fba48` | beide goed |

Het detail in snede 4 is een uitsnede uit startbeeld B (4K). Er is geen extra beeld voor gemaakt.

### Wat niet lukte

- **Startbeeld A1:** een duidelijk andere man (ouder, haar bijna zwart). Afgekeurd, A2 gebruikt.
- **Macro, poging 1:** een ronde naad naast de rits en een platte zoom die het gilet niet heeft. De tweede poging toont alleen de kraag.
- **Flat-lay, drie pogingen:**
  - poging 1: het visgraatpatroon van de vloer liep onderin uit elkaar;
  - poging 2: een opgerolde tee las als een extra kledingstuk;
  - poging 3: het gilet was te breed, met een bronzen rits, en de broek had geen elastiek.

  De flat-lay is daarom uit de reel gelaten. Het beeldmodel legt dit gilet niet betrouwbaar plat neer; bij de volgende reels flat-lays van deze set vermijden of de productfoto's van de winkel gebruiken.

### Lessen voor de volgende reels

- **Voorcontrole van de Seedance-prompt:**
  - Beschrijf de beweging vanuit de pose die al in het startbeeld staat. Hier keek hij al ongeveer 50° opzij, dus "verder draaien" zou te veel worden.
  - Zet geen lijst in de prompt met wat niet mag: dat plant het juist.
  - Noem de kleur aan de buitenkant van een omkeerbaar stuk letterlijk.
- **Afmaken met `draft_job_id`** geeft hetzelfde beeld als het concept, in 1080p, HEVC en 24 fps. Monteer daarom op 24 fps.
- **Een tweede startbeeld als bewerking van het eerste** (dezelfde foto, met alleen het gilet omgekeerd) gaf exact dezelfde plek, pose en gezicht. Zo werkt de harde snede tussen de twee looks.

### Kosten

1000,55 credits voor de proef en 858,55 erna, dus **142 credits**:

- 22 voor 8 stills;
- 24 voor 2 concepten;
- 96 voor het afmaken van 2 clips in 1080p.

## Reel 2: "Total Bordeaux", één snede (opgeleverd)

Wens van de eigenaar (8 oktober), na de proefreel:
- de vele snedes zagen er slecht uit;
- dezelfde video, maar zonder tekst, met alleen het logo (`brand/assets/logo-moderno-milano.png`) klein in het midden in de laatste 2 seconden;
- de MILANO REVERSO SET TOTAL BORDEAUX;
- één snede naar de andere kant van de bodywarmer.

Budget afgesproken: maximaal ongeveer 180 credits.

- **Opzet:** `reel_tb.py`. Shot A (5 s) heeft de bordeaux kant buiten. Het laatste frame van A wordt, met alleen het gilet omgekeerd, het startbeeld van shot B (5 s). Zo valt de snede op de beweging en begint de video niet opnieuw.
- **Regel van de eigenaar voor de Reverso-gilets:** de binnenkleur is alleen te zien binnen in de kraag en langs de open voorkant, **niet bij de armsgaten**. Het moet toch duidelijk een bodywarmer blijven. Bij bordeaux op bordeaux lukt dat met diepe armsgaten binnen het schouderpunt: de schoudernaad en de mouw van de tee zijn zichtbaar, met een schaduwlijn en verschil in stof. Een crème bies of band bij de armen las als een streep op een jasje met korte mouwen; dat waren rondes 1 tot 3, die door de controle werden afgekeurd.
- **Startbeeld A:** ronde 4, Y0 (`66db5823-11ca-4cb1-a1dc-b23e82aff434`), door de eigenaar goedgekeurd ("perfect zo").

### Oplevering

Opgeleverd als één zip: `ModernoMilano-Reverso-Total-Bordeaux-reel.zip` (12 MB). Daarin zitten de video (10,0 s, 1080×1920, 24 fps, H.264, zonder geluid en zonder tekst) en `Cover.jpg`.

Link: https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/5c68bab9-108e-4cd5-b443-c470f604b8c4.zip

De montage staat in `reel_tb-edit.json`:
- shot A van 5 s;
- een harde snede;
- shot B van 5 s, 2,75% ingezoomd zodat hij op het laatste frame van A valt (gemeten met `align.py`);
- het logo op 40% van de breedte in het midden, de laatste 2 s, met 0,5 s opkomen en het beeld 18% donkerder.

| Id | Job | Controle |
|---|---|---|
| Startbeeld A (Y0, ronde 4) | `66db5823-11ca-4cb1-a1dc-b23e82aff434` | eigenaar en beide controles goed |
| Clip A, concept / 1080p | `e076b507-34eb-4c37-8f18-d366ece36e1c` / `e1dfe650-dd2a-4a7d-a644-d7409ecfb11b` | beide goed / beide goed |
| Laatste frame van A (upload) | `8d6bfe7a-d68c-4e8c-91cd-95557f4a2429` | |
| Startbeeld B (ronde 2) | `c6512078-30e2-4408-8f8e-810d80831bf5` | beide goed |
| Clip B, concept 2 / 1080p | `7fea5b6b-5611-4445-a48c-b5d4d1fec538` / `6caa5655-b860-4a8f-9916-d256c6094c18` | beide goed / beide goed |

### Wat niet lukte

- **Startbeeld A, rondes 1 tot 3:** het gilet las als een jasje met korte mouwen. Rondes 2 en 3 hadden ook crème bij de armen, wat de eigenaar daarna uitsloot.
- **Startbeeld B, ronde 1:** de tee zat hoger, waardoor de band van de broek zichtbaar was en het beeld bij de snede zou verspringen.
- **Clip B, concept 1:** het opende niet op het startbeeld (andere camerapositie, hoofd omhoog), en de camera "handheld met lichte deining" dreef de hele shot opzij, ook onder het logo.

### Lessen

- **Snede op de beweging:** begin B met het laatste frame van A en verander alleen wat moet veranderen. Noem in de prompt alles wat gelijk moet blijven, zoals de lengte van de tee.
- **Vaste camera:** voor een shot dat op een snede moet aansluiten, of waar een logo over komt, een "locked off tripod camera" vragen en de prompt laten beginnen met "The shot opens exactly on the start frame". Een handheld-camera laat Seedance afwijken van het startbeeld.
- **Rest bij de snede:** wat er dan nog verschilt (een paar procent schaal), meet `align.py` weg in de montage.
- **Logo:** het witte handschriftlogo is leesbaar op 40% van de breedte met een zachte schaduw en het beeld 18% donkerder, ook boven het crème gilet.

### Kosten

858,55 credits ervoor en 653,55 erna, dus **205 credits**, de afgesproken bovengrens:
- 40 voor 9 startbeelden in 4K;
- 45 voor 3 concepten;
- 120 voor het afmaken van 2 clips in 1080p.


## Serie "Una giornata": video 1, Il lago (MILANO NOBILE SET)

Het draaiboek staat in `VIDEOS4.md`, de opdrachten in `videos4.py` en de montage in `lago-edit.json`. Alle stappen staan ook in het dashboard [CREATIVE ENGINE](https://claude.ai/artifact/HaSkNEqUyTCC7Ta2uCgSR3).

**Opbouw (versie 2, na feedback van de eigenaar).** Versie 1 had twee shots. De eigenaar vond shot A te lang en wilde een snede naar een andere hoek, dichter op de kleding en de details van de boot, en het moest echt ogen. Versie 2 bestaat daarom uit drie shots, samen 9,75 s:
- shot A, 2,3 s, met een langzame inzoom van 2,5% in de montage;
- detail C, 2,5 s;
- shot B, 5 s, met het logo de laatste 2 s.

Opgeleverd als één zip, `ModernoMilano-Il-lago.zip` (8 MB), met de video (9,75 s, 1080×1920, 24 fps, H.264, zonder geluid) en `Cover.jpg` (een frame uit shot B op 6,0 s, vóór het logo).

Link: https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/6dce78de-e98b-41b8-87c0-de8f7cf23b0b.zip

De controle van versie 2 noemde twee kleine punten, geen van beide een afkeur:
- in shot C lijken een paar frames dubbel, wat rond 3,2 tot 3,5 s een heel lichte hapering kan geven;
- bij de eerste snede hangen de vingers aan het eind van A gestrekt en begint C met gekrulde vingers.

| Wat | Job of media | Controle |
|---|---|---|
| Startbeeld A (bijsnede van `afc686cd`, zonder het merkteken op de ruit) | media `304515f9-5388-4a7b-a8c2-5f06eb77a44d` | beide goed |
| Startbeeld B (bewerking van `afc686cd`) | `7292b98e-3543-489b-88e2-727ac10f9835` | beide goed |
| Startbeelden detail C, 2 varianten | `14882de2-e866-4817-8374-6f7570fb1dff` en `29448168-1a03-445c-b790-1f53665a2d78` | beide afgekeurd: keurmerk met nepletters op het glas |
| Startbeeld C (bijsnede van `14882de2`, zonder het keurmerk) | media `a3e5b43c-ef18-44a3-abfe-1c7adddeb7c8` | goed, gecontroleerd in het concept |
| Clip A, concept en 1080p | `cb6ea9b6-ce98-4a8d-8ab7-b713034c3a28` en `99e40dbb-52b0-423d-8fd6-f1167f2f5851` | beide goed |
| Clip B, concept 2 en 1080p | `5bc76890-1435-417b-86f6-c769b0a1d9eb` en `104510a3-7c38-4375-adae-32a0dc4a583d` | beide goed |
| Clip C, concept en 1080p | `33a562bb-5a19-4c0c-bf0e-dd17eed97833` en `08a46084-eef9-42f1-a945-e6fb858e609f` | beide goed (1080p in de eindvideo) |
| Montage versie 1 (8,96 s, A en B) | media `b0a52a2d-37b3-44f9-94c2-0b9daf77a757` | beide goed, vervangen na feedback |
| Montage versie 2 (9,75 s, A, C en B) | media `a181f217-ede0-4e07-812b-3c7b9a34ae7b` | beide goed |

### Wat niet lukte

- **Startbeelden boot, ronde 1:**
  - variant 1: het zwarte gilet op de zwarte polo las als een jasje met mouwen;
  - variant 2: het gezicht oogde ouder.
  Met een zin over de geribde armsgaten lukte het wel.
- **Merktekens op glas:** het beeldmodel zet keurmerken en nepletters op de voorruit, ook als de prompt dat verbiedt (bij A en bij beide detailbeelden). De oplossing was steeds een bijsnede, geen retouche.
- **Concept 1 van shot B:** "lowers his eyes" werd ogen dicht vanaf 2,3 s en een diepe buiging tot 4,3 s, onder het logo. In concept 2 bleven met "eyes open and steady on the horizon, head level" de ogen open en was hij stil.
- **Shot A:** de boot vaart nauwelijks. Seedance maakte er een levende foto van, met alleen het glinsterende water. Dat is geaccepteerd, met een inzoom in de montage.

### Lessen

- Vraag bij een slotshot nooit om de blik te laten zakken. Vraag om open ogen, een recht hoofd en stilstand vanaf seconde 3.
- Snijd bij een detail van een boot het glas weg, of laat het buiten beeld.
- Seedance maakt minimaal 4 s. Een clip direct in 720p kost 28 credits, tegen 60 voor een concept plus 1080p.

### Kosten

653,55 credits bij de start van de serie en 371,55 erna, dus **282 credits**:
- 64 voor alle startbeelden van de vier video's;
- 218 voor Il lago:
  - de startbeelden van detail C: 8;
  - de concepten: A 12, B 15 + 15, C 12 (samen 54);
  - 1080p: A 48, B 60, C 48 (samen 156).

## Morgen verder (stand 8 oktober 2026, 22:45 UTC)

- **Nog te maken:** Pioggia (Total Antracite), Giardino (Blu & Crema) en Sera (Dark Mocha). De startbeelden zijn goedgekeurd door de eigenaar, de prompts staan in `videos4.py` en zijn nagekeken.
- **Feedback van de eigenaar meenemen:** een kort eerste shot en een snede naar een dichtere hoek op de kleding.
  - Pioggia en Giardino: A, dan een close-up van de kraag met de binnenkant, dan B (gilet omgekeerd) met het logo.
  - Sera begint al met een detail.
- **Budget:** 371,55 credits.
  - Pioggia en Giardino in drie shots kosten elk ongeveer 156 credits (detail direct in 720p).
  - Sera kost ongeveer 120.
  - Samen is dat ongeveer 432, dus er is ongeveer 60 credits tekort, zonder reserve. Advies aan de eigenaar: ongeveer 100 credits bijkopen, anders stoppen vóór Sera.

## Haperen in de video's opgelost (9 oktober)

De eigenaar zag in de eerste twee video's (Total Bordeaux en Il lago) een "hele laggy slow motion lag".

**Gemeten oorzaak (Seedance 2.5 zelf, al in de concepten van 480p):**
- Elke 24 frames, dus elke seconde, verandert het beeld bijna twee keer zo veel als normaal. De helderheid springt dan ook even. Seedance maakt de clip in stukken van een seconde, en dit zijn de naden.
- Om de 4 frames pulseert het beeld licht.
- Soms zitten er bijna-dubbele frames in. Bij detail C van Il lago waren dat er twee per seconde.

De container is gewoon 24 fps zonder omzetting. Mijn montage veroorzaakte het dus niet. Seedance heeft geen instelling voor framesnelheid. Higgsfield kan wel opschalen naar 60 fps, maar dat haalt de naden en de dubbele frames niet weg.

**Oplossing, zonder credits: `smooth.py`, standaard aan in `montage.py`.** Het script doet drie dingen:
1. De beweging per stap meten met optische flow (DIS).
2. Die beweging gelijkmatig over de tijd verdelen. Elk frame op zijn nieuwe tijdstip komt uit het dichtstbijzijnde echte frame, dat met optische flow op volle grootte op zijn plek wordt geschoven (Lanczos; bicubisch hield 90%, Lanczos 96% van de scherpte in shot A van Total Bordeaux).
3. De helderheid gladmaken, met afronden in plaats van afkappen.

Wat eerst misging, gevonden door de controle:
- De tussenbeelden mengden twee frames. Daardoor waren ze zachter dan de echte frames, en de scherpte "ademde" eens per seconde.
- Elk frame werd gemiddeld met zijn buren. Dat kostte in shot A van Total Bordeaux de helft van het fijne detail: de rits werd een vage lijn en het haar oogde wasachtig.

Beide stappen zijn eruit. Nu blijft 96% (Total Bordeaux A, mediaan) tot 100% (Il lago) van de scherpte van het origineel over, zonder schokken en zonder dubbele frames.

Lengte, aantal frames en 24 fps blijven gelijk. De montages hoeven dus niet te veranderen.

**Resultaat:**
- Shot A van Total Bordeaux: alle 5 schokken weg.
- Shot A van Il lago: alle 9 schokken weg.
- Detail C van Il lago: van 19 schokken en 9 dubbele frames naar 1 schok en geen dubbele frames.
- Een tussenbeeld op 100% bekeken: geen vervorming.

**Lessen:**
- Maak elke Seedance-clip eerst glad voor de montage.
- Meet schokken op licht vervaagde beelden. Zonder die vervaging meet je vooral pixelruis van één grijswaarde.
- Meet ook de scherpte per frame tegen het origineel (variantie van de Laplaciaan). Gladmaken mag geen detail kosten.
- Ruim tijdelijke frames op: de schijf van de sandbox liep een keer vol.

## Serie "Una giornata": video 4, Sera (DARK MOCHA)

Wens van de eigenaar (8 oktober, 23:00): "het cashmere two tone pak in de stoel, echt focussen op macro detail shots, maak hem helemaal af".

**Idee: "de crème lijn".** De crème band en strepen leiden het oog van de hals via de knie naar de mouw. Pas dan zie je hem, in de fauteuil bij het raam. Daar verschijnt het logo, in het donkere raam waar hij naar kijkt.

**Montage (`sera-edit.json`, ongeveer 10 s):**
- C: de capuchonband aan de hals, 2,0 s;
- D: de strepen over de knie, 1,8 s;
- A: de mouwstrepen, manchet en hand, 2,0 s;
- B: in de fauteuil, 4,2 s, met het logo de laatste 2 s (36% breed, iets boven het midden).

Het capuchonmacro is 18% donkerder gezet (`"gain": 0.82`). De eindcontrole mat er een gemiddelde helderheid van 101, tegen 59 tot 72 in de andere shots, waardoor het licht bij de eerste snede zichtbaar wegviel. Dit trekt alleen de belichting gelijk; er is geen kleurlook of LUT toegevoegd.

| Wat | Job of media | Controle |
|---|---|---|
| C startbeeld, ronde 1 (`da4a661d`) | | afgekeurd: crème bies langs de hele rits, tandjes wisselen van vorm, band eindigt in een vlek |
| C startbeeld, ronde 2, variant 2 (`29e90014`), bijsnede | media `c186e81c-5dcb-4739-8802-3b93e1d83db7` | beide goed |
| D startbeeld, variant 1 | `5e091ce6-1aff-4b47-a8bf-0f9ae0e354b1` | beide goed (variant 2 afgekeurd: been over de armleuning) |
| A startbeeld (mouwdetail, 8 okt) | `98e8323c-ebb0-4e04-82cc-1d0391ab05e7` | beide goed |
| B startbeeld, bijsnede van `7782c3c1` | media `2bde7ce2-4273-4c4f-bbc0-b7c4f42a41a9` | beide goed |
| Concepten C, D, A, B | `e6411249`, `bac96939`, `872422e9`, `0510d7ff` | C, D en A goed; B zie hieronder |
| 1080p C, D, A, B | `71e5a8b9`, `b6dc1d62`, `592caa19`, `fb0f21ca` | in de eindcontrole |

**Toelichting bij B:** de echtheidscontrole keurde het concept af op herkenbaarheid. Volgens de controleur was zijn haar te goudblond en zijn gezicht smaller. Dat oordeel ging over 480p, met een gezicht van ongeveer 100 pixels breed. In 1080p is het duidelijk dezelfde man als in het startbeeld dat de eigenaar goedkeurde. Het goudbruine komt van de lamp. Daarom heb ik B afgemaakt en wordt herkenbaarheid in de eindcontrole nog een keer apart beoordeeld.

**Voorcontrole.** Drie reviewers keken de prompts na vóór de concepten:
- geen beweging van de vingers;
- de camera "a few centimetres" en "stays steady", niet "rakes across";
- bij B "eyes open and gaze level";
- de strepen van de broek benoemd volgens de productfoto.

Alle concepten slaagden in één keer.

**Kosten:** 275 credits:
- 20 voor 5 startbeelden in 4K (een zesde mislukte en werd teruggestort);
- 51 voor 4 concepten;
- 204 voor 1080p.

De uitsneden kostten niets.
