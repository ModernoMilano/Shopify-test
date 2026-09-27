import { describe, expect, it } from "vitest";
import { feesFromTransactions, type ShopifyTransaction } from "./shopify";

// Gebaseerd op een echte order: klant betaalde 669 PLN (= €153,03)
const plnSale: ShopifyTransaction = {
  kind: "SALE",
  status: "SUCCESS",
  amountSet: {
    shopMoney: { amount: "153.03", currencyCode: "EUR" },
    presentmentMoney: { amount: "669.0", currencyCode: "PLN" },
  },
  fees: [
    { type: "processing_fee", amount: { amount: "13.13", currencyCode: "PLN" } },
    { type: "foreign_exchange_fee", amount: { amount: "13.12", currencyCode: "PLN" } },
  ],
};

describe("feesFromTransactions", () => {
  it("rekent fees in vreemde valuta om naar EUR", () => {
    const r = feesFromTransactions([plnSale], "EUR");
    // (13,13 + 13,12) PLN × 153,03/669 ≈ €6,00
    expect(r).toEqual({ feesCents: 600, fxFeesCents: 300 });
  });

  it("laat EUR-fees ongemoeid", () => {
    const eur: ShopifyTransaction = {
      kind: "SALE",
      status: "SUCCESS",
      amountSet: { shopMoney: { amount: "100", currencyCode: "EUR" }, presentmentMoney: { amount: "100", currencyCode: "EUR" } },
      fees: [{ type: "processing_fee", amount: { amount: "2.05", currencyCode: "EUR" } }],
    };
    expect(feesFromTransactions([eur], "EUR")).toEqual({ feesCents: 205, fxFeesCents: 0 });
  });

  it("negeert mislukte transacties en geeft null zonder fee-data", () => {
    expect(feesFromTransactions([{ ...plnSale, status: "FAILURE" }], "EUR")).toBeNull();
    expect(feesFromTransactions([{ ...plnSale, fees: [] }], "EUR")).toBeNull();
  });
});
