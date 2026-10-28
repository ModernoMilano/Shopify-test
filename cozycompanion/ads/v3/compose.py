"""Collection ads v3: final 1080x1920 (Stories/Reels) + its middle square 1080x1080 (Feed).
Raw 9:16 shots are cover-cropped; the two square shots (beds-dens, cats) sit in a cream frame with the wordmark."""
import sys, io, json, ssl, urllib.request
sys.path.insert(0, "/home/user/Shopify-test/cozycompanion")
from lib import DOMAIN
from PIL import Image, ImageDraw, ImageFont
reg = json.load(open("/home/user/Shopify-test/cozycompanion/files.json"))
C = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
def fetch(n):
    u = f"https://{DOMAIN}/cdn/shop/files/" + reg[n]["url"].split("/files/")[-1].split("?")[0]
    return Image.open(io.BytesIO(urllib.request.urlopen(u, context=C).read())).convert("RGB")
def cover(im, w, h):
    s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))
W, H, T = 1080, 1920, (1920 - 1080) // 2
A = "/home/user/Shopify-test/cozycompanion/"
logo = Image.open(A + "logo/logo-dark.png").convert("RGBA"); logo = logo.crop(logo.getbbox())
logo = logo.resize((380, round(380 * logo.height / logo.width)), Image.LANCZOS)
F1, F2 = ImageFont.truetype(A + "ads/fonts/Jost-500.ttf", 30), ImageFont.truetype(A + "ads/fonts/Cormorant-500.ttf", 40)
LABEL = {"beds-dens": "", "cats": "THE  FOR  CATS  EDIT"}
for k in ["wear-walk", "beds-dens", "cats", "groom-clean", "smart-feeding", "pet-travel"]:
    if f"adsq3_{k}" in reg:  # square shot: sharp in the middle of a cream frame with the wordmark (outpainting repeats the text)
        sq = fetch(f"adsq3_{k}").resize((W, W), Image.LANCZOS)
        edge = lambda box: sq.crop(box).resize((1, 1), Image.BOX).getpixel((0, 0))
        base = Image.new("RGB", (W, H), edge((0, 0, W, 6))); base.paste(Image.new("RGB", (W, H - T - W), edge((0, W - 6, W, W))), (0, T + W))
        base.paste(sq, (0, T))
        base.paste(logo, ((W - logo.width) // 2, (T - logo.height) // 2 + 20), logo)
        d = ImageDraw.Draw(base); y = T + W + (H - T - W) // 2 - 40
        d.text(((W - d.textlength(LABEL[k], font=F1)) / 2, y), LABEL[k], font=F1, fill=(26, 26, 26))
        d.text(((W - d.textlength("cozycompanion.us", font=F2)) / 2, y + 50), "cozycompanion.us", font=F2, fill=(183, 110, 121))
    else:
        base = cover(fetch(f"adraw3_{k}"), W, H)
    base.save(f"v3/final/{k}_9x16.jpg", quality=92)
    base.crop((0, T, W, T + W)).save(f"v3/final/{k}_1x1.jpg", quality=92)
    print("ok", k)
