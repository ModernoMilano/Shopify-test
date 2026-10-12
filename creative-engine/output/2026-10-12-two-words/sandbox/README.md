# Sandbox-scripts van de merkfilm "You Won't See a Name" (12 oktober 2026)

Draaien in de Higgsfield-sandbox in `~/tw` (beelden in `img/`, oordelen in `verdicts.json` en `chosen.json`, frames van bestaande clips in `frames/`).

- `looks_defs.py` + `looks.py`: de zes oude-camerafilters als ffmpeg-ketens; `python3 looks.py stills|video|apply <look> <in> <out>`.
- `build.py`: bouwt het storyboard (`rows.py` + `storyboard.py`), het overzicht van alle varianten (`allsheet.py`), het contactblad (`contact.py`) en de zip.
- `verdicts.py` (in de scratchpad van de sessie): leest de journals van de keuringsrondes en schrijft `verdicts.json` en `chosen.json`; zonder goedgekeurde variant wordt de beste van de laatste ronde als VOORLOPIG gekozen.

De keten per filter wordt in de montage (`film.py`) na de belichting per shot op elk shot gelegd, ook op de bestaande clips.
