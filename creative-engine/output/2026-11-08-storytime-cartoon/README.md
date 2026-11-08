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
