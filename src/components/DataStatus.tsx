import Link from "next/link";
import { db } from "@/lib/db";
import { bankCoverage } from "@/finance/coverage";
import { UploadForm } from "@/app/bank/UploadForm";
import { day } from "./ui";

const SOURCES = [
  { id: "shopify_sales", label: "Shopify" },
  { id: "shopify_payments", label: "Payouts" },
  { id: "windsor", label: "Meta" },
  { id: "paypal", label: "PayPal" },
];

function ago(d: Date) {
  const min = Math.round((Date.now() - d.getTime()) / 60_000);
  if (min < 60) return `${Math.max(1, min)} min geleden`;
  const h = Math.round(min / 60);
  if (h < 48) return `${h} uur geleden`;
  return `${Math.round(h / 24)} dagen geleden`;
}

/**
 * Strook bovenaan het overzicht: hoe actueel is elke bron, en welk bankafschrift is nog nodig.
 * Alles behalve de bank komt automatisch binnen; de bank is de enige handmatige stap.
 */
export async function DataStatus() {
  const [coverage, syncs, unknown] = await Promise.all([
    bankCoverage(),
    db.sourceSync.findMany(),
    db.bankTransaction.count({ where: { category: "unknown" } }),
  ]);
  const byId = new Map(syncs.map((s) => [s.source, s]));
  const bankNeeded = !coverage.lastDate || coverage.missingFrom !== null;

  return (
    <section className="card mb-6 p-4">
      <div className="flex flex-wrap items-center gap-x-5 gap-y-2 text-sm">
        <span className="font-medium">Data</span>
        {SOURCES.map((s) => {
          const x = byId.get(s.id);
          const stale = x && Date.now() - x.lastAt.getTime() > 26 * 3_600_000;
          const state = !x ? "niet gekoppeld" : x.status !== "ok" ? "fout" : ago(x.lastAt);
          const tone = !x ? "text-ink-3" : x.status !== "ok" || stale ? "text-neg" : "text-good";
          return (
            <Link key={s.id} href="/settings" className="flex items-center gap-1.5 hover:underline" title={x?.message ?? ""}>
              <span aria-hidden className={tone}>
                ●
              </span>
              {s.label}
              <span className="text-ink-3">{state}</span>
            </Link>
          );
        })}
        <span className="flex items-center gap-1.5">
          <span aria-hidden className={bankNeeded ? "text-warn" : "text-good"}>
            ●
          </span>
          Bank
          <span className="text-ink-3">{coverage.lastDate ? `t/m ${day(coverage.lastDate)}` : "nog geen afschrift"}</span>
        </span>
        {unknown > 0 && (
          <Link href="/bank?cat=unknown" className="text-warn underline">
            {unknown} bankmutaties toewijzen
          </Link>
        )}
      </div>

      {bankNeeded && (
        <details className="mt-3 border-t border-line pt-3" open={!coverage.lastDate || coverage.missingDays >= 7}>
          <summary className="cursor-pointer text-sm">
            <span className="font-medium">Bankafschrift nodig</span>{" "}
            <span className="text-ink-2">
              {coverage.missingFrom
                ? `vanaf ${day(coverage.missingFrom)} (${coverage.missingDays} ${coverage.missingDays === 1 ? "dag" : "dagen"}). Download in de Revolut-app een afschrift van ${day(coverage.missingFrom)} tot vandaag.`
                : "Upload je eerste Revolut-afschrift."}
            </span>
          </summary>
          <div className="mt-3">
            <UploadForm compact />
          </div>
        </details>
      )}
      {coverage.gaps.length > 0 && (
        <p className="mt-2 text-xs text-warn">
          Gat in de bankdata: {coverage.gaps.map((g) => `${day(g.from)} t/m ${day(g.to)}`).join(", ")}. Upload een afschrift van die periode.
        </p>
      )}
    </section>
  );
}
