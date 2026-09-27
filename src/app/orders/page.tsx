import { PageHeader } from "@/components/PageHeader";
import { PeriodPicker } from "@/components/PeriodPicker";
import { orderList } from "@/lib/report";
import { resolvePeriod } from "@/lib/period";
import { formatCents, formatPct } from "@/lib/money";
import { ratio } from "@/lib/profit";

export const dynamic = "force-dynamic";

export default async function OrdersPage({ searchParams }: { searchParams: Promise<Record<string, string>> }) {
  const params = await searchParams;
  const period = resolvePeriod(params);
  const onlyLoss = params.loss === "1";
  let rows = await orderList(period);
  if (onlyLoss) rows = rows.filter((r) => r.counted && r.profit.contributionCents < 0);

  return (
    <div className="mx-auto max-w-7xl">
      <PageHeader title="Orders" subtitle="Bijdrage per order: omzet ex btw min inkoop min transactiekosten, vóór advertenties">
        <PeriodPicker period={period} basePath="/orders" />
      </PageHeader>
      <div className="mb-3 text-sm">
        <a href={`/orders?p=${period.preset}&from=${period.fromKey}&to=${period.toKey}${onlyLoss ? "" : "&loss=1"}`} className="underline text-ink-2">
          {onlyLoss ? "Toon alle orders" : "Toon alleen verliesgevende orders"}
        </a>
      </div>
      <div className="card overflow-x-auto">
        <table className="data">
          <thead>
            <tr>
              <th>Order</th>
              <th>Datum</th>
              <th>Land</th>
              <th>Status</th>
              <th className="r">Omzet</th>
              <th className="r">Inkoop</th>
              <th className="r">Fees</th>
              <th className="r">Bijdrage</th>
              <th className="r">Marge</th>
            </tr>
          </thead>
          <tbody>
            {rows.slice(0, 500).map(({ order: o, profit: p, counted }) => (
              <tr key={o.id} className={counted ? "" : "opacity-50"}>
                <td>
                  <div className="font-medium">{o.name}</div>
                  <div className="max-w-[16rem] truncate text-xs text-ink-3">
                    {o.lineItems.map((li) => `${li.quantity}× ${li.product?.title ?? li.title}`).join(", ")}
                  </div>
                </td>
                <td className="whitespace-nowrap">
                  {o.createdAt.toLocaleString("nl-NL", { timeZone: "Europe/Amsterdam", day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" })}
                </td>
                <td>
                  {o.countryCode ?? ""}
                  {o.presentmentCurrency && o.presentmentCurrency !== "EUR" && <span className="ml-1 text-xs text-ink-3">{o.presentmentCurrency}</span>}
                </td>
                <td className="text-xs text-ink-2">
                  {o.test ? "test" : o.cancelledAt ? "geannuleerd" : (o.financialStatus ?? "").toLowerCase().replace(/_/g, " ")}
                </td>
                <td className="r">{formatCents(p.revenueCents)}</td>
                <td className="r">{p.unitsWithoutCost > 0 ? <span className="text-warn">onbekend</span> : formatCents(p.cogsCents)}</td>
                <td className="r">
                  {formatCents(p.feesCents)}
                  {p.feesEstimated && <span className="text-ink-3">*</span>}
                </td>
                <td className={`r ${p.contributionCents < 0 ? "text-neg" : ""}`}>{formatCents(p.contributionCents)}</td>
                <td className="r">{p.unitsWithoutCost > 0 ? "ontbreekt" : formatPct(ratio(p.contributionCents, p.revenueCents))}</td>
              </tr>
            ))}
            {rows.length === 0 && (
              <tr>
                <td colSpan={9} className="py-8 text-center text-ink-3">
                  Geen orders in deze periode.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <p className="mt-2 text-xs text-ink-3">
        * geschatte transactiekosten (geen fee-data van Shopify Payments). Geannuleerde en testorders tellen niet mee.
        {rows.length > 500 && ` Eerste 500 van ${rows.length} orders getoond.`}
      </p>
    </div>
  );
}
