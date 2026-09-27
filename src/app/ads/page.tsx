import { PageHeader } from "@/components/PageHeader";
import { db } from "@/lib/db";
import { formatCents } from "@/lib/money";
import { dayKey } from "@/lib/period";
import { deleteAdSpend, saveAdSpend } from "./actions";
import { CHANNELS, channelLabel } from "./channels";
import { ImportAds } from "./ImportAds";

export const dynamic = "force-dynamic";

export default async function AdsPage() {
  const since = new Date(Date.now() - 90 * 86_400_000);
  const entries = await db.adSpend.findMany({ where: { date: { gte: since } }, orderBy: [{ date: "desc" }, { channel: "asc" }] });
  const byChannel = new Map<string, number>();
  for (const e of entries) byChannel.set(e.channel, (byChannel.get(e.channel) ?? 0) + e.amountCents);

  return (
    <div className="mx-auto max-w-5xl">
      <PageHeader
        title="Advertenties"
        subtitle="Dagelijkse ad spend per kanaal. Nodig voor nettowinst en ROAS. Een bestaande dag+kanaal wordt overschreven."
      />

      <div className="grid gap-4 md:grid-cols-2">
        <form action={saveAdSpend} className="card flex flex-wrap items-end gap-2 p-4">
          <label className="text-sm">
            Datum
            <input type="date" name="date" required defaultValue={dayKey(new Date())} className="input mt-1 block" />
          </label>
          <label className="text-sm">
            Kanaal
            <select name="channel" className="input mt-1 block">
              {CHANNELS.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.label}
                </option>
              ))}
            </select>
          </label>
          <label className="text-sm">
            Bedrag (€)
            <input name="amount" required inputMode="decimal" placeholder="0,00" className="input mt-1 block w-28" />
          </label>
          <button className="btn">Toevoegen</button>
        </form>
        <div className="card p-4">
          <div className="mb-2 text-sm text-ink-2">
            Bulk: exporteer per dag uit Ads Manager (kolommen <code>datum</code>, <code>bedrag</code>, optioneel <code>kanaal</code>).
          </div>
          <ImportAds />
        </div>
      </div>

      <div className="mt-6 grid gap-3 sm:grid-cols-3">
        {[...byChannel.entries()].map(([ch, cents]) => (
          <div key={ch} className="card p-4">
            <div className="text-sm text-ink-2">{channelLabel(ch)} · 90 dagen</div>
            <div className="num mt-1 text-xl font-semibold">{formatCents(cents, true)}</div>
          </div>
        ))}
      </div>

      <div className="card mt-6 overflow-x-auto">
        <table className="data">
          <thead>
            <tr>
              <th>Datum</th>
              <th>Kanaal</th>
              <th className="r">Bedrag</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {entries.map((e) => (
              <tr key={e.id}>
                <td>{e.date.toISOString().slice(0, 10)}</td>
                <td>{channelLabel(e.channel)}</td>
                <td className="r">{formatCents(e.amountCents)}</td>
                <td className="text-right">
                  <form action={deleteAdSpend}>
                    <input type="hidden" name="id" value={e.id} />
                    <button className="text-xs text-ink-3 underline">verwijder</button>
                  </form>
                </td>
              </tr>
            ))}
            {entries.length === 0 && (
              <tr>
                <td colSpan={4} className="py-8 text-center text-ink-3">
                  Nog geen ad spend ingevoerd.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
