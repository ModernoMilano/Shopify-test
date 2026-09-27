import { PageHeader } from "@/components/PageHeader";
import { PeriodPicker } from "@/components/PeriodPicker";
import { Waterfall } from "@/components/Waterfall";
import { Card, euro } from "@/components/ui";
import { resolvePeriod } from "@/lib/period";
import { periodBridge, periodFinance } from "@/finance/data";

export const dynamic = "force-dynamic";

export default async function BridgePage({ searchParams }: { searchParams: Promise<Record<string, string>> }) {
  const period = resolvePeriod(await searchParams, new Date(), "mtd");
  const f = await periodFinance(period);
  const b = await periodBridge(period, f.pnl.profitCents, f.bank);

  return (
    <div className="mx-auto max-w-5xl">
      <PageHeader title="Winst naar bank" subtitle="Waarom je winst niet één op één op je bankrekening verschijnt.">
        <PeriodPicker period={period} basePath="/winst-naar-bank" />
      </PageHeader>

      {b.missing.length > 0 && (
        <div className="card mb-6 border-l-4 p-4 text-sm" style={{ borderLeftColor: "var(--warn)" }}>
          Niet alles is bekend voor deze periode: {b.missing.join(", ")}. De stap timing en afronding is daardoor minder betrouwbaar.
        </div>
      )}
      {b.timingWarning && (
        <div className="card mb-6 border-l-4 p-4 text-sm" style={{ borderLeftColor: "var(--warn)" }}>
          Timing en afronding ({euro(b.timing, true)}) is meer dan 5% van de winst. Kijk of er leveranciers of Meta-rekeningen bij een andere periode horen
          (pas dat aan bij Bankmutaties, kolom hoort bij periode).
        </div>
      )}

      <Card className="mb-6">
        <Waterfall steps={b.steps} endLabel="Groei bankrekening" />
      </Card>

      <Card title="Uitleg per stap">
        <table className="data">
          <tbody>
            {b.steps.map((s) => (
              <tr key={s.key}>
                <td>
                  <div className="font-medium">{s.label}</div>
                  <div className="text-xs text-ink-2">{s.explanation}</div>
                </td>
                <td className={`r ${s.cents < 0 ? "text-neg" : ""}`}>{euro(s.cents)}</td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr>
              <td>
                Groei bankrekening
                <div className="text-xs font-normal text-ink-3">
                  van {euro(b.bankBegin)} naar {euro(b.bankNow)}
                </div>
              </td>
              <td className="r">{euro(b.bankGrowth)}</td>
            </tr>
          </tfoot>
        </table>
        <p className="mt-3 text-xs text-ink-3">
          Shopify-saldo (payout, pending en reserve): begin {euro(b.shopifyBegin)}, nu {euro(b.shopifyNow)}.
        </p>
      </Card>
    </div>
  );
}
