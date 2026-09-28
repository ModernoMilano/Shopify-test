/**
 * PayPal-koppeling via de REST API (live).
 * Vereist PAYPAL_CLIENT_ID en PAYPAL_SECRET van een Live-app met Transaction Search aan.
 * Let op: nieuwe transacties staan pas na ongeveer 3 uur in de Transaction Search API.
 */

const BASE = process.env.PAYPAL_API_BASE ?? "https://api-m.paypal.com";

export function paypalConfigured(): boolean {
  return Boolean(process.env.PAYPAL_CLIENT_ID && process.env.PAYPAL_SECRET);
}

async function token(): Promise<string> {
  const id = process.env.PAYPAL_CLIENT_ID;
  const secret = process.env.PAYPAL_SECRET;
  if (!id || !secret) throw new Error("PAYPAL_CLIENT_ID en PAYPAL_SECRET zijn niet ingesteld");
  const res = await fetch(`${BASE}/v1/oauth2/token`, {
    method: "POST",
    headers: {
      Authorization: `Basic ${Buffer.from(`${id}:${secret}`).toString("base64")}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: "grant_type=client_credentials",
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`PayPal inloggen mislukt (${res.status}). Controleer de Client ID en Secret.`);
  return ((await res.json()) as { access_token: string }).access_token;
}

async function get<T>(path: string, accessToken: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { headers: { Authorization: `Bearer ${accessToken}` }, cache: "no-store" });
  if (res.status === 403) throw new Error("Geen toegang: zet Transaction Search aan bij de PayPal-app (kan tot 9 uur duren)");
  if (!res.ok) throw new Error(`PayPal API ${res.status}: ${(await res.text()).slice(0, 200)}`);
  return (await res.json()) as T;
}

type Money = { currency_code: string; value: string };

export type PaypalTransaction = {
  id: string;
  date: string;
  /** T-code van PayPal, bv. T0006 = checkout-betaling, T0400 = opname naar bank */
  eventCode: string;
  status: string;
  grossCents: number;
  feeCents: number;
  currency: string;
};

type SearchResponse = {
  transaction_details: {
    transaction_info: {
      transaction_id: string;
      transaction_event_code: string;
      transaction_initiation_date: string;
      transaction_amount: Money;
      fee_amount?: Money;
      transaction_status: string;
    };
  }[];
  total_pages: number;
  page: number;
};

const cents = (m?: Money) => (m ? Math.round(Number(m.value) * 100) : 0);

/** Transacties tussen twee datums. De API staat maximaal 31 dagen per aanvraag toe. */
export async function fetchPaypalTransactions(fromIso: string, toIso: string): Promise<PaypalTransaction[]> {
  const t = await token();
  const out: PaypalTransaction[] = [];
  let start = new Date(fromIso);
  const end = new Date(toIso);
  while (start < end) {
    const chunkEnd = new Date(Math.min(end.getTime(), start.getTime() + 31 * 86_400_000 - 1000));
    let page = 1;
    let totalPages = 1;
    do {
      const q = new URLSearchParams({
        start_date: start.toISOString().replace(/\.\d{3}Z$/, "Z"),
        end_date: chunkEnd.toISOString().replace(/\.\d{3}Z$/, "Z"),
        fields: "transaction_info",
        page_size: "500",
        page: String(page),
      });
      const r = await get<SearchResponse>(`/v1/reporting/transactions?${q}`, t);
      for (const d of r.transaction_details) {
        const i = d.transaction_info;
        out.push({
          id: i.transaction_id,
          date: i.transaction_initiation_date,
          eventCode: i.transaction_event_code,
          status: i.transaction_status,
          grossCents: cents(i.transaction_amount),
          // PayPal geeft fees als negatief bedrag
          feeCents: Math.abs(cents(i.fee_amount)),
          currency: i.transaction_amount.currency_code,
        });
      }
      totalPages = r.total_pages;
      page++;
    } while (page <= totalPages);
    start = new Date(chunkEnd.getTime() + 1000);
  }
  return out;
}

type BalanceResponse = {
  balances: { currency: string; primary?: boolean; total_balance: Money; available_balance?: Money; withheld_balance?: Money }[];
};

/** Saldo per valuta; beschikbaar en vastgehouden (withheld). */
export async function fetchPaypalBalance() {
  const t = await token();
  const r = await get<BalanceResponse>("/v1/reporting/balances?currency_code=ALL", t);
  return r.balances.map((b) => ({
    currency: b.currency,
    totalCents: cents(b.total_balance),
    availableCents: cents(b.available_balance),
    withheldCents: cents(b.withheld_balance),
  }));
}

/** Samenvatting van transacties: verkopen, fees en opnames naar de bank (alleen voltooide, in EUR). */
export function summarizePaypal(txs: PaypalTransaction[]) {
  const done = txs.filter((t) => t.status === "S" && t.currency === "EUR");
  const isSale = (t: PaypalTransaction) => t.eventCode.startsWith("T00") && t.grossCents > 0;
  const isWithdrawal = (t: PaypalTransaction) => t.eventCode.startsWith("T04");
  const isRefund = (t: PaypalTransaction) => t.eventCode.startsWith("T11");
  return {
    salesCents: done.filter(isSale).reduce((s, t) => s + t.grossCents, 0),
    salesCount: done.filter(isSale).length,
    feesCents: done.reduce((s, t) => s + t.feeCents, 0),
    refundsCents: done.filter(isRefund).reduce((s, t) => s + t.grossCents, 0),
    withdrawalsCents: -done.filter(isWithdrawal).reduce((s, t) => s + t.grossCents, 0),
    otherCurrencyCount: txs.filter((t) => t.currency !== "EUR").length,
  };
}
