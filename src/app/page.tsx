import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";
import { PeriodPicker } from "@/components/PeriodPicker";
import { Stat } from "@/components/Stat";
import { ProfitChart } from "@/components/ProfitChart";
import { MoneyFlow } from "@/components/MoneyFlow";
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

export default async function Dashboard({ searchParams }: { searchParams: Promise<Record<string, string>> }) {
  const period = resolvePeriod(await searchParams);
  const [r, prev, orderCount] = await Promise.all([
    buildReport(period),
    buildReport(previousPeriod(period)),
    db.order.count(),
  ]);
  const t = r.totals;
  const missingShare = ratio(t.unitsWithoutCost, t.units);
  const roas = ratio(t.revenueCents, t.adSpendCents);

  return (
    <div className="mx-auto max-w-7xl">
      <PageHeader title="Dashboard" subtitle={`${period.fromKey} t/m ${period.toKey} · bedragen ex btw`}>
        <PeriodPicker period={period} basePath="/" />
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
            <span className="font-medium">⚠ Winst is te hoog ingeschat:</span> {t.unitsWithoutCost} van {t.units} verkochte stuks (
            {formatPct(missingShare)}) hebben nog geen kostprijs.
          </div>
          <Link href="/products?missing=1" className="btn">
            Kostprijzen invullen
          </Link>
        </div>
      )}

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <Stat label="Omzet" value={formatCents(t.revenueCents, true)} sub={delta(t.revenueCents, prev.totals.revenueCents)} />
        <Stat
          label="Nettowinst"
          value={formatCents(t.netProfitCents, true)}
          tone={t.netProfitCents < 0 ? "neg" : undefined}
          sub={<>marge {formatPct(ratio(t.netProfitCents, t.revenueCents))} · {delta(t.netProfitCents, prev.totals.netProfitCents)}</>}
        />
        <Stat
          label="Bijdrage vóór marketing"
          value={formatCents(t.contributionCents, true)}
          sub={`${formatPct(ratio(t.contributionCents, t.revenueCents))} van omzet`}
        />
        <Stat
          label="Orders"
          value={t.orders.toLocaleString("nl-NL")}
          sub={`gem. ${formatCents(t.orders ? Math.round(t.revenueCents / t.orders) : 0)} per order`}
        />
        <Stat
          label="Advertenties"
          value={formatCents(t.adSpendCents, true)}
          sub={roas ? `ROAS ${roas.toFixed(2).replace(".", ",")} (omzet ex btw / spend)` : "nog geen spend ingevoerd"}
        />
        <Stat
          label="Break-even ROAS"
          value={r.breakEvenRoas ? r.breakEvenRoas.toFixed(2).replace(".", ",") : "–"}
          sub="onder deze ROAS kost adverteren geld"
          tone={roas && r.breakEvenRoas && roas < r.breakEvenRoas ? "neg" : undefined}
        />
        <Stat
          label="Transactiekosten"
          value={formatCents(t.feesCents, true)}
          sub={
            <>
              {formatPct(ratio(t.feesCents, t.revenueCents))} van omzet
              {r.estimatedFeeOrders > 0 && ` · ${r.estimatedFeeOrders} geschat`}
            </>
          }
        />
        <Stat
          label="Waarvan wisselkoers-fees"
          value={formatCents(r.fxFeesCents, true)}
          sub="2% extra bij betalingen in GBP, PLN, NOK, …"
        />
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-5">
        <section className="card p-4 lg:col-span-3">
          <h2 className="mb-3 font-medium">Nettowinst per dag</h2>
          <ProfitChart days={r.days} />
        </section>
        <section className="card p-4 lg:col-span-2">
          <h2 className="mb-3 font-medium">Waar gaat de omzet heen</h2>
          <MoneyFlow t={t} />
        </section>
      </div>

      <section className="card mt-6 overflow-hidden">
        <div className="flex items-center justify-between p-4">
          <h2 className="font-medium">Winst per product</h2>
          <span className="text-xs text-ink-3">bijdrage = omzet − inkoop − transactiekosten (vóór ads)</span>
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
                      {p.unitsWithoutCost > 0 ? "–" : formatPct(margin)}
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
