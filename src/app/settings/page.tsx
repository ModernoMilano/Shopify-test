import { PageHeader } from "@/components/PageHeader";
import { Card } from "@/components/ui";
import { db } from "@/lib/db";
import { getProfitSettings } from "@/lib/settings";
import { getFinanceSettings } from "@/finance/settings";
import { saveSettings } from "./actions";
import { SyncButton } from "./SyncButton";

export const dynamic = "force-dynamic";

const SOURCES: Record<string, string> = {
  shopify_sales: "Shopify omzet",
  shopify_payments: "Shopify Payments",
  windsor: "Meta (Windsor.ai)",
  revolut: "Revolut",
  paypal: "PayPal",
};

const e2 = (cents: number) => (cents / 100).toFixed(2).replace(".", ",");

export default async function SettingsPage() {
  const [f, p, syncs, logs] = await Promise.all([
    getFinanceSettings(),
    getProfitSettings(),
    db.sourceSync.findMany(),
    db.syncLog.findMany({ orderBy: { startedAt: "desc" }, take: 5 }),
  ]);
  const bySource = new Map(syncs.map((s) => [s.source, s]));

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <PageHeader title="Instellingen en sync" />

      <Card title="Bronnen">
        <table className="data mb-4">
          <thead>
            <tr>
              <th>Bron</th>
              <th>Laatste sync</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(SOURCES).map(([id, label]) => {
              const s = bySource.get(id);
              const stale = s && Date.now() - s.lastAt.getTime() > 24 * 3_600_000;
              return (
                <tr key={id}>
                  <td>{label}</td>
                  <td className={stale ? "text-warn" : "text-ink-2"}>
                    {s ? s.lastAt.toLocaleString("nl-NL", { timeZone: "Europe/Amsterdam", dateStyle: "medium", timeStyle: "short" }) : "nog nooit"}
                    {stale && ", langer dan 24 uur geleden"}
                  </td>
                  <td className={s?.status === "fout" ? "text-neg" : "text-ink-2"}>
                    {s ? (s.status === "ok" ? "gelukt" : "fout") : "niet gekoppeld"}
                    {s?.message && <div className="max-w-sm truncate text-xs text-ink-3" title={s.message}>{s.message}</div>}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        <SyncButton />
        <p className="mt-3 text-xs text-ink-3">
          De cron-job haalt elk uur automatisch op. Shopify Payments vereist een eigen Shopify-app met de rechten read_shopify_payments_payouts,
          read_shopify_payments_accounts en read_shopify_payments_disputes (zie README).
        </p>
        {logs.length > 0 && (
          <ul className="mt-3 space-y-0.5 text-xs text-ink-3">
            {logs.map((l) => (
              <li key={l.id}>
                {l.startedAt.toLocaleString("nl-NL", { timeZone: "Europe/Amsterdam" })}: {l.kind} {l.status} ({l.count})
              </li>
            ))}
          </ul>
        )}
      </Card>

      <form action={saveSettings} className="space-y-6">
        <Card title="Winst">
          <label className="flex items-start gap-2 text-sm">
            <input type="checkbox" name="reserveVat" defaultChecked={f.reserveVat} className="mt-1" />
            <span>
              Btw reserveren
              <span className="block text-ink-3">Standaard uit (btw fix). Aan: de btw gaat van de winst af als reservering.</span>
            </span>
          </label>
          <div className="mt-4 grid gap-3 text-sm sm:grid-cols-3">
            <label>
              Break-even ROAS afspraak
              <input name="breakEvenTarget" defaultValue={String(f.breakEvenTarget).replace(".", ",")} className="input mt-1 w-full" />
            </label>
            <label>
              Minimale bankbuffer (€)
              <input name="bankBuffer" defaultValue={e2(f.bankBufferCents)} className="input mt-1 w-full" />
            </label>
            <label>
              Software per week (€)
              <input name="softwarePerWeek" defaultValue={e2(f.softwarePerWeekCents)} className="input mt-1 w-full" />
            </label>
          </div>
        </Card>

        <Card title="Prognose">
          <div className="grid gap-3 text-sm sm:grid-cols-3">
            <label>
              Shopify verkoop per dag (€)
              <input name="salesPerDay" defaultValue={e2(f.salesPerDayCents)} className="input mt-1 w-full" />
            </label>
            <label>
              Meta per dag (€)
              <input name="metaPerDay" defaultValue={e2(f.metaPerDayCents)} className="input mt-1 w-full" />
            </label>
            <label>
              PayPal per dag (€)
              <input name="paypalPerDay" defaultValue={e2(f.paypalPerDayCents)} className="input mt-1 w-full" />
            </label>
            <label>
              Privé per week (€)
              <input name="privatePerWeek" defaultValue={e2(f.privatePerWeekCents)} className="input mt-1 w-full" />
            </label>
            <label>
              Leveranciersbetaling (€)
              <input name="supplierPayment" defaultValue={e2(f.supplierPaymentCents)} className="input mt-1 w-full" />
            </label>
            <label>
              Op dag
              <input name="supplierPaymentDay" type="number" min={0} max={30} defaultValue={f.supplierPaymentDay} className="input mt-1 w-full" />
            </label>
            <label>
              Uitbetaalpercentage nieuwe sales (%)
              <input name="payoutRatio" defaultValue={Math.round(f.payoutRatio * 100)} className="input mt-1 w-full" />
            </label>
            <label>
              Vertraging uitbetaling (dagen)
              <input name="payoutDelayDays" type="number" min={0} defaultValue={f.payoutDelayDays} className="input mt-1 w-full" />
            </label>
            <label>
              Standaard aantal dagen
              <input name="forecastDays" type="number" min={7} max={30} defaultValue={f.forecastDays} className="input mt-1 w-full" />
            </label>
          </div>
        </Card>

        <Card title="Marge per product (kostprijzen)">
          <div className="grid gap-3 text-sm sm:grid-cols-2">
            <label>
              Geschatte transactiekosten %
              <input name="paymentFeePercent" defaultValue={(p.paymentFeePercent * 100).toFixed(2).replace(".", ",")} className="input mt-1 w-full" />
            </label>
            <label>
              Plus vast per order (€)
              <input name="paymentFeeFixed" defaultValue={e2(p.paymentFeeFixedCents)} className="input mt-1 w-full" />
            </label>
          </div>
          <label className="mt-3 flex items-start gap-2 text-sm">
            <input type="checkbox" name="cogsOnRefundedItems" defaultChecked={p.cogsOnRefundedItems} className="mt-1" />
            <span>Inkoopkosten meetellen bij gerefunde items (leverancier is dan meestal al betaald)</span>
          </label>
        </Card>

        <button className="btn">Instellingen opslaan</button>
      </form>
    </div>
  );
}
