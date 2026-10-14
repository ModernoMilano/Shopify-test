# Sandbox-scripts van de merkfilm "You Won't See a Name" (12 oktober 2026)

Draaien in de Higgsfield-sandbox in `~/tw` (beelden in `img/`, oordelen in `verdicts.json` en `chosen.json`, frames van bestaande clips in `frames/`).

- `looks_defs.py` + `looks.py`: de zes oude-camerafilters als ffmpeg-ketens; `python3 looks.py stills|video|apply <look> <in> <out>`.
- `build.py`: bouwt het storyboard (`rows.py` + `storyboard.py`), het overzicht van alle varianten (`allsheet.py`), het contactblad (`contact.py`) en de zip.
- `verdicts.py` (in de scratchpad van de sessie): leest de journals van de keuringsrondes en schrijft `verdicts.json` en `chosen.json`; zonder goedgekeurde variant wordt de beste van de laatste ronde als VOORLOPIG gekozen.

De keten per filter wordt in de montage (`film.py`) na de belichting per shot op elk shot gelegd, ook op de bestaande clips.

## De montage (14 oktober 2026, "You Will Look Twice")

Alles draait in `~/tw` naast de scripts van 11 oktober (`film.py`, `montage.py`, `smooth.py`, `vochain.sh`); de stemmen staan in `~/film/vo`, de uitvoer in `~/film/out`.

- `split_read_v3.py <opname.mp3> <map>`: knipt één doorlopende opname van het hele script in de 24 zinnen (`L1_p.wav` … `L24_p.wav`), door de VO-keten; de whisper-woorden worden met difflib aan het script gekoppeld.
- `smooth_all.sh`: maakt alle clips glad naar `vid/s/` (1080p-versie waar die er is, anders de 480p-proefversie; `piano2` met `--raw-from=auto`, `seraB` blijft ruw).
- `build_edit_v3.py <stem> [look]`: bouwt `~/film/out/film-edit-<stem>[-look].json` uit `plan.json` en `vo_script.json`. Het beeld volgt de stem: een zin begint nooit eerder dan 0,3 s na de vorige, en de shots ertussen worden zo veel langer als hun bron toelaat, zodat elke zin op zijn eigen beeld valt. Schrijft ook `timing-<stem>[-look].json` (rijen, zinnen, kaarten).
- `mk_film3.py`: maakt `film3.py` uit `film.py`: dezelfde montage, met een optionele `look` (ffmpeg-keten uit `looks_defs.py`) over het hele beeld, aangebracht vóór de ondertitels en het logo.
- `make_film.sh`: wacht op het gladmaken en de stemmen en rendert Grady + Portra, Holden + Portra en Grady zonder filter.
- `filmqa.py <film> <timing.json> <tag>` en `ff.py <film> <t> [x y w h]`: controlebladen (per snede begin/midden/eind, alle kaarten, het slot, de stem-omhullende) en losse frames op 100% voor de controleurs.
