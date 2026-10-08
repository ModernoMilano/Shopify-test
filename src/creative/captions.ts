// Captions volgens de norm: Engels in de feed, een kop van 3 tot 7 woorden met een punt, één of twee zinnen over stof en
// moment, dan "Wearing:" met de exacte productnamen, en hooguit 4 hashtags. Geen emoji, geen uitroeptekens, geen "shop now".
// De productregel en de hashtags maakt de engine; kop en tekst schrijft Claude bij het opleveren.

import type { Look } from "./looks";
import type { Pillar } from "./shots";

export const MAX_HASHTAGS = 4;
export const BRAND_TAG = "#ModernoMilano";

/** Waar de tekst over gaat, per pijler. */
export const ANGLES: Record<Pillar, string> = {
  product: "Eén stuk of één look, helder: pasvorm, kleur en stof. Op een productpost mag één feitelijke zin als 'Available in N colours.', als het aantal klopt.",
  editorial: "Een moment op een plek: lopen, een ritueel. Geen verkooppraatje.",
  craft: "Stof en afwerking: steek, kraag, knoop, suède. Noem alleen wat in de productdata staat.",
  styling: "Hoe je combineert, laag voor laag. Noem de formule (bv. cardigan over polo, tonaal van kraag tot loafer).",
  world: "De wereld rond het merk: ruimte, rust, een ritueel. Nauwelijks tekst.",
};

export const TONE_RULES = [
  "Rustig en ingetogen. Geen uitroeptekens, geen emoji.",
  "Over stof en gevoel, niet over status.",
  "Alleen claims die in de productdata staan: geen 'traceable', 'Made in Italy' of 'Grade A' zonder bewijs.",
  "Geen korting, geen 'sale', geen 'shop now' in de feed. Verkopen gebeurt via de Wearing-regel en de producttags.",
  "Geen namen of campagnetitels van concurrenten.",
  "Hooguit één vraag aan de volgers per 9 posts.",
];

export interface CaptionDraft {
  angle: string;
  /** Door Claude in te vullen bij het opleveren. */
  headline: string;
  body: string;
  wearing: string;
  hashtags: string[];
}

function titleCase(s: string): string {
  return s.toLowerCase().replace(/\b\p{L}/gu, (c) => c.toUpperCase());
}

/** "MILANO CASHMERE TORINO BLAZER - TORTORA" → "Milano Cashmere Torino Blazer in Tortora". */
export function productName(title: string): string {
  const m = title.match(/^(.*?)\s+-\s+([^-]+)$/);
  return m ? `${titleCase(m[1])} in ${titleCase(m[2])}` : titleCase(title);
}

export function wearingLine(...looks: (Look | undefined)[]): string {
  const names = looks.filter((l): l is Look => Boolean(l)).flatMap((l) => l.items.map((x) => productName(x.item.title)));
  return `Wearing: ${[...new Set(names)].join(", ")}.`;
}

/** Seizoenstag: herfst/winter vanaf september (FW + jaar), lente/zomer vanaf april (SS + jaar). */
export function seasonTag(date: string): string {
  const d = new Date(date);
  const m = d.getUTCMonth() + 1;
  const y = d.getUTCFullYear();
  if (m >= 9) return `${BRAND_TAG}FW${String(y).slice(2)}`;
  if (m <= 3) return `${BRAND_TAG}FW${String(y - 1).slice(2)}`;
  return `${BRAND_TAG}SS${String(y).slice(2)}`;
}

export function hashtags(look: Look, date: string): string[] {
  const tags = [BRAND_TAG, seasonTag(date)];
  if (look.items.some((x) => x.item.material === "cashmere")) tags.push("#cashmere");
  tags.push("#quietluxury");
  return tags.slice(0, MAX_HASHTAGS);
}

export function captionDraft(input: { pillar: Pillar; look: Look; date: string }): CaptionDraft {
  return {
    angle: ANGLES[input.pillar],
    headline: "",
    body: "",
    wearing: wearingLine(input.look),
    hashtags: hashtags(input.look, input.date),
  };
}
