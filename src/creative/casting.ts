// Het vaste model van ModernoMilano (sinds 8 oktober 2026): één man in elke foto en elke video.
// Nooit een andere man en nooit twee mannen in één beeld. Alleen mannen: ModernoMilano verkoopt alleen herenkleding.
// Bron van waarheid: creative-engine/data/model.json. Uitleg: creative-engine/brand/model.md.
// Ontbreekt er iets in model.json, dan stopt de engine meteen met een duidelijke fout.

import modelJson from "../../creative-engine/data/model.json";

export interface FaceRef {
  /** "ref-1" t/m "ref-4", de bestandsnaam zonder extensie. */
  id: string;
  /** Pad in de repo, bv. creative-engine/brand/assets/model/ref-1.jpg. */
  file: string;
  /** Higgsfield media_id van het geïmporteerde originele bestand (klein, 208-348 px breed). */
  mediaId: string;
  /** Higgsfield-job van de 4K-versie. Die gaat mee in de terugval zonder element. */
  upscaleJobId: string;
  view: string;
}

export interface Model {
  id: string;
  /** Alleen intern, om naar hem te verwijzen. Komt nooit in een prompt of caption. */
  name: string;
  identity: string;
  keep: string;
  mustNot: string[];
  realism: string;
  light: string;
  expression: string;
  framing: string;
  publicPlaces: string;
  elementId: string;
  /** `<<<element_id>>>`: Higgsfield voegt dan zelf zijn gezicht toe. */
  elementPlaceholder: string;
  soulId: string;
  faceRefs: FaceRef[];
  /**
   * Alleen voor de terugval zonder element: de gezichtsfoto's die als eerste referenties meegaan, in vaste volgorde
   * (model.json → face_ref_order: ref-1, ref-4, ref-2). Standaard gaan er geen gezichtsfoto's mee; het element brengt zijn gezicht.
   */
  fallbackFaceRefs: FaceRef[];
  /** Maximaal zoveel beelden per batch, daarna eerst controleren. */
  batchMax: number;
  /** Minimale breedte van zijn gezicht in het eindbeeld. */
  faceMinPx: number;
}

/** De vorm van creative-engine/data/model.json, voor zover de engine hem gebruikt. */
export interface ModelFile {
  id?: string;
  name?: string;
  higgsfield?: {
    element_id?: string;
    element_placeholder?: string;
    soul_id?: string;
    face_refs?: { file?: string; media_id?: string; upscale_job_id?: string; view?: string }[];
    face_ref_order?: string[];
  };
  prompt?: {
    identity_en?: string;
    keep_en?: string;
    must_not_en?: string[];
    realism_en?: string;
    light_default_en?: string;
    expression_en?: string;
    framing_en?: string;
    public_places_en?: string;
  };
  rules?: { batch_max?: number; face_min_px?: number };
}

function need<T>(value: T | undefined | null, key: string): T {
  if (value === undefined || value === null || (typeof value === "string" && value.trim() === "")) {
    throw new Error(`creative-engine/data/model.json mist ${key}`);
  }
  return value;
}

/** Leest het model uit model.json en controleert dat alles erin staat. */
export function modelFrom(data: ModelFile): Model {
  const hf = need(data.higgsfield, "higgsfield");
  const p = need(data.prompt, "prompt");
  const elementId = need(hf.element_id, "higgsfield.element_id");
  const elementPlaceholder = need(hf.element_placeholder, "higgsfield.element_placeholder");
  if (elementPlaceholder !== `<<<${elementId}>>>`) {
    throw new Error(`creative-engine/data/model.json: element_placeholder hoort <<<${elementId}>>> te zijn`);
  }
  const refs = need(hf.face_refs, "higgsfield.face_refs");
  if (refs.length === 0) throw new Error("creative-engine/data/model.json mist higgsfield.face_refs");
  const faceRefs = refs.map((r, i): FaceRef => {
    const file = need(r.file, `higgsfield.face_refs[${i}].file`);
    return {
      id: file.replace(/^.*\//, "").replace(/\.[a-z]+$/i, ""),
      file,
      mediaId: need(r.media_id, `higgsfield.face_refs[${i}].media_id`),
      upscaleJobId: need(r.upscale_job_id, `higgsfield.face_refs[${i}].upscale_job_id`),
      view: r.view ?? "",
    };
  });
  const order = need(hf.face_ref_order, "higgsfield.face_ref_order");
  if (order.length === 0) throw new Error("creative-engine/data/model.json mist higgsfield.face_ref_order");
  const fallbackFaceRefs = order.map((id) => {
    const ref = faceRefs.find((r) => r.id === id);
    if (!ref) throw new Error(`creative-engine/data/model.json: face_ref_order noemt ${id}, maar die staat niet in face_refs`);
    return ref;
  });
  const mustNot = need(p.must_not_en, "prompt.must_not_en");
  if (mustNot.length === 0) throw new Error("creative-engine/data/model.json mist prompt.must_not_en");

  return {
    id: need(data.id, "id"),
    name: need(data.name, "name"),
    identity: need(p.identity_en, "prompt.identity_en"),
    keep: need(p.keep_en, "prompt.keep_en"),
    mustNot,
    realism: need(p.realism_en, "prompt.realism_en"),
    light: need(p.light_default_en, "prompt.light_default_en"),
    expression: need(p.expression_en, "prompt.expression_en"),
    framing: need(p.framing_en, "prompt.framing_en"),
    publicPlaces: need(p.public_places_en, "prompt.public_places_en"),
    elementId,
    elementPlaceholder,
    soulId: need(hf.soul_id, "higgsfield.soul_id"),
    faceRefs,
    fallbackFaceRefs,
    batchMax: data.rules?.batch_max ?? 12,
    faceMinPx: data.rules?.face_min_px ?? 500,
  };
}

/** Het enige model. Elke foto en video met een persoon gebruikt hem. */
export const MODEL: Model = modelFrom(modelJson);
