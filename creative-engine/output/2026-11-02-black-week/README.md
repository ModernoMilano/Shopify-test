# Black Week 2026: betaalde video's (geparkeerd op 2 nov, eerst foto's)

De eigenaar stuurde op 2 nov een complete brief voor 5 paid-social video's (Meta Reels/Stories, TikTok), elk met twee
hooks: V1 lijst-inschrijving (3–25 nov), V2 Black Week (20–26 nov), V3 Black Friday "The Big Stack" (27 nov),
V4 "The Milano Stack" (28–30 nov), V5 Winter Drop-teaser (29 nov–2 dec). Product: de Milano Cashmere Lounge Set
(beige, gray, black, navy; €150; alle vier actief in Shopify), wit T-shirt eronder, gratis crème wollen sokken als
Black Week-cadeau. Geen gezichten, alleen handen en silhouetten. Alle tekst, prijzen en logo's in de nabewerking.

Dezelfde dag, 18:50: "laat dat, we gaan later de video's doen, eerst focussen op foto's". Status: voorbereid, niet
gegenereerd, 0 credits uitgegeven.

## Wat klaarstaat

- `blackweek.py`: de shotlijst (17 clips + 1 stilstaand beeld) met start­beeld-prompts en bewegingsprompts, volgens de
  lessen van Reverso Autumn (één fysieke handeling per clip, handen beginnen geplaatst, camera bescheiden maar levend,
  parallax benoemen bij camerabeweging, geen filmwoorden). Handen: "exactly five fingers", kaal, geen sieraden.
  Vereenvoudigd waar de brief te veel handelingen in één shot vroeg (lint lostrekken + deksel + sokken + jasje).
- `bw_build.py`: de nabewerking: clips aaneen (24 → 25 fps door 4% sneller af te spelen, geen dubbele frames),
  tekst-overlays in Oswald Bold / Montserrat Medium (variabele fonts van Google Fonts), wit met zachte schaduw op
  donker, bruin #26201A op licht, goud #D6B680 voor data en urgentie, het officiële logo (wit/zwart PNG, transparant)
  met "TIMELESS. REFINED. YOU." eronder, prijsladders met gouden scheidingstekens, eindkaart op een vastgehouden
  frame of een stilstaand beeld, waarschuwing als iets buiten de veilige zone (22–78%) valt, lichte korrel, H.264
  crf 15, zonder geluid.
- `videos.json`: per video de montage: hook A/B (0–3 s), body (3–8 s), eindkaart (8–10,5 s) met alle teksten en
  prijzen letterlijk uit de brief, en de extra gouden regel voor hook B bij V3 en V4.
- Referenties op Higgsfield (media_import_url 2 nov): beige 209f2622…, gray 0d1b11da…, black 453f3b1b…,
  navy 7be3d17b… (in `data/higgsfield-media.json`). Logo's en fonts staan in de sandbox onder `~/tb/bw/`.

## Kosten (raming, 2 nov)

| Onderdeel | Credits |
|---|---|
| Startbeelden, 3 varianten per shot, 4K | 208 |
| 480p-concepten (10 hooks van 4 s, 7 body-clips van 5 s) | 228 |
| 1080p-eindversies | 1.216 |
| Basis | 1.652 |
| Met 40% herkansingen | ≈ 2.300 |

Per video 330 (V1, V2, V5) tot 450 (V3, V4). Saldo op 2 nov: 206 credits.

## Punten om met de eigenaar te beslissen voordat we beginnen

1. V5 hook A: de brief wil dat het deksel "vanzelf" een paar centimeter omhoog komt, maar verbiedt ook "lids opening
   by themselves". Voorstel: een hand tilt het deksel iets op (zo staat het nu in de prompt).
2. V5 body: twee silhouetten (hij en zij). De huisregel is één man per beeld; de brief vraagt het expliciet, dus de
   tweede figuur is een vrouw, puur silhouet, geen gezicht.
3. V5 hook B: de Galleria heeft winkelnamen; de prompt zet de winkels in het donker zonder borden, de controleur let erop.
4. Witte T-shirt en wollen sokken zijn geen eigen producten; de brief staat ze toe.
5. Seedance levert 1080p (geen 4K) en 24 fps; de montage speelt 4% sneller af naar 25 fps.
