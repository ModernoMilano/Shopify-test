// Contentplan: welke look, in welk beeldtype, op welke dag. Elke regel bevat de complete opdracht voor het beeldmodel.

import { composeLooks, validateLook, type Look } from "./looks";
import { buildPrompt, type GenerationRequest } from "./prompt";
import { SHOTS, shotsFor, type Aspect, type Pillar, type Shot } from "./shots";
import { seasonFor, type WardrobeItem } from "./wardrobe";

export type Format = "feed" | "carousel" | "story";

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
  frames: Frame[];
  /** Waar de caption over gaat; de tekst zelf schrijft Claude bij het posten. */
  angle: string;
}

/** Contentmix per negen posts (een volledig 3x3-raster), afgeleid van de concurrentie. */
export const MIX: Pillar[] = ["product", "editorial", "craft", "product", "editorial", "world", "styling", "editorial", "craft"];

const ANGLES: Record<Pillar, string> = {
  product: "Het product centraal: pasvorm, kleur, materiaal. Eén zin over het gevoel, één over het detail.",
  editorial: "Een moment, geen verkooppraatje: waar draag je dit, hoe voelt het.",
  craft: "Het materiaal en de afwerking: cashmere, suède, breisel, knopen. Rustig en precies.",
  styling: "Eén look in drie beelden: geheel, detail, opgevouwen. Benoem de stukken.",
  world: "De wereld van ModernoMilano: ruimte, rust, Italiaanse elegantie. Nauwelijks tekst.",
};

export interface PlanOptions {
  start: Date;
  posts: number;
  /** Weekdagen om te posten (0 = zondag). */
  days?: number[];
  seed?: number;
  anchors?: string[];
  prefer?: string[];
  aspect?: Aspect;
  casting?: string;
}

function nextDates(start: Date, count: number, days: number[]): string[] {
  const out: string[] = [];
  const d = new Date(Date.UTC(start.getUTCFullYear(), start.getUTCMonth(), start.getUTCDate()));
  while (out.length < count) {
    if (days.includes(d.getUTCDay())) out.push(d.toISOString().slice(0, 10));
    d.setUTCDate(d.getUTCDate() + 1);
  }
  return out;
}

export function makePlan(wardrobe: WardrobeItem[], opts: PlanOptions): PlanEntry[] {
  const season = seasonFor(opts.start);
  const looks = composeLooks(wardrobe, {
    season,
    count: opts.posts,
    seed: opts.seed,
    anchors: opts.anchors,
    prefer: opts.prefer,
  }).filter((l) => validateLook(l, wardrobe, season).every((i) => i.level !== "error"));
  if (looks.length === 0) return [];

  const dates = nextDates(opts.start, opts.posts, opts.days ?? [1, 3, 5]);
  const usedShots = new Map<string, number>();
  const pick = (candidates: Shot[]): Shot => {
    const s = [...candidates].sort((a, b) => (usedShots.get(a.id) ?? 0) - (usedShots.get(b.id) ?? 0))[0];
    usedShots.set(s.id, (usedShots.get(s.id) ?? 0) + 1);
    return s;
  };
  const byId = (id: string) => SHOTS.find((s) => s.id === id)!;
  const req = (look: Look, shot: Shot, aspect?: Aspect) => buildPrompt(look, shot, { aspect: aspect ?? opts.aspect, casting: opts.casting });

  return dates.map((date, i) => {
    const look = looks[i % looks.length];
    const pillar = MIX[i % MIX.length];
    let frames: Frame[];
    let format: Format = "feed";

    if (pillar === "styling") {
      format = "carousel";
      const hero = look.hasShoes ? byId("studio-full") : byId("studio-portrait");
      frames = [hero, byId("texture"), byId("still-life")].map((shot) => ({ shot, request: req(look, shot) }));
    } else {
      const options = shotsFor({ season, hasShoes: look.hasShoes, pillar });
      const shot = pick(options.length ? options : shotsFor({ season, hasShoes: look.hasShoes, pillar: "editorial" }));
      frames = [{ shot, request: req(look, shot) }];
    }
    return { n: i + 1, date, pillar, format, look, frames, angle: ANGLES[pillar] };
  });
}
