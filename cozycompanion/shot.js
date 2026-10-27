const { chromium } = require('playwright');
(async () => {
  const [url, out, w, h, pw] = process.argv.slice(2);
  const b = await chromium.launch({ proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined, ignoreHTTPSErrors: false });
  const ctx = await b.newContext({ viewport: { width: +w, height: +h }, ignoreHTTPSErrors: true });
  const p = await ctx.newPage();
  if (pw) {
    await p.goto(`https://${process.env.COZY_SHOPIFY_DOMAIN}/password`, { waitUntil: 'domcontentloaded' });
    await p.fill('input[type=password]', pw); await p.keyboard.press('Enter'); await p.waitForTimeout(2500);
  }
  await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
  await p.waitForTimeout(2000);
  await p.screenshot({ path: out, fullPage: true });
  await b.close();
})();
