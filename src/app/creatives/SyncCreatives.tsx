"use client";

import { useState, useTransition } from "react";
import { syncAllCreatives } from "./actions";

export function SyncCreatives() {
  const [pending, start] = useTransition();
  const [msg, setMsg] = useState<{ ok: boolean; message: string } | null>(null);
  return (
    <div className="flex items-center gap-2">
      {msg && <span className={`text-sm ${msg.ok ? "text-good" : "text-neg"}`}>{msg.message}</span>}
      <button className="btn btn-ghost" disabled={pending} onClick={() => start(async () => setMsg(await syncAllCreatives()))}>
        {pending ? "Alle maanden ophalen…" : "Alles ophalen uit Windsor.ai"}
      </button>
    </div>
  );
}
