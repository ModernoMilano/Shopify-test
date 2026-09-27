import { db } from "./db";
import { addDays, dayKey, eachDay, type Period } from "./period";
import {
  CostBook,
  breakEvenRoas,
  isCountable,
  orderProfit,
  prorateExpenses,
  sumPeriod,
  type OrderProfit,
  type PeriodTotals,
} from "./profit";
import { getProfitSettings } from "./settings";

export type DayRow = {
  day: string;
  revenueCents: number;
  cogsCents: number;
  feesCents: number;
  adSpendCents: number;
  fixedCostsCents: number;
  netProfitCents: number;
  orders: number;
};

export type ProductRow = {
  productId: string | null;
  title: string;
  imageUrl: string | null;
  units: number;
  revenueCents: number;
  cogsCents: number;
  feesCents: number;
  contributionCents: number;
  unitsWithoutCost: number;
};

export type Report = {
  totals: PeriodTotals;
  fxFeesCents: number;
  estimatedFeeOrders: number;
  breakEvenRoas: number | null;
  days: DayRow[];
  products: ProductRow[];
};

async function loadOrders(period: Pick<Period, "from" | "to">) {
  return db.order.findMany({
    where: { createdAt: { gte: period.from, lt: period.to } },
    select: {
      id: true,
      name: true,
      createdAt: true,
      totalCents: true,
      taxCents: true,
      refundedCents: true,
      feesCents: true,
      fxFeesCents: true,
      cancelledAt: true,
      test: true,
      countryCode: true,
      presentmentCurrency: true,
      financialStatus: true,
      lineItems: {
        select: {
          productId: true,
          variantId: true,
          title: true,
          quantity: true,
          currentQuantity: true,
          unitPriceCents: true,
          product: { select: { title: true, imageUrl: true } },
        },
      },
    },
    orderBy: { createdAt: "desc" },
  });
}

export async function loadCostBook(): Promise<CostBook> {
  const rules = await db.costRule.findMany({
    select: { productId: true, variantId: true, unitCostCents: true, shippingCostCents: true, validFrom: true },
  });
  return new CostBook(rules);
}

export async function buildReport(period: Period): Promise<Report> {
  const [orders, costs, settings, ads, expenses] = await Promise.all([
    loadOrders(period),
    loadCostBook(),
    getProfitSettings(),
    db.adSpend.findMany({
      where: { date: { gte: new Date(period.fromKey), lte: new Date(period.toKey) } },
    }),
    db.expense.findMany(),
  ]);

  const counted = orders.filter(isCountable);
  const profits = counted.map((o) => orderProfit(o, costs, settings));

  // --- per dag
  const byDay = new Map<string, DayRow>(
    eachDay(period.fromKey, period.toKey).map((day) => [
      day,
      {
        day,
        revenueCents: 0,
        cogsCents: 0,
        feesCents: 0,
        adSpendCents: 0,
        fixedCostsCents: 0,
        netProfitCents: 0,
        orders: 0,
      },
    ]),
  );
  counted.forEach((o, i) => {
    const row = byDay.get(dayKey(o.createdAt));
    if (!row) return;
    const p = profits[i];
    row.revenueCents += p.revenueCents;
    row.cogsCents += p.cogsCents;
    row.feesCents += p.feesCents;
    row.orders += 1;
  });
  for (const a of ads) {
    const row = byDay.get(a.date.toISOString().slice(0, 10));
    if (row) row.adSpendCents += a.amountCents;
  }
  for (const row of byDay.values()) {
    row.fixedCostsCents = prorateExpenses(
      expenses,
      new Date(row.day),
      new Date(addDays(row.day, 1)),
    );
    row.netProfitCents = row.revenueCents - row.cogsCents - row.feesCents - row.adSpendCents - row.fixedCostsCents;
  }
  const days = [...byDay.values()];

  const adSpendCents = ads.reduce((s, a) => s + a.amountCents, 0);
  const fixedCostsCents = days.reduce((s, d) => s + d.fixedCostsCents, 0);
  const totals = sumPeriod(profits, adSpendCents, fixedCostsCents);

  return {
    totals,
    fxFeesCents: counted.reduce((s, o) => s + (o.fxFeesCents ?? 0), 0),
    estimatedFeeOrders: profits.filter((p) => p.feesEstimated).length,
    breakEvenRoas: breakEvenRoas(totals),
    days,
    products: productBreakdown(counted, profits, costs, settings.cogsOnRefundedItems),
  };
}

/**
 * Omzet en fees per product: de orderomzet (ex btw, incl. verzending) wordt verdeeld
 * naar rato van de regelwaarde, zodat de productcijfers optellen tot het totaal.
 */
function productBreakdown(
  orders: Awaited<ReturnType<typeof loadOrders>>,
  profits: OrderProfit[],
  costs: CostBook,
  cogsOnRefunds: boolean,
): ProductRow[] {
  const rows = new Map<string, ProductRow>();
  orders.forEach((o, i) => {
    const p = profits[i];
    const gross = o.lineItems.reduce((s, li) => s + li.unitPriceCents * li.currentQuantity, 0);
    for (const li of o.lineItems) {
      const key = li.productId ?? `title:${li.title}`;
      const row =
        rows.get(key) ??
        ({
          productId: li.productId,
          title: li.product?.title ?? li.title,
          imageUrl: li.product?.imageUrl ?? null,
          units: 0,
          revenueCents: 0,
          cogsCents: 0,
          feesCents: 0,
          contributionCents: 0,
          unitsWithoutCost: 0,
        } satisfies ProductRow);
      const share = gross > 0 ? (li.unitPriceCents * li.currentQuantity) / gross : 0;
      const qty = cogsOnRefunds ? li.quantity : li.currentQuantity;
      const unitCost = costs.lookup(li.productId, li.variantId, o.createdAt);
      row.units += li.currentQuantity;
      row.revenueCents += Math.round(p.revenueCents * share);
      row.feesCents += Math.round(p.feesCents * share);
      if (unitCost === null) row.unitsWithoutCost += qty;
      else row.cogsCents += unitCost * qty;
      rows.set(key, row);
    }
  });
  for (const r of rows.values()) r.contributionCents = r.revenueCents - r.cogsCents - r.feesCents;
  return [...rows.values()].sort((a, b) => b.revenueCents - a.revenueCents);
}

export async function orderList(period: Period) {
  const [orders, costs, settings] = await Promise.all([loadOrders(period), loadCostBook(), getProfitSettings()]);
  return orders.map((o) => ({
    order: o,
    counted: isCountable(o),
    profit: orderProfit(o, costs, settings),
  }));
}
