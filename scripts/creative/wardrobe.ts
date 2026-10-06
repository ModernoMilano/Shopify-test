// Bouwt creative-engine/data/wardrobe.json uit de actieve Shopify-producten.
//   npm run creative:wardrobe                       → haalt live op via de Admin API (.env nodig)
//   npm run creative:wardrobe -- --from dump.json   → uit een export (array van product-nodes of GraphQL-pagina's)
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { buildWardrobe, type ShopifyProductNode } from "../../src/creative/wardrobe";
import { CATALOG_QUERY } from "../../src/creative/catalog-query";

const OUT = path.resolve(__dirname, "../../creative-engine/data/wardrobe.json");

function nodesFromDump(file: string): ShopifyProductNode[] {
  const json = JSON.parse(readFileSync(file, "utf8"));
  const pages = Array.isArray(json) ? json : [json];
  return pages.flatMap((x: any) => x?.data?.products?.nodes ?? x?.products?.nodes ?? (x?.id ? [x] : []));
}

async function nodesFromShopify(): Promise<ShopifyProductNode[]> {
  const { shopifyGraphQL } = await import("../../src/lib/shopify");
  const nodes: ShopifyProductNode[] = [];
  let after: string | null = null;
  do {
    const data: any = await shopifyGraphQL(CATALOG_QUERY, { after });
    nodes.push(...data.products.nodes);
    after = data.products.pageInfo.hasNextPage ? data.products.pageInfo.endCursor : null;
  } while (after);
  return nodes;
}

async function main() {
  const i = process.argv.indexOf("--from");
  const nodes = i > -1 ? nodesFromDump(process.argv[i + 1]) : await nodesFromShopify();
  const { items, skipped } = buildWardrobe(nodes);
  writeFileSync(OUT, JSON.stringify({ generatedAt: new Date().toISOString(), count: items.length, items }, null, 1) + "\n");
  console.log(`Garderobe: ${items.length} items → ${path.relative(process.cwd(), OUT)}`);
  if (skipped.length) console.log(`Niet ingedeeld (${skipped.length}): ${skipped.join(", ")}`);
}

main().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
