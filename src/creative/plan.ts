// Contentplan volgens de norm (creative-engine/brand/norm.md): hoofdstukken van 9 posts, gelezen in rijen van 3.
// Per hoofdstuk: 4 carrousels, 3 reels, 2 losse beelden; maximaal 1 studiobeeld als hoofdbeeld; nooit hetzelfde
// beeldtype naast elkaar; één vast gezicht. Elke regel bevat de complete opdracht voor het beeldmodel.

import { captionDraft, type CaptionDraft } from "./captions";
import { castFor, type Cast } from "./casting";
import { composeLooks, validateLook, type Look } from "./looks";
import { buildMotion, buildPrompt, type GenerationRequest, type VideoRequest } from "./prompt";
import { deriveShot, shotById, type Pillar, type Shot } from "./shots";
import { isInSeason, seasonFor, type Season, type WardrobeItem } from "./wardrobe";

export type Format = "single" | "carousel" | "reel";

export interface Frame {
  shot: Shot;
  request: GenerationRequest;
}

export interface PlanEntry {
  n: number;
  date: string;
  pillar: Pillar;
  format: Format;
  look: Look;
  /** Alleen bij twee mannen in beeld. */
  secondLook?: Look;
  frames: Frame[];
  /** Bij een reel: de beweging, met het eerste (goedgekeurde) beeld als startframe. */
  video?: VideoRequest;
  caption: CaptionDraft;
}

type SlotKind = "single" | "product-carousel" | "craft-carousel" | "styling-carousel" | "reel";

interface ChapterSlot {
  pillar: Pillar;
  kind: SlotKind;
  heroes: (season: Exclude<Season, "all">) => string[];
}

const EDITORIAL = (s: Exclude<Season, "all">) =>
  s === "fw"
    ? ["volcanic-coast", "milano-courtyard", "architecture", "library-fireside", "borgo", "interior", "lake-terrace"]
    : ["riviera", "milano-courtyard", "architecture", "borgo", "lake-terrace", "interior"];
const WALKS = (s: Exclude<Season, "all">) =>
  s === "fw" ? ["milano-courtyard", "architecture", "volcanic-coast", "borgo"] : ["milano-courtyard", "architecture", "borgo"];
const WORLD = (s: Exclude<Season, "all">) =>
  s === "fw"
    ? ["landscape", "snowfield", "espresso-terrace", "bw-portrait", "two-generations"]
    : ["island-coast", "espresso-terrace", "bw-portrait", "two-generations"];

/**
 * Eén hoofdstuk van 9 posts. Rij 1: opener, product, ambacht. Rij 2: styling, reel, loafers.
 * Rij 3: wereld, styling, reel. Elke rij heeft een man op een plek én een product dat scherp in beeld is.
 */
export const CHAPTER: ChapterSlot[] = [
  { pillar: "editorial", kind: "single", heroes: EDITORIAL },
  { pillar: "product", kind: "product-carousel", heroes: () => ["studio-full"] },
  { pillar: "craft", kind: "craft-carousel", heroes: () => ["texture"] },
  { pillar: "styling", kind: "styling-carousel", heroes: EDITORIAL },
  { pillar: "editorial", kind: "reel", heroes: WALKS },
  { pillar: "product", kind: "reel", heroes: () => ["loafer-walk"] },
  { pillar: "world", kind: "single", heroes: WORLD },
  { pillar: "styling", kind: "styling-carousel", heroes: EDITORIAL },
  { pillar: "editorial", kind: "reel", heroes: WALKS },
];

/** Maximaal zo vaak hetzelfde hoofdbeeld per hoofdstuk. */
export const MAX_SAME_HERO = 2;

export interface PlanOptions {
  start: Date;
  posts: number;
  /** Weekdagen om te posten (0 = zondag). Norm: zondag, maandag, woensdag, vrijdag. */
  days?: number[];
  seed?: number;
  anchors?: string[];
  prefer?: string[];
  /** Vervangt het hoofdgezicht (bv. `<<<element_id>>>`). */
  casting?: string;
  secondCasting?: string;
}

export const DEFAULT_DAYS = [0, 1, 3, 5];

function nextDates(start: Date, count: number, days: number[]): string[] {
  const out: string[] = [];
  const d = new Date(Date.UTC(start.getUTCFullYear(), start.getUTCMonth(), start.getUTCDate()));
  while (out.length < count) {
    if (days.includes(d.getUTCDay())) out.push(d.toISOString().slice(0, 10));
    d.setUTCDate(d.getUTCDate() + 1);
  }
  return out;
}

const garments = (look: Look) => look.items.filter((x) => !(x.as.length === 1 && x.as[0] === "shoes")).length;
const layered = (look: Look) => look.items.some((x) => x.as.includes("mid") || x.as.includes("outer"));

export function makePlan(wardrobe: WardrobeItem[], opts: PlanOptions): PlanEntry[] {
  const season = seasonFor(opts.start);
  const seed = opts.seed ?? 1;
  const looks = composeLooks(wardrobe, { season, count: opts.posts + 4, seed, anchors: opts.anchors, prefer: opts.prefer })
    .filter((l) => validateLook(l, wardrobe, season).every((i) => i.level !== "error"));
  if (looks.length === 0) return [];

  const cast: Cast = castFor(seed, { main: opts.casting, second: opts.secondCasting });
  const dates = nextDates(opts.start, opts.posts, opts.days ?? DEFAULT_DAYS);
  const pool = wardrobe.filter((w) => isInSeason(w, season));
  // Per hoofdstuk hooguit MAX_SAME_HERO keer hetzelfde hoofdbeeld; over het hele plan wordt er doorgeroteerd.
  const heroCount = new Map<string, number>();
  const totalCount = new Map<string, number>();
  let previousHero = "";
  const usedLooks = new Set<string>();

  const takeLook = (want?: (l: Look) => boolean): Look => {
    const free = looks.filter((l) => !usedLooks.has(l.id));
    const pick = (want && free.find(want)) ?? free[0] ?? looks[usedLooks.size % looks.length];
    usedLooks.add(pick.id);
    return pick;
  };

  const pickHero = (ids: string[], look: Look): Shot => {
    const candidates = ids
      .map(shotById)
      .filter((s) => s.season === "all" || s.season === season)
      .filter((s) => look.hasShoes || s.framing !== "full-body");
    const fresh = candidates.filter((s) => s.id !== previousHero && (heroCount.get(s.id) ?? 0) < MAX_SAME_HERO);
    const list = fresh.length ? fresh : candidates;
    const shot = [...list].sort((a, b) => (totalCount.get(a.id) ?? 0) - (totalCount.get(b.id) ?? 0))[0];
    heroCount.set(shot.id, (heroCount.get(shot.id) ?? 0) + 1);
    totalCount.set(shot.id, (totalCount.get(shot.id) ?? 0) + 1);
    previousHero = shot.id;
    return shot;
  };

  return dates.map((date, i) => {
    const slot = CHAPTER[i % CHAPTER.length];
    if (i % CHAPTER.length === 0) heroCount.clear();
    // Styling, opener en wereldbeeld krijgen bij voorkeur een gelaagde look (norm: minstens 1 op 3 posts gelaagd).
    const wantLayers = slot.kind === "styling-carousel" || (slot.kind === "single" && slot.pillar !== "product");
    const look = takeLook(wantLayers ? (l) => layered(l) && garments(l) >= 2 : undefined);
    const hero = pickHero(slot.heroes(season), look);

    let secondLook: Look | undefined;
    if (hero.people === 2) {
      secondLook = takeLook((l) => l.hasShoes && l.palette?.id === look.palette?.id);
    }

    const request = (shot: Shot, aspect: "4:5" | "9:16" = "4:5") =>
      buildPrompt(look, shot, {
        aspect,
        wardrobe: pool,
        casting: cast.main.description,
        second: secondLook ? { look: secondLook, casting: cast.second.description } : undefined,
      });

    let shots: Shot[];
    let format: Format;
    switch (slot.kind) {
      case "single":
        shots = [hero];
        format = "single";
        break;
      case "product-carousel":
        shots = [hero, deriveShot(hero, "waist-up"), shotById("texture")];
        format = "carousel";
        break;
      case "craft-carousel":
        shots = [hero, shotById("folded-stack"), shotById("sketch")];
        format = "carousel";
        break;
      case "styling-carousel":
        shots = [hero, shotById("studio-full"), deriveShot(hero, "detail"), shotById("look-flatlay")].filter(
          (s) => look.hasShoes || s.framing !== "full-body",
        );
        format = "carousel";
        break;
      case "reel":
        shots = [hero];
        format = "reel";
        break;
    }

    const frames = shots.map((shot) => ({ shot, request: request(shot, format === "reel" ? "9:16" : "4:5") }));
    const entry: PlanEntry = {
      n: i + 1,
      date,
      pillar: slot.pillar,
      format,
      look,
      secondLook,
      frames,
      video: format === "reel" ? buildMotion(hero) : undefined,
      caption: captionDraft({ pillar: slot.pillar, look, secondLook, date }),
    };
    return entry;
  });
}
