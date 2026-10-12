"""Schrijft OVERZICHT.md (voor de eigenaar) uit plan.json, verdicts.json en chosen.json.
Gebruik: python3 -I overzicht.py <verdicts.json> <chosen.json> <links.json> > OVERZICHT.md
links.json: {"zip": url, "storyboard": url, "alle": url, "nieuw": url, "credits_start": 1000.52, "credits_nu": ...}"""
import json, sys
plan = json.load(open("plan.json")); verdicts = json.load(open(sys.argv[1])); chosen = json.load(open(sys.argv[2])); links = json.load(open(sys.argv[3]))
print(f"# {plan['title']} · overzicht van alle beelden (12 oktober 2026, avond)\n")
print("Alles wat hieronder staat is nog **zonder video**: eerst jouw oordeel, dan pas Seedance.\n")
print("## Wat er is veranderd sinds het vorige overzicht\n")
print("- **Nieuwe opening (0–11,2 s).** Je vond de hook niks; de eerste twaalf seconden zijn in tekst én beeld vervangen. Vier ontwerpen zijn door een jury van drie gewogen; de winnaar is samengesteld tot vijf nieuwe beelden H01–H05: "
      "blote enkels in grijs suède die op het marmer van de Galleria landen (\"You will look twice.\"), de lege borst van het gilet onder zijn hand (\"Nothing on him says a word.\"), de kraag van achteren (\"And still, you look.\"), "
      "over zijn schouder omhoog naar het glas (\"He never asked you to.\") en pas dan zijn ogen, de omgekeerde hoek van V01 (\"So where does that come from.\"), waarna \"From the elegance of Milan...\" het antwoord is.")
print("- **Jouw vier correcties.** V01 (kraag verkeerd om), V08 (bordeaux in de kraag), V10 (polokraag) en V12 (vilt, geen gilet) zijn opnieuw gemaakt met de productfoto's als maatstaf; de nieuwe keuzes staan in de tabel. "
      "Bij V10 is de gekozen variant bijgesneden zodat de effen manchet aan de rechterrand (zonder de crème dubbele streep) buiten beeld valt; aan het beeld zelf is niets geretoucheerd.")
print("- **Oude-camerafilter.** De zes opties staan hieronder; je keuze staat nog open.\n")
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
print("De eerste vijf rijen zijn de nieuwe opening; vanaf 11,2 s is de film zoals je hem kende.\n")
print("| tijd | beeld | tekst in beeld |\n|---|---|---|")
for t in plan["timeline"]:
    shot = t["shot"].replace("NEW ", "")
    sid = shot.split()[0]
    tag = f"**nieuw** {shot}" if sid in verdicts else f"bestaand: {shot}"
    print(f"| {t['t_start']:.1f}–{t['t_end']:.1f} s | {tag} | {t['vo'].split(' (')[0].strip() or '(geen stem)'} |")
print(f"\n## De {len(verdicts)} nieuwe beelden: wat gekozen is en waarom\n")
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
      f"Niet via deze sessie: {links.get('spent_other', 0)} ({links.get('spent_other_note', '')}).\n")
vs = links.get('video_shots', 16)
print(f"**Video.** {vs} shots zijn video (V01–V12 en H01, H02, H03, H05); S01–S05 en H04 zijn levende stills zonder videokosten. "
      f"Seedance 2.5 kost per shot 12 (480p-concept) + 48 (1080p) = 60 credits: {vs} × 60 = {vs * 60}, of {vs * 48} als ik de concepten oversla. "
      f"Met {links['credits_nu']} op de teller past dat niet; zeg of je credits bijkoopt of welke shots ik als levende still mag maken.\n")
print("## Wat ik je vraag\n\n1. De nieuwe opening: kloppen de tekst en de vijf beelden?\n2. De vier gecorrigeerde shots en de rest: zeg per shot wat anders moet (ander beeld, andere variant, andere tekst). Ik maak dan alleen dat opnieuw.\n3. Kies de filter (mijn advies: Portra 400).\n4. De credits voor de video (zie hierboven).\n5. Pas daarna maak ik de video's (eerst 480p-concepten, dan 1080p) en de montage.\n")
