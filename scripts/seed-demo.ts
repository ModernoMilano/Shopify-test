/**
 * Demo-data om de schermen te bekijken zonder Shopify-koppeling.
 * Verzonnen cijfers. Niet draaien op de productiedatabase.
 */
import { db } from "../src/lib/db";

const NAMES = ["MILANO RIVIERA SHORT - NAVY", "MILANO CASHMERE LOUNGE SET - GRAY", "MILANO KNITTED VEST - BROWN", "MILANO REVERSO SABBIA SET", "COMO LOAFER - COGNAC", "PORTOFINO PANTALON - BEIGE"];
const PRICES = [5000, 15000, 6000, 14000, 11000, 8000];

async function main() {
  if (process.env.NODE_ENV === "production") throw new Error("Niet in productie draaien");
  await db.lineItem.deleteMany();
  await db.order.deleteMany();
  await db.costRule.deleteMany();
  await db.variant.deleteMany();
  await db.product.deleteMany();
  await db.adSpend.deleteMany();
  await db.expense.deleteMany();
  await db.supplier.deleteMany();

  const sup = await db.supplier.create({ data: { name: "Demo leverancier", country: "CN", processingDays: 3, shippingDays: 8 } });
  for (let i = 0; i < NAMES.length; i++) {
    await db.product.create({
      data: {
        id: String(1000 + i),
        title: NAMES[i],
        status: "ACTIVE",
        supplierId: i < 4 ? sup.id : null,
        variants: { create: ["S", "M", "L"].map((s, j) => ({ id: `${1000 + i}${j}`, title: s, priceCents: PRICES[i] })) },
      },
    });
    if (i < 5) {
      await db.costRule.create({
        data: { productId: String(1000 + i), unitCostCents: Math.round(PRICES[i] * 0.28), shippingCostCents: 700, validFrom: new Date("2000-01-01") },
      });
    }
  }

  let seq = 1;
  const now = Date.now();
  for (let d = 0; d < 60; d++) {
    const day = new Date(now - d * 86_400_000);
    const n = 8 + Math.round(Math.random() * 10);
    for (let k = 0; k < n; k++) {
      const i = Math.floor(Math.random() * NAMES.length);
      const qty = Math.random() < 0.15 ? 2 : 1;
      const total = PRICES[i] * qty;
      const tax = Math.random() < 0.5 ? Math.round(total - total / 1.21) : 0;
      const id = String(900000 + seq);
      await db.order.create({
        data: {
          id,
          name: `#${470000 + seq++}`,
          createdAt: new Date(day.getTime() - Math.random() * 20 * 3_600_000),
          currency: "EUR",
          presentmentCurrency: Math.random() < 0.3 ? "GBP" : "EUR",
          totalCents: total,
          taxCents: tax,
          shippingCents: 0,
          discountCents: 0,
          refundedCents: 0,
          feesCents: Math.round(total * 0.035),
          fxFeesCents: Math.round(total * 0.012),
          financialStatus: "PAID",
          countryCode: ["GB", "DE", "NL", "US"][Math.floor(Math.random() * 4)],
          shopifyUpdatedAt: day,
          lineItems: {
            create: [{ id: `${id}1`, productId: String(1000 + i), variantId: `${1000 + i}1`, title: NAMES[i], quantity: qty, currentQuantity: qty, unitPriceCents: PRICES[i] }],
          },
        },
      });
    }
    await db.adSpend.create({
      data: { date: new Date(day.toISOString().slice(0, 10)), channel: "meta", amountCents: 45000 + Math.round(Math.random() * 30000) },
    });
  }
  await db.expense.createMany({
    data: [
      { name: "Shopify", category: "shopify", amountCents: 3900, startDate: new Date("2026-01-01") },
      { name: "Klaviyo", category: "software", amountCents: 15000, startDate: new Date("2026-01-01") },
      { name: "Gorgias", category: "software", amountCents: 6000, startDate: new Date("2026-01-01") },
    ],
  });
  console.log("Demo-data geladen");
}

main().finally(() => db.$disconnect());
