// Kwaliteitscontrole na het genereren. Een beeld gaat pas door als niets erin buiten de look valt.
// Claude bekijkt elk beeld, vult een Observation in en deze functie beslist: goedgekeurd of afgekeurd.
// Staat er iemand in beeld, dan moet het het vaste model zijn (brand/assets/model, data/model.json). Anders: afgekeurd.

import { MODEL } from "./casting";
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
  /** Merktekens, emblemen of kentekens op auto's en boten, of andere herkenbare merkobjecten. */
  brandedObjects?: string[];
  /** Mensen die scherp of herkenbaar in beeld zijn (een hand of benen in een detail tellen als één). Hoort shot.people te zijn. */
  people: number;
  /** Verre voorbijgangers: klein, onscherp, gezicht onleesbaar. Alleen op een openbare plek (shot.publicPlace), hooguit 3. */
  passersBy?: number;
  feetVisible: boolean;
  socksVisible: boolean;
  /** Clean look: rustige achtergrond, zacht licht, maximaal drie kleurfamilies. */
  clean: boolean;
  /** Anatomie: handen, vingers, gezicht zonder AI-fouten. */
  anatomyOk: boolean;
  /**
   * Is zijn gezicht herkenbaar in beeld? Nee bij een detail, een still life, van achteren, of in een wijd beeld waarin hij
   * opzij staat en zijn gezicht niet te lezen is.
   */
  faceVisible: boolean;
  /**
   * Is dit dezelfde man als op de referentiefoto's (brand/assets/model): gezicht, wenkbrauwen, ogen, kaak, haar, postuur?
   * null alleen als faceVisible false is.
   */
  sameModel: boolean | null;
  /** Ziet het eruit als een echte foto: huid, stof, licht dat bij de achtergrond past, geen filmranden? */
  realPhoto?: boolean;
  /** Breedte van zijn gezicht in het eindbestand, in pixels. Verplicht als faceVisible true is. */
  faceWidthPx?: number;
  notes?: string;
}

export interface Verdict {
  approved: boolean;
  reasons: string[];
}

/** Op een openbare plek hooguit zoveel verre voorbijgangers (model.json → public_places_en: 2 of 3). */
export const MAX_PASSERS_BY = 3;

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
  if (obs.brandedObjects?.length) reasons.push(`merkobjecten in beeld: ${obs.brandedObjects.join(", ")}`);
  if (obs.logosOrText) reasons.push("logo, label of tekst zichtbaar");
  if (obs.people !== shot.people) reasons.push(`aantal personen is ${obs.people}, verwacht ${shot.people}`);
  const passers = obs.passersBy ?? 0;
  if (passers > 0 && !shot.publicPlace) reasons.push(`${passers} voorbijganger(s) op een plek waar verder niemand hoort te staan`);
  if (passers > MAX_PASSERS_BY) reasons.push(`te veel voorbijgangers (${passers}, hooguit ${MAX_PASSERS_BY})`);
  if (obs.feetVisible && !look.hasShoes) reasons.push("voeten in beeld terwijl de look geen loafers heeft");
  if (obs.socksVisible) reasons.push("sokken zichtbaar (loafers worden zonder sokken gedragen)");
  if (!obs.clean) reasons.push("niet clean genoeg (achtergrond, licht of kleuren te druk)");
  if (!obs.anatomyOk) reasons.push("anatomie klopt niet (handen, vingers, gezicht)");
  if (obs.sameModel === false) reasons.push("niet dezelfde man als op de referentiefoto's (brand/assets/model)");
  if (obs.faceVisible && obs.sameModel === null) reasons.push("zijn gezicht is in beeld, maar niet naast de referentiefoto's gelegd");
  if (obs.faceVisible && obs.faceWidthPx === undefined) reasons.push("breedte van zijn gezicht niet gemeten");
  if (obs.faceVisible && obs.faceWidthPx !== undefined && obs.faceWidthPx < MODEL.faceMinPx) {
    reasons.push(`gezicht te klein (${obs.faceWidthPx} px, minimaal ${MODEL.faceMinPx} px)`);
  }
  if (obs.realPhoto === false) reasons.push("ziet er niet uit als een echte foto (huid, stof, licht of randen)");

  return { approved: reasons.length === 0, reasons };
}

/** De vragen die Claude per beeld beantwoordt voordat het naar de gebruiker gaat. */
export const QA_QUESTIONS = [
  "Noem elk zichtbaar kledingstuk en elke schoen. Staat er iets tussen dat niet in de look zit?",
  "Vergelijk elk product met zijn referentiefoto: kleur, breisel of stof, kraag, knopen of rits, zakken, lengte.",
  "Zie je een horloge, sieraad, riem, bril, tas, hoofddeksel, sjaal of das?",
  "Zie je een logo, label, monogram of tekst (ook op de achtergrond)?",
  "Hoeveel mensen zijn scherp of herkenbaar in beeld (people)? Alleen hij, of niemand bij een still life; een hand of benen in een detail tellen als één. " +
    "Nooit een tweede herkenbare man en nooit een vrouw. Op een openbare plek mogen 2 of 3 voorbijgangers ver weg staan, klein en onscherp, " +
    "met onleesbare gezichten: tel die apart (passersBy). Op andere plekken staat er verder niemand.",
  "Staat er een merkteken, embleem of leesbaar kenteken op een auto of boot, of een ander object van een merk in beeld?",
  "Bij loafers: zijn de enkels bloot (geen sokken)? Zonder loafers in de look: zijn de voeten uit beeld?",
  "Is het beeld clean: rustige achtergrond, zacht natuurlijk licht, maximaal drie kleurfamilies?",
  "Zijn handen, vingers en gezicht natuurlijk?",
  "Is zijn gezicht herkenbaar in beeld (faceVisible)? Nee bij een detail, van achteren of in een wijd beeld waarin hij opzij staat: dan sameModel null. " +
    "Zo ja: is dit dezelfde man als in brand/assets/model? Leg het beeld naast ref-1 en ref-4: gezicht, wenkbrauwen, ogen, kaak, haar (kleur, lengte, naar achteren) en postuur.",
  `Hoe breed is zijn gezicht in het eindbestand, in pixels (faceWidthPx)? Alleen als zijn gezicht herkenbaar in beeld is. Minder dan ongeveer ${MODEL.faceMinPx} px is afgekeurd.`,
  "Ziet het eruit als een echte foto: huid met fijne textuur maar niet glad of wasachtig, stof met echte steek en plooien, licht op hem dat bij de achtergrond past, " +
    "loafers als gespiegeld paar (links en rechts), geen filmranden of afgeronde hoeken?",
];
