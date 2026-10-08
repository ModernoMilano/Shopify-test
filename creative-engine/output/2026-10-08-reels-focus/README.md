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

