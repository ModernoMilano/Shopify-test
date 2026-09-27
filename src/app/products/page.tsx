import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";
import { db } from "@/lib/db";
import { formatCents, formatPct } from "@/lib/money";
import { getProfitSettings } from "@/lib/settings";
import { saveProductCost } from "./actions";
import { ImportForm } from "./ImportForm";

export const dynamic = "force-dynamic";

const toInput = (cents: number | undefined) => (cents === undefined ? "" : (cents / 100).toFixed(2).replace(".", ","));

export default async function ProductsPage({ searchParams }: { searchParams: Promise<Record<string, string>> }) {
  const { q = "", missing, supplier } = await searchParams;
  const [products, suppliers, settings] = await Promise.all([
    db.product.findMany({
      where: {
        ...(q ? { title: { contains: q, mode: "insensitive" as const } } : {}),
        ...(missing ? { costRules: { none: {} } } : {}),
        ...(supplier ? { supplierId: supplier } : {}),
      },
      include: {
        variants: { select: { priceCents: true } },
        costRules: { where: { variantId: null }, orderBy: { validFrom: "desc" }, take: 1 },
        _count: { select: { costRules: true } },
      },
      orderBy: [{ status: "asc" }, { title: "asc" }],
      take: 500,
    }),
    db.supplier.findMany({ orderBy: { name: "asc" } }),
    getProfitSettings(),
  ]);
  const totalMissing = await db.product.count({ where: { costRules: { none: {} } } });

  return (
    <div className="mx-auto max-w-7xl">
      <PageHeader
        title="Producten & kostprijs"
        subtitle={
          <>
            Vul per product de inkoopprijs en verzendkosten van je leverancier in (per stuk, ex btw). Een wijziging geldt vanaf
            vandaag; oudere orders houden de oude prijs. {totalMissing > 0 && <strong>{totalMissing} producten zonder kostprijs.</strong>}
          </>
        }
      >
        <a href="/api/export/costs" className="btn btn-ghost">
          Exporteer CSV
        </a>
      </PageHeader>

      <div className="mb-4 flex flex-wrap items-center gap-2">
        <form className="flex flex-wrap items-center gap-2">
          <input name="q" defaultValue={q} placeholder="Zoek product…" className="input w-56" />
          <select name="supplier" defaultValue={supplier ?? ""} className="input">
            <option value="">Alle leveranciers</option>
            {suppliers.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
          <label className="flex items-center gap-1.5 text-sm text-ink-2">
            <input type="checkbox" name="missing" value="1" defaultChecked={!!missing} /> alleen zonder kostprijs
          </label>
          <button className="btn btn-ghost">Filter</button>
          {(q || missing || supplier) && (
            <Link href="/products" className="text-sm text-ink-3 underline">
              wis filters
            </Link>
          )}
        </form>
      </div>

      <div className="card overflow-x-auto">
        <table className="data">
          <thead>
            <tr>
              <th>Product</th>
              <th className="r">Prijs</th>
              <th>Inkoop / stuk</th>
              <th>Verzending / stuk</th>
              <th>Leverancier</th>
              <th className="r">Marge / stuk</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {products.map((p) => {
              const prices = p.variants.map((v) => v.priceCents);
              const price = prices.length ? Math.max(...prices) : 0;
              const rule = p.costRules[0];
              const priceEx = price / (1 + settings.vatRate);
              const fee = price * settings.paymentFeePercent + settings.paymentFeeFixedCents;
              const margin = rule ? priceEx - rule.unitCostCents - rule.shippingCostCents - fee : null;
              const formId = `f-${p.id}`;
              return (
                <tr key={p.id}>
                  <td className="max-w-[20rem]">
                    <div className="flex items-center gap-2">
                      {p.imageUrl ? (
                        // eslint-disable-next-line @next/next/no-img-element
                        <img src={p.imageUrl} alt="" className="size-9 shrink-0 rounded object-cover" />
                      ) : (
                        <div className="size-9 shrink-0 rounded bg-surface-2" />
                      )}
                      <div className="min-w-0">
                        <div className="truncate">{p.title}</div>
                        <div className="text-xs text-ink-3">
                          {p.status?.toLowerCase()} · {p.variants.length} varianten
                          {p._count.costRules > 1 && ` · ${p._count.costRules} prijswijzigingen`}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="r">{formatCents(price)}</td>
                  <td>
                    <input form={formId} name="unitCost" defaultValue={toInput(rule?.unitCostCents)} placeholder="0,00" inputMode="decimal" className="input w-24" aria-label="Inkoopprijs" />
                  </td>
                  <td>
                    <input form={formId} name="shippingCost" defaultValue={toInput(rule?.shippingCostCents)} placeholder="0,00" inputMode="decimal" className="input w-24" aria-label="Verzendkosten" />
                  </td>
                  <td>
                    <select form={formId} name="supplierId" defaultValue={p.supplierId ?? ""} className="input w-40" aria-label="Leverancier">
                      <option value="">—</option>
                      {suppliers.map((s) => (
                        <option key={s.id} value={s.id}>
                          {s.name}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td className={`r ${margin !== null && margin < 0 ? "text-neg" : ""}`}>
                    {margin === null ? (
                      <span className="text-warn">ontbreekt</span>
                    ) : (
                      <>
                        {formatCents(Math.round(margin))} <span className="text-ink-3">{formatPct(priceEx ? margin / priceEx : null)}</span>
                      </>
                    )}
                  </td>
                  <td>
                    <form id={formId} action={saveProductCost}>
                      <input type="hidden" name="productId" value={p.id} />
                      <button className="btn btn-ghost">Opslaan</button>
                    </form>
                  </td>
                </tr>
              );
            })}
            {products.length === 0 && (
              <tr>
                <td colSpan={7} className="py-8 text-center text-ink-3">
                  Geen producten gevonden. Synchroniseer eerst met Shopify via Instellingen.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <p className="mt-2 text-xs text-ink-3">
        Marge / stuk = hoogste variantprijs ex {formatPct(settings.vatRate)} btw − inkoop − verzending − geschatte transactiekosten.
      </p>

      <section className="card mt-8 p-4">
        <h2 className="font-medium">Snel alles invullen via Excel/Google Sheets</h2>
        <p className="mt-1 mb-3 text-sm text-ink-2">
          Exporteer de CSV, vul de kolommen <code>kostprijs</code>, <code>verzendkosten</code> en <code>leverancier</code> in en importeer hem
          hier. Lege kostprijzen worden overgeslagen; nieuwe leveranciers worden automatisch aangemaakt.
        </p>
        <ImportForm />
      </section>
    </div>
  );
}
