import { db } from "@/lib/db";
import { dayKey } from "@/lib/period";
import { addDaysKey, chargebackRate, daysBelow, forecast, payoutDifference, type ForecastSettings } from "./calculations";
import { moneyNow, type PeriodFinance } from "./data";
import type { FinanceSettings } from "./settings";

export type Alert = { level: 1 | 2 | 3; title: string; body: string; href?: string };

const e = (cents: number) =>
  new Intl.NumberFormat("nl-NL", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(cents / 100);

type Money = Awaited<ReturnType<typeof moneyNow>>;

export function forecastSettings(s: FinanceSettings, money: Money, today = dayKey(new Date())): ForecastSettings {
  return {
    days: s.forecastDays,
    startDate: addDaysKey(today, 1),
    bankCents: money.position.bankCents,
    payoutScheduledCents: money.position.payoutScheduledCents,
    payoutScheduledDate: money.snapshot?.payoutScheduledDate?.toISOString().slice(0, 10),
    pendingCents: money.position.pendingCents,
    pendingWorkdays: 3,
    salesPerDayCents: s.salesPerDayCents,
    payoutRatio: s.payoutRatio,
    payoutDelayDays: s.payoutDelayDays,
    paypalPerDayCents: s.paypalPerDayCents,
    metaPerDayCents: s.metaPerDayCents,
    privatePerWeekCents: s.privatePerWeekCents,
    softwarePerWeekCents: s.softwarePerWeekCents,
    supplierPaymentCents: s.supplierPaymentCents,
    supplierPaymentDay: s.supplierPaymentDay,
    bufferCents: s.bankBufferCents,
  };
}

/** 90-dagen chargeback rate per dag over de afgelopen 60 dagen, oudste eerst. */
export async function chargebackHistory(today = new Date()) {
  const since = new Date(today.getTime() - 150 * 86_400_000);
  const [disputes, payments] = await Promise.all([
    db.dispute.findMany({ where: { openedAt: { gte: since } }, select: { openedAt: true } }),
    db.order.findMany({ where: { createdAt: { gte: since }, feesCents: { not: null }, test: false }, select: { createdAt: true } }),
  ]);
  const rates: (number | null)[] = [];
  for (let i = 59; i >= 0; i--) {
    const end = today.getTime() - i * 86_400_000;
    const start = end - 90 * 86_400_000;
    const d = disputes.filter((x) => x.openedAt.getTime() > start && x.openedAt.getTime() <= end).length;
    const t = payments.filter((x) => x.createdAt.getTime() > start && x.createdAt.getTime() <= end).length;
    rates.push(t < 50 ? null : chargebackRate(d, t)); // te weinig data = onbekend
  }
  const current = rates[rates.length - 1];
  return { rates, current, daysBelow1: daysBelow(rates, 0.01), hasData: current !== null };
}

export async function computeAlerts(f: PeriodFinance, money: Money): Promise<Alert[]> {
  const s = f.settings;
  const alerts: Alert[] = [];

  // 1. prognose onder buffer
  const fc = forecast({ ...forecastSettings(s, money), days: 7 });
  if (fc.belowZero || fc.belowBuffer) {
    alerts.push({
      level: 1,
      title: fc.belowZero ? "Bank dreigt onder nul te komen" : "Bank komt onder je buffer",
      body: `Laagste punt de komende 7 dagen: ${e(fc.lowest.balanceCents)} op ${fc.lowest.date}. Buffer: ${e(s.bankBufferCents)}.`,
      href: "/prognose",
    });
  }

  // 2. fulfillment eerst
  const openInvoices = await db.supplierInvoice.aggregate({ where: { paid: false }, _sum: { amountCents: true } });
  const open = openInvoices._sum.amountCents ?? 0;
  const cover = money.position.bankCents + money.position.payoutScheduledCents;
  if (open > 0 && open > cover) {
    alerts.push({
      level: 1,
      title: "Fulfillment eerst: Meta niet verhogen",
      body: `Openstaande leveranciersfacturen (${e(open)}) zijn hoger dan bank plus ingeplande payout (${e(cover)}).`,
      href: "/invoer",
    });
  }

  // 3. Meta te duur
  const today = dayKey(new Date());
  const from3 = addDaysKey(today, -3);
  const [sales3, meta3] = await Promise.all([
    db.dailySales.aggregate({ where: { date: { gte: new Date(from3), lt: new Date(today) } }, _sum: { totalCents: true } }),
    db.metaDaily.aggregate({ where: { date: { gte: new Date(from3), lt: new Date(today) } }, _sum: { spendCents: true } }),
  ]);
  const mer3 = meta3._sum.spendCents ? (sales3._sum.totalCents ?? 0) / meta3._sum.spendCents : null;
  if (mer3 !== null && mer3 < s.breakEvenTarget) {
    alerts.push({
      level: 2,
      title: "Meta te duur",
      body: `MER van de laatste 3 dagen is ${mer3.toFixed(2).replace(".", ",")}, onder je break-even van ${s.breakEvenTarget.toFixed(2).replace(".", ",")}.`,
      href: "/meta",
    });
  }
  if (f.pnl.metaShare !== null && f.pnl.metaShare > s.metaShareLimit) {
    alerts.push({
      level: 2,
      title: "Meta is meer dan 40% van de omzet",
      body: `In deze periode ging ${(f.pnl.metaShare * 100).toFixed(1).replace(".", ",")}% van de omzet naar Meta.`,
      href: "/meta",
    });
  }

  // 4. chargebacks
  const cb = await chargebackHistory();
  if (cb.current !== null && cb.current >= 0.01) {
    alerts.push({
      level: 2,
      title: "Chargeback rate boven 1%",
      body: `90 dagen: ${(cb.current * 100).toFixed(2).replace(".", ",")}%. De reserve blijft staan tot je 30 dagen onder 1% zit.`,
      href: "/payouts",
    });
  }
  const urgent = await db.dispute.count({
    where: { status: { in: ["needs_response", "NEEDS_RESPONSE", "open"] }, dueBy: { lte: new Date(Date.now() + 3 * 86_400_000) } },
  });
  if (urgent > 0) {
    alerts.push({ level: 1, title: `${urgent} dispute(s) binnen 3 dagen reageren`, body: "Reageer voor de deadline, anders is het bedrag verloren.", href: "/payouts" });
  }

  // 5. fees hoog
  const charges = f.payouts.reduce((sum, p) => sum + (p.chargesCents ?? 0), 0);
  const payoutFees = f.payouts.reduce((sum, p) => sum + (p.feesCents ?? 0), 0);
  if (charges > 0 && payoutFees / charges > s.feesLimit) {
    alerts.push({
      level: 3,
      title: "Fees hoog",
      body: `Shopify Payments-fees zijn ${((payoutFees / charges) * 100).toFixed(1).replace(".", ",")}% van de charges. Normaal EU-tarief is 1,5 tot 2,5%. Grootste oorzaak: 2% wisselkoers-fee op betalingen in GBP, USD en andere valuta.`,
      href: "/payouts",
    });
  }

  // 6. ongeverifieerde data
  const syncs = await db.sourceSync.findMany();
  // de bank komt via upload binnen; die staat in de datastrook, niet als verouderde sync
  const stale = syncs.filter((x) => x.source !== "revolut" && (Date.now() - x.lastAt.getTime() > 26 * 3_600_000 || x.status !== "ok"));
  const deviating = f.payouts.filter((p) => p.feesCents !== null && payoutDifference({
    chargesCents: p.chargesCents ?? 0,
    refundsCents: p.refundsCents ?? 0,
    adjustmentsCents: p.adjustmentsCents ?? 0,
    reservedFundsCents: p.reservedFundsCents ?? 0,
    feesCents: p.feesCents ?? 0,
    retriedCents: p.retriedCents ?? 0,
    totalCents: p.totalCents,
  }) !== 0);
  const issues = [
    f.unknownCount > 0 && `${f.unknownCount} onbekende bankmutaties`,
    stale.length > 0 && `${stale.map((x) => x.source).join(", ")} langer dan 24 uur niet gesynct`,
    deviating.length > 0 && `${deviating.length} payout(s) met een afwijking`,
    f.missingSalesDays > 0 && `${f.missingSalesDays} dagen zonder omzetdata`,
  ].filter(Boolean);
  if (issues.length) {
    alerts.push({ level: 3, title: "Data nog niet volledig gecontroleerd", body: issues.join(", ") + ".", href: f.unknownCount ? "/bank?cat=unknown" : "/settings" });
  }

  // 7. teamkosten ontbreken
  if (f.pnl.teamCents === 0) {
    alerts.push({
      level: 3,
      title: "Winst niet volledig: teamkosten staan op € 0",
      body: "Je hebt een team, maar er zijn geen teamkosten ingevoerd. Bij € 3.000 per maand zakt de marge met ongeveer 3 procentpunt.",
      href: "/invoer",
    });
  }

  return alerts.sort((a, b) => a.level - b.level);
}
