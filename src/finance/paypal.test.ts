import { describe, expect, it } from "vitest";
import { summarizePaypal, type PaypalTransaction } from "./paypal";

const tx = (p: Partial<PaypalTransaction>): PaypalTransaction => ({
  id: "x",
  date: "2026-09-10T10:00:00Z",
  eventCode: "T0006",
  status: "S",
  grossCents: 0,
  feeCents: 0,
  currency: "EUR",
  ...p,
});

describe("PayPal-samenvatting", () => {
  it("telt verkopen, fees, refunds en opnames naar de bank", () => {
    const s = summarizePaypal([
      tx({ grossCents: 18900, feeCents: 694 }),
      tx({ grossCents: 15000, feeCents: 560 }),
      tx({ eventCode: "T1107", grossCents: -15000, feeCents: 0 }),
      tx({ eventCode: "T0400", grossCents: -45800 }),
      tx({ status: "P", grossCents: 9900, feeCents: 380 }), // nog niet voltooid
      tx({ currency: "GBP", grossCents: 5000, feeCents: 200 }),
    ]);
    expect(s.salesCents).toBe(33900);
    expect(s.salesCount).toBe(2);
    expect(s.feesCents).toBe(1254);
    expect(s.refundsCents).toBe(-15000);
    expect(s.withdrawalsCents).toBe(45800);
    expect(s.otherCurrencyCount).toBe(1);
  });
});
