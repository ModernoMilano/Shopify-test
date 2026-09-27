import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";
import { PeriodPicker } from "@/components/PeriodPicker";
import { Stat } from "@/components/Stat";
import { buildReport } from "@/lib/report";
import { previousPeriod, resolvePeriod } from "@/lib/period";
import { formatCents, formatPct } from "@/lib/money";
import { ratio } from "@/lib/profit";
import { db } from "@/lib/db";

export const dynamic = "force-dynamic";

function delta(now: number, before: number) {
  if (!before) return null;
  const d = (now - before) / Math.abs(before);
  const arrow = d >= 0 ? "▲" : "▼";
  return (
    <span className={d >= 0 ? "text-good" : "text-neg"}>
      {arrow} {formatPct(Math.abs(d))} <span className="text-ink-3">vs vorige periode</span>
    </span>
  );
}

export default async function MarginsPage({ searchParams }: { searchParams: Promise<Record<string, string>> }) {
  const period = resolvePeriod(await searchParams);
  const [r, prev, orderCount] = await Promise.all([
    buildReport(period),
    buildReport(previousPeriod(period)),
    db.order.count(),
  ]);
  const t = r.totals;
  const missingShare = ratio(t.unitsWithoutCost, t.units);

  return (
    <div className="mx-auto max-w-7xl">
      <PageHeader title="Marge per product" subtitle={`${period.fromKey} t/m ${period.toKey}, bedragen ex btw, op basis van ingevulde kostprijzen`}>
        <PeriodPicker period={period} basePath="/marges" />
      </PageHeader>

      {orderCount === 0 && (
        <div className="card mb-6 p-4 text-sm">
          Nog geen orders in de database. Stel de Shopify-koppeling in en start een sync via{" "}
          <Link href="/settings" className="underline">
            Instellingen
          </Link>
          .
        </div>
      )}

      {missingShare !== null && missingShare > 0 && (
        <div className="card mb-6 flex flex-wrap items-center justify-between gap-3 border-l-4 p-4 text-sm" style={{ borderLeftColor: "var(--warn)" }}>
          <div>
            <span className="font-medium">Marges zijn te hoog ingeschat:</span> {t.unitsWithoutCost} van {t.units} verkochte stuks (
            {formatPct(missingShare)}) hebben nog geen kostprijs.
          </div>
          <Link href="/products?missing=1" className="btn">
            Kostprijzen invullen
          </Link>
        </div>
      )}

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <Stat label="Omzet ex btw" value={formatCents(t.revenueCents, true)} sub={delta(t.revenueCents, prev.totals.revenueCents)} />
        <Stat
          label="Bijdrage (omzet min inkoop en fees)"
          value={formatCents(t.contributionCents, true)}
          sub={`${formatPct(ratio(t.contributionCents, t.revenueCents))} van omzet`}
        />
        <Stat
          label="Transactiekosten"
          value={formatCents(t.feesCents, true)}
          sub={
            <>
              {formatPct(ratio(t.feesCents, t.revenueCents))} van omzet
              {r.estimatedFeeOrders > 0 && `, ${r.estimatedFeeOrders} geschat`}
            </>
          }
        />
        <Stat label="Waarvan wisselkoers-fees" value={formatCents(r.fxFeesCents, true)} sub="2% extra bij betalingen in GBP, PLN, NOK en andere valuta" />
      </div>

      <section className="card mt-6 overflow-hidden">
        <div className="flex items-center justify-between p-4">
          <h2 className="font-medium">Winst per product</h2>
          <span className="text-xs text-ink-3">bijdrage = omzet min inkoop min transactiekosten, vóór Meta</span>
        </div>
        <div className="overflow-x-auto">
          <table className="data">
            <thead>
              <tr>
                <th>Product</th>
                <th className="r">Stuks</th>
                <th className="r">Omzet</th>
                <th className="r">Inkoop</th>
                <th className="r">Bijdrage</th>
                <th className="r">Marge</th>
              </tr>
            </thead>
            <tbody>
              {r.products.slice(0, 25).map((p) => {
                const margin = ratio(p.contributionCents, p.revenueCents);
                return (
                  <tr key={p.productId ?? p.title}>
                    <td className="max-w-[22rem]">
                      <div className="flex items-center gap-2">
                        {p.imageUrl ? (
                          // eslint-disable-next-line @next/next/no-img-element
                          <img src={p.imageUrl} alt="" className="size-8 shrink-0 rounded object-cover" />
                        ) : (
                          <div className="size-8 shrink-0 rounded bg-surface-2" />
                        )}
                        <span className="truncate">{p.title}</span>
                        {p.unitsWithoutCost > 0 && (
                          <Link
                            href={`/products?q=${encodeURIComponent(p.title)}`}
                            className="shrink-0 rounded bg-surface-2 px-1.5 py-0.5 text-[11px] text-warn"
                          >
                            geen kostprijs
                          </Link>
                        )}
                      </div>
                    </td>
                    <td className="r">{p.units}</td>
                    <td className="r">{formatCents(p.revenueCents, true)}</td>
                    <td className="r">{formatCents(p.cogsCents, true)}</td>
                    <td className={`r ${p.contributionCents < 0 ? "text-neg" : ""}`}>{formatCents(p.contributionCents, true)}</td>
                    <td className={`r ${margin !== null && margin < 0.2 ? "text-neg" : ""}`}>
                      {p.unitsWithoutCost > 0 ? "ontbreekt" : formatPct(margin)}
                    </td>
                  </tr>
                );
              })}
              {r.products.length === 0 && (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-ink-3">
                    Geen verkopen in deze periode.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
