"""Bouwt alle overzichten en de zip uit verdicts.json en chosen.json (beide in ~/tw).
python3 build.py  -> out/00_storyboard.jpg, out/01_alle_varianten.jpg, out/02_nieuwe_beelden.jpg, out/gekozen/*.jpg, out/alle_varianten/*.jpg, you-will-look-twice-beelden.zip"""
import json, os, subprocess, shutil, re
from PIL import Image
shutil.rmtree("out", ignore_errors=True)
os.makedirs("out/gekozen", exist_ok=True); os.makedirs("out/alle_varianten", exist_ok=True)
verdicts = json.load(open("verdicts.json")); chosen = json.load(open("chosen.json"))
# 1. storyboard met de gekozen beelden
images = {sid: c["file"] for sid, c in chosen.items()}
json.dump(images, open("images.json", "w"))
subprocess.run(["python3", "rows.py", "plan.json", "frames", "rows.json", "images.json"], check=True)
subprocess.run(["python3", "storyboard.py", "rows.json", "out/00_storyboard.jpg"], check=True)
# 2. alle varianten met oordeel
subprocess.run(["python3", "allsheet.py", "verdicts.json", "out/01_alle_varianten.jpg"], check=True)
# 3. contactblad van de gekozen nieuwe beelden
subprocess.run(["python3", "contact.py", "chosen.json", "out/02_nieuwe_beelden.jpg"], check=True)
# 4. losse JPEG's: gekozen op volle grootte, alle varianten op halve grootte
def safe(s): return re.sub(r"[^A-Za-z0-9 ,'()+-]+", " ", s).strip()
for sid, c in chosen.items():
    im = Image.open(c["file"]).convert("RGB")
    im.save(f"out/gekozen/{sid} {safe(c['title'].split(' ', 1)[1].title())}.jpg", quality=95)
for sid, s in verdicts.items():
    for v in s["variants"]:
        im = Image.open(v["file"]).convert("RGB"); im.thumbnail((1536, 2752), Image.LANCZOS)
        tag = ("GEKOZEN " if v.get("chosen") else "") + ("goed" if v["ok"] else "afgekeurd")
        im.save(f"out/alle_varianten/{safe(v['label'])} - {tag}.jpg", quality=90)
if os.path.exists("you-will-look-twice-beelden.zip"): os.remove("you-will-look-twice-beelden.zip")
subprocess.run(["zip", "-qr", "you-will-look-twice-beelden.zip", "out"], check=True)
print("zip", os.path.getsize("you-will-look-twice-beelden.zip") // 1_000_000, "MB;", len(os.listdir("out/gekozen")), "gekozen;", len(os.listdir("out/alle_varianten")), "varianten")
