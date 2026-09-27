import { db } from "./db";
import { moneyStringToCents } from "./money";
import {
  ORDERS_QUERY,
  PRODUCTS_QUERY,
  gidToId,
  mapOrder,
  shopifyGraphQL,
  type ShopifyOrder,
  type ShopifyProduct,
} from "./shopify";
import { getSetting, setSetting } from "./settings";

type Page<T> = { pageInfo: { hasNextPage: boolean; endCursor: string | null }; nodes: T[] };

/** Marge zodat orders die tijdens een sync wijzigen niet gemist worden. */
const OVERLAP_MS = 10 * 60 * 1000;

async function withLog(kind: string, fn: () => Promise<number>) {
  const log = await db.syncLog.create({ data: { kind, status: "running" } });
  try {
    const count = await fn();
    await db.syncLog.update({ where: { id: log.id }, data: { status: "ok", count, finishedAt: new Date() } });
    return count;
  } catch (e) {
    const message = e instanceof Error ? e.message : String(e);
    await db.syncLog.update({ where: { id: log.id }, data: { status: "error", message, finishedAt: new Date() } });
    throw e;
  }
}

function updatedSinceQuery(since: string | null) {
  return since ? `updated_at:>'${since}'` : null;
}

export async function syncProducts({ full = false } = {}): Promise<number> {
  return withLog("products", async () => {
    const startedAt = new Date();
    const since = full ? null : await getSetting("sync.products.since");
    let after: string | null = null;
    let count = 0;

    do {
      const data: { products: Page<ShopifyProduct> } = await shopifyGraphQL(PRODUCTS_QUERY, {
        after,
        query: updatedSinceQuery(since),
      });
      for (const p of data.products.nodes) {
        const product = {
          title: p.title,
          handle: p.handle,
          status: p.status,
          vendor: p.vendor,
          productType: p.productType || null,
          imageUrl: p.featuredMedia?.preview?.image?.url ?? null,
          shopifyUpdatedAt: new Date(p.updatedAt),
        };
        await db.$transaction([
          db.product.upsert({
            where: { id: p.legacyResourceId },
            create: { id: p.legacyResourceId, ...product },
            update: product,
          }),
          ...p.variants.nodes.map((v) =>
            db.variant.upsert({
              where: { id: v.legacyResourceId },
              create: {
                id: v.legacyResourceId,
                productId: p.legacyResourceId,
                title: v.title,
                sku: v.sku,
                priceCents: moneyStringToCents(v.price),
              },
              update: { title: v.title, sku: v.sku, priceCents: moneyStringToCents(v.price) },
            }),
          ),
        ]);
        count++;
      }
      after = data.products.pageInfo.hasNextPage ? data.products.pageInfo.endCursor : null;
    } while (after);

    await setSetting("sync.products.since", new Date(startedAt.getTime() - OVERLAP_MS).toISOString());
    return count;
  });
}

export async function syncOrders({ full = false } = {}): Promise<number> {
  return withLog("orders", async () => {
    const startedAt = new Date();
    const since = full ? null : await getSetting("sync.orders.since");
    // Eerste/volledige sync: alle orders vanaf SYNC_ORDERS_FROM (standaard: alles wat de token mag zien).
    const from = process.env.SYNC_ORDERS_FROM;
    const query = since ? updatedSinceQuery(since) : from ? `created_at:>='${from}'` : null;
    let after: string | null = null;
    let count = 0;

    do {
      const data: { orders: Page<ShopifyOrder> } = await shopifyGraphQL(ORDERS_QUERY, {
        after,
        query,
      });

      // Line items kunnen verwijzen naar producten die (nog) niet gesynct of verwijderd zijn.
      const productIds = new Set(
        data.orders.nodes.flatMap((o) => o.lineItems.nodes.map((li) => li.product?.legacyResourceId).filter(Boolean)),
      ) as Set<string>;
      const variantIds = new Set(
        data.orders.nodes.flatMap((o) => o.lineItems.nodes.map((li) => li.variant?.legacyResourceId).filter(Boolean)),
      ) as Set<string>;
      const [knownProducts, knownVariants] = await Promise.all([
        db.product.findMany({ where: { id: { in: [...productIds] } }, select: { id: true } }),
        db.variant.findMany({ where: { id: { in: [...variantIds] } }, select: { id: true } }),
      ]);
      const hasProduct = new Set(knownProducts.map((p) => p.id));
      const hasVariant = new Set(knownVariants.map((v) => v.id));

      for (const o of data.orders.nodes) {
        const order = mapOrder(o);
        const lineItems = o.lineItems.nodes.map((li) => {
          const productId = li.product?.legacyResourceId ?? null;
          const variantId = li.variant?.legacyResourceId ?? null;
          return {
            id: gidToId(li.id),
            orderId: order.id,
            productId: productId && hasProduct.has(productId) ? productId : null,
            variantId: variantId && hasVariant.has(variantId) ? variantId : null,
            title: li.title,
            variantTitle: li.variantTitle,
            quantity: li.quantity,
            currentQuantity: li.currentQuantity,
            unitPriceCents: moneyStringToCents(li.originalUnitPriceSet.shopMoney.amount),
          };
        });
        await db.$transaction([
          db.order.upsert({ where: { id: order.id }, create: order, update: { ...order, syncedAt: new Date() } }),
          db.lineItem.deleteMany({ where: { orderId: order.id } }),
          db.lineItem.createMany({ data: lineItems }),
        ]);
        count++;
      }
      after = data.orders.pageInfo.hasNextPage ? data.orders.pageInfo.endCursor : null;
    } while (after);

    await setSetting("sync.orders.since", new Date(startedAt.getTime() - OVERLAP_MS).toISOString());
    return count;
  });
}

/** Producten eerst, zodat line items aan producten gekoppeld kunnen worden. */
export async function syncAll({ full = false } = {}) {
  const products = await syncProducts({ full });
  const orders = await syncOrders({ full });
  return { products, orders };
}
