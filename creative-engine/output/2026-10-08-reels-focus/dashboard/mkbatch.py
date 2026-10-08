"""Maakt de batch voor de store van het dashboard: meta, datasets (met blob-urls) en de pagina."""
import json, sys, datetime
blobs = json.load(open("blobs.json"))
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
META = {
 "videos": ("Video's en concept", "De vier video's met product, moment, plek en de twee shots, uit het draaiboek VIDEOS4.md."),
 "stappen": ("Stappen per video", "Per video de tien stappen van draaiboek tot oplevering, met hun status nu."),
 "beelden": ("Beelden en hun status", "Elk startbeeld, elke productfoto en elke referentie van Luca, met status, reden en een link naar het origineel."),
 "voorbeelden": ("Voorbeeldbeelden", "Kleine versies (360 bij 640 px) van de beelden, gemaakt in de Higgsfield-sandbox."),
 "controles": ("Controles per beeld", "Elke controle door een agent of door de regisseur, samengevat in gewoon Nederlands."),
 "agents": ("Agents en hun rol", "Wie er meewerkt aan de serie: de regisseur, de modellen op Higgsfield, de controleurs en jij."),
 "log": ("Logboek", "Wat er gebeurde en wanneer, met de tijden uit de jobs, de workflows en GitHub."),
 "kosten": ("Kosten per stap", "Credits per stap: uitgegeven volgens het Higgsfield-saldo, gepland volgens het draaiboek."),
 "saldo": ("Higgsfield-saldo", "Het saldo bij de start van de serie en nu, uit de Higgsfield-balans."),
}
writes = [{"op": "set", "collection": "dash", "doc_id": "meta", "data": {"title": "CREATIVE ENGINE"}}]
for k, (t, d) in META.items():
    if k not in blobs: continue
    writes.append({"op": "set", "collection": "datasets", "doc_id": k, "data": {
        "title": t, "description": d,
        "source": {"kind": "file", "url": blobs[k], "name": k + ".json", "format": "json"},
        "updated": {"at": now, "by": "Claude"}}})
json.dump({"text": open("index.html").read()}, open("page.json", "w"), ensure_ascii=False)
writes.append({"op": "set", "collection": "files", "doc_id": "index.html", "file_path": "PAGE"})
json.dump(writes, open("batch.json", "w"), ensure_ascii=False, indent=1)
print(len(writes), "writes")
