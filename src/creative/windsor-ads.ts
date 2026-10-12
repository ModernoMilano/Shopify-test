/**
 * Advertenties op ad-niveau ophalen bij Windsor.ai (Facebook-connector) en samenvoegen tot AdRecord[].
 *
 * Windsor levert ad-niveau alleen betrouwbaar per kalendermaand (langere periodes lopen in een time-out),
 * daarom halen we drie veldgroepen per maand op: cijfers, video en creative (copy en media).
 */
import { angleOf, conceptKey, formatOf, marketOfCampaign } from "./classify";
import type { AdMonthMetrics, AdRecord } from "./types";

export const METRIC_FIELDS = [
  "ad_id", "ad_name", "adset_name", "campaign", "spend", "impressions", "reach", "clicks", "link_clicks",
  "actions_landing_page_view", "actions_add_to_cart", "actions_initiate_checkout", "actions_purchase", "action_values_purchase", "frequency",
];
export const VIDEO_FIELDS = [
  "ad_id", "ad_name", "spend", "impressions", "video_play_actions_video_view", "video_thruplay_watched_actions_video_view",
  "video_p25_watched_actions_video_view", "video_p50_watched_actions_video_view", "video_p75_watched_actions_video_view",
  "video_p100_watched_actions_video_view", "video_avg_time_watched_actions_video_view", "video_continuous_2_sec_watched_actions_video_view",
];
export const CREATIVE_FIELDS = [
  "ad_id", "ad_name", "creative_id", "effective_status", "ad_created_time", "object_type", "call_to_action_type", "title", "body",
  "link_url", "thumbnail_url", "image_url", "instagram_permalink_url", "ad_preview_shareable_link", "spend",
];

export type RawRow = Record<string, unknown>;
export type RawMonth = { month: string; metrics: RawRow[]; video: RawRow[]; creative: RawRow[] };

/** Alle maanden van `from` t/m `to` (YYYY-MM). */
export function monthsBetween(from: string, to: string): string[] {
  const out: string[] = [];
  let [y, m] = from.split("-").map(Number);
  const [ty, tm] = to.split("-").map(Number);
  while (y < ty || (y === ty && m <= tm)) {
    out.push(`${y}-${String(m).padStart(2, "0")}`);
    m += 1;
    if (m > 12) { m = 1; y += 1; }
  }
  return out;
}

export function monthRange(month: string, today = new Date()): { from: string; to: string } {
  const [y, m] = month.split("-").map(Number);
  const last = new Date(Date.UTC(y, m, 0));
  const todayKey = today.toISOString().slice(0, 10);
  const to = last.toISOString().slice(0, 10);
  return { from: `${month}-01`, to: to > todayKey ? todayKey : to };
}

async function windsorGet(fields: string[], from: string, to: string): Promise<RawRow[]> {
  const key = process.env.WINDSOR_API_KEY;
  if (!key) throw new Error("WINDSOR_API_KEY is niet ingesteld");
  const url = new URL("https://connectors.windsor.ai/facebook");
  url.searchParams.set("api_key", key);
  url.searchParams.set("date_from", from);
  url.searchParams.set("date_to", to);
  url.searchParams.set("fields", fields.join(","));
  const res = await fetch(url, { cache: "no-store", signal: AbortSignal.timeout(120_000) });
  if (!res.ok) throw new Error(`Windsor.ai gaf fout ${res.status} voor ${fields[2]}… ${from}`);
  const json = (await res.json()) as { data?: RawRow[] };
  return json.data ?? [];
}

/** Haal de drie veldgroepen voor één maand op. */
export async function fetchRawMonth(month: string): Promise<RawMonth> {
  const { from, to } = monthRange(month);
  const [metrics, video, creative] = await Promise.all([windsorGet(METRIC_FIELDS, from, to), windsorGet(VIDEO_FIELDS, from, to), windsorGet(CREATIVE_FIELDS, from, to)]);
  return { month, metrics, video, creative };
}

const num = (v: unknown) => (v == null || v === "" ? 0 : Number(v) || 0);
const numOrNull = (v: unknown) => (v == null || v === "" ? null : Number(v));
const str = (v: unknown) => (v == null || v === "" ? null : String(v));
const cents = (v: unknown) => Math.round(num(v) * 100);

/** Voeg ruwe maandrijen samen tot één AdRecord per ad, met één maandregel per maand. */
export function mergeRaw(months: RawMonth[]): AdRecord[] {
  const ads = new Map<string, AdRecord>();
  const creativeByAd = new Map<string, RawRow>();
  for (const m of months) for (const r of m.creative) if (r.ad_id) creativeByAd.set(String(r.ad_id), r);

  for (const m of months) {
    const videoByAd = new Map<string, RawRow>();
    for (const r of m.video) if (r.ad_id) videoByAd.set(String(r.ad_id), r);

    for (const r of m.metrics) {
      const id = String(r.ad_id ?? "");
      if (!id) continue;
      const spendCents = cents(r.spend);
      const impressions = num(r.impressions);
      if (spendCents === 0 && impressions === 0) continue;
      const v = videoByAd.get(id);
      const c = creativeByAd.get(id);
      const name = String(r.ad_name ?? c?.ad_name ?? "onbekend");
      const campaign = String(r.campaign ?? "onbekend");
      let ad = ads.get(id);
      if (!ad) {
        const title = str(c?.title);
        const body = str(c?.body);
        ad = {
          id,
          name,
          adsetName: str(r.adset_name),
          campaign,
          market: marketOfCampaign(campaign),
          creativeId: str(c?.creative_id),
          status: str(c?.effective_status),
          createdAt: str(c?.ad_created_time),
          objectType: str(c?.object_type),
          format: formatOf({ name, objectType: str(c?.object_type), title, videoPlays: numOrNull(v?.video_play_actions_video_view) }),
          angle: angleOf({ name, title, body, adsetName: str(r.adset_name) }),
          conceptKey: conceptKey(name),
          cta: str(c?.call_to_action_type),
          title,
          body,
          linkUrl: str(c?.link_url),
          thumbnailUrl: str(c?.thumbnail_url),
          imageUrl: str(c?.image_url),
          instagramUrl: str(c?.instagram_permalink_url),
          previewUrl: str(c?.ad_preview_shareable_link),
          months: [],
        };
        ads.set(id, ad);
      } else if (ad.format === "onbekend" && num(v?.video_play_actions_video_view) > 0) {
        ad.format = "video";
      }
      const row: AdMonthMetrics = {
        month: m.month,
        spendCents,
        impressions,
        reach: num(r.reach),
        clicks: num(r.clicks),
        linkClicks: num(r.link_clicks),
        landingPageViews: num(r.actions_landing_page_view),
        addToCart: num(r.actions_add_to_cart),
        checkouts: num(r.actions_initiate_checkout),
        purchases: num(r.actions_purchase),
        purchaseValueCents: cents(r.action_values_purchase),
        frequency: numOrNull(r.frequency),
        videoPlays: numOrNull(v?.video_play_actions_video_view),
        video2s: numOrNull(v?.video_continuous_2_sec_watched_actions_video_view),
        thruplays: numOrNull(v?.video_thruplay_watched_actions_video_view),
        videoP25: numOrNull(v?.video_p25_watched_actions_video_view),
        videoP50: numOrNull(v?.video_p50_watched_actions_video_view),
        videoP75: numOrNull(v?.video_p75_watched_actions_video_view),
        videoP100: numOrNull(v?.video_p100_watched_actions_video_view),
        avgWatchSec: numOrNull(v?.video_avg_time_watched_actions_video_view),
      };
      const existing = ad.months.findIndex((x) => x.month === m.month);
      if (existing >= 0) ad.months[existing] = row;
      else ad.months.push(row);
    }
  }
  for (const ad of ads.values()) ad.months.sort((a, b) => a.month.localeCompare(b.month));
  return [...ads.values()];
}

/** Haal alle maanden op en voeg samen. */
export async function fetchAds(fromMonth: string, toMonth: string): Promise<AdRecord[]> {
  const raw: RawMonth[] = [];
  for (const month of monthsBetween(fromMonth, toMonth)) raw.push(await fetchRawMonth(month));
  return mergeRaw(raw);
}
