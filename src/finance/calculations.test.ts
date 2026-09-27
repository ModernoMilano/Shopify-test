import { describe, expect, it } from "vitest";
import {
  cashBridge,
  chargebackRate,
  daysBelow,
  forecast,
  isWorkday,
  moneyLocation,
  payoutDifference,
  pnl,
  type ForecastSettings,
} from "./calculations";

const e = (euros: number) => Math.round(euros * 100);

describe("winst en verlies september (spec 5.2)", () => {
  const sept = pnl({
    revenueCents: e(93384),
    taxesCents: e(7481.41),
    orders: 499,
    cogsCents: e(31096),
    metaCents: e(33798),
    feesCents: e(3700),
    chargebacksCents: e(3582),
    otherCents: e(1717),
    teamCents: 0,
  });

  it("winst, marge en MER", () => {
    // De spec noemt €19.490; de afgeronde posten tellen op tot €19.491 (afronding in de spec).
    expect(Math.abs(sept.profitCents - e(19490))).toBeLessThanOrEqual(e(1));
    expect(sept.margin!.toFixed(3)).toBe("0.209");
    expect(sept.mer!.toFixed(2)).toBe("2.76");
  });

  it("percentages en per order", () => {
    expect(sept.metaShare!.toFixed(3)).toBe("0.362");
    expect(sept.cogsShare!.toFixed(3)).toBe("0.333");
    expect(Math.round(sept.aovCents! / 100)).toBe(187);
  });

  it("break-even ROAS = omzet / (omzet − kosten behalve Meta)", () => {
    expect(sept.breakEvenRoas!.toFixed(2)).toBe("1.75");
  });

  it("btw reserveren haalt de btw van de winst af", () => {
    const withVat = pnl({ ...sept, teamCents: 0 }, { reserveVat: true });
    expect(withVat.profitCents).toBe(sept.profitCents - e(7481.41));
    expect(sept.profitAfterVatCents).toBe(withVat.profitCents);
  });

  it("teamkosten van €3.000 laten de marge naar ongeveer 17% zakken (spec 8)", () => {
    const withTeam = pnl({ ...sept, teamCents: e(3000) });
    expect(withTeam.margin!.toFixed(2)).toBe("0.18");
  });
});

describe("waar het geld staat (spec 5.5)", () => {
  const m = moneyLocation({
    bankCents: e(8411),
    payoutScheduledCents: e(2658),
    pendingCents: e(10402),
    holdCents: e(8983),
    paypalCents: e(200),
  });
  it("totaal €30.654, payout niet dubbel in pending", () => {
    expect(m.totalCents).toBe(e(30654));
    expect(m.availableNow).toBe(e(8611));
    expect(m.soon).toBe(e(13060));
    expect(m.locked).toBe(e(8983));
    expect(m.shopifyCents).toBe(e(22043));
  });
});

describe("cash bridge (spec 5.6)", () => {
  const b = cashBridge({
    profitCents: e(19490),
    shopifyNowCents: e(22043),
    shopifyBeginCents: e(7677),
    bankBeginCents: e(1836),
    bankNowCents: e(8411),
    privateCents: e(5705),
    metaPreviousPeriodCents: e(1451),
    loansAndDepositsCents: e(10150),
  });

  it("eindigt op +€6.575 met timing −€1.543", () => {
    expect(b.shopifyGrowth).toBe(e(14366));
    expect(b.bankGrowth).toBe(e(6575));
    expect(b.timing).toBe(e(-1543));
    expect(b.steps.reduce((s, x) => s + x.cents, 0)).toBe(b.bankGrowth);
  });

  it("waarschuwt als timing meer dan 5% van de winst is", () => {
    expect(b.timingWarning).toBe(true); // 1.543 > 974,50
  });
});

describe("Shopify payouts (spec 5.4)", () => {
  it("som van de kolommen wijkt €30 af van het uitbetaalde totaal (10 en 11 sept)", () => {
    const diff = payoutDifference({
      chargesCents: e(68395.46),
      refundsCents: e(-70),
      adjustmentsCents: e(-3581.65),
      reservedFundsCents: e(-6503.69),
      feesCents: e(2831.79),
      retriedCents: e(1525.44),
      totalCents: e(56903.77),
    });
    expect(diff).toBe(e(-30));
  });

  it("reserve ongeveer 9,5% en fees 4,1% van charges", () => {
    expect((6503.69 / 68395.46).toFixed(3)).toBe("0.095");
    expect((2831.79 / 68395.46).toFixed(3)).toBe("0.041");
  });
});

describe("chargebacks", () => {
  it("rate en dagen onder 1%", () => {
    expect(chargebackRate(3, 600)).toBe(0.005);
    expect(chargebackRate(1, 0)).toBeNull();
    expect(daysBelow([0.02, 0.009, 0.012, 0.009, 0.008, 0.0095])).toBe(3);
    expect(daysBelow([0.009, null, 0.008])).toBe(1);
  });
});

describe("prognose (spec 5.7)", () => {
  const base: ForecastSettings = {
    days: 7,
    startDate: "2026-09-28", // maandag
    bankCents: e(8411.16),
    payoutScheduledCents: e(2658),
    payoutScheduledDate: "2026-09-28",
    pendingCents: e(10402),
    pendingWorkdays: 3,
    salesPerDayCents: e(2900),
    payoutRatio: 0.86,
    payoutDelayDays: 3,
    paypalPerDayCents: e(300),
    metaPerDayCents: e(1600),
    privatePerWeekCents: e(1500),
    softwarePerWeekCents: e(300),
    supplierPaymentCents: e(3000),
    supplierPaymentDay: 2,
    bufferCents: e(2000),
  };

  it("werkdagen", () => {
    expect(isWorkday("2026-09-28")).toBe(true);
    expect(isWorkday("2026-10-03")).toBe(false);
  });

  it("sales lopen door", () => {
    const f = forecast(base);
    const bal = f.rows.map((r) => r.balanceCents / 100);
    expect(bal[0]).toBeCloseTo(9512.02, 1); // payout maandag
    expect(bal[1]).toBeCloseTo(8422.21, 1); // pending + leverancier
    expect(bal[3]).toBeCloseTo(14736.59, 1); // pending + eerste nieuwe sales
    expect(f.rows[5].shopifyInCents).toBe(0); // zaterdag geen payout
    expect(f.balanceAfter7Cents / 100).toBeCloseTo(12559.17, 1);
    expect(f.lowest.date).toBe("2026-09-29");
    expect(f.belowBuffer).toBe(false);
  });

  it("weekendverkopen komen maandag binnen", () => {
    const f = forecast({ ...base, days: 8 });
    // verkopen van wo, do, vr (dag 3, 4, 5) worden za, zo, ma uitbetaalbaar en komen samen op maandag binnen
    expect(f.rows[7].shopifyInCents).toBe(Math.round(3 * 2900 * 0.86 * 100));
  });

  it("alleen wat al klaarstaat", () => {
    const f = forecast({ ...base, salesPerDayCents: 0, paypalPerDayCents: 0 });
    expect(f.rows.slice(4).every((r) => r.shopifyInCents === 0)).toBe(true);
    expect(f.endBalanceCents).toBeLessThan(forecast(base).endBalanceCents);
  });

  it("waarschuwt onder buffer en onder nul", () => {
    const f = forecast({ ...base, bankCents: 0, payoutScheduledCents: 0, pendingCents: 0 });
    expect(f.belowZero).toBe(true);
    expect(f.belowBuffer).toBe(true);
  });

  it("30 dagen draait zonder fouten", () => {
    const f = forecast({ ...base, days: 30 });
    expect(f.rows).toHaveLength(30);
    expect(f.rows.filter((r) => !r.workday).every((r) => r.shopifyInCents === 0)).toBe(true);
  });
});
