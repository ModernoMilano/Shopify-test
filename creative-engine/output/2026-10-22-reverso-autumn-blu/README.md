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
