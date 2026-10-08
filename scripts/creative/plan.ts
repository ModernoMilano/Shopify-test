// Maakt een contentplan volgens de norm, met looks, beeldtypes, complete beeldprompts, reels en een captionopzet.
//   npm run creative:plan -- --posts 9 --start 2026-10-12 --seed 3 --anchor milano-cashmere-torino-blazer-perla
// Het model is altijd hetzelfde (creative-engine/data/model.json); daar is geen optie voor. Zijn gezicht komt via het
// Higgsfield-element. Werkt het element niet, voeg dan --face-refs toe: dan gaan zijn gezichtsfoto's als #1-#3 mee.
// Schrijft creative-engine/output/plan-<start>.json (voor Claude/Higgsfield) en .md (om te lezen).
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { MODEL } from "../../src/creative/casting";
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
  faces: process.argv.includes("--face-refs") ? "refs" : "element",
});

const FORMAT = { single: "los beeld", carousel: "carrousel", reel: "reel" };

function md(entries: PlanEntry[]): string {
  const out = [
    `# Contentplan vanaf ${start.toISOString().slice(0, 10)}`,
    "",
    "Gelezen in rijen van 3. Regels: `creative-engine/brand/norm.md`.",
    "",
    `Model: altijd hetzelfde (\`creative-engine/data/model.json\`), element \`${MODEL.elementPlaceholder}\`. ` +
      (process.argv.includes("--face-refs")
        ? "Terugval zonder element: in elk beeld met hem staan zijn gezichtsfoto's (4K) als eerste referenties, daarna de producten. "
        : "Zijn gezicht komt via het element; de referenties zijn alleen productfoto's. ") +
      `Stuur \`medias\` in precies de volgorde van de referenties. Maximaal ${MODEL.batchMax} beelden per batch.`,
    "",
  ];
  for (const e of entries) {
    out.push(`## ${e.n}. ${e.date} · ${e.pillar} · ${FORMAT[e.format]}`, "");
    out.push(`**Look:** ${e.look.name} (${e.look.source === "house" ? "huislook" : "samengesteld"})`, "");
    for (const { item, as } of e.look.items) out.push(`- ${item.title} (${as.join("/")}) · €${item.priceEur}${item.url ? ` · ${item.url}` : ""}`);
    out.push("", `**Caption:** ${e.caption.angle}`, "", "```text", "<kop>", "<een of twee zinnen>", e.caption.wearing, "", e.caption.hashtags.join(" "), "```", "");
    e.frames.forEach((f, i) => {
      out.push(`### Beeld ${i + 1}: ${f.shot.name} (${f.request.aspect})`, "", "Referenties:");
      f.request.references.forEach((r, j) => out.push(`${j + 1}. ${r.label}: ${r.url}${r.mediaId ? ` (id voor medias: ${r.mediaId})` : ""}`));
      out.push("", "```text", f.request.prompt, "```", "");
    });
    if (e.video) {
      const refs = e.video.faceRefs.length ? `, gezichtsfoto's ${e.video.faceRefs.map((r) => `${r.id} (${r.upscaleJobId})`).join(" en ")} als image_references` : "";
      out.push(
        `### Reel (${e.video.model}, ${e.video.mode}, ${e.video.resolution}, ${e.video.duration} s, ${e.video.aspect}, zonder geluid, startframe = goedgekeurd beeld 1${refs}; eerst een concept in 480p)`,
        "", "```text", e.video.prompt, "```", "",
      );
    }
  }
  return out.join("\n");
}

mkdirSync(path.join(ROOT, "output"), { recursive: true });
const base = path.join(ROOT, "output", `plan-${start.toISOString().slice(0, 10)}`);
writeFileSync(`${base}.json`, JSON.stringify(plan, null, 1) + "\n");
writeFileSync(`${base}.md`, md(plan));
console.log(`${plan.length} posts → ${path.relative(process.cwd(), base)}.{json,md}`);
for (const e of plan) {
  console.log(`${String(e.n).padStart(2)}. ${e.date} ${e.pillar.padEnd(9)} ${FORMAT[e.format].padEnd(10)} ${e.frames.map((f) => f.shot.id).join(" + ").padEnd(58)} ${e.look.name}`);
}
