# Writes the 1:1 as an exact crop of the 9:16 master, plus previews with the Reels/Stories UI zones in red.
import sys
from PIL import Image, ImageDraw
Y = 219  # 1:1 = exact crop of the 9:16 master at y 219..1299
for n in sys.argv[1:]:
    im = Image.open(f'out/seronera_ad{n}_9x16.png').convert('RGB')
    assert im.size == (1080, 1920), im.size
    im.save(f'out/seronera_ad{n}_9x16.png', compress_level=6)
    sq = im.crop((0, Y, 1080, Y + 1080)); sq.save(f'out/seronera_ad{n}_1x1.png', compress_level=6)
    ui = im.copy().convert('RGBA'); ov = Image.new('RGBA', ui.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rectangle((0, 0, 1080, 270), fill=(255, 0, 0, 70)); d.rectangle((0, 1248, 1080, 1920), fill=(255, 0, 0, 70))
    d.rectangle((960, 800, 1080, 1500), fill=(255, 0, 0, 70)); d.rectangle((0, 0, 65, 1920), fill=(255, 0, 0, 40)); d.rectangle((1015, 0, 1080, 1920), fill=(255, 0, 0, 40))
    ui = Image.alpha_composite(ui, ov).convert('RGB')
    a = ui.resize((338, 600), Image.LANCZOS); b = sq.resize((600, 600), Image.LANCZOS)
    p = Image.new('RGB', (338 + 12 + 600, 600), 'white'); p.paste(a, (0, 0)); p.paste(b, (350, 0)); p.save(f'prev/p{n}.jpg', quality=80)
print('ok')
