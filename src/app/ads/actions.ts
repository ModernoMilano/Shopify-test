"use server";

import { revalidatePath } from "next/cache";
import { db } from "@/lib/db";
import { parseEuroToCents } from "@/lib/money";
import { parseCsv } from "@/lib/csv";

const isDate = (s: string) => /^\d{4}-\d{2}-\d{2}$/.test(s);

async function upsert(date: string, channel: string, amountCents: number) {
  const d = new Date(date);
  await db.adSpend.upsert({
    where: { date_channel: { date: d, channel } },
    create: { date: d, channel, amountCents },
    update: { amountCents },
  });
}

export async function saveAdSpend(formData: FormData) {
  const date = String(formData.get("date") ?? "");
  const channel = String(formData.get("channel") ?? "meta").toLowerCase().trim();
  const amount = parseEuroToCents(String(formData.get("amount") ?? ""));
  if (!isDate(date) || amount === null || !channel) return;
  await upsert(date, channel, amount);
  revalidatePath("/ads");
  revalidatePath("/");
}

export async function deleteAdSpend(formData: FormData) {
  await db.adSpend.delete({ where: { id: String(formData.get("id")) } });
  revalidatePath("/ads");
  revalidatePath("/");
}

export type AdImportResult = { imported: number; errors: string[] };

/** CSV met kolommen datum (YYYY-MM-DD of DD-MM-YYYY), kanaal, bedrag. Bestaande dagen worden overschreven. */
export async function importAdSpend(_prev: AdImportResult | null, formData: FormData): Promise<AdImportResult> {
  const file = formData.get("file");
  const text = file instanceof File && file.size > 0 ? await file.text() : "";
  const [header, ...rows] = parseCsv(text.replace(/^﻿/, "").trim());
  const errors: string[] = [];
  if (!header) return { imported: 0, errors: ["Leeg bestand"] };
  const h = header.map((x) => x.trim().toLowerCase());
  const iDate = h.findIndex((x) => ["datum", "date", "day", "dag"].includes(x));
  const iChannel = h.findIndex((x) => ["kanaal", "channel", "platform"].includes(x));
  const iAmount = h.findIndex((x) => ["bedrag", "amount", "spend", "kosten", "amount spent (eur)"].includes(x));
  if (iDate < 0 || iAmount < 0) return { imported: 0, errors: ["Kolommen 'datum' en 'bedrag' zijn verplicht"] };
  const defaultChannel = String(formData.get("channel") ?? "meta");

  let imported = 0;
  for (const [idx, r] of rows.entries()) {
    let date = (r[iDate] ?? "").trim();
    const nl = date.match(/^(\d{1,2})[-/](\d{1,2})[-/](\d{4})$/);
    if (nl) date = `${nl[3]}-${nl[2].padStart(2, "0")}-${nl[1].padStart(2, "0")}`;
    const amount = parseEuroToCents((r[iAmount] ?? "").trim());
    const channel = iChannel >= 0 ? (r[iChannel] ?? "").trim().toLowerCase() || defaultChannel : defaultChannel;
    if (!isDate(date) || amount === null) {
      errors.push(`Regel ${idx + 2}: ongeldige datum of bedrag`);
      continue;
    }
    await upsert(date, channel, amount);
    imported++;
  }
  revalidatePath("/ads");
  revalidatePath("/");
  return { imported, errors };
}
