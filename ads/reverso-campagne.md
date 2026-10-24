# Reverso campagne: draaiboek en logboek

Claude beheert deze campagne. Dit bestand is de bron van waarheid voor de regels en elke wijziging.

## Campagne

| Onderdeel | Waarde |
|---|---|
| Ad account | 1429115185245447 (EUR) |
| Campagne | MM \| REVERSO \| CBO, id 120252036387820541 |
| Ad set | REVERSO \| Broad \| Men 20-50 \| EU+US+UK, id 120252036390250541 |
| Live sinds | 2026-10-13 01:10 (Amsterdam) |
| Startbudget | EUR 150 per dag (CBO) |

## Regels (afgesproken met eigenaar op 2026-10-13)

1. **Meetmethode.** ROAS = door Meta gerapporteerde aankoopwaarde gedeeld door spend, campagneniveau, alleen volle kalenderdagen (Amsterdam). Vandaag telt nooit mee.
2. **Moment en wachttijd.** Check en aanpassingen elke nacht om 03:54 (Amsterdam), als de cijfers van de vorige dag binnen zijn. Een nieuw budget geldt dan vrijwel de hele nieuwe dag. Na een budgetwijziging pas weer aanpassen op de check twee nachten later (48 uur). Eerste mogelijke aanpassing: 2026-10-15 03:54, met 13 en 14 oktober als beoordeelde dagen. Lijkt de spend van gisteren onder 80% van het dagbudget terwijl de dagen ervoor wel vol uitgaven, dan zijn de cijfers nog niet compleet: niets wijzigen en de volgende nacht opnieuw beoordelen.
3. **Afschalen gaat voor.** ROAS de laatste 2 volle dagen elk onder 2,0: dagbudget x0,5. Daarna worden regel 4 en 5 niet meer bekeken.
4. **Hard opschalen, alleen met toestemming.** ROAS over de volle dagen sinds de laatste wijziging boven 3,0: voorstel dagbudget x2. Nooit zelf uitvoeren. Eerst in de chat toestemming vragen en tot het antwoord niets aan het budget veranderen.
5. **Rustig opschalen.** ROAS over de volle dagen sinds de laatste wijziging van 2,1 tot en met 3,0: dagbudget x1,2.
   Tussen 2,0 en 2,1, of onder 2,0 zonder dat regel 3 geldt: niets doen.
6. **Plafond.** Nooit een dagbudget boven EUR 600 zetten zonder nieuwe toestemming van de eigenaar in de chat. Als een regel daarboven uitkomt: niet uitvoeren, eerst vragen. (Verhoogd van EUR 500 naar EUR 600 op 2026-10-13.)
7. **Ads pauzeren** (alleen op een dag dat de wachttijd voorbij is, samen met een eventuele budgetwijziging):
   - EUR 60 of meer spend en 0 aankopen, of
   - EUR 120 of meer spend en ROAS onder 1,5.
   Nooit zo veel pauzeren dat er minder dan 4 ads actief blijven.
8. **Nieuwe creatives aanvragen** bij de eigenaar als een van deze geldt:
   - frequentie over 7 dagen boven 2,5;
   - minder dan 6 ads actief na pauzeren;
   - de best presterende ad zakt 2 volle dagen onder ROAS 2,0.
9. **Alleen deze campagne.** Andere campagnes worden niet aangeraakt.

## Logboek

| Datum (Amsterdam) | Actie | Budget voor | Budget na | Onderbouwing |
|---|---|---|---|---|
| 2026-10-13 01:10 | Lancering, 15 ads live | - | EUR 150 | Startinstelling |
| 2026-10-14 03:54 | Observatie, geen actie: Windsor meldt dagbudget EUR 100. Niet door Claude gewijzigd, eigenaar gevraagd | EUR 150 | EUR 100 (gemeld) | Dag 1 (13 okt): EUR 169,13 spend, 0 aankopen, 150 klikken, frequentie 1,79 |
| 2026-10-14 17:00 | Besluit eigenaar: bij de check van 2026-10-15 03:54 de afschaalregel (x0,5) eenmalig overslaan. Ads pauzeren volgens regel 7 gaat wel door | - | - | Te weinig data na EUR 260 spend |
| 2026-10-14 | Shopify-prijzen op verzoek eigenaar: alle 17 "MILANO REVERSO SET ..." van EUR 200 naar EUR 175, plus de 7 oudere sets (Reverso Sabbia/Casa/Nero/Voyage, Milano Sabbia/Oliva/Nero) naar EUR 175. Compare-at ongewijzigd (nieuwe sets EUR 300) | - | - | Let op bij ROAS-vergelijking: lagere orderwaarde vanaf 14 okt. Adcopy noemt op meerdere plekken nog "EUR 200" |
| 2026-10-15 03:54 | Check. Afschalen eenmalig overgeslagen (besluit eigenaar). REV_09_CremaBordeaux_Unboxing (120252036419770541) gepauzeerd volgens regel 7. 14 ads blijven actief | EUR 100 (Meta) | EUR 100 | 13 okt: EUR 169,20 spend, 0 aankopen. 14 okt: EUR 129,62 spend, 0 aankopen, 177 klikken, freq 1,52. REV_09: EUR 131,46 spend, 0 aankopen |
| 2026-10-16 03:54 | Observatie, geen actie: campagne staat op CAMPAIGN_PAUSED (niet door Claude gepauzeerd). Afschalen (regel 3) en pauzeren van REV_12 (regel 7) aangehouden tot de eigenaar laat weten wat de bedoeling is | EUR 100 | EUR 100 | 15 okt: EUR 51,54 spend, 0 aankopen, 35 klikken. Totaal 13-15 okt: EUR 350,55 spend, 0 aankopen. REV_12: EUR 72,29 spend, 0 aankopen |
| 2026-10-17 03:54 | Observatie, geen actie: campagne staat nog op PAUSED, 16 okt geen spend. Regels 3 en 7 blijven aangehouden tot besluit eigenaar | EUR 100 | EUR 100 | Totaal sinds lancering: EUR 350,55 spend, 0 aankopen |
| 2026-10-18 03:54 | Observatie, geen actie: campagne staat nog op PAUSED, 17 okt geen spend | EUR 100 | EUR 100 | Totaal sinds lancering ongewijzigd: EUR 350,55 spend, 0 aankopen |
| 2026-10-19 03:54 | Observatie, geen actie: campagne staat nog op PAUSED, 18 okt geen spend | EUR 100 | EUR 100 | Totaal sinds lancering ongewijzigd: EUR 350,55 spend, 0 aankopen |
| 2026-10-20 03:54 | Observatie, geen actie: campagne staat nog op PAUSED, 19 okt geen spend. Geen ads afgekeurd | EUR 100 | EUR 100 | Totaal sinds lancering ongewijzigd: EUR 350,55 spend, 0 aankopen |
| 2026-10-21 03:54 | Observatie, geen actie: campagne staat nog op PAUSED, 20 okt geen spend. Geen ads afgekeurd | EUR 100 | EUR 100 | Totaal sinds lancering ongewijzigd: EUR 350,55 spend, 0 aankopen |
| 2026-10-22 03:54 | Observatie, geen actie: campagne staat nog op PAUSED, 21 okt geen spend. Geen ads afgekeurd | EUR 100 | EUR 100 | Totaal sinds lancering ongewijzigd: EUR 350,55 spend, 0 aankopen |
| 2026-10-23 03:54 | Observatie, geen actie: campagne staat nog op PAUSED, 22 okt geen spend. Geen ads afgekeurd | EUR 100 | EUR 100 | Totaal sinds lancering ongewijzigd: EUR 350,55 spend, 0 aankopen |
| 2026-10-24 03:54 | Observatie, geen actie: campagne staat nog op PAUSED, 23 okt geen spend. Geen ads afgekeurd | EUR 100 | EUR 100 | Totaal sinds lancering ongewijzigd: EUR 350,55 spend, 0 aankopen |
