import { createHash } from "node:crypto";
import { db } from "@/lib/db";
import { DEFAULT_RULES, matchRule } from "./categories";
import { parseRevolutCsv, parseRevolutPdf, reconcile, type ParsedStatement } from "./revolut";

export async function ensureDefaultRules() {
  if ((await db.categoryRule.count()) === 0) {
    await db.categoryRule.createMany({ data: DEFAULT_RULES });
  }
  return db.categoryRule.findMany();
}

function fingerprint(t: ParsedStatement["transactions"][number], occurrence: number) {
  return createHash("sha256")
    .update([t.date, t.amountCents, t.balanceCents ?? "", t.description, occurrence].join("|"))
    .digest("hex")
    .slice(0, 32);
}

export type ImportSummary = {
  fileName: string;
  transactions: number;
  imported: number;
  duplicates: number;
  unknown: number;
  reconciled: boolean;
  opening: number | null;
  closing: number | null;
  periodFrom: string | null;
  periodTo: string | null;
  message?: string;
};

export async function importStatement(fileName: string, bytes: Uint8Array): Promise<ImportSummary> {
  const isPdf = fileName.toLowerCase().endsWith(".pdf") || (bytes[0] === 0x25 && bytes[1] === 0x50);
  const statement = isPdf ? await parseRevolutPdf(bytes) : parseRevolutCsv(new TextDecoder().decode(bytes));
  const rec = reconcile(statement);
  const rules = await ensureDefaultRules();

  // volgnummer binnen het afschrift + teller voor identieke regels (zelfde dag, bedrag en saldo)
  const seen = new Map<string, number>();
  const rows = statement.transactions.map((t, seq) => {
    const base = [t.date, t.amountCents, t.balanceCents ?? "", t.description].join("|");
    const occurrence = seen.get(base) ?? 0;
    seen.set(base, occurrence + 1);
    const rule = matchRule(t, rules);
    return {
      account: "revolut",
      bookedAt: new Date(`${t.date}T00:00:00Z`),
      description: t.description,
      details: t.details,
      amountCents: t.amountCents,
      feeCents: t.feeCents,
      balanceCents: t.balanceCents,
      category: rule?.category ?? "unknown",
      ruleId: rule?.id ?? null,
      fingerprint: fingerprint(t, occurrence),
      seq,
    };
  });

  const existing = new Set(
    (await db.bankTransaction.findMany({ where: { fingerprint: { in: rows.map((r) => r.fingerprint) } }, select: { fingerprint: true } })).map(
      (r) => r.fingerprint,
    ),
  );
  const fresh = rows.filter((r) => !existing.has(r.fingerprint));
  const message = rec.ok
    ? undefined
    : rec.breaks.length
      ? `Saldo klopt niet vanaf mutatie ${rec.breaks[0].index + 1}`
      : "Beginsaldo + mutaties is niet gelijk aan het eindsaldo";

  const imp = await db.bankImport.create({
    data: {
      fileName,
      format: isPdf ? "pdf" : "csv",
      openingBalanceCents: rec.opening,
      closingBalanceCents: rec.closing,
      periodFrom: statement.periodFrom ? new Date(`${statement.periodFrom}T00:00:00Z`) : null,
      periodTo: statement.periodTo ? new Date(`${statement.periodTo}T00:00:00Z`) : null,
      transactions: rows.length,
      duplicates: rows.length - fresh.length,
      reconciled: rec.ok,
      message,
    },
  });
  if (fresh.length) await db.bankTransaction.createMany({ data: fresh.map((r) => ({ ...r, importId: imp.id })) });
  await db.sourceSync.upsert({
    where: { source: "revolut" },
    create: { source: "revolut", lastAt: new Date(), status: rec.ok ? "ok" : "fout", message },
    update: { lastAt: new Date(), status: rec.ok ? "ok" : "fout", message },
  });

  return {
    fileName,
    transactions: rows.length,
    imported: fresh.length,
    duplicates: rows.length - fresh.length,
    unknown: fresh.filter((r) => r.category === "unknown").length,
    reconciled: rec.ok,
    opening: rec.opening,
    closing: rec.closing,
    periodFrom: statement.periodFrom ?? null,
    periodTo: statement.periodTo ?? null,
    message,
  };
}

/** Pas de regels opnieuw toe op alle mutaties die niet handmatig zijn ingedeeld. */
export async function recategorizeAll() {
  const rules = await ensureDefaultRules();
  const txs = await db.bankTransaction.findMany({ where: { categorySource: "regel" } });
  let changed = 0;
  for (const t of txs) {
    const rule = matchRule(t, rules);
    const category = rule?.category ?? "unknown";
    if (category !== t.category || (rule?.id ?? null) !== t.ruleId) {
      await db.bankTransaction.update({ where: { id: t.id }, data: { category, ruleId: rule?.id ?? null } });
      changed++;
    }
  }
  return changed;
}
