import { PageHeader } from "@/components/PageHeader";
import { PeriodPicker } from "@/components/PeriodPicker";
import { Card, Kpi, SourceBadge, day, euro, pct, times } from "@/components/ui";
import { db } from "@/lib/db";
import { dayKey, resolvePeriod } from "@/lib/period";
import { periodFinance } from "@/finance/data";
import { budgetWarnings, marketOf } from "@/finance/meta";
import { addBudgetChange, deleteBudgetChange } from "./actions";
import { SyncWindsor } from "./SyncWindsor";

export const dynamic = "force-dynamic";

type Agg = { key: string; spend: number; clicks: number; impressions: number; purchases: number; value: number; freqWeighted: number };

function aggregate(rows: { key: string; spendCents: number; clicks: number; impressions: number; purchases: number; purchaseValueCents: number; frequency: number | null }[]) {
  const m = new Map<string, Agg>();
  for (const r of rows) {
    const a = m.get(r.key) ?? { key: r.key, spend: 0, clicks: 0, impressions: 0, purchases: 0, value: 0, freqWeighted: 0 };
    a.spend += r.spendCents;
    a.clicks += r.clicks;
    a.impressions += r.impressions;
    a.purchases += r.purchases;
    a.value += r.purchaseValueCents;
    a.freqWeighted += (r.frequency ?? 0) * r.impressions;
    m.set(r.key, a);
  }
  return [...m.values()].sort((a, b) => b.spend - a.spend);
}

function AggTable({ rows, target, label }: { rows: Agg[]; target: number; label: string }) {
  return (
    <div className="overflow-x-auto">
      <table className="data">
        <thead>
          <tr>
            <th>{label}</th>
            <th className="r">Spend</th>
            <th className="r">Aankopen</th>
            <th className="r">Omzet (Meta)</th>
            <th className="r">ROAS</th>
            <th className="r">CPC</th>
            <th className="r">CPM</th>
            <th className="r">Frequency</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => {
            const roas = r.spend ? r.value / r.spend : null;
            const freq = r.impressions ? r.freqWeighted / r.impressions : null;
            return (
              <tr key={r.key}>
                <td className="max-w-[18rem] truncate" title={r.key}>{r.key}</td>
                <td className="r">{euro(r.spend, true)}</td>
                <td className="r">{r.purchases}</td>
                <td className="r">{euro(r.value, true)}</td>
                <td className={`r font-medium ${roas !== null && roas < target ? "text-neg" : "text-good"}`}>{times(roas)}</td>
                <td className="r">{r.clicks ? euro(Math.round(r.spend / r.clicks)) : "ontbreekt"}</td>
                <td className="r">{r.impressions ? euro(Math.round((r.spend / r.impressions) * 1000)) : "ontbreekt"}</td>
                <td className={`r ${freq !== null && freq >= 2.5 ? "font-medium text-warn" : ""}`}>{freq === null ? "" : freq.toFixed(2).replace(".", ",")}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default async function MetaPage({ searchParams }: { searchParams: Promise<Record<string, string>> }) {
  const period = resolvePeriod(await searchParams, new Date(), "mtd");
  const from = new Date(`${period.fromKey}T00:00:00Z`);
  const to = new Date(`${period.toKey}T00:00:00Z`);
  const [rows, f, changes, sync] = await Promise.all([
    db.metaDaily.findMany({ where: { date: { gte: from, lte: to } } }),
    periodFinance(period),
    db.budgetChange.findMany({ orderBy: { date: "desc" }, take: 50 }),
    db.sourceSync.findUnique({ where: { source: "windsor" } }),
  ]);
  const target = f.settings.breakEvenTarget;
  const spend = rows.reduce((s, r) => s + r.spendCents, 0);
  const value = rows.reduce((s, r) => s + r.purchaseValueCents, 0);
  const campaigns = aggregate(rows.map((r) => ({ ...r, key: r.campaign })));
  const markets = aggregate(rows.map((r) => ({ ...r, key: r.market ?? marketOf(r.campaign) })));
  const warnings = budgetWarnings(changes);
  const campaignNames = [...new Set(rows.map((r) => r.campaign))].sort();

  return (
    <div className="mx-auto max-w-7xl">
      <PageHeader
        title="Meta ads"
        subtitle={
          <>
            Break-even afspraak {times(target)}, rood is eronder. Laatste sync Windsor.ai:{" "}
            {sync ? `${sync.lastAt.toLocaleString("nl-NL", { timeZone: "Europe/Amsterdam" })} (${sync.status})` : "nog niet"}.
          </>
        }
      >
        <SyncWindsor />
        <PeriodPicker period={period} basePath="/meta" />
      </PageHeader>

      <div className="mb-6 grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-6">
        <Kpi label="Spend" value={euro(spend, true)} sub={<SourceBadge source={rows.length ? "Meta" : "ontbreekt"} />} />
        <Kpi label="Betaald (bank)" value={euro(f.pnl.metaCents, true)} sub="loopt achter op spend" />
        <Kpi label="Omzet volgens Meta" value={euro(value, true)} sub={`ROAS ${times(spend ? value / spend : null)}`} />
        <Kpi label="Omzet Shopify" value={euro(f.pnl.revenueCents, true)} sub={`MER ${times(spend ? f.pnl.revenueCents / spend : null)} op spend`} tone={spend && f.pnl.revenueCents / spend < target ? "neg" : undefined} />
        <Kpi label="Meta %" value={pct(f.pnl.revenueCents ? spend / f.pnl.revenueCents : null)} sub="spend / omzet" />
        <Kpi label="Break-even" value={times(f.pnl.breakEvenRoas)} sub={`berekend, afspraak ${times(target)}`} />
      </div>

      <Card title="Per campagne" className="mb-6">
        {campaigns.length ? <AggTable rows={campaigns} target={target} label="Campagne" /> : <p className="text-sm text-ink-3">Nog geen Meta-data. Zet WINDSOR_API_KEY en klik op Ophalen.</p>}
        <p className="mt-2 text-xs text-ink-3">CPC = spend / clicks. Frequency oranje vanaf 2,5: tijd voor nieuwe creatives.</p>
      </Card>

      <Card title="Per markt" className="mb-6">
        <AggTable rows={markets} target={target} label="Markt" />
      </Card>

      <Card title="Budgetwijzigingen">
        <p className="mb-3 text-sm text-ink-2">Protocol: max 20% per ingreep, minimaal 3 tot 4 dagen ertussen, nooit twee ingrepen tegelijk.</p>
        <form action={addBudgetChange} className="mb-4 flex flex-wrap items-end gap-2 text-sm">
          <input type="date" name="date" defaultValue={dayKey(new Date())} className="input" required />
          <input name="campaign" list="campaigns" placeholder="Campagne" className="input w-60" required />
          <datalist id="campaigns">
            {campaignNames.map((c) => (
              <option key={c} value={c} />
            ))}
          </datalist>
          <input name="old" placeholder="oud budget" inputMode="decimal" className="input w-28" required />
          <input name="new" placeholder="nieuw budget" inputMode="decimal" className="input w-28" required />
          <input name="note" placeholder="notitie" className="input w-40" />
          <button className="btn">Toevoegen</button>
        </form>
        <table className="data">
          <tbody>
            {changes.map((c) => {
              const w = warnings.filter((x) => x.id === c.id);
              return (
                <tr key={c.id}>
                  <td className="whitespace-nowrap">{day(c.date)}</td>
                  <td>{c.campaign}</td>
                  <td className="r">
                    {euro(c.oldCents)} naar {euro(c.newCents)} <span className="text-ink-3">({pct(c.oldCents ? (c.newCents - c.oldCents) / c.oldCents : null, 0)})</span>
                  </td>
                  <td className="text-xs">
                    {w.map((x) => (
                      <div key={x.message} className="text-neg">
                        {x.message}
                      </div>
                    ))}
                    {c.note && <div className="text-ink-3">{c.note}</div>}
                  </td>
                  <td className="text-right">
                    <form action={deleteBudgetChange}>
                      <input type="hidden" name="id" value={c.id} />
                      <button className="text-xs text-ink-3 underline">verwijder</button>
                    </form>
                  </td>
                </tr>
              );
            })}
            {changes.length === 0 && (
              <tr>
                <td className="text-ink-3">Nog geen wijzigingen gelogd.</td>
              </tr>
            )}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
