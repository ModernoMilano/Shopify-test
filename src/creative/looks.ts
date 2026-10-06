// Looks: complete outfits die uitsluitend uit de garderobe komen.
// Regel nummer één: elke zichtbare laag is een ModernoMilano-product. Geen accessoires, want die verkopen we niet.

import { PALETTES, SHOE_PAIRING, paletteFits, type ColourFamily, type Palette } from "./colours";
import { isInSeason, slotsOf, type Kind, type Season, type Slot, type WardrobeItem } from "./wardrobe";

export interface LookItem {
  item: WardrobeItem;
  /** Welke zones dit item in deze look vult. */
  as: Slot[];
}

export interface Look {
  id: string;
  name: string;
  source: "house" | "composed";
  palette: Palette | null;
  items: LookItem[];
  hasShoes: boolean;
}

type SlotSpec = { slot: Slot; kinds: Kind[] | "set"; optional?: boolean };

interface Template {
  id: string;
  season: Season;
  slots: SlotSpec[];
}

const TOPS: Kind[] = ["tee", "longsleeve", "polo", "knit-polo", "shirt"];
const TROUSERS: Kind[] = ["trousers"];

/** Opbouwschema's, afgeleid van de huislooks (Terra, Tabacco, Nobile, Eleganza...) en de concurrentie. */
export const TEMPLATES: Template[] = [
  { id: "knit-trouser", season: "fw", slots: [{ slot: "top", kinds: ["knit-polo"] }, { slot: "bottom", kinds: TROUSERS }, { slot: "shoes", kinds: ["loafers"] }] },
  { id: "knit-alone", season: "fw", slots: [{ slot: "top", kinds: ["cardigan", "zip-knit"] }, { slot: "bottom", kinds: TROUSERS }, { slot: "shoes", kinds: ["loafers"] }] },
  { id: "layered-knit", season: "fw", slots: [{ slot: "top", kinds: ["tee", "longsleeve", "knit-polo"] }, { slot: "mid", kinds: ["cardigan", "zip-knit", "knit-gilet"] }, { slot: "bottom", kinds: [...TROUSERS, "joggers"] }, { slot: "shoes", kinds: ["loafers"] }] },
  { id: "blazer", season: "fw", slots: [{ slot: "top", kinds: ["knit-polo", "tee", "shirt"] }, { slot: "outer", kinds: ["blazer"] }, { slot: "bottom", kinds: TROUSERS }, { slot: "shoes", kinds: ["loafers"] }] },
  { id: "gilet", season: "all", slots: [{ slot: "top", kinds: ["knit-polo", "tee", "longsleeve", "polo"] }, { slot: "outer", kinds: ["gilet"] }, { slot: "bottom", kinds: [...TROUSERS, "joggers"] }, { slot: "shoes", kinds: ["loafers"] }] },
  { id: "jacket", season: "fw", slots: [{ slot: "top", kinds: ["knit-polo", "tee", "longsleeve"] }, { slot: "outer", kinds: ["jacket"] }, { slot: "bottom", kinds: TROUSERS }, { slot: "shoes", kinds: ["loafers"] }] },
  { id: "set", season: "all", slots: [{ slot: "top", kinds: "set" }, { slot: "shoes", kinds: ["loafers"] }] },
  { id: "summer", season: "ss", slots: [{ slot: "top", kinds: ["polo", "tee", "shirt"] }, { slot: "bottom", kinds: ["shorts", "trousers"] }, { slot: "shoes", kinds: ["loafers"] }] },
];

export const MAX_ITEMS = 5;

// ---------- controle ----------

export interface LookIssue {
  level: "error" | "warning";
  message: string;
}

/** Controleert een look (ook een look die met de hand of door Claude is samengesteld). */
export function validateLook(look: Look, wardrobe: WardrobeItem[], season?: Exclude<Season, "all">): LookIssue[] {
  const issues: LookIssue[] = [];
  const known = new Set(wardrobe.map((w) => w.id));
  for (const { item } of look.items) {
    if (!known.has(item.id)) issues.push({ level: "error", message: `${item.title} staat niet (meer) in de actieve garderobe` });
  }

  const count = (slot: Slot) => look.items.filter((x) => x.as.includes(slot)).length;
  if (count("top") !== 1) issues.push({ level: "error", message: `precies één bovenstuk nodig, nu ${count("top")}` });
  if (count("bottom") !== 1) issues.push({ level: "error", message: `precies één broek of short nodig, nu ${count("bottom")}` });
  for (const slot of ["mid", "outer", "shoes"] as Slot[]) {
    if (count(slot) > 1) issues.push({ level: "error", message: `meer dan één item als ${slot}` });
  }
  for (const { item, as } of look.items) {
    const can = slotsOf(item);
    for (const s of as) if (!can.includes(s)) issues.push({ level: "error", message: `${item.title} kan niet als ${s} gedragen worden` });
  }
  if (look.items.length > MAX_ITEMS) issues.push({ level: "error", message: `te veel producten (${look.items.length}), maximaal ${MAX_ITEMS}` });

  const families = lookFamilies(look);
  if (families.length > 3) issues.push({ level: "warning", message: `meer dan drie kleurfamilies (${families.join(", ")}), niet clean` });
  if (season) {
    for (const { item } of look.items) {
      if (!isInSeason(item, season)) issues.push({ level: "warning", message: `${item.title} past niet bij het seizoen` });
    }
  }
  return issues;
}

export function lookFamilies(look: Look): ColourFamily[] {
  return [...new Set(look.items.map((x) => x.item.family).filter((f): f is ColourFamily => f !== null))];
}

// ---------- samenstellen ----------

/** Kleine voorspelbare random-generator zodat een plan met dezelfde seed hetzelfde blijft. */
export function rng(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function lookId(items: LookItem[]): string {
  return items.map((x) => x.item.handle).sort().join("+");
}

function lookName(items: LookItem[], palette: Palette | null): string {
  const order: Slot[] = ["outer", "mid", "top", "bottom", "shoes"];
  const main = [...items]
    .sort((a, b) => order.indexOf(a.as[0]) - order.indexOf(b.as[0]))
    .filter((x) => !(x.as.length === 1 && x.as[0] === "shoes"))
    .map((x) => x.item.title.replace(/^(THE |PURO |EXCLUSIVE |IMPERIAL |CLASSIC )?MILANO (CASHMERE )?/, "").toLowerCase());
  return `${palette ? palette.name + " · " : ""}${main.join(" + ")}`;
}

function setCovers(item: WardrobeItem): Slot[] {
  return [...new Set(item.pieces.map((x) => x.slot))];
}

/** Een huislook: een bundel die al compleet is, inclusief loafers. */
export function houseLook(item: WardrobeItem): Look | null {
  const covers = setCovers(item);
  if (!item.isSet || !covers.includes("shoes")) return null;
  const items = [{ item, as: covers }];
  const palette = PALETTES.find((p) => item.family && p.families.includes(item.family)) ?? null;
  return { id: lookId(items), name: lookName(items, palette), source: "house", palette, items, hasShoes: true };
}

export function lookFromItems(items: LookItem[], palette: Palette | null, source: Look["source"] = "composed"): Look {
  return { id: lookId(items), name: lookName(items, palette), source, palette, items, hasShoes: items.some((x) => x.as.includes("shoes")) };
}

export interface ComposeOptions {
  season: Exclude<Season, "all">;
  count: number;
  seed?: number;
  /** Handles die zeker in een look moeten (bv. nieuwe drop of bestsellers), in volgorde. */
  anchors?: string[];
  /** Handles die voorrang krijgen bij het aanvullen (bv. bestsellers). */
  prefer?: string[];
  includeHouseLooks?: boolean;
}

/**
 * Stelt looks samen. Elke look begint bij een anker-item, kiest een palet waar dat item in past en vult de
 * overige zones met items uit hetzelfde palet. Items worden zo min mogelijk herhaald over de looks.
 */
export function composeLooks(wardrobe: WardrobeItem[], opts: ComposeOptions): Look[] {
  const rand = rng(opts.seed ?? 1);
  const pool = wardrobe.filter((w) => isInSeason(w, opts.season));
  const byHandle = new Map(pool.map((w) => [w.handle, w]));
  const preferRank = new Map((opts.prefer ?? []).map((h, i) => [h, i]));
  const used = new Map<string, number>();
  const looks: Look[] = [];
  const seen = new Set<string>();

  const templates = TEMPLATES.filter((t) => t.season === "all" || t.season === opts.season);
  const anchors = (opts.anchors ?? []).map((h) => byHandle.get(h)).filter((w): w is WardrobeItem => Boolean(w));
  // Bestsellers en de rest van de collectie om en om, zodat het raster niet alleen uit dezelfde sets bestaat.
  const candidates = [...pool].sort(() => rand() - 0.5).filter((w) => !w.pieces.some((x) => x.slot === "shoes") || w.isSet);
  const preferred = candidates.filter((w) => preferRank.has(w.handle)).sort((a, b) => preferRank.get(a.handle)! - preferRank.get(b.handle)!);
  const others = candidates.filter((w) => !preferRank.has(w.handle));
  const fallbackAnchors: WardrobeItem[] = [];
  for (let i = 0; i < Math.max(preferred.length, others.length); i++) {
    if (preferred[i]) fallbackAnchors.push(preferred[i]);
    if (others[i]) fallbackAnchors.push(others[i]);
  }
  const anchorQueue = [...anchors, ...fallbackAnchors];

  const score = (w: WardrobeItem) => (used.get(w.id) ?? 0) * 10 + (preferRank.has(w.handle) ? -3 + preferRank.get(w.handle)! / 100 : 0) + rand();

  for (let i = 0; looks.length < opts.count && i < anchorQueue.length * 2; i++) {
    const anchor = anchorQueue[i % anchorQueue.length];

    if (opts.includeHouseLooks !== false) {
      const house = houseLook(anchor);
      if (house) {
        if (!seen.has(house.id)) {
          seen.add(house.id);
          looks.push(house);
          used.set(anchor.id, (used.get(anchor.id) ?? 0) + 1);
        }
        continue;
      }
    }

    const look = composeAround(anchor, pool, templates, score, rand);
    if (!look || seen.has(look.id)) continue;
    seen.add(look.id);
    looks.push(look);
    for (const { item } of look.items) used.set(item.id, (used.get(item.id) ?? 0) + 1);
  }
  return looks;
}

/** Lager is beter: een loafer in een tonaal passende kleur wint van een die alleen in het palet past. */
function shoeRank(shoe: WardrobeItem, anchor: WardrobeItem): number {
  if (!anchor.family || !shoe.family) return 0;
  const i = SHOE_PAIRING[anchor.family].indexOf(shoe.family);
  return i === -1 ? 20 : i * 5;
}

function fits(item: WardrobeItem, spec: SlotSpec): boolean {
  if (spec.kinds === "set") return item.isSet && !item.pieces.some((x) => x.slot === "shoes");
  if (item.isSet) return false;
  if (!slotsOf(item).includes(spec.slot)) return false;
  return item.pieces.some((x) => (spec.kinds as Kind[]).includes(x.kind));
}

function composeAround(
  anchor: WardrobeItem,
  pool: WardrobeItem[],
  templates: Template[],
  score: (w: WardrobeItem) => number,
  rand: () => number,
): Look | null {
  const candidates = templates.filter((t) => t.slots.some((s) => fits(anchor, s)));
  if (candidates.length === 0) return null;
  const template = candidates[Math.floor(rand() * candidates.length)];
  const anchorSpec = template.slots.find((s) => fits(anchor, s))!;

  const palettes = PALETTES.filter((p) => !anchor.family || p.families.includes(anchor.family));
  const palette = palettes[Math.floor(rand() * palettes.length)] ?? null;

  const items: LookItem[] = [{ item: anchor, as: anchorSpec.kinds === "set" ? setCovers(anchor) : [anchorSpec.slot] }];
  const covered = new Set(items[0].as);

  for (const spec of template.slots) {
    if (covered.has(spec.slot)) continue;
    const options = pool
      .filter((w) => fits(w, spec))
      .filter((w) => w.line !== anchor.line && !items.some((x) => x.item.line === w.line))
      .filter((w) => !palette || (w.family !== null && palette.families.includes(w.family)))
      .filter((w) => {
        const families = new Set([...items.map((x) => x.item.family), w.family].filter(Boolean));
        return families.size <= 3;
      })
      .sort((a, b) => score(a) - score(b) + (spec.slot === "shoes" ? shoeRank(a, anchor) - shoeRank(b, anchor) : 0));
    const pick = options[0];
    if (!pick) {
      if (spec.optional) continue;
      return null;
    }
    items.push({ item: pick, as: [spec.slot] });
    covered.add(spec.slot);
  }

  if (palette && !paletteFits(palette, lookFamilies({ items } as Look))) return null;
  return lookFromItems(items, palette);
}
