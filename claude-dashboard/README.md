# ModernoMilano Cijfers (dashboard in Claude)

`dashboard.html` is gepubliceerd als Claude-artifact: https://claude.ai/artifact/MFhtRBQRjkaRQ9iD8UsVyE

- **Shopify** (omzet per dag via ShopifyQL, fees uit de transacties van orders) en **Meta** (via Windsor.ai) komen live binnen via je Claude-connectors. Geen API-sleutels of hosting nodig.
- **Revolut**: upload het afschrift (PDF uit de app of CSV) op de pagina. Mutaties worden per maand bewaard in de opslag van het artifact en automatisch ingedeeld.
- **PayPal** (connector, `list_transactions`): de hele historie per maand. Fees, refunds, chargebacks, uitbetalingen naar de bank, holds en reserve, en daaruit het saldo. Buitenlandse valuta via het T0200-wisselpaar.
- **Shopify berekend**: payout, pending en reserve uit de verkopen via Shopify Payments (uitbetaling na X werkdagen, reserve % voor N dagen, instelbaar), met een controle tegen de payouts op de bank. Disputes en chargebacks uit de orders (`chargeback_status:*`).
- **Handmatig** (optioneel): teamkosten die niet via de bank gaan, openstaande facturen, en een saldo als de berekening ontbreekt.

De rekenregels zijn dezelfde als in `src/finance` en `src/bank` (daar staan de tests).
Wijzigen: pas `dashboard.html` aan en publiceer opnieuw naar dezelfde URL.

## Winstprognose

Tabblad naast Kasprognose: winst voor de rest van de maand of 30, 60 of 90 dagen, verwachte maandwinst, scenario's voor het Meta-budget (-30% tot +100%) en het Meta-budget per dag met de hoogste winst. Model: omzet = vast deel + Meta-deel × (budgetfactor ^ elasticiteit), standaard elasticiteit 0,7 en 80% van de omzet uit Meta, beide instelbaar. COGS uit de bank, zonder afschrift de instelling COGS zonder bankafschrift (30%).

Beide dashboards linken naar elkaar (knoppen Brand check en Financieel).

## Vraag het

Tabblad met een chat (capability `sample`). Claude rekent niet uit het hoofd maar roept de rekenfuncties van de pagina aan:
`cijfers_periode`, `dagcijfers`, `winst_prognose` (omzet, Meta en fees uit de laatste 14 dagen, COGS en vaste kosten uit
de laatste 30 dagen bank), `geld_nu` en `kasprognose`. Elke vraag gebruikt het Claude-tegoed van wie de pagina opent.

# ModernoMilano Brand Check (tweede dashboard)

`brand-check.html` is gepubliceerd als Claude-artifact: https://claude.ai/artifact/P3eRjdNbmRmRjizBVvdDDo

Een brede check van het hele merk, live via je Claude-connectors:

- **Brand check**: totaalscore en pijlers (winst na ads, ads-efficiëntie, groei, conversie, retouren, terugkerende klanten, levering), KPI's met vergelijking met de vorige periode, en een lijst "Wat nu" gesorteerd op geschatte impact per maand.
- **Ads overzicht**: KPI's, wat valt op, 90 dagen spend/ROAS/CPA/CTR/CPM, Meta-funnel van vertoning tot aankoop, campagnes met dagbudget en status, advertentiesets, markt en campagnetype.
- **Per ad**: Meta via Windsor.ai (tien losse, geaggregeerde `get_data`-vragen: ads, vorige periode, teksten en status, copy, dagcijfers, leeftijd en geslacht, landen, plaatsingen, campagnes, sets). Oordeel per ad: Schalen, Verversen, Houden, Kijken, Stoppen of Te vroeg, op basis van break-even en doel-ROAS. Signalen: hoge frequentie, dalende CTR, zwakke hook, klikt wel maar koopt niet.
- **Creatives & copy**: prestaties per angle, per creative (alle kopieën samen), per landingspagina, per formaat en knop; plus **Doelgroep** (leeftijd × geslacht, landen, plaatsingen). Angles (automatisch uit naam en tekst, door Claude in te delen, of zelf per ad te kiezen), per primaire tekst, headline en video tegenover beeld.
- **Producten**, **Funnel & site**, **Klanten & markten** (incl. PayPal-disputes), **Actielijst** (gedeeld, in de artifact-database) en **Advies** (Claude met een samenvatting van alle cijfers, capability `sample`).
- **Instellingen**: inkoop %, verzendkosten per order, betaalkosten en gewenste winst. Btw-aandeel, retour-aandeel en orderwaarde komen live uit Shopify.

Break-even ROAS = 1 / (wat er van €1 omzet incl. btw overblijft na btw, retouren, inkoop, betaalkosten en verzending).
