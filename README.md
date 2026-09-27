# ModernoMilano Backoffice

Financieel dashboard voor ModernoMilano. Het laat zien hoeveel winst je echt maakt, waar je geld staat, waarom de winst niet één op één op je bank staat, en hoe je banksaldo zich de komende 7 tot 30 dagen ontwikkelt.

## Schermen

| Scherm | Wat het laat zien |
|---|---|
| Overzicht | Kop in gewone taal, waarschuwingen, verdeling van elke euro omzet, KPI's (omzet, winst, marge, MER, AOV, Meta %, COGS %), omzet en Meta per dag, winst en verlies met bron per post |
| Waar mijn geld staat | Bank, PayPal, ingeplande payout, pending en reserve (gearceerd, op slot), NDRP-reserve en chargeback rate, openstaande lening |
| Winst naar bank | Waterval van winst naar groei van de bankrekening met uitleg per stap |
| Prognose | Schuifregelaars, 7, 14 of 30 dagen, twee scenario's naast elkaar, laagste punt en waarschuwing onder buffer |
| Meta ads | Spend, betaald, ROAS per campagne en per markt, CPC, CPM, frequency, log van budgetwijzigingen met protocolcontrole |
| Bankmutaties | Import van Revolut PDF of CSV, automatische categorisering met eigen regels, hoort bij periode per mutatie, controle begin + mutaties = eind |
| Payouts en disputes | Shopify payouts met controlekolom (afwijkingen zichtbaar), disputes met deadline, PayPal |
| Marge per product, Kostprijzen, Orders, Leveranciers | Marge per product op basis van ingevulde inkoopprijzen |
| Handmatige invoer | Stand van Shopify en PayPal, teamkosten, openstaande leveranciersfacturen, overige posten, leningen |
| Instellingen en sync | Knop Ophalen met status per bron, btw reserveren, buffer, prognose-instellingen |

## Definities

Alle formules staan in `src/finance/calculations.ts` en zijn getest.

- **Omzet** = Shopify `total_sales`: incl. btw (btw fix), incl. verzendkosten klant, na kortingen en retouren.
- **Kosten** = COGS en verzending + Meta + fees + chargebacks + software, freelancers, boekhouder en bank + team.
- **COGS, Meta en overig** komen uit de bank (cash-basis). Met "hoort bij periode" zet je een betaling in een andere periode, bijvoorbeeld Meta-kosten van de vorige maand.
- **Fees en chargebacks** komen uit de Shopify payouts, PayPal-fees voorlopig handmatig.
- Privé-opnames, leningen en eigen stortingen tellen nooit mee in de winst.
- **Break-even ROAS** = omzet / (omzet min alle kosten behalve Meta).

## Installatie

```bash
npm install
cp .env.example .env          # vul DATABASE_URL en de rest in
npx prisma db push            # tabellen aanmaken
npm run dev                   # http://localhost:3000
```

### Testset september 2026

```bash
# zet het Revolut-afschrift in fixtures/private/revolut-2026-09.pdf (staat niet in git)
npm run db:seed:september
npm test
```

Dit laadt de echte Shopify-dagomzet (augustus en september), de echte Meta-cijfers uit Windsor.ai, het Revolut-afschrift en de startwaarden uit de spec (saldi, payouts-samenvatting, PayPal-fees, lening). Alleen de financiële tabellen worden gewist.

### Koppelingen

- **Shopify**: maak een custom app met de scopes uit `.env.example` en zet de token in `SHOPIFY_ADMIN_TOKEN`. Daarna haalt Ophalen dagomzet, payouts, disputes, orders en producten op.
- **Windsor.ai**: zet `WINDSOR_API_KEY`. Velden: spend, clicks, impressions, actions_purchase, action_values_purchase, frequency.
- **Revolut**: importeer het afschrift (PDF uit de app of CSV-export) bij Bankmutaties. Dubbele mutaties worden overgeslagen.
- **Shopify payouts zonder API**: Finances, Payouts, Export, en importeer de CSV bij Payouts en disputes.
- **PayPal**: nog niet gekoppeld. Saldo en fees voorlopig handmatig.

### Online zetten

Werkt op Vercel met een Postgres-database (Neon of Supabase). `vercel.json` draait elk uur `/api/cron/sync`. Zet `CRON_SECRET` en `TEAM_USERS` in de omgevingsvariabelen. Met `TEAM_USERS` vraagt de browser om naam en wachtwoord.

## Tests

```bash
npm test        # rekenregels, septemberset, Revolut-import, payouts, prognose, Meta-protocol
npm run lint    # typecheck
```

De acceptatietest tegen de database draait alleen als de septemberset geladen is.
