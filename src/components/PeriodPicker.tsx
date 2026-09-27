import Link from "next/link";
import { PRESETS, type Period } from "@/lib/period";

export function PeriodPicker({ period, basePath }: { period: Period; basePath: string }) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      <div className="flex flex-wrap rounded-lg border border-line bg-surface p-0.5 text-sm">
        {PRESETS.map((p) => (
          <Link
            key={p.id}
            href={`${basePath}?p=${p.id}`}
            className={`rounded-md px-2.5 py-1 ${
              period.preset === p.id ? "bg-accent text-accent-text" : "text-ink-2 hover:text-ink"
            }`}
          >
            {p.label}
          </Link>
        ))}
      </div>
      <form action={basePath} className="flex items-center gap-1 text-sm">
        <input type="date" name="from" defaultValue={period.fromKey} className="input" aria-label="Van" />
        <span className="text-ink-3">–</span>
        <input type="date" name="to" defaultValue={period.toKey} className="input" aria-label="Tot en met" />
        <button className="btn btn-ghost" type="submit">
          Toon
        </button>
      </form>
    </div>
  );
}
