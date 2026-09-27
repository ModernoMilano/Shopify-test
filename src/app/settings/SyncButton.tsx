"use client";

import { useActionState } from "react";
import { runSync, type SyncResult } from "./actions";

export function SyncButton({ disabled }: { disabled: boolean }) {
  const [state, action, pending] = useActionState<SyncResult | null, FormData>(runSync, null);
  return (
    <form action={action} className="flex flex-wrap items-center gap-2">
      <button className="btn" name="full" value="0" disabled={disabled || pending}>
        {pending ? "Bezig met synchroniseren…" : "Nu synchroniseren"}
      </button>
      <button className="btn btn-ghost" name="full" value="1" disabled={disabled || pending}>
        Volledige sync
      </button>
      {state && <span className={`text-sm ${state.ok ? "text-good" : "text-neg"}`}>{state.message}</span>}
    </form>
  );
}
