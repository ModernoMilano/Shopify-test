"use server";

import { revalidatePath } from "next/cache";
import { db } from "@/lib/db";
import { importStatement, recategorizeAll, type ImportSummary } from "@/bank/import";

export type ImportState = { ok: boolean; results: ImportSummary[]; error?: string } | null;

export async function uploadStatement(_prev: ImportState, formData: FormData): Promise<ImportState> {
  const files = formData.getAll("file").filter((f): f is File => f instanceof File && f.size > 0);
  if (!files.length) return { ok: false, results: [], error: "Kies een PDF- of CSV-bestand" };
  try {
    const results: ImportSummary[] = [];
    for (const f of files) results.push(await importStatement(f.name, new Uint8Array(await f.arrayBuffer())));
    revalidatePath("/", "layout");
    return { ok: true, results };
  } catch (e) {
    return { ok: false, results: [], error: e instanceof Error ? e.message : String(e) };
  }
}

export async function updateTransaction(formData: FormData) {
  const id = String(formData.get("id"));
  const category = String(formData.get("category"));
  const periodDate = String(formData.get("periodDate") ?? "");
  const tx = await db.bankTransaction.findUniqueOrThrow({ where: { id } });
  await db.bankTransaction.update({
    where: { id },
    data: {
      category,
      categorySource: category !== tx.category ? "handmatig" : tx.categorySource,
      periodDate: periodDate && periodDate !== tx.bookedAt.toISOString().slice(0, 10) ? new Date(`${periodDate}T00:00:00Z`) : null,
    },
  });

  // optioneel: regel maken zodat vergelijkbare mutaties voortaan automatisch goed gaan
  const pattern = String(formData.get("rulePattern") ?? "").trim();
  if (formData.get("makeRule") === "on" && pattern) {
    await db.categoryRule.create({
      data: { pattern, category, direction: tx.amountCents >= 0 ? "in" : "out", priority: 15 },
    });
    await recategorizeAll();
  }
  revalidatePath("/", "layout");
}

export async function addRule(formData: FormData) {
  const pattern = String(formData.get("pattern") ?? "").trim();
  if (!pattern) return;
  await db.categoryRule.create({
    data: {
      pattern,
      category: String(formData.get("category")),
      direction: String(formData.get("direction") ?? "any"),
      priority: Number(formData.get("priority") ?? 50) || 50,
    },
  });
  await recategorizeAll();
  revalidatePath("/", "layout");
}

export async function deleteRule(formData: FormData) {
  await db.categoryRule.delete({ where: { id: String(formData.get("id")) } });
  await recategorizeAll();
  revalidatePath("/", "layout");
}

export async function reapplyRules() {
  await recategorizeAll();
  revalidatePath("/", "layout");
}
