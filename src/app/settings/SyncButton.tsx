"use client";

import { useState, useTransition } from "react";
import { runSync } from "./actions";
import type { SourceResult } from "@/finance/sync-all";

export function SyncButton() {
  const [pending, start] = useTransition();
  const [results, setResults] = useState<SourceResult[] | null>(null);
  return (
    <div>
      <button className="btn" disabled={pending} onClick={() => start(async () => setResults(await runSync()))}>
        {pending ? "Bezig met ophalen…" : "Ophalen"}
      </button>
      {results && (
        <ul className="mt-3 space-y-1 text-sm">
          {results.map((r) => (
            <li key={r.source} className="flex gap-2">
              <span className={r.ok ? "text-good" : "text-neg"}>{r.ok ? "Gelukt" : "Fout"}</span>
              <span className="font-medium">{r.label}:</span>
              <span className="text-ink-2">{r.message}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
