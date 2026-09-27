import { describe, expect, it } from "vitest";
import { budgetWarnings, marketOf } from "./meta";

describe("Meta", () => {
  it("markt uit campagnenaam", () => {
    expect(marketOf("MM | UK  | SCALING | CBO")).toBe("UK/IE");
    expect(marketOf("Nasir | UK+IE LAL Sales Campaign -  22/09/2026")).toBe("UK/IE");
    expect(marketOf("MM | DEU | SCALING | CBO")).toBe("DE/AT");
    expect(marketOf("MM | DE  | TESTING | ABO")).toBe("DE/AT");
    expect(marketOf("USA CBO")).toBe("USA");
    expect(marketOf("Nasir | USA | LAL Sales Campaign - 23/09/2026")).toBe("USA");
    expect(marketOf("SWIS CBO")).toBe("CH");
    expect(marketOf("MODERNO WORLDWIDE TEST")).toBe("Worldwide");
    expect(marketOf("WORLDWIDE 2.0")).toBe("Worldwide");
  });

  it("budgetprotocol", () => {
    const d = (s: string) => new Date(`${s}T00:00:00Z`);
    const w = budgetWarnings([
      { id: "a", date: d("2026-09-01"), campaign: "UK", oldCents: 10000, newCents: 12000 },
      { id: "b", date: d("2026-09-03"), campaign: "UK", oldCents: 12000, newCents: 15000 },
    ]);
    expect(w.filter((x) => x.id === "a")).toHaveLength(0);
    expect(w.filter((x) => x.id === "b").map((x) => x.message)).toEqual([
      "Verhoging van 25%, meer dan 20%",
      "Maar 2 dag(en) na de vorige ingreep, minimaal 3",
    ]);
  });
});
