/** Advertenties uit Windsor.ai in de database zetten. */
import { db } from "@/lib/db";
import type { AdRecord } from "./types";
import { fetchAds } from "./windsor-ads";

export async function saveAds(ads: AdRecord[]): Promise<{ ads: number; months: number }> {
  let months = 0;
  for (const a of ads) {
    const { months: rows, ...meta } = a;
    const data = { ...meta, createdAt: meta.createdAt ? new Date(meta.createdAt) : null, syncedAt: new Date() };
    await db.metaAd.upsert({ where: { id: a.id }, create: data, update: data });
    for (const m of rows) {
      const { month, ...vals } = m;
      await db.metaAdMonth.upsert({ where: { adId_month: { adId: a.id, month } }, create: { adId: a.id, month, ...vals }, update: vals });
      months += 1;
    }
  }
  return { ads: ads.length, months };
}

/** Standaard: de lopende en de vorige maand verversen (ouder verandert niet meer). */
export async function syncCreatives(fromMonth?: string, toMonth?: string): Promise<{ ads: number; months: number }> {
  const now = new Date();
  const to = toMonth ?? now.toISOString().slice(0, 7);
  const prev = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() - 1, 1)).toISOString().slice(0, 7);
  const ads = await fetchAds(fromMonth ?? prev, to);
  return saveAds(ads);
}

export async function loadAds(): Promise<AdRecord[]> {
  const rows = await db.metaAd.findMany({ include: { months: { orderBy: { month: "asc" } } } });
  return rows.map((r) => ({
    id: r.id,
    name: r.name,
    adsetName: r.adsetName,
    campaign: r.campaign,
    market: r.market,
    creativeId: r.creativeId,
    status: r.status,
    createdAt: r.createdAt ? r.createdAt.toISOString() : null,
    objectType: r.objectType,
    format: r.format as AdRecord["format"],
    angle: r.angle as AdRecord["angle"],
    conceptKey: r.conceptKey,
    cta: r.cta,
    title: r.title,
    body: r.body,
    linkUrl: r.linkUrl,
    thumbnailUrl: r.thumbnailUrl,
    imageUrl: r.imageUrl,
    instagramUrl: r.instagramUrl,
    previewUrl: r.previewUrl,
    months: r.months.map((m) => ({
      month: m.month,
      spendCents: m.spendCents,
      impressions: m.impressions,
      reach: m.reach,
      clicks: m.clicks,
      linkClicks: m.linkClicks,
      landingPageViews: m.landingPageViews,
      addToCart: m.addToCart,
      checkouts: m.checkouts,
      purchases: m.purchases,
      purchaseValueCents: m.purchaseValueCents,
      frequency: m.frequency,
      videoPlays: m.videoPlays,
      video2s: m.video2s,
      thruplays: m.thruplays,
      videoP25: m.videoP25,
      videoP50: m.videoP50,
      videoP75: m.videoP75,
      videoP100: m.videoP100,
      avgWatchSec: m.avgWatchSec,
    })),
  }));
}
