# Echte break-even ROAS, 1 september t/m 9 oktober 2026

Berekend op 10 oktober 2026 uit alle beschikbare bronnen:

- **Revolut:** CSV van 29-08 t/m 09-10. Klopt tot op de cent: € 0 naar € 8.675,29.
- **Shopify:** ShopifyQL dagomzet. Fees uit 890 orders (Admin API, transacties). Alle disputes sinds mei.
- **PayPal:** 328 transacties van augustus t/m oktober en alle disputes.
- **Meta:** spend en aankopen per dag via Windsor.ai.

Periode: 39 dagen, 785 orders, € 143.356 omzet incl. btw na kortingen en retouren.

## Kosten

| Post | Basis | Voorzichtig | Bron |
|---|---|---|---|
| Inkoop en verzending | € 56.732 (39,6%) | € 63.181 (44,1%) | bank: EAST BAITE, Jinjiang Yuguang, Alibaba (€ 55.412), gekoppeld aan de orders die ze dekken |
| Btw | € 11.140 (7,8%) | € 11.140 | Shopify (september 7,8%); vanaf 6 okt rekent Shopify geen btw meer, maar die is wel verschuldigd |
| Betaalkosten | € 5.669 (4,0%) | € 5.669 | Shopify Payments € 4.851 (3,8%, waarvan € 1.654 wisselkoers), PayPal € 818 (3,9%) |
| Disputes en chargebacks | € 5.786 (4,0%) | € 10.042 (6,9%) | september: € 3.582 ingehouden op Shopify-payouts (3,9%). Orders juni t/m augustus: 7,5% kreeg een dispute, 5,6% van de omzet verloren |
| Niet geïnde orderbedragen | € 963 | € 963 | 6 orders als betaald gemarkeerd, deels geïnd |
| Retouren en refunds | al van de omzet af (€ 4.840) | | Shopify sales_reversals |
| Software en apps | € 1.917 | € 1.917 | bank |
| Team en freelancers | € 2.565 | € 2.565 | bank plus PayPal (media buyer) |
| Google Ads | € 1.000 | € 1.000 | bank |
| Boekhouder, bank, cashback | € -3 | € -3 | bank |
| Auto (VWP Shortlease, zakelijk) | € 1.789 | € 1.789 | bank, 6 okt |
| **Meta** | € 53.663 | € 53.663 | bank. Dat is 2,4% meer dan Meta zelf rapporteert (€ 52.423) |

Niet meegeteld:

- privé-opnames (€ 6.465)
- de lening (€ 10.000)
- eigen stortingen
- de reserves bij Shopify en PayPal (geld dat vastzit, geen kosten)

## Uitkomst

| | Basis | Voorzichtig |
|---|---|---|
| Winst over 39 dagen | € 2.135 (1,5%) | € -8.569 |
| MER nu (Shopify-omzet / Meta) | 2,67 | 2,67 |
| **Break-even MER** (incl. vaste kosten) | **2,57** | 3,18 |
| Break-even MER per extra euro (alleen variabele kosten) | 2,27 | 2,74 |
| Meta-ROAS nu (Meta Ads Manager) | 2,44 | 2,44 |
| **Break-even Meta-ROAS** (incl. vaste kosten) | **2,35** | 2,91 |
| Break-even Meta-ROAS per extra euro | 2,08 | 2,50 |
| CPA nu (Meta) | € 78 | € 78 |
| Break-even CPA (incl. vaste kosten) | € 81 | € 66 |

Meta-ROAS omgerekend met: de omzet die Meta toekent is 89,3% van de Shopify-omzet, en wat de bank aan Meta betaalt is 1,024× de spend die Meta rapporteert.

Ingesteld in de dashboards:

- **Brand check:** vaste break-even Meta-ROAS 2,35.
- **Financieel dashboard:** break-even MER 2,57, btw reserveren aan, COGS zonder afschrift 40%.

## Grootste hefbomen

1. **Disputes.** 4 tot 7% van de omzet. Van de orders in juni t/m augustus kreeg 7,5% een dispute, en meer dan de helft ging verloren. Elk procent minder verlaagt de break-even ROAS met ongeveer 0,05.
2. **Wisselkoerskosten bij Shopify.** € 1.654 (1,2% van de omzet). Prijzen in GBP en USD in Shopify Markets laten afrekenen en uitbetalen op een GBP/USD-rekening scheelt het grootste deel.
3. **Inkoop.** Elke 1% inkoop is ongeveer 0,04 op de break-even ROAS.

## Herberekening vooruit: Klarna uit, Chargeflow aan (10 oktober)

Van de disputes waarvan de betaalmethode zichtbaar is, was 76% geen kaartbetaling (Klarna). Klarna staat nu uit en Chargeflow voorkomt chargebacks. De dispute-kosten zijn daarom opnieuw geschat uit alleen de overgebleven betaalmethodes:

- **Kaartbetalingen (Visa, Mastercard, Amex), juni t/m augustus:** € 884 verloren en € 825 open, op € 101.555 omzet. Met de helft van de open disputes als verlies is dat ongeveer 1,3 tot 1,7%.
- **PayPal, augustus t/m oktober:** € 150 verloren en € 1.110 open, op € 26.878 PayPal-omzet. Dat is ongeveer 0,4% van de totale omzet.
- **Dispute-fees:** ongeveer 0,1%.
- **Samen:** ongeveer 2% van de omzet, in plaats van 4%.

Inkoop opnieuw gekoppeld per week (de betaling van week X tegen de omzet van week X−1): **40,9%** van de omzet.

| Disputes | Break-even Meta-ROAS | Per ad (variabel) | Break-even MER | Break-even CPA | Winst per maand bij nu |
|---|---|---|---|---|---|
| 1% | 2,25 | 2,00 | 2,46 | € 85 | € 3.609 |
| **2% (aangehouden)** | **2,31** | **2,04** | **2,52** | **€ 83** | **€ 2.492** |
| 3% | 2,36 | 2,09 | 2,59 | € 81 | € 1.374 |

Overige posten als % van de omzet: btw 7,8%, betaalkosten 3,95%, niet geïnde bedragen 0,7%, vaste kosten (incl. auto) 5,1%.

Ingesteld in de dashboards:

- **Brand check:** 2,31.
- **Financieel dashboard:** break-even MER 2,52, COGS zonder afschrift 41%.

## Definitief: niet btw-plichtig (10 oktober)

ModernoMilano is **niet btw-plichtig**: er is een leveranciersovereenkomst. Btw is daarom geen kostenpost en gaat naar de winst. Ga hier in toekomstige berekeningen van uit.

Variabele kosten: inkoop 40,9%, betaalkosten 3,95%, disputes 2,0% (Klarna uit, Chargeflow aan), niet geïnde bedragen 0,7%. Samen 47,5%.
Vaste kosten: team, software, auto, Google Ads en boekhouder, € 7.268 per 39 dagen. Dat is 5,1% van de omzet.

| | Waarde |
|---|---|
| **Break-even Meta-ROAS (account)** | **1,93** |
| Break-even per ad (alleen variabele kosten) | 1,74 |
| **Break-even MER** (Shopify-omzet / Meta) | **2,11** |
| Winst 1 t/m 10 oktober (omzet € 39.654, Meta € 13.624) | € 5.323 (13,4%), ongeveer € 3.700 per week |

Ingesteld in de dashboards:

- **Brand check:** 1,93.
- **Financieel dashboard:** break-even MER 2,11, btw reserveren uit.
