import { db } from "@/lib/db";
import { toCsv } from "@/lib/csv";

export const dynamic = "force-dynamic";

export async function GET() {
  const products = await db.product.findMany({
    include: {
      supplier: { select: { name: true } },
      variants: { select: { priceCents: true } },
      costRules: { where: { variantId: null }, orderBy: { validFrom: "desc" }, take: 1 },
    },
    orderBy: { title: "asc" },
  });
  const fmt = (c: number | undefined) => (c === undefined ? "" : (c / 100).toFixed(2).replace(".", ","));
  const rows = [
    ["product_id", "titel", "status", "verkoopprijs", "kostprijs", "verzendkosten", "leverancier"],
    ...products.map((p) => [
      p.id,
      p.title,
      p.status,
      fmt(Math.max(0, ...p.variants.map((v) => v.priceCents))),
      fmt(p.costRules[0]?.unitCostCents),
      fmt(p.costRules[0]?.shippingCostCents),
      p.supplier?.name ?? "",
    ]),
  ];
  // BOM + puntkomma zodat Nederlandse Excel het bestand direct goed opent
  return new Response("\uFEFF" + toCsv(rows, ";"), {
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="kostprijzen-${new Date().toISOString().slice(0, 10)}.csv"`,
    },
  });
}
