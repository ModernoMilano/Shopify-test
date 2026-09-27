"use server";

import { revalidatePath } from "next/cache";
import { db } from "@/lib/db";
import { parsePayoutsCsv } from "@/finance/payouts";

export type PayoutImportState = { ok: boolean; message: string } | null;

export async function importPayouts(_prev: PayoutImportState, formData: FormData): Promise<PayoutImportState> {
  const file = formData.get("file");
  if (!(file instanceof File) || file.size === 0) return { ok: false, message: "Kies het CSV-bestand met payouts" };
  try {
    const rows = parsePayoutsCsv(await file.text());
    if (!rows.length) return { ok: false, message: "Geen payouts gevonden in dit bestand" };
    const dates = rows.map((r) => r.payoutDate).sort();
    const from = new Date(`${dates[0]}T00:00:00Z`);
    const to = new Date(`${dates[dates.length - 1]}T00:00:00Z`);
    await db.$transaction([
      // samengevatte startwaarden en eerdere imports in dezelfde periode worden vervangen
      db.shopifyPayout.deleteMany({ where: { payoutDate: { gte: from, lte: to }, source: { in: ["seed", "csv"] } } }),
      db.shopifyPayout.createMany({
        data: rows.map((r) => ({ ...r, payoutDate: new Date(`${r.payoutDate}T00:00:00Z`), source: "csv" })),
      }),
      db.sourceSync.upsert({
        where: { source: "shopify_payments" },
        create: { source: "shopify_payments", lastAt: new Date(), status: "ok", message: "CSV-import" },
        update: { lastAt: new Date(), status: "ok", message: "CSV-import" },
      }),
    ]);
    revalidatePath("/", "layout");
    return { ok: true, message: `${rows.length} payouts geïmporteerd (${dates[0]} t/m ${dates[dates.length - 1]}).` };
  } catch (e) {
    return { ok: false, message: e instanceof Error ? e.message : String(e) };
  }
}
