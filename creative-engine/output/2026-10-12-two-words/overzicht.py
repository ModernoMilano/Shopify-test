"""Schrijft OVERZICHT.md (voor de eigenaar) uit plan.json, verdicts.json en chosen.json.
Gebruik: python3 -I overzicht.py <verdicts.json> <chosen.json> <links.json> > OVERZICHT.md
links.json: {"zip": url, "storyboard": url, "alle": url, "nieuw": url, "credits_start": 1000.52, "credits_nu": ...}"""
import json, sys
plan = json.load(open("plan.json")); verdicts = json.load(open(sys.argv[1])); chosen = json.load(open(sys.argv[2])); links = json.load(open(sys.argv[3]))
print(f"# {plan['title']} · overzicht van alle beelden (12 oktober 2026)\n")
print("Alles wat hieronder staat is nog **zonder video**: eerst jouw oordeel, dan pas Seedance.\n")
print("## Links\n")
print(f"- Zip met alles (storyboard, overzicht van alle varianten, de 17 gekozen beelden op volle grootte, alle varianten op halve grootte): {links['zip']}")
print(f"- Storyboard (lange JPEG, scrollen): {links['storyboard']}")
print(f"- Alle varianten met oordeel (lange JPEG): {links['alle']}")
print(f"- De nieuwe beelden groot naast elkaar: {links['nieuw']}")
print(f"- Oude-camerafilters, zes opties op drie beelden: {links['filters']}")
print(f"- Dezelfde filters in beweging (42 s, per filter 3 s regen en 3 s avond): {links['filters_video']}\n")
print("## De filter (jouw keuze)\n")
print("Kodachrome 64 (warm, rijk rood, diepe zwarten, fijne korrel) · Portra 400 (zacht, warme huid, opgelichte zwarten) · Cinestill 800T (nachtfilm: koele schaduwen, warme lichten met gloed) · 16 mm Ektachrome (zichtbare korrel, iets zachter) · Verbleekte print (jaren-70 afdruk, gedempt) · Tri-X 400 (zwart-wit). "
      "Mijn advies: Portra 400 voor de hele film (past bij de merknorm: gedempt, warm, zachte contrasten), met Cinestill als tweede keus omdat de avondscènes thuis (V09, V10, Sera) er mooi van gloeien. De filter gaat over elk shot heen, ook de bestaande clips, na de belichting per shot; de korrel beweegt per frame.\n")
print("## De film in 32 beelden\n")
print("| tijd | beeld | tekst in beeld |\n|---|---|---|")
for t in plan["timeline"]:
    shot = t["shot"].replace("NEW ", "")
    sid = shot.split()[0]
    tag = f"**nieuw** {shot}" if sid in verdicts else f"bestaand: {shot}"
    print(f"| {t['t_start']:.1f}–{t['t_end']:.1f} s | {tag} | {t['vo'].split(' (')[0].strip() or '(geen stem)'} |")
print("\n## De 17 nieuwe beelden: wat gekozen is en waarom\n")
print("Twee onafhankelijke controleurs per beeld (kledingregels en echtheid), elk met uitsneden op 100 %. Eén overtreding is afgekeurd; kleine promptafwijkingen zonder merkregel staan als opmerking.\n")
print("| shot | gekozen | varianten gemaakt | opmerking |\n|---|---|---|---|")
for sid, s in verdicts.items():
    c = chosen.get(sid)
    n = len(s["variants"])
    if c:
        best = next(v for v in s["variants"] if v.get("chosen"))
        note = best["note"]
    else:
        note = "nog geen variant door beide controleurs goedgekeurd; beste kandidaat staat in het overzicht met de reden"
    print(f"| {sid} {s['title'].split(' ', 1)[1]} | {c['label'] if c else '—'} | {n} | {note} |")
print(f"\n## Credits\n\nStart: {links['credits_start']} · nu: {links['credits_nu']} · door mij uitgegeven aan beelden: {links['spent_images']} (4 per 4K-beeld). "
      f"Niet van mij: {links.get('spent_other', 0)} (Ads Studio en GPT Image in het Higgsfield-account, 18:09 en 18:27–18:30).\n")
print("## Wat ik je vraag\n\n1. Loop het storyboard door: klopt de volgorde, de tekst per beeld en de keuze per shot?\n2. Zeg per shot wat anders moet (ander beeld, andere variant, andere tekst). Ik maak dan alleen dat opnieuw.\n3. Pas daarna maak ik de 12 video's (eerst 480p-concepten, dan 1080p) en de montage.\n")
