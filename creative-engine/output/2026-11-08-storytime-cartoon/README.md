# Story-time cartoon ad voor ModernoMilano (gestart 8 nov 2026)

De eigenaar wil de vorm van een Meta-advertentie van Penrose Skin nabouwen (Ad Library 1092227623428399): een 3D-cartoon in
Pixar-stijl, een ik-verteller die een verhaal vertelt, woord-voor-woord ondertitels, AI-muziek eronder, 3 min 26 s. Ons verhaal:
een meisje gaat weg bij haar vriend voor een man die ModernoMilano draagt en zijn leven op orde lijkt te hebben; grappig, met
zelfspot, inspelend op pijnpunten (geen moeite meer doen, onzichtbaar zijn) zonder haar of de kijker neer te halen.

Beslissingen van de eigenaar (8 nov): stem 2 = **Harrison** (Higgsfield preset 573e5163-59b3-4926-aab1-951ef2985f81, Seed Audio),
lengte **ongeveer 3 minuten**, **goedkoop**: cartoonkwaliteit is genoeg.

## Wat de analyse van het voorbeeld opleverde (workflow wf_4ca1b84b, stijl-lens)

- 99 shots in 206 s, gemiddeld 2,1 s; 55% close-ups van gezichten, 25% medium, 10% wide, 10% inserts (hand, telefoon, kalender).
- Camera vrijwel stil: trage push-in van 3–4%, nooit pannen; alle energie uit mimiek (wenkbrauwen, ogen) en de snelle montage.
- Kleurtaal: warm oranje = de held en het product, koud blauw = stiekem en verdrietig, zwart-wit = het dure middel dat faalt.
- Ondertitels: Montserrat Black-achtig, caps, wit met dunne zwarte outline en zachte schaduw, caphoogte 3% van de framehoogte,
  gecentreerd op 63,5% van de hoogte, 1–3 woorden per kaart, wisselend op het ritme van de stem (0,5–1 s), hard gesneden;
  hoofdstukwoorden ("DAY 9", de merknaam) 2x zo groot; één kaart in rood.
- Geen eindkaart: prijs, garantie en "link's below" als ondertitels over het verhaal, met de verteller die naar beneden wijst.
- Goedkope signalen die we vermijden: wisselende gezichten per shot, extra vingers, geseksualiseerde vrouwen, meme-captions zonder
  merk. Wij: vaste karakterreferenties, ons woordmerk op de slotkaart, dezelfde kleurtaal in onze merkkleuren (beige, crème, navy).

## Goedkoopste productie op Higgsfield (prijzen opgevraagd 8 nov)

| Onderdeel | Model | Prijs |
|---|---|---|
| Keyframes (stills) | GPT Image 2.6 (`gpt_image_2_6`), 9:16, quality low 1k | 0,25 credit per beeld |
| Keyframes beter | zelfde, quality medium/high 2k | zie tabel hieronder |
| Video uit een keyframe | Kling 3.0 `std`, sound off | 1,5 credit per seconde (7,5 per 5 s) |
| Alternatief video | Grok Video 1.5 480p 2,5/s · Seedance 2.5 480p 3/s, 720p 7/s, 1080p 16/s | |
| Vertelstem | Seed Audio, preset Harrison | ≈ 3 credits per minuut tekst |
| Muziek | ElevenLabs Music v2.5, instrumentaal, eigen prompt | ≈ 13 credits per 90 s (≈ 26 voor 3 min) |
| Ondertitels, montage, mix | eigen script in de sandbox (bw_build.py-familie) | 0 |

Raming voor een film van 180 s, volledig geanimeerd: ~45 clips van 4–5 s met Kling std ≈ 300 credits (+30% herkansingen ≈ 390),
stijlmaster + karakterbladen + 45 keyframes in 2–3 varianten ≈ 40–80 credits, stem ≈ 9, muziek ≈ 26. **Totaal ≈ 500–550 credits.**
Saldo 8 nov: 206 (min ~8 voor de stemtest). Advies: bijkopen tot ~600.

Higgsfield heeft ook een kant-en-klare "Cartoon story"-pijplijn (Ads Studio micro drama, /microdrama-ads) die bij 480p 3 credits
per seconde rekent (≈ 540 voor 180 s plus referenties): duurder dan Kling std met eigen montage, maar met ingebouwde
scriptregels en controles. Eerste keus: eigen pijplijn met Kling std; terugval: micro drama.

## Pijplijn

1. Script (Engels, ~450 woorden voor 180 s bij ~150 wpm) volgens de beats van het voorbeeld: hook (3 s), pijn, de ander, inzicht,
   ontdekking, test met dagtellers, social proof, obstakel, payoff, reveal van merk en prijs, aanbieding, CTA.
2. Stem: Harrison inspreken per alinea (batch), duur per zin meten, woordtijden verdelen voor de ondertitels.
3. Stijlmaster + karakterbladen (verteller, de ModernoMilano-man = cartoonversie van ons vaste model, zij, huisgenoot, barista,
   collega) met GPT Image 2.6; daarna elk keyframe met die bladen als referentie.
4. Kling 3.0 std per keyframe (camera stil, trage push-in, mimiek), 4–5 s, ondertitels later eroverheen.
5. Muziek: ElevenLabs Music, instrumentaal, warm en speels met een stapje omhoog bij de payoff; ducking onder de stem.
6. Montage op de stem (gemiddeld 2–2,5 s per shot), captions Montserrat Black-stijl in onze typografie, slotkaart met woordmerk,
   prijs en aanbieding als overlay; controle door onafhankelijke controleurs (gezichten consistent, vingers, geen tekst in beeld,
   geen merknamen van anderen, geen seksualisering).

## Regels en risico's

- Zij is eerlijk, niet de schurk; de verteller lacht om zichzelf; geen uitspraken over het lichaam of het karakter van de kijker
  (Meta: geen personal attributes, geen negatief zelfbeeld als argument).
- De tweede man (de ModernoMilano-man) is de cartoonversie van het vaste model; de verteller is een andere cartoonman. Dat is
  een bewuste uitzondering op de één-man-regel, door de eigenaar gevraagd voor dit format.
- Geen echte merknamen of producten van anderen in beeld (het voorbeeld toont Creed en Baccarat; wij niet).
- Licentie van ElevenLabs-muziek via Higgsfield voor betaalde advertenties nog zwart-op-wit controleren.
- De stem van het voorbeeld wordt niet gekloond (iemands stem zonder toestemming); Harrison is de dichtstbijzijnde preset op
  toonhoogte (~167 Hz tegen ~174 Hz) en tempo.

## Kostenraming hele video (180 s, 51 shots), prijzen opgevraagd 8 nov

| Onderdeel | Rekening | Credits |
|---|---|---|
| Keyframes: 51 shots + 6 extra karakterbladen, ~50% herkansing, GPT Image 2.6 medium 2k à 1 | ~85 beelden | 85 |
| Video: 51 clips Kling 3.0 std (1,5 per seconde; 3 s = 4,5; 5 s = 7,5), ~190 s | 285 | |
| Herkansingen video (~30%) | 85 | 370 |
| Vertelstem Harrison, ~3.000 tekens in 2–3 delen (10,5 per ~1.550 tekens) | | 21 |
| Muziek 180 s, ElevenLabs Music v2.5 instrumentaal | | 26 |
| Ondertitels, montage, mix (eigen script) | | 0 |
| **Totaal** | | **≈ 500**, met marge **550** |

Goedkoper kan door de keyframes op quality low 1k (0,25) te maken (−60) of minder shots (elke shot ≈ 6 credits all-in).
Duurder: Seedance 480p i.p.v. Kling verdubbelt de video (≈ 570 i.p.v. 285); 1080p-eindversies zijn voor dit format niet nodig
(het voorbeeld zelf is 720p). Tot nu toe uitgegeven aan tests: ~16 credits (7 stemmen, 3 beelden, 1 Kling-clip).

## Versie 1 gemaakt (8 nov, avond)

De eigenaar koos voor de rap als kern ("het is de hele ai gemaakte rap die het filmpje zo goed maakt"). Versie 1 is daarom
gebouwd op song v2 (162,4 s, drie ElevenLabs-delen aan elkaar, zie `rap_v3_lyrics.txt`), met 47 shots cartoon als bijbeeld
en de songtekst woord voor woord in beeld. Bestanden: `tools/assemble2.py` (montage + ondertitels), `tools/plan_full_v1.json`
(alle shots op de seconde), job-ids in `jobs.json` (`video_partA_8nov`, `video_partB_8nov`, `video_partC_8nov`).

**Shotlijst** (globale seconden in de song)

| Deel | Shots | Wat |
|---|---|---|
| A 0–51 | 1–16 | hoodie op de bank, lijstje, zij "you used to make an effort", verjaardag moeder, pasta, de ander voor het eerst gezien (MODERNO MILANO-kaart), hij kijkt naar zichzelf, zij lacht met de ander |
| B 51–101 | 17–30 | te groot pak op het werk, de baas, influencer-look met kettingen, de zus, DAY ONE in de regen, de ander weer bij de koffiebar, hij vraagt het hem, de ander legt uit, telefoon met de Duomo, kast met twee sets, bestellen op de laptop, kettingen in de la |
| C 101–162 | 31–47 | DAY ONE met de vuilniszak en Dave, DAY FOUR barista, DAY NINE collega, DAY TWELVE joggingbroek in de bak, wegwandelen, DAY SIXTEEN het berichtje, telefoon omgekeerd en sleutels, dak met Duomo recht in de camera, rits-close-up zonder logo, gevouwen set, drie dozen navy/grijs/beige met wollen sokken, de zus knikt, close-up, wijst omlaag, beide mannen in de Galleria, eindkaart met woordmerk, MAKE AN EFFORT. en Black Week-aanbieding |

**Werkelijke kosten versie 1** (uit de transactielijst van Higgsfield, 20:08–21:40 op 8 nov)

| Onderdeel | Credits |
|---|---|
| Stemtests (Seed Audio) en preview-muziek | 5 |
| Stijltest en preview: 4 keyframes, 4 Kling-clips | 25 |
| Rap, ElevenLabs Music v2.5: netto 6 bruikbare delen à 9–11 | ≈ 60 |
| Rap, dubbel betaald: `batch_size: 3` rekent drie keer af en geeft één bestand (eerste vier rondes) | ≈ 85 |
| Keyframes GPT Image 2.6 medium 2k, 45 stuks (incl. K48) | 45 |
| Kling 3.0 std clips, 47 stuks (3 s = 4,5; 4 s = 6; 5 s = 7,5) | ≈ 232 |
| **Totaal versie 1 + 1b** | **≈ 450** |

De mislukte lange rapdelen (14,54 per stuk) zijn door Higgsfield teruggeboekt. Zonder de dubbele batch-afrekening was het
≈ 365 geweest. In dezelfde uren liepen er ook spends van Nano Banana 2.1 en Outpaint (≈ 150) die niet bij deze video horen.

**Wat een volgende video kost** (zelfde stijl en karakterbladen, geen nieuwe tests)

| Variant | Credits |
|---|---|
| Nieuwe songtekst op dezelfde beelden (3 delen, 1 take per deel; herkansing +10 per deel) | 30–60 |
| Nieuwe hook (eerste 10 s): 3 keyframes + 3 clips | ≈ 20 |
| Los shot vervangen (keyframe + clip) | 6–7 |
| Hele nieuwe video van 160 s: 47 keyframes (+ ~5 herkansing), 46 clips, nieuwe song | ≈ 330–360 |

Alle clips Kling 3.0 std zonder geluid, 3 of 4 s; keyframes GPT Image 2.6 medium 2k met de karakterbladen als referentie.

**Bekende punten voor versie 2**

- De rapper struikelt op een paar plekken over de beat (te veel lettergrepen per maat); de eigenaar accepteert dat voor v1.
  Volgende tekst: hooguit ~10–11 lettergrepen per regel en kortere zinnen bij de dagtellers.
- Twee lasnaden in de song (~0:51 en ~1:41) waar de stem iets van kleur kan wisselen.
- Ondertitels breken nu niet meer over een punt of vraagteken heen (aangepast na deel A).
- De uitspraak "mo-DER-no mi-LA-no" is in deel B het mooist; in deel A klinkt de eerste keer korter.

**Controle door twee onafhankelijke controleurs (workflow wf_0a39dba0, 157 + 60 frames bekeken)**

- Beeld: geen tekst of logo's in de gegenereerde beelden, geen extra of versmolten vingers, kleding klopt in elk navy-shot.
  Eén echt punt: in shot 31 (vuilniszak) verandert de navy trui vanaf 103,7 s in een wit overhemd; opgelost door de clip op
  103,5 s te bevriezen. Kleine punten voor later: de verteller is in shot 24 wat off-model (bredere kop, bruine ogen), de
  ogen van de vriendin zijn in shot 16 blauw in plaats van bruin, de mist onder de wijzende hand in shot 45 oogt vreemd.
- Ondertitels: 30 van de 30 gecontroleerde woorden stonden op het juiste moment in beeld; alle zes MODERNO MILANO-momenten en
  alle DAY-kaarten groot. Eén echt punt: "fifteen off, three sets twenty" flitste in 0,3 s voorbij door samengeperste
  woordtijden uit de uitlijning; opgelost met `tools/retime_words.py` (korte woorden opnieuw verdeeld) en een samenvoegpas
  voor kaarten korter dan 0,2 s in `assemble2.py`.

**Versie 1b** (zelfde avond, op verzoek van de eigenaar): de Black Week-aanbieding is van de eindkaart af. Het slot is nu een
nieuw beeld, de verteller in de navy set op de piazza bij avondlicht (keyframe K48, clip C48, 5 s, laatste beeld vastgehouden
tot het einde) met alleen het woordmerk en MAKE AN EFFORT. als overlay (`tools/plan_full_v1b.json`). De regel over Black Week
in de songtekst zelf (136–141 s, "it's Black Week, boys: two sets fifteen off...") staat er nog in; die kan pas in een
volgende songversie weg.

**Download versie 1b** (de versie om te gebruiken; zip: mp4 1080x1920 crf 20, 98 MB; de song als mp3; de tekst per deel):
https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/ac0e5a70-fcf7-430c-9a5c-3788ec6735b7.zip
(media-id ac0e5a70-fcf7-430c-9a5c-3788ec6735b7; master crf 17 in de sandbox: ~/tb/rapvid/full_v1b.mp4.)

**Download versie 1** (eerste versie, met de Black Week-eindkaart; zip: mp4 crf 20, 97 MB; song; tekst; eindkaart als png):
https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/94c6f7e7-230f-4e84-a2f7-1271cc329b5d.zip
(media-id 94c6f7e7-230f-4e84-a2f7-1271cc329b5d; de master op crf 17, 151 MB, staat in de sandbox als ~/tb/rapvid/full.mp4.)

## Duet (versie 2 van het liedje): "hij rapt, zij zingt", 8–9 nov

De eigenaar wil een versie met een beter verhaal (zij komt terug), van twee kanten: R&B, hij rapt, zij zingt met een mooie stem,
later met nieuwe beelden en meerdere outfits. Eerst alleen het liedje. Zie `duet_v1_lyrics.md` (eerste tekst + hook-toernooi),
`duet_v3_lyrics.txt` (take 3), `duet_v4_lyrics.md` (take 4), `duet_v5_lyrics.md` (gepolijst, nog niet gegenereerd) en `jobs.json`
(`duet_8nov`). Geleerd over ElevenLabs Music v2.5 voor duetten:

- Delen van ~60 s met ≤ 90 woorden (rap + refrein) of ≤ 125 woorden (alleen rap) blijven compleet; bij 150+ woorden per deel
  laat de zangeres regels weg en gaat de rapper rennen. De rapper doet één regel per maat (≈ 2,8 s bij 88 BPM): 9–10 lettergrepen
  per regel klinkt ontspannen, 13+ struikelt.
- Elk deel krijgt toch een intro van ~10 s; die knippen we weg (join.py snijdt 0,4 s voor het eerste woord).
- Stemtoewijzing is niet altijd correct: tag elke sectie met de stem ("[Chorus: female vocal]") en zet in de stijlprompt dat de
  man zwijgt tijdens haar secties; het slot als aparte mini-secties (zijn regel / haar regels / duet). Controleer met de
  transcriptie (faster-whisper) welke regels ontbreken; toonhoogtemeting is onbetrouwbaar door de A-mineur-akkoorden op 110/220 Hz.
- Kosten: ≈ 8,7 credits per deel van 60 s; een complete song in 3 delen ≈ 26 credits per take. Tot nu toe ≈ 114 credits aan het
  duet (proef, 2 takes van 2 delen, 2 takes van 3 delen, 1 herkansing van deel A).

## Duet-video versie 1 (9 nov, nacht)

Liedje: take 5 ("Make an Effort", tekst v5, twee ElevenLabs-delen met één naad op 1:08, gladgestreken met `join2.py`:
knippen op de maat, omgekeerde swell van het volgende deel onder het vorige, korte crossfade). 142,5 s.
Video: 43 shots, elke tekstregel een passend beeld (`tools/plan_duet_v1.json`). 26 shots hergebruikt uit versie 1,
17 nieuw: zij zingt in close-up, zij eenzaam naast hem op de bank, zij aan haar raam, de volle bank ("lost and found"),
Thomas in de oatmeal knit bij het winkelraam (twee shots), zij ziet hem door het raam (haar kant, haar close-up, hij loopt door),
zij fatsoeneert haar jas in de spiegeling, zij aan zijn deur, hij doet open, de hoodie met verf aan de haak, zij stapt binnen,
samen met de voorhoofden tegen elkaar, het stel in de Galleria (hij in taupe cashmere cardigan) met de eindoverlay.
Kosten: 17 keyframes (17) + 14 clips (≈ 75) ≈ 92 credits. Job-ids in `jobs.json` onder `video_duet_9nov`.

**Download duet-video v1** (zip: mp4 1080x1920 crf 20, 85 MB; het liedje als mp3; de tekst):
https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/dab21e98-b7c5-4a40-9eb4-e30ef1296831.zip

**Controle duet-video v1** (twee controleurs, workflow wf_de85ded5): tekst-bij-beeld 36 van 41 regels sterk, 5 zwak, 0 mis;
beeld: 60 frames, anatomie en kleding per verhaalfase in orde, geen tekst of logo's in de gegenereerde beelden. Eén echt punt:
de eindtekst viel over de gezichten van het stel. **Versie 1b**: eindtekst onderin met een zachte donkere band, de "man met een
plan" krijgt een eigen shot (de ander met een planner op het terras, N141), "takeaway binned" toont nu afhaalbakjes in een
vuilniszak (N142), en haar regel "I hope you did it for you" gebruikt een jas-shot (N122) zodat haar kleding in de brug klopt.

**Download duet-video v1b** (de versie om te gebruiken; zip: mp4 1080x1920 crf 20, 86 MB; het liedje als mp3; de tekst):
https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/15a7b67a-d8dc-4687-9870-f3310074bd49.zip

## Take 6 en duet-video v2 (9 nov)

De eigenaar over take 5 in de video: "hij brabbelt, rare pauzes, er missen stukken, de teksten kloppen niet echt." Eerlijk:
mijn controle liep via de transcriptie en die is te mild voor verstaanbaarheid en pauzes; ik kan het geluid zelf niet horen.
Aanpak take 6: tekst v6 (`duet_v6_lyrics.txt`) in volledige, simpele zinnen met een duidelijke verhaallijn in plaats van
telegramstijl, 84 BPM met de opdracht "storyteller, every word articulated, no instrumental breaks", twee delen met één naad.
Nieuwe gereedschappen in de sandbox: `linecheck.py` (per regel het aandeel letterlijk herkende woorden; alles 80–100%, alleen de
merknaam wordt door de transcriptie als "Moderna-no Milano" geschreven) en `tighten.py` (knipt instrumentale gaten > 1,6 s op de
maat weg; hier één gat van 1,4 s na regel 2). Deel 1 begon zonder intro. Duet-video v2 = dezelfde shots opnieuw getimed op de
nieuwe regels (`tools/plan_duet_v2.json`), 0 extra credits.

**Download duet-video v2** (take 6 van het liedje, 2:12; zip: mp4 1080x1920 crf 20, 84 MB; het liedje als mp3; de tekst):
https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/3e76cd26-301b-4128-b95d-0208f6a96a3d.zip

## Video 2, verhaal 3: liedje take 1 (9 november)

Nieuw verhaal (door de eigenaar bepaald): hij is verliefd, zij wijst hem af omdat hij onverzorgd is, hij gaat werken aan kleding en verzorging, zij wil hem nu wel, maar alle meisjes lopen achter hem aan en hij kiest een ander. Duet met twee kanten: hij rapt zijn gedachten, zij zingt de hare na elk couplet.

- Tekst: `story3_v1_lyrics.txt` (4 delen, volle zinnen, 9 tot 12 lettergrepen per rapregel, merknaam 2 keer: de onthulling aan de bar en de slotregel).
- Stem: andere man dan in de duet-video (diepe, schorre bariton), 90 BPM, F mineur, Wurlitzer en gedempte trompet.
- Delen X1 tot X4 (ElevenLabs, elk met intro die eraf is geknipt), samengevoegd met join2 (beat-uitgelijnde knippen, swell, 0,35 s crossfade) en tighten (1 knip van 1,33 s). Lengte 2:42 (162,2 s).
- Controle op transcriptie: alle 46 regels aanwezig. Zwakste regel: "But a no is a no, and you knew" (33 procent herkend, waarschijnlijk gemompeld). "Moderno Milano" op het eind werd gehoord als "More than on Milano". Ik kan het geluid niet horen; de oren van de eigenaar beslissen.
- Bestand: media 5b23b659-d1f1-4cf5-8566-ea6fb822b28b (zie `jobs.json`, `video2_story3_9nov.song_joined_take1`).
- Kosten take 1: ongeveer 33 credits (4 delen van 50 tot 62 s).
- Beelden volgen pas na goedkeuring van het liedje, volgens `story3_shotplan.md` (46 shots, alles bewegende clips, geen stilstaande frames, ongeveer 280 credits).

## Video 2, verhaal 3: liedje take 2 (duet) en beelden (9 november)

Eigenaar over take 1: opening te zwak, meer duetgevoel, beginnen met beide stemmen. Tekst v2 via een workflow (4 schrijvers, 3 beoordelaars, synthese, 2 controleurs): hook "Careful what you ask a man to be" door beide stemmen, daarna om en om (zij zingt, hij rapt), hook komt terug na couplet 2 en aan het slot; barscène als vraag en antwoord; merknaam 2 keer. Tekst: `story3_v2_lyrics.txt`.

- Liedje take 2: delen Y1 tot Y4 (70/58/62/58 s, ongeveer 36 credits), samengevoegd tot 3:23 (media bf95551e). Alle 60 regels aanwezig op transcriptie.
- Lessen: (1) de VAD-onsetfix zat bij Y2 fout (13,9 s in plaats van 10,2 s) en bij Y4 0,8 s te laat: nu altijd controleren met whisper op een uitgeknipt stuk rond het begin (`chain.py --onsetat`, `--firstfix`); (2) ElevenLabs herhaalde bij een te lange duur (70 s) het laatste couplet: weggeknipt op de maat met `cutpart.py`; (3) `chain.py` doet nu de hele keten in een keer.
- Beelden: shotlijst met prompts in `tools/shots_v2.py` (59 shots, een per regel, plus K34b en K60 zodat geen shot hoeft te bevriezen). 66 keyframes (1 cr elk) incl. karakterblad van het andere meisje (W_OTHER). Retakes: K21 (mannen verwisseld), K27 (tweeluik), K46 (taart in beeld), K19 (vlek op de kappersdoek), K33 (achtergrondman in donker), K49 (spiegelbeeld als reuzengezicht). Twee onafhankelijke controleurs (workflow) bevestigden K33 en K49.
- Clips: Kling 3.0 std, 3/4/5 s, cliplengte altijd >= shotlengte. Blok 1 (shots 1 tot 17, 65 s) = 97,5 credits. Hele video ongeveer 224 clipseconden = 336 credits; met liedje en keyframes ongeveer 440 credits in totaal (de eerdere schatting van 280 was voor 46 shots en een liedje van 2:40).
- Ondertitels: `assemble2.py` koppelt nu geen woorden meer over een regelgrens (vlag `line_start` in de woordtijdlijn) en maakt alleen een grote DAG-kaart bij het woord DAY zelf (niet bij "days"). Grote kaarten: DAY ONE/TWO/THREE/TEN/FIFTEEN/TWENTY en MODERNO MILANO (2 keer).

## Video 2, verhaal 3: tekst v3 en de definitieve video (10 november)

De eigenaar: "wat is jouw verhaal in dit liedje, niet wat ik vroeg". Analyse: v2 week op drie punten af (de man koos het meisje dat lachte voordat ze keek in plaats van gewoon omdat alle meiden hem nu willen; "alle meiden" was één regel; de hook "Careful what you ask a man to be" was een waarschuwing). Tekst v3 (`story3_v3_lyrics.txt`) volgt het verhaal letterlijk: opening met beide stemmen ("Look at us now", zij: "I said no to him once", hij: "She said no to me once"), zij wijst hem af om zijn verzorging, hij werkt aan kleding en verzorging, zij wil hem heel graag ("I want him, I want him now"), iedereen wil hem ("Girls I've never met are asking where I shop", merknaam hier), zij vraagt een nieuwe kans, hij zegt vriendelijk nee omdat hij nu kan kiezen ("Now I get to choose, so I don't run again"), zij is verdrietig, slot met beide stemmen en Moderno Milano. Twee controleurs (workflow) toetsten de tekst aan het letterlijke verzoek; drie restanten van v2 verwijderd.

- Liedje take 3: Z1 (opening met beide stemmen; de tweede hook voor couplet 1 werd niet gezongen en is uit de tekst gehaald), Z2, Z3, Z4d (haar antwoord in twee regels, na drie pogingen waarin de korte regel steeds werd overgeslagen of door de man gezongen). 192,4 s (3:12), 61 regels, media a22b1000. Kosten liedje incl. retakes ongeveer 50 credits.
- Credits: saldo was op (0,95) en de automatische bijvulling stond op "betaling mislukt"; eigenaar kocht 500 credits.
- Beelden: alle 66 keyframes van v2 hergebruikt plus K25b (hij stapt naar buiten in de navy set) en K38b (twee meisjes op een terras vragen waar hij koopt). Regel-naar-keyframe in `~/tb/rapvid/plan_v3.py` (SEQ); lange gezongen regels gesplitst over twee keyframes (11, 12, 13) of afgekapt op 5 s (15, 32). 14 clips van blok 1 hergebruikt, 51 nieuwe clips (184 s, ongeveer 276 credits), elk gecontroleerd op begin/midden/eindframe.
- Les: Kling-clips nooit korter dan het shot; shots langer dan 5 s splitsen over twee beelden in plaats van een frame te bevriezen.

## Video 2, verhaal 3: oplevering (10 november)

- **Clipcontrole**: alle 51 nieuwe clips op begin-, midden- en eindframe bekeken (zelf plus twee onafhankelijke controleurs via een workflow). Twee clips afgekeurd en opnieuw gemaakt (12 credits): K06 (op de bank verscheen een los stuk pizza) en K05_2 (zijn gezicht dreef in de spiegel weg). Geaccepteerd met kleine schoonheidsfoutjes: K53 (korte witte veeg boven de kathedraal), K14_2 (wazig stuk pizza op de voorgrond), K47 (een extra man bij het sjouwen), K19r (de handen van de kapper verdwijnen even), K35 en K38b (hij loopt uit beeld).
- **Ondertitelfout gevonden en hersteld**: `chain.py` zet de vlag `line_start` niet in de woordtijdlijn, waardoor `assemble2.py` in de eerste render 17 woordparen over een regelgrens heen maakte ("GATE OLD", "BEARD SHE", "NOW I" op de wissel van zijn stem naar de hare). De vlaggen zijn achteraf gezet (61 van 61 regels), "three-day" is weer één woord, en de video is opnieuw gerenderd: 249 kaarten, 2 grote (MODERNO MILANO bij 123 s en bij 187 s), 0 paren over een regelgrens. Les: na elke nieuwe tijdlijn eerst `tools/v3/`-controle draaien (aantal gevlagde woorden = aantal regels) voordat de render start.
- **Eindcontrole op de video**: (controle door twee onafhankelijke controleurs loopt; uitkomst volgt hieronder)
- **Bestanden**: `tools/plan_v3.py` (regel-naar-keyframe), `tools/assemble2.py` (render met ondertitels), `tools/frames2s.py` (controlestroken om de 2 s), `tools/v3/` (tijdlijnen, montageplan, clipverzoeken, keyframe-ids, eindoverlay, liedje-scripts en de vier gezongen delen).
- **Kosten v3 in totaal**: liedje take 3 met retakes ≈ 50, keyframes 2, clips 51 × ≈ 5,4 ≈ 276, clip-retakes 12: ≈ 340 credits. Saldo na afloop: 172 credits (Plus-abonnement).
- **Eerlijk**: ik kan het geluid niet horen; de controle van het liedje (alle 61 regels, aansluiting van de vier delen) liep via transcriptie en de tijdlijn. De tweede hook voor couplet 1 werd door ElevenLabs niet gezongen en is uit de tekst gehaald. De oren van de eigenaar beslissen.

**Download video 2, verhaal 3** (zip: mp4 1080x1920 crf 20; het liedje als mp3; de tekst):
(volgt na de controle)
