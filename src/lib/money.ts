const eur = new Intl.NumberFormat("nl-NL", { style: "currency", currency: "EUR" });
const eurRound = new Intl.NumberFormat("nl-NL", {
  style: "currency",
  currency: "EUR",
  maximumFractionDigits: 0,
});

export function formatCents(cents: number, round = false): string {
  return (round ? eurRound : eur).format(cents / 100);
}

export function formatPct(value: number | null): string {
  if (value === null || !Number.isFinite(value)) return "ontbreekt";
  return `${(value * 100).toFixed(1).replace(".", ",")}%`;
}

/** Parse "12,50" / "12.50" / "€ 12,50" naar centen. Geeft null bij ongeldige invoer. */
export function parseEuroToCents(input: string): number | null {
  const cleaned = input.replace(/[€\s]/g, "");
  if (!cleaned) return null;
  // "1.234,56" -> "1234.56"; "1234.56" blijft; "12,5" -> "12.5"
  const normalized = cleaned.includes(",")
    ? cleaned.replace(/\./g, "").replace(",", ".")
    : cleaned;
  const n = Number(normalized);
  if (!Number.isFinite(n)) return null;
  return Math.round(n * 100);
}

/** Shopify geeft bedragen als string ("12.50"). */
export function moneyStringToCents(amount: string | null | undefined): number {
  if (!amount) return 0;
  return Math.round(Number(amount) * 100);
}
