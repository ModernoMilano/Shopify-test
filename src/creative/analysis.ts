/**
 * Analyse van advertenties: wat werkt (concept, invalshoek, formaat, markt, copy) en welke
 * concepten bewezen winnaars zijn. Pure functies op AdRecord[]; geen database.
 */
import { ANGLE_LABEL, FORMAT_LABEL, type AdMonthMetrics, type AdRecord, type Angle, type AdFormat } from "./types";
import { COPY_FEATURES, conceptLabel, copyFeatures } from "./classify";

export type Totals = {
  spendCents: number;
  impressions: number;
  reach: number;
  clicks: number;
  linkClicks: number;
  landingPageViews: number;
  addToCart: number;
  checkouts: number;
  purchases: number;
  purchaseValueCents: number;
  videoPlays: number;
  video2s: number;
  thruplays: number;
  videoP100: number;
  videoImpressions: number; // impressies van maanden met videocijfers, voor hook rate
  ads: number;
  months: Set<string>;
};

export type Rates = {
  roas: number | null;
  cpaCents: number | null;
  ctr: number | null; // link clicks / impressies
  cpmCents: number | null;
  cpcCents: number | null;
  lpvRate: number | null; // landing page views / link clicks
  atcRate: number | null; // add to cart / landing page views
  cvr: number | null; // aankopen / link clicks
  aovCents: number | null;
  hookRate: number | null; // 2 sec kijkers / impressies
  holdRate: number | null; // thruplays / plays
  completion: number | null; // 100% / plays
};

export type Verdict = "winnaar" | "kansrijk" | "te vroeg" | "zwak" | "verliezer";

export const VERDICT_ORDER: Verdict[] = ["winnaar", "kansrijk", "te vroeg", "zwak", "verliezer"];

export type Thresholds = {
  targetRoas: number; // break-even of doel-ROAS
  winnerSpendCents: number; // minimaal besteed om "winnaar" te heten
  winnerPurchases: number;
  minSpendCents: number; // onder dit bedrag is een oordeel "te vroeg"
};

export const DEFAULT_THRESHOLDS: Thresholds = { targetRoas: 2, winnerSpendCents: 30_000, winnerPurchases: 5, minSpendCents: 10_000 };

export function emptyTotals(): Totals {
  return {
    spendCents: 0, impressions: 0, reach: 0, clicks: 0, linkClicks: 0, landingPageViews: 0, addToCart: 0, checkouts: 0,
    purchases: 0, purchaseValueCents: 0, videoPlays: 0, video2s: 0, thruplays: 0, videoP100: 0, videoImpressions: 0, ads: 0, months: new Set(),
  };
}

export function addMonth(t: Totals, m: AdMonthMetrics): void {
  t.spendCents += m.spendCents;
  t.impressions += m.impressions;
  t.reach += m.reach;
  t.clicks += m.clicks;
  t.linkClicks += m.linkClicks;
  t.landingPageViews += m.landingPageViews;
  t.addToCart += m.addToCart;
  t.checkouts += m.checkouts;
  t.purchases += m.purchases;
  t.purchaseValueCents += m.purchaseValueCents;
  if (m.videoPlays != null && m.videoPlays > 0) {
    t.videoPlays += m.videoPlays;
    t.video2s += m.video2s ?? 0;
    t.thruplays += m.thruplays ?? 0;
    t.videoP100 += m.videoP100 ?? 0;
    t.videoImpressions += m.impressions;
  }
  t.months.add(m.month);
}

export function totalsOf(ads: AdRecord[]): Totals {
  const t = emptyTotals();
  for (const ad of ads) {
    t.ads += 1;
    for (const m of ad.months) addMonth(t, m);
  }
  return t;
}

const div = (a: number, b: number) => (b > 0 ? a / b : null);

export function ratesOf(t: Totals): Rates {
  return {
    roas: div(t.purchaseValueCents, t.spendCents),
    cpaCents: t.purchases > 0 ? Math.round(t.spendCents / t.purchases) : null,
    ctr: div(t.linkClicks, t.impressions),
    cpmCents: t.impressions > 0 ? Math.round((t.spendCents / t.impressions) * 1000) : null,
    cpcCents: t.linkClicks > 0 ? Math.round(t.spendCents / t.linkClicks) : null,
    lpvRate: div(t.landingPageViews, t.linkClicks),
    atcRate: div(t.addToCart, t.landingPageViews),
    cvr: div(t.purchases, t.linkClicks),
    aovCents: t.purchases > 0 ? Math.round(t.purchaseValueCents / t.purchases) : null,
    // Windsor levert "2 seconden bekeken" niet altijd (dan 0): geen hook rate in plaats van 0%
    hookRate: t.video2s > 0 ? div(t.video2s, t.videoImpressions) : null,
    holdRate: div(t.thruplays, t.videoPlays),
    completion: div(t.videoP100, t.videoPlays),
  };
}

export function verdictOf(t: Totals, th: Thresholds = DEFAULT_THRESHOLDS): Verdict {
  const roas = div(t.purchaseValueCents, t.spendCents);
  if (t.spendCents < th.minSpendCents) return "te vroeg";
  if (roas !== null && roas >= th.targetRoas && t.spendCents >= th.winnerSpendCents && t.purchases >= th.winnerPurchases) return "winnaar";
  if (roas !== null && roas >= th.targetRoas) return "kansrijk";
  if (t.purchases === 0 || (roas ?? 0) < th.targetRoas * 0.5) return "verliezer";
  return "zwak";
}

export type Group<K extends string = string> = {
  key: K;
  label: string;
  totals: Totals;
  rates: Rates;
  verdict: Verdict;
  ads: AdRecord[];
};

function groupBy<K extends string>(ads: AdRecord[], keyOf: (a: AdRecord) => K, labelOf: (k: K, a: AdRecord) => string, th: Thresholds): Group<K>[] {
  const m = new Map<K, { label: string; ads: AdRecord[] }>();
  for (const a of ads) {
    const k = keyOf(a);
    const g = m.get(k) ?? { label: labelOf(k, a), ads: [] };
    g.ads.push(a);
    m.set(k, g);
  }
  return [...m.entries()]
    .map(([key, g]) => {
      const totals = totalsOf(g.ads);
      return { key, label: g.label, totals, rates: ratesOf(totals), verdict: verdictOf(totals, th), ads: g.ads };
    })
    .sort((a, b) => b.totals.spendCents - a.totals.spendCents);
}

/** Concepten: dezelfde creative in alle campagnes en markten samen, gesorteerd op oordeel en spend. */
export function concepts(ads: AdRecord[], th: Thresholds = DEFAULT_THRESHOLDS): Group[] {
  const groups = groupBy(ads, (a) => a.conceptKey, (_k, a) => conceptLabel(a.name), th);
  return groups.sort((a, b) => VERDICT_ORDER.indexOf(a.verdict) - VERDICT_ORDER.indexOf(b.verdict) || b.totals.spendCents - a.totals.spendCents);
}

export function byAngle(ads: AdRecord[], th: Thresholds = DEFAULT_THRESHOLDS): Group<Angle>[] {
  return groupBy(ads, (a) => a.angle, (k) => ANGLE_LABEL[k], th);
}

export function byFormat(ads: AdRecord[], th: Thresholds = DEFAULT_THRESHOLDS): Group<AdFormat>[] {
  return groupBy(ads, (a) => a.format, (k) => FORMAT_LABEL[k], th);
}

export function byMarket(ads: AdRecord[], th: Thresholds = DEFAULT_THRESHOLDS): Group[] {
  return groupBy(ads, (a) => a.market, (k) => k, th);
}

export function byMonth(ads: AdRecord[]): { month: string; totals: Totals; rates: Rates }[] {
  const m = new Map<string, Totals>();
  for (const a of ads) {
    for (const mm of a.months) {
      const t = m.get(mm.month) ?? emptyTotals();
      addMonth(t, mm);
      m.set(mm.month, t);
    }
  }
  return [...m.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([month, totals]) => ({ month, totals, rates: ratesOf(totals) }));
}

/** Invalshoek × formaat: welke combinatie levert het meeste op. */
export function angleFormatMatrix(ads: AdRecord[], th: Thresholds = DEFAULT_THRESHOLDS): Group[] {
  return groupBy(ads, (a) => `${a.angle}|${a.format}`, (_k, a) => `${ANGLE_LABEL[a.angle]} · ${FORMAT_LABEL[a.format]}`, th).filter(
    (g) => g.totals.spendCents >= th.minSpendCents,
  );
}

export type CopyPattern = { key: string; label: string; ads: number; totals: Totals; rates: Rates; liftVsRest: number | null };

/** Per copy-kenmerk: ROAS van ads mét dat kenmerk vergeleken met ads zonder. Alleen ads met copy tellen mee. */
export function copyPatterns(ads: AdRecord[]): CopyPattern[] {
  const withCopy = ads.filter((a) => (a.title || a.body) && !/\{\{product\.name\}\}/.test(a.title ?? ""));
  return COPY_FEATURES.map((f) => {
    const has = withCopy.filter((a) => copyFeatures(a.title, a.body).includes(f.key));
    const not = withCopy.filter((a) => !copyFeatures(a.title, a.body).includes(f.key));
    const totals = totalsOf(has);
    const rates = ratesOf(totals);
    const restRoas = ratesOf(totalsOf(not)).roas;
    return {
      key: f.key,
      label: f.label,
      ads: has.length,
      totals,
      rates,
      liftVsRest: rates.roas !== null && restRoas !== null && restRoas > 0 ? rates.roas / restRoas - 1 : null,
    };
  })
    .filter((p) => p.ads > 0)
    .sort((a, b) => (b.rates.roas ?? 0) - (a.rates.roas ?? 0));
}

export type CopyEntry = { title: string | null; body: string | null; concepts: string[]; totals: Totals; rates: Rates; verdict: Verdict };

/** Alle unieke copy's (titel + body) met hun gezamenlijke cijfers, beste eerst. */
export function copyLibrary(ads: AdRecord[], th: Thresholds = DEFAULT_THRESHOLDS): CopyEntry[] {
  const m = new Map<string, { title: string | null; body: string | null; concepts: Set<string>; ads: AdRecord[] }>();
  for (const a of ads) {
    if ((!a.title && !a.body) || /\{\{product\.name\}\}/.test(a.title ?? "")) continue;
    const k = `${(a.title ?? "").trim()}\n${(a.body ?? "").trim()}`;
    const e = m.get(k) ?? { title: a.title, body: a.body, concepts: new Set<string>(), ads: [] };
    e.concepts.add(conceptLabel(a.name));
    e.ads.push(a);
    m.set(k, e);
  }
  return [...m.values()]
    .map((e) => {
      const totals = totalsOf(e.ads);
      return { title: e.title, body: e.body, concepts: [...e.concepts], totals, rates: ratesOf(totals), verdict: verdictOf(totals, th) };
    })
    .sort((a, b) => VERDICT_ORDER.indexOf(a.verdict) - VERDICT_ORDER.indexOf(b.verdict) || b.totals.spendCents - a.totals.spendCents);
}

export type Brief = {
  concept: string;
  angle: Angle;
  format: AdFormat;
  markets: { market: string; roas: number | null; spendCents: number }[];
  title: string | null;
  body: string | null;
  cta: string | null;
  thumbnailUrl: string | null;
  previewUrl: string | null;
  instagramUrl: string | null;
  totals: Totals;
  rates: Rates;
  why: string[];
  variants: string[];
};

const VARIANTS: Record<Angle, string[]> = {
  bundel: ["Zelfde bundel in een andere kleurstelling (navy, zwart, beige) met dezelfde titel", "Prijsanker toevoegen: 'los € X, als set € Y'", "Video-versie: outfit in 3 shots opgebouwd (vest, polo, broek)"],
  cashmere_sale: ["Andere kleur of ander product uit de cashmere-collectie met dezelfde '50% off' kop", "Seizoenshook vervangen: 'The cold is coming' → feestdagen/cadeau", "Statische versie met prijs doorgestreept"],
  cashmere: ["Zelfde beeld met een sale-kop (cashmere + korting scoort beter dan cashmere zonder)", "Close-up van de stof als eerste frame"],
  unboxing: ["Unboxing van een ander product in dezelfde verpakking", "Cadeau-hook voor Q4: 'ready to give or keep'"],
  ugc: ["Dezelfde UGC-stijl met een andere set", "Zelfde hook ('Tired of guessing what goes with what?') als video-opener"],
  tijdloos: ["Zelfde fotografiestijl (close-up, buiten) met ander product", "Kop behouden, body korter maken"],
  lounge: ["Zelfde video-opbouw met een andere set", "Garantielijst (✅) behouden, kop testen zonder korting"],
  reverso: ["Reversible-moment als eerste frame tonen", "Statisch beeld met beide kanten naast elkaar"],
  catalogus: ["Catalogus met alleen bestsellers als productset", "Dezelfde catalogus in een nieuwe markt"],
  jacket: ["Zelfde studio-setting met een ander hero-product", "Versie met copy (titel + body); de winnaar draait nu zonder tekst"],
  zomer: ["Zelfde opzet (event, 72 uur sale) voor de winter- of feestdagencollectie"],
  product: ["Hetzelfde product als onderdeel van een bundel laten zien (bundels scoren hoger dan losse stukken)", "Close-up van stof of pasvorm als eerste beeld, met één concreet voordeel in de kop"],
  overig: ["Winnende elementen (kop, CTA, formaat) overzetten naar een nieuw product"],
};

/** Recepten voor nieuwe ads: de bewezen winnaars, met waarom ze werken en welke variant je kunt maken. */
export function briefs(ads: AdRecord[], th: Thresholds = DEFAULT_THRESHOLDS, limit = 8): Brief[] {
  const all = ratesOf(totalsOf(ads));
  return concepts(ads, th)
    .filter((g) => g.verdict === "winnaar" || g.verdict === "kansrijk")
    .slice(0, limit)
    .map((g) => {
      const best = [...g.ads].sort((a, b) => totalsOf([b]).spendCents - totalsOf([a]).spendCents)[0];
      const markets = byMarket(g.ads, th).map((m) => ({ market: m.key, roas: m.rates.roas, spendCents: m.totals.spendCents }));
      const why: string[] = [];
      if (g.rates.roas !== null && all.roas !== null && g.rates.roas > all.roas) why.push(`ROAS ${g.rates.roas.toFixed(2)} tegen ${all.roas.toFixed(2)} gemiddeld`);
      if (g.rates.ctr !== null && all.ctr !== null && g.rates.ctr > all.ctr * 1.15) why.push(`CTR ${(g.rates.ctr * 100).toFixed(2)}% tegen ${(all.ctr * 100).toFixed(2)}% gemiddeld: het beeld stopt de scroll`);
      if (g.rates.cvr !== null && all.cvr !== null && g.rates.cvr > all.cvr * 1.15) why.push(`Conversie per klik ${(g.rates.cvr * 100).toFixed(2)}% tegen ${(all.cvr * 100).toFixed(2)}%: de belofte wordt op de site waargemaakt`);
      if (g.rates.hookRate !== null && all.hookRate !== null && g.rates.hookRate > all.hookRate * 1.15) why.push(`Hook rate ${(g.rates.hookRate * 100).toFixed(0)}% tegen ${(all.hookRate * 100).toFixed(0)}%: de eerste seconden werken`);
      if (markets.filter((m) => m.roas !== null && m.roas >= th.targetRoas).length >= 2) why.push("Werkt in meerdere markten, dus het concept is sterk en niet toevallig");
      if (g.totals.months.size >= 2) why.push(`Al ${g.totals.months.size} maanden rendabel`);
      return {
        concept: g.label,
        angle: best.angle,
        format: best.format,
        markets,
        title: best.title,
        body: best.body,
        cta: best.cta,
        thumbnailUrl: best.thumbnailUrl,
        previewUrl: best.previewUrl,
        instagramUrl: best.instagramUrl,
        totals: g.totals,
        rates: g.rates,
        why,
        variants: VARIANTS[best.angle],
      };
    });
}
