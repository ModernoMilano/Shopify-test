import fs from "node:fs";
import path from "node:path";
import { PageHeader } from "@/components/PageHeader";
import { Card, Kpi, euro, pct, times } from "@/components/ui";
import { db } from "@/lib/db";
import { getFinanceSettings } from "@/finance/settings";
import { loadAds } from "@/creative/sync";
import { ANGLE_LABEL, FORMAT_LABEL, type AdRecord } from "@/creative/types";
import {
  DEFAULT_THRESHOLDS, angleFormatMatrix, briefs, byAngle, byFormat, byMarket, byMonth, concepts, copyLibrary, copyPatterns, ratesOf, totalsOf,
  type Group, type Verdict,
} from "@/creative/analysis";
import { SyncCreatives } from "./SyncCreatives";

export const dynamic = "force-dynamic";

const VERDICT_TONE: Record<Verdict, string> = {
  winnaar: "bg-good/15 text-good",
  kansrijk: "bg-info/15 text-info",
  "te vroeg": "bg-surface-2 text-ink-3",
  zwak: "bg-warn/15 text-warn",
  verliezer: "bg-neg/15 text-neg",
};

function VerdictPill({ v }: { v: Verdict }) {
  return <span className={`inline-block rounded-full px-2 py-px text-[11px] font-medium whitespace-nowrap ${VERDICT_TONE[v]}`}>{v}</span>;
}

/** Database, of anders de meegeleverde dataset uit scripts/data (na `npm run ads:scrape`). */
async function getAds(): Promise<{ ads: AdRecord[]; source: string }> {
  try {
    const ads = await loadAds();
    if (ads.length) return { ads, source: "database" };
  } catch {
    // geen database beschikbaar: val terug op het bestand
  }
  try {
    const file = path.join(process.cwd(), "scripts", "data", "meta-ads.json");
    const json = JSON.parse(fs.readFileSync(file, "utf8")) as { generatedAt: string; ads: AdRecord[] };
    return { ads: json.ads, source: `bestand van ${json.generatedAt.slice(0, 10)}` };
  } catch {
    return { ads: [], source: "geen" };
  }
}

function GroupTable({ groups, label, target, showVerdict = true }: { groups: Group[]; label: string; target: number; showVerdict?: boolean }) {
  return (
    <div className="overflow-x-auto">
      <table className="data">
        <thead>
          <tr>
            <th>{label}</th>
            {showVerdict && <th>Oordeel</th>}
            <th className="r">Ads</th>
            <th className="r">Spend</th>
            <th className="r">Aankopen</th>
            <th className="r">Omzet</th>
            <th className="r">ROAS</th>
            <th className="r">CPA</th>
            <th className="r">CTR</th>
            <th className="r">CPM</th>
            <th className="r">CVR</th>
          </tr>
        </thead>
        <tbody>
          {groups.map((g) => (
            <tr key={g.key}>
              <td className="max-w-[20rem] truncate" title={g.label}>{g.label}</td>
              {showVerdict && <td><VerdictPill v={g.verdict} /></td>}
              <td className="r">{g.totals.ads}</td>
              <td className="r">{euro(g.totals.spendCents, true)}</td>
              <td className="r">{g.totals.purchases}</td>
              <td className="r">{euro(g.totals.purchaseValueCents, true)}</td>
              <td className={`r font-medium ${g.rates.roas !== null && g.rates.roas < target ? "text-neg" : "text-good"}`}>{times(g.rates.roas)}</td>
              <td className="r">{g.rates.cpaCents === null ? "–" : euro(g.rates.cpaCents)}</td>
              <td className="r">{g.rates.ctr === null ? "–" : pct(g.rates.ctr, 2)}</td>
              <td className="r">{g.rates.cpmCents === null ? "–" : euro(g.rates.cpmCents)}</td>
              <td className="r">{g.rates.cvr === null ? "–" : pct(g.rates.cvr, 2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default async function CreativesPage({ searchParams }: { searchParams: Promise<Record<string, string>> }) {
  const params = await searchParams;
  const [{ ads, source }, settings, sync] = await Promise.all([
    getAds(),
    getFinanceSettings().catch(() => null),
    db.sourceSync.findUnique({ where: { source: "windsor_ads" } }).catch(() => null),
  ]);
  const target = settings?.breakEvenTarget ?? DEFAULT_THRESHOLDS.targetRoas;
  const th = { ...DEFAULT_THRESHOLDS, targetRoas: target };
  const filter = params.oordeel as Verdict | undefined;

  const all = totalsOf(ads);
  const allR = ratesOf(all);
  const cons = concepts(ads, th);
  const shown = filter ? cons.filter((c) => c.verdict === filter) : cons;
  const winners = cons.filter((c) => c.verdict === "winnaar");
  const winnerTotals = totalsOf(winners.flatMap((w) => w.ads));
  const lib = copyLibrary(ads, th).filter((c) => c.verdict === "winnaar" || c.verdict === "kansrijk").slice(0, 12);
  const patterns = copyPatterns(ads);
  const recipes = briefs(ads, th);
  const months = byMonth(ads);
  const video = byFormat(ads, th).find((g) => g.key === "video");

  return (
    <div className="mx-auto max-w-7xl">
      <PageHeader
        title="Creative engine"
        subtitle={
          <>
            Alle advertenties uit het Meta-account sinds april 2026, samengevoegd per concept. Doel-ROAS {times(target)}. Bron: {source}
            {sync ? `, laatste sync ${sync.lastAt.toLocaleString("nl-NL", { timeZone: "Europe/Amsterdam" })} (${sync.status})` : ""}.
          </>
        }
      >
        <SyncCreatives />
      </PageHeader>

      {!ads.length && (
        <Card className="mb-6">
          <p className="text-sm text-ink-2">Nog geen advertenties. Zet WINDSOR_API_KEY en klik op Alles ophalen, of draai <code>npm run ads:scrape</code>.</p>
        </Card>
      )}

      <div className="mb-6 grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-6">
        <Kpi label="Spend totaal" value={euro(all.spendCents, true)} sub={`${ads.length} ads, ${cons.length} concepten`} />
        <Kpi label="ROAS" value={times(allR.roas)} sub={`CPA ${allR.cpaCents === null ? "–" : euro(allR.cpaCents)}`} tone={allR.roas !== null && allR.roas < target ? "neg" : "good"} />
        <Kpi label="Winnende concepten" value={String(winners.length)} sub={`${euro(winnerTotals.spendCents, true)} spend, ROAS ${times(ratesOf(winnerTotals).roas)}`} tone="good" />
        <Kpi label="CTR" value={pct(allR.ctr, 2)} sub={`CPM ${allR.cpmCents === null ? "–" : euro(allR.cpmCents)}`} />
        <Kpi label="Conversie per klik" value={pct(allR.cvr, 2)} sub={`AOV ${allR.aovCents === null ? "–" : euro(allR.aovCents)}`} />
        <Kpi label="Video hook / hold" value={video ? `${pct(video.rates.hookRate, 0)} / ${pct(video.rates.holdRate, 0)}` : "–"} sub="2 sec kijkers, ThruPlay" />
      </div>

      <Card
        title="Concepten"
        className="mb-6"
        action={
          <div className="flex flex-wrap gap-1 text-xs">
            <a href="/creatives" className={`rounded-full border px-2 py-px ${!filter ? "border-ink bg-surface-2 font-medium" : "border-line text-ink-2"}`}>alle</a>
            {(["winnaar", "kansrijk", "te vroeg", "zwak", "verliezer"] as Verdict[]).map((v) => (
              <a key={v} href={`/creatives?oordeel=${encodeURIComponent(v)}`} className={`rounded-full border px-2 py-px ${filter === v ? "border-ink bg-surface-2 font-medium" : "border-line text-ink-2"}`}>
                {v} ({cons.filter((c) => c.verdict === v).length})
              </a>
            ))}
          </div>
        }
      >
        <p className="mb-3 text-sm text-ink-2">
          Winnaar: minimaal {euro(th.winnerSpendCents, true)} spend, {th.winnerPurchases} aankopen en ROAS boven doel. Kansrijk: ROAS boven doel maar nog weinig spend. Te vroeg: onder {euro(th.minSpendCents, true)} spend.
        </p>
        <div className="overflow-x-auto">
          <table className="data">
            <thead>
              <tr>
                <th></th>
                <th>Concept</th>
                <th>Oordeel</th>
                <th>Invalshoek</th>
                <th>Formaat</th>
                <th>Markten</th>
                <th className="r">Spend</th>
                <th className="r">Aankopen</th>
                <th className="r">ROAS</th>
                <th className="r">CPA</th>
                <th className="r">CTR</th>
                <th className="r">Hook</th>
                <th className="r">Maanden</th>
              </tr>
            </thead>
            <tbody>
              {shown.map((g) => {
                const best = g.ads[0];
                const markets = byMarket(g.ads, th);
                return (
                  <tr key={g.key}>
                    <td className="w-12">
                      {best.thumbnailUrl ? (
                        <a href={best.previewUrl ?? best.instagramUrl ?? best.thumbnailUrl} target="_blank" rel="noreferrer">
                          {/* eslint-disable-next-line @next/next/no-img-element */}
                          <img src={best.thumbnailUrl} alt="" className="h-10 w-10 rounded object-cover" />
                        </a>
                      ) : (
                        <div className="h-10 w-10 rounded bg-surface-2" />
                      )}
                    </td>
                    <td className="max-w-[18rem]">
                      <div className="truncate font-medium" title={g.label}>{g.label}</div>
                      {best.title && <div className="truncate text-xs text-ink-3" title={best.title}>{best.title}</div>}
                    </td>
                    <td><VerdictPill v={g.verdict} /></td>
                    <td className="whitespace-nowrap">{ANGLE_LABEL[best.angle]}</td>
                    <td className="whitespace-nowrap">{FORMAT_LABEL[best.format]}</td>
                    <td className="text-xs whitespace-nowrap">{markets.map((m) => `${m.key} ${times(m.rates.roas)}`).join(" · ")}</td>
                    <td className="r">{euro(g.totals.spendCents, true)}</td>
                    <td className="r">{g.totals.purchases}</td>
                    <td className={`r font-medium ${g.rates.roas !== null && g.rates.roas < target ? "text-neg" : "text-good"}`}>{times(g.rates.roas)}</td>
                    <td className="r">{g.rates.cpaCents === null ? "–" : euro(g.rates.cpaCents)}</td>
                    <td className="r">{g.rates.ctr === null ? "–" : pct(g.rates.ctr, 2)}</td>
                    <td className="r">{g.rates.hookRate === null ? "–" : pct(g.rates.hookRate, 0)}</td>
                    <td className="r">{g.totals.months.size}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>

      <Card title="Recepten voor nieuwe ads" className="mb-6">
        <p className="mb-3 text-sm text-ink-2">De bewezen winnaars, met waarom ze werken en welke variant je als volgende maakt.</p>
        <div className="grid gap-4 md:grid-cols-2">
          {recipes.map((b) => (
            <div key={b.concept} className="rounded-lg border border-line p-4">
              <div className="flex items-start gap-3">
                {b.thumbnailUrl && (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={b.thumbnailUrl} alt="" className="h-20 w-20 shrink-0 rounded object-cover" />
                )}
                <div className="min-w-0">
                  <div className="font-medium">{b.concept}</div>
                  <div className="text-xs text-ink-3">
                    {ANGLE_LABEL[b.angle]} · {FORMAT_LABEL[b.format]} · CTA {b.cta ?? "–"}
                  </div>
                  <div className="mt-1 text-sm">
                    {euro(b.totals.spendCents, true)} spend, ROAS <span className="font-medium text-good">{times(b.rates.roas)}</span>, CPA {b.rates.cpaCents === null ? "–" : euro(b.rates.cpaCents)}
                  </div>
                  <div className="text-xs text-ink-3">{b.markets.map((m) => `${m.market} ${times(m.roas)}`).join(" · ")}</div>
                </div>
              </div>
              {(b.title || b.body) && (
                <div className="mt-3 rounded bg-surface-2 p-3 text-sm">
                  {b.title && <div className="font-medium">{b.title}</div>}
                  {b.body && <div className="mt-1 whitespace-pre-line text-ink-2">{b.body}</div>}
                </div>
              )}
              {b.why.length > 0 && (
                <ul className="mt-3 list-disc pl-5 text-sm text-ink-2">
                  {b.why.map((w) => <li key={w}>{w}</li>)}
                </ul>
              )}
              <div className="mt-3 text-xs font-medium tracking-wider text-ink-3 uppercase">Volgende variant</div>
              <ul className="mt-1 list-disc pl-5 text-sm">
                {b.variants.map((v) => <li key={v}>{v}</li>)}
              </ul>
              <div className="mt-2 flex gap-3 text-xs">
                {b.previewUrl && <a className="underline" href={b.previewUrl} target="_blank" rel="noreferrer">Preview</a>}
                {b.instagramUrl && <a className="underline" href={b.instagramUrl} target="_blank" rel="noreferrer">Instagram</a>}
              </div>
            </div>
          ))}
        </div>
      </Card>

      <div className="mb-6 grid gap-6 lg:grid-cols-2">
        <Card title="Invalshoek">
          <GroupTable groups={byAngle(ads, th)} label="Invalshoek" target={target} showVerdict={false} />
        </Card>
        <Card title="Formaat">
          <GroupTable groups={byFormat(ads, th)} label="Formaat" target={target} showVerdict={false} />
          <div className="mt-4">
            <GroupTable groups={byMarket(ads, th)} label="Markt" target={target} showVerdict={false} />
          </div>
        </Card>
      </div>

      <Card title="Invalshoek × formaat" className="mb-6">
        <GroupTable groups={angleFormatMatrix(ads, th)} label="Combinatie" target={target} />
      </Card>

      <div className="mb-6 grid gap-6 lg:grid-cols-2">
        <Card title="Wat werkt in de copy">
          <p className="mb-3 text-sm text-ink-2">ROAS van ads mét het kenmerk, en het verschil met ads zonder.</p>
          <table className="data">
            <thead>
              <tr><th>Kenmerk</th><th className="r">Ads</th><th className="r">Spend</th><th className="r">ROAS</th><th className="r">Verschil</th></tr>
            </thead>
            <tbody>
              {patterns.map((p) => (
                <tr key={p.key}>
                  <td>{p.label}</td>
                  <td className="r">{p.ads}</td>
                  <td className="r">{euro(p.totals.spendCents, true)}</td>
                  <td className="r font-medium">{times(p.rates.roas)}</td>
                  <td className={`r ${p.liftVsRest === null ? "" : p.liftVsRest >= 0 ? "text-good" : "text-neg"}`}>
                    {p.liftVsRest === null ? "–" : `${p.liftVsRest >= 0 ? "+" : ""}${Math.round(p.liftVsRest * 100)}%`}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
        <Card title="Per maand">
          <table className="data">
            <thead>
              <tr><th>Maand</th><th className="r">Spend</th><th className="r">Aankopen</th><th className="r">ROAS</th><th className="r">CPA</th><th className="r">CTR</th><th className="r">CPM</th></tr>
            </thead>
            <tbody>
              {months.map((m) => (
                <tr key={m.month}>
                  <td>{m.month}</td>
                  <td className="r">{euro(m.totals.spendCents, true)}</td>
                  <td className="r">{m.totals.purchases}</td>
                  <td className={`r font-medium ${m.rates.roas !== null && m.rates.roas < target ? "text-neg" : "text-good"}`}>{times(m.rates.roas)}</td>
                  <td className="r">{m.rates.cpaCents === null ? "–" : euro(m.rates.cpaCents)}</td>
                  <td className="r">{pct(m.rates.ctr, 2)}</td>
                  <td className="r">{m.rates.cpmCents === null ? "–" : euro(m.rates.cpmCents)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      </div>

      <Card title="Copy-bibliotheek: bewezen teksten">
        <div className="grid gap-3 md:grid-cols-2">
          {lib.map((c, i) => (
            <div key={i} className="rounded-lg border border-line p-3 text-sm">
              <div className="flex items-center justify-between gap-2">
                <div className="font-medium">{c.title ?? "(geen titel)"}</div>
                <VerdictPill v={c.verdict} />
              </div>
              <p className="mt-1 whitespace-pre-line text-ink-2">{c.body}</p>
              <div className="mt-2 text-xs text-ink-3">
                {euro(c.totals.spendCents, true)} spend · ROAS {times(c.rates.roas)} · CPA {c.rates.cpaCents === null ? "–" : euro(c.rates.cpaCents)} · {c.concepts.join(", ")}
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
