/**
 * Haalt de cijfers voor een periode uit de database en voert ze door de rekenregels.
 * Elk bedrag krijgt een bron mee, zodat het dashboard kan tonen waar het vandaan komt.
 */
import { db } from "@/lib/db";
import type { Period } from "@/lib/period";
import { CATEGORY_BY_ID, splitAmounts } from "@/bank/categories";
import { cashBridge, moneyLocation, pnl, type Pnl } from "./calculations";
import { getFinanceSettings } from "./settings";

export type Source = "Shopify" | "bank" | "payouts" | "handmatig" | "Meta" | "ontbreekt";

export type PnlLine = { key: string; label: string; cents: number; sources: Source[]; note?: string };

const DAY = 86_400_000;
const dateOnly = (key: string) => new Date(`${key}T00:00:00Z`);
const keyOf = (d: Date) => d.toISOString().slice(0, 10);

function daysInclusive(from: Date, to: Date) {
  return Math.round((to.getTime() - from.getTime()) / DAY) + 1;
}

/** Deel van een bedrag over [start, end] dat in [from, to] valt (inclusief, per dag). */
function prorate(amount: number, start: Date, end: Date, from: Date, to: Date) {
  const s = Math.max(start.getTime(), from.getTime());
  const e = Math.min(end.getTime(), to.getTime());
  if (e < s) return 0;
  return (amount * daysInclusive(new Date(s), new Date(e))) / daysInclusive(start, end);
}

export async function bankTransactionsIn(fromKey: string, toKey: string) {
  const from = dateOnly(fromKey);
  const to = dateOnly(toKey);
  // effectieve datum = "hoort bij periode" of anders boekdatum
  return db.bankTransaction.findMany({
    where: {
      OR: [
        { periodDate: { gte: from, lte: to } },
        { periodDate: null, bookedAt: { gte: from, lte: to } },
      ],
    },
    orderBy: [{ bookedAt: "asc" }, { seq: "asc" }],
  });
}

export type PeriodFinance = Awaited<ReturnType<typeof periodFinance>>;

export async function periodFinance(period: Pick<Period, "fromKey" | "toKey">) {
  const from = dateOnly(period.fromKey);
  const to = dateOnly(period.toKey);
  const [settings, sales, txs, payouts, manual, expenses, bankCount] = await Promise.all([
    getFinanceSettings(),
    db.dailySales.findMany({ where: { date: { gte: from, lte: to } }, orderBy: { date: "asc" } }),
    bankTransactionsIn(period.fromKey, period.toKey),
    db.shopifyPayout.findMany({ where: { payoutDate: { gte: from, lte: to } } }),
    db.manualEntry.findMany({ where: { periodStart: { lte: to }, periodEnd: { gte: from } } }),
    db.expense.findMany({ where: { category: "team" } }),
    db.bankTransaction.count(),
  ]);

  // --- omzet
  const days = daysInclusive(from, to);
  const revenueCents = sales.reduce((s, d) => s + d.totalCents, 0);
  const taxesCents = sales.reduce((s, d) => s + d.taxesCents, 0);
  const orders = sales.reduce((s, d) => s + d.orders, 0);
  const missingSalesDays = days - sales.length;

  // --- bank per post
  const bank: Record<string, number> = {};
  for (const tx of txs) {
    for (const part of splitAmounts(tx)) bank[part.category] = (bank[part.category] ?? 0) + part.cents;
  }
  const bankBucket = (bucket: string) =>
    Object.entries(bank)
      .filter(([cat]) => CATEGORY_BY_ID.get(cat)?.bucket === bucket)
      .reduce((s, [, v]) => s - v, 0);

  // --- handmatig
  const manualSum = (...kinds: string[]) =>
    Math.round(
      manual
        .filter((m) => kinds.includes(m.kind))
        .reduce((s, m) => s + prorate(m.amountCents, m.periodStart, m.periodEnd, from, to), 0),
    );
  const teamFromExpenses = Math.round(
    expenses.reduce((s, e) => {
      const end = e.endDate ?? to;
      // maandbedrag × 12 / 365 per dag
      return s + prorate((e.amountCents * 12 * daysInclusive(e.startDate, end)) / 365, e.startDate, end, from, to);
    }, 0),
  );

  // --- payouts
  const payoutFees = payouts.reduce((s, p) => s + (p.feesCents ?? 0), 0);
  const payoutAdjustments = payouts.reduce((s, p) => s + (p.adjustmentsCents ?? 0), 0);
  const hasPayoutDetail = payouts.some((p) => p.feesCents !== null);

  const cogs = bankBucket("cogs") + manualSum("cogs");
  const meta = bankBucket("meta") + manualSum("meta");
  const fees = payoutFees + manualSum("fees", "paypal_fees");
  const chargebacks = -payoutAdjustments + bankBucket("chargebacks") + manualSum("chargebacks");
  const other = bankBucket("other") + manualSum("other");
  const team = bankBucket("team") + manualSum("team") + teamFromExpenses;

  const result: Pnl = pnl(
    {
      revenueCents,
      taxesCents,
      orders,
      cogsCents: cogs,
      metaCents: meta,
      feesCents: fees,
      chargebacksCents: chargebacks,
      otherCents: other,
      teamCents: team,
      inventoryIncreaseCents: manualSum("inventory"),
    },
    { reserveVat: settings.reserveVat },
  );

  const src = (...s: (Source | false)[]) => s.filter(Boolean) as Source[];
  const lines: PnlLine[] = [
    {
      key: "revenue",
      label: "Omzet",
      cents: revenueCents,
      sources: sales.length ? ["Shopify"] : ["ontbreekt"],
      note: missingSalesDays > 0 ? `${missingSalesDays} dagen zonder omzetdata` : undefined,
    },
    { key: "cogs", label: "COGS en verzending", cents: cogs, sources: src(bankCount > 0 && "bank", manualSum("cogs") !== 0 && "handmatig") },
    { key: "meta", label: "Meta ads", cents: meta, sources: src(bankCount > 0 && "bank", manualSum("meta") !== 0 && "handmatig"), note: "betaald volgens bank, per 'hoort bij periode'" },
    {
      key: "fees",
      label: "Shopify en PayPal fees",
      cents: fees,
      sources: src(hasPayoutDetail && "payouts", manualSum("fees", "paypal_fees") !== 0 && "handmatig", !hasPayoutDetail && fees === 0 && "ontbreekt"),
    },
    {
      key: "chargebacks",
      label: "Chargebacks en disputes",
      cents: chargebacks,
      sources: src(hasPayoutDetail && "payouts", manualSum("chargebacks") !== 0 && "handmatig", !hasPayoutDetail && chargebacks === 0 && "ontbreekt"),
    },
    { key: "other", label: "Software, freelancers, boekhouder, bank", cents: other, sources: src(bankCount > 0 && "bank", manualSum("other") !== 0 && "handmatig") },
    {
      key: "team",
      label: "Teamkosten",
      cents: team,
      sources: team === 0 ? ["ontbreekt"] : ["handmatig"],
      note: team === 0 ? "nog niet ingevoerd" : undefined,
    },
  ];

  const unknownTx = txs.filter((t) => t.category === "unknown");

  return {
    period,
    settings,
    pnl: result,
    lines,
    bank,
    unknownCount: unknownTx.length,
    unknownCents: unknownTx.reduce((s, t) => s + t.amountCents, 0),
    missingSalesDays,
    daily: sales.map((d) => ({ date: keyOf(d.date), revenueCents: d.totalCents, orders: d.orders })),
    txs,
    payouts,
  };
}

/** Meta-afschrijvingen die in de periode geboekt zijn maar bij een eerdere periode horen. */
async function metaPreviousPeriod(fromKey: string, toKey: string) {
  const from = dateOnly(fromKey);
  const txs = await db.bankTransaction.findMany({
    where: { category: "meta", bookedAt: { gte: from, lte: dateOnly(toKey) }, periodDate: { lt: from } },
  });
  return -txs.reduce((s, t) => s + t.amountCents, 0);
}

/** Banksaldo aan het eind van een dag, uit de mutaties. */
export async function bankBalanceAt(key: string): Promise<number | null> {
  const last = await db.bankTransaction.findFirst({
    where: { bookedAt: { lte: dateOnly(key) }, balanceCents: { not: null } },
    orderBy: [{ bookedAt: "desc" }, { seq: "desc" }],
  });
  if (last) return last.balanceCents;
  // geen mutatie op of vóór deze dag: terugrekenen vanaf de eerste mutatie erna
  const next = await db.bankTransaction.findFirst({
    where: { bookedAt: { gt: dateOnly(key) }, balanceCents: { not: null } },
    orderBy: [{ bookedAt: "asc" }, { seq: "asc" }],
  });
  return next ? next.balanceCents! - next.amountCents : null;
}

export async function latestSnapshot(atOrBefore?: Date) {
  return db.moneySnapshot.findFirst({
    where: atOrBefore ? { takenAt: { lte: atOrBefore } } : undefined,
    orderBy: { takenAt: "desc" },
  });
}

export async function moneyNow() {
  const snap = await latestSnapshot();
  const lastTx = await db.bankTransaction.findFirst({
    where: { balanceCents: { not: null } },
    orderBy: [{ bookedAt: "desc" }, { seq: "desc" }],
  });
  const bankCents = lastTx?.balanceCents ?? snap?.bankCents ?? null;
  const position = {
    bankCents: bankCents ?? 0,
    payoutScheduledCents: snap?.payoutScheduledCents ?? 0,
    pendingCents: snap?.pendingCents ?? 0,
    holdCents: snap?.holdCents ?? 0,
    paypalCents: snap?.paypalCents ?? 0,
  };
  return {
    snapshot: snap,
    bankDate: lastTx?.bookedAt ?? null,
    bankSource: lastTx ? ("bank" as const) : snap?.bankCents != null ? ("handmatig" as const) : ("ontbreekt" as const),
    position,
    ...moneyLocation(position),
  };
}

export async function periodBridge(period: Pick<Period, "fromKey" | "toKey">, profitCents: number, bank: Record<string, number>) {
  const dayBefore = keyOf(new Date(dateOnly(period.fromKey).getTime() - DAY));
  const [bankBegin, bankNow, snapBegin, snapNow, metaPrev] = await Promise.all([
    bankBalanceAt(dayBefore),
    bankBalanceAt(period.toKey),
    latestSnapshot(new Date(dateOnly(period.fromKey).getTime() + DAY - 1)),
    latestSnapshot(new Date(dateOnly(period.toKey).getTime() + DAY - 1)),
    metaPreviousPeriod(period.fromKey, period.toKey),
  ]);
  const shopify = (s: typeof snapNow) => (s ? s.payoutScheduledCents + s.pendingCents + s.holdCents : null);
  const missing: string[] = [];
  if (bankBegin === null) missing.push("banksaldo aan het begin");
  if (bankNow === null) missing.push("banksaldo aan het eind");
  if (!snapBegin || snapBegin.takenAt > new Date(dateOnly(period.fromKey).getTime() + DAY)) missing.push("Shopify-saldo aan het begin");
  if (!snapNow) missing.push("Shopify-saldo nu");

  const bridge = cashBridge({
    profitCents,
    shopifyNowCents: shopify(snapNow) ?? 0,
    shopifyBeginCents: shopify(snapBegin) ?? 0,
    bankBeginCents: bankBegin ?? 0,
    bankNowCents: bankNow ?? 0,
    // bank[...] is negatief voor uitgaven
    privateCents: -(bank.private ?? 0),
    metaPreviousPeriodCents: metaPrev,
    loansAndDepositsCents: (bank.loan ?? 0) + (bank.owner_deposit ?? 0),
  });
  return { ...bridge, missing, bankBegin, bankNow, shopifyBegin: shopify(snapBegin), shopifyNow: shopify(snapNow) };
}
