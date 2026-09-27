# ModernoMilano Backoffice

Intern dashboard voor marges, kosten en leveranciers, gekoppeld aan Shopify.

## Wat zit erin (fase 1)

- **Dashboard**: omzet, nettowinst, bijdrage vóór marketing, ROAS en break-even ROAS, transactiekosten (incl. wisselkoers-fees), winst per dag en per product.
- **Producten & kostprijs**: inkoopprijs + verzendkosten per product, met historie (een prijswijziging raakt oude orders niet). Bulk invullen via CSV (export, invullen in Excel, import).
- **Orders**: bijdrage per order, filter op verliesgevende orders.
- **Leveranciers**, **Advertenties** (handmatig of CSV), **Vaste lasten**.
- **Shopify-sync**: producten en orders incrementeel, echte Shopify Payments-fees omgerekend naar EUR (Shopify rapporteert fees in de valuta van de klant).

## Installatie

```bash
npm install
cp .env.example .env      # vul DATABASE_URL, SHOPIFY_* en TEAM_USERS in
npx prisma db push        # maakt de tabellen aan
npm run sync -- --full    # eerste keer alles ophalen uit Shopify
npm run dev               # http://localhost:3000
```

Demo zonder Shopify: `npm run db:seed` (verzonnen data, wist de database).

### Shopify-token

Shopify admin, Settings, Apps and sales channels, Develop apps, Create an app. Admin API scopes: `read_products`, `read_orders`, `read_all_orders`. Installeer de app en zet de Admin API access token in `SHOPIFY_ADMIN_TOKEN`.

### Hosting

Werkt op Vercel met een Postgres-database (Neon of Supabase). `vercel.json` draait elk uur `/api/cron/sync`; zet `CRON_SECRET` in de omgevingsvariabelen.

## Tests

```bash
npm test        # rekenregels, valuta-omrekening, CSV, tijdzones
npm run lint    # typecheck
```
