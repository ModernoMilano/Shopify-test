// Van look + shot naar een beeldprompt met de echte productfoto's als referentie.
// De prompt is Engels (dat volgen beeldmodellen het best); de regels erin zijn de harde merkregels.

import { FAMILY_WORDS } from "./colours";
import type { Look } from "./looks";
import type { Aspect, Shot } from "./shots";
import type { Slot } from "./wardrobe";

/** Alles wat ModernoMilano niet verkoopt en dus nooit in beeld mag. */
export const FORBIDDEN = [
  "watch", "smartwatch", "bracelet", "ring", "necklace", "earrings", "any jewellery",
  "belt", "tie", "bow tie", "pocket square", "scarf", "hat", "cap", "beanie",
  "sunglasses", "eyeglasses", "bag", "backpack", "briefcase", "gloves",
  "visible socks", "sneakers", "boots", "any shoes other than the referenced loafers",
  "undershirt or extra layer peeking out", "coat or garment that is not in the references",
  "logos", "brand labels", "monograms", "text", "watermarks",
  "tattoos", "other people in the background",
];

export const CLEAN_LOOK =
  "Clean quiet-luxury aesthetic: uncluttered composition, generous negative space, muted tonal colour palette, " +
  "soft natural light, true-to-life colours, fine natural skin texture, subtle analogue film grain, " +
  "no HDR, no heavy filters, no lens flare, no vignette, no text or graphics. Looks like a real editorial photograph, not CGI.";

export const DEFAULT_CASTING =
  "a handsome Mediterranean man in his early thirties, well-groomed short dark hair, light natural stubble, " +
  "lean athletic build, calm confident expression, no jewellery, no tattoos";

export interface Reference {
  url: string;
  label: string;
}

export interface GenerationRequest {
  model: "nano_banana_pro";
  aspect: Aspect;
  resolution: "2k" | "4k";
  prompt: string;
  references: Reference[];
}

const SLOT_ORDER: Slot[] = ["outer", "mid", "top", "bottom", "shoes"];

const FRAMING: Record<Shot["framing"], string> = {
  "full-body": "Full-length photograph, the whole figure visible from head to the loafers",
  "three-quarter": "Three-quarter length photograph framed from the knees up, feet out of frame",
  "waist-up": "Photograph framed from the waist up",
  detail: "Close-up detail photograph",
  "still-life": "Still-life product photograph without any person",
};

function wearingOrder(look: Look) {
  return [...look.items].sort((a, b) => SLOT_ORDER.indexOf(a.as[0]) - SLOT_ORDER.indexOf(b.as[0]));
}

/** Eén zin per product: wat het is, welke kleur, welke referentiefoto. */
function wardrobeLines(look: Look, refIndex: Map<string, number[]>): string[] {
  return wearingOrder(look).map(({ item }) => {
    const pieces = item.pieces.map((p) => p.label).join(", ");
    const colour = item.colour ? item.colour.toLowerCase() : item.family ? FAMILY_WORDS[item.family] : "";
    const material = item.material && !pieces.toLowerCase().includes(item.material) ? ` in ${item.material}` : "";
    const refs = refIndex.get(item.id)!.map((n) => `#${n}`).join(" and ");
    const what = item.isSet ? `the complete "${item.title}" outfit set (${pieces})` : `the ${colour} ${pieces}${material} ("${item.title}")`;
    return `${what}, exactly as shown in reference image ${refs}`;
  });
}

function layering(look: Look): string | null {
  const covered = new Set(look.items.flatMap((x) => x.as));
  const parts: string[] = [];
  if (covered.has("mid")) parts.push("the mid layer is worn over the base top");
  if (covered.has("outer")) parts.push("the outer layer is worn over the other layers, closed or open exactly as in its reference");
  return parts.length ? `Layering: ${parts.join("; ")}.` : null;
}

/** Bouwt de referentielijst: per product de hoofdfoto, plus een modelfoto als die er is (beter voor pasvorm). */
export function references(look: Look, perItem = 2): { refs: Reference[]; index: Map<string, number[]> } {
  const refs: Reference[] = [];
  const index = new Map<string, number[]>();
  for (const { item } of wearingOrder(look)) {
    const urls = [item.images.primary, item.images.model, item.images.detail].filter((u): u is string => Boolean(u));
    const unique = [...new Set(urls)].slice(0, perItem);
    index.set(item.id, unique.map((url) => {
      refs.push({ url, label: item.title });
      return refs.length;
    }));
  }
  return { refs, index };
}

export function buildPrompt(look: Look, shot: Shot, opts: { aspect?: Aspect; casting?: string; resolution?: "2k" | "4k" } = {}): GenerationRequest {
  const { refs, index } = references(look);
  const hasPerson = shot.people > 0;
  const lines = wardrobeLines(look, index);
  const palette = look.palette ? ` Colour mood: ${look.palette.mood}.` : "";

  const subject = hasPerson
    ? `Subject: ${opts.casting ?? DEFAULT_CASTING}. Pose: ${shot.pose}.`
    : "Subject: only the garments of this look, no person, no mannequin, no hanger.";

  const wardrobe = hasPerson
    ? `He wears ONLY the following ModernoMilano pieces and nothing else:\n- ${lines.join("\n- ")}`
    : `The objects are ONLY these ModernoMilano pieces:\n- ${lines.join("\n- ")}`;

  const fidelity =
    "Reproduce every garment exactly as in its reference: same colour and shade, same knit or weave texture, same collar, " +
    "same number and position of buttons or zip, same pockets, same length and fit. Do not add, remove or redesign any detail.";

  const shoes = look.hasShoes
    ? "The loafers are worn sockless with bare ankles visible."
    : "No shoes are part of this look: keep the feet out of frame.";

  const rules = `Absolutely none of the following may appear: ${FORBIDDEN.join(", ")}.`;

  const prompt = [
    `${FRAMING[shot.framing]}.`,
    `Setting: ${shot.setting}. Light: ${shot.light}. Camera: ${shot.camera}.`,
    subject,
    wardrobe,
    layering(look),
    fidelity,
    hasPerson || look.hasShoes ? shoes : null,
    rules,
    CLEAN_LOOK + palette,
  ]
    .filter(Boolean)
    .join("\n\n");

  return {
    model: "nano_banana_pro",
    aspect: opts.aspect ?? "4:5",
    resolution: opts.resolution ?? "2k",
    prompt,
    references: refs,
  };
}
