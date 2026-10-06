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

## Creative engine

Instagram-content in de stijl van Zegna, Loro Piana, Cucinelli en Boggi, met uitsluitend kleding uit de eigen winkel. Zie [`creative-engine/README.md`](creative-engine/README.md); Claude gebruikt de skill in `.claude/skills/creative-engine/`.

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

## Wat automatisch gaat en wat niet

| Bron | Hoe | Wat |
|---|---|---|
| Shopify | automatisch, elk uur | dagomzet, orders, payouts, pending, reserve (afgeleid uit alle payouts), disputes |
| Meta | automatisch via Windsor.ai | spend, clicks, aankopen, omzet per campagne en markt |
| PayPal | automatisch via de PayPal API | verkopen, fees, opnames, saldo |
| Revolut | **jij uploadt het afschrift** | alle bankmutaties; worden automatisch ingedeeld |

Het overzicht laat bovenaan zien hoe actueel elke bron is en vanaf welke datum er een bankafschrift nodig is, met de uploadknop erbij. Een afschrift mag elke periode beslaan; overlap wordt overgeslagen. Mutaties die het systeem niet herkent wijs je één keer toe met "regel", daarna gaat het automatisch.

## Online zetten (eenmalig, ongeveer 20 minuten)

1. **Database**: maak een gratis project op neon.tech en kopieer de connection string (`DATABASE_URL`).
2. **Shopify**: maak op dev.shopify.com een app, geef de scopes uit `.env.example`, installeer hem op je winkel en kopieer Client ID en Secret.
3. **Windsor.ai**: kopieer je API key (onboard.windsor.ai).
4. **PayPal**: Live-app met Transaction Search (developer.paypal.com). Client ID en Secret.
5. **Vercel**: vercel.com, New Project, kies deze GitHub-repo. Zet bij Environment Variables alle waarden uit `.env.example`. Deploy. De tabellen worden bij de deploy automatisch aangemaakt.
6. **Elk uur ophalen**: zet in GitHub (Settings, Secrets and variables, Actions) `DASHBOARD_URL` (je Vercel-adres) en `CRON_SECRET`. De workflow `Data ophalen` draait dan elk uur; Vercel zelf haalt daarnaast één keer per dag op.
7. Open het dashboard, log in met `TEAM_USERS`, upload je laatste Revolut-afschrift. Klaar.

Sleutels horen alleen in Vercel en GitHub Secrets, nooit in de code of in een chat.

### Handmatig (optioneel)

- **Shopify payouts zonder API**: Finances, Payouts, Export, en importeer de CSV bij Payouts en disputes.
- **Handmatige invoer**: alleen nog voor wat nergens anders staat, zoals teamkosten die niet via Revolut lopen, openstaande leveranciersfacturen of voorraadwaarde.

## Tests

```bash
npm test        # rekenregels, septemberset, Revolut-import, payouts, prognose, Meta-protocol
npm run lint    # typecheck
```

De acceptatietest tegen de database draait alleen als de septemberset geladen is.
