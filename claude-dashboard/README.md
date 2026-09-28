# ModernoMilano Cijfers (dashboard in Claude)

`dashboard.html` is gepubliceerd als Claude-artifact: https://claude.ai/artifact/MFhtRBQRjkaRQ9iD8UsVyE

- **Shopify** (omzet per dag via ShopifyQL, fees uit de transacties van orders) en **Meta** (via Windsor.ai) komen live binnen via je Claude-connectors. Geen API-sleutels of hosting nodig.
- **Revolut**: upload het afschrift (PDF uit de app of CSV) op de pagina. Mutaties worden per maand bewaard in de opslag van het artifact en automatisch ingedeeld.
- **Handmatig** (je Shopify-connector mag geen Payments lezen): stand van payout, pending en reserve, chargebacks, PayPal-saldo en PayPal-fees, teamkosten.

De rekenregels zijn dezelfde als in `src/finance` en `src/bank` (daar staan de tests).
Wijzigen: pas `dashboard.html` aan en publiceer opnieuw naar dezelfde URL.

## Order backlog

`orders-achterstand.html` is published as a Claude artifact (English UI): https://claude.ai/artifact/EoC6GWMrwv3pPzhCsDzrWK

- Loads every open order that is **unfulfilled** or **partially fulfilled** live through the Shopify connector (oldest first, up to 1000).
- Age per order: 0 to 3 days is on time, 4 to 7 late, 8+ seriously late (`LIMIT_DAYS` at the top of the script).
- Per order: customer details (email, phone, WhatsApp, address), open items, earlier tracking, link to the Shopify admin.
- Follow-up per order: status, problem type, problem, solution, expectation and expected date, a "customer informed" checkbox, and a history. Saved automatically in the artifact's shared storage (collection `cases`, document id = Shopify order id).
- "Copy update email" builds a customer email containing the expectation; "Export CSV" downloads the filtered list.
