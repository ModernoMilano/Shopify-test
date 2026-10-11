# Merkfilm "Let the Day Do the Dressing" (11 oktober 2026)

## Wat de eigenaar vroeg

- "De ziekste ModernoMilano cinematic video": storytelling, met een diepe cinematic stem.
- Research bij de grote merken naar hoe zij zulke films maken.
- Alle credits die er nog zijn (70,55) gebruiken.
- Tijdens het werk kwamen er drie wensen bij:
  - "een Amerikaans-Engelse, diepe cinematic stem die echt goed is in storytelling";
  - "ik vind dit allemaal niks, gewoon een goeie diepe cinematic stem" (na de stemvoorbeelden van Higgsfield);
  - "zo lang mogelijk met de credits die je hebt, en met de beste kwaliteit".

## Research (workflow, 8 agents)

Zes onderzoekers keken elk vanuit één invalshoek: menswear-films, geurfilms, voice-over, Reels, montage en geluid, en storytelling. Daarna kwamen een factcheck en een brief. De volledige brief staat in de sessie; de kern:

- **Eén idee en één richting.** Zegna *Born in Oasi* gaat van de kamers van de villa naar het landschap.
- **Een wending.** The Impression vond Zegna SS26 "almost too resolved": mooi, maar zonder spanning.
- **Frame 1 beweegt al.** Geen logo vooraan en geen zwart beeld.
- **De stem gaat over het moment, nooit over het merk.** Het Apple-spotje "Designed by Apple in California" scoorde het laagst van 26 Apple-spots.
- **Kleding gedragen, niet getoond.** Twee of drie macro's laten de kwaliteit zien (Loro Piana: "everyday moments").
- **Geluid draagt het verhaal.** De "ASMR-esque" sound van Zegna *Summer in Oasi*.
- **Voice-over.**
  - Eerste persoon, kort, warm en dichtbij.
  - Geen omroeper- of trailerstem.
  - Pauzes worden mee geschreven.
  - Geen superlatieven, geen claims over herkomst of ambacht, geen call to action.
- **Ondertitels in beeld.** Eén frase per kaart, hooguit ongeveer 26 tekens, een verfijnde schreefletter, binnen de veilige zone (y 270-1250 px, x 65-960 px).
- **Mix.**
  - -14 tot -16 LUFS, true peak hooguit -1 dBTP.
  - Geen toonhoogte-drones of gestemde klappen, zodat er ruimte blijft voor de muziek uit de Instagram-bibliotheek.

Wat er bewust níet is overgenomen:
- **Een woordmerk vooraan (3-5 s).** De eigenaar wil het logo alleen aan het eind, klein en zonder effect.
- **"Light grain".** Er komt geen korrel en geen LUT (SKILL.md).
- **Een film van 38 s.** De eigenaar wil hem zo lang mogelijk: het is 48,2 s geworden, met al het goedgekeurde 1080p-materiaal dat in het verhaal past.

## Het verhaal

Eén dag, van een grijze regenochtend in Milaan tot het blauwe uur thuis.
- **De verteller** herinnert zich zijn vader: die had nooit een paraplu, en had één regel over kleding, "Let the day do the dressing."
- **Het misverstand:** als jongen dacht hij dat zijn vader de regen bedoelde. Jarenlang was hij "dressed for the evening by breakfast", altijd te vroeg.
- **De wending (29,8 s, 62% van de film):** de regel was toestemming. "To stop being early for my own life. On time."
- **Het eind:** "Moderno Milano." eenmaal gezegd, onder het logo.

Het script komt uit een panel (workflow, 7 agents). Drie schrijvers schreven elk een eigen versie: de regel van de vader, een innerlijke monoloog met een refrein, en "twee kanten" (het omkeerbare gilet). Drie beoordelaars gaven punten: copy chief, merkstrateeg en editor. Alle drie kozen "de regel van de vader" (48, 47 en 49 van de 60). Een finisher voerde hun verbeteringen per zin door.

| Tijd | Shot | Voice-over |
|---|---|---|
| 0,8 | Regen, arcade in Milaan | My father never owned an umbrella. |
| 4,3 | Villa, hand op de piano | He had one rule about clothes. |
| 7,0 | Villa, hij loopt naar het glas | Let the day do the dressing. |
| 9,5-12,3 | De zee komt in beeld | (geen stem) |
| 12,3 | Profiel aan het glas | I was eight. |
| 14,6 | Binnenplaats, bordeaux | I thought he meant the rain. |
| 19,2 | Binnenplaats, het gilet omgekeerd | Some afternoons want the other side of me. |
| 22,9 | Comomeer, de boot | For years, I was dressed for the evening by breakfast. |
| 29,8 | Comomeer, zijn gezicht | Turns out, his rule was permission. |
| 35,4 | Thuis, macro's | To stop being early for my own life. |
| 43,3 | Thuis, de fauteuil | On time. |
| 45,5 | Logo | Moderno Milano. |

62 woorden. Er wordt ongeveer 27 s gesproken; de rest is stilte en geluid, met ruimte voor muziek.

## Beeld (48,2 s, 11 shots, harde snedes)

| # | Tijd | Clip | Product |
|---|---|---|---|
| 1 | 0,0-3,9 | **Nieuw:** regen onder de arcade, Seedance 2.5 vanaf het goedgekeurde startbeeld van "Pioggia" (`6f98f485`). Concept `98a3d77b`, 1080p `70d1dfc8` | MILANO REVERSO SET TOTAL ANTRACITE |
| 2 | 3,9-13,9 | Il pianoforte v2 (de hele take van 10 s) | MILANO REVERSO SET ANTRACITE & PIETRA, MILANO SUEDE LOAFER - GRIGIO |
| 3-4 | 13,9-22,2 | Total Bordeaux A en B (het gilet omgekeerd; B ingekort tot 3,7 s) | MILANO REVERSO SET TOTAL BORDEAUX |
| 5-7 | 22,2-34,4 | Il lago A, het detail C en B | MILANO NOBILE SET |
| 8-11 | 34,4-48,2 | Sera C, D, A en B; het logo de laatste 3 s, in het raam (y 0,44) | MILANO KNITTED TWO-TONE CASHMERE SET - DARK MOCHA, PURO SUPIMA MERCER TEE - WHITE |

- Elke clip is eerst gladgemaakt met `smooth.py`: de schok die Seedance elke seconde geeft. Bij Il pianoforte en de regen bleven de echte frames aan het eind staan (`--raw-from=auto`). Sera B bleef ruw, zoals op 9 oktober.
- **Controle van het nieuwe regenconcept** (twee controleurs): goedgekeurd met notities.
  - Kleding, identiteit en architectuur zijn in orde.
  - Hij kijkt vanaf ongeveer 1,8 s verder omhoog dan "a little" (ongeveer 40°, binnen de grens van 45°). Op de eerste zin ("My father never owned an umbrella.") leest dat als herinneren.
  - Vallende regen is nauwelijks te zien, alleen de natte straat; de regen zit in het geluid.
  - Een tweede concept paste niet meer in het budget.
- Niet gebruikt:
  - Proefreel 1 (dezelfde binnenplaats en hetzelfde omkeren als Total Bordeaux: dubbel);
  - Il pianoforte v1 (het raam-probleem).

## De stem

- **Model:** ElevenLabs v4. Eleven v4 kost ongeveer 0,005 credit per teken, met een minimum van ongeveer 0,23 per opname.
- **Stem:** de preset "Gideon" (`1ad38ba4-9cc4-4f2f-9fde-b0fefdf67ae5`). Gekozen uit alle 43 mannenstemmen, op meting, omdat Claude niet kan luisteren:
  - **Toonhoogte** (Praat): Gideon is de diepste bruikbare stem, mediaan 82 Hz in ElevenLabs. Vlad (63 Hz) is een horrorstem.
  - **Accent** (CommonAccent-herkenner, SpeechBrain): "us" bovenaan (0,66). Alistair, Landon en Jasper scoorden "england" en vielen af.
  - **Expressie:** 12,9 halve tonen bereik. Dezelfde stem in Seed Audio had maar 4,9: vlak.
- **Opname:** elke zin apart, in twee versies: een gewone lezing (a) en een met een geschreven pauze (b). Per zin gekozen op tempo, een dalend einde en een woordelijk kloppende transcriptie (faster-whisper). "Moderno Milano" is nagemeten op zes lettergrepen; in het Italiaans transcribeert whisper het als "Moderno Milano". Niets is in tempo gerekt.
- **Keten** (`vochain.sh`, brief): high-pass op 70 Hz, iets warmte rond 110 Hz, -2 dB bij 300 Hz, presence op 3,8 kHz, de-esser en compressie 3:1. Stilte voor en na eraf.
- Elke zin staat op dezelfde luidheid (RMS -20 dBFS).

## Geluid (`film.py`, zelf gemaakt uit ruis en sinussen)

Higgsfield heeft geen muziek- of geluidsmodel voor gewoon gebruik. Elke laag is getoetst met een AudioSet-herkenner (AST, `MIT/ast-finetuned-audioset-10-10-0.4593`):

| Laag | Waar | Herkenning |
|---|---|---|
| Regen: duizenden losse druppels met belletjes | 0-4,1 s | Rain on surface 0,42, Rain 0,19, Raindrop 0,18 |
| Lucht binnen in de villa, en de zee eerst heel ver, dan bij het glas | 3,8-14,2 s | Ocean 0,26, Waves 0,25 |
| Lucht op de binnenplaats, met een paar verre vogels in de pauzes van de stem | 13,6-22,4 s | Chirp 0,71, Bird 0,53 |
| Water tegen de boot | 21,9-34,6 s | Waves 0,20 |
| Bijna stilte thuis | 34,2-48,2 s | (heel zacht) |
| Eén lage klap zonder toonhoogte onder het logo, 45-180 Hz | 45,2 s | |

- **Afgekeurd:**
  - de eerste regen, gewone gefilterde ruis: "Static";
  - een pianonoot: "Electronic tuner" en "Guitar";
  - een lage sinus-zwelling: een toon die met de muziek botst.
- **Mix:**
  - De lagen zakken 4 dB als de stem spreekt, de regen 7 dB.
  - Elke laag begint 0,3 s vóór zijn beeld (J-cut), en er is een doorlopende bodem: nergens digitale stilte.
  - Eindmix -14,0 LUFS (lineair genormaliseerd, eerst de zeldzame pieken begrensd), true peak -2,0 dBFS, LRA 6,6 LU.
  - Een whisper-transcriptie van de eindmix geeft elke zin woordelijk terug.

## Eindcontrole (workflow: beeld, geluid, verhaal en merk, en een rechter)

**Ronde 1: niet opleveren.** Vier punten moesten eerst opgelost worden; alle vier zijn opgelost zonder credits.

1. **Ondertitels onleesbaar op licht beeld:** contrast 1,5-1,8:1 op het crème gilet, de witte villa en het glinsterende meer. Opgelost met SemiBold 52 en vier donkere lagen onder de letters (`SHADOWS` in `film.py`); de rechter mat daarmee minstens ongeveer 4,5:1 op alle kaarten.
2. **Digitale stilte:** 4 s in vijf stukken. Er kwam lucht binnen in de villa en op de binnenplaats bij, en de zee hoor je al zacht vanaf de snede. `film.py` meldt nu elke stilte.
3. **Een mondklik** na "about clothes." (-22,6 dBFS). Die is geknipt, en elke zin heeft fades van 10 ms.
4. **Het crème shot stond aan het eind ruim 2 s bijna stil**, net na het sterkste moment. Het is 1,1 s korter gemaakt, en alles erna schoof op.

Ook meegenomen:
- de kaarten wisselen op de echte pauzes in de stem ("My father … never owned an umbrella.");
- "To stop being early" komt 2,7 s na "permission." (was 4,4 s), zodat de zin over de snede naar huis doorloopt;
- vogels, meer en regen zachter;
- de klap onder het logo hoorbaar op een telefoon;
- de loudness lineair (ffmpeg viel stil terug op dynamisch, en de lagen pompten in de pauzes);
- geen dubbele frames meer voor de snedes.

Bewust niet veranderd:
- **De voorbijgangers met paraplu ver weg in het regenshot.** Regel 7 staat 2 à 3 verre, wazige voorbijgangers toe, en retoucheren mag niet. Een paraplu juist onder "My father never owned an umbrella" werkt bovendien.
- **Het bordeaux gilet over een bordeaux tee.** Dat is de TOTAL BORDEAUX-set zoals hij verkocht wordt. Het omkeren maakt duidelijk dat het een bodywarmer is.
- **De roze zweem op de binnenplaats en het warme haar in het laatste shot.** Alleen een kleurcorrectie of een nieuwe clip helpt, en de regels staan alleen een belichtingsfactor toe. Voor een witbalans per kanaal is toestemming van de eigenaar nodig.

## Credits

| Wat | Credits |
|---|---|
| Stemtests (vier stemmen in ElevenLabs, één in Seed Audio) | 3,56 |
| Regenshot: concept 480p (4 s) | 12 |
| Regenshot: 1080p (4 s) | 48 |
| Voice-over: 11 zinnen + 6 tweede versies (2 zinnen opnieuw na een limiet) | 4,37 |
| **Totaal** | **67,93** van 70,55 (2,62 over) |

## Bestanden

- `film.py`: de montage: beeld via `montage.py`, ondertitels, geluidslagen, mix en loudness.
- `build_edit.py`: schrijft `film-edit.json` met de kaarten getimed op de woorden in de opname, en `film-edit-clean.json` zonder ondertitels.
- Oplevering: zie hieronder.
