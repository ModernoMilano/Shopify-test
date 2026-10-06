// Van look + shot naar een beeldprompt met de echte productfoto's als referentie, en van een goedgekeurd beeld naar een reel.
// De prompt is Engels (dat volgen beeldmodellen het best); de regels erin zijn de harde merkregels.

import { FAMILY_WORDS } from "./colours";
import { DEFAULT_FACE } from "./casting";
import { lookFromItems, type Look, type LookItem } from "./looks";
import type { Aspect, Grade, Shot } from "./shots";
import type { Slot, WardrobeItem } from "./wardrobe";

/** Alles wat ModernoMilano niet verkoopt en dus nooit in beeld mag. */
export const FORBIDDEN = [
  "watch", "smartwatch", "bracelet", "ring", "necklace", "earrings", "any jewellery",
  "belt", "tie", "bow tie", "pocket square", "scarf", "hat", "cap", "beanie",
  "sunglasses", "eyeglasses", "headphones", "bag", "backpack", "briefcase", "holdall", "gloves",
  "visible socks", "sneakers", "boots", "any shoes other than the referenced loafers",
  "undershirt or extra layer peeking out", "coat, suit or garment that is not in the references",
  "logos", "brand labels", "monograms", "text", "watermarks",
  "cars", "boats", "branded objects",
  "tattoos", "women", "other people in the background",
];

export const CLEAN_LOOK =
  "Clean quiet-luxury aesthetic: uncluttered composition, generous negative space, muted tonal colour palette, " +
  "soft natural light, fine natural skin texture, subtle analogue film grain, " +
  "no HDR, no heavy filters, no lens flare, no vignette, no text or graphics. Looks like a real editorial photograph, not CGI.";

const GRADE: Record<Grade, string> = {
  natural: "Colour: true-to-life natural colours, neutral white balance.",
  "muted-warm": "Colour: gently muted, warm filmic grade with soft contrast; the garment colours stay true and recognisable.",
  "muted-cool": "Colour: desaturated, slightly cool filmic grade with soft contrast, like a quiet film photograph; the garment colours stay recognisable.",
  bw: "Black-and-white fine-art photograph with rich greys, soft contrast and fine grain.",
};

export { DEFAULT_FACE };

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

export interface VideoRequest {
  model: "kling3_0";
  /** Het goedgekeurde beeld (in 9:16) is het startframe. */
  startFrame: "approved-still";
  aspect: "9:16";
  duration: number;
  mode: "pro";
  sound: "off";
  prompt: string;
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

/** Wat er in beeld komt bij dit shot: de hele look, het hoofdstuk, alle kleuren ervan, of alleen broek en loafers. */
export function subjectOf(look: Look, shot: Shot, wardrobe: WardrobeItem[] = []): Look {
  const anchor = look.items[0];
  switch (shot.subject) {
    case "look": {
      // Halflang of tot de taille: de voeten vallen buiten beeld, dus de loafers gaan niet mee als referentie.
      if (shot.framing !== "three-quarter" && shot.framing !== "waist-up") return look;
      const visible = look.items.filter((x) => !(x.as.length === 1 && x.as[0] === "shoes"));
      return visible.length === look.items.length ? look : lookFromItems(visible, look.palette, look.source);
    }
    case "anchor":
      return lookFromItems([anchor], look.palette, look.source);
    case "line": {
      const siblings = wardrobe.filter((w) => w.line === anchor.item.line && w.id !== anchor.item.id).slice(0, 3);
      return lookFromItems([anchor, ...siblings.map((item): LookItem => ({ item, as: anchor.as }))], look.palette, look.source);
    }
    case "lower": {
      const lower = look.items.filter((x) => x.as.includes("bottom") || x.as.includes("shoes"));
      return lookFromItems(lower.length ? lower : look.items, look.palette, look.source);
    }
  }
}

/** Eén zin per product: wat het is, welke kleur, welke referentiefoto. */
function wardrobeLines(look: Look, refIndex: Map<string, number[]>): string[] {
  return wearingOrder(look).map(({ item }) => {
    const pieces = item.pieces.map((p) => p.label).join(", ");
    const colour = item.colour ? item.colour.toLowerCase() : item.family ? FAMILY_WORDS[item.family] : "";
    const said = pieces.toLowerCase();
    const material = item.material && !item.material.split(" ").some((w) => w.length > 4 && said.includes(w.toLowerCase())) ? ` in ${item.material}` : "";
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

/** Referentielijst: per product de hoofdfoto, plus een modelfoto als die er is (beter voor pasvorm). Nummering loopt door over looks. */
export function references(looks: Look[], perItem = 2): { refs: Reference[]; index: Map<string, number[]> } {
  const refs: Reference[] = [];
  const index = new Map<string, number[]>();
  for (const look of looks) {
    for (const { item } of wearingOrder(look)) {
      if (index.has(item.id)) continue;
      const urls = [item.images.primary, item.images.model, item.images.detail].filter((u): u is string => Boolean(u));
      const unique = [...new Set(urls)].slice(0, perItem);
      index.set(item.id, unique.map((url) => {
        refs.push({ url, label: item.title });
        return refs.length;
      }));
    }
  }
  return { refs, index };
}

export interface PromptOptions {
  aspect?: Aspect;
  resolution?: "2k" | "4k";
  /** Beschrijving van het hoofdgezicht (of `<<<element_id>>>`). */
  casting?: string;
  /** Voor beelden met twee mannen: de look en het gezicht van de tweede, jongere man. */
  second?: { look: Look; casting: string };
  /** Nodig voor shots die alle kleuren van een stuk tonen. */
  wardrobe?: WardrobeItem[];
}

export function buildPrompt(look: Look, shot: Shot, opts: PromptOptions = {}): GenerationRequest {
  const main = subjectOf(look, shot, opts.wardrobe);
  const duo = shot.people === 2 && opts.second ? subjectOf(opts.second.look, shot, opts.wardrobe) : null;
  const { refs, index } = references(duo ? [main, duo] : [main]);
  const hasPerson = shot.people > 0;
  const sketch = shot.render === "sketch";
  const hasShoes = main.hasShoes && (!duo || duo.hasShoes);
  const palette = look.palette && shot.subject !== "line" ? ` Colour mood: ${look.palette.mood}.` : "";
  const casting = opts.casting ?? DEFAULT_FACE;

  let subject: string;
  let wardrobe: string;
  if (duo) {
    subject = `Subjects: exactly two men. The older man: ${casting}. The younger man: ${opts.second!.casting}. Pose: ${shot.pose}.`;
    wardrobe =
      `The older man wears ONLY the following ModernoMilano pieces and nothing else:\n- ${wardrobeLines(main, index).join("\n- ")}\n\n` +
      `The younger man wears ONLY the following ModernoMilano pieces and nothing else:\n- ${wardrobeLines(duo, index).join("\n- ")}`;
  } else if (hasPerson) {
    subject = shot.framing === "detail" ? `Subject: only part of the man is visible (${shot.pose}).` : `Subject: ${casting}. Pose: ${shot.pose}.`;
    wardrobe = `He wears ONLY the following ModernoMilano pieces and nothing else:\n- ${wardrobeLines(main, index).join("\n- ")}`;
  } else if (sketch) {
    subject = `Subject: ${shot.pose}.`;
    wardrobe = `The sketch depicts ONLY these ModernoMilano pieces, drawn from the references:\n- ${wardrobeLines(main, index).join("\n- ")}`;
  } else {
    subject = shot.pose === "no person" ? "Subject: only these garments, no person, no mannequin." : `Subject: only these garments, no person, no mannequin; ${shot.pose.replace(/^no person;\s*/, "")}.`;
    wardrobe = `The objects are ONLY these ModernoMilano pieces:\n- ${wardrobeLines(main, index).join("\n- ")}`;
  }

  const fidelity =
    "Reproduce every garment exactly as in its reference: same colour and shade, same knit or weave texture, same collar, " +
    "same number and position of buttons or zip, same pockets, same length and fit. Do not add, remove or redesign any detail.";

  const feetInFrame = shot.framing === "full-body" || shot.subject === "lower";
  const feet = !hasPerson
    ? null
    : !feetInFrame
      ? "The feet are out of frame."
      : hasShoes
        ? "The loafers are worn sockless with bare ankles visible."
        : "No shoes are part of this look: keep the feet out of frame.";

  const prompt = [
    sketch ? "Photograph of a pencil fashion sketch." : `${FRAMING[shot.framing]}.`,
    `Setting: ${shot.setting}. Light: ${shot.light}. Camera: ${shot.camera}.`,
    subject,
    wardrobe,
    main.items.length > 1 ? layering(main) : null,
    fidelity,
    feet,
    `Absolutely none of the following may appear: ${FORBIDDEN.join(", ")}.`,
    sketch ? "Clean, calm, generous empty paper around the drawing." : `${CLEAN_LOOK}${palette} ${GRADE[shot.grade]}`,
  ]
    .filter(Boolean)
    .join("\n\n");

  return { model: "nano_banana_pro", aspect: opts.aspect ?? "4:5", resolution: opts.resolution ?? "2k", prompt, references: refs };
}

/** Reel van een goedgekeurd beeld: rustige beweging, kleding en gezicht blijven exact gelijk. */
export function buildMotion(shot: Shot): VideoRequest {
  const who = shot.people > 0 ? "the man, his face, every garment, the loafers" : "every garment";
  return {
    model: "kling3_0",
    startFrame: "approved-still",
    aspect: "9:16",
    duration: shot.pillar === "product" ? 6 : 10,
    mode: "pro",
    sound: "off",
    prompt:
      `Animate this exact photograph: ${shot.motion}. Keep ${who}, the colours and the setting exactly as in the start frame: ` +
      "garments must not change colour, shape, length or details. No new objects, no accessories, no text, no extra people. " +
      "Calm, slow, real-time motion, one continuous shot, no cuts, no zoom effects, no camera shake.",
  };
}
