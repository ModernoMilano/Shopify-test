/** Categorieën voor bankmutaties en hoe ze meetellen. */

export type CategoryKind = "income" | "cost" | "debt" | "equity" | "private" | "neutral" | "unknown";

/** In welke post van de winst- en verliesrekening een kostencategorie valt. */
export type PnlBucket = "cogs" | "meta" | "fees" | "chargebacks" | "other" | "team";

export type Category = {
  id: string;
  label: string;
  kind: CategoryKind;
  bucket?: PnlBucket;
};

export const CATEGORIES: Category[] = [
  { id: "shopify_payout", label: "Inkomsten Shopify", kind: "income" },
  { id: "paypal_payout", label: "Inkomsten PayPal", kind: "income" },
  { id: "loan", label: "Lening", kind: "debt" },
  { id: "owner_deposit", label: "Eigen storting", kind: "equity" },
  { id: "meta", label: "Meta ads", kind: "cost", bucket: "meta" },
  { id: "cogs", label: "COGS en verzending", kind: "cost", bucket: "cogs" },
  { id: "private", label: "Privé", kind: "private" },
  { id: "software", label: "Software en tools", kind: "cost", bucket: "other" },
  { id: "freelancers", label: "Freelancers", kind: "cost", bucket: "other" },
  { id: "accountant", label: "Boekhouder", kind: "cost", bucket: "other" },
  { id: "bank_fees", label: "Bankkosten", kind: "cost", bucket: "other" },
  { id: "other_business", label: "Overig zakelijk", kind: "cost", bucket: "other" },
  { id: "chargebacks", label: "Chargebacks en disputes", kind: "cost", bucket: "chargebacks" },
  { id: "team", label: "Team", kind: "cost", bucket: "team" },
  { id: "internal", label: "Interne boeking", kind: "neutral" },
  { id: "unknown", label: "Onbekend", kind: "unknown" },
];

export const CATEGORY_BY_ID = new Map(CATEGORIES.map((c) => [c.id, c]));

export const categoryLabel = (id: string) => CATEGORY_BY_ID.get(id)?.label ?? id;

export type Direction = "in" | "out" | "any";

export type Rule = {
  id?: string;
  /** tekst die in omschrijving, tegenpartij of referentie moet voorkomen (hoofdletterongevoelig) */
  pattern: string;
  /** "in" | "out" | "any" */
  direction: Direction | string;
  category: string;
  /** lager = eerder */
  priority: number;
};

export type Categorizable = {
  description: string;
  details: string;
  amountCents: number;
};

export function matchRule<R extends Rule>(tx: Categorizable, rules: R[]): R | null {
  const haystack = `${tx.description}\n${tx.details}`.toLowerCase();
  const dir: Direction = tx.amountCents >= 0 ? "in" : "out";
  const sorted = [...rules].sort((a, b) => a.priority - b.priority);
  for (const r of sorted) {
    if (r.direction !== "any" && r.direction !== dir) continue;
    if (haystack.includes(r.pattern.toLowerCase())) return r;
  }
  return null;
}

/**
 * Startregels op basis van het septemberafschrift.
 * Specifieke regels (lening, eigen storting) hebben een lagere prioriteit dan algemene.
 */
export const DEFAULT_RULES: Rule[] = [
  { pattern: "Referentie: Lening", direction: "in", category: "loan", priority: 10 },
  { pattern: "HR RJ KOMEN", direction: "in", category: "loan", priority: 10 },
  { pattern: "Betaling van GIJS BASTIAAN FONTEIN", direction: "in", category: "owner_deposit", priority: 10 },
  { pattern: "Tijdelijk geblokkeerd", direction: "any", category: "internal", priority: 10 },
  { pattern: "Release", direction: "in", category: "internal", priority: 20 },
  { pattern: "STRIPE TECHNOLOGY", direction: "in", category: "shopify_payout", priority: 20 },
  { pattern: "PAYPAL", direction: "in", category: "paypal_payout", priority: 20 },
  { pattern: "Facebk", direction: "any", category: "meta", priority: 20 },
  { pattern: "Facebook", direction: "any", category: "meta", priority: 30 },
  { pattern: "Meta Platforms", direction: "any", category: "meta", priority: 30 },
  { pattern: "Jinjiang Yuguang", direction: "out", category: "cogs", priority: 20 },
  { pattern: "EAST BAITE", direction: "out", category: "cogs", priority: 20 },
  { pattern: "Alibaba", direction: "out", category: "cogs", priority: 20 },
  { pattern: "kungfubuy", direction: "out", category: "cogs", priority: 20 },
  { pattern: "To Gijs Bastiaan Fontein", direction: "out", category: "private", priority: 20 },
  { pattern: "As Fontein", direction: "any", category: "private", priority: 20 },
  { pattern: "Frederike", direction: "any", category: "private", priority: 20 },
  { pattern: "EUR Personal", direction: "any", category: "private", priority: 20 },
  // geld terug van de privé-pocket naar de Pro-rekening verlaagt de privé-opnames
  { pattern: "To EUR Pro", direction: "in", category: "private", priority: 20 },
  { pattern: "Chargeback.io", direction: "out", category: "software", priority: 20 },
  { pattern: "Shopify*", direction: "out", category: "software", priority: 30 },
  { pattern: "Klaviyo", direction: "out", category: "software", priority: 30 },
  { pattern: "Higgsfield", direction: "out", category: "software", priority: 30 },
  { pattern: "Weglot", direction: "out", category: "software", priority: 30 },
  { pattern: "Gorgias", direction: "out", category: "software", priority: 30 },
  { pattern: "OpenAI", direction: "out", category: "software", priority: 30 },
  { pattern: "Google Workspace", direction: "out", category: "software", priority: 30 },
  { pattern: "Apple.com", direction: "out", category: "software", priority: 30 },
  { pattern: "rinkel", direction: "out", category: "software", priority: 30 },
  { pattern: "wetracked", direction: "out", category: "software", priority: 30 },
  { pattern: "Fiverr", direction: "out", category: "freelancers", priority: 30 },
  { pattern: "OnlineJobs", direction: "out", category: "freelancers", priority: 30 },
  { pattern: "Boekhouding", direction: "out", category: "accountant", priority: 30 },
];

/** Stukje van een transactie dat in een categorie valt (transferkosten worden apart geteld). */
export type CategorizedAmount = { category: string; cents: number };

/**
 * Splits een mutatie in categoriebedragen. Revolut rekent transferkosten in het afgeschreven bedrag;
 * die gaan naar bankkosten, de rest naar de categorie van de mutatie.
 */
export function splitAmounts(tx: { amountCents: number; feeCents: number; category: string }): CategorizedAmount[] {
  if (!tx.feeCents || tx.amountCents >= 0) return [{ category: tx.category, cents: tx.amountCents }];
  return [
    { category: tx.category, cents: tx.amountCents + tx.feeCents },
    { category: "bank_fees", cents: -tx.feeCents },
  ];
}

export function totalsByCategory(
  txs: { amountCents: number; feeCents: number; category: string }[],
): Map<string, number> {
  const out = new Map<string, number>();
  for (const tx of txs) {
    for (const part of splitAmounts(tx)) out.set(part.category, (out.get(part.category) ?? 0) + part.cents);
  }
  return out;
}
