"use client";

import { useState } from "react";
import type { DayRow } from "@/lib/report";
import { formatCents } from "@/lib/money";

const W = 800;
const H = 220;
const PAD = { top: 12, right: 8, bottom: 24, left: 56 };

function niceStep(range: number) {
  const raw = range / 4;
  const mag = 10 ** Math.floor(Math.log10(raw || 1));
  const n = raw / mag;
  return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10) * mag;
}

/** Nettowinst per dag: staven boven nul in blauw, onder nul in rood. */
export function ProfitChart({ days }: { days: DayRow[] }) {
  const [hover, setHover] = useState<number | null>(null);
  const values = days.map((d) => d.netProfitCents);
  const max = Math.max(0, ...values);
  const min = Math.min(0, ...values);
  const step = niceStep(max - min || 100);
  const top = Math.ceil(max / step) * step || step;
  const bottom = Math.floor(min / step) * step;
  const innerW = W - PAD.left - PAD.right;
  const innerH = H - PAD.top - PAD.bottom;
  const y = (v: number) => PAD.top + ((top - v) / (top - bottom)) * innerH;
  const slot = innerW / Math.max(days.length, 1);
  const barW = Math.max(2, Math.min(28, slot - 2));
  const ticks: number[] = [];
  for (let v = bottom; v <= top + 1; v += step) ticks.push(v);
  const labelEvery = Math.ceil(days.length / 8);
  const h = hover !== null ? days[hover] : null;

  return (
    <div className="relative">
      <svg viewBox={`0 0 ${W} ${H}`} className="h-auto w-full" role="img" aria-label="Nettowinst per dag">
        {ticks.map((t) => (
          <g key={t}>
            <line x1={PAD.left} x2={W - PAD.right} y1={y(t)} y2={y(t)} stroke="var(--grid)" strokeWidth={t === 0 ? 1.5 : 1} />
            <text x={PAD.left - 8} y={y(t)} dy="0.32em" textAnchor="end" fontSize="11" fill="var(--text-3)" className="num">
              {formatCents(t, true)}
            </text>
          </g>
        ))}
        {days.map((d, i) => {
          const v = d.netProfitCents;
          const x = PAD.left + i * slot + (slot - barW) / 2;
          const y0 = y(0);
          const y1 = y(v);
          const hgt = Math.max(Math.abs(y1 - y0), v === 0 ? 0 : 1);
          const r = Math.min(4, barW / 2, hgt);
          const pos = v >= 0;
          // afgeronde datakant, vlak op de nullijn
          const path = pos
            ? `M${x},${y0} V${y1 + r} Q${x},${y1} ${x + r},${y1} H${x + barW - r} Q${x + barW},${y1} ${x + barW},${y1 + r} V${y0} Z`
            : `M${x},${y0} V${y0 + hgt - r} Q${x},${y0 + hgt} ${x + r},${y0 + hgt} H${x + barW - r} Q${x + barW},${y0 + hgt} ${x + barW},${y0 + hgt - r} V${y0} Z`;
          return (
            <g key={d.day}>
              {hgt > 0 && (
                <path d={path} fill={pos ? "var(--series-1)" : "var(--neg)"} opacity={hover === null || hover === i ? 1 : 0.45} />
              )}
              {i % labelEvery === 0 && (
                <text x={x + barW / 2} y={H - 6} textAnchor="middle" fontSize="11" fill="var(--text-3)">
                  {d.day.slice(8, 10)}-{d.day.slice(5, 7)}
                </text>
              )}
              <rect
                x={PAD.left + i * slot}
                y={PAD.top}
                width={slot}
                height={innerH}
                fill="transparent"
                onMouseEnter={() => setHover(i)}
                onMouseLeave={() => setHover(null)}
              />
            </g>
          );
        })}
      </svg>
      {h && hover !== null && (
        <div
          className="card pointer-events-none absolute top-2 z-10 w-56 p-3 text-xs shadow-lg"
          style={{
            left: `${Math.min(Math.max(((PAD.left + hover * slot) / W) * 100, 0), 70)}%`,
          }}
        >
          <div className="mb-1.5 font-medium text-ink">
            {new Date(h.day).toLocaleDateString("nl-NL", { weekday: "short", day: "numeric", month: "short" })} · {h.orders} orders
          </div>
          {[
            ["Omzet (ex btw)", h.revenueCents],
            ["Inkoop + verzending", -h.cogsCents],
            ["Transactiekosten", -h.feesCents],
            ["Advertenties", -h.adSpendCents],
            ["Vaste lasten", -h.fixedCostsCents],
          ].map(([label, v]) => (
            <div key={label as string} className="flex justify-between text-ink-2">
              <span>{label}</span>
              <span className="num">{formatCents(v as number)}</span>
            </div>
          ))}
          <div className="mt-1 flex justify-between border-t border-line pt-1 font-medium text-ink">
            <span>Nettowinst</span>
            <span className="num">{formatCents(h.netProfitCents)}</span>
          </div>
        </div>
      )}
    </div>
  );
}
