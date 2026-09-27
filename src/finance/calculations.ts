/**
 * Financiële rekenregels van ModernoMilano. Puur (geen database), alle bedragen in centen.
 * Definities volgen de spec: omzet is inclusief btw (btw fix), winst is cash-basis.
 */

// ---------------------------------------------------------------------------
// Winst en verlies

export type PnlInput = {
  /** Shopify total_sales: incl. btw, incl. verzendkosten klant, na kortingen en retouren */
  revenueCents: number;
  /** btw in de omzet, alleen gebruikt als btw gereserveerd wordt */
  taxesCents: number;
  orders: number;
  cogsCents: number;
  metaCents: number;
  feesCents: number;
  chargebacksCents: number;
  /** software, freelancers, boekhouder, bankkosten, overig zakelijk */
  otherCents: number;
  teamCents: number;
  /** optioneel: toename voorraadwaarde in de periode (bezit, geen kosten) */
  inventoryIncreaseCents?: number;
};

export type PnlOptions = { reserveVat: boolean };

export type Pnl = PnlInput & {
  costsCents: number;
  profitCents: number;
  /** winst als de btw toch afgedragen moet worden */
  profitAfterVatCents: number;
  /** winst na voorraadcorrectie (voorraadtoename is bezit, geen kosten) */
  profitAfterInventoryCents: number;
  margin: number | null;
  mer: number | null;
  breakEvenRoas: number | null;
  metaShare: number | null;
  cogsShare: number | null;
  aovCents: number | null;
  profitPerOrderCents: number | null;
  cogsPerOrderCents: number | null;
};

export const div = (a: number, b: number): number | null => (b === 0 ? null : a / b);

export function pnl(input: PnlInput, opts: PnlOptions = { reserveVat: false }): Pnl {
  const costsCents =
    input.cogsCents + input.metaCents + input.feesCents + input.chargebacksCents + input.otherCents + input.teamCents;
  const grossProfit = input.revenueCents - costsCents;
  const profitCents = opts.reserveVat ? grossProfit - input.taxesCents : grossProfit;
  const nonMetaCosts = costsCents - input.metaCents;
  return {
    ...input,
    costsCents,
    profitCents,
    profitAfterVatCents: grossProfit - input.taxesCents,
    profitAfterInventoryCents: profitCents + (input.inventoryIncreaseCents ?? 0),
    margin: div(profitCents, input.revenueCents),
    mer: div(input.revenueCents, input.metaCents),
    breakEvenRoas: input.revenueCents - nonMetaCosts > 0 ? input.revenueCents / (input.revenueCents - nonMetaCosts) : null,
    metaShare: div(input.metaCents, input.revenueCents),
    cogsShare: div(input.cogsCents, input.revenueCents),
    aovCents: input.orders ? Math.round(input.revenueCents / input.orders) : null,
    profitPerOrderCents: input.orders ? Math.round(profitCents / input.orders) : null,
    cogsPerOrderCents: input.orders ? Math.round(input.cogsCents / input.orders) : null,
  };
}

// ---------------------------------------------------------------------------
// Waar het geld staat

export type MoneyPosition = {
  bankCents: number;
  payoutScheduledCents: number;
  pendingCents: number;
  holdCents: number;
  paypalCents: number;
};

export function moneyLocation(m: MoneyPosition) {
  const availableNow = m.bankCents + m.paypalCents;
  const soon = m.payoutScheduledCents + m.pendingCents;
  const locked = m.holdCents;
  return {
    availableNow,
    soon,
    locked,
    totalCents: availableNow + soon + locked,
    /** alles wat bij Shopify staat: payout + pending + hold */
    shopifyCents: m.payoutScheduledCents + m.pendingCents + m.holdCents,
  };
}

// ---------------------------------------------------------------------------
// Cash bridge: van winst naar bankrekening

export type BridgeInput = {
  profitCents: number;
  shopifyNowCents: number;
  shopifyBeginCents: number;
  bankBeginCents: number;
  bankNowCents: number;
  privateCents: number;
  metaPreviousPeriodCents: number;
  loansAndDepositsCents: number;
};

export type BridgeStep = { key: string; label: string; cents: number; explanation: string };

export function cashBridge(b: BridgeInput) {
  const shopifyGrowth = b.shopifyNowCents - b.shopifyBeginCents;
  const bankGrowth = b.bankNowCents - b.bankBeginCents;
  const explained = b.profitCents - shopifyGrowth - b.privateCents - b.metaPreviousPeriodCents + b.loansAndDepositsCents;
  const timing = bankGrowth - explained;
  const steps: BridgeStep[] = [
    { key: "profit", label: "Winst", cents: b.profitCents, explanation: "Wat je in deze periode verdiende." },
    {
      key: "shopify",
      label: "Nog bij Shopify",
      cents: -shopifyGrowth,
      explanation: "Geld dat Shopify nog vasthoudt (payout, pending en reserve) is gegroeid en staat dus nog niet op je bank.",
    },
    { key: "private", label: "Naar privé", cents: -b.privateCents, explanation: "Opnames naar privé. Geen kosten, wel weg van de zakelijke rekening." },
    {
      key: "metaPrev",
      label: "Meta vorige periode",
      cents: -b.metaPreviousPeriodCents,
      explanation: "Meta boekte in deze periode nog kosten van de vorige periode af.",
    },
    {
      key: "loans",
      label: "Lening en stortingen",
      cents: b.loansAndDepositsCents,
      explanation: "Geleend geld en eigen stortingen. Geen omzet, wel geld op de bank.",
    },
    {
      key: "timing",
      label: "Timing en afronding",
      cents: timing,
      explanation: "Het deel dat niet door de stappen hierboven verklaard wordt, bijvoorbeeld leveranciers betaald voor een andere periode.",
    },
  ];
  return {
    shopifyGrowth,
    bankGrowth,
    explained,
    timing,
    steps,
    /** waarschuwing als het onverklaarde deel groter is dan 5% van de winst */
    timingWarning: b.profitCents !== 0 && Math.abs(timing) > Math.abs(b.profitCents) * 0.05,
  };
}

// ---------------------------------------------------------------------------
// Shopify payouts

export type PayoutColumns = {
  chargesCents: number;
  refundsCents: number;
  adjustmentsCents: number;
  reservedFundsCents: number;
  /** positief bedrag, wordt afgetrokken */
  feesCents: number;
  retriedCents: number;
  totalCents: number;
};

/** Verschil tussen het uitbetaalde totaal en de som van de kolommen. 0 = klopt. */
export function payoutDifference(p: PayoutColumns): number {
  const expected = p.chargesCents + p.refundsCents + p.adjustmentsCents + p.reservedFundsCents - p.feesCents + p.retriedCents;
  return p.totalCents - expected;
}

// ---------------------------------------------------------------------------
// Chargebacks

/** Chargeback rate = disputes / Shopify Payments-transacties, over een rollend venster. */
export function chargebackRate(disputes: number, transactions: number): number | null {
  return div(disputes, transactions);
}

/**
 * Aantal opeenvolgende dagen (eindigend op de laatste dag) dat de 90-dagen rate onder de grens lag.
 * dailyRates: oudste eerst, null = geen data.
 */
export function daysBelow(dailyRates: (number | null)[], limit = 0.01): number {
  let n = 0;
  for (let i = dailyRates.length - 1; i >= 0; i--) {
    const r = dailyRates[i];
    if (r === null || r >= limit) break;
    n++;
  }
  return n;
}

// ---------------------------------------------------------------------------
// Cashflow prognose

export type ForecastSettings = {
  days: number;
  /** eerste prognosedag, "YYYY-MM-DD" (meestal morgen) */
  startDate: string;
  bankCents: number;
  payoutScheduledCents: number;
  /** datum van de ingeplande payout; standaard de eerste werkdag */
  payoutScheduledDate?: string;
  pendingCents: number;
  /** aantal werkdagen waarover pending wordt uitbetaald */
  pendingWorkdays: number;
  salesPerDayCents: number;
  /** deel van nieuwe verkopen dat wordt uitbetaald (reserve en fees eraf) */
  payoutRatio: number;
  payoutDelayDays: number;
  paypalPerDayCents: number;
  metaPerDayCents: number;
  privatePerWeekCents: number;
  softwarePerWeekCents: number;
  supplierPaymentCents: number;
  /** dagnummer (1 = eerste prognosedag) van de leveranciersbetaling, 0 = geen */
  supplierPaymentDay: number;
  reserveReleaseCents?: number;
  reserveReleaseDate?: string;
  /** extra vaste uitgaven per dag (bv. teamkosten) */
  extraPerDayCents?: number;
  bufferCents: number;
};

export type ForecastDay = {
  day: number;
  date: string;
  workday: boolean;
  shopifyInCents: number;
  paypalInCents: number;
  metaCents: number;
  supplierCents: number;
  privateAndSoftwareCents: number;
  otherCents: number;
  balanceCents: number;
};

export type Forecast = {
  rows: ForecastDay[];
  endBalanceCents: number;
  /** saldo na 7 dagen (of na de laatste dag als de prognose korter is) */
  balanceAfter7Cents: number;
  lowest: { date: string; balanceCents: number };
  changeCents: number;
  belowBuffer: boolean;
  belowZero: boolean;
};

export function addDaysKey(key: string, n: number): string {
  const [y, m, d] = key.split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, d + n)).toISOString().slice(0, 10);
}

export function isWorkday(key: string): boolean {
  const [y, m, d] = key.split("-").map(Number);
  const dow = new Date(Date.UTC(y, m - 1, d)).getUTCDay();
  return dow >= 1 && dow <= 5;
}

/**
 * Dag voor dag prognose van het banksaldo.
 * Shopify betaalt alleen op werkdagen uit: eerst de ingeplande payout, dan pending verdeeld over
 * een aantal werkdagen, en nieuwe verkopen komen na de vertraging binnen als payoutRatio × verkoop.
 * Verkopen waarvan de uitbetaaldatum in het weekend valt, komen op de eerstvolgende werkdag.
 */
export function forecast(s: ForecastSettings): Forecast {
  const rows: ForecastDay[] = [];
  let balance = s.bankCents;
  let payableSales = 0; // opgebouwde nieuwe verkopen die uitbetaald mogen worden
  const scheduledDate = s.payoutScheduledDate;
  let scheduledPaid = false;
  const pendingPart = s.pendingWorkdays > 0 ? s.pendingCents / s.pendingWorkdays : 0;
  let pendingPaidDays = 0;

  for (let i = 1; i <= s.days; i++) {
    const date = addDaysKey(s.startDate, i - 1);
    const workday = isWorkday(date);

    // verkopen van (i - delay) worden vandaag uitbetaalbaar
    const saleDay = i - s.payoutDelayDays;
    if (saleDay >= 1) payableSales += s.salesPerDayCents * s.payoutRatio;

    let shopifyIn = 0;
    if (workday) {
      if (!scheduledPaid && (scheduledDate ? date >= scheduledDate : true)) {
        shopifyIn += s.payoutScheduledCents;
        scheduledPaid = true;
      } else if (scheduledPaid && pendingPaidDays < s.pendingWorkdays) {
        shopifyIn += pendingPart;
        pendingPaidDays++;
      }
      shopifyIn += payableSales;
      payableSales = 0;
    }

    // vrijgave van de reserve komt via Shopify binnen
    if (s.reserveReleaseCents && s.reserveReleaseDate === date) shopifyIn += s.reserveReleaseCents;

    const other = s.extraPerDayCents ?? 0;
    const paypalIn = s.paypalPerDayCents;
    const meta = s.metaPerDayCents;
    const supplier = s.supplierPaymentDay === i ? s.supplierPaymentCents : 0;
    const privSoft = (s.privatePerWeekCents + s.softwarePerWeekCents) / 7;

    balance += shopifyIn + paypalIn - meta - supplier - privSoft - other;
    const row: ForecastDay = {
      day: i,
      date,
      workday,
      shopifyInCents: Math.round(shopifyIn),
      paypalInCents: Math.round(paypalIn),
      metaCents: Math.round(meta),
      supplierCents: Math.round(supplier),
      privateAndSoftwareCents: Math.round(privSoft),
      otherCents: Math.round(other),
      balanceCents: Math.round(balance),
    };
    rows.push(row);
  }

  // laagste punt over de prognosedagen
  const lowest = rows.length
    ? rows.reduce((lo, r) => (r.balanceCents < lo.balanceCents ? { date: r.date, balanceCents: r.balanceCents } : lo), {
      date: rows[0].date,
        balanceCents: rows[0].balanceCents,
      })
    : { date: s.startDate, balanceCents: s.bankCents };
  const endBalanceCents = rows.length ? rows[rows.length - 1].balanceCents : s.bankCents;
  const after7 = rows[Math.min(6, rows.length - 1)]?.balanceCents ?? s.bankCents;
  return {
    rows,
    endBalanceCents,
    balanceAfter7Cents: after7,
    lowest,
    changeCents: endBalanceCents - s.bankCents,
    belowBuffer: lowest.balanceCents < s.bufferCents,
    belowZero: lowest.balanceCents < 0,
  };
}
