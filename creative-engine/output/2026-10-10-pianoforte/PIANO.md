# Il pianoforte (10 oktober 2026)

Wens van de eigenaar: geen slow motion maar normaal tempo, in een luxe huis bij een vleugel.
- Het shot begint dichtbij op zijn hand met een vinger op een toets, met de focus op kleding en kwaliteit.
- Daarna wordt er steeds verder uitgezoomd, terwijl hij naar een groot raam loopt en naar buiten kijkt.
- Aan het eind is de hele outfit van opzij te zien.

Outfit: MILANO REVERSO SET ANTRACITE & PIETRA (de bodywarmer met de antracietkant buiten) en MILANO SUEDE LOAFER - GRIGIO, met blote voeten.

Prompts en referenties: `piano.py`.

## Start- en eindbeeld

| Index | Job | Wat | Oordeel |
|---|---|---|---|
| 80 | 7efef2b6-0e84-4f80-be0f-079f864ec5e5 | eindbeeld, ronde 1 (4k) | afgekeurd: penny loafers (overgenomen van de setfoto aan het model), toetsenbord met zwarte toetsen in een gelijkmatige rij, haar te donker en te koel |
| 81 | bcd5e98d-0013-408c-b146-461b9a7b8eba | eindbeeld, ronde 1 (4k) | afgekeurd: tv met stopcontacten aan de muur, te zware stoppels |
| 82 | b7b4a090-e4c0-47d3-83b3-7b7006f0a5a3 | startbeeld, ronde 1 | afgekeurd: tweede hand op de toetsen |
| 83 | 4b10063d-90bf-493f-81e0-5c1097fdb686 | startbeeld, ronde 1 | afgekeurd: toetsenbord in tweeën, hij leunt over de vleugel |
| 84 | b2deb574-4993-43cb-9cf3-90eb4e0161d5 | startbeeld, ronde 2 | afgekeurd: losse vingers aan de rand, gouden letters op de klep |
| 85 | d1d73c1f-ee16-40c0-9b2b-d17ebe12c5e0 | startbeeld, ronde 2 | afgekeurd: losse vingers aan de rand |
| 86 | da532965-af9c-4711-bd2c-c33c97dfcfa9 | startbeeld, ronde 3 | afgekeurd: tweede hand (of spiegeling) in de klep |
| **87** | **928c365c-4920-4184-a043-8e9a9e801112** | **startbeeld, ronde 3 (4k)** | **gekozen**: één hand, armsgaten antraciet. De zwarte toetsen staan in de onscherpte vrij gelijkmatig. |
| 88 | e27304f9-e5cf-4f09-a470-3593d1d88dae | bewerking van 80, alleen de schoenen (2k) | afgekeurd: de penny loafers bleven staan |
| **90** | **3cb9512a-2879-4588-8944-e52ed9384978** | **eindbeeld, ronde 2 (2k)** | **gekozen**: Grigio met glad voorblad, warm kastanjebruin haar. Linksonder staat toch een stuk toetsenbord, onscherp. |
| 91 | 1b1eb7bc-4529-4695-8900-c1a4ded99217 | eindbeeld, ronde 2 (2k) | reserve: ook goed, maar zwaardere stoppels |

Ronde 2 van het eindbeeld gebruikt het goedgekeurde startbeeld 87 als referentie voor de kamer. De setfoto aan het model is boven de enkels afgesneden (media 3de9e4be), zodat zijn penny loafers niet meer meekomen.

2k is genoeg voor een video-eindbeeld (de video wordt 1080p) en kost 2 credits in plaats van 4.

## Lessen

- **Set aan het model met andere schoenen:** snijd de foto boven de enkels af voordat hij referentie wordt. Anders neemt het model die schoenen over, ook met een loafer-referentie erbij.
- **Bewerking voor alleen de schoenen:** werkt niet. Het model houdt de schoenen uit het bronbeeld vast.
- **Hand op de toetsen:** zonder meer instructie komt er een tweede hand of losse vingers bij. Wat hielp:
  - zijn andere hand benoemen ("hidden behind his body");
  - maar één octaaf in beeld laten;
  - letters op de klep uitdrukkelijk verbieden.
- **Links of rechts:** staat hij met zijn gezicht naar de rechterkant van het beeld, dan zie je zijn rechterkant. In het startbeeld kijkt hij naar de vleugel (links). Dus draait hij zich om en loopt hij naar het raam.

## Kosten en saldo

Vandaag 38 credits: 8 beelden op 4k à 4 credits en 3 op 2k à 2 credits. Saldo na afloop: 10,55.

Volgens de transactielijst stond er vóór vandaag 48,55, niet de 96,55 uit het vorige verslag; dat verschil staat niet in de transacties.

## Video (wacht op goedkeuring van de beelden en een top-up)

Opzet: Seedance 2.5 met 87 als start_image en 90 als end_image, op normaal tempo, zonder slow motion. Dan gladmaken met `smooth.py` (dat vertraagt niets) en het logo aan het eind.

Prijzen opgevraagd met get_cost (10 okt), met beide beelden en de 2 gezichtsreferenties:

| Optie | Credits |
|---|---|
| 8 s: concept (480p) en dan 1080p | 24 + 96 = 120 |
| 8 s: direct 720p, zonder concept | 56 |
| 6 s: concept (480p) en dan 1080p | ongeveer 18 + 72 = 90 (3 en 12 per seconde) |

Opdracht bouwen: `python3 -I piano.py video draft 8`, en daarna `python3 -I piano.py video <concept job>` voor 1080p.
