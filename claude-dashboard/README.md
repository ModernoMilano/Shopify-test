# ModernoMilano Cijfers (dashboard in Claude)

`dashboard.html` is gepubliceerd als Claude-artifact: https://claude.ai/artifact/MFhtRBQRjkaRQ9iD8UsVyE

- **Shopify** (omzet per dag via ShopifyQL, fees uit de transacties van orders) en **Meta** (via Windsor.ai) komen live binnen via je Claude-connectors. Geen API-sleutels of hosting nodig.
- **Revolut**: upload het afschrift (PDF uit de app of CSV) op de pagina. Mutaties worden per maand bewaard in de opslag van het artifact en automatisch ingedeeld.
- **Handmatig** (je Shopify-connector mag geen Payments lezen): stand van payout, pending en reserve, chargebacks, PayPal-saldo en PayPal-fees, teamkosten.

De rekenregels zijn dezelfde als in `src/finance` en `src/bank` (daar staan de tests).
Wijzigen: pas `dashboard.html` aan en publiceer opnieuw naar dezelfde URL.
