# You Will Look Twice · de film (14 oktober 2026)

Eén film, twee stemmen, en een versie zonder filter om te vergelijken. Beeld 1080x1920, 24 fps, geluid op -14 LUFS (Instagram). Muziek komt er bij het posten bij uit de Instagram-bibliotheek; de film is gemaakt om daar zacht onder te liggen.

## Links

- **Grady, Portra 400** (mijn voorkeur, 67,2 s): https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/d071667d-7b84-4a50-8791-4b3b11a32e8a.mp4
- **Holden, Portra 400** (de tweede stem, 65,1 s): https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/d9a0dc91-f88c-494a-a319-5f2135e6e27c.mp4
- **Grady zonder filter** (ter vergelijking, 67,2 s): https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/901e1edf-7c7c-4dfd-9adc-bfaa2b739d92.mp4

## Wat je ziet

- **Acht shots zijn nog de 480p-proefversies**, opgeschaald naar 1080p: V01 (Galleria van achteren), V03 (de lat), V04 (het paneel), V05 (het meetlint), V06 (de naald), V08 (het gilet op tafel), V10 (de kraag) en V11 (de naad). Ze zijn zachter dan de rest; de beweging is wel de goedgekeurde. De 1080p-versie kost 64 credits per shot: 8 × 64 = 512. Het tegoed staat op 23,37 (de vijf 1080p-versies van H01, H02, H03, V02 en V12 en de twee stemopnames zijn ervan betaald). **Koop ongeveer 520 credits bij**, dan maak ik de acht af en bouw ik de film opnieuw; de montage en de stem blijven precies zo.
- **Het beeld volgt de stem.** De opname van Grady is langzamer dan het plan (24 zinnen, 52 s spraak). Een zin begint daarom nooit eerder dan 0,3 s na de vorige, en de shots ertussen zijn zo veel langer geworden als hun bron toeliet (H01 +0,35 s, H03 +0,26, V08 +0,81, V10 +0,55, en kleine stappen elders). Een kaart die volgens het plan op een eigen beeld hoort ("until the seam" op de naad, "it was new." op de knie, "of the atelier." op de stapel) begint nooit voor dat beeld. Daardoor duurt de film 67,2 s (plan 65,2) met Grady en 65,1 s met Holden.
- **Portra 400** ligt over het hele beeld, ook over de bestaande clips, onder de letters en het woordmerk (die blijven schoon). Cinestill was mijn tweede keus; zeg het als je die wilt zien.
- **Slot.** Het woordmerk komt klein in het midden op de fauteuil bij het raam; het beeld gaat in 1,8 s naar zwart, de naam wordt één keer gezegd, de film eindigt op het woordmerk op zwart.
- **Geluid.** Geen muziek. Per scène een zachte bodem: lucht en steen in de Galleria (met één stap bij het eerste beeld), de droge kamer van het atelier, zee achter het glas van de villa, water op het meer (met een lage motor op de boot), regen op het raam thuis, vogels op de binnenplaats, bijna stilte op het label; één lage klap onder het woordmerk. De lagen zakken 4 dB als de stem spreekt (2 dB bij de regen).

## Controle

CONTROLE

## Hoe het gemaakt is

Alles in de Higgsfield-sandbox, zonder credits: `sandbox/split_read_v3.py` (de opname in 24 zinnen), `sandbox/smooth_all.sh` (elke clip glad), `sandbox/build_edit_v3.py` (de montage-opzet uit `plan.json` en `vo_script.json`), `sandbox/film3.py` via `mk_film3.py` (de montage met de filter onder de tekst), `sandbox/filmqa.py` (de controlebladen). Zie `sandbox/README.md`.
