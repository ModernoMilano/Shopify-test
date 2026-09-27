import { COST_COLORS, euro, pct } from "./ui";

export type CostPart = { key: string; label: string; cents: number };

/** Waar elke euro omzet naartoe gaat: gestapelde balk + legenda met bedragen en percentages. */
export function CostBar({ parts, revenueCents }: { parts: CostPart[]; revenueCents: number }) {
  const positive = parts.filter((p) => p.cents > 0);
  const total = positive.reduce((s, p) => s + p.cents, 0);
  if (total <= 0) return <p className="text-sm text-ink-3">Nog geen data in deze periode.</p>;
  return (
    <div>
      <div className="flex h-8 w-full gap-[2px] overflow-hidden rounded-md" role="img" aria-label="Verdeling van de omzet">
        {positive.map((p) => (
          <div key={p.key} title={`${p.label}: ${euro(p.cents)}`} style={{ width: `${(p.cents / total) * 100}%`, background: COST_COLORS[p.key] }} />
        ))}
      </div>
      <ul className="mt-4 grid gap-x-8 gap-y-1.5 text-sm sm:grid-cols-2">
        {parts.map((p) => (
          <li key={p.key} className="flex items-center justify-between gap-3">
            <span className="flex items-center gap-2 text-ink-2">
              <span className="inline-block size-2.5 shrink-0 rounded-sm" style={{ background: COST_COLORS[p.key] }} />
              {p.label}
            </span>
            <span className={`num whitespace-nowrap ${p.cents < 0 ? "text-neg" : ""}`}>
              {euro(p.cents, true)} <span className="text-ink-3">{pct(revenueCents ? p.cents / revenueCents : null)}</span>
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
