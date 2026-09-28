import fs from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import { DEFAULT_RULES, matchRule, totalsByCategory } from "./categories";
import { parseDutchDate, parseEuroAmount, parseRevolutCsv, parseRevolutPdf, parseRevolutPdfItems, reconcile, type PdfTextItem } from "./revolut";

describe("hulpfuncties", () => {
  it("datums en bedragen", () => {
    expect(parseDutchDate("1 sep 2026")).toBe("2026-09-01");
    expect(parseDutchDate("27 okt 2026")).toBe("2026-10-27");
    expect(parseEuroAmount("€1.836,01")).toBe(183601);
    expect(parseEuroAmount("$60,00")).toBeNull();
  });
});

describe("PDF-regels", () => {
  // Nagebouwd uit de posities in een echt Revolut-afschrift
  const it_ = (x: number, y: number, str: string): PdfTextItem => ({ page: 1, x, y, str });
  const items = [
    it_(43, 529, "Pro"), it_(253, 529, "€100,00"), it_(335, 529, "€50,00"), it_(417, 529, "€20,00"), it_(519, 529, "€70,00"),
    it_(43, 420, "Datum"), it_(125, 420, "Beschrijving"), it_(335, 420, "Uitgegeven geld"), it_(417, 420, "Ontvangen geld"), it_(535, 420, "Saldo"),
    it_(43, 401, "1 sep 2026"), it_(125, 401, "To Jinjiang Yuguang Trading Co., Ltd."), it_(335, 401, "€50,00"), it_(526, 401, "€50,00"),
    it_(125, 394, "Kosten: €0,72"), it_(335, 394, "€49,28"),
    it_(125, 388, "Aan: Jinjiang Yuguang Trading Co., Ltd., 123"),
    it_(43, 372, "2 sep 2026"), it_(125, 372, "Betaling van PAYPAL"), it_(417, 372, "€20,00"), it_(526, 372, "€70,00"),
    it_(125, 364, "Referentie: INSTANT TRANSFER"),
    it_(200, 36, "Pagina 1 van 1"),
  ];

  it("leest uit, in, saldo en transferkosten", () => {
    const s = parseRevolutPdfItems(items);
    expect(s.openingBalanceCents).toBe(10000);
    expect(s.closingBalanceCents).toBe(7000);
    expect(s.transactions).toHaveLength(2);
    expect(s.transactions[0]).toMatchObject({ date: "2026-09-01", amountCents: -5000, feeCents: 72, balanceCents: 5000 });
    expect(s.transactions[1]).toMatchObject({ amountCents: 2000, balanceCents: 7000 });
    expect(s.transactions[1].details).toContain("INSTANT TRANSFER");
    expect(reconcile(s).ok).toBe(true);
  });

  it("transferkosten gaan naar bankkosten", () => {
    const s = parseRevolutPdfItems(items);
    const txs = s.transactions.map((t) => ({ ...t, category: matchRule(t, DEFAULT_RULES)?.category ?? "unknown" }));
    const totals = totalsByCategory(txs);
    expect(totals.get("cogs")).toBe(-4928);
    expect(totals.get("bank_fees")).toBe(-72);
    expect(totals.get("paypal_payout")).toBe(2000);
  });
});

describe("CSV", () => {
  it("Revolut Business-export", () => {
    const csv = [
      "Date started (UTC),Date completed (UTC),ID,Type,State,Description,Reference,Payer,Amount,Fee,Balance",
      "2026-09-04,2026-09-04,a,TOPUP,COMPLETED,Payment from HR RJ KOMEN,Lening,HR RJ KOMEN,10000.00,0.00,10100.00",
      "2026-09-05,2026-09-05,b,TRANSFER,COMPLETED,To EAST BAITE LIMITED,,,-2000.00,-0.50,8099.50",
      "2026-09-05,,c,CARD_PAYMENT,DECLINED,Facebook,,,-10.00,0,8099.50",
    ].join("\n");
    const s = parseRevolutCsv(csv);
    expect(s.transactions).toHaveLength(2);
    expect(s.transactions[1]).toMatchObject({ amountCents: -200050, feeCents: 50, balanceCents: 809950 });
    expect(reconcile(s).ok).toBe(true);
    expect(matchRule(s.transactions[0], DEFAULT_RULES)?.category).toBe("loan");
  });
});

// Echte data (staat niet in git). Draait alleen als het afschrift lokaal aanwezig is.
const fixture = path.join(process.cwd(), "fixtures/private/revolut-2026-09.pdf");
describe.skipIf(!fs.existsSync(fixture))("Revolut september 2026 (spec 5.3)", () => {
  it("sluit tot op de cent en categorieën kloppen", async () => {
    const s = await parseRevolutPdf(new Uint8Array(fs.readFileSync(fixture)));
    const rec = reconcile(s);
    expect(s.transactions).toHaveLength(159);
    expect(rec.opening).toBe(183601);
    expect(rec.closing).toBe(841116);
    expect(rec.ok).toBe(true);

    const txs = s.transactions.map((t) => ({ ...t, category: matchRule(t, DEFAULT_RULES)?.category ?? "unknown" }));
    // Ok (Alkmaar) en Sona hebben geen regel: die wijst de gebruiker toe. In de spec vallen ze onder software.
    const unknown = txs.filter((t) => t.category === "unknown");
    expect(unknown.map((t) => t.description).sort()).toEqual(["Ok", "Sona"]);
    for (const t of unknown) t.category = "software";

    const tot = totalsByCategory(txs);
    const eur = (id: string) => (tot.get(id) ?? 0) / 100;
    expect(eur("shopify_payout")).toBe(56903.77);
    expect(eur("paypal_payout")).toBe(13048);
    expect(eur("loan")).toBe(10000);
    expect(eur("owner_deposit")).toBe(150);
    expect(eur("meta")).toBe(-35248.69);
    expect(eur("cogs")).toBe(-31095.6);
    expect(eur("private")).toBe(-5705);
    expect(eur("software")).toBe(-1022.64);
    expect(eur("freelancers")).toBe(-346.12);
    expect(eur("accountant")).toBe(-88.21);
    expect(eur("bank_fees")).toBe(-20.36);
    expect(eur("internal")).toBe(0);
    expect(txs.filter((t) => t.category === "shopify_payout")).toHaveLength(16);
    expect(txs.filter((t) => t.category === "paypal_payout")).toHaveLength(30);
    expect([s.periodFrom, s.periodTo]).toEqual(["2026-09-01", "2026-09-27"]);
  }, 30_000);
});
