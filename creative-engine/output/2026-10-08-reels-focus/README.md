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
