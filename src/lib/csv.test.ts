import { describe, expect, it } from "vitest";
import { parseCostCsv, parseCsv, toCsv } from "./csv";
import { parseEuroToCents } from "./money";

describe("csv", () => {
  it("leest ; en , en quotes", () => {
    expect(parseCsv('a;b\n"x;y";2')).toEqual([["a", "b"], ["x;y", "2"]]);
    expect(parseCsv('a,b\r\n"he said ""hi""",3\n')).toEqual([["a", "b"], ['he said "hi"', "3"]]);
  });

  it("round-trip met toCsv", () => {
    const rows = [["product_id", "titel"], ["1", 'Set "Black", L']];
    expect(parseCsv(toCsv(rows))).toEqual(rows);
  });

  it("parseert kostprijzen met NL-notatie en slaat lege over", () => {
    const { rows, errors } = parseCostCsv(
      "product_id;titel;kostprijs;verzendkosten;leverancier\n1;A;12,50;4,95;CJ\n2;B;;;\n3;C;abc;;",
    );
    expect(rows).toEqual([{ line: 2, product: "1", unitCostCents: 1250, shippingCostCents: 495, supplier: "CJ" }]);
    expect(errors).toEqual(['Regel 4: ongeldige kostprijs "abc"']);
  });

  it("euro parsing", () => {
    expect(parseEuroToCents("€ 1.234,56")).toBe(123456);
    expect(parseEuroToCents("12.5")).toBe(1250);
    expect(parseEuroToCents("")).toBeNull();
  });
});

describe("export → import", () => {
  it("leest een geëxporteerd bestand (BOM, puntkomma) terug", () => {
    const exported =
      "﻿" +
      toCsv(
        [
          ["product_id", "titel", "status", "verkoopprijs", "kostprijs", "verzendkosten", "leverancier"],
          ["42", "MILANO SET, BLACK", "ACTIVE", "150,00", "38,50", "7,00", "Supplier X"],
        ],
        ";",
      );
    expect(parseCostCsv(exported).rows).toEqual([
      { line: 2, product: "42", unitCostCents: 3850, shippingCostCents: 700, supplier: "Supplier X" },
    ]);
  });
});
