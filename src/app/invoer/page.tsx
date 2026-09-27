import { PageHeader } from "@/components/PageHeader";
import { Card, day, euro } from "@/components/ui";
import { db } from "@/lib/db";
import { dayKey } from "@/lib/period";
import {
  addInvoice,
  addManualEntry,
  addSnapshot,
  addTeamCost,
  deleteInvoice,
  deleteManualEntry,
  deleteTeamCost,
  saveLoan,
  toggleInvoicePaid,
} from "./actions";

export const dynamic = "force-dynamic";

const KINDS: Record<string, string> = {
  paypal_fees: "PayPal fees",
  fees: "Overige fees",
  chargebacks: "Chargebacks en disputes",
  cogs: "COGS (niet via bank)",
  meta: "Meta (niet via bank)",
  other: "Overige kosten",
  team: "Teamkosten eenmalig",
  inventory: "Toename voorraadwaarde",
};

export default async function InputPage() {
  const today = dayKey(new Date());
  const monthStart = today.slice(0, 8) + "01";
  const [team, entries, snaps, invoices, loans] = await Promise.all([
    db.expense.findMany({ where: { category: "team" }, orderBy: { startDate: "desc" } }),
    db.manualEntry.findMany({ orderBy: { periodStart: "desc" } }),
    db.moneySnapshot.findMany({ orderBy: { takenAt: "desc" }, take: 5 }),
    db.supplierInvoice.findMany({ orderBy: [{ paid: "asc" }, { dueDate: "asc" }] }),
    db.loan.findMany({ orderBy: { startDate: "desc" } }),
  ]);
  const teamMonthly = team.filter((t) => !t.endDate || t.endDate >= new Date()).reduce((s, t) => s + t.amountCents, 0);

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <PageHeader title="Handmatige invoer" subtitle="Alles wat niet uit een koppeling komt. Deze bedragen krijgen overal het label handmatig." />

      <Card title="Waar het geld staat, nieuwe stand" action={<span className="text-xs text-ink-3">laat bank leeg om het saldo uit de bankmutaties te nemen</span>}>
        <form action={addSnapshot} className="grid gap-2 text-sm sm:grid-cols-4">
          <label>
            Bank
            <input name="bank" inputMode="decimal" className="input mt-1 w-full" placeholder="uit bank" />
          </label>
          <label>
            Payout ingepland
            <input name="payout" inputMode="decimal" className="input mt-1 w-full" required />
          </label>
          <label>
            Payout datum
            <input name="payoutDate" type="date" className="input mt-1 w-full" />
          </label>
          <label>
            Pending
            <input name="pending" inputMode="decimal" className="input mt-1 w-full" required />
          </label>
          <label>
            Hold (reserve)
            <input name="hold" inputMode="decimal" className="input mt-1 w-full" required />
          </label>
          <label>
            PayPal
            <input name="paypal" inputMode="decimal" className="input mt-1 w-full" required />
          </label>
          <label className="sm:col-span-2">
            Notitie
            <input name="note" className="input mt-1 w-full" />
          </label>
          <div className="sm:col-span-4">
            <button className="btn">Stand opslaan</button>
          </div>
        </form>
        <ul className="mt-3 space-y-1 text-xs text-ink-2">
          {snaps.map((s) => (
            <li key={s.id}>
              {s.takenAt.toLocaleString("nl-NL", { timeZone: "Europe/Amsterdam", dateStyle: "medium", timeStyle: "short" })}: payout {euro(s.payoutScheduledCents, true)}, pending{" "}
              {euro(s.pendingCents, true)}, hold {euro(s.holdCents, true)}, PayPal {euro(s.paypalCents, true)}
              {s.note && <span className="text-ink-3">. {s.note}</span>}
            </li>
          ))}
        </ul>
      </Card>

      <Card title="Teamkosten per maand" action={<span className="num text-sm">{euro(teamMonthly)} per maand</span>}>
        <form action={addTeamCost} className="mb-3 flex flex-wrap items-end gap-2 text-sm">
          <input name="name" placeholder="rol of naam, bv. media buyer" className="input w-56" required />
          <input name="amount" placeholder="per maand" inputMode="decimal" className="input w-28" required />
          <label className="text-xs text-ink-3">
            vanaf
            <input type="date" name="start" defaultValue={monthStart} className="input ml-1" required />
          </label>
          <label className="text-xs text-ink-3">
            tot
            <input type="date" name="end" className="input ml-1" />
          </label>
          <button className="btn">Toevoegen</button>
        </form>
        <table className="data">
          <tbody>
            {team.map((t) => (
              <tr key={t.id}>
                <td>{t.name}</td>
                <td className="r">{euro(t.amountCents)}</td>
                <td className="text-ink-2">
                  {day(t.startDate)} t/m {t.endDate ? day(t.endDate) : "doorlopend"}
                </td>
                <td className="text-right">
                  <form action={deleteTeamCost}>
                    <input type="hidden" name="id" value={t.id} />
                    <button className="text-xs text-ink-3 underline">verwijder</button>
                  </form>
                </td>
              </tr>
            ))}
            {team.length === 0 && (
              <tr>
                <td className="text-warn">Nog geen teamkosten. De winst is daardoor te hoog.</td>
              </tr>
            )}
          </tbody>
        </table>
      </Card>

      <Card title="Openstaande leveranciersfacturen">
        <form action={addInvoice} className="mb-3 grid gap-2 text-sm sm:grid-cols-4">
          <input name="supplier" placeholder="leverancier" className="input" required />
          <input name="amount" placeholder="bedrag" inputMode="decimal" className="input" required />
          <label className="text-xs text-ink-3">
            factuurdatum
            <input type="date" name="invoiceDate" defaultValue={today} className="input mt-1 w-full" required />
          </label>
          <label className="text-xs text-ink-3">
            vervaldatum
            <input type="date" name="dueDate" className="input mt-1 w-full" />
          </label>
          <label className="text-xs text-ink-3">
            hoort bij verkopen vanaf
            <input type="date" name="salesFrom" className="input mt-1 w-full" />
          </label>
          <label className="text-xs text-ink-3">
            tot en met
            <input type="date" name="salesTo" className="input mt-1 w-full" />
          </label>
          <input name="note" placeholder="notitie" className="input self-end" />
          <button className="btn self-end">Toevoegen</button>
        </form>
        <table className="data">
          <tbody>
            {invoices.map((i) => (
              <tr key={i.id} className={i.paid ? "opacity-50" : ""}>
                <td>{i.supplierName}</td>
                <td className="r">{euro(i.amountCents)}</td>
                <td className="text-ink-2">
                  {day(i.invoiceDate)}
                  {i.dueDate && `, vervalt ${day(i.dueDate)}`}
                  {i.salesFrom && i.salesTo && <span className="text-ink-3">, verkopen {day(i.salesFrom)} t/m {day(i.salesTo)}</span>}
                </td>
                <td className="text-right whitespace-nowrap">
                  <form action={toggleInvoicePaid} className="inline">
                    <input type="hidden" name="id" value={i.id} />
                    <button className="btn btn-ghost">{i.paid ? "Toch open" : "Betaald"}</button>
                  </form>{" "}
                  <form action={deleteInvoice} className="inline">
                    <input type="hidden" name="id" value={i.id} />
                    <button className="text-xs text-ink-3 underline">verwijder</button>
                  </form>
                </td>
              </tr>
            ))}
            {invoices.length === 0 && (
              <tr>
                <td className="text-ink-3">Geen openstaande facturen. Nodig voor de waarschuwing fulfillment eerst.</td>
              </tr>
            )}
          </tbody>
        </table>
        <p className="mt-2 text-xs text-ink-3">
          Een betaalde factuur staat ook op de bank. Hoort die bij een andere verkoopperiode, pas dan bij Bankmutaties de datum hoort bij periode aan.
        </p>
      </Card>

      <Card title="Overige posten over een periode">
        <form action={addManualEntry} className="mb-3 grid gap-2 text-sm sm:grid-cols-6">
          <select name="kind" className="input sm:col-span-2">
            {Object.entries(KINDS).map(([k, v]) => (
              <option key={k} value={k}>
                {v}
              </option>
            ))}
          </select>
          <input name="label" placeholder="omschrijving" className="input sm:col-span-2" required />
          <input name="amount" placeholder="bedrag" inputMode="decimal" className="input" required />
          <span />
          <label className="text-xs text-ink-3 sm:col-span-2">
            van
            <input type="date" name="start" defaultValue={monthStart} className="input mt-1 w-full" required />
          </label>
          <label className="text-xs text-ink-3 sm:col-span-2">
            tot en met
            <input type="date" name="end" defaultValue={today} className="input mt-1 w-full" />
          </label>
          <button className="btn self-end">Toevoegen</button>
        </form>
        <table className="data">
          <tbody>
            {entries.map((e) => (
              <tr key={e.id}>
                <td>
                  {e.label} <span className="text-xs text-ink-3">{KINDS[e.kind] ?? e.kind}</span>
                  {e.note && <div className="text-xs text-ink-3">{e.note}</div>}
                </td>
                <td className="r">{euro(e.amountCents)}</td>
                <td className="whitespace-nowrap text-ink-2">
                  {day(e.periodStart)} t/m {day(e.periodEnd)}
                </td>
                <td className="text-right">
                  <form action={deleteManualEntry}>
                    <input type="hidden" name="id" value={e.id} />
                    <button className="text-xs text-ink-3 underline">verwijder</button>
                  </form>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>

      <Card title="Leningen">
        {loans.map((l) => (
          <form key={l.id} action={saveLoan} className="mb-2 flex flex-wrap items-end gap-2 text-sm">
            <input type="hidden" name="id" value={l.id} />
            <input name="lender" defaultValue={l.lender} className="input w-40" />
            <input name="principal" defaultValue={(l.principalCents / 100).toFixed(2).replace(".", ",")} className="input w-28" aria-label="Hoofdsom" />
            <input type="date" name="start" defaultValue={l.startDate.toISOString().slice(0, 10)} className="input" />
            <input name="repaid" defaultValue={(l.repaidCents / 100).toFixed(2).replace(".", ",")} className="input w-28" aria-label="Afgelost" title="Afgelost" />
            <input name="schedule" defaultValue={l.schedule ?? ""} placeholder="aflossingsschema" className="input w-56" />
            <button className="btn btn-ghost">Opslaan</button>
          </form>
        ))}
        <form action={saveLoan} className="flex flex-wrap items-end gap-2 border-t border-line pt-3 text-sm">
          <input name="lender" placeholder="geldverstrekker" className="input w-40" required />
          <input name="principal" placeholder="bedrag" className="input w-28" required />
          <input type="date" name="start" defaultValue={today} className="input" required />
          <input name="schedule" placeholder="aflossingsschema" className="input w-56" />
          <button className="btn">Lening toevoegen</button>
        </form>
      </Card>
    </div>
  );
}
