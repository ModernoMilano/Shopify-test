// Renders each ad in ads.json as one 1080x1920 master (text + logo on exact pixels) and
// checks that every text box sits in the area that is safe in BOTH 9:16 and the 1:1 crop.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ads = JSON.parse(fs.readFileSync('ads.json', 'utf8'));
const only = process.argv.slice(2);
const css = fs.readFileSync('fonts/g.css', 'utf8').replace(/https:\/\/fonts\.gstatic\.com\/s\/[a-z]+\/v\d+\//g, 'fonts/');
// Key area: free of Reels/Stories UI (top 14%, bottom 35%, sides 6%) and inside the 1:1 crop (y 219-1299).
const SAFE = { x0: 65, y0: 284, x1: 1015, y1: 1234 };
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const report = [];
  for (const ad of ads) {
    if (only.length && !only.includes(String(ad.id))) continue;
    const dark = ad.theme === 'dark';
    const html = `<!doctype html><html><head><meta charset="utf-8"><style>${css}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#000}
.bg{position:absolute;inset:0;background:url('bgx/${ad.bg}.png') 0 0/1080px 1920px no-repeat}
.scrim{position:absolute;left:0;right:0;top:0;height:${ad.scrimH || 900}px;background:linear-gradient(to bottom, ${ad.scrim || 'transparent'} 0%, ${ad.scrim || 'transparent'} 50%, transparent 100%)}
.block{position:absolute;left:90px;right:90px;top:${ad.top || 300}px;text-align:center;color:${dark ? '#EFECEC' : '#252525'}}
.logo{display:block;margin:0 auto;height:${ad.logoH || 46}px}
h1{font-family:'Trirong',serif;font-weight:300;font-size:${ad.hSize || 84}px;line-height:1.08;letter-spacing:-0.005em;margin-top:${ad.gap1 || 34}px;text-wrap:balance}
.rule{width:64px;height:3px;background:#A38A56;margin:${ad.gap2 || 28}px auto 0}
.sub{font-family:'Quattrocento Sans',sans-serif;font-weight:${ad.sWeight || 400};font-size:${ad.sSize || 34}px;line-height:1.2;letter-spacing:.12em;margin-top:${ad.gap3 || 24}px;color:${ad.subColor || (dark ? '#C8AE78' : '#4A4436')};${ad.upper === false ? '' : 'text-transform:uppercase;'}}
</style></head><body><div class="bg"></div><div class="scrim"></div>
<div class="block"><img class="logo" src="logo/${dark ? 'white' : 'black'}_t.png"><h1>${ad.headline}</h1><div class="rule"></div><div class="sub">${ad.sub}</div></div></body></html>`;
    fs.writeFileSync(`tmp_${ad.id}.html`, html);
    await page.goto('file://' + path.resolve(`tmp_${ad.id}.html`));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(200);
    const m = await page.evaluate(() => {
      const r = e => { const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom].map(v => Math.round(v * 10) / 10); };
      const ink = e => { const rg = document.createRange(); rg.selectNodeContents(e); const rs = [...rg.getClientRects()]; const x0 = Math.min(...rs.map(q => q.left)), y0 = Math.min(...rs.map(q => q.top)), x1 = Math.max(...rs.map(q => q.right)), y1 = Math.max(...rs.map(q => q.bottom)); return { box: [x0, y0, x1, y1].map(v => Math.round(v * 10) / 10), lines: new Set(rs.map(q => Math.round(q.top))).size }; };
      return {
        logo: r(document.querySelector('.logo')), h1: ink(document.querySelector('h1')), rule: r(document.querySelector('.rule')), sub: ink(document.querySelector('.sub')),
        fonts: [document.fonts.check("300 84px Trirong"), document.fonts.check("400 34px 'Quattrocento Sans'")],
        logoLoaded: document.querySelector('.logo').naturalWidth > 0
      };
    });
    const parts = { logo: m.logo, headline: m.h1.box, rule: m.rule, sub: m.sub.box };
    const issues = [];
    for (const [k, b] of Object.entries(parts)) {
      if (b[0] < SAFE.x0 || b[2] > SAFE.x1 || b[1] < SAFE.y0 || b[3] > SAFE.y1) issues.push(`${k} outside safe area ${JSON.stringify(b)}`);
    }
    const bottom = Math.max(...Object.values(parts).map(b => b[3]));
    if (ad.productTop && bottom > ad.productTop - 24) issues.push(`text bottom ${bottom} too close to product top ${ad.productTop}`);
    if (!m.fonts.every(Boolean)) issues.push('brand font not loaded');
    if (!m.logoLoaded) issues.push('logo not loaded');
    if (m.h1.lines > (ad.maxLines || 2)) issues.push(`headline ${m.h1.lines} lines`);
    if (m.sub.lines > 1) issues.push(`subline wraps to ${m.sub.lines} lines`);
    await page.screenshot({ path: `out/seronera_ad${ad.id}_9x16.png`, clip: { x: 0, y: 0, width: 1080, height: 1920 } });
    // Same page with the text hidden: the exact background (incl. scrim) used by contrast.py
    await page.addStyleTag({ content: '.block{visibility:hidden}' });
    await page.screenshot({ path: `chk/bgonly_${ad.id}.png`, clip: { x: 0, y: 0, width: 1080, height: 1920 } });
    report.push({ id: ad.id, parts, headlineLines: m.h1.lines, textBottom: bottom, issues });
  }
  await browser.close();
  fs.writeFileSync('out/report.json', JSON.stringify(report, null, 1));
  console.log(JSON.stringify(report.map(r => ({ id: r.id, bottom: r.textBottom, lines: r.headlineLines, issues: r.issues }))));
})();
