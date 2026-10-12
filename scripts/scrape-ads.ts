/**
 * Creative engine: alle advertenties uit het Meta-account ophalen (via Windsor.ai), analyseren en opslaan.
 *
 * Gebruik:
 *   npm run ads:scrape                               # april 2026 t/m nu, via Windsor (WINDSOR_API_KEY)
 *   npm run ads:scrape -- --from 2026-04 --to 2026-10
 *   npm run ads:scrape -- --raw-dir pad/naar/map     # ruwe Windsor-JSON per maand (metrics-/video-/creative-YYYY-MM.json)
 *   npm run ads:scrape -- --no-db                    # alleen JSON en rapport, niets in de database
 *
 * Schrijft scripts/data/meta-ads.json (alle ads met cijfers per maand) en docs/creative-insights.md,
 * en zet alles in de database als DATABASE_URL is ingesteld.
 */
import fs from "node:fs";
import path from "node:path";
import { fetchRawMonth, mergeRaw, monthsBetween, type RawMonth, type RawRow } from "../src/creative/windsor-ads";
import { renderReport } from "../src/creative/report";
import { DEFAULT_THRESHOLDS } from "../src/creative/analysis";

const arg = (k: string) => {
  const i = process.argv.indexOf(k);
  return i >= 0 ? process.argv[i + 1] : undefined;
};
const from = arg("--from") ?? "2026-04";
const to = arg("--to") ?? new Date().toISOString().slice(0, 7);
const rawDir = arg("--raw-dir");
const noDb = process.argv.includes("--no-db") || !process.env.DATABASE_URL;
const target = Number(arg("--target") ?? DEFAULT_THRESHOLDS.targetRoas);

function readRaw(dir: string, group: string, month: string): RawRow[] {
  const rows: RawRow[] = [];
  for (const f of fs.readdirSync(dir)) {
    if (!f.startsWith(`${group}-${month}`) || !f.endsWith(".json")) continue;
    const json = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8")) as { result?: RawRow[]; data?: RawRow[] };
    rows.push(...(json.result ?? json.data ?? []));
  }
  return rows;
}

async function main() {
  const months = monthsBetween(from, to);
  const raw: RawMonth[] = [];
  for (const month of months) {
    if (rawDir) {
      raw.push({ month, metrics: readRaw(rawDir, "metrics", month), video: readRaw(rawDir, "video", month), creative: readRaw(rawDir, "creative", month) });
    } else {
      process.stdout.write(`Windsor ${month}… `);
      raw.push(await fetchRawMonth(month));
      console.log(`${raw.at(-1)!.metrics.length} rijen`);
    }
  }
  const ads = mergeRaw(raw);
  const outData = path.join("scripts", "data", "meta-ads.json");
  fs.mkdirSync(path.dirname(outData), { recursive: true });
  fs.writeFileSync(outData, JSON.stringify({ generatedAt: new Date().toISOString(), from, to, ads }, null, 1));
  const report = renderReport(ads, { ...DEFAULT_THRESHOLDS, targetRoas: target });
  fs.mkdirSync("docs", { recursive: true });
  fs.writeFileSync(path.join("docs", "creative-insights.md"), report);
  console.log(`${ads.length} advertenties, ${ads.reduce((n, a) => n + a.months.length, 0)} maandregels → ${outData}, docs/creative-insights.md`);

  if (!noDb) {
    const { saveAds } = await import("../src/creative/sync");
    const { db } = await import("../src/lib/db");
    const r = await saveAds(ads);
    console.log(`Database: ${r.ads} ads, ${r.months} maandregels`);
    await db.$disconnect();
  }
}

main().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
