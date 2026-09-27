"use client";

import { useState, useTransition } from "react";
import { syncWindsor } from "./actions";

export function SyncWindsor() {
  const [pending, start] = useTransition();
  const [msg, setMsg] = useState<{ ok: boolean; message: string } | null>(null);
  return (
    <div className="flex items-center gap-2">
      {msg && <span className={`text-sm ${msg.ok ? "text-good" : "text-neg"}`}>{msg.message}</span>}
      <button className="btn btn-ghost" disabled={pending} onClick={() => start(async () => setMsg(await syncWindsor()))}>
        {pending ? "Ophalen…" : "Ophalen uit Windsor.ai"}
      </button>
    </div>
  );
}
