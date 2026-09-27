export function Stat({
  label,
  value,
  sub,
  tone,
}: {
  label: string;
  value: string;
  sub?: React.ReactNode;
  tone?: "neg" | "good";
}) {
  return (
    <div className="card p-4">
      <div className="text-sm text-ink-2">{label}</div>
      <div
        className={`num mt-1 text-2xl font-semibold tracking-tight ${
          tone === "neg" ? "text-neg" : tone === "good" ? "text-good" : ""
        }`}
      >
        {value}
      </div>
      {sub && <div className="mt-1 text-xs text-ink-3">{sub}</div>}
    </div>
  );
}
