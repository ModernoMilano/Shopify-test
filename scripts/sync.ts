import { syncAll } from "../src/lib/sync";
import { db } from "../src/lib/db";

const full = process.argv.includes("--full");

syncAll({ full })
  .then((r) => console.log(`Klaar: ${r.products} producten, ${r.orders} orders`))
  .catch((e) => {
    console.error(e);
    process.exitCode = 1;
  })
  .finally(() => db.$disconnect());
