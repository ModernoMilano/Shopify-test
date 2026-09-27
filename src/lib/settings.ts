import { db } from "./db";
import { DEFAULT_SETTINGS, type ProfitSettings } from "./profit";

export async function getSetting(key: string): Promise<string | null> {
  const row = await db.setting.findUnique({ where: { key } });
  return row?.value ?? null;
}

export async function setSetting(key: string, value: string): Promise<void> {
  await db.setting.upsert({ where: { key }, create: { key, value }, update: { value } });
}

export async function getProfitSettings(): Promise<ProfitSettings> {
  const raw = await getSetting("profit");
  if (!raw) return DEFAULT_SETTINGS;
  return { ...DEFAULT_SETTINGS, ...(JSON.parse(raw) as Partial<ProfitSettings>) };
}

export async function saveProfitSettings(s: ProfitSettings): Promise<void> {
  await setSetting("profit", JSON.stringify(s));
}
