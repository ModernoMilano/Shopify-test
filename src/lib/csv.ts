import { parseEuroToCents } from "./money";

/** Minimale CSV-parser met ondersteuning voor quotes en ; of , als scheidingsteken. */
export function parseCsv(text: string): string[][] {
  const firstLine = text.split(/\r?\n/, 1)[0] ?? "";
  const sep = (firstLine.match(/;/g)?.length ?? 0) > (firstLine.match(/,/g)?.length ?? 0) ? ";" : ",";
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') {
        field += '"';
        i++;
      } else if (c === '"') quoted = false;
      else field += c;
    } else if (c === '"') quoted = true;
    else if (c === sep) {
      row.push(field);
      field = "";
    } else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field);
      rows.push(row);
      row = [];
      field = "";
    } else field += c;
  }
  if (field || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows.filter((r) => r.some((f) => f.trim() !== ""));
}

export type CostCsvRow = {
  line: number;
  product: string;
  unitCostCents: number;
  shippingCostCents: number;
  supplier: string | null;
};

const HEADER_ALIASES: Record<string, string[]> = {
  product: ["product_id", "product", "handle", "titel", "title"],
  unit: ["unit_cost", "kostprijs", "inkoopprijs", "cost"],
  ship: ["shipping_cost", "verzendkosten", "shipping"],
  supplier: ["supplier", "leverancier"],
};

/**
 * Verwacht kolommen: product_id (of handle/titel), kostprijs, verzendkosten, leverancier.
 * Dezelfde indeling als de export, zodat je kunt exporteren → invullen in Excel → importeren.
 */
export function parseCostCsv(text: string): { rows: CostCsvRow[]; errors: string[] } {
  const [header, ...data] = parseCsv(text.replace(/^\uFEFF/, "").trim());
  const errors: string[] = [];
  if (!header) return { rows: [], errors: ["Leeg bestand"] };
  const norm = header.map((h) => h.trim().toLowerCase());
  const col = (k: keyof typeof HEADER_ALIASES) => norm.findIndex((h) => HEADER_ALIASES[k].includes(h));
  const iProduct = col("product");
  const iUnit = col("unit");
  const iShip = col("ship");
  const iSupplier = col("supplier");
  if (iProduct < 0 || iUnit < 0) {
    return { rows: [], errors: ["Kolommen 'product_id' en 'kostprijs' zijn verplicht"] };
  }

  const rows: CostCsvRow[] = [];
  data.forEach((r, idx) => {
    const line = idx + 2;
    const product = (r[iProduct] ?? "").trim();
    const unitRaw = (r[iUnit] ?? "").trim();
    if (!product || !unitRaw) return; // lege kostprijs = overslaan
    const unitCostCents = parseEuroToCents(unitRaw);
    const shippingCostCents = iShip >= 0 ? parseEuroToCents((r[iShip] ?? "").trim()) ?? 0 : 0;
    if (unitCostCents === null) {
      errors.push(`Regel ${line}: ongeldige kostprijs "${unitRaw}"`);
      return;
    }
    rows.push({
      line,
      product,
      unitCostCents,
      shippingCostCents,
      supplier: iSupplier >= 0 ? (r[iSupplier] ?? "").trim() || null : null,
    });
  });
  return { rows, errors };
}

export function toCsv(rows: (string | number | null)[][], sep = ","): string {
  return rows
    .map((r) =>
      r
        .map((v) => {
          const s = v === null ? "" : String(v);
          return /[",;\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
        })
        .join(sep),
    )
    .join("\n");
}
