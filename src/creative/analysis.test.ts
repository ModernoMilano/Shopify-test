import { describe, expect, it } from "vitest";
import { briefs, byAngle, byFormat, concepts, copyLibrary, copyPatterns, ratesOf, totalsOf, verdictOf } from "./analysis";
import type { AdMonthMetrics, AdRecord } from "./types";

const month = (p: Partial<AdMonthMetrics>): AdMonthMetrics => ({
  month: "2026-09", spendCents: 0, impressions: 0, reach: 0, clicks: 0, linkClicks: 0, landingPageViews: 0, addToCart: 0, checkouts: 0,
  purchases: 0, purchaseValueCents: 0, frequency: null, videoPlays: null, video2s: null, thruplays: null, videoP25: null, videoP50: null,
  videoP75: null, videoP100: null, avgWatchSec: null, ...p,
});

const ad = (p: Partial<AdRecord> & { id: string; name: string }): AdRecord => ({
  adsetName: null, campaign: "MM | UK  | SCALING | CBO", market: "UK/IE", creativeId: null, status: "ACTIVE", createdAt: null, objectType: "SHARE",
  format: "beeld", angle: "bundel", conceptKey: p.name.toLowerCase(), cta: "SHOP_NOW", title: null, body: null, linkUrl: null, thumbnailUrl: null,
  imageUrl: null, instagramUrl: null, previewUrl: null, months: [], ...p,
});

const winner = ad({
  id: "1", name: "BUNDLE AD 8", title: "More Pieces. One Price.", body: "Why settle for one piece when the full set costs less together?",
  months: [month({ spendCents: 100_000, impressions: 60_000, linkClicks: 1200, landingPageViews: 1000, addToCart: 100, purchases: 12, purchaseValueCents: 300_000 })],
});
const copyOfWinner = ad({ ...winner, id: "2", name: "BUNDLE AD 8 - Copy", market: "DE/AT", campaign: "MM | DEU | SCALING | CBO",
  months: [month({ spendCents: 50_000, impressions: 30_000, linkClicks: 500, purchases: 6, purchaseValueCents: 120_000 })] });
const loser = ad({ id: "3", name: "NEW TEST 3", angle: "tijdloos", title: "Effortless", body: "Milan doesn't try.",
  months: [month({ spendCents: 20_000, impressions: 9_000, linkClicks: 100, purchases: 0 })] });
const early = ad({ id: "4", name: "CT | Week 1 | IMG 9", months: [month({ spendCents: 2_300, impressions: 400 })] });
const video = ad({ id: "5", name: "UNBOXING", angle: "unboxing", format: "video", objectType: "VIDEO",
  months: [month({ spendCents: 40_000, impressions: 20_000, linkClicks: 500, purchases: 5, purchaseValueCents: 100_000, videoPlays: 10_000, video2s: 6_000, thruplays: 2_000, videoP100: 1_000 })] });

const weak = ad({ id: "6", name: "CASHMERE SALE", angle: "cashmere_sale", title: "50% Off Cashmere", body: "Our full cashmere collection, half price.",
  months: [month({ spendCents: 12_000, impressions: 5_000, linkClicks: 80, purchases: 1, purchaseValueCents: 15_000 })] });

const ADS = [winner, copyOfWinner, loser, early, video, weak];

describe("analyse", () => {
  it("totalen en ratio's", () => {
    const t = totalsOf([winner]);
    const r = ratesOf(t);
    expect(r.roas).toBe(3);
    expect(r.cpaCents).toBe(Math.round(100_000 / 12));
    expect(r.ctr).toBeCloseTo(0.02);
    expect(r.cpmCents).toBe(Math.round((100_000 / 60_000) * 1000));
    expect(r.lpvRate).toBeCloseTo(1000 / 1200);
    expect(r.atcRate).toBeCloseTo(0.1);
    expect(r.aovCents).toBe(25_000);
    expect(r.hookRate).toBeNull();
    expect(ratesOf(totalsOf([ad({ id: "v0", name: "v0", months: [month({ impressions: 1000, videoPlays: 100, video2s: 0, thruplays: 10 })] })])).hookRate).toBeNull();
  });

  it("videocijfers", () => {
    const r = ratesOf(totalsOf([video]));
    expect(r.hookRate).toBeCloseTo(0.3);
    expect(r.holdRate).toBeCloseTo(0.2);
    expect(r.completion).toBeCloseTo(0.1);
  });

  it("oordeel", () => {
    expect(verdictOf(totalsOf([winner]))).toBe("winnaar");
    expect(verdictOf(totalsOf([loser]))).toBe("verliezer");
    expect(verdictOf(totalsOf([early]))).toBe("te vroeg");
    expect(verdictOf(totalsOf([ad({ id: "x", name: "x", months: [month({ spendCents: 15_000, purchases: 2, purchaseValueCents: 20_000 })] })]))).toBe("zwak");
    expect(verdictOf(totalsOf([ad({ id: "y", name: "y", months: [month({ spendCents: 15_000, purchases: 2, purchaseValueCents: 40_000 })] })]))).toBe("kansrijk");
  });

  it("concepten voegen kopieën samen, winnaars eerst", () => {
    const c = concepts(ADS);
    expect(c[0].label).toBe("BUNDLE AD 8");
    expect(c[0].ads).toHaveLength(2);
    expect(c[0].totals.spendCents).toBe(150_000);
    expect(c[0].verdict).toBe("winnaar");
    expect(c.map((g) => g.verdict)).toEqual(["winnaar", "winnaar", "te vroeg", "zwak", "verliezer"]);
  });

  it("per invalshoek en formaat", () => {
    expect(byAngle(ADS).map((g) => g.key)).toEqual(["bundel", "unboxing", "tijdloos", "cashmere_sale"]);
    expect(byFormat(ADS).find((g) => g.key === "video")?.totals.spendCents).toBe(40_000);
  });

  it("copy-patronen en bibliotheek", () => {
    const lib = copyLibrary(ADS);
    expect(lib[0].title).toBe("More Pieces. One Price.");
    expect(lib[0].concepts).toEqual(["BUNDLE AD 8"]);
    expect(lib[0].totals.spendCents).toBe(150_000);
    const p = copyPatterns(ADS);
    const vraag = p.find((x) => x.key === "vraag");
    expect(vraag?.ads).toBe(2);
    expect(vraag?.rates.roas).toBeCloseTo(420_000 / 150_000);
    expect(vraag?.liftVsRest).toBeGreaterThan(0);
  });

  it("recepten voor nieuwe ads", () => {
    const b = briefs(ADS);
    expect(b.map((x) => x.concept)).toEqual(["BUNDLE AD 8", "UNBOXING"]);
    expect(b[0].markets.map((m) => m.market)).toEqual(["UK/IE", "DE/AT"]);
    expect(b[0].why.some((w) => w.includes("meerdere markten"))).toBe(true);
    expect(b[0].variants.length).toBeGreaterThan(0);
  });
});
