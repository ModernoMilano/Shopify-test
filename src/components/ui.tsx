import type { Source } from "@/finance/data";

const eur = new Intl.NumberFormat("nl-NL", { style: "currency", currency: "EUR" });
const eur0 = new Intl.NumberFormat("nl-NL", { style: "currency", currency: "EUR", maximumFractionDigits: 0, minimumFractionDigits: 0 });

/** € 1.234,56 (of afgerond € 1.235) */
export function euro(cents: number | null | undefined, round = false): string {
  if (cents === null || cents === undefined || !Number.isFinite(cents)) return "ontbreekt";
  const v = round ? Math.round(cents / 100) : Math.round(cents) / 100;
  return (round ? eur0 : eur).format(v === 0 ? 0 : v);
}

export function pct(v: number | null | undefined, digits = 1): string {
  if (v === null || v === undefined || !Number.isFinite(v)) return "ontbreekt";
  return `${(v * 100).toFixed(digits).replace(".", ",")}%`;
}

export function times(v: number | null | undefined): string {
  if (v === null || v === undefined || !Number.isFinite(v)) return "ontbreekt";
  return `${v.toFixed(2).replace(".", ",")}x`;
}

const dayFmt = new Intl.DateTimeFormat("nl-NL", { weekday: "short", day: "numeric", month: "short", timeZone: "UTC" });

/** "ma 28 sep" */
export function day(d: Date | string): string {
  const date = typeof d === "string" ? new Date(`${d.slice(0, 10)}T00:00:00Z`) : d;
  return dayFmt.format(date).replace(/\./g, "");
}

export const COST_COLORS: Record<string, string> = {
  cogs: "var(--c-cogs)",
  meta: "var(--c-meta)",
  fees: "var(--c-fees)",
  chargebacks: "var(--c-chargebacks)",
  other: "var(--c-other)",
  profit: "var(--c-profit)",
  team: "var(--c-team)",
};

const SOURCE_TEXT: Record<Source, string> = {
  Shopify: "uit Shopify",
  bank: "uit bank",
  payouts: "uit payouts",
  handmatig: "handmatig",
  Meta: "uit Meta",
  ontbreekt: "ontbreekt",
};

export function SourceBadge({ source }: { source: Source }) {
  const tone =
    source === "ontbreekt"
      ? "text-neg border-neg/40"
      : source === "handmatig"
        ? "text-warn border-warn/40"
        : "text-ink-3 border-line";
  return <span className={`inline-block rounded-full border px-1.5 py-px text-[10px] leading-4 whitespace-nowrap ${tone}`}>{SOURCE_TEXT[source]}</span>;
}

export function Card({ title, children, className = "", action }: { title?: React.ReactNode; children: React.ReactNode; className?: string; action?: React.ReactNode }) {
  return (
    <section className={`card p-4 md:p-5 ${className}`}>
      {(title || action) && (
        <div className="mb-3 flex items-center justify-between gap-3">
          {title && <h2 className="font-medium">{title}</h2>}
          {action}
        </div>
      )}
      {children}
    </section>
  );
}

export function Kpi({ label, value, sub, tone }: { label: string; value: string; sub?: React.ReactNode; tone?: "neg" | "good" }) {
  return (
    <div className="card p-4">
      <div className="text-[13px] text-ink-2">{label}</div>
      <div className={`num mt-1 text-xl font-semibold tracking-tight md:text-2xl ${tone === "neg" ? "text-neg" : tone === "good" ? "text-good" : ""}`}>
        {value}
      </div>
      {sub && <div className="mt-1 text-xs text-ink-3">{sub}</div>}
    </div>
  );
}
