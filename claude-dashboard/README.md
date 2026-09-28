# ModernoMilano Cijfers (dashboard in Claude)

`dashboard.html` is gepubliceerd als Claude-artifact: https://claude.ai/artifact/MFhtRBQRjkaRQ9iD8UsVyE

- **Shopify** (omzet per dag via ShopifyQL, fees uit de transacties van orders) en **Meta** (via Windsor.ai) komen live binnen via je Claude-connectors. Geen API-sleutels of hosting nodig.
- **Revolut**: upload het afschrift (PDF uit de app of CSV) op de pagina. Mutaties worden per maand bewaard in de opslag van het artifact en automatisch ingedeeld.
- **Handmatig** (je Shopify-connector mag geen Payments lezen): stand van payout, pending en reserve, chargebacks, PayPal-saldo en PayPal-fees, teamkosten.

De rekenregels zijn dezelfde als in `src/finance` en `src/bank` (daar staan de tests).
Wijzigen: pas `dashboard.html` aan en publiceer opnieuw naar dezelfde URL.

## Orderachterstand

`orders-achterstand.html` is gepubliceerd als Claude-artifact: https://claude.ai/artifact/EoC6GWMrwv3pPzhCsDzrWK

- Haalt live via je Shopify-connector alle open orders op die **unfulfilled** of **gedeeltelijk verzonden** zijn (oudste eerst, tot 1000).
- Leeftijd per order: 0 tot 3 dagen is binnen termijn, 4 tot 7 te laat, 8+ ernstig te laat (`LIMIT_DAYS` bovenaan het script).
- Per order: klantgegevens (e-mail, telefoon, WhatsApp, adres), open artikelen, eerdere tracking, link naar Shopify-admin.
- Opvolging per order: status, soort probleem, probleem, oplossing, verwachting en verwachte datum, vinkje "klant ingelicht", geschiedenis. Wordt automatisch bewaard in de gedeelde opslag van het artifact (collectie `cases`, document-id = Shopify order-id).
- Knop "Kopieer update-mail" maakt een Engelse klantmail met de verwachting erin; "Export CSV" voor Excel.
