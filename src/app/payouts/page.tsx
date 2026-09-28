import { PageHeader } from "@/components/PageHeader";
import { Card, day, euro, pct } from "@/components/ui";
import { db } from "@/lib/db";
import { payoutDifference } from "@/finance/calculations";
import { moneyNow } from "@/finance/data";
import { ImportPayouts } from "./ImportPayouts";

export const dynamic = "force-dynamic";

export default async function PayoutsPage() {
  const since30 = new Date(Date.now() - 30 * 86_400_000);
  const [payouts, disputes, money, paypalFees, paypalIn, pp] = await Promise.all([
    db.shopifyPayout.findMany({ orderBy: { payoutDate: "desc" }, take: 120 }),
    db.dispute.findMany({ orderBy: [{ dueBy: "asc" }] }),
    moneyNow(),
    db.manualEntry.findMany({ where: { kind: "paypal_fees" }, orderBy: { periodStart: "desc" } }),
    db.bankTransaction.aggregate({ where: { category: "paypal_payout" }, _sum: { amountCents: true }, _count: true }),
    db.paypalDaily.aggregate({
      where: { date: { gte: since30 } },
      _sum: { salesCents: true, salesCount: true, feesCents: true, refundsCents: true, withdrawalsCents: true },
      _count: true,
    }),
  ]);
  const withDiff = payouts.map((p) => ({
    p,
    diff:
      p.chargesCents === null
        ? null
        : payoutDifference({
            chargesCents: p.chargesCents,
            refundsCents: p.refundsCents ?? 0,
            adjustmentsCents: p.adjustmentsCents ?? 0,
            reservedFundsCents: p.reservedFundsCents ?? 0,
            feesCents: p.feesCents ?? 0,
            retriedCents: p.retriedCents ?? 0,
            totalCents: p.totalCents,
          }),
  }));
  const sum = (k: "chargesCents" | "refundsCents" | "adjustmentsCents" | "reservedFundsCents" | "feesCents" | "retriedCents" | "totalCents") =>
    payouts.reduce((s, p) => s + (p[k] ?? 0), 0);
  const soon = Date.now() + 3 * 86_400_000;
  const open = disputes.filter((d) => !["won", "lost", "accepted", "charge_refunded"].includes(d.status.toLowerCase()));

  return (
    <div className="mx-auto max-w-7xl">
      <PageHeader title="Payouts en disputes" subtitle="Controle per payout: charges + refunds + adjustments + reserve min fees + retried moet gelijk zijn aan het totaal." />

      <Card title="Shopify payouts" className="mb-6" action={<ImportPayouts />}>
        <div className="overflow-x-auto">
          <table className="data">
            <thead>
              <tr>
                <th>Datum</th>
                <th className="r">Charges</th>
                <th className="r">Refunds</th>
                <th className="r">Adjustments</th>
                <th className="r">Reserve</th>
                <th className="r">Fees</th>
                <th className="r">Retried</th>
                <th className="r">Uitbetaald</th>
                <th className="r">Controle</th>
              </tr>
            </thead>
            <tbody>
              {withDiff.map(({ p, diff }) => (
                <tr key={p.id}>
                  <td className="whitespace-nowrap">
                    {p.summaryUntil ? <>t/m {day(p.summaryUntil)} <span className="text-xs text-warn">samengevat, startwaarde</span></> : day(p.payoutDate)}
                  </td>
                  <td className="r">{euro(p.chargesCents)}</td>
                  <td className="r">{euro(p.refundsCents)}</td>
                  <td className="r">{euro(p.adjustmentsCents)}</td>
                  <td className="r">{euro(p.reservedFundsCents)}</td>
                  <td className="r">{p.feesCents === null ? "ontbreekt" : euro(-p.feesCents)}</td>
                  <td className="r">{euro(p.retriedCents)}</td>
                  <td className="r font-medium">{euro(p.totalCents)}</td>
                  <td className={`r ${diff ? "font-medium text-neg" : "text-good"}`}>{diff === null ? "ontbreekt" : diff === 0 ? "klopt" : euro(diff)}</td>
                </tr>
              ))}
              {payouts.length === 0 && (
                <tr>
                  <td colSpan={9} className="py-8 text-center text-ink-3">
                    Nog geen payouts. Exporteer ze in Shopify via Finances, Payouts, Export, en importeer de CSV hier.
                  </td>
                </tr>
              )}
            </tbody>
            {payouts.length > 1 && (
              <tfoot>
                <tr>
                  <td>Totaal</td>
                  <td className="r">{euro(sum("chargesCents"))}</td>
                  <td className="r">{euro(sum("refundsCents"))}</td>
                  <td className="r">{euro(sum("adjustmentsCents"))}</td>
                  <td className="r">{euro(sum("reservedFundsCents"))}</td>
                  <td className="r">{euro(-sum("feesCents"))}</td>
                  <td className="r">{euro(sum("retriedCents"))}</td>
                  <td className="r">{euro(sum("totalCents"))}</td>
                  <td />
                </tr>
              </tfoot>
            )}
          </table>
        </div>
        {sum("chargesCents") > 0 && (
          <p className="mt-3 text-xs text-ink-3">
            Reserve {pct(-sum("reservedFundsCents") / sum("chargesCents"))} van charges, fees {pct(sum("feesCents") / sum("chargesCents"))}. Afwijkingen worden getoond,
            niet verborgen: vaak zijn het niet gespecificeerde dispute fees van € 15.
          </p>
        )}
      </Card>

      <Card title="Disputes" className="mb-6">
        {open.length === 0 ? (
          <p className="text-sm text-ink-3">
            Geen open disputes bekend. Disputes komen binnen zodra Shopify Payments gekoppeld is (scope read_shopify_payments_disputes).
          </p>
        ) : (
          <table className="data">
            <thead>
              <tr>
                <th>Deadline</th>
                <th>Order</th>
                <th>Land</th>
                <th>Reden</th>
                <th>Status</th>
                <th className="r">Bedrag</th>
              </tr>
            </thead>
            <tbody>
              {open.map((d) => {
                const urgent = d.dueBy && d.dueBy.getTime() < soon;
                return (
                  <tr key={d.id} className={urgent ? "bg-surface-2" : ""}>
                    <td className={urgent ? "font-medium text-neg" : ""}>{d.dueBy ? day(d.dueBy) : "ontbreekt"}{urgent && ", binnen 3 dagen"}</td>
                    <td>{d.orderName ?? "ontbreekt"}</td>
                    <td>{d.country ?? ""}</td>
                    <td>{d.reason ?? ""}</td>
                    <td>{d.status}</td>
                    <td className="r">{euro(d.amountCents)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </Card>

      <Card title="PayPal">
        <div className="grid gap-4 text-sm sm:grid-cols-3">
          <div>
            <div className="text-ink-2">Opnames naar bank (alle geïmporteerde maanden)</div>
            <div className="num text-lg font-semibold">{euro(paypalIn._sum.amountCents ?? 0)}</div>
            <div className="text-xs text-ink-3">{paypalIn._count} opnames, uit bank</div>
          </div>
          <div>
            <div className="text-ink-2">Saldo</div>
            <div className="num text-lg font-semibold">{euro(money.position.paypalCents)}</div>
            {money.snapshot?.source === "paypal" ? (
              <div className="text-xs text-ink-3">uit PayPal{money.snapshot.note ? `, ${money.snapshot.note.split(";")[0].replace("PayPal-saldo uit PayPal ", "")}` : ""}</div>
            ) : (
              <div className="text-xs text-warn">handmatig</div>
            )}
          </div>
          <div>
            <div className="text-ink-2">Fees</div>
            {pp._count > 0 ? (
              <>
                <div className="num text-lg font-semibold">{euro(pp._sum.feesCents ?? 0)}</div>
                <div className="text-xs text-ink-3">
                  laatste 30 dagen, uit PayPal: {pp._sum.salesCount ?? 0} verkopen voor {euro(pp._sum.salesCents ?? 0, true)}, fees{" "}
                  {(pp._sum.salesCents ?? 0) > 0 ? `${(((pp._sum.feesCents ?? 0) / (pp._sum.salesCents ?? 1)) * 100).toFixed(1).replace(".", ",")}%` : ""}
                </div>
              </>
            ) : paypalFees.length ? (
              paypalFees.map((f) => (
                <div key={f.id} className="num">
                  {euro(f.amountCents)} <span className="text-xs text-warn">{f.label}, handmatig</span>
                </div>
              ))
            ) : (
              <div className="text-neg">ontbreekt</div>
            )}
          </div>
        </div>
        <p className="mt-3 text-xs text-ink-3">
          Gekoppeld via de PayPal API (PAYPAL_CLIENT_ID en PAYPAL_SECRET). Nieuwe transacties verschijnen met ongeveer 3 uur vertraging. Zonder koppeling gelden de
          handmatige fees en het handmatige saldo.
        </p>
      </Card>
    </div>
  );
}
