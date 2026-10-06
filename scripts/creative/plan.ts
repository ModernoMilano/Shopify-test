// Maakt een contentplan met looks, beeldtypes en complete beeldprompts.
//   npm run creative:plan -- --posts 9 --start 2026-10-12 --seed 3 --anchor milano-cashmere-torino-blazer-perla
//   --casting "<<<element-id>>>, calm expression"  vervangt het standaardmodel (bv. een vast Higgsfield Element)
// Schrijft creative-engine/output/plan-<start>.json (voor Claude/Higgsfield) en .md (om te lezen).
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { makePlan, type PlanEntry } from "../../src/creative/plan";
import type { WardrobeItem } from "../../src/creative/wardrobe";

const ROOT = path.resolve(__dirname, "../../creative-engine");
const arg = (name: string) => {
  const i = process.argv.indexOf(`--${name}`);
  return i > -1 ? process.argv[i + 1] : undefined;
};
const args = (name: string) => process.argv.flatMap((a, i) => (a === `--${name}` ? [process.argv[i + 1]] : []));

const wardrobe: WardrobeItem[] = JSON.parse(readFileSync(path.join(ROOT, "data/wardrobe.json"), "utf8")).items;
const bestTitles: string[] = JSON.parse(readFileSync(path.join(ROOT, "data/bestsellers.json"), "utf8")).titles;
const prefer = bestTitles.map((t) => wardrobe.find((w) => w.title === t)?.handle).filter((h): h is string => Boolean(h));

const start = new Date(arg("start") ?? new Date().toISOString().slice(0, 10));
const plan = makePlan(wardrobe, {
  start,
  posts: Number(arg("posts") ?? 9),
  seed: Number(arg("seed") ?? 1),
  anchors: args("anchor"),
  prefer,
  casting: arg("casting"),
});

function md(entries: PlanEntry[]): string {
  const out = [`# Contentplan vanaf ${start.toISOString().slice(0, 10)}`, ""];
  for (const e of entries) {
    out.push(`## ${e.n}. ${e.date} · ${e.pillar} · ${e.format}`, "");
    out.push(`**Look:** ${e.look.name} (${e.look.source === "house" ? "huislook" : "samengesteld"})`, "");
    for (const { item, as } of e.look.items) out.push(`- ${item.title} (${as.join("/")}) · €${item.priceEur}${item.url ? ` · ${item.url}` : ""}`);
    out.push("", `**Invalshoek caption:** ${e.angle}`, "");
    for (const f of e.frames) {
      out.push(`### Beeld: ${f.shot.name} (${f.request.aspect})`, "", "Referenties:");
      f.request.references.forEach((r, i) => out.push(`${i + 1}. ${r.label}: ${r.url}`));
      out.push("", "```text", f.request.prompt, "```", "");
    }
  }
  return out.join("\n");
}

mkdirSync(path.join(ROOT, "output"), { recursive: true });
const base = path.join(ROOT, "output", `plan-${start.toISOString().slice(0, 10)}`);
writeFileSync(`${base}.json`, JSON.stringify(plan, null, 1) + "\n");
writeFileSync(`${base}.md`, md(plan));
console.log(`${plan.length} posts → ${path.relative(process.cwd(), base)}.{json,md}`);
for (const e of plan) console.log(`${e.n}. ${e.date} ${e.pillar.padEnd(9)} ${e.frames.map((f) => f.shot.id).join("+").padEnd(28)} ${e.look.name}`);
