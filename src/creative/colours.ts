// Kleuren van ModernoMilano: elke kleurnaam uit een producttitel valt in één familie.
// Paletten zijn de toegestane combinaties (quiet luxury: tonaal, maximaal drie families per look).

export type ColourFamily =
  | "black"
  | "charcoal"
  | "grey"
  | "white"
  | "cream"
  | "beige"
  | "taupe"
  | "camel"
  | "brown"
  | "navy"
  | "blue"
  | "green"
  | "red";

/** Kleurnaam (zoals in de titel, hoofdletters) → familie. */
const COLOUR_WORDS: Record<string, ColourFamily> = {
  BLACK: "black", NERO: "black", ONYX: "black", ONICE: "black",
  ANTRACITE: "charcoal", GRAFITE: "charcoal", CHARCOAL: "charcoal", "DARK GREY": "charcoal", FUMO: "charcoal",
  GREY: "grey", GRAY: "grey", GRIGIO: "grey", "LIGHT GREY": "grey", "LIGHT GRAY": "grey", ARGENTO: "grey", PERLA: "grey",
  WHITE: "white", "OFF WHITE": "white", GHIACCIO: "white",
  IVORY: "cream", AVORIO: "cream", PANNA: "cream", CHAMPAGNE: "cream",
  BEIGE: "beige", SAND: "beige", SABBIA: "beige", "SAND BEIGE": "beige", "STONE BEIGE": "beige", AVENA: "beige", "LIGHT KHAKI": "beige", DUNA: "beige",
  TAUPE: "taupe", TORTORA: "taupe", "TAUPE BROWN": "taupe",
  CAMEL: "camel", CAMMELLO: "camel", NOCCIOLA: "camel", TABACCO: "camel",
  BROWN: "brown", MORO: "brown", ESPRESSO: "brown", "DARK MOCHA": "brown", TERRA: "brown", TERRACOTE: "brown",
  NAVY: "navy", NOTTE: "navy", MIDNIGHT: "navy", NOTTURNO: "navy",
  BLUE: "blue", "LIGHT BLUE": "blue", CELESTE: "blue", "DENIM BLUE": "blue", AVIO: "blue", "GRAY BLUE": "blue", AZZURRO: "blue",
  GREEN: "green", OLIVA: "green", OLIVE: "green", "FOREST GREEN": "green", OTTANIO: "green",
  BURGUNDY: "red", BORDEAUX: "red", ROSSO: "red",
};

/** Benaderde kleur voor previews en moodboards. */
export const FAMILY_HEX: Record<ColourFamily, string> = {
  black: "#1c1c1c", charcoal: "#3d3d3f", grey: "#9a9a98", white: "#f4f3ef", cream: "#ece3d2",
  beige: "#d6c6a8", taupe: "#9c8b7a", camel: "#b08a5a", brown: "#5b4033", navy: "#1f2a44",
  blue: "#7d93b2", green: "#5d6a4a", red: "#6e2a32",
};

/** Engelse omschrijving voor in de beeldprompt. */
export const FAMILY_WORDS: Record<ColourFamily, string> = {
  black: "black", charcoal: "charcoal grey", grey: "light grey", white: "white", cream: "ivory cream",
  beige: "sand beige", taupe: "taupe", camel: "camel", brown: "dark brown", navy: "navy",
  blue: "soft blue", green: "olive green", red: "burgundy",
};

export function colourFamily(word: string | null | undefined): ColourFamily | null {
  if (!word) return null;
  return COLOUR_WORDS[word.trim().toUpperCase()] ?? null;
}

/** Zoekt een bekend kleurwoord in een titel zonder " - KLEUR" (bv. "MILANO REVERSO SABBIA SET"). */
export function colourWordInTitle(title: string): string | null {
  const upper = title.toUpperCase();
  const words = Object.keys(COLOUR_WORDS).sort((a, b) => b.length - a.length);
  return words.find((w) => new RegExp(`\\b${w}\\b`).test(upper)) ?? null;
}

export interface Palette {
  id: string;
  name: string;
  families: ColourFamily[];
  mood: string;
}

/** Paletten afgeleid van wat Loro Piana, Zegna, Cucinelli en Boggi laten zien. */
export const PALETTES: Palette[] = [
  { id: "sabbia", name: "Tonaal zand", families: ["beige", "cream", "taupe", "camel", "white"], mood: "warm tonal sand and ivory, sun-washed, Cucinelli-like softness" },
  { id: "terra", name: "Terra", families: ["brown", "camel", "beige", "cream", "taupe"], mood: "earthy browns and camel lifted by ivory, autumnal and grounded" },
  { id: "grigio", name: "Grigio Milano", families: ["grey", "charcoal", "white", "black"], mood: "cool urban greys, architectural, precise" },
  { id: "notte", name: "Notte", families: ["navy", "cream", "white", "grey", "blue"], mood: "deep navy with ivory and soft blue, crisp and nautical" },
  { id: "nero", name: "Nero assoluto", families: ["black", "charcoal", "white"], mood: "monochrome black, evening, graphic and calm" },
  { id: "oliva", name: "Oliva", families: ["green", "beige", "brown", "cream"], mood: "olive and sand, countryside and alpine calm" },
  // Eén accent per look op een aardse basis (Cucinelli FW25 bordeaux, Loro Piana-lookbook met één kleur).
  { id: "bordeaux", name: "Bordeaux", families: ["red", "brown", "camel", "cream", "charcoal"], mood: "one deep bordeaux accent on earthy browns, camel and cream" },
];

export function paletteFits(palette: Palette, families: ColourFamily[]): boolean {
  return families.every((f) => palette.families.includes(f));
}

/** Welke loaferkleuren tonaal bij een outfitkleur passen, beste eerst. */
export const SHOE_PAIRING: Record<ColourFamily, ColourFamily[]> = {
  black: ["black", "charcoal"],
  charcoal: ["black", "grey"],
  grey: ["grey", "black"],
  white: ["beige", "grey", "camel"],
  cream: ["beige", "camel", "brown"],
  beige: ["beige", "camel", "brown"],
  taupe: ["brown", "camel", "beige"],
  camel: ["camel", "brown"],
  brown: ["brown", "camel"],
  navy: ["navy", "blue", "brown"],
  blue: ["navy", "blue", "beige"],
  green: ["brown", "camel", "beige"],
  red: ["brown", "black"],
};
