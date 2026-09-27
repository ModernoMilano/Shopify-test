/**
 * Laadt de testset van september 2026 (spec sectie 5).
 *
 * - Dagomzet augustus en 1 t/m 26 september: echte cijfers uit Shopify (scripts/data).
 * - 27 september: momentopname uit de spec (499 orders, totale omzet € 93.384,19 over 1 t/m 27 sept).
 * - Revolut: het echte afschrift uit fixtures/private (niet in git), of een pad als argument.
 * - Payouts, saldi, PayPal-fees en lening: startwaarden uit de spec, gemarkeerd als handmatig.
 *
 * Gebruik: npm run db:seed:september [-- pad/naar/afschrift.pdf]
 * Wist alleen de financiële tabellen, niet producten of orders.
 */
import fs from "node:fs";
import path from "node:path";
import { db } from "../src/lib/db";
import { importStatement } from "../src/bank/import";
import { setSetting } from "../src/lib/settings";
import daily from "./data/shopify-daily-2026-08-09.json";
import meta from "./data/meta-2026-09.json";
import { marketOf } from "../src/finance/meta";

const c = (s: string | number) => Math.round(Number(s) * 100);
const d = (key: string) => new Date(`${key}T00:00:00Z`);

async function main() {
  await db.$transaction([
    db.bankTransaction.deleteMany(),
    db.bankImport.deleteMany(),
    db.categoryRule.deleteMany(),
    db.dailySales.deleteMany(),
    db.shopifyPayout.deleteMany(),
    db.moneySnapshot.deleteMany(),
    db.manualEntry.deleteMany(),
    db.loan.deleteMany(),
    db.supplierInvoice.deleteMany(),
    db.sourceSync.deleteMany(),
    db.metaDaily.deleteMany(),
  ]);

  // --- omzet
  await db.dailySales.createMany({
    data: daily.days.map((r) => ({
      date: d(r.date),
      orders: r.orders,
      grossCents: c(r.gross),
      discountCents: c(r.discounts),
      returnsCents: c(r.returns),
      netCents: c(r.net),
      shippingCents: c(r.shipping),
      taxesCents: c(r.taxes),
      totalCents: c(r.total),
      source: "shopify",
    })),
  });
  // 27 sept: verschil tussen de spec (1 t/m 27) en Shopify (1 t/m 26)
  const sept = daily.days.filter((r) => r.date >= "2026-09-01");
  const sum = (k: "orders" | "gross" | "discounts" | "returns" | "net" | "shipping" | "taxes" | "total") =>
    sept.reduce((s, r) => s + (k === "orders" ? r.orders : c(r[k])), 0);
  await db.dailySales.create({
    data: {
      date: d("2026-09-27"),
      orders: 499 - sum("orders"),
      grossCents: c(87020.75) - sum("gross"),
      discountCents: c(-1008.36) - sum("discounts"),
      returnsCents: c(-252.08) - sum("returns"),
      netCents: c(85760.31) - sum("net"),
      shippingCents: c(142.47) - sum("shipping"),
      taxesCents: c(7481.41) - sum("taxes"),
      totalCents: c(93384.19) - sum("total"),
      source: "seed",
    },
  });

  // --- Meta (echte cijfers uit Windsor.ai)
  await db.metaDaily.createMany({
    data: meta.rows.map((r) => ({
      date: d(r.date),
      campaign: r.campaign,
      market: marketOf(r.campaign),
      spendCents: c(r.spend),
      clicks: r.clicks,
      impressions: r.impressions,
      purchases: r.purchases,
      purchaseValueCents: c(r.value),
      frequency: r.frequency,
      source: "windsor",
    })),
  });

  // --- bank
  const file = process.argv[2] ?? path.join(process.cwd(), "fixtures/private/revolut-2026-09.pdf");
  if (fs.existsSync(file)) {
    const r = await importStatement(path.basename(file), new Uint8Array(fs.readFileSync(file)));
    console.log(`Revolut: ${r.imported} mutaties, sluit: ${r.reconciled ? "ja" : "nee"}, onbekend: ${r.unknown}`);

    // Ok en Sona hebben geen regel; in de spec vallen ze onder software en tools
    await db.bankTransaction.updateMany({
      where: { description: { in: ["Ok", "Sona"] }, category: "unknown" },
      data: { category: "software", categorySource: "handmatig", note: "toegewezen volgens spec 5.3" },
    });
    // De drie Facebook-afschrijvingen van 1 sept (€ 1.450,60) horen bij 31 augustus
    await db.bankTransaction.updateMany({
      where: { category: "meta", bookedAt: d("2026-09-01") },
      data: { periodDate: d("2026-08-31"), note: "Meta-rekening van 31 augustus" },
    });
  } else {
    console.log(`Geen afschrift gevonden op ${file}; bankmutaties overgeslagen. Importeer het via Bankmutaties.`);
  }

  // --- Shopify payouts 1 t/m 26 sept, samengevat (spec 5.4). Een echte import vervangt deze rij.
  await db.shopifyPayout.create({
    data: {
      payoutDate: d("2026-09-26"),
      summaryUntil: d("2026-09-26"),
      status: "paid",
      chargesCents: c(68395.46),
      refundsCents: c(-70),
      adjustmentsCents: c(-3581.65),
      reservedFundsCents: c(-6503.69),
      feesCents: c(2831.79),
      retriedCents: c(1525.44),
      totalCents: c(56903.77),
      source: "seed",
    },
  });

  await db.manualEntry.create({
    data: {
      kind: "paypal_fees",
      label: "PayPal fees september",
      amountCents: c(3700) - c(2831.79),
      periodStart: d("2026-09-01"),
      periodEnd: d("2026-09-27"),
      note: "Afgeleid: fees totaal € 3.700 (spec 5.2) minus Shopify-fees € 2.831,79. Vervangen zodra PayPal gekoppeld is.",
    },
  });

  // --- saldi
  await db.moneySnapshot.create({
    data: {
      takenAt: new Date("2026-09-01T00:00:00Z"),
      bankCents: c(1836.01),
      payoutScheduledCents: 0,
      pendingCents: c(7677),
      holdCents: 0,
      paypalCents: 0,
      note: "Begin september: Shopify pending + hold samen € 7.677 (niet gesplitst)",
    },
  });
  await db.moneySnapshot.create({
    data: {
      takenAt: new Date("2026-09-27T12:00:00Z"),
      bankCents: c(8411.16),
      payoutScheduledCents: c(2658),
      payoutScheduledDate: d("2026-09-28"),
      pendingCents: c(10402),
      holdCents: c(8983),
      paypalCents: c(200),
      note: "Spec 5.5. PayPal-saldo is een schatting.",
    },
  });

  await db.loan.create({
    data: { lender: "HR RJ Komen", principalCents: c(10000), startDate: d("2026-09-04"), schedule: "nog vast te leggen" },
  });

  await setSetting(
    "control.2026-08",
    JSON.stringify({
      revenueCents: c(43737),
      costsCents: c(41196),
      profitCents: c(2541),
      breakEvenRoas: 2.09,
      roas: 2.38,
      shopifyFeesCents: c(1494.85),
      note: "Elders is ongeveer € 9.000 winst over augustus genoemd. Deze cijfers spreken elkaar tegen: nog bevestigen.",
    }),
  );

  console.log("Septemberset geladen.");
}

main().finally(() => db.$disconnect());
