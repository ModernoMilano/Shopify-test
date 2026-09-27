/** Periodes en dagen in de tijdzone van de winkel (Amsterdam). */

export const TZ = "Europe/Amsterdam";

const dayFmt = new Intl.DateTimeFormat("en-CA", { timeZone: TZ, year: "numeric", month: "2-digit", day: "2-digit" });

/** "2026-09-27" in Amsterdamse tijd. */
export function dayKey(d: Date): string {
  return dayFmt.format(d);
}

function tzOffsetMs(at: Date): number {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: TZ,
    hourCycle: "h23",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  }).formatToParts(at);
  const get = (t: string) => Number(parts.find((p) => p.type === t)!.value);
  const asUtc = Date.UTC(get("year"), get("month") - 1, get("day"), get("hour"), get("minute"), get("second"));
  return asUtc - at.getTime();
}

/** Middernacht Amsterdamse tijd van de gegeven dag ("YYYY-MM-DD") als UTC-instant. */
export function startOfDay(key: string): Date {
  const [y, m, d] = key.split("-").map(Number);
  const guess = new Date(Date.UTC(y, m - 1, d));
  return new Date(guess.getTime() - tzOffsetMs(guess));
}

export function addDays(key: string, n: number): string {
  const [y, m, d] = key.split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, d + n)).toISOString().slice(0, 10);
}

export type Period = {
  preset: string;
  /** eerste dag, inclusief */
  fromKey: string;
  /** laatste dag, inclusief */
  toKey: string;
  from: Date;
  /** exclusief */
  to: Date;
  label: string;
};

export const PRESETS: { id: string; label: string }[] = [
  { id: "today", label: "Vandaag" },
  { id: "yesterday", label: "Gisteren" },
  { id: "thisweek", label: "Deze week" },
  { id: "lastweek", label: "Vorige week" },
  { id: "mtd", label: "Deze maand" },
  { id: "lastmonth", label: "Vorige maand" },
  { id: "30d", label: "Laatste 30 dagen" },
];

/** maandag van de week van `key` */
function mondayOf(key: string): string {
  const [y, m, d] = key.split("-").map(Number);
  const dow = new Date(Date.UTC(y, m - 1, d)).getUTCDay(); // 0 = zondag
  return addDays(key, -((dow + 6) % 7));
}

const isKey = (s: string | undefined): s is string => !!s && /^\d{4}-\d{2}-\d{2}$/.test(s);

export function resolvePeriod(
  params: { p?: string; from?: string; to?: string },
  now = new Date(),
  defaultPreset = "30d",
): Period {
  const today = dayKey(now);
  let fromKey: string;
  let toKey = today;
  let preset = params.p ?? defaultPreset;

  if (isKey(params.from) && isKey(params.to) && params.from <= params.to) {
    preset = "custom";
    fromKey = params.from;
    toKey = params.to;
  } else {
    switch (preset) {
      case "today":
        fromKey = today;
        break;
      case "yesterday":
        fromKey = toKey = addDays(today, -1);
        break;
      case "thisweek":
        fromKey = mondayOf(today);
        break;
      case "lastweek":
        fromKey = addDays(mondayOf(today), -7);
        toKey = addDays(fromKey, 6);
        break;
      case "7d":
        fromKey = addDays(today, -6);
        break;
      case "mtd":
        fromKey = today.slice(0, 8) + "01";
        break;
      case "lastmonth": {
        const firstThisMonth = today.slice(0, 8) + "01";
        toKey = addDays(firstThisMonth, -1);
        fromKey = toKey.slice(0, 8) + "01";
        break;
      }
      case "90d":
        fromKey = addDays(today, -89);
        break;
      default:
        preset = "30d";
        fromKey = addDays(today, -29);
    }
  }

  const label = PRESETS.find((p) => p.id === preset)?.label ?? `${fromKey} t/m ${toKey}`;
  return { preset, fromKey, toKey, from: startOfDay(fromKey), to: startOfDay(addDays(toKey, 1)), label };
}

export function eachDay(fromKey: string, toKey: string): string[] {
  const out: string[] = [];
  for (let k = fromKey; k <= toKey; k = addDays(k, 1)) out.push(k);
  return out;
}

/** Vorige periode van dezelfde lengte, om te vergelijken. */
export function previousPeriod(p: Period): Period {
  const days = eachDay(p.fromKey, p.toKey).length;
  const toKey = addDays(p.fromKey, -1);
  const fromKey = addDays(toKey, -(days - 1));
  return { preset: "custom", fromKey, toKey, from: startOfDay(fromKey), to: startOfDay(addDays(toKey, 1)), label: "vorige periode" };
}
