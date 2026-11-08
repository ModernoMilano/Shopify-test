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

**Werkelijke kosten versie 1** (saldo gemeten): rap ≈ 55 (6 delen van ≈ 60–75 s, waarvan 3 gebruikt), stijltests en preview
≈ 30, deel A ≈ 75, delen B en C samen 179 (31 keyframes à 1, 30 clips à 4,5–6). Totaal ≈ 340 credits; de raming was 500–550.
Alle clips Kling 3.0 std zonder geluid, 3 of 4 s; keyframes GPT Image 2.6 medium 2k met de karakterbladen als referentie.

**Bekende punten voor versie 2**

- De rapper struikelt op een paar plekken over de beat (te veel lettergrepen per maat); de eigenaar accepteert dat voor v1.
  Volgende tekst: hooguit ~10–11 lettergrepen per regel en kortere zinnen bij de dagtellers.
- Twee lasnaden in de song (~0:51 en ~1:41) waar de stem iets van kleur kan wisselen.
- Ondertitels breken nu niet meer over een punt of vraagteken heen (aangepast na deel A).
- De uitspraak "mo-DER-no mi-LA-no" is in deel B het mooist; in deel A klinkt de eerste keer korter.
