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
