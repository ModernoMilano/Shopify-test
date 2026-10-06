// Kwaliteitscontrole na het genereren. Een beeld gaat pas door als niets erin buiten de look valt.
// Claude bekijkt elk beeld, vult een Observation in en deze functie beslist: goedgekeurd of afgekeurd.

import type { Look } from "./looks";
import type { Shot } from "./shots";

export interface Observation {
  /** Elk zichtbaar kledingstuk of schoen, in gewone woorden ("navy knit polo", "beige trousers"). */
  garments: string[];
  /** Per product uit de look: komt het overeen met de referentie (kleur, structuur, kraag, knopen)? */
  matches: Record<string, boolean>;
  /** Alles wat geen kledingstuk is maar wel gedragen wordt: horloge, riem, zonnebril... */
  accessories: string[];
  logosOrText: boolean;
  people: number;
  feetVisible: boolean;
  socksVisible: boolean;
  /** Clean look: rustige achtergrond, zacht licht, maximaal drie kleurfamilies. */
  clean: boolean;
  /** Anatomie: handen, vingers, gezicht zonder AI-fouten. */
  anatomyOk: boolean;
  notes?: string;
}

export interface Verdict {
  approved: boolean;
  reasons: string[];
}

export function judge(look: Look, shot: Shot, obs: Observation): Verdict {
  const reasons: string[] = [];
  const expected = look.items.flatMap((x) => (x.item.isSet ? x.item.pieces.map(() => x.item.title) : [x.item.title]));

  for (const { item } of look.items) {
    if (obs.matches[item.title] === false) reasons.push(`${item.title} wijkt af van de productfoto`);
    if (obs.matches[item.title] === undefined) reasons.push(`${item.title} is niet beoordeeld`);
  }
  if (obs.garments.length > expected.length) {
    reasons.push(`meer zichtbare kledingstukken (${obs.garments.length}) dan in de look (${expected.length}): ${obs.garments.join(", ")}`);
  }
  if (obs.accessories.length) reasons.push(`accessoires die we niet verkopen: ${obs.accessories.join(", ")}`);
  if (obs.logosOrText) reasons.push("logo, label of tekst zichtbaar");
  if (obs.people !== shot.people) reasons.push(`aantal personen is ${obs.people}, verwacht ${shot.people}`);
  if (obs.feetVisible && !look.hasShoes) reasons.push("voeten in beeld terwijl de look geen loafers heeft");
  if (obs.socksVisible) reasons.push("sokken zichtbaar (loafers worden zonder sokken gedragen)");
  if (!obs.clean) reasons.push("niet clean genoeg (achtergrond, licht of kleuren te druk)");
  if (!obs.anatomyOk) reasons.push("anatomie klopt niet (handen, vingers, gezicht)");

  return { approved: reasons.length === 0, reasons };
}

/** De vragen die Claude per beeld beantwoordt voordat het naar de gebruiker gaat. */
export const QA_QUESTIONS = [
  "Noem elk zichtbaar kledingstuk en elke schoen. Staat er iets tussen dat niet in de look zit?",
  "Vergelijk elk product met zijn referentiefoto: kleur, breisel of stof, kraag, knopen of rits, zakken, lengte.",
  "Zie je een horloge, sieraad, riem, bril, tas, hoofddeksel, sjaal of das?",
  "Zie je een logo, label, monogram of tekst (ook op de achtergrond)?",
  "Klopt het aantal personen, en staat er niemand op de achtergrond?",
  "Bij loafers: zijn de enkels bloot (geen sokken)? Zonder loafers in de look: zijn de voeten uit beeld?",
  "Is het beeld clean: rustige achtergrond, zacht natuurlijk licht, maximaal drie kleurfamilies?",
  "Zijn handen, vingers en gezicht natuurlijk?",
];
