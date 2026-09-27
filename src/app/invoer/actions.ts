"use server";

import { revalidatePath } from "next/cache";
import { db } from "@/lib/db";
import { parseEuroToCents } from "@/lib/money";

const str = (f: FormData, k: string) => String(f.get(k) ?? "").trim();
const date = (s: string) => (s ? new Date(`${s}T00:00:00Z`) : null);
const done = () => revalidatePath("/", "layout");

export async function addTeamCost(f: FormData) {
  const amount = parseEuroToCents(str(f, "amount"));
  if (!str(f, "name") || amount === null || !str(f, "start")) return;
  await db.expense.create({
    data: { name: str(f, "name"), category: "team", amountCents: amount, startDate: date(str(f, "start"))!, endDate: date(str(f, "end")) },
  });
  done();
}

export async function deleteTeamCost(f: FormData) {
  await db.expense.delete({ where: { id: str(f, "id") } });
  done();
}

export async function addManualEntry(f: FormData) {
  const amount = parseEuroToCents(str(f, "amount"));
  const start = date(str(f, "start"));
  const end = date(str(f, "end")) ?? start;
  if (amount === null || !start || !end || !str(f, "label")) return;
  await db.manualEntry.create({ data: { kind: str(f, "kind"), label: str(f, "label"), amountCents: amount, periodStart: start, periodEnd: end, note: str(f, "note") || null } });
  done();
}

export async function deleteManualEntry(f: FormData) {
  await db.manualEntry.delete({ where: { id: str(f, "id") } });
  done();
}

export async function addSnapshot(f: FormData) {
  const c = (k: string) => parseEuroToCents(str(f, k)) ?? 0;
  await db.moneySnapshot.create({
    data: {
      takenAt: new Date(),
      bankCents: str(f, "bank") ? c("bank") : null,
      payoutScheduledCents: c("payout"),
      payoutScheduledDate: date(str(f, "payoutDate")),
      pendingCents: c("pending"),
      holdCents: c("hold"),
      paypalCents: c("paypal"),
      note: str(f, "note") || null,
    },
  });
  done();
}

export async function addInvoice(f: FormData) {
  const amount = parseEuroToCents(str(f, "amount"));
  if (amount === null || !str(f, "supplier") || !str(f, "invoiceDate")) return;
  await db.supplierInvoice.create({
    data: {
      supplierName: str(f, "supplier"),
      amountCents: amount,
      invoiceDate: date(str(f, "invoiceDate"))!,
      dueDate: date(str(f, "dueDate")),
      salesFrom: date(str(f, "salesFrom")),
      salesTo: date(str(f, "salesTo")),
      note: str(f, "note") || null,
    },
  });
  done();
}

export async function toggleInvoicePaid(f: FormData) {
  const inv = await db.supplierInvoice.findUniqueOrThrow({ where: { id: str(f, "id") } });
  await db.supplierInvoice.update({ where: { id: inv.id }, data: { paid: !inv.paid } });
  done();
}

export async function deleteInvoice(f: FormData) {
  await db.supplierInvoice.delete({ where: { id: str(f, "id") } });
  done();
}

export async function saveLoan(f: FormData) {
  const principal = parseEuroToCents(str(f, "principal"));
  if (!str(f, "lender") || principal === null || !str(f, "start")) return;
  const data = {
    lender: str(f, "lender"),
    principalCents: principal,
    startDate: date(str(f, "start"))!,
    repaidCents: parseEuroToCents(str(f, "repaid")) ?? 0,
    schedule: str(f, "schedule") || null,
  };
  const id = str(f, "id");
  if (id) await db.loan.update({ where: { id }, data });
  else await db.loan.create({ data });
  done();
}
