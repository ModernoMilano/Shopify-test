# Vier reels op de focuscollecties (plan, 8 oktober 2026)

De eigenaar wil nieuwe video's die zijn Canva-bord als inspiratie nemen (zie `research/2026-10-canva-videos.md`), met Seedance 2.5 (`model.json`, `rules.video`). Er komt alleen eigen kleding in beeld. De focus ligt op vier collecties: Reverso Collection, Cashmere Sets, Cashmere Tops en Bundle & Save.

Status (8 oktober): de eigenaar koos eerst reel 1 als proef, in Bordeaux & Crema. Die proef is af en kostte 142 credits (zie `README.md`). De flat-lay is uit reel 1 gelaten. Reel 2 tot en met 4 wachten op zijn oordeel over de proef.

## Wat de winkel zegt (de enige claims die in beeld mogen)

Bron: Shopify (producten en collecties) en de webshop modernomilano.com, opgehaald op 8 oktober 2026.

- **Reverso Set** (17 kleurcombinaties, € 200, vergelijkprijs € 300, "Save €100"). Elke set bestaat uit:
  - een gilet. De winkel zegt: "Fully reversible gilet construction, two looks in one", "Regular fit gilet with stand collar and full zip closure" en "Lightweight, wrinkle resistant and quick drying gilet and trousers";
  - een tee in "100% mercerized cotton";
  - een broek met "mid-rise elastic waistband".

  De productpagina noemt het "Bundle & Save 3 piece set". De naam geeft de kleuren: bij CREMA & NERO is het gilet crème met zwart aan de binnenkant, de tee zwart en de broek crème. Omgekeerd draagt hij het gilet met de zwarte kant naar buiten (de productfoto "reversed").
- **Bundle & Save**. De collectie zegt: "Mix and match your favourite essentials and save more the more you add." De productpagina's zeggen: "Mix & Match. More You Add, More You Save." De vragen onderaan de pagina:
  - "your discount is applied at checkout, no code needed";
  - "Exact tiers and savings are shown directly in your cart".

  De balk boven aan de site zegt: "WE ALREADY MATCHED YOUR OUTFIT. SHOP BUNDLE & SAVE". De korting komt van de FastBundle-app, niet van een Shopify-korting, dus de exacte staffel staat niet in Shopify. Daarom komen er geen percentages in beeld.
- **Cashmere Sets** (13 producten, € 150 tot € 300) en **Cashmere Tops** (55 producten, € 110 tot € 420). Er staan geen prijzen of kortingen in beeld; de site meldt wel "CASHMERE SALE NOW LIVE. UP TO 50% OFF".

Niet gebruiken: verzendbeloftes. De balk zegt "free … shipping on every order", maar de vragen noemen "orders above €150"; dat spreekt elkaar tegen.

## Opbouw van elke reel (les van het bord)

- 9:16, 10 tot 15 seconden, harde snedes om de 1 à 2,5 seconden.
- Tekst in beeld in het Engels, rustige schreefletter.
- Eindbeeld met ModernoMilano. Muziek komt er bij het posten bij.
- Elk bewegend shot is één Seedance-clip van 4 seconden: eerst een concept in 480p (12 credits), dan de controle frame voor frame, en pas daarna afmaken in 1080p (48 credits).
  - Uit één clip komen één of twee snedes.
  - Bij elke clip kleine bewegingen: een rits, een mouw, een hand in de zak, wind in een gordijn. Geen lopen, geen hoofddraai van meer dan 45 graden, niemand anders dichtbij.
- Close-ups van stof en flat-lays zijn foto's (Nano Banana Pro) met een langzame camerabeweging in de montage. Zo doet het bord het ook (1-10).
- Montage, tekst en snedes: ffmpeg in de Higgsfield-sandbox, zonder credits.

## Reel 1: "One gilet. Two looks." (Reverso Collection)

Product: **MILANO REVERSO SET BORDEAUX & CREMA** (keuze van de eigenaar): een bordeaux gilet met crème binnenkant, een crème tee en een bordeaux broek. De andere kandidaten waren CREMA & NERO en MARRONE & CAMMELLO. Zoals gemaakt: zie `README.md`. De flat-lay viel af, in de plaats daarvan kwam een detail uit startbeeld B.

| # | Duur | Beeld | Tekst |
|---|---|---|---|
| 1 | 1,2 s | Macro (foto): de opstaande kraag met zilveren rits, de zwarte binnenkant zichtbaar bij de opening, ochtendlicht | One gilet. |
| 2 | 2,2 s | **Clip A**: binnenplaats in Brera, waist-up, crème kant buiten; hij trekt de rits het laatste stuk dicht en kijkt opzij | |
| 3 | 2,2 s | **Clip B**: zelfde plek en uitsnede, gilet met de zwarte kant buiten (crème aan de binnenkant); hand in de broekzak | Two looks. |
| 4 | 1,4 s | Flat-lay (foto): gilet, tee en broek op een houten vloer, raamlicht | Reversible gilet, tee and trousers. |
| 5 | 1,8 s | Clip A, tweede helft | |
| 6 | 1,5 s | Eindbeeld: laatste frame van clip B, rustig | Milano Reverso Set / ModernoMilano |

Startbeeld B is een bewerking van startbeeld A, met de productfoto "reversed" als referentie. Zo blijven plek en licht gelijk.

Kosten: 2 clips × 60 = 120. Daarbij komen ongeveer 24 voor de startbeelden en foto's, inclusief een herkansing, en 12 voor een reserveconcept. **Ongeveer 155 credits.**

## Reel 2: "Autumn knits rotation" (Cashmere Tops)

Het format van bord 1-09 en 1-11. Telkens dezelfde plek: een hoog raam in een appartement in Milaan, een witte muur en een visgraatvloer. De camera staat stil. Het beeld loopt van de kin tot halverwege de dij, zonder hoofd, zodat alle aandacht naar het breisel gaat. Hij draagt steeds dezelfde MILANO SIGNATURE TROUSERS - GREY. Elke snede is een andere top met zijn naam in beeld.

| # | Top | Beweging | Tekst |
|---|---|---|---|
| 0 | (eerste frame van 1) | | Autumn knits rotation |
| 1 | MILANO CASHMERE LIDO - AVENA | strijkt de voorkant glad | Lido, Avena |
| 2 | MILANO CASHMERE BERGAMO POLO - BORDEAUX | trekt een manchet recht | Bergamo, Bordeaux |
| 3 | MILANO CASHMERE BELLAGIO - FOREST GREEN | trekt de rits een stukje op | Bellagio, Forest Green |
| 4 | MILANO CASHMERE SORRENTO POLO - CAMMELLO | hand in de zak, gewicht op één been | Sorrento, Cammello |
| 5 | eindbeeld | | Milano Cashmere / ModernoMilano |

Dit zijn tops die in eerdere series goed uit het beeldmodel kwamen.

Kosten: 4 clips × 60 = 240, plus ongeveer 32 voor de startbeelden en 12 als reserve. **Ongeveer 285 credits.** Met 3 tops is dat ongeveer 210.

## Reel 3: "Three looks. Cashmere." (Cashmere Sets)

Het format van bord 4-01: drie scènes in een warm interieur in Milaan, elk met een titel in gele schreefletters. Zijn gezicht is in beeld (met de gezichtsfoto's als referentie).

| Scène | Set | Moment | Tekst |
|---|---|---|---|
| Morning | MILANO KNITTED CASHMERE SET - CHAMPAGNE | aan een marmeren tafeltje bij het raam, een espresso staat ernaast, hij kijkt naar buiten en weer terug | Morning |
| Afternoon | MILANO KNITTED TWO-TONE CASHMERE SET - NAVY | bij de openstaande balkondeuren, het gordijn beweegt, hij zet de rits bij de kraag goed | Afternoon |
| Evening | MILANO KNITTED TWO-TONE CASHMERE SET - DARK MOCHA | in een fauteuil bij een staande lamp, een platenspeler draait, hij leunt achterover | Evening |

Per scène komen er één clip en één macro van het breisel (foto). De reel opent met "Three looks. Cashmere." en eindigt met "Milano Cashmere Sets".

Kosten: 3 clips × 60 = 180, plus ongeveer 36 voor de startbeelden en macro's en 12 als reserve. **Ongeveer 230 credits.**

## Reel 4: "We already matched your outfit." (Bundle & Save)

Het promotieformat van bord 3-01 en 2-01, grotendeels gemaakt van materiaal uit reel 1 en 3.

| # | Duur | Beeld | Tekst |
|---|---|---|---|
| 1 | 2 s | Stop-motion (foto's, zonder persoon): op dezelfde houten hanger tegen een kalkmuur wisselt de set elke 0,4 s (Reverso Bordeaux & Crema, Champagne, Two-tone Navy, Dark Mocha; een gilet van de Reverso Set plat of op een hanger laten tekenen lukte in reel 1 niet, dus eerst testen of de productfoto gebruiken) | We already matched your outfit. |
| 2 | 1,8 s | Clip A uit reel 1 | Mix & match. |
| 3 | 1,8 s | Morning uit reel 3 | |
| 4 | 1,8 s | Evening uit reel 3 | The more you add, the more you save. |
| 5 | 2 s | Eindbeeld | Bundle & Save. Discount applied at checkout, no code needed. |

Kosten: 4 hangerfoto's in 2K plus een herkansing. **Ongeveer 16 credits.**

## Totaal

| Reel | Credits (ongeveer) |
|---|---|
| 1 Reverso | 155 |
| 2 Cashmere Tops | 285 |
| 3 Cashmere Sets | 230 |
| 4 Bundle & Save | 16 |
| **Samen** | **ongeveer 690** (saldo 8 oktober: 1000) |

Volgorde: reel 1 eerst, als proef, en daarna de eigenaar laten kijken. Pas na zijn akkoord volgen reel 3, 2 en 4. Komt een clip twee keer afgekeurd uit het concept, dan stoppen we en vragen we het hem (`rules.video`).
