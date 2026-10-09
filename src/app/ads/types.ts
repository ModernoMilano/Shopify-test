export type AdCollection = "Cashmere" | "Reverso" | "Bundle & Save" | "Other";

/** Eén advertentie: een Higgsfield-beeld met de copy die erbij geschreven is. */
export type Ad = {
  id: string;
  image: string;
  thumb: string;
  aspect: string;
  created: string;
  collection: AdCollection;
  product: string;
  price: string;
  scene: string;
  angle: string;
  hookType: string;
  hook: string;
  primaryText: string;
  headline: string;
  description: string;
  cta: string;
  placement: "Feed" | "Stories/Reels";
  /** Tekst die op het beeld zelf staat en gecontroleerd moet worden (korting, prijs, claim). */
  warning?: string;
};
