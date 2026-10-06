// Concurrenten volgen: posts van publieke Instagram-accounts (via Windsor.ai "Instagram Public")
// samenvatten tot wat werkt: welke soort post, hoe vaak, wanneer, welke onderwerpen.

export const COMPETITORS = [
  { handle: "zegna", name: "Zegna" },
  { handle: "loropiana", name: "Loro Piana" },
  { handle: "boggimilanoofficial", name: "Boggi Milano" },
  { handle: "brunellocucinelli_brand", name: "Brunello Cucinelli" },
] as const;

export type MediaType = "image" | "carousel" | "video";

export interface CompetitorPost {
  account: string;
  postedAt: string;
  type: MediaType;
  caption: string;
  likes: number;
  comments: number;
  permalink: string | null;
  mediaUrl: string | null;
  followers: number | null;
}

type Row = Record<string, unknown>;

function first(row: Row, keys: string[]): unknown {
  for (const k of keys) if (row[k] !== undefined && row[k] !== null && row[k] !== "") return row[k];
  return undefined;
}

function mediaType(v: unknown): MediaType {
  const t = String(v ?? "").toUpperCase();
  if (t.includes("CAROUSEL") || t.includes("ALBUM")) return "carousel";
  if (t.includes("VIDEO") || t.includes("REEL")) return "video";
  return "image";
}

/**
 * Zet een rij uit Windsor om. De veldnamen verschillen per connectorversie; daarom proberen we de gangbare namen.
 * Controleer na het koppelen met get_fields welke namen de connector echt gebruikt en vul ze hier aan.
 */
export function fromWindsorRow(row: Row): CompetitorPost | null {
  const account = first(row, ["username", "account_username", "profile_username", "account_name", "account"]);
  const postedAt = first(row, ["media_timestamp", "timestamp", "post_date", "date", "created_time"]);
  if (!account || !postedAt) return null;
  return {
    account: String(account).replace(/^@/, "").toLowerCase(),
    postedAt: String(postedAt),
    type: mediaType(first(row, ["media_type", "media_product_type", "type"])),
    caption: String(first(row, ["media_caption", "caption", "text"]) ?? ""),
    likes: Number(first(row, ["media_like_count", "like_count", "likes"]) ?? 0),
    comments: Number(first(row, ["media_comments_count", "comments_count", "comments"]) ?? 0),
    permalink: (first(row, ["media_permalink", "permalink", "url"]) as string) ?? null,
    mediaUrl: (first(row, ["media_url", "thumbnail_url", "image_url"]) as string) ?? null,
    followers: Number(first(row, ["followers_count", "followers"]) ?? NaN) || null,
  };
}

export interface AccountSummary {
  account: string;
  posts: number;
  postsPerWeek: number;
  mix: Record<MediaType, number>;
  avgEngagement: number;
  /** Interacties per post als % van volgers, als volgers bekend zijn. */
  engagementRate: number | null;
  bestType: MediaType | null;
  bestWeekdays: string[];
  topHashtags: string[];
  topPosts: CompetitorPost[];
}

const WEEKDAYS = ["zo", "ma", "di", "wo", "do", "vr", "za"];

export function summarize(posts: CompetitorPost[]): AccountSummary[] {
  const byAccount = new Map<string, CompetitorPost[]>();
  for (const p of posts) byAccount.set(p.account, [...(byAccount.get(p.account) ?? []), p]);

  return [...byAccount.entries()].map(([account, list]) => {
    const eng = (p: CompetitorPost) => p.likes + p.comments;
    const times = list.map((p) => new Date(p.postedAt).getTime()).filter(Number.isFinite);
    const spanWeeks = times.length > 1 ? Math.max(1, (Math.max(...times) - Math.min(...times)) / (7 * 86_400_000)) : 1;

    const mix: Record<MediaType, number> = { image: 0, carousel: 0, video: 0 };
    const engByType: Record<MediaType, number[]> = { image: [], carousel: [], video: [] };
    for (const p of list) {
      mix[p.type]++;
      engByType[p.type].push(eng(p));
    }
    const avg = (xs: number[]) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : 0);
    const bestType = (Object.keys(engByType) as MediaType[])
      .filter((t) => engByType[t].length > 0)
      .sort((a, b) => avg(engByType[b]) - avg(engByType[a]))[0] ?? null;

    const dayEng = new Map<number, number[]>();
    for (const p of list) {
      const d = new Date(p.postedAt).getUTCDay();
      if (Number.isFinite(d)) dayEng.set(d, [...(dayEng.get(d) ?? []), eng(p)]);
    }
    const bestWeekdays = [...dayEng.entries()].sort((a, b) => avg(b[1]) - avg(a[1])).slice(0, 2).map(([d]) => WEEKDAYS[d]);

    const tags = new Map<string, number>();
    for (const p of list) for (const t of p.caption.match(/#[\p{L}\p{N}_]+/gu) ?? []) tags.set(t.toLowerCase(), (tags.get(t.toLowerCase()) ?? 0) + 1);

    const followers = list.find((p) => p.followers)?.followers ?? null;
    const avgEngagement = avg(list.map(eng));
    return {
      account,
      posts: list.length,
      postsPerWeek: Math.round((list.length / spanWeeks) * 10) / 10,
      mix,
      avgEngagement: Math.round(avgEngagement),
      engagementRate: followers ? Math.round((avgEngagement / followers) * 10_000) / 100 : null,
      bestType,
      bestWeekdays,
      topHashtags: [...tags.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8).map(([t]) => t),
      topPosts: [...list].sort((a, b) => eng(b) - eng(a)).slice(0, 5),
    };
  });
}
