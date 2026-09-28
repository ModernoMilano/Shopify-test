import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";
import { PeriodPicker } from "@/components/PeriodPicker";
import { Alerts } from "@/components/Alerts";
import { DataStatus } from "@/components/DataStatus";
import { CostBar } from "@/components/CostBar";
import { LineChart } from "@/components/LineChart";
import { Card, Kpi, SourceBadge, day, euro, pct, times } from "@/components/ui";
import { resolvePeriod, eachDay } from "@/lib/period";
import { periodFinance, moneyNow } from "@/finance/data";
import { computeAlerts } from "@/finance/alerts";
import { getSetting } from "@/lib/settings";
import { db } from "@/lib/db";

export const dynamic = "force-dynamic";

export default async function Overview({ searchParams }: { searchParams: Promise<Record<string, string>> }) {
  const period = resolvePeriod(await searchParams, new Date(), "mtd");
  const [f, money] = await Promise.all([periodFinance(period), moneyNow()]);
  const alerts = await computeAlerts(f, money);
  const p = f.pnl;

  // dagelijkse Meta: spend uit Windsor als die er is, anders betaald volgens bank
  const days = eachDay(period.fromKey, period.toKey);
  const metaDaily = await db.metaDaily.groupBy({
    by: ["date"],
    where: { date: { gte: new Date(period.fromKey), lte: new Date(period.toKey) } },
    _sum: { spendCents: true },
  });
  const metaByDay = new Map<string, number>();
  if (metaDaily.length) {
    for (const m of metaDaily) metaByDay.set(m.date.toISOString().slice(0, 10), m._sum.spendCents ?? 0);
  } else {
    for (const t of f.txs.filter((t) => t.category === "meta")) {
      const k = (t.periodDate ?? t.bookedAt).toISOString().slice(0, 10);
      metaByDay.set(k, (metaByDay.get(k) ?? 0) - t.amountCents);
    }
  }
  const revByDay = new Map(f.daily.map((d) => [d.date, d.revenueCents]));
  const revenueSeries = days.map((d) => revByDay.get(d) ?? null);
  const metaSeries = days.map((d) => metaByDay.get(d) ?? (revByDay.has(d) ? 0 : null));
  const merSeries = days.map((d, i) => {
    const m = metaSeries[i];
    const r = revenueSeries[i];
    return m && r !== null ? r / m : null;
  });

  const inBank = money.availableNow;
  const notInBank = money.soon + money.locked;
  const headline =
    p.revenueCents === 0
      ? "Nog geen omzet in deze periode."
      : p.profitCents >= 0
        ? `Je verdiende ${euro(p.profitCents, true)} in deze periode.`
        : `Je maakte ${euro(-p.profitCents, true)} verlies in deze periode.`;
  const subline =
    notInBank > inBank ? "Het meeste staat nog niet op je bank." : "Het grootste deel staat al op je bank of PayPal.";

  const controlRaw = period.fromKey.startsWith("2026-08") && period.toKey.startsWith("2026-08") ? await getSetting("control.2026-08") : null;
  const control = controlRaw ? (JSON.parse(controlRaw) as { profitCents: number; revenueCents: number; note: string }) : null;

  return (
    <div className="mx-auto max-w-6xl">
      <PageHeader title="Overzicht" subtitle={`${period.preset === "custom" ? "" : `${period.label}, `}${day(period.fromKey)} t/m ${day(period.toKey)}`}>
        <PeriodPicker period={period} basePath="/" />
      </PageHeader>

      <DataStatus />

      <Alerts alerts={alerts} />

      <section className="mb-6">
        <h2 className="serif text-2xl leading-tight md:text-4xl">
          {headline} {p.revenueCents > 0 && <span className="text-ink-2 italic">{subline}</span>}
        </h2>
        <p className="mt-3 text-sm text-ink-2 md:text-base">
          Omzet {euro(p.revenueCents, true)}, {p.orders} orders, winst {euro(p.profitCents, true)}, marge {pct(p.margin)}.
          {p.mer !== null && <> Elke euro Meta leverde {euro(Math.round(p.mer * 100))} omzet op.</>}
          {f.settings.reserveVat && <> Btw ({euro(p.taxesCents, true)}) is gereserveerd.</>}
        </p>
      </section>

      {control && (
        <Card className="mb-6" title="Augustus ter controle">
          <p className="text-sm text-ink-2">
            Opgegeven: omzet {euro(control.revenueCents, true)}, winst {euro(control.profitCents, true)}. {control.note}
          </p>
        </Card>
      )}

      <Card title="Waar elke euro omzet naartoe gaat" className="mb-6">
        <CostBar
          revenueCents={p.revenueCents}
          parts={[
            { key: "cogs", label: "COGS en verzending", cents: p.cogsCents },
            { key: "meta", label: "Meta ads", cents: p.metaCents },
            { key: "fees", label: "Fees", cents: p.feesCents },
            { key: "chargebacks", label: "Chargebacks", cents: p.chargebacksCents },
            { key: "other", label: "Software en overig", cents: p.otherCents },
            { key: "profit", label: "Winst", cents: p.profitCents },
            { key: "team", label: "Team", cents: p.teamCents },
          ]}
        />
      </Card>

      <div className="grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-5">
        <Kpi label="Omzet" value={euro(p.revenueCents, true)} sub="incl. btw" />
        <Kpi label="Winst" value={euro(p.profitCents, true)} tone={p.profitCents < 0 ? "neg" : "good"} sub={`marge ${pct(p.margin)}`} />
        <Kpi label="MER" value={times(p.mer)} tone={p.mer !== null && p.mer < f.settings.breakEvenTarget ? "neg" : undefined} sub={`break-even ${times(p.breakEvenRoas)}, afspraak ${times(f.settings.breakEvenTarget)}`} />
        <Kpi label="AOV" value={euro(p.aovCents, true)} sub={`${p.orders} orders`} />
        <Kpi label="Winst per order" value={euro(p.profitPerOrderCents)} sub={`COGS per order ${euro(p.cogsPerOrderCents)}`} />
        <Kpi label="Meta %" value={pct(p.metaShare)} tone={p.metaShare !== null && p.metaShare > f.settings.metaShareLimit ? "neg" : undefined} sub="van omzet" />
        <Kpi label="COGS %" value={pct(p.cogsShare)} sub="van omzet" />
        <Kpi label="Na btw-afdracht" value={euro(p.profitAfterVatCents, true)} sub={`als ${euro(p.taxesCents, true)} btw afgedragen moet worden`} />
        <Kpi
          label="Na voorraadcorrectie"
          value={euro(p.profitAfterInventoryCents, true)}
          sub={p.inventoryIncreaseCents ? "voorraadtoename is bezit" : "voorraadwaarde nog niet ingevuld"}
        />
        <Kpi label="Geld totaal" value={euro(money.totalCents, true)} sub={<Link href="/geld" className="underline">waar staat het</Link>} />
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-5">
        <Card title="Omzet en Meta per dag" className="lg:col-span-3">
          <LineChart
            dates={days}
            series={[
              { label: "Omzet", color: "var(--text)", values: revenueSeries },
              { label: metaDaily.length ? "Meta spend" : "Meta betaald (bank)", color: "var(--c-meta)", values: metaSeries },
            ]}
          />
          {!metaDaily.length && (
            <p className="mt-2 text-xs text-ink-3">
              Meta boekt in bedragen af zodra een drempel bereikt is, dus per dag schommelt dit. Koppel Windsor.ai voor de echte dagelijkse spend.
            </p>
          )}
        </Card>
        <Card title="MER per dag" className="lg:col-span-2">
          <LineChart dates={days} format="x" series={[{ label: "MER", color: "var(--c-meta)", values: merSeries }]} refLine={{ value: f.settings.breakEvenTarget, label: `break-even ${times(f.settings.breakEvenTarget)}` }} />
        </Card>
      </div>

      <Card title="Winst en verlies" className="mt-6">
        <div className="overflow-x-auto">
          <table className="data">
            <tbody>
              {f.lines.map((l) => (
                <tr key={l.key}>
                  <td>
                    <div className="flex flex-wrap items-center gap-2">
                      {l.key !== "revenue" && <span className="inline-block size-2.5 rounded-sm" style={{ background: `var(--c-${l.key})` }} />}
                      {l.label}
                      {l.sources.map((s) => (
                        <SourceBadge key={s} source={s} />
                      ))}
                    </div>
                    {l.note && <div className="text-xs text-ink-3">{l.note}</div>}
                  </td>
                  <td className="r">{l.key === "revenue" ? euro(l.cents) : euro(-l.cents)}</td>
                  <td className="r text-ink-3">{pct(p.revenueCents ? l.cents / p.revenueCents : null)}</td>
                </tr>
              ))}
              {f.settings.reserveVat && (
                <tr>
                  <td>Btw gereserveerd</td>
                  <td className="r">{euro(-p.taxesCents)}</td>
                  <td className="r text-ink-3">{pct(p.revenueCents ? p.taxesCents / p.revenueCents : null)}</td>
                </tr>
              )}
            </tbody>
            <tfoot>
              <tr>
                <td>Winst</td>
                <td className={`r ${p.profitCents < 0 ? "text-neg" : "text-good"}`}>{euro(p.profitCents)}</td>
                <td className="r">{pct(p.margin)}</td>
              </tr>
            </tfoot>
          </table>
        </div>
        <p className="mt-3 text-xs text-ink-3">
          Privé-opnames, leningen en eigen stortingen tellen nooit mee in de winst. Btw in de omzet: {euro(p.taxesCents)} (btw fix, apart te reserveren in Instellingen).
        </p>
      </Card>
    </div>
  );
}
