// Casting volgens de norm: één vast hoofdgezicht per hoofdstuk (35 tot 55, grijs mag), zoals Zegna met Mikkelsen
// en Cucinelli met een ervaren model naast jonge. Een tweede, jonger gezicht alleen voor beelden met twee mannen.
// Alleen mannen: ModernoMilano verkoopt alleen herenkleding.
// Staat er een Higgsfield Element-id in creative-engine/data/models.json, dan vervangt dat de beschrijving.

export interface Face {
  id: string;
  role: "main" | "second";
  description: string;
}

const COMMON = "natural skin texture, no jewellery, no tattoos, no piercings";

export const FACES: Face[] = [
  { id: "marco", role: "main", description: `a calm, handsome Italian man in his mid-forties, short dark hair greying at the temples, neatly trimmed salt-and-pepper beard, lean build, warm intelligent eyes, ${COMMON}` },
  { id: "alessandro", role: "main", description: `a composed Mediterranean man in his early fifties, swept-back silver-grey hair, short grey beard, tall and lean, weathered handsome face, ${COMMON}` },
  { id: "luca", role: "main", description: `a relaxed Mediterranean man in his late thirties, short dark curly hair, light stubble, athletic build, an easy genuine smile, ${COMMON}` },
  { id: "matteo", role: "second", description: `a Mediterranean man in his late twenties, short dark hair, clean-shaven, slim build, ${COMMON}` },
  { id: "karim", role: "second", description: `a man of North African heritage in his early thirties, short black hair, light beard, slim build, ${COMMON}` },
];

export interface Cast {
  main: Face;
  second: Face;
}

/** Kiest per hoofdstuk een vast hoofd- en tweede gezicht; dezelfde seed geeft dezelfde cast. */
export function castFor(seed: number, overrides: { main?: string; second?: string } = {}): Cast {
  const mains = FACES.filter((f) => f.role === "main");
  const seconds = FACES.filter((f) => f.role === "second");
  const pick = (list: Face[], override?: string) =>
    override ? { id: "element", role: list[0].role, description: override } : list[Math.abs(seed) % list.length];
  return { main: pick(mains, overrides.main), second: pick(seconds, overrides.second) };
}

/** Standaard hoofdgezicht als er geen cast is gekozen. */
export const DEFAULT_FACE = FACES[0].description;
