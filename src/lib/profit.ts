/**
 * Winstberekening. Puur (geen database), zodat het goed te testen is.
 *
 * Definities (alle bedragen in centen):
 *  - omzet            = orderbedrag incl. verzending, min btw, na refunds (Shopify "current" bedragen)
 *  - inkoop (COGS)    = inkoopprijs + verzendkosten leverancier per stuk × aantal
 *  - transactiekosten = echte fees uit Shopify Payments, anders een schatting (% + vast bedrag)
 *  - bijdrage         = omzet − inkoop − transactiekosten   (wat een order oplevert vóór marketing)
 *  - nettowinst       = bijdrage − advertenties − vaste lasten
 */

export type CostRuleLite = {
  productId: string;
  variantId: string | null;
  unitCostCents: number;
  shippingCostCents: number;
  validFrom: Date;
};

export type LineItemLite = {
  productId: string | null;
  variantId: string | null;
  quantity: number;
  currentQuantity: number;
  unitPriceCents: number;
};

export type OrderLite = {
  id: string;
  createdAt: Date;
  totalCents: number;
  taxCents: number;
  refundedCents: number;
  feesCents: number | null;
  cancelledAt: Date | null;
  test: boolean;
  lineItems: LineItemLite[];
};

export type ProfitSettings = {
  /** bv. 0.019 voor 1,9% */
  paymentFeePercent: number;
  paymentFeeFixedCents: number;
  /** Bij dropshipping is de leverancier vaak al betaald als er een refund komt. */
  cogsOnRefundedItems: boolean;
  /** Alleen voor weergave van marge per stuk op basis van de verkoopprijs (incl. btw). */
  vatRate: number;
};

export const DEFAULT_SETTINGS: ProfitSettings = {
  paymentFeePercent: 0.019,
  paymentFeeFixedCents: 25,
  cogsOnRefundedItems: true,
  vatRate: 0.21,
};

export type OrderProfit = {
  orderId: string;
  revenueCents: number;
  cogsCents: number;
  feesCents: number;
  feesEstimated: boolean;
  contributionCents: number;
  unitsWithoutCost: number;
  units: number;
};

/** Index van kostenregels per product, nieuwste eerst. */
export class CostBook {
  private byProduct = new Map<string, CostRuleLite[]>();

  constructor(rules: CostRuleLite[]) {
    for (const r of rules) {
      const list = this.byProduct.get(r.productId) ?? [];
      list.push(r);
      this.byProduct.set(r.productId, list);
    }
    for (const list of this.byProduct.values()) {
      list.sort((a, b) => b.validFrom.getTime() - a.validFrom.getTime());
    }
  }

  /**
   * Kostprijs per stuk op een datum. Een variant-specifieke regel gaat voor een productregel.
   * Als alle regels van na de orderdatum zijn, gebruiken we de oudste: kostprijzen worden
   * vaak pas achteraf ingevoerd en gelden dan ook voor oudere orders.
   */
  lookup(productId: string | null, variantId: string | null, at: Date): number | null {
    if (!productId) return null;
    const rules = this.byProduct.get(productId);
    if (!rules?.length) return null;

    const pick = (candidates: CostRuleLite[]) =>
      candidates.find((r) => r.validFrom <= at) ?? candidates[candidates.length - 1];

    const variantRules = variantId ? rules.filter((r) => r.variantId === variantId) : [];
    const productRules = rules.filter((r) => r.variantId === null);
    const rule = variantRules.length ? pick(variantRules) : productRules.length ? pick(productRules) : null;
    return rule ? rule.unitCostCents + rule.shippingCostCents : null;
  }
}

export function isCountable(order: Pick<OrderLite, "cancelledAt" | "test">): boolean {
  return !order.test && !order.cancelledAt;
}

export function estimateFees(order: OrderLite, s: ProfitSettings): number {
  const charged = order.totalCents + order.refundedCents;
  if (charged <= 0) return 0;
  return Math.round(charged * s.paymentFeePercent) + s.paymentFeeFixedCents;
}

export function orderProfit(order: OrderLite, costs: CostBook, s: ProfitSettings): OrderProfit {
  const revenueCents = order.totalCents - order.taxCents;

  let cogsCents = 0;
  let unitsWithoutCost = 0;
  let units = 0;
  for (const li of order.lineItems) {
    const qty = s.cogsOnRefundedItems ? li.quantity : li.currentQuantity;
    if (qty <= 0) continue;
    units += qty;
    const unit = costs.lookup(li.productId, li.variantId, order.createdAt);
    if (unit === null) unitsWithoutCost += qty;
    else cogsCents += unit * qty;
  }

  const feesEstimated = order.feesCents === null;
  const feesCents = order.feesCents ?? estimateFees(order, s);

  return {
    orderId: order.id,
    revenueCents,
    cogsCents,
    feesCents,
    feesEstimated,
    contributionCents: revenueCents - cogsCents - feesCents,
    unitsWithoutCost,
    units,
  };
}

export type PeriodTotals = {
  orders: number;
  units: number;
  revenueCents: number;
  cogsCents: number;
  feesCents: number;
  adSpendCents: number;
  fixedCostsCents: number;
  contributionCents: number;
  netProfitCents: number;
  unitsWithoutCost: number;
  ordersWithMissingCost: number;
};

export function sumPeriod(
  profits: OrderProfit[],
  adSpendCents: number,
  fixedCostsCents: number,
): PeriodTotals {
  const t = profits.reduce(
    (acc, p) => {
      acc.orders += 1;
      acc.units += p.units;
      acc.revenueCents += p.revenueCents;
      acc.cogsCents += p.cogsCents;
      acc.feesCents += p.feesCents;
      acc.contributionCents += p.contributionCents;
      acc.unitsWithoutCost += p.unitsWithoutCost;
      if (p.unitsWithoutCost > 0) acc.ordersWithMissingCost += 1;
      return acc;
    },
    {
      orders: 0,
      units: 0,
      revenueCents: 0,
      cogsCents: 0,
      feesCents: 0,
      contributionCents: 0,
      unitsWithoutCost: 0,
      ordersWithMissingCost: 0,
    },
  );
  return {
    ...t,
    adSpendCents,
    fixedCostsCents,
    netProfitCents: t.contributionCents - adSpendCents - fixedCostsCents,
  };
}

/** Omzet / bijdrage vóór marketing: boven deze ROAS verdien je aan advertenties. */
export function breakEvenRoas(t: Pick<PeriodTotals, "revenueCents" | "contributionCents">): number | null {
  if (t.contributionCents <= 0) return null;
  return t.revenueCents / t.contributionCents;
}

export function ratio(numerator: number, denominator: number): number | null {
  return denominator === 0 ? null : numerator / denominator;
}

export type ExpenseLite = { amountCents: number; startDate: Date; endDate: Date | null };

const DAY_MS = 86_400_000;

/**
 * Vaste maandlasten omgeslagen naar de dagen in [from, to) (UTC-dagen).
 * Een maandbedrag telt als bedrag × 12 / 365 per actieve dag.
 */
export function prorateExpenses(expenses: ExpenseLite[], from: Date, to: Date): number {
  let total = 0;
  for (const e of expenses) {
    const start = Math.max(from.getTime(), startOfUtcDay(e.startDate).getTime());
    const end = Math.min(
      to.getTime(),
      e.endDate ? startOfUtcDay(e.endDate).getTime() + DAY_MS : Number.POSITIVE_INFINITY,
    );
    if (end <= start) continue;
    const days = (end - start) / DAY_MS;
    total += (e.amountCents * 12 * days) / 365;
  }
  return Math.round(total);
}

export function startOfUtcDay(d: Date): Date {
  return new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()));
}
