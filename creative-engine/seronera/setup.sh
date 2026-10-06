#!/usr/bin/env bash
# Run inside the Higgsfield sandbox (sandbox_exec): it can reach seronera.shop, Google Fonts and the Higgsfield CDN.
# Downloads fonts, logo and the backgrounds listed in backgrounds.json, and scales them to exactly 1080x1920.
set -e
mkdir -p fonts logo bg bgx out chk prev
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
GCSS=$(python3 -c "import json;print(json.load(open('brand.json'))['fonts']['googleCss'])")
curl -sSL -A "$UA" "$GCSS" -o fonts/g.css
grep -oE "url\(https://fonts.gstatic.com[^)]+\)" fonts/g.css | sed 's/url(//;s/)//' | sort -u | while read u; do curl -sSL "$u" -o "fonts/$(basename "$u")"; done
curl -sSL -A "$UA" "$(python3 -c "import json;print(json.load(open('brand.json'))['logo']['wordmark'])")" -o logo/wordmark.png
convert logo/wordmark.png -trim +repage -fill '#252525' -colorize 100 logo/black_t.png
convert logo/wordmark.png -trim +repage -fill '#EFECEC' -colorize 100 logo/white_t.png
python3 - <<'PY'
import json, subprocess
from PIL import Image
cfg = json.load(open('backgrounds.json'))
for b in cfg['used']:
    subprocess.run(['curl', '-sSf', cfg['resultBase'] + b['file'], '-o', f"bg/{b['bg']}.png"], check=True)
    im = Image.open(f"bg/{b['bg']}.png").convert('RGB'); w, h = im.size
    s = max(1080 / w, 1920 / h); im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    W, H = im.size; l = (W - 1080) // 2; t = (H - 1920) // 2
    im.crop((l, t, l + 1080, t + 1920)).save(f"bgx/{b['bg']}.png")
print('setup ok')
PY
