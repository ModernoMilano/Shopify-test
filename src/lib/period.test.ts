import { describe, expect, it } from "vitest";
import { dayKey, eachDay, previousPeriod, resolvePeriod, startOfDay } from "./period";

describe("period", () => {
  it("rekent met Amsterdamse dagen (zomer- en wintertijd)", () => {
    expect(startOfDay("2026-07-01").toISOString()).toBe("2026-06-30T22:00:00.000Z");
    expect(startOfDay("2026-01-15").toISOString()).toBe("2026-01-14T23:00:00.000Z");
    expect(dayKey(new Date("2026-06-30T22:30:00Z"))).toBe("2026-07-01");
  });

  it("vorige maand", () => {
    const p = resolvePeriod({ p: "lastmonth" }, new Date("2026-09-27T10:00:00Z"));
    expect([p.fromKey, p.toKey]).toEqual(["2026-08-01", "2026-08-31"]);
    expect(p.to.toISOString()).toBe("2026-08-31T22:00:00.000Z");
  });

  it("30 dagen inclusief vandaag, en vorige periode even lang", () => {
    const p = resolvePeriod({}, new Date("2026-09-27T10:00:00Z"));
    expect(eachDay(p.fromKey, p.toKey)).toHaveLength(30);
    const prev = previousPeriod(p);
    expect(prev.toKey).toBe("2026-08-28");
    expect(eachDay(prev.fromKey, prev.toKey)).toHaveLength(30);
  });

  it("weken beginnen op maandag", () => {
    const now = new Date("2026-09-27T10:00:00Z"); // zondag
    expect([resolvePeriod({ p: "thisweek" }, now).fromKey, resolvePeriod({ p: "thisweek" }, now).toKey]).toEqual(["2026-09-21", "2026-09-27"]);
    const lw = resolvePeriod({ p: "lastweek" }, now);
    expect([lw.fromKey, lw.toKey]).toEqual(["2026-09-14", "2026-09-20"]);
    expect(resolvePeriod({ p: "yesterday" }, now).fromKey).toBe("2026-09-26");
  });

  it("eigen bereik", () => {
    const p = resolvePeriod({ from: "2026-09-01", to: "2026-09-10" });
    expect(p.preset).toBe("custom");
  });
});
