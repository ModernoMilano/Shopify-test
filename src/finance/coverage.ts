/**
 * Welke periode dekken de geïmporteerde bankafschriften, en vanaf wanneer ontbreekt er iets?
 * Het uploaden van het afschrift is de enige handmatige stap; het dashboard zegt precies welke data nodig is.
 */
import { db } from "@/lib/db";
import { dayKey } from "@/lib/period";
import { addDaysKey } from "./calculations";

export type Range = { from: string; to: string };

/** Voeg overlappende of aansluitende periodes samen. */
export function mergeRanges(ranges: Range[]): Range[] {
  const sorted = [...ranges].filter((r) => r.from <= r.to).sort((a, b) => a.from.localeCompare(b.from));
  const out: Range[] = [];
  for (const r of sorted) {
    const last = out[out.length - 1];
    if (last && r.from <= addDaysKey(last.to, 1)) {
      if (r.to > last.to) last.to = r.to;
    } else out.push({ ...r });
  }
  return out;
}

export type Coverage = {
  ranges: Range[];
  /** gaten tussen afschriften */
  gaps: Range[];
  lastDate: string | null;
  /** vanaf welke dag een afschrift nodig is (dag na de laatste gedekte dag), null als alles tot vandaag er is */
  missingFrom: string | null;
  missingDays: number;
};

export function coverageFrom(ranges: Range[], today: string): Coverage {
  const merged = mergeRanges(ranges);
  const gaps: Range[] = [];
  for (let i = 1; i < merged.length; i++) {
    gaps.push({ from: addDaysKey(merged[i - 1].to, 1), to: addDaysKey(merged[i].from, -1) });
  }
  const lastDate = merged.length ? merged[merged.length - 1].to : null;
  // het afschrift van vandaag is nooit compleet; tot en met gisteren telt als bijgewerkt
  const yesterday = addDaysKey(today, -1);
  const missingFrom = lastDate && lastDate < yesterday ? addDaysKey(lastDate, 1) : null;
  const missingDays = missingFrom
    ? Math.round((Date.parse(`${yesterday}T00:00:00Z`) - Date.parse(`${missingFrom}T00:00:00Z`)) / 86_400_000) + 1
    : 0;
  return { ranges: merged, gaps, lastDate, missingFrom, missingDays };
}

export async function bankCoverage(): Promise<Coverage> {
  const imports = await db.bankImport.findMany({ where: { periodFrom: { not: null }, periodTo: { not: null } } });
  const ranges: Range[] = imports.map((i) => ({ from: i.periodFrom!.toISOString().slice(0, 10), to: i.periodTo!.toISOString().slice(0, 10) }));
  if (!ranges.length) {
    // oudere imports zonder periode: eerste en laatste mutatie
    const agg = await db.bankTransaction.aggregate({ _min: { bookedAt: true }, _max: { bookedAt: true } });
    if (agg._min.bookedAt && agg._max.bookedAt) {
      ranges.push({ from: agg._min.bookedAt.toISOString().slice(0, 10), to: agg._max.bookedAt.toISOString().slice(0, 10) });
    }
  }
  return coverageFrom(ranges, dayKey(new Date()));
}
