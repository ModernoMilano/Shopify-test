import { describe, expect, it } from "vitest";
import { mergeRaw, monthRange, monthsBetween } from "./windsor-ads";

describe("Windsor ads", () => {
  it("maanden", () => {
    expect(monthsBetween("2026-04", "2026-10")).toEqual(["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]);
    expect(monthsBetween("2025-11", "2026-02")).toEqual(["2025-11", "2025-12", "2026-01", "2026-02"]);
    expect(monthRange("2026-09", new Date("2026-10-12T10:00:00Z"))).toEqual({ from: "2026-09-01", to: "2026-09-30" });
    expect(monthRange("2026-10", new Date("2026-10-12T10:00:00Z"))).toEqual({ from: "2026-10-01", to: "2026-10-12" });
  });

  it("voegt cijfers, video en creative samen", () => {
    const ads = mergeRaw([
      {
        month: "2026-09",
        metrics: [
          { ad_id: "1", ad_name: "UNBOXING - Copy", adset_name: "WW", campaign: "WORLDWIDE 2.0", spend: "12.5", impressions: 1000, link_clicks: 20, actions_purchase: 1, action_values_purchase: 150, frequency: 1.4 },
          { ad_id: "2", ad_name: "leeg", campaign: "x", spend: 0, impressions: 0 },
        ],
        video: [{ ad_id: "1", video_play_actions_video_view: 400, video_continuous_2_sec_watched_actions_video_view: 250, video_thruplay_watched_actions_video_view: 60 }],
        creative: [{ ad_id: "1", creative_id: "c1", effective_status: "ACTIVE", object_type: "SHARE", call_to_action_type: "SHOP_NOW", title: "Luxury, Delivered Properly.", body: "Every piece arrives the way it deserves to." }],
      },
      { month: "2026-10", metrics: [{ ad_id: "1", ad_name: "UNBOXING - Copy", campaign: "WORLDWIDE 2.0", spend: 3, impressions: 100 }], video: [], creative: [] },
    ]);
    expect(ads).toHaveLength(1);
    const a = ads[0];
    expect(a.conceptKey).toBe("unboxing");
    expect(a.angle).toBe("unboxing");
    expect(a.format).toBe("video");
    expect(a.market).toBe("Worldwide");
    expect(a.title).toBe("Luxury, Delivered Properly.");
    expect(a.months.map((m) => m.month)).toEqual(["2026-09", "2026-10"]);
    expect(a.months[0]).toMatchObject({ spendCents: 1250, impressions: 1000, linkClicks: 20, purchases: 1, purchaseValueCents: 15000, frequency: 1.4, videoPlays: 400, video2s: 250, thruplays: 60 });
    expect(a.months[1]).toMatchObject({ spendCents: 300, videoPlays: null });
  });
});
