import { describe, expect, it } from "vitest";
import {
  CostBook,
  DEFAULT_SETTINGS,
  breakEvenRoas,
  orderProfit,
  prorateExpenses,
  sumPeriod,
  type OrderLite,
} from "./profit";

const d = (s: string) => new Date(s);

function order(partial: Partial<OrderLite> = {}): OrderLite {
  return {
    id: "1",
    createdAt: d("2026-09-10T12:00:00Z"),
    totalCents: 12100, // €121 incl. 21% btw
    taxCents: 2100,
    refundedCents: 0,
    feesCents: null,
    cancelledAt: null,
    test: false,
    lineItems: [{ productId: "p1", variantId: "v1", quantity: 2, currentQuantity: 2, unitPriceCents: 6050 }],
    ...partial,
  };
}

describe("CostBook", () => {
  const book = new CostBook([
    { productId: "p1", variantId: null, unitCostCents: 1500, shippingCostCents: 500, validFrom: d("2026-01-01") },
    { productId: "p1", variantId: null, unitCostCents: 1800, shippingCostCents: 500, validFrom: d("2026-09-01") },
    { productId: "p1", variantId: "vXL", unitCostCents: 2500, shippingCostCents: 500, validFrom: d("2026-01-01") },
  ]);

  it("kiest de regel die gold op de orderdatum", () => {
    expect(book.lookup("p1", "v1", d("2026-08-15"))).toBe(2000);
    expect(book.lookup("p1", "v1", d("2026-09-15"))).toBe(2300);
  });

  it("variant-regel gaat voor productregel", () => {
    expect(book.lookup("p1", "vXL", d("2026-09-15"))).toBe(3000);
  });

  it("valt terug op de oudste regel voor orders van vóór de eerste regel", () => {
    expect(book.lookup("p1", "v1", d("2025-06-01"))).toBe(2000);
  });

  it("geeft null zonder kostprijs", () => {
    expect(book.lookup("p2", null, d("2026-09-15"))).toBeNull();
    expect(book.lookup(null, null, d("2026-09-15"))).toBeNull();
  });
});

describe("orderProfit", () => {
  const book = new CostBook([
    { productId: "p1", variantId: null, unitCostCents: 2000, shippingCostCents: 500, validFrom: d("2026-01-01") },
  ]);

  it("rekent omzet ex btw, inkoop en geschatte fees", () => {
    const p = orderProfit(order(), book, DEFAULT_SETTINGS);
    expect(p.revenueCents).toBe(10000);
    expect(p.cogsCents).toBe(5000);
    expect(p.feesCents).toBe(Math.round(12100 * 0.019) + 25);
    expect(p.feesEstimated).toBe(true);
    expect(p.contributionCents).toBe(10000 - 5000 - p.feesCents);
  });

  it("gebruikt echte fees als die bekend zijn", () => {
    const p = orderProfit(order({ feesCents: 199 }), book, DEFAULT_SETTINGS);
    expect(p.feesCents).toBe(199);
    expect(p.feesEstimated).toBe(false);
  });

  it("telt inkoop van gerefunde items mee, tenzij uitgezet", () => {
    const refunded = order({
      totalCents: 6050,
      taxCents: 1050,
      refundedCents: 6050,
      lineItems: [{ productId: "p1", variantId: "v1", quantity: 2, currentQuantity: 1, unitPriceCents: 6050 }],
    });
    expect(orderProfit(refunded, book, DEFAULT_SETTINGS).cogsCents).toBe(5000);
    expect(orderProfit(refunded, book, { ...DEFAULT_SETTINGS, cogsOnRefundedItems: false }).cogsCents).toBe(2500);
  });

  it("markeert stuks zonder kostprijs", () => {
    const p = orderProfit(
      order({ lineItems: [{ productId: "px", variantId: null, quantity: 3, currentQuantity: 3, unitPriceCents: 1000 }] }),
      book,
      DEFAULT_SETTINGS,
    );
    expect(p.unitsWithoutCost).toBe(3);
    expect(p.cogsCents).toBe(0);
  });
});

describe("periode", () => {
  it("trekt ads en vaste lasten af van de bijdrage", () => {
    const book = new CostBook([]);
    const p = orderProfit(order({ feesCents: 0 }), book, DEFAULT_SETTINGS);
    const t = sumPeriod([p], 3000, 1000);
    expect(t.netProfitCents).toBe(10000 - 3000 - 1000);
    expect(t.ordersWithMissingCost).toBe(1);
  });

  it("break-even ROAS = omzet / bijdrage", () => {
    expect(breakEvenRoas({ revenueCents: 10000, contributionCents: 4000 })).toBe(2.5);
    expect(breakEvenRoas({ revenueCents: 10000, contributionCents: -1 })).toBeNull();
  });

  it("slaat vaste lasten om naar dagen", () => {
    const exp = [{ amountCents: 36500, startDate: d("2026-01-01"), endDate: null }];
    // €365/maand × 12 / 365 = €12 per dag → 10 dagen = €120
    expect(prorateExpenses(exp, d("2026-09-01"), d("2026-09-11"))).toBe(12000);
    // eindigt op 5 sept (inclusief) → 5 dagen
    expect(prorateExpenses([{ ...exp[0], endDate: d("2026-09-05") }], d("2026-09-01"), d("2026-09-11"))).toBe(6000);
    // begint na de periode
    expect(prorateExpenses([{ ...exp[0], startDate: d("2026-10-01") }], d("2026-09-01"), d("2026-09-11"))).toBe(0);
  });
});
