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

# Versie 2 (23 oktober 2026) · na de afkeuring

De eigenaar: "echt heel slecht, veel te AI, vooral als hij uitblaast"; de rits-beweging klopt niet; aan het einde wegloper met het gilet
omgedraaid; in plaats van het uitademen een vertraagde beweging; het gilet niet over een reling maar over een stoel bij een Italiaans
koffietentje. Drie onafhankelijke kijkers (workflow wf_2f43d4aa: regisseur, VFX, Instagram-kijker) plusten de oude film uit;
hun synthese staat in de workflow-journal. Kern: geacteerde "beats" in de prompt (rits, hand laat los, uitademen), een loopband in V2
(camera op rails, hij wordt kleiner), dode camera en bevroren achtergrond, stills met Ken-Burns-zoom, logo op zijn rug.

## Nieuwe opzet (autumn_blu_v2.py)

| Shot | Wat | Startbeeld | Concept | 1080p |
|---|---|---|---|---|
| N1 | slow motion macro: hand trekt de rits van de trui dicht, gezicht buiten beeld | N1c (9748571a…) na N1a (T-shirt) en N1b (onderlaag, glitterdruppels) | fbf13fa3… | cd8fa2a5… |
| N2 | slow motion aan het kanaal: hand glijdt langs de voorrand van het gilet, blik op het water | N2b (92672912…); N2a had een wit T-shirt | take 1 4904ef4a… (take 2 acc6a60b…: hand in zijzak + blik omhoog, afgevallen: hoofd draait naar de camera) | 976efc0d… |
| N3 | café: gilet crème over een bistrostoel, espresso, ober ver weg | N3d (fd307777…); N3a/b toonden ook trui en broek, N3c zoom zonder elastiek | ad0b418d… | a4df108a… |
| N4 | de wegloper: van achteren, loafers navy (zonder sokken) zodat voeten mogen, camera loopt mee | N4a (1948422a…); N4b had sneakers | 72c62539… (5 s) | zie hieronder |

Controle concepten (wf_8a90b1a9, 2 lenzen): N1, N2, N3 goedgekeurd (AI-gevoel 2 / 3 / 2). N2 blijft "een levende foto" (haar en lichaam
stil); take 2 had meer leven maar draaide het hoofd naar de camera, de controleur koos take 1. Wegloper (wf_e19489ef): geen loopband
meer, de kasseien schuiven onder het kader, de man blijft even groot, de muur links komt in beeld; camera te glad voor "handheld".
Loafer-productfoto geïmporteerd als 85b7e720… (higgsfield-media.json).

## Montage en oplevering versie 2 (23 okt, 00:17)

`reverso_autumn_v2-edit.json`: N1 0,4–3,5 · N2 0,6–3,9 · N3 1,2–3,6 · N4 1,0–4,4 (12,2 s, 293 frames), snijden op beweging, kop en
staart van elke clip eraf. Eindkaart in navy (endcard_navy.png, zelfde vorm als endcard.png) rechtsonder over het mistwater, zonder
dim: crème op de mist was onleesbaar en de eerste plaatsing viel over zijn rug (montage-lens, wf_d72f48c5). De regels-lens keurde
de montage goed (AI-gevoel 2): geen T-shirt, polsen bloot, geen tekst, gilet navy in N1/N2 en crème in N3/N4, loafers zonder sokken,
één man, mond dicht, zelfde man, vijf vingers, de wereld schuift langs in de wegloper.

**Zip (video + Cover.jpg):** https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/c812644e-8522-4476-b94a-8784b2984c0f.zip
(media c812644e…). Het 480p-voorbeeld van de concepten: media 6ca33050… (niet gebruiken).

Wat blijft (uit de bronclips, niet te monteren): N2 is nog steeds een rustige slow-motion pose (één bewegende hand, stil haar);
het gezicht is glad op 100%. De camera in N4 loopt te glad voor "handheld". De zoomtrekker van de trui verandert in N1 licht van vorm.

## Kosten versie 2

| Post | Credits |
|---|---|
| 12 startbeelden 4K | 48 |
| 5 concepten 480p (N1, N2 take 1, N2 take 2, N3, N4 5 s) | 63 |
| 4 × 1080p (N1, N2, N3 4 s; N4 5 s) | 272 |
| **Totaal versie 2** | **383** (saldo na afloop 476,25; de eigenaar kocht tussendoor bij) |

## Correctie 23 okt: de wegloper met het gilet navy buiten

De eigenaar: "de laatste scène is niet goed, de bodywarmer is niet in de navy kleur, alleen in de kraag, de hele bodywarmer moet blauw".
Dus "weer andersom" betekende: aan het einde navy buiten, crème alleen in de kraag. Startbeelden N4c/N4d (70d2f3de…, b34fd38a…)
met FRONT + BACK + loafer als referentie. Take 1 (190fb00e…, start N4c) werd door de echtheid-lens afgekeurd als halve loopband
(stenen schuiven, huizen stil, passen van 10-20 cm, standvoet glijdt). Take 2 met expliciet meereizende camera en lange passen,
twee concepten: D (6b5126f9…, start N4d, muur links) en C (13e0eaed…, start N4c). Kleding-lens koos D; echtheid-lens keurde D af
(korte passen, teen glijdt, gimbal-zweef) en C goed (voet vast op de stenen, pas-synchrone bob, AI-gevoel 2,5). C naar 1080p:
347adfeb…. Montage `reverso_autumn_v2-edit.json`: N4 1,2–4,6 s, navy woordmerk rechts over het water (x 0,80, y 0,62, 0,32 breed).
Extra kosten: 8 + 15 + 30 + 80 = 133 credits.

**Montagecontrole en oplevering (23 okt, 11:40).** Montage v2d (N1 0,4–3,5 · N2 0,6–3,9 · N3 1,2–3,6 · N4 1,2–4,6; 12,2 s) door
twee controleurs (wf_1e6e5b89): beide goedgekeurd, AI-gevoel 2 van 5. Gemeten: cuts op 3,08 / 6,38 / 8,79 s, geen bevroren of dubbele
frames, gilet navy over de hele rug en zijkanten in elk N4-frame, crème alleen binnen in de kraag bij de nek, loafers zonder sokken,
geen accessoires, geen tekst behalve de eindkaart, mond dicht, zelfde man. Enige punt: aan het eind kwam zijn broekspijp tot 1–2 px van
de M van het woordmerk. Daarom v2e: N4 1,2–4,3 s (0,3 s korter, 11,9 s totaal) en de kaart 0,30 breed op x 0,81; per frame nagemeten:
minstens 43 px tussen been en woordmerk, rechtermarge 44 px. Kleine punten die blijven: N2 is een rustige slow-motion pose, N3 is bijna
stil (stoom, ober, lichte camerabeweging), de crème kraagband bij de nek leest op afstand als een sjaaltje, de zolen flitsen donkerbruin
bij het afzetten, en de rechter iconenkolom van Instagram kan over het einde van "Milano" vallen.

**Zip (video + Cover.jpg):** https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/8a6e08eb-0372-4487-be06-0080072a8ab0.zip
(media 8a6e08eb…). De eerdere zip c812644e… (wegloper met crème buiten) vervalt.

## Derde ronde 23 okt: de kraag moet ook navy

De eigenaar: "de kraag in het laatste beeld dat hij wegloopt is beige terwijl die gewoon blauw moet zijn". Mijn N4-prompt vroeg zelf om
"cream showing only as the inner side of the stand collar at the nape"; dat was de fout. Nieuw shot `N4n` in `autumn_blu_v2.py`:
rits dicht, kraag rechtop, "one unbroken deep navy from the top of the collar to the hem", de productfoto van de rug (BACK) als
referentie #1 en een eigen SET-regel ("zipped up with the stand collar standing, the inner colour is completely hidden").
Vier startbeelden N4n-a..d (16 credits): c geweigerd door het nsfw-filter (vals alarm); a, b en d hebben de kraag navy rondom,
maar b en d kregen een witte rubberzool onder de loafer (het product heeft een donkere zool); a heeft donkere zolen en de handen in
de broekzakken. Gekozen: a (9d380e4a…). Bewegingsprompt `N4nz` (zakken): als N4 take 2, met "his hands staying in his trouser
pockets the whole time, his elbows moving gently with each step". Concept 480p: ecf0699e… (15 credits), controle wf_7d5ef22e
(kleding-lens en echtheid-lens).

**Concepten en keuze (23 okt, 12:00–12:50).** Concept N4nz-a (ecf0699e…): kleding-lens goed (kraagband RGB ≈ 45/46/57 in alle 121
frames, nul warme pixels), echtheid-lens afgekeurd: loopband (gevels stil terwijl de grond 3 px per frame schuift), gladde glijvlucht,
72 passen per minuut. Daarom twee nieuwe concepten vanaf hetzelfde startbeeld (30 credits): N4nz-b (36da4535…, dezelfde prompt) en
N4nz2-c (c6e39603…, prompt `N4nz2` met expliciete parallax: deuren en luiken links worden groter en verlaten het kader, bollards rechts
trekken voorbij, hij blijft even groot, honderd passen per minuut). Controle wf_16634991: b afgekeurd (morfende wereld: bollard krimpt
en schuift opzij, muur groeit uit de linkerrand); c goedgekeurd door beide lenzen (bollard rechts groeit van 130 naar 250 px en
verlaat het kader, 96–110 passen per minuut, standvoet vast op de stenen, kraag navy in elk frame, AI-gevoel 2). Les: de prompt
moet de parallax benoemen (wat groter wordt en het kader verlaat), "de camera reist mee" alleen is voor Seedance niet genoeg.
1080p van c: 0580660e… (80 credits); bij 1080p zelf nagemeten: kraagband RGB 36–41 / 38–42 / 49–53 in elk achtste frame, nul warme
pixels.

**Montage versie 3.** `reverso_autumn_v2-edit.json`: N1 0,4–3,5 · N2 0,6–3,9 · N3 1,2–3,6 · N4 (nieuw) 1,2–4,7 (12,3 s, 295 frames),
de nieuwe clip gladgemaakt met smooth.py (de hik op elke seconde). Het woordmerk kan niet meer rechtsonder (daar staan nu de
bollards en de donkere kasseien): nu rechtsboven over het mistwater naast zijn schouder, 0,28 breed op x 0,81 / y 0,22; op y 0,27
raakte zijn elleboog de M (−10 px), op y 0,22 blijft er minstens 51 px vrij (per rij gemeten over de laatste 2 s), rechtermarge 54 px.

**Montagecontrole en oplevering versie 3 (23 okt, 13:20).** Controle wf_4f6e8b2f op v3b: montage-lens goed (AI-gevoel 2,5; cuts op
3,08 / 6,38 / 8,79 s, geen bevroren frames, de hik van elke seconde is weg na smooth.py, de wereld schuift echt voorbij, ~100 passen
per minuut) en regels-lens goed (AI-gevoel 2; kraagband L 43–47 met B−R +11..13 in alle 84 frames van de laatste scène, de rug L 36–41;
ter vergelijking: de kraag in v2e was RGB 166/135/113 = beige, in v3 56/53/63 = navy). Enige puntje: de onderregel van het woordmerk
kwam in het laatste frame tot 26 px van zijn schouder; daarom v3c met de kaart op y 0,20 (dichtste punt 49 px, per rij nagemeten,
geen overlap). Wat blijft: N2 is nog steeds een rustige slow-motion pose (het meest "AI"-moment), N3 bijna stil, de ober ver op de
achtergrond in N3, een dunne koele mistrand op de kraagrand (grijsblauw, geen crème), rechtermarge van de kaart 55 px.

**Zip (video + Cover.jpg):** https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/be4c5ce3-08bf-4514-903e-6c6598290cbd.zip
(media be4c5ce3…). De zips 8a6e08eb… (crème kraag) en c812644e… (crème gilet) vervallen.

**Kosten derde ronde:** 4 startbeelden 16 + 3 concepten 45 + 1080p 80 = 141 credits. Totaal voor Reverso Autumn tot nu toe:
v1 + v2 383, correctie navy 133, correctie kraag 141.
