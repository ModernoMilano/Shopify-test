import { describe, expect, it } from "vitest";
import { angleOf, conceptKey, conceptLabel, copyFeatures, formatOf, marketOfCampaign } from "./classify";

describe("classificatie", () => {
  it("concept zonder kopie-suffix", () => {
    expect(conceptKey("BUNDLE AD 8 - Copy 2")).toBe("bundle ad 8");
    expect(conceptKey("MM WIN 1 - Kopie - Kopie")).toBe("mm win 1");
    expect(conceptKey("MM_Bestseller_Jacket_Studio_01 - Copy 3")).toBe("mm_bestseller_jacket_studio_01");
    expect(conceptKey("Ad 5 — Bundle & Save (navy vest, tee, trousers) - Copy 4")).toBe("ad 5 — bundle & save (navy vest, tee, trousers)");
    expect(conceptLabel("UNBOXING - Copy")).toBe("UNBOXING");
  });

  it("invalshoek", () => {
    expect(angleOf({ name: "CATALOG AD DE - Copy", title: "{{product.name}}" })).toBe("catalogus");
    expect(angleOf({ name: "UNBOXING", title: "Luxury, Delivered Properly." })).toBe("unboxing");
    expect(angleOf({ name: "CASHMERE SALE", title: "50% Off Cashmere. While It Lasts." })).toBe("cashmere_sale");
    expect(angleOf({ name: "WW NATION", body: "Autumn is coming. Meet it in cashmere." })).toBe("cashmere");
    expect(angleOf({ name: "BATCH 3 4", title: "Bundle Up, Save More" })).toBe("bundel");
    expect(angleOf({ name: "UGC_BundleSave_Beige_Static_v1" })).toBe("ugc");
    expect(angleOf({ name: "Lounge-set | Video Ad 2" })).toBe("lounge");
    expect(angleOf({ name: "Reverso Set | IMG 1" })).toBe("reverso");
    expect(angleOf({ name: "Photo-Closeup-Polo-Beach", title: "Timeless Style. Modern Essence." })).toBe("tijdloos");
    expect(angleOf({ name: "MM_Bestseller_Jacket_Studio_01" })).toBe("jacket");
    expect(angleOf({ name: "SUMMER AD 4" })).toBe("zomer");
    expect(angleOf({ name: "AD 2" })).toBe("overig");
  });

  it("formaat", () => {
    expect(formatOf({ name: "Lounge-set | Video Ad 2", objectType: "SHARE" })).toBe("video");
    expect(formatOf({ name: "MM_Bestseller_Jacket_Studio_01", objectType: "VIDEO" })).toBe("video");
    expect(formatOf({ name: "CT | Week 1 | IMG 5", objectType: "SHARE" })).toBe("beeld");
    expect(formatOf({ name: "CATALOG AD DE", title: "{{product.name}}" })).toBe("catalogus");
    expect(formatOf({ name: "AD 2", objectType: null, videoPlays: 120 })).toBe("video");
    expect(formatOf({ name: "AD 2", objectType: null })).toBe("onbekend");
  });

  it("markt, ook oude Nederlandse namen", () => {
    expect(marketOfCampaign("ModernoMilano NEDERLAND")).toBe("NL");
    expect(marketOfCampaign("ModernoMilano ENGELAND")).toBe("UK/IE");
    expect(marketOfCampaign("SUMMER COLLECTION GERMANY")).toBe("DE/AT");
    expect(marketOfCampaign("MM | UK  | SCALING | CBO")).toBe("UK/IE");
    expect(marketOfCampaign("Nasir | Worldwide | Retargeting Campaign - 24/09/2026")).toBe("Worldwide");
  });

  it("copy-kenmerken", () => {
    expect(copyFeatures("Up To 50% OFF - Limited Stock", "A style worth coming back to. ✅Premium tracked worldwide delivery. ✅30-day money-back guarantee.")).toEqual(
      expect.arrayContaining(["korting", "urgentie", "garanties"]),
    );
    expect(copyFeatures("We did the matching for you", "Tired of guessing what goes with what? Every ModernoMilano set is already put together for you.")).toEqual(
      expect.arrayContaining(["vraag", "kort"]),
    );
    expect(copyFeatures(null, null)).toEqual([]);
  });
});
