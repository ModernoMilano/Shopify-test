"""Bouwt verdicts.json (voor allsheet.py) en chosen.json uit de journals van de keuringsrondes.
Gebruik: python3 -I verdicts.py <plan.json> <uit-map> <journal...>  (latere journals overschrijven eerdere voor dezelfde sid+lens+versie)
Versies: per sid wordt bijgehouden welke bestanden bij welke ronde horen (ORIG-tabel hieronder)."""
import json, sys, collections
plan = json.load(open(sys.argv[1])); outdir = sys.argv[2]; journals = sys.argv[3:]
# versie-administratie: (sid, ronde) -> {variant: bestand}; de laatste ronde staat in img/<sid><v>.png
ROUNDS = {
  "V02": [{"a": "img/orig/V02a_v1.png", "b": "img/orig/V02b_v1.png"}, {"a": "img/orig/V02a_v2.png", "b": "img/orig/V02b_v2.png"}, {"a": "img/orig/V02a_v3.png", "b": "img/orig/V02b_v3.png"}, {"a": "img/V02a.png", "b": "img/V02b.png"}],
  "V07": [{"a": "img/orig/V07a_v1.png", "b": "img/orig/V07b_v1.png"}, {"a": "img/orig/V07a_v2.png", "b": "img/orig/V07b_v2.png"}, {"a": "img/orig/V07a_v3.png", "b": "img/orig/V07b_v3.png"}, {"a": "img/V07a.png", "b": "img/V07b.png"}],
  "V12": [{"a": "img/orig/V12a_v1.png", "b": "img/orig/V12b_v1.png"}, {"a": "img/orig/V12a_v2.png", "b": "img/orig/V12b_v2.png"}, {"a": "img/V12a.png", "b": "img/V12b.png"}],
  "V10": [{"a": "img/orig/V10a_v1.png", "b": "img/orig/V10b_v1.png"}, {"a": "img/orig/V10a_v2.png", "b": "img/orig/V10b_v2.png"}, {"a": "img/orig/V10a_v3.png", "b": "img/orig/V10b_v3.png"}, {"a": "img/V10a.png", "b": "img/V10b.png"}, {"a": "img/V10b_crop.png", "b": "img/V10b.png"}],
  "V01": [{"a": "img/orig/V01a_v1.png", "b": "img/orig/V01b_v1.png"}, {"a": "img/V01a.png", "b": "img/V01b.png"}],
  "V08": [{"a": "img/orig/V08a_v1.png", "b": "img/orig/V08b_v1.png"}, {"a": "img/V08a.png", "b": "img/V08b.png"}],
  "V11": [{"a": "img/orig/V11a_v1.png", "b": "img/orig/V11b_v1.png"}, {"a": "img/orig/V11a_v2.png", "b": "img/orig/V11b_v2.png"}, {"a": "img/V11a.png", "b": "img/V11b.png"}],
  "S02": [{"a": "img/S02a.png", "b": "img/S02b.png"}],
  "S05": [{"a": "img/orig/S05a_v1.png", "b": "img/orig/S05b_v1.png"}, {"a": "img/orig/S05a_v2.png", "b": "img/orig/S05b_v2.png"}, {"a": "img/S05a.png", "b": "img/S05b.png"}],
  "H01": [{"a": "img/orig/H01a_v1.png", "b": "img/orig/H01b_v1.png"}, {"a": "img/H01a.png", "b": "img/H01b.png"}],  # ronde 1: penny-strap, het product heeft geen bandje
  "H04": [{"a": "img/H04a.png", "b": "img/H04b.png"}],
  "H02": [{"a": "img/orig/H02a_v1.png", "b": "img/orig/H02b_v1.png"}, {"a": "img/H02a.png", "b": "img/H02b.png"}],
  "H05": [{"a": "img/orig/H05a_v1.png", "b": "img/orig/H05b_v1.png"}, {"a": "img/H05a.png", "b": "img/H05b.png"}],  # ronde 1 (profiel zichtbaar) staat in UNCHECKED; de keuring begint bij ronde 2
}
V10_CROP = {"a": "img/V10b_crop.png", "b": "img/V10b.png"}  # ronde 5 van V10: a = uitsnede zonder de manchet, b = het volle beeld
# welke journal hoort bij welke ronde van een sid (volgorde van de journals op de commandoregel = chronologisch)
# we nemen aan: voor sids met meerdere rondes komen de journals in chronologische volgorde binnen; elke nieuwe journal met die sid = volgende ronde
OWNER_REJECT = {("V01", 0, "b"): "door de eigenaar afgekeurd: kraag verkeerd om (binnenkleur buiten)", ("V08", 0, "a"): "door de eigenaar afgekeurd: bordeaux binnenin de kraag",
                ("V10", 2, "b"): "door de eigenaar afgekeurd: polokraag, niet de capuchonjas", ("V12", 1, "b"): "door de eigenaar afgekeurd: gevilte wol met raglannaad, niet zijn gilet"}
UNCHECKED = {"S02": [{"file": "img/orig/S02a_v1.png", "label": "S02a (ronde 1)", "note": "op zicht afgewezen: een afgewerkt kledingstuk met een snede erin, geen losse stof"},
                     {"file": "img/orig/S02b_v1.png", "label": "S02b (ronde 1)", "note": "op zicht afgewezen: gedrukte merknaam op de kraag, rits en tee in beeld"}],
             "H04": [{"file": "img/orig/H04a_v1.png", "label": "H04a (ronde 1)", "note": "op zicht afgewezen: zijn gezicht staat in profiel in beeld, het moet afgewend blijven tot H05"},
                     {"file": "img/orig/H04b_v1.png", "label": "H04b (ronde 1)", "note": "op zicht afgewezen: zijn gezicht staat in profiel in beeld, het moet afgewend blijven tot H05"}]}
PREFER = {"H02": ("b", "beide goedgekeurd; b heeft de rits dicht tot boven, zoals het shot vraagt")}
SKIP = {("wf_fdec4132-fa9", "V07")}  # de afgebroken eerste ronde had V07 al half gekeurd; ronde 2 keurde dezelfde beelden volledig
titles = {s["id"].split()[0]: s["id"] for s in plan["new_shots"]}
vo = {}
for t in plan["timeline"]:
    sid = t["shot"].replace("NEW ", "").split()[0]
    if sid in titles and sid not in vo: vo[sid] = t["vo"].split(" (")[0].strip()
vo.update({"V03": "A line in chalk.", "V04": "Cut once."})  # bij deze shots houdt de kaart van de vorige regel aan
seen_round = collections.defaultdict(int); results = collections.defaultdict(dict)  # (sid, round) -> lens -> verdict
for path in journals:
    sids_in_this = set()
    for l in open(path):
        j = json.loads(l)
        if j.get("type") != "result": continue
        r = j.get("result")
        if not isinstance(r, dict) or "variants" not in r: continue
        sid = r["sid"].split()[0]
        if any(k in path and sid == v for k, v in SKIP): continue
        if sid not in ROUNDS:  # één versie: alle oordelen in ronde 0, latere overschrijven eerdere
            results[(sid, 0)][r["lens"]] = r; continue
        if sid not in sids_in_this:
            sids_in_this.add(sid)
            if (sid, seen_round[sid]) in results and r["lens"] in results[(sid, seen_round[sid])]:
                seen_round[sid] += 1
        rnd = seen_round[sid]
        results[(sid, rnd)][r["lens"]] = r
out = {}; chosen = {}
for sid in titles:
    rounds = [k for k in results if k[0] == sid]
    variants = [dict(u, ok=False, score=0, round=-1, variant="?", lenses=0) for u in UNCHECKED.get(sid, [])]
    for (s, rnd) in sorted(rounds, key=lambda k: k[1]):
        files = ROUNDS.get(sid, [{"a": f"img/{sid}a.png", "b": f"img/{sid}b.png"}])
        fmap = files[min(rnd, len(files) - 1)]
        lenses = results[(sid, rnd)]
        for v in "ab":
            ok = True; scores = []; probs = []
            for lens, r in lenses.items():
                for x in r["variants"]:
                    if x["variant"] != v: continue
                    ok = ok and x["pass"]; scores.append(x["score"]); probs += [p for p in x["problems"]] if not x["pass"] else []
            label = f"{sid}{v}" + (f" (ronde {rnd+1})" if len(files) > 1 else "")
            if sid == "S05" and rnd == 2: label = "S05 uitsnede uit b (ronde 2)" if v == "a" else "S05b (ronde 2, vol)"
            if sid == "V10" and rnd == 4: label = "V10 uitsnede uit b (zonder manchet)" if v == "a" else "V10b (ronde 4, vol)"
            note = ("goedgekeurd door beide controleurs" if ok else (probs[0][:160] if probs else "afgekeurd")) + (f" · score {sum(scores)/len(scores):.1f}" if scores else "")
            if (sid, rnd, v) in OWNER_REJECT: ok = False; note = OWNER_REJECT[(sid, rnd, v)]
            variants.append({"file": fmap[v], "label": label, "ok": ok and bool(scores), "score": sum(scores)/len(scores) if scores else 0, "note": note, "round": rnd, "variant": v, "lenses": len(lenses)})
    good = [x for x in variants if x["ok"] and x["lenses"] >= 2]
    if good:
        best = max(good, key=lambda x: (x["round"], x["score"]))  # laatste ronde eerst, dan score
        if sid in PREFER:  # redactionele voorkeur tussen twee goedgekeurde varianten
            pref = [x for x in good if x["variant"] == PREFER[sid][0] and x["round"] == best["round"]]
            if pref: best = pref[0]; best["why"] = PREFER[sid][1]
        best["chosen"] = True; chosen[sid] = {"file": best["file"], "title": titles[sid], "vo": vo.get(sid, ""), "label": best["label"]}
    else:
        cands = [x for x in variants if x["lenses"] >= 1 and x["round"] >= 0]
        if cands:  # geen variant door beide goedgekeurd: beste van de laatste ronde als VOORLOPIGE keuze, met kanttekening
            best = max(cands, key=lambda x: (x["round"], x["score"]))
            best["chosen"] = True; best["provisional"] = True; best["note"] = "VOORLOPIG (niet goedgekeurd): " + best["note"]
            chosen[sid] = {"file": best["file"], "title": titles[sid], "vo": vo.get(sid, ""), "label": best["label"] + " (voorlopig)", "provisional": True}
    out[sid] = {"title": titles[sid], "vo": vo.get(sid, ""), "variants": variants}
json.dump(out, open(f"{outdir}/verdicts.json", "w"), ensure_ascii=False, indent=1)
json.dump(chosen, open(f"{outdir}/chosen.json", "w"), ensure_ascii=False, indent=1)
for sid, s in out.items():
    print(sid, [(x["label"], "OK" if x["ok"] else "x", round(x["score"], 1), x["lenses"], "*" if x.get("chosen") else "") for x in s["variants"]])
print("gekozen:", len(chosen), "van", len(titles))
