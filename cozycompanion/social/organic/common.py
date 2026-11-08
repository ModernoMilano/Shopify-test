"""Shared drawing helpers for the organic interaction content: brand fonts, colour emoji, text pills, cover-crop."""
import os, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
FONTS = os.path.join(ROOT, "..", "cozycompanion", "ads", "fonts")
if not os.path.isdir(FONTS):
    FONTS = os.path.join(ROOT, "ads", "fonts")
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
CREAM, CHAR, ROSE = (245, 241, 237), (26, 26, 26), (183, 110, 121)
W, H = 1080, 1920
SAFE_TOP, SAFE_BOTTOM = 250, H - 380

def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

_EMOJI_RE = re.compile("([\U0001F000-\U0001FAFF☀-➿⭐⬆↔-↪⏩-⏺️‍]+)")
_emoji_cache = {}

def _emoji_img(seq, size):
    key = (seq, size)
    if key not in _emoji_cache:
        f = ImageFont.truetype(EMOJI_FONT, 109)
        im = Image.new("RGBA", (160 * max(1, len(seq)), 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((0, 0), seq, font=f, embedded_color=True)
        bb = im.getbbox() or (0, 0, 1, 1)
        im = im.crop(bb)
        s = size / 109 * 1.05
        _emoji_cache[key] = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    return _emoji_cache[key]

def _runs(text):
    return [(p, bool(_EMOJI_RE.fullmatch(p))) for p in _EMOJI_RE.split(text) if p]

def text_width(text, f, spacing=0):
    w = 0
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    for part, emo in _runs(text):
        if emo:
            w += _emoji_img(part.replace("️", ""), f.size).width + 4
        else:
            w += d.textlength(part, font=f) + spacing * max(0, len(part) - 1)
    return w

def draw_text(im, xy, text, f, fill, spacing=0):
    """Draw text with inline colour emoji at xy (top-left)."""
    d = ImageDraw.Draw(im); x, y = xy
    asc, desc = f.getmetrics()
    for part, emo in _runs(text):
        if emo:
            e = _emoji_img(part.replace("️", ""), f.size)
            im.alpha_composite(e, (int(x), int(y + (asc - e.height) * 0.75)))
            x += e.width + 4
        else:
            if spacing:
                for c in part:
                    d.text((x, y), c, font=f, fill=fill); x += d.textlength(c, font=f) + spacing
                x -= spacing
            else:
                d.text((x, y), part, font=f, fill=fill); x += d.textlength(part, font=f)
    return x

def wrap(text, f, max_w):
    words, lines, cur = text.split(" "), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_width(t, f) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def text_block(lines_spec, max_w=900, pad=(54, 38), radius=36, bg=(26, 26, 26, 150), gap=14):
    """lines_spec: list of (text, font, fill, spacing). Returns an RGBA pill with the wrapped, centred lines."""
    rows = []
    for text, f, fill, sp in lines_spec:
        for ln in wrap(text, f, max_w - 2 * pad[0]):
            asc, desc = f.getmetrics()
            rows.append((ln, f, fill, sp, asc + desc))
    bw = int(max(text_width(r[0], r[1], r[3]) for r in rows)) + 2 * pad[0]
    bh = sum(r[4] for r in rows) + gap * (len(rows) - 1) + 2 * pad[1]
    im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    if bg:
        ImageDraw.Draw(im).rounded_rectangle((0, 0, bw - 1, bh - 1), radius, fill=bg)
    y = pad[1]
    for ln, f, fill, sp, lh in rows:
        tw = text_width(ln, f, sp)
        draw_text(im, ((bw - tw) / 2, y), ln, f, fill, sp)
        y += lh + gap
    return im

def shadowed(block, blur=18, alpha=110):
    """Soft drop shadow behind an RGBA block (for blocks without a pill background)."""
    sh = Image.new("RGBA", (block.width + 80, block.height + 80), (0, 0, 0, 0))
    m = block.split()[3].point(lambda v: min(255, v) * alpha // 255)
    s = Image.new("RGBA", block.size, (0, 0, 0, 255)); s.putalpha(m)
    sh.alpha_composite(s, (40, 46)); sh = sh.filter(ImageFilter.GaussianBlur(blur))
    sh.alpha_composite(block, (40, 40))
    return sh

def cover(im, w, h, focus=(0.5, 0.5)):
    im = im.convert("RGB"); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s) + 1, round(im.height * s) + 1), Image.LANCZOS)
    x = int((im.width - w) * focus[0]); y = int((im.height - h) * focus[1])
    return im.crop((x, y, x + w, y + h))

def wordmark(width=300, light=True):
    p = os.path.join(ROOT, "logo", "logo-light.png" if light else "logo-dark.png")
    lg = Image.open(p).convert("RGBA"); lg = lg.crop(lg.getbbox())
    return lg.resize((width, round(lg.height * width / lg.width)), Image.LANCZOS)
