"use client";

import { useMemo, useState } from "react";
import { forecast, type ForecastSettings } from "@/finance/calculations";
import { LineChart } from "@/components/LineChart";

const eur = new Intl.NumberFormat("nl-NL", { style: "currency", currency: "EUR", maximumFractionDigits: 0 });
const e = (c: number) => eur.format(c / 100);
const fmtDay = new Intl.DateTimeFormat("nl-NL", { weekday: "short", day: "numeric", month: "short", timeZone: "UTC" });
const d = (k: string) => fmtDay.format(new Date(`${k}T00:00:00Z`)).replace(/\./g, "");

type Key = keyof ForecastSettings;

const SLIDERS: { key: Key; label: string; max: number; step: number; suffix?: string }[] = [
  { key: "salesPerDayCents", label: "Shopify verkoop per dag", max: 1_000_000, step: 10_000 },
  { key: "metaPerDayCents", label: "Meta per dag", max: 500_000, step: 5_000 },
  { key: "paypalPerDayCents", label: "PayPal per dag", max: 150_000, step: 5_000 },
  { key: "privatePerWeekCents", label: "Privé per week", max: 500_000, step: 10_000 },
  { key: "softwarePerWeekCents", label: "Software per week", max: 150_000, step: 5_000 },
  { key: "supplierPaymentCents", label: "Leveranciersbetaling", max: 2_000_000, step: 10_000 },
  { key: "bufferCents", label: "Minimale buffer", max: 1_000_000, step: 10_000 },
];

export function ForecastView({ base }: { base: ForecastSettings }) {
  const [s, setS] = useState<ForecastSettings>(base);
  const set = (k: Key, v: number | string | undefined) => setS((prev) => ({ ...prev, [k]: v }));

  const withSales = useMemo(() => forecast(s), [s]);
  const readyOnly = useMemo(() => forecast({ ...s, salesPerDayCents: 0, paypalPerDayCents: 0 }), [s]);
  const dates = withSales.rows.map((r) => r.date);

  return (
    <div className="grid gap-6 lg:grid-cols-[17rem_minmax(0,1fr)]">
      <div className="card space-y-4 p-4">
        <div className="flex gap-1 rounded-lg border border-line p-0.5 text-sm">
          {[7, 14, 30].map((n) => (
            <button key={n} onClick={() => set("days", n)} className={`flex-1 rounded-md px-2 py-1 ${s.days === n ? "bg-accent text-accent-text" : "text-ink-2"}`}>
              {n} dagen
            </button>
          ))}
        </div>
        {SLIDERS.map((sl) => (
          <label key={sl.key} className="block text-sm">
            <div className="flex justify-between">
              <span className="text-ink-2">{sl.label}</span>
              <span className="num font-medium">{e(s[sl.key] as number)}</span>
            </div>
            <input type="range" min={0} max={sl.max} step={sl.step} value={s[sl.key] as number} onChange={(ev) => set(sl.key, Number(ev.target.value))} className="w-full accent-[var(--text)]" />
          </label>
        ))}
        <label className="block text-sm">
          <div className="flex justify-between">
            <span className="text-ink-2">Uitbetaald deel nieuwe sales</span>
            <span className="num font-medium">{Math.round(s.payoutRatio * 100)}%</span>
          </div>
          <input type="range" min={0.6} max={1} step={0.01} value={s.payoutRatio} onChange={(ev) => set("payoutRatio", Number(ev.target.value))} className="w-full accent-[var(--text)]" />
        </label>
        <label className="block text-sm">
          <span className="text-ink-2">Dag leveranciersbetaling</span>
          <select className="input mt-1 w-full" value={s.supplierPaymentDay} onChange={(ev) => set("supplierPaymentDay", Number(ev.target.value))}>
            <option value={0}>Geen</option>
            {withSales.rows.map((r) => (
              <option key={r.day} value={r.day}>
                Dag {r.day}, {d(r.date)}
              </option>
            ))}
          </select>
        </label>
        <fieldset className="space-y-2 border-t border-line pt-3 text-sm">
          <legend className="text-ink-2">Vrijgave reserve</legend>
          <div className="flex gap-2">
            <input type="date" className="input flex-1" value={s.reserveReleaseDate ?? ""} onChange={(ev) => set("reserveReleaseDate", ev.target.value || undefined)} aria-label="Datum vrijgave" />
            <input
              type="number"
              className="input w-28"
              placeholder="bedrag"
              value={s.reserveReleaseCents ? s.reserveReleaseCents / 100 : ""}
              onChange={(ev) => set("reserveReleaseCents", ev.target.value ? Math.round(Number(ev.target.value) * 100) : undefined)}
              aria-label="Bedrag vrijgave"
            />
          </div>
        </fieldset>
        <label className="block text-sm">
          <span className="text-ink-2">Teamkosten en overig per dag (€)</span>
          <input
            type="number"
            className="input mt-1 w-full"
            value={s.extraPerDayCents ? s.extraPerDayCents / 100 : ""}
            onChange={(ev) => set("extraPerDayCents", ev.target.value ? Math.round(Number(ev.target.value) * 100) : undefined)}
          />
        </label>
      </div>

      <div className="min-w-0 space-y-6">
        <div className="grid gap-3 sm:grid-cols-2">
          {[
            { name: "Sales lopen door", f: withSales },
            { name: "Alleen wat al klaarstaat", f: readyOnly },
          ].map(({ name, f }) => (
            <div key={name} className={`card p-4 ${f.belowZero || f.belowBuffer ? "border-l-4" : ""}`} style={f.belowZero || f.belowBuffer ? { borderLeftColor: "var(--neg)" } : undefined}>
              <div className="text-sm font-medium">{name}</div>
              <dl className="mt-2 grid grid-cols-2 gap-y-1 text-sm">
                <dt className="text-ink-2">Saldo na {Math.min(7, s.days)} dagen</dt>
                <dd className="num text-right font-semibold">{e(f.balanceAfter7Cents)}</dd>
                <dt className="text-ink-2">Laagste punt</dt>
                <dd className={`num text-right ${f.belowZero || f.belowBuffer ? "font-semibold text-neg" : ""}`}>
                  {e(f.lowest.balanceCents)} <span className="text-xs text-ink-3">{d(f.lowest.date)}</span>
                </dd>
                <dt className="text-ink-2">Eindsaldo</dt>
                <dd className="num text-right">{e(f.endBalanceCents)}</dd>
                <dt className="text-ink-2">Verschil met nu</dt>
                <dd className={`num text-right ${f.changeCents < 0 ? "text-neg" : "text-good"}`}>{e(f.changeCents)}</dd>
              </dl>
              {(f.belowZero || f.belowBuffer) && <p className="mt-2 text-xs text-neg">{f.belowZero ? "Saldo komt onder nul." : "Saldo komt onder je buffer."}</p>}
            </div>
          ))}
        </div>

        <div className="card p-4">
          <LineChart
            dates={dates}
            zeroLine
            series={[
              { label: "Sales lopen door", color: "var(--c-profit)", values: withSales.rows.map((r) => r.balanceCents) },
              { label: "Alleen wat al klaarstaat", color: "var(--c-meta)", values: readyOnly.rows.map((r) => r.balanceCents), dashed: true },
            ]}
          />
        </div>

        <div className="card overflow-x-auto">
          <table className="data">
            <thead>
              <tr>
                <th>Dag</th>
                <th className="r">Shopify in</th>
                <th className="r">PayPal in</th>
                <th className="r">Meta</th>
                <th className="r">Leverancier</th>
                <th className="r">Privé, software</th>
                <th className="r">Saldo</th>
              </tr>
            </thead>
            <tbody>
              <tr className="text-ink-3">
                <td>Nu</td>
                <td colSpan={5} />
                <td className="r">{e(s.bankCents)}</td>
              </tr>
              {withSales.rows.map((r) => (
                <tr key={r.day}>
                  <td className="whitespace-nowrap">
                    {d(r.date)}
                    {!r.workday && <span className="ml-1 text-xs text-ink-3">weekend</span>}
                  </td>
                  <td className="r">{r.shopifyInCents ? e(r.shopifyInCents) : ""}</td>
                  <td className="r">{r.paypalInCents ? e(r.paypalInCents) : ""}</td>
                  <td className="r">{r.metaCents ? e(-r.metaCents) : ""}</td>
                  <td className="r">{r.supplierCents ? e(-r.supplierCents) : ""}</td>
                  <td className="r">{r.privateAndSoftwareCents ? e(-(r.privateAndSoftwareCents + r.otherCents)) : ""}</td>
                  <td className={`r font-medium ${r.balanceCents < 0 ? "text-neg" : r.balanceCents < s.bufferCents ? "text-warn" : ""}`}>{e(r.balanceCents)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="text-xs text-ink-3">
          Volgorde van Shopify-instroom: eerst de ingeplande payout, dan pending verdeeld over 3 werkdagen, en nieuwe verkopen na {s.payoutDelayDays} dagen als{" "}
          {Math.round(s.payoutRatio * 100)}% van de verkoop. Verkopen die in het weekend uitbetaalbaar worden, komen maandag binnen.
        </p>
      </div>
    </div>
  );
}
