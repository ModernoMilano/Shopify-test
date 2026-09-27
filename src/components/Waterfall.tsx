import { euro } from "./ui";

type Step = { key: string; label: string; cents: number };

/** Waterval van winst naar groei van de bankrekening. Eindbalk is de som van alle stappen. */
export function Waterfall({ steps, endLabel }: { steps: Step[]; endLabel: string }) {
  const W = 800;
  const H = 280;
  const PAD = { top: 24, bottom: 56, left: 8, right: 8 };
  const all = [...steps, { key: "end", label: endLabel, cents: steps.reduce((s, x) => s + x.cents, 0) }];
  let running = 0;
  const bars = all.map((s, i) => {
    const isEnd = i === all.length - 1;
    const start = isEnd || i === 0 ? 0 : running;
    const end = isEnd ? s.cents : i === 0 ? s.cents : running + s.cents;
    if (!isEnd) running = i === 0 ? s.cents : running + s.cents;
    return { ...s, start, end, isEnd, isFirst: i === 0 };
  });
  const vals = bars.flatMap((b) => [b.start, b.end, 0]);
  const max = Math.max(...vals);
  const min = Math.min(...vals);
  const innerH = H - PAD.top - PAD.bottom;
  const y = (v: number) => PAD.top + ((max - v) / (max - min || 1)) * innerH;
  const slot = (W - PAD.left - PAD.right) / bars.length;
  const bw = Math.min(64, slot * 0.6);

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="h-auto w-full" role="img" aria-label="Van winst naar bankrekening">
      <line x1={PAD.left} x2={W - PAD.right} y1={y(0)} y2={y(0)} stroke="var(--grid)" strokeWidth={1.5} />
      {bars.map((b, i) => {
        const x = PAD.left + i * slot + (slot - bw) / 2;
        const top = y(Math.max(b.start, b.end));
        const h = Math.max(1, Math.abs(y(b.start) - y(b.end)));
        const color = b.isFirst ? "var(--c-profit)" : b.isEnd ? "var(--text)" : b.cents >= 0 ? "var(--good)" : "var(--neg)";
        return (
          <g key={b.key}>
            <rect x={x} y={top} width={bw} height={h} rx={3} fill={color} opacity={b.isFirst || b.isEnd ? 1 : 0.85} />
            {i < bars.length - 1 && (
              <line x1={x + bw} x2={x + slot} y1={y(b.end)} y2={y(b.end)} stroke="var(--text-3)" strokeDasharray="2 3" />
            )}
            <text x={x + bw / 2} y={top - 6} textAnchor="middle" fontSize="12" fill="var(--text)" className="num" fontWeight={500}>
              {b.cents > 0 && !b.isFirst && !b.isEnd ? "+" : ""}
              {euro(b.cents, true)}
            </text>
            <foreignObject x={PAD.left + i * slot} y={H - PAD.bottom + 8} width={slot} height={PAD.bottom}>
              <div style={{ fontSize: 11, lineHeight: 1.25, textAlign: "center", color: "var(--text-2)", padding: "0 2px" }}>{b.label}</div>
            </foreignObject>
          </g>
        );
      })}
    </svg>
  );
}
