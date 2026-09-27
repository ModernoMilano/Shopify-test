import { getSetting, setSetting } from "@/lib/settings";

export type FinanceSettings = {
  /** btw apart zetten als reservering (standaard uit: btw fix) */
  reserveVat: boolean;
  /** werkafspraak break-even ROAS */
  breakEvenTarget: number;
  bankBufferCents: number;
  payoutRatio: number;
  payoutDelayDays: number;
  softwarePerWeekCents: number;
  salesPerDayCents: number;
  metaPerDayCents: number;
  paypalPerDayCents: number;
  privatePerWeekCents: number;
  supplierPaymentCents: number;
  supplierPaymentDay: number;
  forecastDays: number;
  /** maximale Meta-share van de omzet voor de waarschuwing */
  metaShareLimit: number;
  feesLimit: number;
  inventoryValueCents: number | null;
};

export const DEFAULT_FINANCE: FinanceSettings = {
  reserveVat: false,
  breakEvenTarget: 2.0,
  bankBufferCents: 200000,
  payoutRatio: 0.86,
  payoutDelayDays: 3,
  softwarePerWeekCents: 30000,
  salesPerDayCents: 290000,
  metaPerDayCents: 160000,
  paypalPerDayCents: 30000,
  privatePerWeekCents: 150000,
  supplierPaymentCents: 300000,
  supplierPaymentDay: 2,
  forecastDays: 7,
  metaShareLimit: 0.4,
  feesLimit: 0.03,
  inventoryValueCents: null,
};

export async function getFinanceSettings(): Promise<FinanceSettings> {
  const raw = await getSetting("finance");
  return raw ? { ...DEFAULT_FINANCE, ...(JSON.parse(raw) as Partial<FinanceSettings>) } : DEFAULT_FINANCE;
}

export async function saveFinanceSettings(s: FinanceSettings) {
  await setSetting("finance", JSON.stringify(s));
}
