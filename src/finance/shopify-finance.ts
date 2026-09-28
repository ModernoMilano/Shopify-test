/**
 * Shopify-connectors voor het financiële dashboard:
 *  - dagomzet via ShopifyQL (scope read_reports)
 *  - Shopify Payments: saldo, payouts, reserve en disputes (scopes read_shopify_payments_payouts,
 *    read_shopify_payments_accounts, read_shopify_payments_disputes)
 */
import { db } from "@/lib/db";
import { shopifyGraphQL } from "@/lib/shopify";

const c = (s: string | number | null | undefined) => Math.round(Number(s ?? 0) * 100);

async function markSync(source: string, status: "ok" | "fout", message?: string) {
  await db.sourceSync.upsert({
    where: { source },
    create: { source, lastAt: new Date(), status, message },
    update: { lastAt: new Date(), status, message: message ?? null },
  });
}

const SALES_QUERY = /* GraphQL */ `
  query DailySales($q: String!) {
    shopifyqlQuery(query: $q) {
      tableData { columns { name dataType } rows }
      parseErrors
    }
  }
`;

type ShopifyqlResult = {
  shopifyqlQuery: {
    tableData: { columns: { name: string; dataType: string }[]; rows: unknown } | null;
    parseErrors: string[] | null;
  };
};

export async function syncDailySales(fromKey: string, toKey: string) {
  try {
    const q = `FROM sales SHOW orders, gross_sales, discounts, returns, net_sales, shipping_charges, taxes, total_sales TIMESERIES day SINCE ${fromKey} UNTIL ${toKey}`;
    const data = await shopifyGraphQL<ShopifyqlResult>(SALES_QUERY, { q });
    const res = data.shopifyqlQuery;
    if (res.parseErrors?.length) throw new Error(res.parseErrors.join("; "));
    if (!res.tableData) throw new Error("Geen data van ShopifyQL");
    const cols = res.tableData.columns.map((x) => x.name);
    const rows = (res.tableData.rows as unknown[]).map((r) =>
      Array.isArray(r) ? Object.fromEntries(cols.map((name, i) => [name, r[i]])) : (r as Record<string, unknown>),
    );
    for (const r of rows) {
      const key = String(r.day ?? "").slice(0, 10);
      if (!/^\d{4}-\d{2}-\d{2}$/.test(key)) continue;
      const data = {
        orders: Number(r.orders ?? 0),
        grossCents: c(r.gross_sales as string),
        discountCents: c(r.discounts as string),
        returnsCents: c(r.returns as string),
        netCents: c(r.net_sales as string),
        shippingCents: c(r.shipping_charges as string),
        taxesCents: c(r.taxes as string),
        totalCents: c(r.total_sales as string),
        source: "shopify",
        syncedAt: new Date(),
      };
      const date = new Date(`${key}T00:00:00Z`);
      await db.dailySales.upsert({ where: { date }, create: { date, ...data }, update: data });
    }
    await markSync("shopify_sales", "ok", `${rows.length} dagen`);
    return rows.length;
  } catch (e) {
    await markSync("shopify_sales", "fout", e instanceof Error ? e.message : String(e));
    throw e;
  }
}

const ACCOUNT_QUERY = /* GraphQL */ `
  query PaymentsAccount {
    shopifyPaymentsAccount {
      balance { amount currencyCode }
      disputes(first: 100) {
        nodes {
          legacyResourceId
          amount { amount }
          evidenceDueBy
          initiatedAt
          reasonDetails { reason }
          status
          order { name shippingAddress { countryCodeV2 } }
        }
      }
    }
  }
`;

const PAYOUTS_QUERY = /* GraphQL */ `
  query Payouts($after: String) {
    shopifyPaymentsAccount {
      payouts(first: 100, after: $after, reverse: true) {
        pageInfo { hasNextPage endCursor }
        nodes {
          legacyResourceId
          issuedAt
          status
          net { amount }
          summary {
            chargesGross { amount }
            chargesFee { amount }
            refundsFeeGross { amount }
            refundsFee { amount }
            adjustmentsGross { amount }
            adjustmentsFee { amount }
            reservedFundsGross { amount }
            reservedFundsFee { amount }
            retriedPayoutsGross { amount }
            retriedPayoutsFee { amount }
          }
        }
      }
    }
  }
`;

type Amt = { amount: string } | null;

type AccountResult = {
  shopifyPaymentsAccount: {
    balance: { amount: string; currencyCode: string }[];
    disputes: {
      nodes: {
        legacyResourceId: string;
        amount: Amt;
        evidenceDueBy: string | null;
        initiatedAt: string;
        reasonDetails: { reason: string } | null;
        status: string;
        order: { name: string; shippingAddress: { countryCodeV2: string | null } | null } | null;
      }[];
    };
  } | null;
};

type PayoutNode = {
  legacyResourceId: string;
  issuedAt: string;
  status: string;
  net: Amt;
  summary: Record<string, Amt>;
};

type PayoutsResult = {
  shopifyPaymentsAccount: {
    payouts: { pageInfo: { hasNextPage: boolean; endCursor: string | null }; nodes: PayoutNode[] };
  } | null;
};

export type ShopifyPosition = {
  payoutScheduledCents: number;
  payoutScheduledDate: Date | null;
  pendingCents: number;
  /** reserve afgeleid uit alle payouts (vastgehouden min vrijgegeven); null als dat niet betrouwbaar kan */
  holdCents: number | null;
  payouts: number;
  disputes: number;
};

export async function syncShopifyPayments(): Promise<ShopifyPosition> {
  try {
    const account = await shopifyGraphQL<AccountResult>(ACCOUNT_QUERY);
    const acc = account.shopifyPaymentsAccount;
    if (!acc) throw new Error("Geen toegang tot Shopify Payments (controleer de rechten van de app)");

    // alle payouts ophalen: de reserve is de optelsom van wat ooit is vastgehouden en vrijgegeven
    const payouts: PayoutNode[] = [];
    let after: string | null = null;
    do {
      const page: PayoutsResult = await shopifyGraphQL<PayoutsResult>(PAYOUTS_QUERY, { after });
      const conn = page.shopifyPaymentsAccount?.payouts;
      if (!conn) break;
      payouts.push(...conn.nodes);
      after = conn.pageInfo.hasNextPage ? conn.pageInfo.endCursor : null;
    } while (after);

    const s = (p: PayoutNode, k: string) => c(p.summary[k]?.amount);
    let scheduled = 0;
    let scheduledDate: Date | null = null;
    let reservedTotal = 0;
    for (const p of payouts) {
      const date = new Date(`${p.issuedAt.slice(0, 10)}T00:00:00Z`);
      const fees = ["chargesFee", "refundsFee", "adjustmentsFee", "reservedFundsFee", "retriedPayoutsFee"].reduce((sum, k) => sum + s(p, k), 0);
      const row = {
        payoutDate: date,
        status: p.status.toLowerCase(),
        chargesCents: s(p, "chargesGross"),
        refundsCents: s(p, "refundsFeeGross"),
        adjustmentsCents: s(p, "adjustmentsGross"),
        reservedFundsCents: s(p, "reservedFundsGross"),
        feesCents: Math.abs(fees),
        retriedCents: s(p, "retriedPayoutsGross"),
        totalCents: c(p.net?.amount),
        source: "api",
      };
      reservedTotal += row.reservedFundsCents;
      await db.shopifyPayout.upsert({ where: { externalId: p.legacyResourceId }, create: { externalId: p.legacyResourceId, ...row }, update: row });
      if (["scheduled", "in_transit"].includes(row.status)) {
        scheduled += row.totalCents;
        if (!scheduledDate || date < scheduledDate) scheduledDate = date;
      }
    }
    if (payouts.length) {
      // samengevatte startwaarden en CSV-imports overlappen met echte payouts
      await db.shopifyPayout.deleteMany({ where: { source: { in: ["seed", "csv"] } } });
    }

    for (const d of acc.disputes.nodes) {
      const row = {
        orderName: d.order?.name ?? null,
        openedAt: new Date(d.initiatedAt),
        amountCents: c(d.amount?.amount),
        reason: d.reasonDetails?.reason ?? null,
        status: d.status.toLowerCase(),
        dueBy: d.evidenceDueBy ? new Date(d.evidenceDueBy) : null,
        country: d.order?.shippingAddress?.countryCodeV2 ?? null,
        source: "shopify",
      };
      await db.dispute.upsert({ where: { id: d.legacyResourceId }, create: { id: d.legacyResourceId, ...row }, update: row });
    }

    const eur = acc.balance.find((b) => b.currencyCode === "EUR") ?? acc.balance[0];
    // vastgehouden bedragen staan als negatief bedrag in de payouts; vrijgaven als positief
    const hold = -reservedTotal;
    await markSync("shopify_payments", "ok", `${payouts.length} payouts, ${acc.disputes.nodes.length} disputes`);
    return {
      payoutScheduledCents: scheduled,
      payoutScheduledDate: scheduledDate,
      pendingCents: c(eur?.amount),
      holdCents: hold >= 0 ? hold : null,
      payouts: payouts.length,
      disputes: acc.disputes.nodes.length,
    };
  } catch (e) {
    await markSync("shopify_payments", "fout", e instanceof Error ? e.message : String(e));
    throw e;
  }
}
