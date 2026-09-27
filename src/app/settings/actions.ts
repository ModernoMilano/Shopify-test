"use server";

import { revalidatePath } from "next/cache";
import { saveProfitSettings } from "@/lib/settings";
import { syncAll } from "@/lib/sync";

export async function saveSettings(formData: FormData) {
  const pct = Number(String(formData.get("paymentFeePercent") ?? "").replace(",", "."));
  const fixed = Number(String(formData.get("paymentFeeFixed") ?? "").replace(",", "."));
  const vat = Number(String(formData.get("vatRate") ?? "").replace(",", "."));
  await saveProfitSettings({
    paymentFeePercent: Number.isFinite(pct) ? pct / 100 : 0.019,
    paymentFeeFixedCents: Number.isFinite(fixed) ? Math.round(fixed * 100) : 25,
    vatRate: Number.isFinite(vat) ? vat / 100 : 0.21,
    cogsOnRefundedItems: formData.get("cogsOnRefundedItems") === "on",
  });
  revalidatePath("/", "layout");
}

export type SyncResult = { ok: boolean; message: string };

export async function runSync(_prev: SyncResult | null, formData: FormData): Promise<SyncResult> {
  try {
    const r = await syncAll({ full: formData.get("full") === "1" });
    revalidatePath("/", "layout");
    return { ok: true, message: `${r.products} producten en ${r.orders} orders bijgewerkt.` };
  } catch (e) {
    return { ok: false, message: e instanceof Error ? e.message : String(e) };
  }
}
