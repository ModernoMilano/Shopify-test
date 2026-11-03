import os, csv, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t26_data import C

RULES = """GLOBAL RULES (apply to every video in this file)
- Format: 9:16, 1080x1920 or higher, 25/30 fps, 10-12 s, no audio track (music is added in Meta).
- Structure: 0-3 s HOOK (strongest motion in the first 0.5 s) / 3-8 s BODY / last 2 s END FRAME.
- Deliver every video 3 times: identical body and end frame, only the first 3 s differ (H1, H2, H3).
- END FRAME (last 2 s): a calm, near-still frame; keep the TOP 20% of the frame completely empty (no product, no text)
  so a Black Week offer badge can be added later without a reshoot.
- Safe zone: product and text inside the central area; nothing important in the top 14% or bottom 20%.
- No faces, ever: hands, forearms, chest-down crops or backlit silhouettes only. Natural male hands, no rings or watches
  (female hands only where stated), exactly five fingers.
- Product fidelity: use only the garment named for the video, exactly as on the product photos (colour, knit, zip, stripes,
  drawstrings). No other brands, no logos on garments, no other clothing except a plain white tee under the jacket.
  Lounge Set: zip jacket + drawstring trousers, no stripes (Beige / Gray / Navy / Black).
  Two-Tone set: zip jacket + trousers with white/cream contrast stripes (Black / Dark Mocha / Grey / Navy).
- Never generate text, prices or logos inside the footage. All text below is a clean overlay added in post:
  hooks in Oswald Bold caps or Cormorant Garamond (match the statics), supporting lines in Montserrat.
  Logo: only the official ModernoMilano file, with 'TIMELESS. REFINED. YOU.' underneath.
- Claims: say "cashmere blend" (never "100% cashmere"). No discounts, no sale wording, no crossed-out prices,
  no ratings or review counts. Prices only as listed: Lounge Set €150, Two-Tone set €250. "Free shipping" is allowed.
- Match the polish, grading and pacing of our previous ModernoMilano videos: warm, quiet luxury, real light, slow camera.
"""

FOLDER = {c["id"]: f"T26_{c['id']}_{c['name']}" for c in C}

def video_md(c):
    out = [f"# {c['id']} {c['name']}: video engine prompt", "", RULES, ""]
    for v in c["videos"]:
        out.append(f"## Video {v['v']} - product: {v['product']}")
        for i, (vis, txt) in enumerate(v["hooks"], 1):
            out.append(f"- **T26_{c['id']}_916{v['v']}_H{i}_v1** - HOOK 0-3 s: {vis} Overlay text: \"{txt}\"")
        out.append(f"- BODY 3-8 s (same for H1-H3): {v['body']}")
        out.append(f"- END FRAME, last 2 s (same for H1-H3): {v['end']}")
        out.append("")
    return "\n".join(out)

def copy_txt(c):
    k = c["copy"]
    return "\n".join([
        f"{c['id']} {c['name']}: COPY SET", "",
        "PRIMARY TEXT (short):", k["short"], "",
        "PRIMARY TEXT (medium):", k["medium"], "",
        "PRIMARY TEXT (long):", k["long"], "",
        "HEADLINES:", *[f"{i}. {h}" for i, h in enumerate(k["headlines"], 1)], "",
        "DESCRIPTION:", k["description"], ""])

def rows():
    R = []
    for c in C:
        k = c["copy"]
        base = [k["short"], k["medium"], k["long"], " | ".join(k["headlines"]), k["description"]]
        for s in c["statics"]:
            txt = " / ".join(s["lines"]) + (f" / {s['sub']} / {s['cta']}" if s.get("sub") else "")
            for fmt, lab in (("45", "Static 4:5"), ("916", "Static 9:16")):
                R.append([f"T26_{c['id']}_{fmt}_{s['s']}_v1", f"{c['id']} {c['name']}", lab, txt, *base, s["product"], s["visual"], "Delivered (image)"])
        for v in c["videos"]:
            for i, (vis, txt) in enumerate(v["hooks"], 1):
                R.append([f"T26_{c['id']}_916{v['v']}_H{i}_v1", f"{c['id']} {c['name']}", f"Video 9:16 ({v['v']}), hook H{i}", txt, *base, v["product"], vis, "Prompt ready for video engine"])
    return R

HEAD = ["name", "concept", "format", "hook / text in image", "primary text (short)", "primary text (medium)",
        "primary text (long)", "headlines", "description", "product shown", "visual", "status"]

def write_all(outdir, xlsx=True):
    os.makedirs(outdir, exist_ok=True)
    for c in C:
        d = os.path.join(outdir, FOLDER[c["id"]]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, f"T26_{c['id']}_COPY.txt"), "w").write(copy_txt(c))
        open(os.path.join(d, f"T26_{c['id']}_VIDEO_ENGINE_PROMPT.md"), "w").write(video_md(c))
    with open(os.path.join(outdir, "T26_SHEET.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(HEAD); w.writerows(rows())
    if xlsx:
        from openpyxl import Workbook
        from openpyxl.styles import Font, Alignment
        wb = Workbook(); ws = wb.active; ws.title = "T26"
        ws.append(HEAD)
        for r in rows(): ws.append(r)
        for cell in ws[1]: cell.font = Font(bold=True)
        widths = [26, 12, 22, 40, 40, 60, 80, 50, 34, 50, 60, 26]
        for i, wdt in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = wdt
        for row in ws.iter_rows(min_row=2):
            for cell in row: cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws.freeze_panes = "A2"
        wb.save(os.path.join(outdir, "T26_SHEET.xlsx"))

if __name__ == "__main__":
    write_all(sys.argv[1], xlsx=(len(sys.argv) < 3))
    print("written", len(rows()), "rows")
