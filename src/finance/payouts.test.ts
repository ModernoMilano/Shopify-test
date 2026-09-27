import { describe, expect, it } from "vitest";
import { parsePayoutsCsv } from "./payouts";
import { payoutDifference } from "./calculations";

describe("payouts-export", () => {
  const csv = [
    "Payout Date,Status,Charges,Refunds,Adjustments,Reserved Funds,Fees,Retried Amount,Total,Currency",
    "2026-09-10,paid,1650.00,0.00,-15.00,-156.75,-67.65,0.00,1395.60,EUR",
    "2026-09-11,paid,2800.00,-70.00,0.00,-266.00,-114.80,0.00,2334.20,EUR",
  ].join("\n");

  it("leest de kolommen en toont afwijkingen per payout", () => {
    const rows = parsePayoutsCsv(csv);
    expect(rows).toHaveLength(2);
    expect(rows[0]).toMatchObject({ payoutDate: "2026-09-10", feesCents: 6765, reservedFundsCents: -15675 });
    expect(payoutDifference(rows[0])).toBe(-1500); // € 15 lager dan de som
    expect(payoutDifference(rows[1])).toBe(-1500);
  });
});
