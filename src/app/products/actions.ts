"use server";

import { revalidatePath } from "next/cache";
import { db } from "@/lib/db";
import { parseEuroToCents } from "@/lib/money";
import { parseCostCsv } from "@/lib/csv";

/** Oudste datum: eerste kostprijs van een product geldt ook voor alle oudere orders. */
const BEGINNING = new Date("2000-01-01T00:00:00Z");

async function upsertProductCost(productId: string, unitCostCents: number, shippingCostCents: number, note?: string) {
  const latest = await db.costRule.findFirst({
    where: { productId, variantId: null },
    orderBy: { validFrom: "desc" },
  });
  if (latest && latest.unitCostCents === unitCostCents && latest.shippingCostCents === shippingCostCents) return false;
  await db.costRule.create({
    data: {
      productId,
      unitCostCents,
      shippingCostCents,
      validFrom: latest ? new Date() : BEGINNING,
      note,
    },
  });
  return true;
}

export async function saveProductCost(formData: FormData) {
  const productId = String(formData.get("productId"));
  const unit = parseEuroToCents(String(formData.get("unitCost") ?? ""));
  const ship = parseEuroToCents(String(formData.get("shippingCost") ?? "")) ?? 0;
  const supplierId = String(formData.get("supplierId") ?? "") || null;

  if (unit !== null) await upsertProductCost(productId, unit, ship);
  await db.product.update({ where: { id: productId }, data: { supplierId } });
  revalidatePath("/products");
  revalidatePath("/");
}

export type ImportResult = { updated: number; unchanged: number; errors: string[] };

export async function importCosts(_prev: ImportResult | null, formData: FormData): Promise<ImportResult> {
  const file = formData.get("file");
  const text = file instanceof File && file.size > 0 ? await file.text() : String(formData.get("csv") ?? "");
  const { rows, errors } = parseCostCsv(text);

  const products = await db.product.findMany({ select: { id: true, handle: true, title: true } });
  const suppliers = await db.supplier.findMany({ select: { id: true, name: true } });
  const byKey = new Map<string, string>();
  for (const p of products) {
    byKey.set(p.id, p.id);
    if (p.handle) byKey.set(p.handle.toLowerCase(), p.id);
    byKey.set(p.title.toLowerCase(), p.id);
  }
  const supplierByName = new Map(suppliers.map((s) => [s.name.toLowerCase(), s.id]));

  let updated = 0;
  let unchanged = 0;
  for (const row of rows) {
    const productId = byKey.get(row.product.toLowerCase());
    if (!productId) {
      errors.push(`Regel ${row.line}: product "${row.product}" niet gevonden`);
      continue;
    }
    if (row.supplier) {
      let supplierId = supplierByName.get(row.supplier.toLowerCase());
      if (!supplierId) {
        const s = await db.supplier.create({ data: { name: row.supplier } });
        supplierId = s.id;
        supplierByName.set(row.supplier.toLowerCase(), s.id);
      }
      await db.product.update({ where: { id: productId }, data: { supplierId } });
    }
    const changed = await upsertProductCost(productId, row.unitCostCents, row.shippingCostCents, "CSV-import");
    if (changed) updated++;
    else unchanged++;
  }
  revalidatePath("/products");
  revalidatePath("/");
  return { updated, unchanged, errors };
}
