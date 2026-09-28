/**
 * Revolut-afschriften inlezen: de PDF uit de app (Nederlands) en de CSV-export.
 * Beide leveren dezelfde ParsedStatement op.
 */
import { parseCsv } from "@/lib/csv";

export type ParsedTransaction = {
  /** "YYYY-MM-DD" */
  date: string;
  description: string;
  /** extra regels: tegenpartij, referentie, kaart, koers */
  details: string;
  /** positief = ontvangen, negatief = uitgegeven (incl. eventuele transferkosten) */
  amountCents: number;
  /** transferkosten die in het bedrag zitten */
  feeCents: number;
  balanceCents: number | null;
};

export type ParsedStatement = {
  openingBalanceCents: number | null;
  closingBalanceCents: number | null;
  /** periode van het afschrift, "YYYY-MM-DD"; bij CSV de eerste en laatste mutatie */
  periodFrom?: string | null;
  periodTo?: string | null;
  transactions: ParsedTransaction[];
};

const PERIOD = /(?:transacties van|transactions from)\s+(\d{1,2} \w+ \d{4})\s+(?:aan|tot|t\/m|to|until)\s+(\d{1,2} \w+ \d{4})/i;

/** "Pro-transacties van 1 september 2026 aan 27 september 2026" → ["2026-09-01", "2026-09-27"] */
export function parseStatementPeriod(text: string): [string, string] | null {
  const m = text.match(PERIOD);
  if (!m) return null;
  const from = parseDutchDate(m[1]);
  const to = parseDutchDate(m[2]);
  return from && to ? [from, to] : null;
}

const MONTHS: Record<string, number> = {
  jan: 1, feb: 2, mrt: 3, mar: 3, apr: 4, mei: 5, may: 5, jun: 6, jul: 7, aug: 8, sep: 9, okt: 10, oct: 10, nov: 11, dec: 12,
};

/** "1 sep 2026" → "2026-09-01" */
export function parseDutchDate(s: string): string | null {
  const m = s.trim().match(/^(\d{1,2}) (\w{3})\w* (\d{4})$/);
  if (!m) return null;
  const month = MONTHS[m[2].toLowerCase()];
  if (!month) return null;
  return `${m[3]}-${String(month).padStart(2, "0")}-${m[1].padStart(2, "0")}`;
}

/** "€1.234,56" → 123456 */
export function parseEuroAmount(s: string): number | null {
  const m = s.trim().match(/^-?€\s?(-?[\d.]+,\d{2})$/);
  if (!m) return null;
  const n = Number(m[1].replace(/\./g, "").replace(",", "."));
  return Math.round((s.trim().startsWith("-") ? -n : n) * 100);
}

// ---------------------------------------------------------------------------
// PDF

export type PdfTextItem = { page: number; x: number; y: number; str: string };

type Line = { page: number; y: number; items: PdfTextItem[] };

function toLines(items: PdfTextItem[]): Line[] {
  const lines: Line[] = [];
  const sorted = [...items].filter((i) => i.str.trim()).sort((a, b) => a.page - b.page || b.y - a.y || a.x - b.x);
  for (const it of sorted) {
    const last = lines[lines.length - 1];
    if (last && last.page === it.page && Math.abs(last.y - it.y) <= 2) last.items.push(it);
    else lines.push({ page: it.page, y: it.y, items: [it] });
  }
  for (const l of lines) l.items.sort((a, b) => a.x - b.x);
  return lines;
}

const FOOTER = /Verloren of gestolen|Revolut Bank UAB is|© \d{4} Revolut|Pagina \d/;

/** Zet de tekstfragmenten van een Revolut-PDF om in mutaties. Kolommen worden per pagina aan de kop herkend. */
export function parseRevolutPdfItems(items: PdfTextItem[]): ParsedStatement {
  const lines = toLines(items);
  const statement: ParsedStatement = { openingBalanceCents: null, closingBalanceCents: null, transactions: [] };
  let cols: { out: number; in: number; balance: number; desc: number } | null = null;
  let inTable = false;
  let current: ParsedTransaction | null = null;
  let currentDetails: string[] = [];

  const flush = () => {
    if (current) {
      current.details = currentDetails.join("\n");
      const fee = current.details.match(/Kosten: €([\d.]+,\d{2})/);
      if (fee) current.feeCents = parseEuroAmount(`€${fee[1]}`) ?? 0;
      statement.transactions.push(current);
    }
    current = null;
    currentDetails = [];
  };

  let lastPage = 0;
  for (const line of lines) {
    const text = line.items.map((i) => i.str).join(" ");
    if (!statement.periodFrom) {
      const period = parseStatementPeriod(text);
      if (period) [statement.periodFrom, statement.periodTo] = period;
    }
    if (line.page !== lastPage) {
      inTable = false;
      lastPage = line.page;
    }

    // Balansoverzicht: "Pro  €opening  €uit  €in  €afsluitend"
    if (statement.openingBalanceCents === null && /^(Pro|Totaal)\b/.test(line.items[0].str.trim())) {
      const amounts = line.items.map((i) => parseEuroAmount(i.str)).filter((a): a is number => a !== null);
      if (amounts.length === 4) {
        statement.openingBalanceCents = amounts[0];
        statement.closingBalanceCents = amounts[3];
        continue;
      }
    }

    const header = line.items.find((i) => i.str.includes("Uitgegeven geld"));
    const saldo = line.items.find((i) => i.str.trim() === "Saldo");
    const received = line.items.find((i) => i.str.includes("Ontvangen geld"));
    const beschrijving = line.items.find((i) => i.str.includes("Beschrijving"));
    if (header && saldo && received && beschrijving) {
      cols = { desc: beschrijving.x, out: header.x, in: received.x, balance: saldo.x };
      inTable = true;
      continue;
    }
    if (!inTable || !cols) continue;
    if (FOOTER.test(text)) {
      flush();
      inTable = false;
      continue;
    }

    const date = parseDutchDate(line.items[0].str);
    if (date && line.items[0].x < cols.desc - 5) {
      flush();
      const c = cols;
      let out = 0;
      let inn = 0;
      let balance: number | null = null;
      const desc: string[] = [];
      for (const it of line.items.slice(1)) {
        const amount = parseEuroAmount(it.str);
        if (amount === null || it.x < c.out - 10) {
          if (it.x < c.out - 10) desc.push(it.str.trim());
          continue;
        }
        if (it.x < c.in - 10) out += amount;
        else if (it.x < c.balance - 30) inn += amount;
        else balance = amount;
      }
      current = { date, description: desc.join(" "), details: "", amountCents: inn - out, feeCents: 0, balanceCents: balance };
    } else if (current) {
      // detailregel; bedragen in vreemde valuta of netto na kosten staan rechts en laten we weg
      const detail = line.items
        .filter((i) => i.x < cols!.out - 10)
        .map((i) => i.str.trim())
        .join(" ");
      const extra = line.items.filter((i) => i.x >= cols!.out - 10).map((i) => i.str.trim());
      if (detail) currentDetails.push(extra.length ? `${detail} (${extra.join(" ")})` : detail);
    }
  }
  flush();
  return statement;
}

export async function parseRevolutPdf(data: Uint8Array): Promise<ParsedStatement> {
  const { getDocument } = await import("pdfjs-dist/legacy/build/pdf.mjs");
  const doc = await getDocument({ data, useSystemFonts: true, isEvalSupported: false }).promise;
  const items: PdfTextItem[] = [];
  for (let p = 1; p <= doc.numPages; p++) {
    const page = await doc.getPage(p);
    const content = await page.getTextContent();
    for (const it of content.items) {
      if ("str" in it) items.push({ page: p, x: it.transform[4], y: it.transform[5], str: it.str });
    }
  }
  return parseRevolutPdfItems(items);
}

// ---------------------------------------------------------------------------
// CSV (Revolut Business-export en de eenvoudige app-export)

const pick = (header: string[], names: string[]) => header.findIndex((h) => names.includes(h.trim().toLowerCase()));

function csvAmount(s: string | undefined): number | null {
  if (s === undefined || s.trim() === "") return null;
  const t = s.trim().replace(/[€\s]/g, "");
  const normalized = /,\d{1,2}$/.test(t) ? t.replace(/\./g, "").replace(",", ".") : t.replace(/,/g, "");
  const n = Number(normalized);
  return Number.isFinite(n) ? Math.round(n * 100) : null;
}

export function parseRevolutCsv(text: string): ParsedStatement {
  const [header, ...rows] = parseCsv(text.replace(/^﻿/, "").trim());
  if (!header) return { openingBalanceCents: null, closingBalanceCents: null, transactions: [] };
  const iDate = pick(header, ["date completed (utc)", "completed date", "date completed", "datum", "date"]);
  const iStarted = pick(header, ["date started (utc)", "started date"]);
  const iDesc = pick(header, ["description", "beschrijving", "omschrijving"]);
  const iRef = pick(header, ["reference", "referentie"]);
  const iPayer = pick(header, ["payer", "counterparty", "tegenpartij"]);
  const iAmount = pick(header, ["amount", "bedrag"]);
  const iFee = pick(header, ["fee", "kosten"]);
  const iBalance = pick(header, ["balance", "saldo"]);
  const iState = pick(header, ["state", "status"]);
  const iType = pick(header, ["type"]);
  if ((iDate < 0 && iStarted < 0) || iAmount < 0) throw new Error("Onbekend CSV-formaat: kolommen voor datum en bedrag ontbreken");

  const transactions: ParsedTransaction[] = [];
  for (const r of rows) {
    const state = iState >= 0 ? (r[iState] ?? "").trim().toUpperCase() : "COMPLETED";
    if (state && !["COMPLETED", "VOLTOOID"].includes(state)) continue;
    const rawDate = (r[iDate >= 0 ? iDate : iStarted] ?? r[iStarted] ?? "").trim();
    const date = rawDate.slice(0, 10);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) continue;
    const amount = csvAmount(r[iAmount]) ?? 0;
    const fee = Math.abs(csvAmount(r[iFee]) ?? 0);
    const details = [
      iType >= 0 && r[iType] ? `Type: ${r[iType]}` : "",
      iRef >= 0 && r[iRef] ? `Referentie: ${r[iRef]}` : "",
      iPayer >= 0 && r[iPayer] ? `Tegenpartij: ${r[iPayer]}` : "",
    ]
      .filter(Boolean)
      .join("\n");
    transactions.push({
      date,
      description: (r[iDesc] ?? "").trim(),
      details,
      // In de CSV staat de fee in een aparte kolom; het saldo daalt met bedrag + fee.
      amountCents: amount - fee,
      feeCents: fee,
      balanceCents: iBalance >= 0 ? csvAmount(r[iBalance]) : null,
    });
  }
  transactions.sort((a, b) => a.date.localeCompare(b.date));
  return {
    openingBalanceCents: null,
    closingBalanceCents: null,
    periodFrom: transactions[0]?.date ?? null,
    periodTo: transactions[transactions.length - 1]?.date ?? null,
    transactions,
  };
}

// ---------------------------------------------------------------------------

/** Controle: beginsaldo + mutaties = eindsaldo, en elk tussensaldo klopt. */
export function reconcile(s: ParsedStatement) {
  const sum = s.transactions.reduce((acc, t) => acc + t.amountCents, 0);
  const opening =
    s.openingBalanceCents ??
    (s.transactions[0]?.balanceCents != null ? s.transactions[0].balanceCents - s.transactions[0].amountCents : null);
  const closing = s.closingBalanceCents ?? s.transactions[s.transactions.length - 1]?.balanceCents ?? null;
  const breaks: { index: number; expected: number; actual: number }[] = [];
  let running = opening;
  s.transactions.forEach((t, index) => {
    if (running === null) return;
    running += t.amountCents;
    if (t.balanceCents !== null && t.balanceCents !== running) {
      breaks.push({ index, expected: running, actual: t.balanceCents });
      running = t.balanceCents;
    }
  });
  const ok = opening !== null && closing !== null && opening + sum === closing && breaks.length === 0;
  return { opening, closing, sum, ok, breaks };
}
