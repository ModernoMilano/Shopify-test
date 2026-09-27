import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";
import { db } from "@/lib/db";
import { deleteSupplier, saveSupplier } from "./actions";

export const dynamic = "force-dynamic";

const KINDS: Record<string, string> = { dropship: "Dropshipping", pod: "Print on demand", wholesale: "Inkoop / voorraad" };

export default async function SuppliersPage({ searchParams }: { searchParams: Promise<Record<string, string>> }) {
  const { edit } = await searchParams;
  const suppliers = await db.supplier.findMany({
    orderBy: [{ active: "desc" }, { name: "asc" }],
    include: { _count: { select: { products: true } } },
  });
  const editing = edit && edit !== "new" ? suppliers.find((s) => s.id === edit) : undefined;
  const showForm = edit === "new" || !!editing;

  return (
    <div className="mx-auto max-w-5xl">
      <PageHeader title="Leveranciers" subtitle="Wie levert wat, hoe snel, en tegen welke afspraken.">
        {!showForm && (
          <Link href="/suppliers?edit=new" className="btn">
            + Leverancier
          </Link>
        )}
      </PageHeader>

      {showForm && (
        <form action={saveSupplier} className="card mb-6 grid gap-3 p-4 sm:grid-cols-2">
          <input type="hidden" name="id" value={editing?.id ?? ""} />
          <label className="text-sm">
            Naam
            <input name="name" required defaultValue={editing?.name} className="input mt-1 w-full" />
          </label>
          <label className="text-sm">
            Type
            <select name="kind" defaultValue={editing?.kind ?? "dropship"} className="input mt-1 w-full">
              {Object.entries(KINDS).map(([k, v]) => (
                <option key={k} value={k}>
                  {v}
                </option>
              ))}
            </select>
          </label>
          <label className="text-sm">
            Contactpersoon
            <input name="contactName" defaultValue={editing?.contactName ?? ""} className="input mt-1 w-full" />
          </label>
          <label className="text-sm">
            E-mail
            <input name="email" type="email" defaultValue={editing?.email ?? ""} className="input mt-1 w-full" />
          </label>
          <label className="text-sm">
            Website / portal
            <input name="website" defaultValue={editing?.website ?? ""} className="input mt-1 w-full" />
          </label>
          <label className="text-sm">
            Land
            <input name="country" defaultValue={editing?.country ?? ""} className="input mt-1 w-full" />
          </label>
          <label className="text-sm">
            Verwerkingstijd (dagen)
            <input name="processingDays" type="number" min={0} defaultValue={editing?.processingDays ?? ""} className="input mt-1 w-full" />
          </label>
          <label className="text-sm">
            Levertijd naar klant (dagen)
            <input name="shippingDays" type="number" min={0} defaultValue={editing?.shippingDays ?? ""} className="input mt-1 w-full" />
          </label>
          <label className="text-sm sm:col-span-2">
            Notities (afspraken, MOQ, betaalvoorwaarden…)
            <textarea name="notes" rows={3} defaultValue={editing?.notes ?? ""} className="input mt-1 w-full" />
          </label>
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" name="active" defaultChecked={editing?.active ?? true} /> Actief
          </label>
          <div className="flex justify-end gap-2 sm:col-span-2">
            <Link href="/suppliers" className="btn btn-ghost">
              Annuleren
            </Link>
            <button className="btn">Opslaan</button>
          </div>
        </form>
      )}

      <div className="card overflow-x-auto">
        <table className="data">
          <thead>
            <tr>
              <th>Naam</th>
              <th>Type</th>
              <th>Land</th>
              <th className="r">Verwerking</th>
              <th className="r">Levertijd</th>
              <th className="r">Producten</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {suppliers.map((s) => (
              <tr key={s.id} className={s.active ? "" : "opacity-50"}>
                <td>
                  <div className="font-medium">{s.name}</div>
                  <div className="text-xs text-ink-3">{[s.contactName, s.email].filter(Boolean).join(" · ")}</div>
                </td>
                <td>{KINDS[s.kind] ?? s.kind}</td>
                <td>{s.country ?? "–"}</td>
                <td className="r">{s.processingDays != null ? `${s.processingDays} d` : "–"}</td>
                <td className="r">{s.shippingDays != null ? `${s.shippingDays} d` : "–"}</td>
                <td className="r">
                  <Link href={`/products?supplier=${s.id}`} className="underline">
                    {s._count.products}
                  </Link>
                </td>
                <td className="whitespace-nowrap text-right">
                  <Link href={`/suppliers?edit=${s.id}`} className="btn btn-ghost">
                    Bewerk
                  </Link>{" "}
                  {s._count.products === 0 && (
                    <form action={deleteSupplier} className="inline">
                      <input type="hidden" name="id" value={s.id} />
                      <button className="btn btn-ghost text-neg">Verwijder</button>
                    </form>
                  )}
                </td>
              </tr>
            ))}
            {suppliers.length === 0 && (
              <tr>
                <td colSpan={7} className="py-8 text-center text-ink-3">
                  Nog geen leveranciers.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
