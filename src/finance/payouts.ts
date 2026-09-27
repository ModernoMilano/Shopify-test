import { parseCsv } from "@/lib/csv";

export type PayoutRow = {
  payoutDate: string;
  status: string;
  chargesCents: number;
  refundsCents: number;
  adjustmentsCents: number;
  reservedFundsCents: number;
  /** positief */
  feesCents: number;
  retriedCents: number;
  totalCents: number;
  currency: string;
};

const num = (s: string | undefined) => {
  const t = (s ?? "").trim().replace(/[€\s]/g, "");
  if (!t) return 0;
  const n = Number(/,\d{1,2}$/.test(t) ? t.replace(/\./g, "").replace(",", ".") : t.replace(/,/g, ""));
  return Number.isFinite(n) ? Math.round(n * 100) : 0;
};

/** Shopify Payments payouts-export (Finances, Payouts, Export). */
export function parsePayoutsCsv(text: string): PayoutRow[] {
  const [header, ...rows] = parseCsv(text.replace(/^﻿/, "").trim());
  if (!header) return [];
  const h = header.map((x) => x.trim().toLowerCase());
  const col = (...names: string[]) => h.findIndex((x) => names.includes(x));
  const i = {
    date: col("payout date", "date", "datum"),
    status: col("status"),
    charges: col("charges"),
    refunds: col("refunds"),
    adjustments: col("adjustments"),
    reserved: col("reserved funds", "reserved"),
    fees: col("fees"),
    retried: col("retried amount", "retried"),
    total: col("total", "amount", "net"),
    currency: col("currency"),
  };
  if (i.date < 0 || i.total < 0) throw new Error("Onbekend formaat: kolommen 'Payout Date' en 'Total' ontbreken");
  return rows
    .map((r) => ({
      payoutDate: (r[i.date] ?? "").trim().slice(0, 10),
      status: (r[i.status] ?? "paid").trim().toLowerCase() || "paid",
      chargesCents: num(r[i.charges]),
      refundsCents: num(r[i.refunds]),
      adjustmentsCents: num(r[i.adjustments]),
      reservedFundsCents: num(r[i.reserved]),
      // Shopify zet fees als negatief bedrag in de export; wij bewaren ze positief
      feesCents: Math.abs(num(r[i.fees])),
      retriedCents: num(r[i.retried]),
      totalCents: num(r[i.total]),
      currency: (r[i.currency] ?? "EUR").trim() || "EUR",
    }))
    .filter((r) => /^\d{4}-\d{2}-\d{2}$/.test(r.payoutDate));
}
