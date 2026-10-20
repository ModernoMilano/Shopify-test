# ModernoMilano Cijfers (dashboard in Claude)

`dashboard.html` is gepubliceerd als Claude-artifact: https://claude.ai/artifact/MFhtRBQRjkaRQ9iD8UsVyE

- **Shopify** (omzet per dag via ShopifyQL, fees uit de transacties van orders) en **Meta** (via Windsor.ai) komen live binnen via je Claude-connectors. Geen API-sleutels of hosting nodig.
- **Revolut**: upload het afschrift (PDF uit de app of CSV) op de pagina. Mutaties worden per maand bewaard in de opslag van het artifact en automatisch ingedeeld.
- **PayPal** (connector, `list_transactions`): de hele historie per maand. Fees, refunds, chargebacks, uitbetalingen naar de bank, holds en reserve, en daaruit het saldo. Buitenlandse valuta via het T0200-wisselpaar.
- **Shopify berekend**: payout, pending en reserve uit de verkopen via Shopify Payments (uitbetaling na X werkdagen, reserve % voor N dagen, instelbaar), met een controle tegen de payouts op de bank. Disputes en chargebacks uit de orders (`chargeback_status:*`).
- **Handmatig** (optioneel): teamkosten die niet via de bank gaan, openstaande facturen, en een saldo als de berekening ontbreekt.

De rekenregels zijn dezelfde als in `src/finance` en `src/bank` (daar staan de tests).
Wijzigen: pas `dashboard.html` aan en publiceer opnieuw naar dezelfde URL.

## Vraag het

Tabblad met een chat (capability `sample`). Claude rekent niet uit het hoofd maar roept de rekenfuncties van de pagina aan:
`cijfers_periode`, `dagcijfers`, `winst_prognose` (omzet, Meta en fees uit de laatste 14 dagen, COGS en vaste kosten uit
de laatste 30 dagen bank), `geld_nu` en `kasprognose`. Elke vraag gebruikt het Claude-tegoed van wie de pagina opent.

## Betrouwbaarheid van de winst

- Een afschrift dat niet tot op de cent sluit wordt niet opgeslagen. De lezer kent beide notaties: "€1.234,56" en "1.234,56€".
- Dezelfde mutatie uit een PDF en een CSV telt één keer (zelfde dag, bedrag en saldo).
- Dagen zonder bankafschrift krijgen een zichtbare schatting voor COGS, software en team uit de laatste 30 dagen bank.
- Chargebacks komen uit de tijdlijn van de order: het bedrag dat Shopify echt van de payout inhield, op die datum, min wat na een gewonnen dispute terugkwam.
- Hold: Shopify houdt standaard 10% van de verkopen 35 dagen vast, PayPal komt uit de transacties. Op Overzicht staat de winst die je nu kunt gebruiken.
