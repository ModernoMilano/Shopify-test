import { formatCents, formatPct } from "@/lib/money";
import type { PeriodTotals } from "@/lib/profit";

/** Waar gaat elke euro omzet naartoe? Horizontale gestapelde balk + legenda met bedragen. */
export function MoneyFlow({ t }: { t: PeriodTotals }) {
  const parts = [
    { label: "Nettowinst", cents: Math.max(t.netProfitCents, 0), color: "var(--series-1)" },
    { label: "Inkoop + verzending", cents: t.cogsCents, color: "var(--series-2)" },
    { label: "Transactiekosten", cents: t.feesCents, color: "var(--series-3)" },
    { label: "Advertenties", cents: t.adSpendCents, color: "var(--series-4)" },
    { label: "Vaste lasten", cents: t.fixedCostsCents, color: "var(--series-5)" },
  ];
  const total = parts.reduce((s, p) => s + p.cents, 0);
  if (total <= 0) return <p className="text-sm text-ink-3">Nog geen data in deze periode.</p>;

  return (
    <div>
      <div className="flex h-7 w-full gap-[2px] overflow-hidden rounded-md" role="img" aria-label="Verdeling van de omzet">
        {parts
          .filter((p) => p.cents > 0)
          .map((p) => (
            <div
              key={p.label}
              title={`${p.label}: ${formatCents(p.cents)}`}
              style={{ width: `${(p.cents / total) * 100}%`, background: p.color }}
            />
          ))}
      </div>
      <ul className="mt-4 grid grid-cols-1 gap-2 text-sm">
        {parts.map((p) => (
          <li key={p.label} className="flex items-center justify-between gap-3">
            <span className="flex items-center gap-2 text-ink-2">
              <span className="inline-block size-2.5 rounded-sm" style={{ background: p.color }} />
              {p.label}
            </span>
            <span className="num text-ink">
              {formatCents(p.cents, true)}{" "}
              <span className="text-ink-3">{formatPct(t.revenueCents ? p.cents / t.revenueCents : null)}</span>
            </span>
          </li>
        ))}
        {t.netProfitCents < 0 && (
          <li className="text-neg">
            Verlies in deze periode: {formatCents(t.netProfitCents, true)} (kosten zijn hoger dan de omzet)
          </li>
        )}
      </ul>
    </div>
  );
}
