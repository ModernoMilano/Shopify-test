# 25 foto's en 5 video's met het vaste model (8 oktober 2026)

Opgeleverd als één zip: `ModernoMilano-Luca-25-fotos-5-videos.zip` (90 MB), met de mappen `Foto's` (25 JPEG's, q95) en `Video's` (5 mp4's, 9:16, zonder geluid).

| Bestand | Wat |
|---|---|
| `shots.py` | Alle shots (M = model, D = macro, A = sfeer, V = startbeeld video), de vaste identiteitsregel, correcties per ronde en de videobouwer voor Seedance 2.5 (`--video`, standaard als concept) |
| `fotos.tsv` | De 25 foto's in volgorde, met titel en eventuele bijsnede |
| `videos.tsv` | De 5 video's met hun bewerking (inkorten, bovenkant bijsnijden) |
| `bronnen.json` | Per id het Higgsfield-resultaat |
| `build_zip.py` | Bouwt de zip in de Higgsfield-sandbox |

## Hoe gemaakt

- **Model:** het element `modernomilano-model` (zie `brand/model.md`).
- **Foto's:** Nano Banana Pro, in batches van maximaal 12, met de echte productfoto's als referentie. Rondes 1 tot 3 zijn in 4K gemaakt. Daarna is overgestapt op 2K om binnen de credits te blijven; dat is ruim boven de 1080 px breedte van Instagram.
- **Video's:** Kling 3.0 pro, 5 seconden, vanaf een goedgekeurd 9:16-startbeeld. De eigenaar vond ze te duidelijk AI. Daarom gaan alle video's vanaf nu alleen met Seedance 2.5: eerst een concept in 480p, pas na de controle afmaken in 1080p (zie `brand/model.md`). `shots.py --video` bouwt die opdrachten al, met rustigere bewegingen.
- **Controle:** elk beeld en elke video is gecontroleerd door twee onafhankelijke controleurs. De ene keek naar kleding en regels, de andere naar echtheid en identiteit.
- **Kosten:** na de tweede ronde stond het saldo op 166 credits; na afloop is er 3,55 over.

## Eigen beslissingen (bewust goedgekeurd)

- **04 Aan het stuur op het Comomeer:** de polo is iets blauwer dan de productfoto van de Sorrento Ottanio. Eén controleur keurde af, de andere en de video met dezelfde polo keurden goed. Het is het startbeeld van video 1, bijgesneden tot 4:5.
- **13 Bij de oude auto:** startbeeld van video 2, tot 4:5 bijgesneden boven de voeten.
- **19 Espresso op het dak:** onderaan bijgesneden, zodat een broek die niet in de opdracht stond wegvalt.
- **24 Espresso in een café in Brera:** onder- en rechterkant bijgesneden. Daarmee vallen de broek en een donker bandje om de pols weg.
- **07 Brera op een grijze ochtend:** het gilet hangt open in plaats van half dicht. Dat is styling, geen productfout.
- **Video 1:** ingekort tot 3 seconden. Bij het omkijken daarna vervormt het haar.
- **Video 3:** bij de beige Morbido-hoodie is de rits onder het lipje niet zichtbaar en is het lipje zilver in plaats van donker. Dat was de derde poging; in een clip van 5 seconden valt het nauwelijks op.
- **Video 4 en 5:** de bovenste 150 px van elk beeld zijn weggesneden, zodat kin en mond buiten beeld blijven. Video 5 is daarnaast ingekort tot 3,5 seconden, omdat daarna twee voorbijgangers op de achtergrond in elkaar overlopen.

## Niet gelukt binnen de pogingen

Deze shots kwamen na drie pogingen nog steeds met fouten terug en zijn vervangen door andere beelden:

- M02 (Navigli, blauw uur);
- M03 (tegen de oude Spider);
- M08 (tram);
- M13 (avond in Brera);
- A06 (balkon);
- D03 (rits-macro).

De fouten per poging staan in `shots.py` als correctiezinnen.
