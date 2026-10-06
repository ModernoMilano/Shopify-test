// De garderobe: alle actieve Shopify-producten, ingedeeld naar wat ze op het lichaam bedekken.
// Alleen wat hier staat mag in een beeld. Wat ModernoMilano niet verkoopt bestaat voor de engine niet.

import { colourFamily, colourWordInTitle, type ColourFamily } from "./colours";

/** Lichaamszone: top = basislaag, mid = tussenlaag (cardigan, gebreide gilet), outer = buitenlaag. */
export type Slot = "top" | "mid" | "outer" | "bottom" | "shoes";

export type Kind =
  | "tee" | "longsleeve" | "polo" | "knit-polo" | "shirt" | "zip-knit" | "cardigan" | "knit-gilet"
  | "lounge-top" | "gilet" | "jacket" | "blazer" | "trousers" | "joggers" | "shorts" | "loafers";

export type Season = "fw" | "ss" | "all";

export interface Piece {
  slot: Slot;
  kind: Kind;
  label: string;
}

export interface ProductImages {
  /** Beste referentie voor het product zelf (packshot of eerste foto). */
  primary: string;
  model?: string;
  detail?: string;
  back?: string;
  all: string[];
}

export interface WardrobeItem {
  id: string;
  handle: string;
  title: string;
  /** Productlijn zonder kleur, bv. "MILANO CASHMERE CORTINA POLO". */
  line: string;
  colour: string | null;
  family: ColourFamily | null;
  /** Losse items hebben één stuk, sets meerdere. */
  pieces: Piece[];
  isSet: boolean;
  /** Mag het stuk ook als een andere laag gedragen worden (bv. cardigan zonder iets eronder). */
  alsoAs: Slot[];
  season: Season;
  material: string | null;
  priceEur: number;
  url: string | null;
  collections: string[];
  images: ProductImages;
}

/** Vorm van een product zoals de Shopify Admin GraphQL-query in creative-engine/README.md het teruggeeft. */
export interface ShopifyProductNode {
  id: string;
  title: string;
  handle: string;
  description?: string | null;
  onlineStoreUrl?: string | null;
  category?: { fullName: string } | null;
  options?: { name: string; values: string[] }[];
  priceRangeV2?: { minVariantPrice: { amount: string } };
  collections?: { nodes: { title: string }[] };
  media?: { nodes: { mediaContentType?: string; image?: { url: string } | null }[] };
}

interface LineRule {
  match: RegExp;
  pieces: Piece[];
  alsoAs?: Slot[];
  season?: Season;
}

const p = (slot: Slot, kind: Kind, label: string): Piece => ({ slot, kind, label });

/**
 * Losse productlijnen. Shopify-categorieën zijn niet consequent ingevuld (dezelfde polo staat als
 * Polos én Sweaters), daarom beslist de titel. Volgorde telt: de eerste match wint.
 */
const LINE_RULES: LineRule[] = [
  { match: /LOAFER/, pieces: [p("shoes", "loafers", "suede loafers")] },
  { match: /TORINO BLAZER/, pieces: [p("outer", "blazer", "double-breasted cashmere knit blazer")], season: "fw" },
  { match: /REVERSIBLE JACKET/, pieces: [p("outer", "jacket", "reversible jacket")], season: "fw" },
  { match: /HOODED JACKET/, pieces: [p("outer", "jacket", "hooded jacket")], season: "fw" },
  { match: /CLASSIC JACKET/, pieces: [p("outer", "jacket", "classic jacket")], season: "fw" },
  { match: /JACKET/, pieces: [p("outer", "jacket", "jacket")], season: "fw" },
  { match: /PIENO GILET/, pieces: [p("mid", "knit-gilet", "full-zip cashmere sweater vest")], season: "fw" },
  { match: /GILET|BODYWARMER|MILANO VEST/, pieces: [p("outer", "gilet", "padded gilet")] },
  { match: /KNITTED VEST/, pieces: [p("mid", "zip-knit", "zip turtleneck knit")], alsoAs: ["top"], season: "fw" },
  { match: /BELLAGIO/, pieces: [p("mid", "zip-knit", "full-zip cashmere knit with stand collar")], alsoAs: ["top"], season: "fw" },
  { match: /CARDIGAN/, pieces: [p("mid", "cardigan", "cashmere cardigan")], alsoAs: ["top"], season: "fw" },
  { match: /VELA/, pieces: [p("mid", "cardigan", "V-neck cashmere cardigan")], alsoAs: ["top"], season: "fw" },
  { match: /LIDO|CORTINA POLO|BERGAMO POLO|SORRENTO POLO/, pieces: [p("top", "knit-polo", "long-sleeve cashmere knit polo")], season: "fw" },
  { match: /CAMICIA/, pieces: [p("top", "shirt", "cashmere shirt")], alsoAs: ["mid"], season: "fw" },
  { match: /LONG SLEEVE POLO/, pieces: [p("top", "polo", "long-sleeve polo")] },
  { match: /LONG SLEEVE/, pieces: [p("top", "longsleeve", "long-sleeve top")] },
  { match: /RIVIERA POLO|PORTOFINO POLO/, pieces: [p("top", "polo", "short-sleeve polo")], season: "ss" },
  { match: /POLO/, pieces: [p("top", "polo", "polo")] },
  { match: /TEE|T-SHIRT/, pieces: [p("top", "tee", "mercerised Supima tee")] },
  { match: /JOGGER/, pieces: [p("bottom", "joggers", "cashmere joggers")], season: "fw" },
  { match: /COMO PANT/, pieces: [p("bottom", "trousers", "cashmere trousers")], season: "fw" },
  { match: /LINO PANT/, pieces: [p("bottom", "trousers", "linen trousers")], season: "ss" },
  { match: /SHORT/, pieces: [p("bottom", "shorts", "shorts")], season: "ss" },
  { match: /PANT|TROUSER/, pieces: [p("bottom", "trousers", "tailored trousers")] },
];

/** Optienaam in een bundel (bv. "LOAFER", "SUPIMA TEE", "REVERSO GILET") → stuk(ken). */
function piecesFromOptionName(name: string): Piece[] {
  const n = name.toUpperCase();
  if (n === "SIZE" || n === "MAAT") return [];
  if (/TRACKSUIT|CASHMERE SET/.test(n)) return [p("mid", "lounge-top", "zip lounge top"), p("bottom", "joggers", "matching lounge pants")];
  if (n === "TOP") return [p("top", "lounge-top", "knitted top")];
  if (n === "BOTTOM") return [p("bottom", "joggers", "matching drawstring pants")];
  if (n === "SHIRT" || n === "SUPIMA TEE") return [p("top", "tee", "tee")];
  const single = LINE_RULES.find((r) => r.match.test(n));
  return single ? single.pieces : [];
}

/** Sets met alleen een maatoptie: de stukken staan in de omschrijving. */
function piecesFromDescription(description: string): Piece[] {
  const d = description.toLowerCase();
  if (/shirt and shorts/.test(d)) return [p("top", "shirt", "short-sleeve shirt"), p("bottom", "shorts", "matching shorts")];
  if (/tee with a matching pair of shorts/.test(d)) return [p("top", "tee", "tee"), p("bottom", "shorts", "matching shorts")];
  if (/shirt and trousers/.test(d)) return [p("top", "shirt", "long-sleeve shirt"), p("bottom", "trousers", "matching trousers")];
  if (/hooded zip-up jacket/.test(d)) return [p("top", "lounge-top", "hooded zip-up knit jacket"), p("bottom", "joggers", "matching relaxed pants")];
  if (/zip-up (top|jacket)/.test(d)) return [p("top", "lounge-top", "collared zip-up top"), p("bottom", "joggers", "matching pants")];
  if (/fold-over collar top/.test(d)) return [p("top", "lounge-top", "fold-over collar top"), p("bottom", "joggers", "matching pants")];
  if (/knitted (top|jacket)/.test(d)) return [p("top", "lounge-top", "knitted top"), p("bottom", "joggers", "matching drawstring pants")];
  return [p("top", "lounge-top", "matching top"), p("bottom", "joggers", "matching pants")];
}

function setSeason(pieces: Piece[], title: string, description: string): Season {
  if (pieces.some((x) => x.kind === "shorts") || /LINEN|RIVIERA|CASA|AMALFI/.test(title)) return "ss";
  if (/cashmere/i.test(description) || pieces.some((x) => ["jacket", "blazer", "knit-gilet", "zip-knit", "cardigan"].includes(x.kind))) return "fw";
  return "all";
}

function material(text: string): string | null {
  const t = text.toLowerCase();
  if (t.includes("cashmere")) return "cashmere";
  if (t.includes("suede")) return "suede";
  if (t.includes("supima")) return "mercerised Supima cotton";
  if (t.includes("seersucker")) return "seersucker";
  if (/\blinn?en\b|\blino\b/.test(t)) return "linen";
  if (t.includes("cotton")) return "cotton";
  if (t.includes("polyamide") || t.includes("spandex")) return "technical stretch knit";
  return null;
}

/** Kiest de beste referentiefoto's op basis van de bestandsnamen die in de winkel gebruikt worden. */
export function pickImages(urls: string[]): ProductImages {
  const name = (u: string) => u.split("/").pop()!.split("?")[0].toLowerCase();
  const find = (re: RegExp) => urls.find((u) => re.test(name(u)));
  const packshot = find(/(^|_)1_product|_product[._]|packshot/);
  return {
    primary: packshot ?? urls[0],
    model: find(/_model[._]/),
    detail: find(/_detail[._]/),
    back: find(/_back[._]/),
    all: urls,
  };
}

/** Bundels zonder kleur in de titel noemen hun palet in de tekst, bv. "in a sharp, monochrome black palette". */
function paletteFromDescription(description: string): ColourFamily | null {
  const m = description.match(/\bin an? ([\w ,-]+?) palette/i);
  if (!m) return null;
  const word = m[1].toUpperCase().split(/[ ,-]+/).reverse().find((w) => colourFamily(w));
  return colourFamily(word);
}

export function splitTitle(title: string): { line: string; colour: string | null } {
  const m = title.match(/^(.*?)\s+-\s+([^-]+)$/);
  if (m) return { line: m[1].trim(), colour: m[2].trim() };
  return { line: title.trim(), colour: colourWordInTitle(title) };
}

export function toWardrobeItem(node: ShopifyProductNode): WardrobeItem | null {
  const title = node.title.toUpperCase();
  const description = node.description ?? "";
  const images = (node.media?.nodes ?? []).map((m) => m.image?.url).filter((u): u is string => Boolean(u));
  if (images.length === 0) return null;

  const { line, colour } = splitTitle(title);
  const isSet = /\bSET\b/.test(line);
  let pieces: Piece[];
  let alsoAs: Slot[] = [];
  let season: Season;

  if (isSet) {
    const options = (node.options ?? []).flatMap((o) => o.name.split("/"));
    pieces = options.flatMap(piecesFromOptionName);
    if (!pieces.some((x) => x.slot === "top") || !pieces.some((x) => x.slot === "bottom")) {
      for (const x of piecesFromDescription(description)) if (!pieces.some((y) => y.slot === x.slot)) pieces.push(x);
    }
    season = setSeason(pieces, title, description);
  } else {
    const rule = LINE_RULES.find((r) => r.match.test(line));
    if (!rule) return null;
    pieces = rule.pieces.map((x) => ({ ...x }));
    alsoAs = rule.alsoAs ?? [];
    season = rule.season ?? (/LINEN|LINNEN|LINO|RIVIERA|AMALFI/.test(line) ? "ss" : "all");
  }

  return {
    id: node.id.split("/").pop()!,
    handle: node.handle,
    title: node.title,
    line,
    colour,
    family: colourFamily(colour) ?? paletteFromDescription(description),
    pieces,
    isSet,
    alsoAs,
    season,
    material: material(`${line} ${description}`),
    priceEur: Number(node.priceRangeV2?.minVariantPrice.amount ?? 0),
    url: node.onlineStoreUrl ?? null,
    collections: (node.collections?.nodes ?? []).map((c) => c.title),
    images: pickImages(images),
  };
}

export function buildWardrobe(nodes: ShopifyProductNode[]): { items: WardrobeItem[]; skipped: string[] } {
  const items: WardrobeItem[] = [];
  const skipped: string[] = [];
  for (const n of nodes) {
    const item = toWardrobeItem(n);
    if (item) items.push(item);
    else skipped.push(n.title);
  }
  items.sort((a, b) => a.title.localeCompare(b.title));
  return { items, skipped };
}

/** Welke zones een item kan vullen (eigen stukken plus alsoAs). */
export function slotsOf(item: WardrobeItem): Slot[] {
  return [...new Set([...item.pieces.map((x) => x.slot), ...item.alsoAs])];
}

export function isInSeason(item: WardrobeItem, season: Exclude<Season, "all">): boolean {
  return item.season === "all" || item.season === season;
}

/** Herfst/winter van september tot en met maart, anders lente/zomer. */
export function seasonFor(date: Date): Exclude<Season, "all"> {
  const m = date.getMonth() + 1;
  return m >= 9 || m <= 3 ? "fw" : "ss";
}
