import { db } from "@/lib/db";
import { dayKey } from "@/lib/period";
import { shopifyConfigured } from "@/lib/shopify";
import { syncAll as syncShopifyCatalog } from "@/lib/sync";
import { addDaysKey } from "./calculations";
import { fetchWindsorMeta, marketOf } from "./meta";
import { syncDailySales, syncShopifyPayments, type ShopifyPosition } from "./shopify-finance";
import { fetchPaypalBalance, fetchPaypalTransactions, paypalConfigured, summarizePaypal, type PaypalTransaction } from "./paypal";

export type SourceResult = { source: string; label: string; ok: boolean; message: string };

const msg = (e: unknown) => (e instanceof Error ? e.message : String(e));
const eur = (cents: number) => (cents / 100).toFixed(2).replace(".", ",");

async function markSync(source: string, ok: boolean, message: string) {
  await db.sourceSync.upsert({
    where: { source },
    create: { source, lastAt: new Date(), status: ok ? "ok" : "fout", message },
    update: ok ? { lastAt: new Date(), status: "ok", message } : { status: "fout", message },
  });
}

/** PayPal: dagtotalen van de afgelopen periode en het huidige saldo in EUR. */
async function syncPaypal(fromKey: string): Promise<{ message: string; balanceCents: number | null }> {
  const txs = await fetchPaypalTransactions(`${fromKey}T00:00:00Z`, new Date().toISOString());
  const byDay = new Map<string, PaypalTransaction[]>();
  for (const t of txs) {
    const k = dayKey(new Date(t.date));
    byDay.set(k, [...(byDay.get(k) ?? []), t]);
  }
  for (const [k, list] of byDay) {
    const s = summarizePaypal(list);
    const date = new Date(`${k}T00:00:00Z`);
    const data = {
      salesCents: s.salesCents,
      salesCount: s.salesCount,
      feesCents: s.feesCents,
      refundsCents: s.refundsCents,
      withdrawalsCents: s.withdrawalsCents,
      syncedAt: new Date(),
    };
    await db.paypalDaily.upsert({ where: { date }, create: { date, ...data }, update: data });
  }
  const balances = await fetchPaypalBalance();
  const euro = balances.find((b) => b.currency === "EUR");
  const other = balances.filter((b) => b.currency !== "EUR" && b.totalCents !== 0).map((b) => `${b.currency} ${eur(b.totalCents)}`);
  return {
    message: `${txs.length} transacties, saldo € ${euro ? eur(euro.totalCents) : "onbekend"}${euro?.withheldCents ? ` (waarvan € ${eur(euro.withheldCents)} vastgehouden)` : ""}${other.length ? `, ook ${other.join(", ")}` : ""}`,
    balanceCents: euro ? euro.totalCents : null,
  };
}

/**
 * Synct alle bronnen onafhankelijk van elkaar; een fout bij de ene bron stopt de andere niet.
 * Daarna één nieuwe stand van "waar het geld staat". Wat niet automatisch op te halen is,
 * wordt overgenomen van de vorige stand en blijft als "handmatig" gelabeld.
 */
export async function syncAllSources(): Promise<SourceResult[]> {
  const today = dayKey(new Date());
  const from = addDaysKey(today, -35);
  const results: SourceResult[] = [];
  let shopify: ShopifyPosition | null = null;
  let paypalBalance: number | null = null;

  if (shopifyConfigured()) {
    try {
      const n = await syncDailySales(from, today);
      results.push({ source: "shopify_sales", label: "Shopify omzet", ok: true, message: `${n} dagen bijgewerkt` });
    } catch (e) {
      results.push({ source: "shopify_sales", label: "Shopify omzet", ok: false, message: msg(e) });
    }
    try {
      shopify = await syncShopifyPayments();
      results.push({
        source: "shopify_payments",
        label: "Shopify Payments",
        ok: true,
        message: `${shopify.payouts} payouts, ${shopify.disputes} disputes, pending € ${eur(shopify.pendingCents)}${shopify.holdCents !== null ? `, reserve € ${eur(shopify.holdCents)}` : ""}`,
      });
    } catch (e) {
      results.push({ source: "shopify_payments", label: "Shopify Payments", ok: false, message: msg(e) });
    }
    try {
      const r = await syncShopifyCatalog();
      results.push({ source: "shopify_orders", label: "Shopify orders en producten", ok: true, message: `${r.orders} orders, ${r.products} producten` });
    } catch (e) {
      results.push({ source: "shopify_orders", label: "Shopify orders en producten", ok: false, message: msg(e) });
    }
  } else {
    results.push({ source: "shopify", label: "Shopify", ok: false, message: "Niet gekoppeld: zet SHOPIFY_STORE_DOMAIN en SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET" });
  }

  if (process.env.WINDSOR_API_KEY) {
    try {
      const rows = await fetchWindsorMeta(from, today);
      for (const r of rows) {
        const date = new Date(`${r.date}T00:00:00Z`);
        const data = {
          market: marketOf(r.campaign),
          spendCents: r.spendCents,
          clicks: r.clicks,
          impressions: r.impressions,
          purchases: r.purchases,
          purchaseValueCents: r.purchaseValueCents,
          frequency: r.frequency,
          source: "windsor",
        };
        await db.metaDaily.upsert({ where: { date_campaign: { date, campaign: r.campaign } }, create: { date, campaign: r.campaign, ...data }, update: data });
      }
      const m = `${rows.length} campagnedagen`;
      await markSync("windsor", true, m);
      results.push({ source: "windsor", label: "Meta (Windsor.ai)", ok: true, message: m });
    } catch (e) {
      await markSync("windsor", false, msg(e));
      results.push({ source: "windsor", label: "Meta (Windsor.ai)", ok: false, message: msg(e) });
    }
  } else {
    results.push({ source: "windsor", label: "Meta (Windsor.ai)", ok: false, message: "Niet gekoppeld: zet WINDSOR_API_KEY" });
  }

  if (paypalConfigured()) {
    try {
      const r = await syncPaypal(from);
      paypalBalance = r.balanceCents;
      await markSync("paypal", true, r.message);
      results.push({ source: "paypal", label: "PayPal", ok: true, message: r.message });
    } catch (e) {
      await markSync("paypal", false, msg(e));
      results.push({ source: "paypal", label: "PayPal", ok: false, message: msg(e) });
    }
  } else {
    results.push({ source: "paypal", label: "PayPal", ok: false, message: "Niet gekoppeld: zet PAYPAL_CLIENT_ID en PAYPAL_SECRET" });
  }

  if (shopify || paypalBalance !== null) {
    const last = await db.moneySnapshot.findFirst({ orderBy: { takenAt: "desc" } });
    const hold = shopify?.holdCents ?? null;
    await db.moneySnapshot.create({
      data: {
        payoutScheduledCents: shopify?.payoutScheduledCents ?? last?.payoutScheduledCents ?? 0,
        payoutScheduledDate: shopify ? shopify.payoutScheduledDate : (last?.payoutScheduledDate ?? null),
        pendingCents: shopify?.pendingCents ?? last?.pendingCents ?? 0,
        holdCents: hold ?? last?.holdCents ?? 0,
        paypalCents: paypalBalance ?? last?.paypalCents ?? 0,
        source: "automatisch",
        shopifySource: shopify ? "Shopify" : (last?.shopifySource ?? "handmatig"),
        holdSource: hold !== null ? "Shopify" : (last?.holdSource ?? "handmatig"),
        paypalSource: paypalBalance !== null ? "PayPal" : (last?.paypalSource ?? "handmatig"),
      },
    });
  }

  results.push({ source: "revolut", label: "Revolut", ok: true, message: "Via upload van het afschrift (PDF of CSV)" });
  return results;
}
