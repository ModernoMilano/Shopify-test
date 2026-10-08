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

## Reel 2: "Total Bordeaux", één snede (in de maak)

Wens van de eigenaar (8 oktober), na de proefreel:
- de vele snedes zagen er slecht uit;
- dezelfde video, maar zonder tekst, met alleen het logo (`brand/assets/logo-moderno-milano.png`) klein in het midden in de laatste 2 seconden;
- de MILANO REVERSO SET TOTAL BORDEAUX;
- één snede naar de andere kant van de bodywarmer.

Budget afgesproken: maximaal ongeveer 180 credits.

- **Opzet:** `reel_tb.py`. Shot A (5 s) heeft de bordeaux kant buiten. Het laatste frame van A wordt, met alleen het gilet omgekeerd, het startbeeld van shot B (5 s). Zo valt de snede op de beweging en begint de video niet opnieuw.
- **Regel van de eigenaar voor de Reverso-gilets:** de binnenkleur is alleen te zien binnen in de kraag en langs de open voorkant, **niet bij de armsgaten**. Het moet toch duidelijk een bodywarmer blijven. Bij bordeaux op bordeaux lukt dat met diepe armsgaten binnen het schouderpunt: de schoudernaad en de mouw van de tee zijn zichtbaar, met een schaduwlijn en verschil in stof. Een crème bies of band bij de armen las als een streep op een jasje met korte mouwen; dat waren rondes 1 tot 3, die door de controle werden afgekeurd.
- **Startbeeld A:** ronde 4, Y0 (`66db5823-11ca-4cb1-a1dc-b23e82aff434`), door de eigenaar goedgekeurd ("perfect zo").
