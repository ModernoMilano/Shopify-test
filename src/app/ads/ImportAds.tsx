"use client";

import { useActionState } from "react";
import { importAdSpend, type AdImportResult } from "./actions";
import { CHANNELS } from "./channels";

export function ImportAds() {
  const [state, action, pending] = useActionState<AdImportResult | null, FormData>(importAdSpend, null);
  return (
    <form action={action} className="flex flex-wrap items-center gap-2">
      <input type="file" name="file" accept=".csv,text/csv" className="text-sm" />
      <select name="channel" className="input" aria-label="Standaard kanaal">
        {CHANNELS.map((c) => (
          <option key={c.id} value={c.id}>
            {c.label}
          </option>
        ))}
      </select>
      <button className="btn btn-ghost" disabled={pending}>
        {pending ? "Importeren…" : "Importeer CSV"}
      </button>
      {state && (
        <span className="text-sm">
          {state.imported} dagen geïmporteerd
          {state.errors.length > 0 && <span className="text-neg"> · {state.errors.slice(0, 3).join("; ")}</span>}
        </span>
      )}
    </form>
  );
}
