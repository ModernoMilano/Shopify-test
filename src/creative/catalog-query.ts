/** Alle actieve producten met foto's; dezelfde query werkt via de Shopify-connector in Claude. */
export const CATALOG_QUERY = `query Catalog($after: String) {
  products(first: 50, after: $after, query: "status:active", sortKey: TITLE) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id title handle productType tags vendor description(truncateAt: 700) onlineStoreUrl totalInventory
      category { fullName }
      options { name values }
      priceRangeV2 { minVariantPrice { amount } maxVariantPrice { amount } }
      collections(first: 6) { nodes { title handle } }
      media(first: 12) { nodes { mediaContentType ... on MediaImage { image { url altText width height } } } }
    }
  }
}`;
