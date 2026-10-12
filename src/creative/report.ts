/** Markdown-rapport van de creative-analyse, voor docs/ en de CLI. */
import { ANGLE_LABEL, FORMAT_LABEL, type AdRecord } from "./types";
import {
  angleFormatMatrix, briefs, byAngle, byFormat, byMarket, byMonth, concepts, copyLibrary, copyPatterns, ratesOf, totalsOf,
  DEFAULT_THRESHOLDS, type Group, type Rates, type Thresholds, type Totals,
} from "./analysis";

const eur = (c: number | null) => (c === null ? "–" : `€ ${(c / 100).toLocaleString("nl-NL", { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`);
const eur2 = (c: number | null) => (c === null ? "–" : `€ ${(c / 100).toLocaleString("nl-NL", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`);
const x = (v: number | null) => (v === null ? "–" : `${v.toFixed(2).replace(".", ",")}x`);
const pct = (v: number | null, d = 1) => (v === null ? "–" : `${(v * 100).toFixed(d).replace(".", ",")}%`);
const cell = (s: string | null | undefined) => (s ?? "").replace(/\|/g, "/").replace(/\s+/g, " ").trim();

function metricRow(label: string, t: Totals, r: Rates): string {
  return `| ${cell(label)} | ${eur(t.spendCents)} | ${t.purchases} | ${eur(t.purchaseValueCents)} | ${x(r.roas)} | ${eur2(r.cpaCents)} | ${pct(r.ctr, 2)} | ${eur2(r.cpmCents)} | ${pct(r.cvr, 2)} |`;
}
const HEADER = `| | Spend | Aankopen | Omzet | ROAS | CPA | CTR | CPM | CVR |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|`;

function groupTable(groups: Group[], withVerdict = false): string {
  const head = withVerdict ? HEADER.replace("| | Spend", "| | Oordeel | Spend").replace("|---|---:", "|---|---|---:") : HEADER;
  return [head, ...groups.map((g) => (withVerdict ? metricRow(g.label, g.totals, g.rates).replace("| ", `| ${g.verdict} | `).replace(`| ${g.verdict} | ${cell(g.label)}`, `| ${cell(g.label)} | ${g.verdict}`) : metricRow(g.label, g.totals, g.rates)))].join("\n");
}

export function renderReport(ads: AdRecord[], th: Thresholds = DEFAULT_THRESHOLDS, generatedAt = new Date()): string {
  const all = totalsOf(ads);
  const allR = ratesOf(all);
  const months = byMonth(ads);
  const cons = concepts(ads, th);
  const winners = cons.filter((c) => c.verdict === "winnaar");
  const losers = cons.filter((c) => c.verdict === "verliezer" && c.totals.spendCents >= th.minSpendCents).slice(0, 12);
  const lib = copyLibrary(ads, th);
  const patterns = copyPatterns(ads);
  const recipes = briefs(ads, th);
  const videos = byFormat(ads, th).find((g) => g.key === "video");

  const out: string[] = [];
  out.push(`# Creative engine: wat werkt in de Meta-ads van ModernoMilano`);
  out.push(``);
  out.push(`Gegenereerd ${generatedAt.toISOString().slice(0, 10)} uit ${ads.length} advertenties, ${months[0]?.month ?? "?"} t/m ${months.at(-1)?.month ?? "?"}. Doel-ROAS ${th.targetRoas.toFixed(1).replace(".", ",")}x; een concept is een winnaar bij minimaal ${eur(th.winnerSpendCents)} spend, ${th.winnerPurchases} aankopen en ROAS boven doel.`);
  out.push(``);
  out.push(`## Samenvatting`);
  out.push(``);
  out.push(`- Totaal ${eur(all.spendCents)} besteed, ${all.purchases} aankopen, ${eur(all.purchaseValueCents)} omzet (Meta-attributie), ROAS ${x(allR.roas)}, CPA ${eur2(allR.cpaCents)}.`);
  out.push(`- CTR ${pct(allR.ctr, 2)}, CPM ${eur2(allR.cpmCents)}, conversie per klik ${pct(allR.cvr, 2)}, gemiddelde orderwaarde ${eur2(allR.aovCents)}.`);
  out.push(`- ${winners.length} bewezen winnende concepten, samen ${eur(totalsOf(winners.flatMap((w) => w.ads)).spendCents)} spend met ROAS ${x(ratesOf(totalsOf(winners.flatMap((w) => w.ads))).roas)}.`);
  if (videos) out.push(`- Video: hook rate ${pct(videos.rates.hookRate, 0)} (2 sec kijkers per impressie), hold rate ${pct(videos.rates.holdRate, 0)} (ThruPlay per start).`);
  out.push(``);
  out.push(`## Per maand`);
  out.push(``);
  out.push(HEADER);
  for (const m of months) out.push(metricRow(m.month, m.totals, m.rates));
  out.push(``);
  out.push(`## Winnende concepten`);
  out.push(``);
  out.push(`Een concept is dezelfde creative in alle campagnes, markten en kopieën samen.`);
  out.push(``);
  out.push(groupTable(cons.filter((c) => c.verdict === "winnaar" || c.verdict === "kansrijk"), true));
  out.push(``);
  out.push(`## Invalshoek`);
  out.push(``);
  out.push(groupTable(byAngle(ads, th)));
  out.push(``);
  out.push(`## Formaat`);
  out.push(``);
  out.push(groupTable(byFormat(ads, th)));
  out.push(``);
  out.push(`## Invalshoek × formaat (minimaal ${eur(th.minSpendCents)} spend)`);
  out.push(``);
  out.push(groupTable(angleFormatMatrix(ads, th)));
  out.push(``);
  out.push(`## Markt`);
  out.push(``);
  out.push(groupTable(byMarket(ads, th)));
  out.push(``);
  out.push(`## Wat werkt in de copy`);
  out.push(``);
  out.push(`ROAS van advertenties mét een kenmerk, vergeleken met advertenties zonder dat kenmerk (alleen ads met tekst).`);
  out.push(``);
  out.push(`| Kenmerk | Ads | Spend | ROAS | Verschil met de rest |\n|---|---:|---:|---:|---:|`);
  for (const p of patterns) out.push(`| ${p.label} | ${p.ads} | ${eur(p.totals.spendCents)} | ${x(p.rates.roas)} | ${p.liftVsRest === null ? "–" : `${p.liftVsRest >= 0 ? "+" : ""}${Math.round(p.liftVsRest * 100)}%`} |`);
  out.push(``);
  out.push(`## Copy-bibliotheek: bewezen teksten`);
  out.push(``);
  for (const c of lib.filter((e) => e.verdict === "winnaar" || e.verdict === "kansrijk").slice(0, 15)) {
    out.push(`### ${c.title ?? "(geen titel)"}`);
    out.push(``);
    out.push(`> ${(c.body ?? "(geen body)").replace(/\n+/g, " ")}`);
    out.push(``);
    out.push(`${c.verdict}, ${eur(c.totals.spendCents)} spend, ROAS ${x(c.rates.roas)}, CPA ${eur2(c.rates.cpaCents)}, gebruikt in: ${c.concepts.join(", ")}`);
    out.push(``);
  }
  out.push(`## Recepten voor nieuwe ads`);
  out.push(``);
  for (const b of recipes) {
    out.push(`### ${b.concept}`);
    out.push(``);
    out.push(`${ANGLE_LABEL[b.angle]}, ${FORMAT_LABEL[b.format].toLowerCase()}, CTA ${b.cta ?? "–"}. ${eur(b.totals.spendCents)} spend, ROAS ${x(b.rates.roas)}, CPA ${eur2(b.rates.cpaCents)}.`);
    out.push(``);
    out.push(`Markten: ${b.markets.map((m) => `${m.market} ${x(m.roas)} (${eur(m.spendCents)})`).join(", ")}`);
    out.push(``);
    if (b.title || b.body) {
      out.push(`Copy: **${b.title ?? ""}** ${(b.body ?? "").replace(/\n+/g, " ")}`);
      out.push(``);
    }
    if (b.why.length) {
      out.push(`Waarom het werkt:`);
      for (const w of b.why) out.push(`- ${w}`);
      out.push(``);
    }
    out.push(`Varianten om te maken:`);
    for (const v of b.variants) out.push(`- ${v}`);
    if (b.previewUrl || b.instagramUrl) out.push(`\nBekijk: ${[b.previewUrl, b.instagramUrl].filter(Boolean).join(" · ")}`);
    out.push(``);
  }
  out.push(`## Wat niet werkt (niet opnieuw maken)`);
  out.push(``);
  out.push(groupTable(losers));
  out.push(``);
  return out.join("\n");
}
