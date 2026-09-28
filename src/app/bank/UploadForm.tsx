"use client";

import Link from "next/link";
import { useActionState } from "react";
import { uploadStatement, type ImportState } from "./actions";

const eur = new Intl.NumberFormat("nl-NL", { style: "currency", currency: "EUR" });
const fmtDay = new Intl.DateTimeFormat("nl-NL", { weekday: "short", day: "numeric", month: "short", timeZone: "UTC" });
const d = (k: string) => fmtDay.format(new Date(`${k}T00:00:00Z`)).replace(/\./g, "");

export function UploadForm({ compact = false }: { compact?: boolean }) {
  const [state, action, pending] = useActionState<ImportState, FormData>(uploadStatement, null);
  return (
    <form action={action} className="space-y-3">
      <div className="flex flex-wrap items-center gap-2">
        <input type="file" name="file" multiple accept=".pdf,.csv,application/pdf,text/csv" className="max-w-full text-sm" />
        <button className="btn" disabled={pending}>
          {pending ? "Bezig met inlezen…" : "Afschrift uploaden"}
        </button>
      </div>
      {!compact && (
        <p className="text-xs text-ink-3">
          Revolut PDF (afschrift uit de app) of CSV-export, van elke periode. Overlap is geen probleem: dubbele mutaties worden overgeslagen.
        </p>
      )}
      {state?.error && <p className="text-sm text-neg">{state.error}</p>}
      {state?.results.map((r) => (
        <div key={r.fileName} className={`rounded-lg border p-3 text-sm ${r.reconciled ? "border-line" : "border-neg"}`}>
          <div className="font-medium">
            {r.fileName}
            {r.periodFrom && r.periodTo && (
              <span className="font-normal text-ink-2">
                , {d(r.periodFrom)} t/m {d(r.periodTo)}
              </span>
            )}
          </div>
          <div className="text-ink-2">
            {r.imported} nieuw, {r.duplicates} al aanwezig.{" "}
            {r.opening !== null && r.closing !== null && (
              <>
                Saldo {eur.format(r.opening / 100)} naar {eur.format(r.closing / 100)}.{" "}
              </>
            )}
            {r.reconciled ? <span className="text-good">Sluit tot op de cent.</span> : <span className="text-neg">{r.message}</span>}
          </div>
          {r.unknown > 0 && (
            <Link href="/bank?cat=unknown" className="mt-1 inline-block text-warn underline">
              {r.unknown} mutaties herkende ik niet. Wijs ze één keer toe, daarna gaat het automatisch.
            </Link>
          )}
        </div>
      ))}
    </form>
  );
}
