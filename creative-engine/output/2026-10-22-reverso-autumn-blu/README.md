# Reverso Autumn (Total Blu) · cinematic video, 22 oktober 2026

Scenario 2 "Het eerste koude licht", gekozen door de eigenaar ("2 wil ik maar wel echt met de beste seedance").
Set: MILANO REVERSO AUTUMN SET – TOTAL BLU · QUARTER ZIP (gid://shopify/Product/11263352963409): omkeerbaar gilet navy/crème,
Mezza Zip navy, broek navy. Model: het vaste model. Navigli, ochtendmist, 13 s, 9:16. Eindkaart: woordmerk met daaronder
REVERSO AUTUMN (endcard.py). Beste Seedance op Higgsfield op 22 okt: `seedance_2_5` (models_explore; Seedance 2.0 heeft wel
4k maar is het oudere model), dus 1080p, `bitrate_mode: high`, eerst 480p-concept, dan 1080p via `draft_job_id`.

| Shot | Wat | Duur |
|---|---|---|
| S1 | levende still: macro ribkraag + rits met druppels, gezicht boven beeld | 2,5 s |
| V1 | video: hij trekt de rits van het gilet dicht tot de hals, kijkt het water over (navy buiten) | 4 s |
| S2 | levende still: het gilet over de reling, crème buiten, één blad | 2,5 s |
| V2 | video: van achteren het licht in langs het kanaal, gilet crème buiten; logo + REVERSO AUTUMN laatste 2 s | 4 s |

## Bestanden

- `autumn_blu.py` — prompts en requests (beelden, concept, 1080p). Productfoto-ids staan in `creative-engine/data/higgsfield-media.json`.
- `jobs.json` — alle job-ids. `endcard.py` + `endcard.png` — de eindkaart. `reverso_autumn-edit.json` — de montage (montage.py uit 2026-10-08-reels-focus).

## Stappen

| Stap | Resultaat |
|---|---|
| Startbeelden ronde 1 (8 × 4K, 32 credits) | S1a/S1b, V1a/V1b, S2a/S2b, V2a/V2b |
| Eigen blik | V1a/V1b: wit T-shirt onder de trui (niet van ons) → afgekeurd. V2a/V2b: ten voeten uit met schoenen, geen loafers in de look → afgekeurd. S1: lippen in beeld → wordt bijgesneden (bovenste 12%). |
| Ronde 2 (4 × 4K, 16 credits) | V1c (rits trui dicht), V1d (rits half open, blote hals), V2c/V2d (tot onder de knie, geen voeten) |
| Controle (workflow, 2 lenzen per shot) | zie hieronder |

### Controle startbeelden (workflow wf_d3641878, 8 controleurs, 22 okt)

| Shot | Kleding-lens | Echtheid-lens | Keuze |
|---|---|---|---|
| S1 | S1a nee (ritstanden navy i.p.v. zilver, kin blijft in beeld); S1b ja | beide ja, S1b schoner | **S1b**, bijgesneden tot macro [0.20, 0.115, 0.80, 0.7103] |
| S2 | S2a nee (zwevende ritsschuiver binnenin de kraag); S2b ja | S2a nee (zelfde schuiver); S2b ja | **S2b** |
| V1 | V1c nee (crème bies langs armsgat en zoom); V1d ja | V1c nee (dichte stoppels, ander gezicht); V1d ja, zelfde man, gezicht 650 px | **V1d** (hand aan de rits van de trui) |
| V2 | V2c nee (kraag navy aan de buitenkant); V2d ja | beide ja | **V2d** |

Kleine punten die blijven: zoomtrekker van het gilet in V1d koper/rosé i.p.v. zilver; vier verre voorbijgangers in V1d; de zoom van het gilet
oogt niet duidelijk elastisch; in V2d een smalle navy ribband van de trui onder het gilet.

### Concepten 480p (workflow wf_3946eb9d, 4 controleurs)

| Clip | Kleding-lens | Echtheid-lens | Besluit |
|---|---|---|---|
| V1 (job 221b8703…, start V1d) | ja: rits van de trui gaat dicht 0–1,75 s, hand zakt, gilet navy buiten, polsen bloot, geen tekst | ja: zelfde man op 0/2/3,9 s, vingers in orde, vaste camera | **1080p** job a4327f99… |
| V2 (job 3eb31d6a…, start V2d) | ja, mits bijgesneden: een sneaker komt onderin in beeld vanaf ~2 s, hoogste punt y = 0,925 | ja, zelfde opmerking (0,93); man wordt ~10% kleiner, water bijna stil | **1080p** job d0da38aa…, montage snijdt de onderste 13% weg |

Les: een volgshot houdt de voeten niet buiten beeld zodra hij een hiel optilt. Volgende keer het startbeeld tot halverwege de kuit
kaderen, of de camera laten meelopen én iets omhoog kantelen.

## Montage

`python3 montage.py reverso_autumn-edit.json reverso_autumn.mp4` (montage.py en smooth.py uit `2026-10-08-reels-focus`, Cormorant Garamond
in `f/cormorant.ttf`, de eindkaart als `src/LOGO.png`). 1080×1920, 24 fps, 312 frames = 13,0 s, zonder geluid (muziek bij het plaatsen).
S1 2,5 s (macro-uitsnede, zoom 1,00→1,04) · V1 4 s · S2 2,5 s (zoom 1,00→1,03) · V2 4 s (onderste 13% weg) · eindkaart over de laatste 2 s
(breedte 0,40, dim 0,26). Beide clips door smooth.py.

## Kosten

| Post | Credits |
|---|---|
| 12 startbeelden 4K (8 + 4) | 48 |
| 2 concepten 480p, 4 s | 24 |
| 2 × 1080p, 4 s, bitrate high | 128 |
| **Totaal** | **200** (saldo 333,25 → 133,25) |

### Controle montage (workflow wf_25d1353e, 2 controleurs)

Beide lenzen keuren goed: snedes exact op 2,5 / 6,5 / 9,0 s zonder dubbele of zwarte frames, geen randen, stills bewegen, eindkaart
gecentreerd en leesbaar ("REVERSO AUTUMN"), geen schoen in V2, geen mond of kin in S1, polsen bloot, geen T-shirt, zelfde man op
2,6 / 4,5 / 6,4 s. Verwerkt in de oplevering: S2 was donkerder dan V1 en V2 (luma 113 tegen 140 en 154) → gain 1,18 (luma 131);
de eindkaart maakte het gilet te grijs → dim 0,22; S1 toonde bovenin nog een reep hals → bovenrand van de uitsnede naar 15%.
Blijft (uit de bronclips): de zoomtrekker van het gilet is in V1 koper/rosé en in S1/S2 zilver; de rits van de trui is overal zilver.

## Oplevering (22 okt, 21:42)

**Zip (video + Cover.jpg):** https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/adc7d3b4-57ad-4e36-be1d-6f0a7bcd359e.zip
(media adc7d3b4…; Reverso Autumn.mp4 1080×1920, 24 fps, 13,0 s, zonder geluid; Cover.jpg = frame op 4,5 s).
De eigenaar vroeg om een bestand; deze cloudomgeving mag de Higgsfield-hosts (d2ol7oe51mr4n9.cloudfront.net, d8j0ntlcm91z4.cloudfront.net)
niet benaderen (netwerkbeleid van de omgeving, 403 op CONNECT), dus de video kon niet als bijlage worden gestuurd; de link is de weg.
