"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { db } from "@/lib/db";

const str = (f: FormData, k: string) => {
  const v = String(f.get(k) ?? "").trim();
  return v || null;
};
const int = (f: FormData, k: string) => {
  const v = Number(String(f.get(k) ?? "").trim());
  return String(f.get(k) ?? "").trim() && Number.isFinite(v) ? Math.round(v) : null;
};

export async function saveSupplier(formData: FormData) {
  const id = str(formData, "id");
  const data = {
    name: str(formData, "name") ?? "Naamloos",
    kind: str(formData, "kind") ?? "dropship",
    contactName: str(formData, "contactName"),
    email: str(formData, "email"),
    website: str(formData, "website"),
    country: str(formData, "country"),
    processingDays: int(formData, "processingDays"),
    shippingDays: int(formData, "shippingDays"),
    notes: str(formData, "notes"),
    active: formData.get("active") === "on",
  };
  if (id) await db.supplier.update({ where: { id }, data });
  else await db.supplier.create({ data });
  revalidatePath("/suppliers");
  redirect("/suppliers");
}

export async function deleteSupplier(formData: FormData) {
  await db.supplier.delete({ where: { id: String(formData.get("id")) } });
  revalidatePath("/suppliers");
  redirect("/suppliers");
}
