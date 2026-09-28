import { moneyStringToCents } from "./money";

const API_VERSION = process.env.SHOPIFY_API_VERSION ?? "2026-07";

export class ShopifyNotConfiguredError extends Error {
  constructor() {
    super("Shopify is niet gekoppeld: zet SHOPIFY_STORE_DOMAIN en SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET (of SHOPIFY_ADMIN_TOKEN)");
  }
}

export function shopifyConfigured(): boolean {
  return Boolean(
    process.env.SHOPIFY_STORE_DOMAIN &&
      (process.env.SHOPIFY_ADMIN_TOKEN || (process.env.SHOPIFY_CLIENT_ID && process.env.SHOPIFY_CLIENT_SECRET)),
  );
}

let cachedToken: { value: string; expiresAt: number } | null = null;

/**
 * Toegangstoken voor de Admin API.
 * - Oude custom app in de Shopify-admin: vaste token in SHOPIFY_ADMIN_TOKEN.
 * - App uit het Dev Dashboard (standaard sinds 2026): Client ID + Secret, token via client credentials (24 uur geldig).
 */
async function accessToken(domain: string): Promise<string> {
  if (process.env.SHOPIFY_ADMIN_TOKEN) return process.env.SHOPIFY_ADMIN_TOKEN;
  const id = process.env.SHOPIFY_CLIENT_ID;
  const secret = process.env.SHOPIFY_CLIENT_SECRET;
  if (!id || !secret) throw new ShopifyNotConfiguredError();
  if (cachedToken && cachedToken.expiresAt > Date.now() + 60_000) return cachedToken.value;
  const res = await fetch(`https://${domain}/admin/oauth/access_token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ grant_type: "client_credentials", client_id: id, client_secret: secret }),
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`Shopify inloggen mislukt (${res.status}). Controleer Client ID, Secret en of de app op de winkel is geïnstalleerd.`);
  const json = (await res.json()) as { access_token: string; expires_in?: number };
  cachedToken = { value: json.access_token, expiresAt: Date.now() + (json.expires_in ?? 86_400) * 1000 };
  return json.access_token;
}

type GraphQLResponse<T> = {
  data?: T;
  errors?: { message: string; extensions?: { code?: string } }[];
};

/** Admin GraphQL-call met retry bij throttling (Shopify rate limits). */
export async function shopifyGraphQL<T>(query: string, variables: Record<string, unknown> = {}): Promise<T> {
  const domain = process.env.SHOPIFY_STORE_DOMAIN;
  if (!domain) throw new ShopifyNotConfiguredError();
  const token = await accessToken(domain);

  for (let attempt = 0; ; attempt++) {
    const res = await fetch(`https://${domain}/admin/api/${API_VERSION}/graphql.json`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Shopify-Access-Token": token },
      body: JSON.stringify({ query, variables }),
      cache: "no-store",
    });

    if ((res.status === 429 || res.status >= 500) && attempt < 5) {
      await sleep(1000 * 2 ** attempt);
      continue;
    }
    if (!res.ok) throw new Error(`Shopify API ${res.status}: ${await res.text()}`);

    const json = (await res.json()) as GraphQLResponse<T>;
    const throttled = json.errors?.some((e) => e.extensions?.code === "THROTTLED");
    if (throttled && attempt < 5) {
      await sleep(1000 * 2 ** attempt);
      continue;
    }
    if (json.errors?.length) throw new Error(json.errors.map((e) => e.message).join("; "));
    return json.data as T;
  }
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

// ---------------------------------------------------------------------------
// Queries

export const PRODUCTS_QUERY = /* GraphQL */ `
  query Products($after: String, $query: String) {
    products(first: 50, after: $after, query: $query, sortKey: UPDATED_AT) {
      pageInfo { hasNextPage endCursor }
      nodes {
        legacyResourceId
        title
        handle
        status
        vendor
        productType
        updatedAt
        featuredMedia { preview { image { url(transform: { maxWidth: 160 }) } } }
        variants(first: 100) {
          nodes { legacyResourceId title sku price }
        }
      }
    }
  }
`;

export type ShopifyProduct = {
  legacyResourceId: string;
  title: string;
  handle: string;
  status: string;
  vendor: string;
  productType: string;
  updatedAt: string;
  featuredMedia: { preview: { image: { url: string } | null } | null } | null;
  variants: { nodes: { legacyResourceId: string; title: string; sku: string | null; price: string }[] };
};

export const ORDERS_QUERY = /* GraphQL */ `
  query Orders($after: String, $query: String) {
    orders(first: 50, after: $after, query: $query, sortKey: UPDATED_AT) {
      pageInfo { hasNextPage endCursor }
      nodes {
        legacyResourceId
        name
        createdAt
        updatedAt
        cancelledAt
        test
        currencyCode
        presentmentCurrencyCode
        displayFinancialStatus
        currentTotalPriceSet { shopMoney { amount } }
        currentTotalTaxSet { shopMoney { amount } }
        currentTotalDiscountsSet { shopMoney { amount } }
        totalShippingPriceSet { shopMoney { amount } }
        totalRefundedSet { shopMoney { amount } }
        shippingAddress { countryCodeV2 }
        transactions(first: 20) {
          kind
          status
          amountSet {
            shopMoney { amount currencyCode }
            presentmentMoney { amount currencyCode }
          }
          fees {
            type
            amount { amount currencyCode }
          }
        }
        lineItems(first: 100) {
          nodes {
            id
            title
            variantTitle
            quantity
            currentQuantity
            originalUnitPriceSet { shopMoney { amount } }
            product { legacyResourceId }
            variant { legacyResourceId }
          }
        }
      }
    }
  }
`;

type Money = { amount: string; currencyCode: string };

export type ShopifyTransaction = {
  kind: string;
  status: string;
  amountSet: { shopMoney: Money; presentmentMoney: Money };
  fees: { type: string; amount: Money }[];
};

export type ShopifyOrder = {
  legacyResourceId: string;
  name: string;
  createdAt: string;
  updatedAt: string;
  cancelledAt: string | null;
  test: boolean;
  currencyCode: string;
  presentmentCurrencyCode: string;
  displayFinancialStatus: string | null;
  currentTotalPriceSet: { shopMoney: { amount: string } };
  currentTotalTaxSet: { shopMoney: { amount: string } };
  currentTotalDiscountsSet: { shopMoney: { amount: string } };
  totalShippingPriceSet: { shopMoney: { amount: string } };
  totalRefundedSet: { shopMoney: { amount: string } };
  shippingAddress: { countryCodeV2: string | null } | null;
  transactions: ShopifyTransaction[];
  lineItems: {
    nodes: {
      id: string;
      title: string;
      variantTitle: string | null;
      quantity: number;
      currentQuantity: number;
      originalUnitPriceSet: { shopMoney: { amount: string } };
      product: { legacyResourceId: string } | null;
      variant: { legacyResourceId: string } | null;
    }[];
  };
};

/**
 * Tel Shopify Payments-fees op in de winkelvaluta.
 * Let op: Shopify rapporteert fees in de valuta waarin de klant betaalde (GBP, PLN, NOK, ...),
 * dus we rekenen om met de koers van de transactie zelf (shopMoney / presentmentMoney).
 * Geeft null als er geen fee-informatie is (bv. PayPal), zodat een schatting gebruikt wordt.
 */
export function feesFromTransactions(
  transactions: ShopifyTransaction[],
  shopCurrency: string,
): { feesCents: number; fxFeesCents: number } | null {
  let fees = 0;
  let fx = 0;
  let seen = false;
  for (const t of transactions) {
    if (t.status !== "SUCCESS" || !t.fees.length) continue;
    const shop = Number(t.amountSet.shopMoney.amount);
    const presentment = Number(t.amountSet.presentmentMoney.amount);
    const rate = presentment > 0 ? shop / presentment : 1;
    for (const f of t.fees) {
      seen = true;
      const amount = Number(f.amount.amount);
      const inShopCurrency = f.amount.currencyCode === shopCurrency ? amount : amount * rate;
      fees += inShopCurrency;
      if (f.type === "foreign_exchange_fee") fx += inShopCurrency;
    }
  }
  return seen ? { feesCents: Math.round(fees * 100), fxFeesCents: Math.round(fx * 100) } : null;
}

export function mapOrder(o: ShopifyOrder) {
  const fees = feesFromTransactions(o.transactions, o.currencyCode);
  return {
    id: o.legacyResourceId,
    name: o.name,
    createdAt: new Date(o.createdAt),
    currency: o.currencyCode,
    presentmentCurrency: o.presentmentCurrencyCode,
    totalCents: moneyStringToCents(o.currentTotalPriceSet.shopMoney.amount),
    taxCents: moneyStringToCents(o.currentTotalTaxSet.shopMoney.amount),
    shippingCents: moneyStringToCents(o.totalShippingPriceSet.shopMoney.amount),
    discountCents: moneyStringToCents(o.currentTotalDiscountsSet.shopMoney.amount),
    refundedCents: moneyStringToCents(o.totalRefundedSet.shopMoney.amount),
    feesCents: fees?.feesCents ?? null,
    fxFeesCents: fees?.fxFeesCents ?? null,
    financialStatus: o.displayFinancialStatus,
    cancelledAt: o.cancelledAt ? new Date(o.cancelledAt) : null,
    countryCode: o.shippingAddress?.countryCodeV2 ?? null,
    test: o.test,
    shopifyUpdatedAt: new Date(o.updatedAt),
  };
}

export function gidToId(gid: string): string {
  return gid.slice(gid.lastIndexOf("/") + 1);
}
