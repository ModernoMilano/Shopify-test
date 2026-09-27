"use server";

import { revalidatePath } from "next/cache";
import { db } from "@/lib/db";
import { parseEuroToCents } from "@/lib/money";

export async function addExpense(formData: FormData) {
  const name = String(formData.get("name") ?? "").trim();
  const amountCents = parseEuroToCents(String(formData.get("amount") ?? ""));
  const start = String(formData.get("startDate") ?? "");
  const end = String(formData.get("endDate") ?? "");
  if (!name || amountCents === null || !start) return;
  await db.expense.create({
    data: {
      name,
      category: String(formData.get("category") ?? "software"),
      amountCents,
      startDate: new Date(start),
      endDate: end ? new Date(end) : null,
    },
  });
  revalidatePath("/expenses");
  revalidatePath("/");
}

export async function endExpense(formData: FormData) {
  await db.expense.update({
    where: { id: String(formData.get("id")) },
    data: { endDate: new Date(new Date().toISOString().slice(0, 10)) },
  });
  revalidatePath("/expenses");
  revalidatePath("/");
}

export async function deleteExpense(formData: FormData) {
  await db.expense.delete({ where: { id: String(formData.get("id")) } });
  revalidatePath("/expenses");
  revalidatePath("/");
}
