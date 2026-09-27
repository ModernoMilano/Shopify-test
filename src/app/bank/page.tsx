import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";
import { PeriodPicker } from "@/components/PeriodPicker";
import { Card, day, euro } from "@/components/ui";
import { db } from "@/lib/db";
import { resolvePeriod } from "@/lib/period";
import { CATEGORIES, categoryLabel, totalsByCategory } from "@/bank/categories";
import { bankTransactionsIn } from "@/finance/data";
import { addRule, deleteRule, reapplyRules, updateTransaction } from "./actions";
import { UploadForm } from "./UploadForm";

export const dynamic = "force-dynamic";

const KIND_LABEL: Record<string, string> = {
  income: "omzet (cash)",
  cost: "kosten",
  debt: "schuld, geen omzet",
  equity: "eigen vermogen",
  private: "opname, geen kosten",
  neutral: "telt niet mee",
  unknown: "toewijzen",
};

export default async function BankPage({ searchParams }: { searchParams: Promise<Record<string, string>> }) {
  const params = await searchParams;
  const period = resolvePeriod(params, new Date(), "mtd");
  const { cat, q } = params;
  const [all, imports, rules] = await Promise.all([
    bankTransactionsIn(period.fromKey, period.toKey),
    db.bankImport.findMany({ orderBy: { createdAt: "desc" }, take: 5 }),
    db.categoryRule.findMany({ orderBy: [{ priority: "asc" }, { pattern: "asc" }] }),
  ]);
  const totals = totalsByCategory(all);
  const txs = all.filter(
    (t) =>
      (!cat || t.category === cat || (cat === "bank_fees" && t.feeCents > 0)) &&
      (!q || `${t.description} ${t.details}`.toLowerCase().includes(q.toLowerCase())),
  );
  const inSum = all.filter((t) => t.category !== "internal" && t.amountCents > 0).reduce((s, t) => s + t.amountCents, 0);
  const outSum = all.filter((t) => t.category !== "internal" && t.amountCents < 0).reduce((s, t) => s + t.amountCents, 0);
  const qs = (extra: Record<string, string | undefined>) => {
    const u = new URLSearchParams({ from: period.fromKey, to: period.toKey });
    for (const [k, v] of Object.entries({ cat, q, ...extra })) if (v) u.set(k, v);
    return `/bank?${u}`;
  };

  return (
    <div className="mx-auto max-w-7xl">
      <PageHeader title="Bankmutaties" subtitle="Revolut Pro. Mutaties tellen in de periode van hun datum hoort bij periode.">
        <PeriodPicker period={period} basePath="/bank" />
      </PageHeader>

      <div className="mb-6 grid gap-6 lg:grid-cols-2">
        <Card title="Afschrift importeren">
          <UploadForm />
          {imports.length > 0 && (
            <ul className="mt-4 space-y-1 text-xs text-ink-2">
              {imports.map((i) => (
                <li key={i.id}>
                  {i.createdAt.toLocaleDateString("nl-NL")}: {i.fileName}, {i.transactions} mutaties{" "}
                  {i.reconciled ? <span className="text-good">sluit</span> : <span className="text-neg">{i.message ?? "sluit niet"}</span>}
                </li>
              ))}
            </ul>
          )}
        </Card>
        <Card title="Totalen per categorie" action={<span className="text-xs text-ink-3">in {euro(inSum, true)}, uit {euro(outSum, true)}</span>}>
          <table className="data">
            <tbody>
              {CATEGORIES.filter((c) => totals.has(c.id)).map((c) => (
                <tr key={c.id}>
                  <td>
                    <Link href={qs({ cat: c.id })} className={`hover:underline ${c.id === "unknown" ? "font-medium text-neg" : ""}`}>
                      {c.label}
                    </Link>
                    <span className="ml-2 text-xs text-ink-3">{KIND_LABEL[c.kind]}</span>
                  </td>
                  <td className={`r ${totals.get(c.id)! < 0 ? "" : "text-good"}`}>{euro(totals.get(c.id)!)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      </div>

      <div className="mb-3 flex flex-wrap items-center gap-2">
        <form action="/bank" className="flex flex-wrap items-center gap-2">
          <input type="hidden" name="from" value={period.fromKey} />
          <input type="hidden" name="to" value={period.toKey} />
          <input name="q" defaultValue={q} placeholder="Zoek omschrijving…" className="input w-56" />
          <select name="cat" defaultValue={cat ?? ""} className="input">
            <option value="">Alle categorieën</option>
            {CATEGORIES.map((c) => (
              <option key={c.id} value={c.id}>
                {c.label}
              </option>
            ))}
          </select>
          <button className="btn btn-ghost">Filter</button>
        </form>
        {(cat || q) && (
          <Link href={`/bank?from=${period.fromKey}&to=${period.toKey}`} className="text-sm text-ink-3 underline">
            wis filters
          </Link>
        )}
        <span className="ml-auto text-sm text-ink-3">{txs.length} mutaties</span>
      </div>

      <div className="card overflow-x-auto">
        <table className="data">
          <thead>
            <tr>
              <th>Datum</th>
              <th>Omschrijving</th>
              <th className="r">Bedrag</th>
              <th>Categorie en periode</th>
            </tr>
          </thead>
          <tbody>
            {txs.map((t) => {
              const formId = `tx-${t.id}`;
              const suggestion = t.description.replace(/^(To|Betaling van)\s+/i, "");
              return (
                <tr key={t.id} className={t.category === "unknown" ? "bg-surface-2" : ""}>
                  <td className="whitespace-nowrap">{day(t.bookedAt)}</td>
                  <td className="max-w-[26rem]">
                    <div className="font-medium">{t.description}</div>
                    <div className="truncate text-xs text-ink-3" title={t.details}>
                      {t.details.split("\n").filter((l) => !l.startsWith("Kaart:")).join(", ")}
                    </div>
                    {t.note && <div className="text-xs text-warn">{t.note}</div>}
                  </td>
                  <td className={`r ${t.amountCents > 0 ? "text-good" : ""}`}>
                    {euro(t.amountCents)}
                    {t.feeCents > 0 && <div className="text-xs text-ink-3">waarvan {euro(t.feeCents)} kosten</div>}
                  </td>
                  <td>
                    <form id={formId} action={updateTransaction} className="flex items-center gap-1.5 whitespace-nowrap">
                      <input type="hidden" name="id" value={t.id} />
                      <select name="category" defaultValue={t.category} className="input w-40" aria-label="Categorie">
                        {CATEGORIES.map((c) => (
                          <option key={c.id} value={c.id}>
                            {c.label}
                          </option>
                        ))}
                      </select>
                      <input
                        type="date"
                        name="periodDate"
                        defaultValue={(t.periodDate ?? t.bookedAt).toISOString().slice(0, 10)}
                        className={`input w-36 ${t.periodDate ? "border-warn" : ""}`}
                        aria-label="Hoort bij periode"
                        title="Hoort bij periode"
                      />
                      <details className="relative text-xs">
                        <summary className="cursor-pointer text-ink-3">regel</summary>
                        <div className="card absolute right-0 z-20 mt-1 w-64 space-y-1 p-2 whitespace-normal shadow-lg">
                          <label className="flex items-center gap-1">
                            <input type="checkbox" name="makeRule" /> voortaan automatisch als de tekst bevat:
                          </label>
                          <input name="rulePattern" defaultValue={suggestion} className="input w-full" />
                        </div>
                      </details>
                      <button className="btn btn-ghost">Opslaan</button>
                      {t.categorySource === "handmatig" && <span className="text-[10px] text-warn">handmatig</span>}
                    </form>
                  </td>
                </tr>
              );
            })}
            {txs.length === 0 && (
              <tr>
                <td colSpan={4} className="py-8 text-center text-ink-3">
                  Geen mutaties in deze periode. Importeer een afschrift.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <Card title="Regels" className="mt-8" action={<form action={reapplyRules}><button className="btn btn-ghost">Regels opnieuw toepassen</button></form>}>
        <p className="mb-3 text-sm text-ink-2">
          Bevat de omschrijving of een detailregel de tekst, dan krijgt de mutatie de categorie. Lagere prioriteit gaat voor. Handmatig ingedeelde mutaties
          blijven zoals ze zijn.
        </p>
        <form action={addRule} className="mb-4 flex flex-wrap items-end gap-2 text-sm">
          <input name="pattern" placeholder="tekst, bv. Klaviyo" className="input w-48" required />
          <select name="direction" className="input">
            <option value="any">in en uit</option>
            <option value="in">alleen ontvangen</option>
            <option value="out">alleen uitgegeven</option>
          </select>
          <select name="category" className="input">
            {CATEGORIES.filter((c) => c.id !== "unknown").map((c) => (
              <option key={c.id} value={c.id}>
                {c.label}
              </option>
            ))}
          </select>
          <input name="priority" type="number" defaultValue={50} className="input w-20" aria-label="Prioriteit" />
          <button className="btn">Regel toevoegen</button>
        </form>
        <div className="overflow-x-auto">
          <table className="data">
            <thead>
              <tr>
                <th>Tekst bevat</th>
                <th>Richting</th>
                <th>Categorie</th>
                <th className="r">Prioriteit</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {rules.map((r) => (
                <tr key={r.id}>
                  <td className="font-mono text-xs">{r.pattern}</td>
                  <td className="text-ink-2">{r.direction === "in" ? "ontvangen" : r.direction === "out" ? "uitgegeven" : "beide"}</td>
                  <td>{categoryLabel(r.category)}</td>
                  <td className="r">{r.priority}</td>
                  <td className="text-right">
                    <form action={deleteRule}>
                      <input type="hidden" name="id" value={r.id} />
                      <button className="text-xs text-ink-3 underline">verwijder</button>
                    </form>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
