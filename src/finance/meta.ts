/** Meta ads: markt afleiden uit campagnenaam, Windsor.ai ophalen, en budgetregels uit het protocol. */

export function marketOf(campaign: string): string {
  const c = campaign.toUpperCase();
  if (/\bUK\b|UK\+IE|\bIE\b/.test(c)) return "UK/IE";
  if (/\bDEU?\b|\bAT\b/.test(c)) return "DE/AT";
  if (/\bUSA?\b/.test(c)) return "USA";
  if (/SWIS|SWISS|\bCH\b/.test(c)) return "CH";
  if (/WORLDWIDE|\bWW\b/.test(c)) return "Worldwide";
  return "Overig";
}

export type MetaRow = {
  date: string;
  campaign: string;
  spendCents: number;
  clicks: number;
  impressions: number;
  purchases: number;
  purchaseValueCents: number;
  frequency: number | null;
};

const FIELDS = ["date", "campaign", "spend", "clicks", "impressions", "actions_purchase", "action_values_purchase", "frequency"];

/** Haal dagcijfers per campagne op bij Windsor.ai (Facebook-connector). */
export async function fetchWindsorMeta(dateFrom: string, dateTo: string): Promise<MetaRow[]> {
  const key = process.env.WINDSOR_API_KEY;
  if (!key) throw new Error("WINDSOR_API_KEY is niet ingesteld");
  const url = new URL("https://connectors.windsor.ai/facebook");
  url.searchParams.set("api_key", key);
  url.searchParams.set("date_from", dateFrom);
  url.searchParams.set("date_to", dateTo);
  url.searchParams.set("fields", FIELDS.join(","));
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error(`Windsor.ai gaf fout ${res.status}`);
  const json = (await res.json()) as { data?: Record<string, unknown>[] };
  return (json.data ?? [])
    .map((r) => ({
      date: String(r.date),
      campaign: String(r.campaign ?? "onbekend"),
      spendCents: Math.round(Number(r.spend ?? 0) * 100),
      clicks: Number(r.clicks ?? 0),
      impressions: Number(r.impressions ?? 0),
      purchases: Number(r.actions_purchase ?? 0),
      purchaseValueCents: Math.round(Number(r.action_values_purchase ?? 0) * 100),
      frequency: r.frequency == null ? null : Number(r.frequency),
    }))
    .filter((r) => r.spendCents > 0 || r.impressions > 0);
}

export type BudgetWarning = { id: string; message: string };

/** Protocol: max 20% verhoging per ingreep, minimaal 3 dagen tussen wijzigingen, nooit twee tegelijk. */
export function budgetWarnings(changes: { id: string; date: Date; campaign: string; oldCents: number; newCents: number }[]): BudgetWarning[] {
  const out: BudgetWarning[] = [];
  const sorted = [...changes].sort((a, b) => a.date.getTime() - b.date.getTime());
  sorted.forEach((c, i) => {
    if (c.oldCents > 0 && (c.newCents - c.oldCents) / c.oldCents > 0.2) {
      out.push({ id: c.id, message: `Verhoging van ${Math.round(((c.newCents - c.oldCents) / c.oldCents) * 100)}%, meer dan 20%` });
    }
    const prev = sorted.slice(0, i).reverse().find((p) => p.campaign === c.campaign);
    if (prev) {
      const days = (c.date.getTime() - prev.date.getTime()) / 86_400_000;
      if (days < 3) out.push({ id: c.id, message: `Maar ${days} dag(en) na de vorige ingreep, minimaal 3` });
    }
    const sameDay = sorted.filter((o) => o !== c && o.date.getTime() === c.date.getTime());
    if (sameDay.length) out.push({ id: c.id, message: "Meerdere ingrepen op dezelfde dag" });
  });
  return out;
}
