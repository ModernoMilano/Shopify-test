"use server";

import { revalidatePath } from "next/cache";
import { db } from "@/lib/db";
import { syncCreatives } from "@/creative/sync";

/** Haalt alle maanden sinds de start van het account opnieuw op (duurt een paar minuten). */
export async function syncAllCreatives(): Promise<{ ok: boolean; message: string }> {
  try {
    const r = await syncCreatives("2026-04");
    const message = `${r.ads} advertenties, ${r.months} maandregels`;
    await db.sourceSync.upsert({
      where: { source: "windsor_ads" },
      create: { source: "windsor_ads", lastAt: new Date(), status: "ok", message },
      update: { lastAt: new Date(), status: "ok", message },
    });
    revalidatePath("/creatives");
    return { ok: true, message };
  } catch (e) {
    const message = e instanceof Error ? e.message : String(e);
    await db.sourceSync.upsert({
      where: { source: "windsor_ads" },
      create: { source: "windsor_ads", lastAt: new Date(), status: "fout", message },
      update: { status: "fout", message },
    });
    return { ok: false, message };
  }
}
