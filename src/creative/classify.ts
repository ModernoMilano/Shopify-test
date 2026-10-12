/**
 * Classificatie van advertenties: concept (zonder "- Copy"), invalshoek, formaat en markt.
 * Pure functies, zonder database.
 */
import { marketOf } from "@/finance/meta";
import type { AdFormat, Angle } from "./types";

/** "BUNDLE AD 8 - Copy 2" en "BUNDLE AD 8 - Kopie" zijn dezelfde creative. */
export function conceptKey(adName: string): string {
  return adName
    .replace(/(\s*[-–—]\s*(copy|kopie)(\s*\d+)?)+\s*$/i, "")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}

/** Nette weergavenaam van een concept: eerste ad-naam zonder kopie-suffix. */
export function conceptLabel(adName: string): string {
  return adName.replace(/(\s*[-–—]\s*(copy|kopie)(\s*\d+)?)+\s*$/i, "").replace(/\s+/g, " ").trim();
}

export function angleOf(input: { name: string; title?: string | null; body?: string | null; adsetName?: string | null }): Angle {
  const name = input.name.toLowerCase();
  const title = (input.title ?? "").toLowerCase();
  const body = (input.body ?? "").toLowerCase();
  const strong = `${name} ${title}`; // naam en titel wegen zwaarder dan de body
  const all = `${strong} ${body}`;
  const sale = /\d+%|sale|off\b|half price|soldes|rabatt|%/;
  if (/\{\{product\.name\}\}/.test(title) || /catalog/.test(name)) return "catalogus";
  if (/unboxing|delivered properly|packaging/.test(all)) return "unboxing";
  if (/reverso/.test(strong)) return "reverso";
  if (/lounge/.test(strong)) return "lounge";
  if (/ugc/.test(name)) return "ugc";
  if (/cashmere|\bcash\b/.test(strong)) return sale.test(all) ? "cashmere_sale" : "cashmere";
  if (/bundle|complete the look|matching for you|one price|buying looks|one outfit|bundled|komplette.? look|looks zu/.test(all)) return "bundel";
  if (/jacket/.test(name)) return "jacket";
  if (/summer|sommer|soldes|été|stadium|stadion|voetbal|game day|riviera|monaco/.test(all)) return "zomer";
  if (/cashmere/.test(body)) return sale.test(body) ? "cashmere_sale" : "cashmere";
  if (/reverso/.test(body)) return "reverso";
  if (/lounge/.test(body)) return "lounge";
  const brand = /timeless|modern essence|milan made|quiet confidence|quiet luxury|effortless|the standard|intemporel/;
  if (brand.test(strong)) return "tijdloos";
  if (/polo|\btee\b|t-shirt|pant|linen|loafer|blazer|shirt|trousers|knit/.test(strong)) return "product";
  if (brand.test(body)) return "tijdloos";
  return "overig";
}

export function formatOf(input: { name: string; objectType?: string | null; title?: string | null; videoPlays?: number | null }): AdFormat {
  const name = input.name.toLowerCase();
  if (/\{\{product\.name\}\}/.test(input.title ?? "") || /catalog/.test(name)) return "catalogus";
  if ((input.objectType ?? "").toUpperCase() === "VIDEO") return "video";
  if (/video|unboxing/.test(name)) return "video";
  if ((input.videoPlays ?? 0) > 0) return "video";
  if ((input.objectType ?? "").toUpperCase() === "SHARE" || /img|photo|static|image/.test(name)) return "beeld";
  return input.objectType ? "beeld" : "onbekend";
}

/** Markt uit campagnenaam, inclusief de oude Nederlandse campagnenamen. */
export function marketOfCampaign(campaign: string): string {
  const c = campaign.toUpperCase();
  if (/NEDERLAND|\bNL\b/.test(c)) return "NL";
  if (/ENGELAND/.test(c)) return "UK/IE";
  if (/DUITSLAND|GERMANY/.test(c)) return "DE/AT";
  if (/\bDXB\b|DUBAI|\bUAE\b/.test(c)) return "UAE";
  if (/\bFR\b|FRANCE|FRANKRIJK/.test(c)) return "FR";
  if (/\bAU\b|\bDEN\b|\bNO\b|NORDIC/.test(c)) return "AU/Nordics";
  return marketOf(campaign);
}

/** Kenmerken van de copy, om te zien welke elementen samengaan met goede cijfers. */
export const COPY_FEATURES: { key: string; label: string; test: (title: string, body: string) => boolean }[] = [
  { key: "korting", label: "Korting / sale genoemd", test: (t, b) => /\d+%|sale|off\b|half price/i.test(t + " " + b) },
  { key: "urgentie", label: "Urgentie (limited, while it lasts)", test: (t, b) => /limited|while it lasts|once it'?s gone|now on sale/i.test(t + " " + b) },
  { key: "bundel", label: "Bundel / save", test: (t, b) => /bundle|save|complete the look|one price/i.test(t + " " + b) },
  { key: "garanties", label: "Garantielijst (✅ levering, geld terug, Klarna)", test: (t, b) => /✅|✔|money-back|klarna|pay later|tracked/i.test(b) },
  { key: "vraag", label: "Vraag als hook", test: (_t, b) => /\?/.test(b.split(/[.!\n]/)[0] ?? "") },
  { key: "herkomst", label: "Italië / Milaan", test: (t, b) => /ital|milan/i.test(t + " " + b) },
  { key: "comfort", label: "Zacht / comfort", test: (t, b) => /soft|comfort/i.test(t + " " + b) },
  { key: "tijdloos", label: "Tijdloos / kwaliteit", test: (t, b) => /timeless|last|quality|refined/i.test(t + " " + b) },
  { key: "kort", label: "Korte body (< 120 tekens)", test: (_t, b) => b.length > 0 && b.length < 120 },
  { key: "lang", label: "Lange body (> 250 tekens)", test: (_t, b) => b.length > 250 },
];

export function copyFeatures(title: string | null, body: string | null): string[] {
  const t = title ?? "";
  const b = body ?? "";
  if (!t && !b) return [];
  return COPY_FEATURES.filter((f) => f.test(t, b)).map((f) => f.key);
}
