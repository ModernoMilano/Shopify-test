"use client";

import { useEffect, useRef, useState } from "react";

export type Series = { label: string; color: string; values: (number | null)[]; dashed?: boolean };

const H = 240;
const PAD = { top: 14, right: 12, bottom: 26, left: 64 };

function niceStep(range: number) {
  const raw = range / 4 || 1;
  const mag = 10 ** Math.floor(Math.log10(raw));
  const n = raw / mag;
  return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10) * mag;
}

const eur0 = new Intl.NumberFormat("nl-NL", { style: "currency", currency: "EUR", maximumFractionDigits: 0 });
const fmtDay = new Intl.DateTimeFormat("nl-NL", { weekday: "short", day: "numeric", month: "short", timeZone: "UTC" });

/**
 * Lijngrafiek met één as. Bedragen in centen (format "eur") of factoren (format "x").
 * Hover toont een crosshair en tooltip met alle series voor die dag.
 */
export function LineChart({
  dates,
  series,
  format = "eur",
  refLine,
  zeroLine,
  height = H,
}: {
  dates: string[];
  series: Series[];
  format?: "eur" | "x";
  refLine?: { value: number; label: string };
  zeroLine?: boolean;
  height?: number;
}) {
  const [hover, setHover] = useState<number | null>(null);
  const ref = useRef<HTMLDivElement>(null);
  const [W, setW] = useState(800);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const ro = new ResizeObserver(([entry]) => setW(Math.max(280, Math.round(entry.contentRect.width))));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  const fmt = (v: number) => (format === "eur" ? eur0.format(v / 100) : `${v.toFixed(2).replace(".", ",")}x`);
  const all = series.flatMap((s) => s.values.filter((v): v is number => v !== null));
  if (refLine) all.push(refLine.value);
  if (zeroLine) all.push(0);
  const max = Math.max(...all, 0);
  const min = Math.min(...all, 0);
  const step = niceStep(max - min);
  const top = Math.ceil(max / step) * step || step;
  const bottom = Math.floor(min / step) * step;
  const innerW = W - PAD.left - PAD.right;
  const innerH = height - PAD.top - PAD.bottom;
  const x = (i: number) => PAD.left + (dates.length <= 1 ? innerW / 2 : (i / (dates.length - 1)) * innerW);
  const y = (v: number) => PAD.top + ((top - v) / (top - bottom || 1)) * innerH;
  const ticks: number[] = [];
  for (let v = bottom; v <= top + step / 2; v += step) ticks.push(v);
  const labelEvery = Math.max(1, Math.ceil(dates.length / Math.max(2, Math.floor(innerW / 90))));

  const path = (vals: (number | null)[]) => {
    let d = "";
    vals.forEach((v, i) => {
      if (v === null) return;
      d += `${d && vals[i - 1] !== null ? "L" : "M"}${x(i).toFixed(1)},${y(v).toFixed(1)} `;
    });
    return d;
  };

  if (!dates.length) return <p className="py-10 text-center text-sm text-ink-3">Geen data in deze periode.</p>;

  return (
    <div className="relative" ref={ref}>
      {series.length > 1 && (
        <div className="mb-2 flex flex-wrap gap-4 text-xs text-ink-2">
          {series.map((s) => (
            <span key={s.label} className="flex items-center gap-1.5">
              <span className="inline-block h-0.5 w-4 rounded" style={{ background: s.color }} />
              {s.label}
            </span>
          ))}
        </div>
      )}
      <svg
        viewBox={`0 0 ${W} ${height}`}
        width={W}
        height={height}
        className="block h-auto w-full touch-none"
        role="img"
        onPointerMove={(ev) => {
          const r = (ev.currentTarget as SVGSVGElement).getBoundingClientRect();
          const px = ((ev.clientX - r.left) / r.width) * W;
          const i = Math.round(((px - PAD.left) / innerW) * (dates.length - 1));
          setHover(Math.max(0, Math.min(dates.length - 1, i)));
        }}
        onPointerLeave={() => setHover(null)}
      >
        {ticks.map((t) => (
          <g key={t}>
            <line x1={PAD.left} x2={W - PAD.right} y1={y(t)} y2={y(t)} stroke="var(--grid)" />
            <text x={PAD.left - 8} y={y(t)} dy="0.32em" textAnchor="end" fontSize="11" fill="var(--text-3)" className="num">
              {fmt(t)}
            </text>
          </g>
        ))}
        {zeroLine && <line x1={PAD.left} x2={W - PAD.right} y1={y(0)} y2={y(0)} stroke="var(--neg)" strokeDasharray="4 4" strokeWidth={1.5} />}
        {refLine && (
          <g>
            <line x1={PAD.left} x2={W - PAD.right} y1={y(refLine.value)} y2={y(refLine.value)} stroke="var(--text-3)" strokeDasharray="4 4" />
            <text x={W - PAD.right} y={y(refLine.value) - 5} textAnchor="end" fontSize="11" fill="var(--text-2)">
              {refLine.label}
            </text>
          </g>
        )}
        {dates.map((d, i) =>
          i % labelEvery === 0 ? (
            <text key={d} x={x(i)} y={height - 6} textAnchor="middle" fontSize="11" fill="var(--text-3)">
              {fmtDay.format(new Date(`${d}T00:00:00Z`)).replace(/\./g, "")}
            </text>
          ) : null,
        )}
        {series.map((s) => (
          <path key={s.label} d={path(s.values)} fill="none" stroke={s.color} strokeWidth={2} strokeLinejoin="round" strokeLinecap="round" strokeDasharray={s.dashed ? "5 4" : undefined} />
        ))}
        {hover !== null && (
          <g>
            <line x1={x(hover)} x2={x(hover)} y1={PAD.top} y2={height - PAD.bottom} stroke="var(--text-3)" strokeWidth={1} />
            {series.map((s) =>
              s.values[hover] !== null ? (
                <circle key={s.label} cx={x(hover)} cy={y(s.values[hover]!)} r={4.5} fill={s.color} stroke="var(--surface)" strokeWidth={2} />
              ) : null,
            )}
          </g>
        )}
      </svg>
      {hover !== null && (
        <div
          className="card pointer-events-none absolute top-8 z-10 min-w-44 p-2.5 text-xs shadow-lg"
          style={{ left: `${Math.min(Math.max((x(hover) / W) * 100 - 10, 0), 62)}%` }}
        >
          <div className="mb-1 font-medium">{fmtDay.format(new Date(`${dates[hover]}T00:00:00Z`)).replace(/\./g, "")}</div>
          {series.map((s) => (
            <div key={s.label} className="flex items-center justify-between gap-3 text-ink-2">
              <span className="flex items-center gap-1.5">
                <span className="inline-block size-2 rounded-full" style={{ background: s.color }} />
                {s.label}
              </span>
              <span className="num text-ink">{s.values[hover] === null ? "ontbreekt" : fmt(s.values[hover]!)}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
