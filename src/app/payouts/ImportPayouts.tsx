"use client";

import { useActionState } from "react";
import { importPayouts, type PayoutImportState } from "./actions";

export function ImportPayouts() {
  const [state, action, pending] = useActionState<PayoutImportState, FormData>(importPayouts, null);
  return (
    <form action={action} className="flex flex-wrap items-center gap-2">
      <input type="file" name="file" accept=".csv,text/csv" className="max-w-full text-sm" />
      <button className="btn btn-ghost" disabled={pending}>
        {pending ? "Importeren…" : "Importeer payouts-CSV"}
      </button>
      {state && <span className={`text-sm ${state.ok ? "text-good" : "text-neg"}`}>{state.message}</span>}
    </form>
  );
}
