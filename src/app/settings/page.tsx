import { PageHeader } from "@/components/PageHeader";
import { db } from "@/lib/db";
import { getProfitSettings } from "@/lib/settings";
import { shopifyConfigured } from "@/lib/shopify";
import { saveSettings } from "./actions";
import { SyncButton } from "./SyncButton";

export const dynamic = "force-dynamic";

export default async function SettingsPage() {
  const [s, logs, counts] = await Promise.all([
    getProfitSettings(),
    db.syncLog.findMany({ orderBy: { startedAt: "desc" }, take: 10 }),
    Promise.all([db.product.count(), db.order.count()]),
  ]);
  const configured = shopifyConfigured();

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <PageHeader title="Instellingen" />

      <section className="card p-4">
        <h2 className="font-medium">Shopify-koppeling</h2>
        <p className="mt-1 mb-3 text-sm text-ink-2">
          {configured ? (
            <>
              Verbonden met <code>{process.env.SHOPIFY_STORE_DOMAIN}</code> · {counts[0]} producten, {counts[1]} orders in de database.
              Een normale sync haalt alleen wijzigingen op; de cron-job doet dit automatisch elk uur.
            </>
          ) : (
            <>
              Niet ingesteld. Zet <code>SHOPIFY_STORE_DOMAIN</code> en <code>SHOPIFY_ADMIN_TOKEN</code> in de omgevingsvariabelen (zie README).
            </>
          )}
        </p>
        <SyncButton disabled={!configured} />
        {logs.length > 0 && (
          <table className="data mt-4">
            <thead>
              <tr>
                <th>Gestart</th>
                <th>Soort</th>
                <th>Status</th>
                <th className="r">Aantal</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((l) => (
                <tr key={l.id}>
                  <td>{l.startedAt.toLocaleString("nl-NL", { timeZone: "Europe/Amsterdam" })}</td>
                  <td>{l.kind}</td>
                  <td className={l.status === "error" ? "text-neg" : ""} title={l.message ?? ""}>
                    {l.status}
                    {l.message && <div className="max-w-xs truncate text-xs">{l.message}</div>}
                  </td>
                  <td className="r">{l.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <form action={saveSettings} className="card space-y-4 p-4">
        <h2 className="font-medium">Winstberekening</h2>
        <p className="text-sm text-ink-2">
          Voor Shopify Payments worden de echte fees uit Shopify gebruikt. Deze schatting geldt alleen voor orders zonder fee-data
          (bv. PayPal, Klarna).
        </p>
        <div className="grid gap-3 sm:grid-cols-3">
          <label className="text-sm">
            Transactiekosten %
            <input name="paymentFeePercent" defaultValue={(s.paymentFeePercent * 100).toFixed(2)} inputMode="decimal" className="input mt-1 w-full" />
          </label>
          <label className="text-sm">
            + vast per order (€)
            <input name="paymentFeeFixed" defaultValue={(s.paymentFeeFixedCents / 100).toFixed(2)} inputMode="decimal" className="input mt-1 w-full" />
          </label>
          <label className="text-sm">
            Btw-tarief voor marge/stuk %
            <input name="vatRate" defaultValue={(s.vatRate * 100).toFixed(0)} inputMode="decimal" className="input mt-1 w-full" />
          </label>
        </div>
        <label className="flex items-start gap-2 text-sm">
          <input type="checkbox" name="cogsOnRefundedItems" defaultChecked={s.cogsOnRefundedItems} className="mt-1" />
          <span>
            Inkoopkosten meetellen bij gerefunde items
            <span className="block text-ink-3">
              Aan laten bij dropshipping: de leverancier is meestal al betaald als de klant zijn geld terugkrijgt.
            </span>
          </span>
        </label>
        <button className="btn">Opslaan</button>
      </form>
    </div>
  );
}
