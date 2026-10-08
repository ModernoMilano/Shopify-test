// Van look + shot naar een beeldprompt met de echte productfoto's als referentie, en van een goedgekeurd beeld naar een reel.
// De prompt is Engels (dat volgen beeldmodellen het best); de regels erin zijn de harde merkregels.
// Staat er iemand in beeld, dan is dat het vaste model (casting.ts). Standaard komt zijn gezicht via het Higgsfield-element
// (de placeholder in de prompt) en gaan alleen productfoto's mee (#1..#n). Alleen in de terugval zonder element gaan
// zijn gezichtsfoto's als eerste mee (#1-#3), de productfoto's daarna. Nooit een andere man en nooit twee.

import { FAMILY_WORDS } from "./colours";
import { MODEL, type FaceRef } from "./casting";
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
  "car or boat badges, emblems or brand names", "readable number plates", "branded objects",
  "tattoos", "women",
];

/** Andere mensen. Op een openbare plek mogen 2 of 3 verre, onscherpe voorbijgangers (MODEL.publicPlaces), verder niemand. */
const OTHER_PEOPLE = { public: "any other person who is near, sharp or recognisable", private: "other people" };

/**
 * Filmrol-woorden. In de batch van 100 gaven ze nepfilmranden en opgeplakte korrel, dus ze komen in geen enkele prompt.
 * Ook geen los "film": alleen het vaste "No film borders" uit realism_en mag. Voorlopig komt er ook achteraf geen korrel bij.
 */
export const FILM_WORDS = [
  "Kodak", "Portra", "Ektar", "Vision3", "Fuji", "Fujifilm", "Cinestill", "Ilford",
  "photographed on film", "shot on film", "film photograph", "film stock", "35mm film", "film grain", "film look",
  "still from a film", "film still", "filmic", "analog", "analogue", "grain", "grainy", "halation",
];
const escapeRe = (w: string) => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
export const FILM_RE = new RegExp(`\\b(?:${FILM_WORDS.map(escapeRe).join("|")})\\b|\\bfilm\\b(?! borders)`, "i");
export const hasFilmWords = (text: string) => FILM_RE.test(text);

export const CLEAN_LOOK =
  "Calm, uncluttered composition with room around the subject and a muted tonal colour palette; " +
  "no HDR, no heavy filters, no lens flare, no vignette, no text or graphics. A real editorial photograph, not CGI.";

const GRADE: Record<Grade, string> = {
  natural: "Colour: true-to-life natural colours, neutral white balance.",
  "muted-warm": "Colour: gently muted, warm grade with soft contrast; the garment colours stay true and recognisable.",
  "muted-cool": "Colour: desaturated, slightly cool grade with soft contrast; the garment colours stay recognisable.",
  bw: "Black-and-white photograph with rich greys and soft contrast.",
};

/** Hoogstens zoveel referentiebeelden per opdracht (gezicht en producten samen). */
export const MAX_REFERENCES = 14;

/**
 * Met het model in beeld hoogstens zoveel productfoto's, zodat zijn gezicht niet verwatert (model.json → rules).
 * Elk product krijgt er wel altijd minstens één: een look van 5 stukken krijgt er dus 5.
 */
export const MAX_PRODUCT_REFS_WITH_MODEL = 4;

export interface Reference {
  /** product = foto van een ModernoMilano-product. face = gezichtsfoto van het model, alleen in de terugval zonder element (vooraan). */
  kind: "face" | "product";
  /** Product: de Shopify-URL (importeren met media_import_url). Gezicht: het bestand in de repo (niet importeren). */
  url: string;
  label: string;
  /** Het Higgsfield-id voor `medias`. Bij een gezichtsfoto de 4K-versie (upscale_job_id uit model.json). */
  mediaId?: string;
}

export interface GenerationRequest {
  model: "nano_banana_pro";
  aspect: Aspect;
  resolution: "2k" | "4k";
  prompt: string;
  references: Reference[];
}

/**
 * Video volgens model.json → rules.video (besluit van de eigenaar, 8 oktober 2026): alleen Seedance 2.5, nooit vanuit
 * alleen tekst. Het goedgekeurde beeld is het startframe. Seedance 2.5 kent het element niet: zijn gezicht komt uit het
 * startbeeld en, als het in beeld is, uit de 4K-gezichtsfoto's (`videoFaceRefs`) als image_references.
 * Altijd eerst een concept in 480p (`draft`), pas na de controle afmaken in 1080p.
 */
export interface VideoRequest {
  model: "seedance_2_5";
  mode: "omni_reference";
  /** Het goedgekeurde beeld (in 9:16) is het startframe (`start_image`). */
  startFrame: "approved-still";
  /** Gezichtsfoto's als `image_references`, na het startbeeld. Leeg als zijn gezicht niet in beeld komt. */
  faceRefs: FaceRef[];
  aspect: "9:16";
  resolution: "1080p";
  bitrate: "high";
  duration: number;
  audio: false;
  /** Eerst `draft: true` (480p); na goedkeuring afmaken met `draft_job_id`. */
  draftFirst: true;
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

/**
 * Referentielijst: eerst `lead` (alleen in de terugval: de gezichtsfoto's van het model), dan per product de hoofdfoto,
 * plus een modelfoto als die er is (beter voor pasvorm). De productnummers lopen door na `lead`.
 */
export function references(looks: Look[], perItem = 2, lead: Reference[] = []): { refs: Reference[]; index: Map<string, number[]> } {
  const refs: Reference[] = [...lead];
  const index = new Map<string, number[]>();
  for (const look of looks) {
    for (const { item } of wearingOrder(look)) {
      if (index.has(item.id)) continue;
      const urls = [item.images.primary, item.images.model, item.images.detail].filter((u): u is string => Boolean(u));
      const unique = [...new Set(urls)].slice(0, perItem);
      index.set(item.id, unique.map((url) => {
        refs.push({ kind: "product", url, label: item.title });
        return refs.length;
      }));
    }
  }
  return { refs, index };
}

/**
 * Hoe zijn gezicht in beeld komt. element (standaard): de element-placeholder in de prompt, geen gezichtsfoto's in medias.
 * refs: de terugval als het element niet werkt; dan gaan ref-1, ref-4 en ref-2 (4K) als #1-#3 vooraan mee.
 */
export type FaceMode = "element" | "refs";

/**
 * De gezichtsfoto's van het model voor dit shot: alleen in de terugval (refs), in de volgorde van model.json → face_ref_order.
 * Bij een detail (gezicht uit beeld) is één foto genoeg voor huid en handen.
 */
export function faceReferences(shot: Shot, faces: FaceMode = "element"): Reference[] {
  if (shot.people === 0 || faces === "element") return [];
  const refs = shot.framing === "detail" ? MODEL.fallbackFaceRefs.slice(0, 1) : MODEL.fallbackFaceRefs;
  return refs.map((r): Reference => ({ kind: "face", url: r.file, label: `ModernoMilano model (face, ${r.id})`, mediaId: r.upscaleJobId }));
}

/** Productfoto's per stuk met het model in beeld: binnen MAX_PRODUCT_REFS_WITH_MODEL en MAX_REFERENCES, minstens één. */
function productsPerItem(items: number, faces: number): number {
  const budget = Math.min(MAX_REFERENCES - faces, MAX_PRODUCT_REFS_WITH_MODEL);
  return Math.max(1, Math.min(2, Math.floor(budget / Math.max(1, items))));
}

/** "#1" of "#1-#4". */
const span = (from: number, to: number) => (from === to ? `#${from}` : `#${from}-#${to}`);
const sentence = (text: string) => `${text[0].toUpperCase()}${text.slice(1)}.`;

/** De ene lichtbron op hem: die van het shot, anders het standaardlicht van het model. Bij een detail het licht van de plek. */
function keyLight(shot: Shot): string {
  if (shot.framing === "detail") return `One motivated light source: ${shot.light}; his skin and the fabric share that same light.`;
  return shot.keyLight ?? MODEL.light;
}

export interface PromptOptions {
  aspect?: Aspect;
  /** Standaard 4k met het model in beeld (zijn gezicht moet scherp zijn), anders 2k. */
  resolution?: "2k" | "4k";
  /** Nodig voor shots die alle kleuren van een stuk tonen. */
  wardrobe?: WardrobeItem[];
  /** Standaard element; refs alleen als het element niet werkt (zie FaceMode). */
  faces?: FaceMode;
}

export function buildPrompt(look: Look, shot: Shot, opts: PromptOptions = {}): GenerationRequest {
  const main = subjectOf(look, shot, opts.wardrobe);
  const hasPerson = shot.people > 0;
  const detail = hasPerson && shot.framing === "detail";
  const viaRefs = opts.faces === "refs";
  const faces = faceReferences(shot, opts.faces);
  const k = faces.length;
  const { refs, index } = references([main], hasPerson ? productsPerItem(main.items.length, k) : 2, faces);
  const sketch = shot.render === "sketch";
  const palette = look.palette && shot.subject !== "line" ? ` Colour mood: ${look.palette.mood}.` : "";

  // Standaard brengt het element zijn gezicht; zijn gezicht wordt dan niet opnieuw in woorden beschreven (dat vecht met
  // het element). Alleen in de terugval zijn zijn gezichtsfoto's #1..#k, met identity_en erbij.
  const hisRefs = viaRefs
    ? ` His reference ${k === 1 ? "image is" : "images are"} ${span(1, k)}: use ${k === 1 ? "it" : "them"} only for him and ignore ${k === 1 ? "its" : "their"} clothing, light and setting.`
    : "";
  const him = viaRefs ? `the man in reference ${k === 1 ? "image" : "images"} ${span(1, k)}` : MODEL.elementPlaceholder;

  let subject: string;
  let wardrobe: string;
  if (hasPerson) {
    subject = detail
      ? `Subject: only part of him is visible (${shot.pose}); his face is out of frame. He is ${him}: the same skin tone, hands and build.${hisRefs}`
      : viaRefs
        ? `Subject: ${him}, ${MODEL.identity}. ${MODEL.keep}${hisRefs} Pose: ${shot.pose}.`
        : `Subject: ${him}. ${MODEL.keep} Pose: ${shot.pose}.`;
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
    "same number and position of buttons or zip, same pockets, same length and fit. Do not add, remove or redesign any detail." +
    (hasPerson
      ? refs.length === k + 1
        ? ` The garment reference (#${k + 1}) is only for the clothes: ignore any person or face in it.`
        : ` The garment references (${span(k + 1, refs.length)}) are only for the clothes: ignore any person or face in them.`
      : "");

  const feetInFrame = shot.framing === "full-body" || shot.subject === "lower";
  const feet = !hasPerson
    ? null
    : !feetInFrame
      ? "The feet are out of frame."
      : main.hasShoes
        ? "The loafers are worn sockless with bare ankles visible, a mirrored left and right pair."
        : "No shoes are part of this look: keep the feet out of frame.";

  // framing_en hoort bij locatiebeelden tot de taille of driekwart; niet bij de studio en niet bij ten voeten uit.
  const framing = hasPerson && !detail && shot.pillar !== "product" && shot.framing !== "full-body";
  const forbidden = [...FORBIDDEN, shot.publicPlace ? OTHER_PEOPLE.public : OTHER_PEOPLE.private];

  // Licht, uitsnede en uitdrukking vooraan, de kledingregels erachter. Met hem in beeld is er één lichtbron (keyLight),
  // dus geen tweede lichtbeschrijving in de Setting-regel.
  const prompt = [
    sketch ? "Photograph of a pencil fashion sketch." : `${FRAMING[shot.framing]}.`,
    hasPerson ? `Setting: ${shot.setting}. Camera: ${shot.camera}.` : `Setting: ${shot.setting}. Light: ${shot.light}. Camera: ${shot.camera}.`,
    subject,
    framing ? `Framing: ${MODEL.framing}.` : null,
    hasPerson ? keyLight(shot) : null,
    hasPerson && !detail ? `Expression: ${MODEL.expression}.` : null,
    hasPerson && !detail ? `For him: ${MODEL.mustNot.join("; ")}.` : null,
    shot.publicPlace ? sentence(MODEL.publicPlaces) : null,
    wardrobe,
    main.items.length > 1 ? layering(main) : null,
    fidelity,
    feet,
    `Absolutely none of the following may appear: ${forbidden.join(", ")}.`,
    sketch ? "Clean, calm, generous empty paper around the drawing." : `${CLEAN_LOOK}${palette} ${GRADE[shot.grade]}`,
    hasPerson ? MODEL.realism : null,
  ]
    .filter(Boolean)
    .join("\n\n");

  return {
    model: "nano_banana_pro",
    aspect: opts.aspect ?? "4:5",
    resolution: opts.resolution ?? (hasPerson ? "4k" : "2k"),
    prompt,
    references: refs,
  };
}

/** Reel van een goedgekeurd beeld: rustige beweging; het model, de kleding en de plek blijven exact gelijk. */
export function buildMotion(shot: Shot): VideoRequest {
  const person = shot.people > 0;
  const detail = person && shot.framing === "detail";
  const face = person && !detail;
  return {
    model: "seedance_2_5",
    mode: "omni_reference",
    startFrame: "approved-still",
    faceRefs: face ? MODEL.videoFaceRefs : [],
    aspect: "9:16",
    resolution: "1080p",
    bitrate: "high",
    duration: 5,
    audio: false,
    draftFirst: true,
    prompt: [
      `Start from the approved still: it is the first frame. Animate it: ${shot.motion}.`,
      detail
        ? "His face stays out of frame for the whole shot; keep the same skin tone, hands and build; the camera does not tilt up. No other man appears."
        : face
          ? "He is the man in the start frame and in the reference images; use the reference images only for his face and hair. " +
            "Keep exactly the same man, with the same face, hair, brows, eyes, jaw and build from the first frame to the last. " +
            "No other man appears. Small natural movement only: no head turn of more than 45 degrees, nothing passes in front of his face."
          : null,
      `Keep ${person ? "every garment, the loafers" : "every garment"}, the colours and the setting exactly as in the start frame: ` +
        "garments must not change colour, shape, length or details. No new objects, no accessories, no text, no new people; " +
        "anyone already far in the background stays small, out of focus and unchanged. " +
        "Real-time motion with natural motion blur, one continuous shot, no cuts, no zoom effects.",
    ]
      .filter(Boolean)
      .join(" "),
  };
}
