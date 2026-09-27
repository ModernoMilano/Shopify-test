import { db } from "@/lib/db";
import { dayKey } from "@/lib/period";
import { shopifyConfigured } from "@/lib/shopify";
import { syncAll as syncShopifyCatalog } from "@/lib/sync";
import { addDaysKey } from "./calculations";
import { fetchWindsorMeta, marketOf } from "./meta";
import { syncDailySales, syncShopifyPayments } from "./shopify-finance";

export type SourceResult = { source: string; label: string; ok: boolean; message: string };

const msg = (e: unknown) => (e instanceof Error ? e.message : String(e));

/** Synct alle bronnen onafhankelijk van elkaar; een fout bij de ene bron stopt de andere niet. */
export async function syncAllSources(): Promise<SourceResult[]> {
  const today = dayKey(new Date());
  const from = addDaysKey(today, -35);
  const results: SourceResult[] = [];

  if (shopifyConfigured()) {
    try {
      const n = await syncDailySales(from, today);
      results.push({ source: "shopify_sales", label: "Shopify omzet", ok: true, message: `${n} dagen bijgewerkt` });
    } catch (e) {
      results.push({ source: "shopify_sales", label: "Shopify omzet", ok: false, message: msg(e) });
    }
    try {
      const r = await syncShopifyPayments();
      results.push({ source: "shopify_payments", label: "Shopify Payments", ok: true, message: `${r.payouts} payouts, ${r.disputes} disputes` });
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
    results.push({ source: "shopify", label: "Shopify", ok: false, message: "Niet gekoppeld: zet SHOPIFY_STORE_DOMAIN en SHOPIFY_ADMIN_TOKEN" });
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
      await db.sourceSync.upsert({
        where: { source: "windsor" },
        create: { source: "windsor", lastAt: new Date(), status: "ok" },
        update: { lastAt: new Date(), status: "ok", message: null },
      });
      results.push({ source: "windsor", label: "Meta (Windsor.ai)", ok: true, message: `${rows.length} campagnedagen` });
    } catch (e) {
      results.push({ source: "windsor", label: "Meta (Windsor.ai)", ok: false, message: msg(e) });
    }
  } else {
    results.push({ source: "windsor", label: "Meta (Windsor.ai)", ok: false, message: "Niet gekoppeld: zet WINDSOR_API_KEY" });
  }

  results.push({ source: "paypal", label: "PayPal", ok: false, message: "Nog niet gekoppeld (fase 3). Saldo en fees handmatig." });
  results.push({ source: "revolut", label: "Revolut", ok: true, message: "Via import van het afschrift (PDF of CSV) bij Bankmutaties" });
  return results;
}
