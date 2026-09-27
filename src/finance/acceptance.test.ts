/**
 * Acceptatie (spec sectie 11) tegen de database met de septemberset.
 * Draait alleen na `npm run db:seed:september` met het echte afschrift in fixtures/private.
 */
import fs from "node:fs";
import path from "node:path";
import { afterAll, describe, expect, it } from "vitest";
import { db } from "@/lib/db";
import { moneyNow, periodBridge, periodFinance } from "./data";

const hasFixture = fs.existsSync(path.join(process.cwd(), "fixtures/private/revolut-2026-09.pdf"));
const seeded = hasFixture && !!process.env.DATABASE_URL && (await db.bankTransaction.count().catch(() => 0)) === 159;

describe.skipIf(!seeded)("septemberset in de database", () => {
  const sept = { fromKey: "2026-09-01", toKey: "2026-09-27" };
  afterAll(() => db.$disconnect());

  it("overzicht: omzet, MER en posten", async () => {
    const f = await periodFinance(sept);
    const eur = (c: number) => c / 100;
    expect(eur(f.pnl.revenueCents)).toBe(93384.19);
    expect(f.pnl.orders).toBe(499);
    expect(eur(f.pnl.cogsCents)).toBe(31095.6);
    expect(eur(f.pnl.metaCents)).toBe(33798.09); // excl. € 1.450,60 voor 31 augustus
    expect(eur(f.pnl.feesCents)).toBe(3700);
    expect(eur(f.pnl.chargebacksCents)).toBe(3581.65);
    expect(f.pnl.mer!.toFixed(2)).toBe("2.76");
    // Bank: software 1.022,64 + freelancers 346,12 + boekhouder 88,21 + bankkosten 20,36.
    // De spec noemt € 1.717 voor deze post; het verschil van € 239,67 staat niet op het afschrift.
    expect(eur(f.pnl.otherCents)).toBe(1477.33);
    expect(eur(f.pnl.profitCents)).toBe(19731.52);
  });

  it("waar het geld staat: € 30.654", async () => {
    const m = await moneyNow();
    expect(Math.round(m.totalCents / 100)).toBe(30654);
  });

  it("cash bridge eindigt op de groei van de bank (+€ 6.575,15)", async () => {
    const f = await periodFinance(sept);
    const b = await periodBridge(sept, f.pnl.profitCents, f.bank);
    expect(b.bankGrowth).toBe(657515);
    expect(b.shopifyGrowth).toBe(1436600);
    expect(b.steps.reduce((s, x) => s + x.cents, 0)).toBe(b.bankGrowth);
    // met de spec-winst van € 19.490 zou timing −€ 1.543 zijn; met de bankdata is het:
    expect(b.timing).toBe(-178477);
    expect(b.missing).toEqual([]);
  });
});
