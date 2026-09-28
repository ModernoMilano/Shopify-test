import { describe, expect, it } from "vitest";
import { coverageFrom, mergeRanges } from "./coverage";
import { parseStatementPeriod } from "@/bank/revolut";

describe("dekking bankafschriften", () => {
  it("voegt aansluitende en overlappende periodes samen", () => {
    expect(
      mergeRanges([
        { from: "2026-09-01", to: "2026-09-27" },
        { from: "2026-08-01", to: "2026-08-31" },
        { from: "2026-09-20", to: "2026-09-30" },
      ]),
    ).toEqual([{ from: "2026-08-01", to: "2026-09-30" }]);
  });

  it("meldt gaten en vanaf wanneer een afschrift nodig is", () => {
    const c = coverageFrom(
      [
        { from: "2026-07-01", to: "2026-07-31" },
        { from: "2026-09-01", to: "2026-09-27" },
      ],
      "2026-10-05",
    );
    expect(c.gaps).toEqual([{ from: "2026-08-01", to: "2026-08-31" }]);
    expect(c.lastDate).toBe("2026-09-27");
    expect(c.missingFrom).toBe("2026-09-28");
    expect(c.missingDays).toBe(7); // 28 sep t/m 4 okt
  });

  it("bijgewerkt tot en met gisteren is compleet", () => {
    expect(coverageFrom([{ from: "2026-09-01", to: "2026-09-27" }], "2026-09-28").missingFrom).toBeNull();
    expect(coverageFrom([], "2026-09-28").lastDate).toBeNull();
  });

  it("leest de periode uit de kop van het Revolut-afschrift", () => {
    expect(parseStatementPeriod("Pro-transacties van 1 september 2026 aan 27 september 2026")).toEqual(["2026-09-01", "2026-09-27"]);
    expect(parseStatementPeriod("Transactions from 1 October 2026 to 31 October 2026")).toEqual(["2026-10-01", "2026-10-31"]);
  });
});
