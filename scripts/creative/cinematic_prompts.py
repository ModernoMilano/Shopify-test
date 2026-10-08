# Filmische serie (stijl Zegna / moodboard van de eigenaar): per shot de definitieve prompt + referentielijst.
# Een shot heeft een scene_prompt (cameraman-brief), handles uit de garderobe (leeg = sfeerbeeld van Milaan zonder kleding),
# optioneel ref_keys per handle (bv. ["primary", "back"]), optioneel light (de ene lichtbron op hem) en optioneel
# public: true voor een openbare plek (straat, kade, plein): dan komen er 2 of 3 verre, onscherpe voorbijgangers in.
# Zonder light geldt light_default_en uit model.json; beschrijf dan geen ander licht in scene_prompt. Een detail
# (framing "detail") heeft altijd een eigen light nodig: light_default_en gaat over zijn gezicht, en dat is uit beeld.
# Voorbeeld van de vorm: creative-engine/output/2026-10-06-zegna-stijl/shots.json. De teksten daarin zijn van vóór
# 8 oktober (filmwoorden, een andere man): niet overnemen, het script weigert ze.
# Staat er iemand in beeld (people 1), dan is dat altijd het vaste model uit creative-engine/data/model.json. Zijn gezicht
# komt via het Higgsfield-element (de placeholder); de referenties zijn alleen productfoto's (#1..#n), hooguit 4.
# Werkt het element niet, voeg dan --face-refs toe: dan gaan ref-1, ref-4 en ref-2 (4K) als #1-#3 vooraan mee.
# Nooit een andere man en nooit twee (people is 0 of 1). Het script stopt als model.json onvolledig is, of als een shot
# filmrol-woorden, een tweede man of een ander gezicht beschrijft.
# Gebruik: python3 -I scripts/creative/cinematic_prompts.py shots.json built.json [--face-refs]
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W = {i["handle"]: i for i in json.load(open(f"{ROOT}/creative-engine/data/wardrobe.json"))["items"]}
MEDIA = json.load(open(f"{ROOT}/creative-engine/data/higgsfield-media.json"))["media"]
MODEL_FILE = f"{ROOT}/creative-engine/data/model.json"

# Deze woorden gaven in de batch van 100 nepfilmranden en opgeplakte korrel. Ook geen los "film", behalve het vaste
# "No film borders" uit realism_en. Voorlopig komt er ook achteraf geen korrel bij. Gelijk aan FILM_WORDS in src/creative/prompt.ts.
FILM_WORDS = ["kodak", "portra", "ektar", "vision3", "fuji", "fujifilm", "cinestill", "ilford",
              "photographed on film", "shot on film", "film photograph", "film stock", "35mm film", "film grain", "film look",
              "still from a film", "film still", "filmic", "analog", "analogue", "grain", "grainy", "halation"]
FILM_RE = re.compile(r"\b(?:" + "|".join(re.escape(w) for w in FILM_WORDS) + r")\b|\bfilm\b(?! borders)", re.IGNORECASE)
# Een tweede of andere man (of een vrouw): er staat alleen het vaste model scherp in beeld.
SECOND_MAN_RE = re.compile(r"\b(?:two men|men|second man|other man|another man|older man|younger man|his son|son|father|"
                           r"brothers?|friends?|couple|woman|women|girlfriend|wife)\b", re.IGNORECASE)
# Een gezicht of haar dat niet het zijne is (model.json -> must_not_en). Zijn gezicht komt van het element.
OTHER_FACE_RE = re.compile(r"\b(?:beard|bearded|moustache|mustache|goatee|bald|balding|blond|blonde|shaved head|middle-aged|elderly|"
                           r"in his (?:thirties|forties|fifties|sixties)|"
                           r"(?:grey|gray|silver|white|black|red|blond|blonde)(?:-(?:grey|gray))?[- ](?:hair|haired))\b", re.IGNORECASE)
# model.json -> rules.image_model_with_products: met het model in beeld hoogstens 4 productfoto's (elk product minstens 1,
# dus een look van 5 stukken krijgt er 5). Een look heeft hooguit 5 stukken.
MAX_PRODUCT_REFS = 4
MAX_PIECES = 5


def load_model():
    """Leest het vaste model uit model.json en stopt met een duidelijke fout als er iets ontbreekt."""
    try:
        data = json.load(open(MODEL_FILE))
    except (OSError, ValueError) as e:
        raise SystemExit(f"{MODEL_FILE} is niet leesbaar: {e}")
    hf = data.get("higgsfield") or {}
    p = data.get("prompt") or {}
    keys = ("identity_en", "keep_en", "must_not_en", "realism_en", "light_default_en", "expression_en", "framing_en", "public_places_en")
    missing = [f"prompt.{k}" for k in keys if not p.get(k)]
    if not hf.get("element_placeholder"):
        missing.append("higgsfield.element_placeholder")
    faces = hf.get("face_refs") or []
    if not faces:
        missing.append("higgsfield.face_refs")
    for i, f in enumerate(faces):
        for k in ("file", "media_id", "upscale_job_id"):
            if not f.get(k):
                missing.append(f"higgsfield.face_refs[{i}].{k}")
    order = hf.get("face_ref_order") or []
    if not order:
        missing.append("higgsfield.face_ref_order")
    if missing:
        raise SystemExit(f"{MODEL_FILE} mist: {', '.join(missing)}")
    by_id = {os.path.splitext(os.path.basename(f["file"]))[0]: f for f in faces}
    unknown = [r for r in order if r not in by_id]
    if unknown:
        raise SystemExit(f"{MODEL_FILE}: face_ref_order noemt {', '.join(unknown)}, maar die staan niet in face_refs")
    return {
        "identity": p["identity_en"],
        "keep": p["keep_en"],
        "must_not": p["must_not_en"],
        "realism": p["realism_en"],
        "light": p["light_default_en"],
        "expression": p["expression_en"],
        "framing": p["framing_en"],
        "public_places": p["public_places_en"],
        "element": hf["element_placeholder"],
        # Alleen voor de terugval zonder element: de 4K-versies in vaste volgorde (ref-1, ref-4, ref-2).
        "fallback": [{"id": r, "file": by_id[r]["file"], "job_id": by_id[r]["upscale_job_id"]} for r in order],
    }


MODEL = load_model()
FACE = MODEL["identity"]


def sentence(text):
    return text[0].upper() + text[1:] + "."


def describe(item):
    labels = " + ".join(p["label"] for p in item["pieces"])
    return f'{item["title"]} ({labels})'

def refs_for(item, hero, keys=None):
    imgs = item["images"]
    if keys:
        return [imgs[k] for k in keys if imgs.get(k)]
    urls = [imgs["primary"]]
    if hero:
        for k in ("detail", "model"):
            if imgs.get(k) and imgs[k] not in urls:
                urls.append(imgs[k]); break
    return urls

def span(a, b):
    return f"#{a}" if a == b else f"#{a}-#{b}"

def his_refs(k):
    if k == 1:
        return "His reference image is #1: use it only for him and ignore its clothing, light and setting."
    return f"His reference images are {span(1, k)}: use them only for him and ignore their clothing, light and setting."

def face_refs(shot):
    """Alleen in de terugval (--face-refs): zijn gezichtsfoto's in 4K, vooraan. Bij een detail is één foto genoeg."""
    faces = MODEL["fallback"][:1] if shot["framing"] == "detail" else MODEL["fallback"]
    return [{"url": None, "file": f["file"], "label": f'ModernoMilano model (face, {f["id"]})', "media_id": f["job_id"], "kind": "face"} for f in faces]

def check_text(shot):
    text = " ".join(str(shot.get(k, "")) for k in ("scene_prompt", "worn_notes", "light"))
    found = sorted({m.lower() for m in FILM_RE.findall(text)})
    if found:
        raise SystemExit(f'{shot["n"]}: filmrol-woorden in het shot ({", ".join(found)}); haal ze weg')
    found = sorted({m.lower() for m in SECOND_MAN_RE.findall(text)})
    if found:
        raise SystemExit(f'{shot["n"]}: het shot noemt een andere persoon ({", ".join(found)}). Er staat alleen het vaste model '
                         f'scherp in beeld; noem geen tweede man, ook niet ontkennend (het script zet zelf dat hij de enige is). '
                         f'Verre voorbijgangers: zet "public": true')
    found = sorted({m.lower() for m in OTHER_FACE_RE.findall(text)})
    if found:
        raise SystemExit(f'{shot["n"]}: het shot beschrijft een ander gezicht of haar ({", ".join(found)}). Beschrijf zijn gezicht '
                         f'niet: dat komt van het element (creative-engine/data/model.json)')

def cap_products(shot, items, urls, keys):
    """Met hem in beeld hoogstens MAX_PRODUCT_REFS productfoto's; elk stuk houdt er minstens één."""
    if len(items) > MAX_PIECES:
        raise SystemExit(f'{shot["n"]}: {len(items)} stukken met het model in beeld, dus meer dan {MAX_PIECES} productfoto\'s. '
                         f'Kies minder stukken (een look heeft er hooguit {MAX_PIECES})')
    # Eerst de extra foto's van stukken zonder ref_keys, dan die van ref_keys, de langste lijst eerst.
    urls = [u if keys.get(it["handle"]) else u[:1] for it, u in zip(items, urls)]
    while sum(len(u) for u in urls) > MAX_PRODUCT_REFS and any(len(u) > 1 for u in urls):
        longest = max(range(len(urls)), key=lambda i: (len(urls[i]), i))
        urls[longest] = urls[longest][:-1]
    return urls

def build(shot, faces="element"):
    check_text(shot)
    if shot["people"] not in (0, 1):
        raise SystemExit(f'{shot["n"]}: people is {shot["people"]}; er staat nooit meer dan één man in beeld')
    handles = shot["handles"]
    items = [W[h] for h in handles]
    person = shot["people"] == 1
    detail = person and shot["framing"] == "detail"
    public = bool(shot.get("public"))
    if not items:
        if person:
            raise SystemExit(f'{shot["n"]}: het model staat in beeld, maar er zijn geen ModernoMilano-stukken (handles) opgegeven')
        if public:
            tail = (f'Nobody is in focus and there is no clothing in the picture. {sentence(MODEL["public_places"])} '
                    "No logos, labels or readable text anywhere. Photographic, not CGI: real optics.")
        else:
            tail = "There are no people and no clothing in the picture. No logos, signs, labels or readable text anywhere. Photographic, not CGI: real optics."
        return {"n": shot["n"], "title": shot["title_nl"], "handles": [], "people": 0, "framing": shot["framing"],
                "prompt": shot["scene_prompt"].strip() + "\n\n" + tail, "refs": []}
    if detail and not shot.get("light"):
        raise SystemExit(f'{shot["n"]}: een detail heeft een eigen "light" nodig (één lichtbron met richting); '
                         "light_default_en gaat over zijn gezicht, en dat is uit beeld")

    # Standaard alleen de producten (#1..#n); in de terugval eerst zijn gezicht (#1..#k).
    via_refs = person and faces == "refs"
    refs = face_refs(shot) if via_refs else []
    k = len(refs)
    hero = shot["framing"] in ("detail", "still-life") or len(items) <= 2
    keys = shot.get("ref_keys", {})
    urls = [refs_for(it, hero, keys.get(it["handle"])) for it in items]
    if person and sum(len(u) for u in urls) > MAX_PRODUCT_REFS:
        urls = cap_products(shot, items, urls, keys)
    lines = []
    for it, its_urls in zip(items, urls):
        nums = []
        for u in its_urls:
            refs.append({"url": u, "label": it["title"], "media_id": MEDIA.get(u), "kind": "product"})
            nums.append(f"#{len(refs)}")
        lines.append(f'- {describe(it)}, exactly as in reference image {" and ".join(nums)}')

    has_shoes = any(p["slot"] == "shoes" for it in items for p in it["pieces"])
    parts = [shot["scene_prompt"].strip()]
    if person:
        # Licht, uitsnede en uitdrukking vooraan, de kledingregels erachter.
        him = f"the man in reference image{'s' if k > 1 else ''} {span(1, k)}" if via_refs else MODEL["element"]
        if detail:
            parts.append(f'Only part of him is visible; his face is out of frame. He is {him}: the same skin tone, hands and build.'
                         + (f" {his_refs(k)}" if via_refs else ""))
        elif via_refs:
            parts.append(f'The man in reference images {span(1, k)}: {FACE}. {MODEL["keep"]} {his_refs(k)}')
        else:
            # Zijn gezicht komt van het element; niet opnieuw in woorden beschrijven.
            parts.append(f'The man: {him}. {MODEL["keep"]}')
        parts.append(shot.get("light") or MODEL["light"])
        if not detail and shot["framing"] in ("three-quarter", "waist-up"):
            parts.append(f'Framing: {MODEL["framing"]}.')
        if not detail:
            parts.append(f'Expression: {MODEL["expression"]}.')
            parts.append("For him: " + "; ".join(MODEL["must_not"]) + ".")
        parts.append("He wears only these ModernoMilano pieces and nothing else:\n" + "\n".join(lines))
    else:
        parts.append("The only clothing in the picture is these ModernoMilano pieces:\n" + "\n".join(lines))
    parts.append(f'How they are worn or arranged: {shot["worn_notes"].strip()}')
    fidelity = ("Reproduce every piece exactly as in its reference: same colour and shade, same knit or weave, same collar, "
                "same buttons or zip, same pockets, same length and fit. Do not redesign anything.")
    if person:
        if len(refs) == k + 1:
            fidelity += f" The garment reference (#{k + 1}) is only for the clothes: ignore any person or face in it."
        else:
            fidelity += f" The garment references ({span(k + 1, len(refs))}) are only for the clothes: ignore any person or face in them."
    parts.append(fidelity)
    if person:
        rules = ["His hands and wrists are bare."]
        if has_shoes:
            rules.append("The loafers are worn without socks, ankles bare, a mirrored left and right pair.")
        elif shot["framing"] in ("full-body",):
            raise SystemExit(f'{shot["n"]}: full-body without loafers')
        else:
            rules.append("His feet are not in the picture.")
        rules.append("He is the only person in focus." if public else "He is the only person in the picture.")
        parts.append(" ".join(rules))
        if public:
            parts.append(sentence(MODEL["public_places"]))
        parts.append("No logos, labels, badges or readable text anywhere in the picture. Photographic, not CGI.")
        parts.append(MODEL["realism"])
    else:
        parts.append("No logos, labels, badges or readable text anywhere in the picture. Photographic, not CGI: real optics.")
    return {"n": shot["n"], "title": shot["title_nl"], "handles": handles, "people": shot["people"],
            "framing": shot["framing"], "prompt": "\n\n".join(parts), "refs": refs}

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--face-refs"]
    if len(args) != 2:
        raise SystemExit("Gebruik: python3 -I scripts/creative/cinematic_prompts.py shots.json built.json [--face-refs] "
                         "(het gezicht komt uit creative-engine/data/model.json, niet uit een argument)")
    faces = "refs" if "--face-refs" in sys.argv else "element"
    final = json.load(open(args[0]))
    shots = final["final"]["shots"] if "final" in final else final["shots"]
    out = [build(s, faces) for s in shots]
    json.dump(out, open(args[1], "w"), indent=1)
    for o in out:
        n_faces = sum(1 for r in o["refs"] if r["kind"] == "face")
        missing = [r["url"] for r in o["refs"] if r["kind"] == "product" and not r["media_id"]]
        print(o["n"], o["title"], len(o["refs"]), "refs", f"({n_faces} face)", len(missing), "to import", len(o["prompt"].split()), "words")
