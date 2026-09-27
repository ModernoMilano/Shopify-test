"use client";

import { useActionState } from "react";
import { importCosts, type ImportResult } from "./actions";

export function ImportForm() {
  const [state, action, pending] = useActionState<ImportResult | null, FormData>(importCosts, null);
  return (
    <form action={action} className="space-y-3">
      <input type="file" name="file" accept=".csv,text/csv" className="block text-sm" />
      <button className="btn" disabled={pending}>
        {pending ? "Importeren…" : "Importeer kostprijzen"}
      </button>
      {state && (
        <div className="text-sm">
          <p>
            {state.updated} bijgewerkt, {state.unchanged} ongewijzigd.
          </p>
          {state.errors.length > 0 && (
            <ul className="mt-1 list-disc pl-5 text-neg">
              {state.errors.slice(0, 20).map((e) => (
                <li key={e}>{e}</li>
              ))}
            </ul>
          )}
        </div>
      )}
    </form>
  );
}
