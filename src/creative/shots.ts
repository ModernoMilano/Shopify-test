// Shotlijst: de beeldtypes van de engine. Elk type is gebaseerd op wat de concurrenten laten zien
// (screenshots van hun raster, oktober 2026, en hun campagnes; zie creative-engine/research/2026-10-concurrenten.md).
// Alle shots delen dezelfde clean look; ze verschillen in kader, plek, licht en nabewerking.

import type { Season } from "./wardrobe";

export type Framing = "full-body" | "three-quarter" | "waist-up" | "detail" | "still-life";
export type Pillar = "product" | "editorial" | "craft" | "styling" | "world";
export type Aspect = "4:5" | "9:16" | "1:1" | "3:4";

/** Nabewerking. Studio is natuurgetrouw, locaties zijn gedempt filmisch, portretten soms zwart-wit (Cucinelli). */
export type Grade = "natural" | "muted-warm" | "muted-cool" | "bw";

/** Wat er in beeld komt: de hele look, alleen het hoofdstuk, alle kleuren van dat stuk, of alleen broek en loafers. */
export type Subject = "look" | "anchor" | "line" | "lower";

export interface Shot {
  id: string;
  name: string;
  pillar: Pillar;
  framing: Framing;
  season: Season;
  people: 0 | 1 | 2;
  subject: Subject;
  grade: Grade;
  setting: string;
  light: string;
  camera: string;
  pose: string;
  /** Beweging voor een reel van dit beeld (Kling, startframe = het goedgekeurde beeld). */
  motion: string;
  /** Een tekening in plaats van een foto (de schets van Cucinelli). */
  render?: "photo" | "sketch";
  inspiredBy: string[];
}

export const SHOTS: Shot[] = [
  // ---------- product ----------
  {
    id: "studio-full",
    name: "Studio, ten voeten uit",
    pillar: "product",
    framing: "full-body",
    season: "all",
    people: 1,
    subject: "look",
    grade: "natural",
    setting: "seamless warm off-white paper backdrop with a soft floor curve, completely empty studio",
    light: "large soft window-like key light from the left, gentle fill, a soft cast shadow on the floor behind the model",
    camera: "85mm lens at chest height, f/8, figure centred, entire figure in frame head to toe with generous space above and below",
    pose: "standing relaxed, weight on one leg, hands resting naturally at the sides or one hand loosely in a trouser pocket, looking slightly past the camera",
    motion: "he turns slowly a quarter to the side and back, the fabric settling naturally; static camera",
    inspiredBy: ["loropiana", "zegna"],
  },
  {
    id: "studio-portrait",
    name: "Studio, halflang",
    pillar: "product",
    framing: "three-quarter",
    season: "all",
    people: 1,
    subject: "look",
    grade: "natural",
    setting: "seamless warm grey backdrop, empty studio",
    light: "soft directional daylight from a high side window, subtle falloff into the background",
    camera: "85mm lens, f/4, framed from mid-thigh up, model slightly turned three-quarter to camera",
    pose: "calm, looking slightly past the camera, one hand adjusting a cuff",
    motion: "he slowly straightens his cuff and looks up; very slow push-in",
    inspiredBy: ["brunellocucinelli", "zegna"],
  },
  {
    id: "hanger",
    name: "Aan de hanger",
    pillar: "product",
    framing: "still-life",
    season: "all",
    people: 0,
    subject: "anchor",
    grade: "natural",
    setting: "the garment hanging on a plain light wooden hanger against a warm off-white lime-plaster wall, nothing else in frame",
    light: "soft window light from the side, a gentle shadow of the garment on the wall",
    camera: "50mm lens, straight on, the whole garment sharp with generous empty wall around it",
    pose: "no person; the garment hangs naturally, fully closed so collar, buttons or zip are clearly visible",
    motion: "the garment sways very gently as if touched by a breeze; static camera",
    inspiredBy: ["modernomilano", "loropiana"],
  },
  {
    id: "loafer-walk",
    name: "Loafers in beweging",
    pillar: "product",
    framing: "detail",
    season: "all",
    people: 1,
    subject: "lower",
    grade: "muted-warm",
    setting: "warm sunlit stone pavement of an empty Italian lane, a low stone step at the edge of the frame, no signs, no other people",
    light: "low warm afternoon sun from the side, long soft shadows, the suede nap catching the light",
    camera: "50mm lens at ankle height, framed from mid-calf down, shallow depth of field, the leading loafer sharp, background softly blurred",
    pose: "walking slowly mid-stride, bare ankles, sockless suede loafers, the hem of the trousers or shorts just visible",
    motion: "slow steady steps across the stone, real-time; camera follows at ankle height",
    inspiredBy: ["zegna", "loropiana", "boggimilanoofficial"],
  },

  // ---------- craft ----------
  {
    id: "texture",
    name: "Stof van dichtbij",
    pillar: "craft",
    framing: "detail",
    season: "all",
    people: 1,
    subject: "anchor",
    grade: "natural",
    setting: "neutral soft background, out of focus",
    light: "raking side light that reveals the knit structure, suede nap or weave",
    camera: "100mm macro lens, very shallow depth of field, crop on collar, placket, cuff or a hand touching the fabric, no face",
    pose: "a hand gently touching the fabric or adjusting the collar",
    motion: "fingers slowly run over the knit; very slow push-in",
    inspiredBy: ["loropiana", "brunellocucinelli", "modernomilano"],
  },
  {
    id: "folded-stack",
    name: "Alle kleuren gestapeld",
    pillar: "craft",
    framing: "still-life",
    season: "all",
    people: 0,
    subject: "line",
    grade: "natural",
    setting: "the colourways of this one piece folded and stacked, slightly fanned so each colour and the collar or zip show, on a pale travertine surface, nothing else",
    light: "soft natural daylight from a window, gentle shadows",
    camera: "45-degree angle, 85mm, close enough to see the stitch, generous empty space around the stack",
    pose: "no person",
    motion: "very slow lateral camera slide along the stack; light shifts softly",
    inspiredBy: ["modernomilano", "loropiana"],
  },
  {
    id: "sketch",
    name: "Schets",
    render: "sketch",
    pillar: "craft",
    framing: "still-life",
    season: "all",
    people: 0,
    subject: "anchor",
    grade: "natural",
    setting: "a fine graphite pencil fashion sketch of the garment on off-white drawing paper on a wooden table, a pencil lying beside it, nothing else",
    light: "soft daylight from a window",
    camera: "top-down, 50mm, the whole sheet sharp",
    pose: "no person; the sketch shows the garment's real collar, buttons or zip, pockets and proportions, with no writing, no labels and no logo on the paper",
    motion: "a hand enters and adds a few soft pencil strokes of shading; static camera",
    inspiredBy: ["brunellocucinelli", "loropiana"],
  },
  {
    id: "still-life",
    name: "Still life",
    pillar: "craft",
    framing: "still-life",
    season: "all",
    people: 0,
    subject: "look",
    grade: "natural",
    setting: "the garments neatly folded and stacked on a travertine slab, loafers placed beside them if part of the look, a sprig of dried olive branch at most, nothing else",
    light: "soft natural daylight from a window, gentle shadows",
    camera: "top-down or 45-degree angle, 50mm, everything sharp, generous empty space around the objects",
    pose: "no person",
    motion: "very slow push-in; sunlight moves slightly across the stack",
    inspiredBy: ["loropiana", "zegna"],
  },

  // ---------- styling ----------
  {
    id: "look-flatlay",
    name: "Flatlay van de look",
    pillar: "styling",
    framing: "still-life",
    season: "all",
    people: 0,
    subject: "look",
    grade: "natural",
    setting: "one complete outfit laid out flat as if worn, on a warm pale linen or travertine surface: top layer, under layer, trousers or shorts, suede loafers at the bottom, nothing else",
    light: "soft even daylight from a large window, very gentle shadows",
    camera: "straight top-down, 35mm, everything sharp, every garment fully visible with even spacing and generous empty margin",
    pose: "no person; garments arranged neatly, sleeves relaxed, cardigan or blazer slightly open to show the layer underneath",
    motion: "very slow top-down push-in",
    inspiredBy: ["boggimilanoofficial"],
  },

  // ---------- editorial ----------
  {
    id: "architecture",
    name: "Stille architectuur",
    pillar: "editorial",
    framing: "full-body",
    season: "all",
    people: 1,
    subject: "look",
    grade: "muted-cool",
    setting: "minimalist modernist architecture: travertine floor, pale lime-plaster or dark concrete walls, a single wide opening onto landscape, no furniture, no signage, nobody else present",
    light: "soft overcast daylight with long gentle shadows, calm and quiet atmosphere",
    camera: "50mm lens, eye level, figure placed off-centre with wide negative space around him",
    pose: "walking slowly through the space, mid-stride, looking ahead and away from the camera",
    motion: "he walks slowly through the space, real-time; static camera",
    inspiredBy: ["loropiana", "brunellocucinelli"],
  },
  {
    id: "milano-courtyard",
    name: "Milanese binnenplaats",
    pillar: "editorial",
    framing: "three-quarter",
    season: "all",
    people: 1,
    subject: "look",
    grade: "muted-warm",
    setting: "quiet Milanese palazzo courtyard with long stone arcades and an old wooden door, empty, no cars, no shop signs, no readable text anywhere",
    light: "late-afternoon sun bouncing off warm stone, soft and golden, arcade columns casting long soft shadows",
    camera: "50mm lens, framed from the knees up, arcades receding in soft focus behind him",
    pose: "walking slowly under the arcade, mid-stride, glancing to the side, one hand relaxed",
    motion: "he walks slowly under the arcade toward the camera, real-time; camera drifts back slowly",
    inspiredBy: ["zegna", "boggimilanoofficial"],
  },
  {
    id: "volcanic-coast",
    name: "Zwarte kust",
    pillar: "editorial",
    framing: "full-body",
    season: "fw",
    people: 1,
    subject: "look",
    grade: "muted-cool",
    setting: "wide empty black volcanic sand beach at the waterline, a soft white curve of surf, grey sea and sky, no buildings, nobody else",
    light: "flat soft overcast daylight, cool and quiet",
    camera: "35mm lens, figure about a third of the frame height, off-centre, generous sky and sand around him",
    pose: "walking slowly along the shoreline, one hand in a pocket, looking out to sea, not at the camera",
    motion: "he walks slowly along the waterline, surf rolling in softly; static camera",
    inspiredBy: ["brunellocucinelli"],
  },
  {
    id: "borgo",
    name: "Italiaans dorp",
    pillar: "editorial",
    framing: "three-quarter",
    season: "all",
    people: 1,
    subject: "look",
    grade: "muted-warm",
    setting: "sunlit stone lane in a small Umbrian hill village with an olive tree and a low stone wall, empty street",
    light: "warm afternoon sun softened by the stone, relaxed and human",
    camera: "50mm lens, framed from the knees up, background softly out of focus",
    pose: "a natural warm smile, glancing to the side as if greeting someone out of frame, one hand in a pocket",
    motion: "he walks a few slow steps up the lane and smiles; static camera",
    inspiredBy: ["brunellocucinelli"],
  },
  {
    id: "lake-terrace",
    name: "Balustrade aan het water",
    pillar: "editorial",
    framing: "waist-up",
    season: "all",
    people: 1,
    subject: "look",
    grade: "muted-warm",
    setting: "stone balustrade terrace above a calm north-Italian lake or the sea, soft hills across the water, nobody else present",
    light: "soft morning light with a light haze, muted and serene",
    camera: "85mm lens, framed from the waist up, water softly blurred behind",
    pose: "leaning forearms on the balustrade, calm gaze across the water",
    motion: "he looks out over the water and slowly turns his head; light haze drifts",
    inspiredBy: ["zegna", "loropiana", "modernomilano"],
  },
  {
    id: "interior",
    name: "Bewoond interieur",
    pillar: "editorial",
    framing: "full-body",
    season: "all",
    people: 1,
    subject: "look",
    grade: "muted-warm",
    setting: "warm lived-in villa sitting room: oak floor, linen armchair, a low stack of plain books with blank linen spines, travertine side table with a single plain white espresso cup, tall window onto a green garden, nothing else",
    light: "soft window light from the side, warm and intimate, gentle shadows",
    camera: "35mm lens, seated figure fully in frame including the feet, window and garden softly visible",
    pose: "seated with one ankle resting on the knee, looking out of the window, one hand resting on the armrest, relaxed and unposed",
    motion: "he lifts the espresso cup slowly and looks out of the window; static camera",
    inspiredBy: ["loropiana", "brunellocucinelli", "boggimilanoofficial"],
  },
  {
    id: "library-fireside",
    name: "Bibliotheek bij het vuur",
    pillar: "editorial",
    framing: "three-quarter",
    season: "fw",
    people: 1,
    subject: "look",
    grade: "muted-warm",
    setting: "wood-panelled library room with a stone fireplace and a low fire, a worn tan leather armchair, a wooden chess table with a game in progress, shelves of books with plain unreadable spines, nobody else",
    light: "soft low window light mixed with warm firelight, intimate and calm, deep but gentle shadows",
    camera: "50mm lens, framed from the knees up, fireplace and shelves softly out of focus behind",
    pose: "seated on the arm of the leather chair, looking down at the chessboard, one hand resting on the knee",
    motion: "he moves one chess piece slowly; the fire flickers softly; static camera",
    inspiredBy: ["boggimilanoofficial", "loropiana"],
  },
  {
    id: "riviera",
    name: "Stenen kade",
    pillar: "editorial",
    framing: "three-quarter",
    season: "ss",
    people: 1,
    subject: "look",
    grade: "muted-warm",
    setting: "sun-bleached stone jetty on a calm turquoise Ligurian bay, a white stone village far behind across the water, no boats, no signs, nobody else",
    light: "bright clean summer sun, soft reflections from the water",
    camera: "50mm lens, framed from the knees up, sea softly out of focus behind",
    pose: "sitting on the edge of the stone jetty, relaxed, looking toward the sea",
    motion: "he looks out to sea, the water glitters softly; static camera",
    inspiredBy: ["loropiana", "boggimilanoofficial", "brunellocucinelli"],
  },

  // ---------- world ----------
  {
    id: "landscape",
    name: "Weids landschap",
    pillar: "world",
    framing: "full-body",
    season: "fw",
    people: 1,
    subject: "look",
    grade: "muted-cool",
    setting: "wide alpine meadow in early autumn with a soft mountain ridge on the horizon, no paths, no buildings, no other people",
    light: "golden hour, low warm sun, light haze",
    camera: "35mm lens, the figure at least a quarter of the frame height, vast landscape around him",
    pose: "standing still and looking out over the valley, hands relaxed",
    motion: "grass moves in the wind, he stands still; very slow push-in",
    inspiredBy: ["zegna"],
  },
  {
    id: "snowfield",
    name: "Sneeuwveld",
    pillar: "world",
    framing: "full-body",
    season: "fw",
    people: 1,
    subject: "look",
    grade: "muted-cool",
    setting: "vast snowfield streaked with dark volcanic rock below a pale mountain, no tracks, no buildings, nobody else",
    light: "bright soft overcast daylight, cool and clean",
    camera: "35mm lens, the figure at least a quarter of the frame height, off-centre, wide pale sky",
    pose: "standing still facing the mountain, hands relaxed, looking away from the camera",
    motion: "fine snow drifts across the ground, he stands still; static camera",
    inspiredBy: ["brunellocucinelli", "modernomilano"],
  },
  {
    id: "island-coast",
    name: "Eilandkust",
    pillar: "world",
    framing: "full-body",
    season: "ss",
    people: 1,
    subject: "look",
    grade: "muted-warm",
    setting: "wild Mediterranean island coast of dark volcanic rock and low dry shrubs above a calm deep-blue sea, a narrow stone path, no buildings, no boats, nobody else",
    light: "warm late-afternoon sun, slight sea haze, sand and sky tones",
    camera: "35mm lens, full figure including the loafers, figure about a third of the frame height, sea and sky around him",
    pose: "walking slowly along the rock path toward the camera, hands relaxed",
    motion: "he walks slowly toward the camera, shirt moving in the breeze; static camera",
    inspiredBy: ["boggimilanoofficial", "brunellocucinelli", "loropiana"],
  },
  {
    id: "espresso-terrace",
    name: "Espresso op het plein",
    pillar: "world",
    framing: "waist-up",
    season: "all",
    people: 1,
    subject: "look",
    grade: "muted-warm",
    setting: "small round marble table on an empty stone terrace of an Italian town square in the morning, one plain white porcelain espresso cup and saucer, no logos, no signs, no other people",
    light: "clear soft morning sun from the side, warm stone tones, gentle shadows",
    camera: "85mm lens, framed from the waist up, seated at the table, square softly blurred behind",
    pose: "seated, lifting the espresso cup with one hand, glance resting on the square, calm half-smile",
    motion: "he lifts the cup slowly and sets it down; static camera",
    inspiredBy: ["zegna", "brunellocucinelli"],
  },
  {
    id: "bw-portrait",
    name: "Portret in zwart-wit",
    pillar: "world",
    framing: "waist-up",
    season: "all",
    people: 1,
    subject: "look",
    grade: "bw",
    setting: "outdoors against a soft misty background, empty",
    light: "soft diffuse daylight, gentle contrast",
    camera: "85mm lens, close portrait from the chest up, the collar and knit clearly visible",
    pose: "leaning forward slightly, looking down and away, calm and contemplative",
    motion: "he slowly raises his gaze toward the camera; very slow push-in",
    inspiredBy: ["brunellocucinelli"],
  },
  {
    id: "two-generations",
    name: "Twee generaties",
    pillar: "world",
    framing: "full-body",
    season: "all",
    people: 2,
    subject: "look",
    grade: "muted-warm",
    setting: "quiet stone courtyard of an old Italian villa with a single olive tree, empty apart from the two men",
    light: "soft late-afternoon daylight, warm and calm",
    camera: "50mm lens, both figures fully in frame including the loafers, natural distance between them",
    pose: "the older man gently straightens the collar or lapel of the younger man, both calm and quietly smiling",
    motion: "the older man adjusts the collar and steps back; both smile; static camera",
    inspiredBy: ["zegna", "brunellocucinelli", "loropiana"],
  },
];

const CAMERA_FOR: Partial<Record<Framing, string>> = {
  "waist-up": "85mm lens, framed from the waist up, same place and light, background softly out of focus",
  detail: "100mm macro lens, very shallow depth of field, crop on collar, placket, cuff or fabric, no face",
};

/** Een tweede beeld uit dezelfde shoot (voor een carrousel): zelfde plek en licht, ander kader. */
export function deriveShot(shot: Shot, framing: Extract<Framing, "waist-up" | "detail">): Shot {
  return {
    ...shot,
    id: `${shot.id}~${framing}`,
    name: `${shot.name} (${framing === "detail" ? "detail" : "halflang"})`,
    framing,
    people: shot.people === 2 ? 1 : shot.people,
    subject: framing === "detail" ? "anchor" : shot.subject,
    camera: CAMERA_FOR[framing]!,
    pose: framing === "detail" ? "a hand resting on or adjusting the garment" : shot.pose,
  };
}

export function shotById(id: string): Shot {
  const s = SHOTS.find((x) => x.id === id);
  if (!s) throw new Error(`Onbekend shot: ${id}`);
  return s;
}

export function shotsFor(opts: { season: Exclude<Season, "all">; hasShoes: boolean; pillar?: Pillar; people?: number }): Shot[] {
  return SHOTS.filter(
    (s) =>
      (s.season === "all" || s.season === opts.season) &&
      (opts.hasShoes || s.framing !== "full-body") &&
      (!opts.pillar || s.pillar === opts.pillar) &&
      s.people <= (opts.people ?? 1),
  );
}
