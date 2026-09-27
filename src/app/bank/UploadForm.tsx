"use client";

import { useActionState } from "react";
import { uploadStatement, type ImportState } from "./actions";

const eur = new Intl.NumberFormat("nl-NL", { style: "currency", currency: "EUR" });

export function UploadForm() {
  const [state, action, pending] = useActionState<ImportState, FormData>(uploadStatement, null);
  return (
    <form action={action} className="space-y-3">
      <div className="flex flex-wrap items-center gap-2">
        <input type="file" name="file" multiple accept=".pdf,.csv,application/pdf,text/csv" className="max-w-full text-sm" />
        <button className="btn" disabled={pending}>
          {pending ? "Bezig met inlezen…" : "Importeer afschrift"}
        </button>
      </div>
      <p className="text-xs text-ink-3">Revolut PDF (afschrift uit de app) of CSV-export. Dubbele mutaties worden automatisch overgeslagen.</p>
      {state?.error && <p className="text-sm text-neg">{state.error}</p>}
      {state?.results.map((r) => (
        <div key={r.fileName} className={`rounded-lg border p-3 text-sm ${r.reconciled ? "border-line" : "border-neg"}`}>
          <div className="font-medium">{r.fileName}</div>
          <div className="text-ink-2">
            {r.imported} nieuw, {r.duplicates} al aanwezig, {r.unknown} onbekend.{" "}
            {r.opening !== null && r.closing !== null && (
              <>
                Saldo {eur.format(r.opening / 100)} naar {eur.format(r.closing / 100)}.{" "}
              </>
            )}
            {r.reconciled ? <span className="text-good">Sluit tot op de cent.</span> : <span className="text-neg">{r.message}</span>}
          </div>
        </div>
      ))}
    </form>
  );
}
