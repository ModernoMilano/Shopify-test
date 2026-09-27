import Link from "next/link";
import { PRESETS, type Period } from "@/lib/period";

export function PeriodPicker({ period, basePath }: { period: Period; basePath: string }) {
  return (
    <div className="flex max-w-full min-w-0 flex-wrap items-center gap-2">
      <div className="flex max-w-full overflow-x-auto rounded-lg border border-line bg-surface p-0.5 text-sm">
        {PRESETS.map((p) => (
          <Link
            key={p.id}
            href={`${basePath}?p=${p.id}`}
            className={`shrink-0 rounded-md px-2.5 py-1 whitespace-nowrap ${
              period.preset === p.id ? "bg-accent text-accent-text" : "text-ink-2 hover:text-ink"
            }`}
          >
            {p.label}
          </Link>
        ))}
      </div>
      <form action={basePath} className="flex max-w-full flex-wrap items-center gap-1 text-sm">
        <input type="date" name="from" defaultValue={period.fromKey} className="input w-36" aria-label="Van" />
        <span className="text-ink-3">t/m</span>
        <input type="date" name="to" defaultValue={period.toKey} className="input w-36" aria-label="Tot en met" />
        <button className="btn btn-ghost" type="submit">
          Toon
        </button>
      </form>
    </div>
  );
}
