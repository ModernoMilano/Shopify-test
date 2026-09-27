import { syncAllSources } from "@/finance/sync-all";

export const dynamic = "force-dynamic";
export const maxDuration = 300;

/** Aangeroepen door een cron (bv. Vercel Cron) met Authorization: Bearer CRON_SECRET. */
export async function GET(req: Request) {
  const secret = process.env.CRON_SECRET;
  if (!secret || req.headers.get("authorization") !== `Bearer ${secret}`) {
    return new Response("Unauthorized", { status: 401 });
  }
  const results = await syncAllSources();
  return Response.json({ ok: results.every((r) => r.ok || r.message.startsWith("Niet gekoppeld") || r.source === "paypal"), results });
}
