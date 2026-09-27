import Link from "next/link";
import type { Alert } from "@/finance/alerts";

const STYLE: Record<number, { border: string; icon: string; label: string }> = {
  1: { border: "var(--neg)", icon: "●", label: "Urgent" },
  2: { border: "var(--warn)", icon: "▲", label: "Let op" },
  3: { border: "var(--text-3)", icon: "○", label: "Info" },
};

export function Alerts({ alerts }: { alerts: Alert[] }) {
  if (!alerts.length) return null;
  return (
    <div className="mb-6 space-y-2">
      {alerts.map((a) => {
        const s = STYLE[a.level];
        const body = (
          <div className="card flex gap-3 border-l-4 p-3 text-sm" style={{ borderLeftColor: s.border }}>
            <span aria-hidden style={{ color: s.border }}>
              {s.icon}
            </span>
            <div className="min-w-0">
              <div className="font-medium">
                <span className="sr-only">{s.label}: </span>
                {a.title}
              </div>
              <div className="text-ink-2">{a.body}</div>
            </div>
          </div>
        );
        return a.href ? (
          <Link key={a.title} href={a.href} className="block hover:opacity-90">
            {body}
          </Link>
        ) : (
          <div key={a.title}>{body}</div>
        );
      })}
    </div>
  );
}
