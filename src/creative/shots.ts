// Shotlijst: de beeldtypes van de engine, elk afgeleid van wat de vier concurrenten goed doen.
// Alle shots delen dezelfde clean look; ze verschillen in kader, plek en licht.

import type { Season } from "./wardrobe";

export type Framing = "full-body" | "three-quarter" | "waist-up" | "detail" | "still-life";
export type Pillar = "product" | "editorial" | "craft" | "styling" | "world";
export type Aspect = "4:5" | "9:16" | "1:1" | "3:4";

export interface Shot {
  id: string;
  name: string;
  pillar: Pillar;
  framing: Framing;
  season: Season;
  people: 0 | 1 | 2;
  setting: string;
  light: string;
  camera: string;
  pose: string;
  inspiredBy: string[];
}

export const SHOTS: Shot[] = [
  {
    id: "studio-full",
    name: "Studio, ten voeten uit",
    pillar: "product",
    framing: "full-body",
    season: "all",
    people: 1,
    setting: "seamless warm off-white paper backdrop with a soft floor curve, completely empty studio",
    light: "large soft window-like key light from the left, gentle fill, soft natural shadow on the floor",
    camera: "85mm lens at chest height, f/8, entire figure in frame head to toe with generous space above and below",
    pose: "standing relaxed, weight on one leg, hands resting naturally at the sides or one hand loosely in a trouser pocket",
    inspiredBy: ["loropiana", "zegna"],
  },
  {
    id: "studio-portrait",
    name: "Studio, halflang",
    pillar: "product",
    framing: "three-quarter",
    season: "all",
    people: 1,
    setting: "seamless warm grey backdrop, empty studio",
    light: "soft directional daylight from a high side window, subtle falloff into the background",
    camera: "85mm lens, f/4, framed from mid-thigh up, model slightly turned three-quarter to camera",
    pose: "calm, looking slightly past the camera, one hand adjusting a cuff",
    inspiredBy: ["brunellocucinelli", "zegna"],
  },
  {
    id: "architecture",
    name: "Stille architectuur",
    pillar: "editorial",
    framing: "full-body",
    season: "all",
    people: 1,
    setting: "minimalist modernist architecture: travertine floor, pale lime-plaster walls, a single wide doorway, no furniture, no signage, nobody else present",
    light: "soft overcast daylight with long gentle shadows, calm and quiet atmosphere",
    camera: "50mm lens, eye level, figure placed off-centre with wide negative space of wall around him",
    pose: "walking slowly through the space, mid-stride, unposed and natural",
    inspiredBy: ["loropiana"],
  },
  {
    id: "milano-courtyard",
    name: "Milanese binnenplaats",
    pillar: "editorial",
    framing: "three-quarter",
    season: "all",
    people: 1,
    setting: "quiet Milanese palazzo courtyard with stone arcades and an old wooden door, empty, no cars, no shop signs",
    light: "late-afternoon sun bouncing off warm stone, soft and golden",
    camera: "50mm lens, framed from knees up, arcades softly out of focus behind",
    pose: "leaning lightly against a stone column, relaxed, looking away from camera",
    inspiredBy: ["boggimilanoofficial", "zegna"],
  },
  {
    id: "landscape",
    name: "Weids landschap",
    pillar: "world",
    framing: "full-body",
    season: "fw",
    people: 1,
    setting: "wide alpine meadow in early autumn with a soft mountain ridge on the horizon, no paths, no buildings, no other people",
    light: "golden hour, low warm sun, light haze",
    camera: "35mm lens, figure small in the frame (about a quarter of the height), vast landscape around him",
    pose: "standing still and looking out over the valley, hands relaxed",
    inspiredBy: ["zegna"],
  },
  {
    id: "borgo",
    name: "Italiaans dorp",
    pillar: "editorial",
    framing: "three-quarter",
    season: "all",
    people: 1,
    setting: "sunlit stone lane in a small Umbrian hill village with an olive tree and a low stone wall, empty street",
    light: "warm midday-to-afternoon sun softened by the stone, relaxed and human",
    camera: "50mm lens, framed from knees up, background softly out of focus",
    pose: "natural smile, mid-conversation glance to the side, one hand in pocket",
    inspiredBy: ["brunellocucinelli"],
  },
  {
    id: "lake-terrace",
    name: "Terras aan het meer",
    pillar: "editorial",
    framing: "waist-up",
    season: "all",
    people: 1,
    setting: "stone balustrade terrace above a calm north-Italian lake, misty hills across the water, nobody else present",
    light: "soft morning light with light mist, muted and serene",
    camera: "85mm lens, framed from the waist up, lake softly blurred behind",
    pose: "leaning forearms on the balustrade, calm gaze across the water",
    inspiredBy: ["loropiana", "zegna"],
  },
  {
    id: "interior",
    name: "Rustig interieur",
    pillar: "editorial",
    framing: "full-body",
    season: "fw",
    people: 1,
    setting: "minimalist warm interior: linen armchair, oak floor, travertine side table with a single espresso cup, large window, nothing else",
    light: "soft window light from the side, warm and intimate",
    camera: "35mm lens, seated figure fully in frame including the feet",
    pose: "seated with one ankle resting on the knee, relaxed, hands resting on the armrests",
    inspiredBy: ["brunellocucinelli", "loropiana"],
  },
  {
    id: "riviera",
    name: "Riviera",
    pillar: "editorial",
    framing: "three-quarter",
    season: "ss",
    people: 1,
    setting: "teak deck of a classic wooden boat moored on a calm turquoise Ligurian bay, white stone village far behind, nobody else",
    light: "bright clean summer sun, soft reflections from the water",
    camera: "50mm lens, framed from knees up",
    pose: "sitting on the edge of the deck, relaxed, looking toward the sea",
    inspiredBy: ["boggimilanoofficial", "loropiana"],
  },
  {
    id: "texture",
    name: "Stof van dichtbij",
    pillar: "craft",
    framing: "detail",
    season: "all",
    people: 1,
    setting: "neutral soft background, out of focus",
    light: "raking side light that reveals the knit structure, suede nap or weave",
    camera: "100mm macro lens, very shallow depth of field, crop on collar, placket, cuff or hand touching the fabric, no face",
    pose: "hand gently touching the fabric or adjusting the collar",
    inspiredBy: ["loropiana", "brunellocucinelli"],
  },
  {
    id: "still-life",
    name: "Still life",
    pillar: "craft",
    framing: "still-life",
    season: "all",
    people: 0,
    setting: "the garments neatly folded and stacked on a travertine slab, loafers placed beside them if part of the look, a sprig of dried olive branch at most, nothing else",
    light: "soft natural daylight from a window, gentle shadows",
    camera: "top-down or 45-degree angle, 50mm, everything sharp, generous empty space around the objects",
    pose: "no person",
    inspiredBy: ["loropiana", "zegna"],
  },
  {
    id: "two-generations",
    name: "Twee generaties",
    pillar: "world",
    framing: "full-body",
    season: "all",
    people: 2,
    setting: "quiet stone courtyard or minimalist architecture, empty apart from the two men",
    light: "soft overcast daylight",
    camera: "50mm lens, both figures fully in frame, natural distance between them",
    pose: "father in his late fifties and son in his late twenties walking side by side, relaxed conversation",
    inspiredBy: ["zegna", "loropiana"],
  },
];

export function shotsFor(opts: { season: Exclude<Season, "all">; hasShoes: boolean; pillar?: Pillar }): Shot[] {
  return SHOTS.filter(
    (s) =>
      (s.season === "all" || s.season === opts.season) &&
      (opts.hasShoes || s.framing !== "full-body") &&
      (!opts.pillar || s.pillar === opts.pillar) &&
      s.people < 2,
  );
}
