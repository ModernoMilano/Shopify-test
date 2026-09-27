"use server";

import { revalidatePath } from "next/cache";
import { db } from "@/lib/db";
import { fetchWindsorMeta, marketOf } from "@/finance/meta";
import { parseEuroToCents } from "@/lib/money";
import { dayKey } from "@/lib/period";
import { addDaysKey } from "@/finance/calculations";

export async function syncWindsor(): Promise<{ ok: boolean; message: string }> {
  try {
    const to = dayKey(new Date());
    const rows = await fetchWindsorMeta(addDaysKey(to, -35), to);
    for (const r of rows) {
      const data = {
        market: marketOf(r.campaign),
        spendCents: r.spendCents,
        clicks: r.clicks,
        impressions: r.impressions,
        purchases: r.purchases,
        purchaseValueCents: r.purchaseValueCents,
        frequency: r.frequency,
        source: "windsor",
      };
      const date = new Date(`${r.date}T00:00:00Z`);
      await db.metaDaily.upsert({ where: { date_campaign: { date, campaign: r.campaign } }, create: { date, campaign: r.campaign, ...data }, update: data });
    }
    await db.sourceSync.upsert({
      where: { source: "windsor" },
      create: { source: "windsor", lastAt: new Date(), status: "ok", message: `${rows.length} rijen` },
      update: { lastAt: new Date(), status: "ok", message: `${rows.length} rijen` },
    });
    revalidatePath("/", "layout");
    return { ok: true, message: `${rows.length} campagnedagen opgehaald` };
  } catch (e) {
    const message = e instanceof Error ? e.message : String(e);
    await db.sourceSync.upsert({
      where: { source: "windsor" },
      create: { source: "windsor", lastAt: new Date(), status: "fout", message },
      update: { status: "fout", message },
    });
    return { ok: false, message };
  }
}

export async function addBudgetChange(formData: FormData) {
  const date = String(formData.get("date"));
  const oldCents = parseEuroToCents(String(formData.get("old") ?? ""));
  const newCents = parseEuroToCents(String(formData.get("new") ?? ""));
  const campaign = String(formData.get("campaign") ?? "").trim();
  if (!date || !campaign || oldCents === null || newCents === null) return;
  await db.budgetChange.create({
    data: { date: new Date(`${date}T00:00:00Z`), campaign, oldCents, newCents, note: String(formData.get("note") ?? "") || null },
  });
  revalidatePath("/meta");
}

export async function deleteBudgetChange(formData: FormData) {
  await db.budgetChange.delete({ where: { id: String(formData.get("id")) } });
  revalidatePath("/meta");
}
