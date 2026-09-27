"use server";

import { revalidatePath } from "next/cache";
import { saveProfitSettings, getProfitSettings } from "@/lib/settings";
import { syncAllSources, type SourceResult } from "@/finance/sync-all";
import { getFinanceSettings, saveFinanceSettings } from "@/finance/settings";
import { parseEuroToCents } from "@/lib/money";

const num = (f: FormData, k: string, fallback: number) => {
  const n = Number(String(f.get(k) ?? "").replace(",", "."));
  return Number.isFinite(n) && String(f.get(k) ?? "").trim() !== "" ? n : fallback;
};
const cents = (f: FormData, k: string, fallback: number) => parseEuroToCents(String(f.get(k) ?? "")) ?? fallback;

export async function saveSettings(formData: FormData) {
  const cur = await getFinanceSettings();
  await saveFinanceSettings({
    ...cur,
    reserveVat: formData.get("reserveVat") === "on",
    breakEvenTarget: num(formData, "breakEvenTarget", cur.breakEvenTarget),
    bankBufferCents: cents(formData, "bankBuffer", cur.bankBufferCents),
    payoutRatio: num(formData, "payoutRatio", cur.payoutRatio * 100) / 100,
    payoutDelayDays: num(formData, "payoutDelayDays", cur.payoutDelayDays),
    softwarePerWeekCents: cents(formData, "softwarePerWeek", cur.softwarePerWeekCents),
    salesPerDayCents: cents(formData, "salesPerDay", cur.salesPerDayCents),
    metaPerDayCents: cents(formData, "metaPerDay", cur.metaPerDayCents),
    paypalPerDayCents: cents(formData, "paypalPerDay", cur.paypalPerDayCents),
    privatePerWeekCents: cents(formData, "privatePerWeek", cur.privatePerWeekCents),
    supplierPaymentCents: cents(formData, "supplierPayment", cur.supplierPaymentCents),
    supplierPaymentDay: num(formData, "supplierPaymentDay", cur.supplierPaymentDay),
    forecastDays: num(formData, "forecastDays", cur.forecastDays),
  });
  const p = await getProfitSettings();
  await saveProfitSettings({
    ...p,
    paymentFeePercent: num(formData, "paymentFeePercent", p.paymentFeePercent * 100) / 100,
    paymentFeeFixedCents: cents(formData, "paymentFeeFixed", p.paymentFeeFixedCents),
    cogsOnRefundedItems: formData.get("cogsOnRefundedItems") === "on",
  });
  revalidatePath("/", "layout");
}

export async function runSync(): Promise<SourceResult[]> {
  const r = await syncAllSources();
  revalidatePath("/", "layout");
  return r;
}
