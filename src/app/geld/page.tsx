import { PageHeader } from "@/components/PageHeader";
import { Card, Kpi, SourceBadge, day, euro, pct } from "@/components/ui";
import { moneyNow, type Source } from "@/finance/data";
import { chargebackHistory } from "@/finance/alerts";
import { db } from "@/lib/db";

export const dynamic = "force-dynamic";

export default async function MoneyPage() {
  const [m, cb, lastPayout, loans, loanTxs] = await Promise.all([
    moneyNow(),
    chargebackHistory(),
    db.shopifyPayout.findFirst({ where: { chargesCents: { not: null } }, orderBy: { payoutDate: "desc" } }),
    db.loan.findMany({ where: { active: true } }),
    db.bankTransaction.findMany({ where: { category: "loan" }, orderBy: { bookedAt: "asc" } }),
  ]);
  const p = m.position;
  const src = (s: string | undefined): Source => (s === "Shopify" || s === "PayPal" ? s : "handmatig");
  const shopifySrc = src(m.snapshot?.shopifySource);
  const parts = [
    { key: "bank", label: "Bank (Revolut)", cents: p.bankCents, when: "Nu beschikbaar", color: "var(--text)", locked: false, source: m.bankSource },
    { key: "paypal", label: "PayPal", cents: p.paypalCents, when: "Nu beschikbaar", color: "var(--series-1)", locked: false, source: src(m.snapshot?.paypalSource) },
    {
      key: "payout",
      label: "Shopify payout ingepland",
      cents: p.payoutScheduledCents,
      when: m.snapshot?.payoutScheduledDate ? day(m.snapshot.payoutScheduledDate) : "Eerstvolgende werkdag",
      color: "var(--series-3)",
      locked: false,
      source: shopifySrc,
    },
    { key: "pending", label: "Shopify pending", cents: p.pendingCents, when: "Komende werkdagen", color: "var(--series-4)", locked: false, source: shopifySrc },
    { key: "hold", label: "Shopify reserve (hold)", cents: p.holdCents, when: "Op slot", color: "var(--series-2)", locked: true, source: src(m.snapshot?.holdSource) },
  ];
  const total = m.totalCents;
  const reservePct =
    lastPayout?.chargesCents && lastPayout.reservedFundsCents ? -lastPayout.reservedFundsCents / lastPayout.chargesCents : null;
  // leningen uit de bank: ontvangen (+) en aflossingen (-) per geldverstrekker
  const byLender = new Map<string, { name: string; since: Date; receivedCents: number; repaidCents: number }>();
  for (const t of loanTxs) {
    const name = t.description.replace(/^(Betaling van|To)\s+/i, "").trim().toUpperCase();
    const row = byLender.get(name) ?? { name, since: t.bookedAt, receivedCents: 0, repaidCents: 0 };
    if (t.amountCents > 0) row.receivedCents += t.amountCents;
    else row.repaidCents += -t.amountCents;
    if (t.bookedAt < row.since) row.since = t.bookedAt;
    byLender.set(name, row);
  }
  const lenders = [...byLender.values()].map((l) => ({
    ...l,
    openCents: l.receivedCents - l.repaidCents,
    schedule: loans.find((x) => x.lender.toUpperCase() === l.name)?.schedule ?? null,
  }));
  const debt = lenders.reduce((s, l) => s + l.openCents, 0);

  return (
    <div className="mx-auto max-w-5xl">
      <PageHeader
        title="Waar mijn geld staat"
        subtitle={
          m.snapshot
            ? `Shopify en PayPal: stand van ${m.snapshot.takenAt.toLocaleString("nl-NL", { timeZone: "Europe/Amsterdam", dateStyle: "medium", timeStyle: "short" })}. Bank: laatste afschrift t/m ${m.bankDate ? day(m.bankDate) : "ontbreekt"}.`
            : "Nog geen stand van Shopify en PayPal. Die komt automatisch zodra Shopify en PayPal gekoppeld zijn."
        }
      />

      <div className="mb-6 grid grid-cols-2 gap-3 md:grid-cols-4">
        <Kpi label="Totaal" value={euro(total, true)} />
        <Kpi label="Direct beschikbaar" value={euro(m.availableNow, true)} sub="bank en PayPal" tone="good" />
        <Kpi label="Binnenkort" value={euro(m.soon, true)} sub="payout en pending" />
        <Kpi label="Op slot" value={euro(m.locked, true)} sub="Shopify reserve" tone="neg" />
      </div>

      <Card title="Verdeling" className="mb-6">
        <div className="flex h-10 w-full gap-[2px] overflow-hidden rounded-md" role="img" aria-label="Verdeling van je geld">
          {parts
            .filter((x) => x.cents > 0)
            .map((x) => (
              <div key={x.key} className="relative" style={{ width: `${(x.cents / total) * 100}%`, background: x.color }} title={`${x.label}: ${euro(x.cents)}`}>
                {x.locked && <div className="hatched absolute inset-0 text-[var(--surface)]" />}
              </div>
            ))}
        </div>
        <div className="mt-4 overflow-x-auto">
          <table className="data">
            <thead>
              <tr>
                <th>Plek</th>
                <th className="r">Bedrag</th>
                <th className="r">Aandeel</th>
                <th>Beschikbaar</th>
              </tr>
            </thead>
            <tbody>
              {parts.map((x) => (
                <tr key={x.key}>
                  <td>
                    <div className="flex items-center gap-2">
                      <span className={`inline-block size-3 rounded-sm ${x.locked ? "relative overflow-hidden" : ""}`} style={{ background: x.color }}>
                        {x.locked && <span className="hatched absolute inset-0 text-[var(--surface)]" />}
                      </span>
                      {x.label}
                      <SourceBadge source={x.source} />
                    </div>
                  </td>
                  <td className="r">{euro(x.cents)}</td>
                  <td className="r text-ink-3">{pct(total ? x.cents / total : null)}</td>
                  <td className={x.locked ? "text-neg" : "text-ink-2"}>{x.when}</td>
                </tr>
              ))}
            </tbody>
            <tfoot>
              <tr>
                <td>Totaal</td>
                <td className="r">{euro(total)}</td>
                <td />
                <td />
              </tr>
            </tfoot>
          </table>
        </div>
        <p className="mt-3 text-xs text-ink-3">De ingeplande payout zit niet in pending en wordt apart geteld.</p>
      </Card>

      <Card title="Shopify reserve (NDRP)" className="mb-6">
        <div className="grid gap-4 sm:grid-cols-3">
          <div>
            <div className="text-sm text-ink-2">Vastgehouden</div>
            <div className="num text-xl font-semibold">{euro(p.holdCents)}</div>
            <div className="text-xs text-ink-3">{reservePct !== null ? `${pct(reservePct)} van de charges in de laatste payout` : "percentage per payout: importeer payouts"}</div>
          </div>
          <div>
            <div className="text-sm text-ink-2">Chargeback rate (90 dagen)</div>
            <div className={`num text-xl font-semibold ${cb.current !== null && cb.current >= 0.01 ? "text-neg" : ""}`}>{cb.hasData ? pct(cb.current, 2) : "ontbreekt"}</div>
            <div className="text-xs text-ink-3">{cb.hasData ? "exit: 30 dagen achter elkaar onder 1%" : "Koppel Shopify Payments (disputes) en sync orders"}</div>
          </div>
          <div>
            <div className="text-sm text-ink-2">Dagen onder 1%</div>
            <div className="num text-xl font-semibold">{cb.hasData ? `${cb.daysBelow1} van 30` : "ontbreekt"}</div>
            <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-surface-2">
              <div className="h-full rounded-full" style={{ width: `${Math.min(100, (cb.daysBelow1 / 30) * 100)}%`, background: "var(--good)" }} />
            </div>
          </div>
        </div>
      </Card>

      {debt > 0 && (
        <Card title="Openstaande schuld" action={<SourceBadge source="bank" />}>
          <ul className="text-sm">
            {lenders.map((l) => (
              <li key={l.name} className="flex justify-between border-b border-line py-1.5 last:border-0">
                <span>
                  Lening {l.name}, sinds {day(l.since)}
                  {l.repaidCents > 0 && <span className="text-ink-3">, al {euro(l.repaidCents)} afgelost</span>}
                  {l.schedule && <span className="text-ink-3">, aflossing: {l.schedule}</span>}
                </span>
                <span className="num">{euro(l.openCents)}</span>
              </li>
            ))}
          </ul>
          <p className="mt-2 text-xs text-ink-3">
            Uit de bankmutaties met categorie Lening: ontvangen min afgelost. Een lening is geen omzet. Dit geld staat wel op je bank, maar moet terug.
          </p>
        </Card>
      )}
    </div>
  );
}
