import { syncAllSources } from "@/finance/sync-all";

export const dynamic = "force-dynamic";
export const maxDuration = 300;

/**
 * Aangeroepen door Vercel Cron (dagelijks) en de GitHub Action (elk uur)
 * met Authorization: Bearer CRON_SECRET.
 */
export async function GET(req: Request) {
  const secret = process.env.CRON_SECRET;
  if (!secret || req.headers.get("authorization") !== `Bearer ${secret}`) {
    return new Response("Unauthorized", { status: 401 });
  }
  const results = await syncAllSources();
  // niet-gekoppelde bronnen zijn geen fout; een gekoppelde bron die faalt wel
  const failed = results.filter((r) => !r.ok && !r.message.startsWith("Niet gekoppeld"));
  return Response.json({ ok: failed.length === 0, results }, { status: failed.length ? 500 : 200 });
}
