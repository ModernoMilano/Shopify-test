# Reel "Autumn Set Antracite & Pietra" (22 oktober 2026)

Wens van de eigenaar: precies de video van Total Bordeaux (8 oktober), maar met de **MILANO REVERSO AUTUMN SET – ANTRACITE & PIETRA · QUARTER ZIP** (https://modernomilano.com/products/milano-reverso-autumn-set-antracite-pietra-quarter-zip), met het vaste model.

Opzet (zoals `2026-10-08-reels-focus/reel_tb.py`): shot A van 5 s, het gilet antraciet buiten over de lichtgrijze Mezza Zip; één snede op de beweging; shot B van 5 s vanaf het laatste frame van A met het gilet omgekeerd (pietra buiten); geen tekst, geen geluid, het woordmerk de laatste 2 s. Startbeeld A is "dezelfde foto" als het goedgekeurde startbeeld van Total Bordeaux (Y0, `66db5823-11ca-4cb1-a1dc-b23e82aff434`), alleen de kleding verschilt. Opdrachten: `reel_ap.py`.

Productfoto's op Higgsfield (`data/higgsfield-media.json`): flatlay `7fc22639-b017-4f6c-98be-cfc86c97617e`, macro `ea50c54f-0f1a-483d-8587-fada31aaf697`, front `8762fe28-b46e-4e0b-a7e0-da2f25367718`, back `74d2f154-841b-470b-af28-dd10e26e0ea5`, reversed `f568e105-1876-45f9-bd2f-0933f215bc1a`.

## Kosten (gemeten 22 okt)

4K-startbeeld 4 · 480p-concept van 5 s 15 · 1080p-clip van 5 s **80** (was 60 op 8 oktober). Begroting bij één ronde per stap: 2 startbeelden A (8) + startbeeld B (4) + 2 concepten (30) + 2 clips 1080p (160) = **202 credits**. Tegoed bij de start: 176,25; na de 1080p-versie van A en het concept van B 46,25; de eigenaar heeft daarna bijgekocht (413,25 op 22 okt, 19:05).

## Stappen

| Stap | Job | Controle |
|---|---|---|
| Startbeeld A, 2 varianten | `873252fa-c538-4e3d-84ec-fe37dde62b53` (A0), `3a8b6c84-05e1-46da-8a52-72db6846afab` (A1) | beide goed bij beide controleurs (8,5 en 8); **A0 gekozen** (schonere huid, helderder oog, leesbaarder laagopbouw aan de zoom). Opmerking: lichte magenta zweem t.o.v. het bordeaux-beeld, een kleurgradatie, geen scènefout. |
| Clip A, concept 480p | `18c28230-bf76-4834-8544-e97004c6931a` | beide goed (9 en 7,5): dezelfde man in elk frame, kleding blijft gelijk, geen pietra bij armsgaten of zoom; beweging zoals gevraagd (kin en blik omhoog naar links, hoofddraai ~30-35°). Minor: de camera drijft in de laatste halve seconde nog ~1,7% naar rechts en stopt op de snede; in de montage opvangen (laatste frames uitlopen of B met dezelfde drift laten beginnen); frame 119 als basis voor startbeeld B. |
| Clip A, 1080p | `9976dc4f-958c-4a35-846e-80cc4f3ba531` | 1080x1920, 121 frames |
| Frame 119 van A (upload, basis voor startbeeld B) | `a8ca88f4-7c57-4d02-82fb-daf53b65321f` | |
| Startbeeld B, 2 varianten | `e9cffc12-c473-4e7d-94e5-13b117276f6d` (B0), `7e2ebd1d-98ec-422f-88a0-9b2401c471b1` (B1) | beide goed bij beide controleurs; **B0 gekozen** (9 en 9; B1 heeft onderaan de rits twee lopers op elkaar). Pixel-geregistreerd op frame 119 van A (hoofd, handen, zuil, achtergrond 0 px verschil), pietra buiten, antraciet alleen in de kraag en langs de voorranden, armsgaten en zoom pietra. |
| Clip B, concept 480p | `b3c9b024-f67f-41c4-8ff6-3c2d6724c410` | beide goed (9 en 8): opent op het startbeeld (zelfde houding, blik, handen), camera echt stil (max 0,04 px), kin en blik zakken 0,5-2,5 s, rust vanaf 3,1 s, laatste 2 s stil; gilet blijft pietra buiten. Minor: kader 3% wijder dan A (montage), vijf enkele stilstaande frames (onzichtbaar op 24 fps; gladmaken). |
| Clip B, 1080p | `76df01c4-5715-48e1-a863-121c9af82cc1` | 1080x1920, 121 frames |

Uitlijning (align.py, concept van B op frame 119 van A): B opent 6% wijder; crop [0.0021, 0.0106, 0.9455, 0.954]. Op de 1080p-versie gaf align.py (randen over het hele beeld) 5,75% wijder, maar dat was fout: het lichtere pietra-gilet misleidt de meting (eindcontrole 22 okt: handen en broek versprongen 41-51 px op de snede). Met SIFT op het beeld zonder het gilet: schaal 0,992. Gebruikte crops: A [0.0287, 0.0044, 1.0, 0.9757], B [0.0024, 0.0003, 0.9656, 0.9635]; rest op de snede hoofd 3 px, bogen 6 px, zuil 11 px (parallax). Daarbovenop een push-in van 3% over A ("zoom" 1,0 naar 1,03) en B constant op 1,03, zodat de snede blijft kloppen en A iets dichterbij komt, zoals bij Total Bordeaux.

## Montage

`reel_ap-edit.json` met `montage.py` (2026-10-08-reels-focus), in de sandbox in `~/tb/mont`: shot A 5,0 s (gladgemaakt met smooth.py), harde snede, shot B 5,0 s (gladgemaakt; A en B elk met een eigen uitsnede zodat het eerste frame van B op het laatste frame van A valt, zie hierboven), het woordmerk op 40% van de breedte in het midden de laatste 2 s, 0,5 s opkomen, beeld 18% donkerder. Uitvoer 1080x1920, 24 fps, 240 frames, 10,0 s, zonder geluid en zonder tekst. Cover: frame uit shot B op 6,0 s.

## Oplevering

Eén zip, `ModernoMilano-Reverso-Autumn-Set-reel.zip` (9,9 MB): de video (10,0 s, 1080x1920, 24 fps, H.264, zonder geluid en zonder tekst) en `Cover.jpg`.

Link: https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/6cc4429b-6172-47a0-afa3-6cb7f026dc6d.zip

Eindcontrole van de montage: EINDCONTROLE
