/** Gedeelde types van de creative engine. Alle bedragen in centen. */

export type AdMeta = {
  id: string;
  name: string;
  adsetName: string | null;
  campaign: string;
  market: string;
  creativeId: string | null;
  status: string | null;
  createdAt: string | null; // ISO
  objectType: string | null;
  format: AdFormat;
  angle: Angle;
  conceptKey: string;
  cta: string | null;
  title: string | null;
  body: string | null;
  linkUrl: string | null;
  thumbnailUrl: string | null;
  imageUrl: string | null;
  instagramUrl: string | null;
  previewUrl: string | null;
};

export type AdMonthMetrics = {
  month: string; // YYYY-MM
  spendCents: number;
  impressions: number;
  reach: number;
  clicks: number;
  linkClicks: number;
  landingPageViews: number;
  addToCart: number;
  checkouts: number;
  purchases: number;
  purchaseValueCents: number;
  frequency: number | null;
  videoPlays: number | null;
  video2s: number | null;
  thruplays: number | null;
  videoP25: number | null;
  videoP50: number | null;
  videoP75: number | null;
  videoP100: number | null;
  avgWatchSec: number | null;
};

export type AdRecord = AdMeta & { months: AdMonthMetrics[] };

export type AdFormat = "video" | "beeld" | "catalogus" | "onbekend";

export type Angle =
  | "bundel"
  | "cashmere"
  | "cashmere_sale"
  | "unboxing"
  | "ugc"
  | "tijdloos"
  | "lounge"
  | "reverso"
  | "catalogus"
  | "jacket"
  | "zomer"
  | "product"
  | "overig";

export const ANGLE_LABEL: Record<Angle, string> = {
  bundel: "Bundle & Save",
  cashmere: "Cashmere",
  cashmere_sale: "Cashmere sale (50%)",
  unboxing: "Unboxing / verpakking",
  ugc: "UGC",
  tijdloos: "Tijdloos / merk",
  lounge: "Lounge set",
  reverso: "Reverso set",
  catalogus: "Catalogus (dynamisch)",
  jacket: "Jacket studio",
  zomer: "Zomercollectie / summer sale",
  product: "Eén product (polo, tee, broek)",
  overig: "Overig",
};

export const FORMAT_LABEL: Record<AdFormat, string> = {
  video: "Video",
  beeld: "Beeld (statisch)",
  catalogus: "Catalogus",
  onbekend: "Onbekend",
};
