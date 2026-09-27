import { PageHeader } from "@/components/PageHeader";
import { db } from "@/lib/db";
import { formatCents } from "@/lib/money";
import { addExpense, deleteExpense, endExpense } from "./actions";

export const dynamic = "force-dynamic";

const CATEGORIES: Record<string, string> = {
  software: "Software & apps",
  shopify: "Shopify",
  personeel: "Personeel / freelancers",
  content: "Content & fotografie",
  kantoor: "Kantoor",
  overig: "Overig",
};

export default async function ExpensesPage() {
  const expenses = await db.expense.findMany({ orderBy: [{ endDate: "asc" }, { amountCents: "desc" }] });
  const today = new Date();
  const active = expenses.filter((e) => !e.endDate || e.endDate >= today);
  const monthly = active.reduce((s, e) => s + e.amountCents, 0);

  return (
    <div className="mx-auto max-w-5xl">
      <PageHeader
        title="Vaste lasten"
        subtitle="Maandelijkse kosten die niet per order zijn: apps, abonnementen, personeel. Worden per dag omgeslagen in het dashboard."
      >
        <div className="card px-4 py-2 text-sm">
          Actief per maand: <span className="num font-semibold">{formatCents(monthly)}</span>
        </div>
      </PageHeader>

      <form action={addExpense} className="card mb-6 flex flex-wrap items-end gap-2 p-4">
        <label className="text-sm">
          Omschrijving
          <input name="name" required placeholder="bv. Klaviyo" className="input mt-1 block w-48" />
        </label>
        <label className="text-sm">
          Categorie
          <select name="category" className="input mt-1 block">
            {Object.entries(CATEGORIES).map(([k, v]) => (
              <option key={k} value={k}>
                {v}
              </option>
            ))}
          </select>
        </label>
        <label className="text-sm">
          Per maand (€)
          <input name="amount" required inputMode="decimal" placeholder="0,00" className="input mt-1 block w-28" />
        </label>
        <label className="text-sm">
          Vanaf
          <input type="date" name="startDate" required defaultValue={today.toISOString().slice(0, 8) + "01"} className="input mt-1 block" />
        </label>
        <label className="text-sm">
          Tot en met (optioneel)
          <input type="date" name="endDate" className="input mt-1 block" />
        </label>
        <button className="btn">Toevoegen</button>
      </form>

      <div className="card overflow-x-auto">
        <table className="data">
          <thead>
            <tr>
              <th>Omschrijving</th>
              <th>Categorie</th>
              <th className="r">Per maand</th>
              <th>Periode</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {expenses.map((e) => {
              const ended = e.endDate && e.endDate < today;
              return (
                <tr key={e.id} className={ended ? "opacity-50" : ""}>
                  <td className="font-medium">{e.name}</td>
                  <td>{CATEGORIES[e.category] ?? e.category}</td>
                  <td className="r">{formatCents(e.amountCents)}</td>
                  <td className="text-sm text-ink-2">
                    {e.startDate.toISOString().slice(0, 10)} – {e.endDate ? e.endDate.toISOString().slice(0, 10) : "doorlopend"}
                  </td>
                  <td className="whitespace-nowrap text-right">
                    {!e.endDate && (
                      <form action={endExpense} className="inline">
                        <input type="hidden" name="id" value={e.id} />
                        <button className="text-xs text-ink-3 underline">stop per vandaag</button>
                      </form>
                    )}{" "}
                    <form action={deleteExpense} className="inline">
                      <input type="hidden" name="id" value={e.id} />
                      <button className="text-xs text-neg underline">verwijder</button>
                    </form>
                  </td>
                </tr>
              );
            })}
            {expenses.length === 0 && (
              <tr>
                <td colSpan={5} className="py-8 text-center text-ink-3">
                  Nog geen vaste lasten ingevoerd.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
