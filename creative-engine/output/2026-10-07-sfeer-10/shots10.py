# Tien sfeerbeelden voor social media (7 okt 2026): Reverso / Bundle & Save, Cashmere Sets,
# Cashmere Tops, Milano Sets (alleen lounge en Imperial). Bouwt de batch voor generate_image_batch.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
B = "https://cdn.shopify.com/s/files/1/1009/1197/2689/files/"
MEDIA_PATH = os.path.join(ROOT, "creative-engine", "data", "higgsfield-media.json")

NEW = {  # in deze serie geüpload
    "ChatGPTImageJul17_2026_07_11_07PM.png?v=1784324757": "822936aa-4606-495f-a52c-9fab92700ea6",
    "hf_20260822_130410_3847c12a-f3af-4168-ad00-7fce78052bdd_min.webp?v=1787810925": "01e88a16-778b-4c39-bff5-a41ea0c5b6a4",
    "ChatGPTImageJul28_2026_06_55_38PM.png?v=1785273393": "f781dc44-bec0-44be-95bf-55d565328cda",
    "ChatGPTImageJul28_2026_08_50_54PM.png?v=1785280107": "bcd51aea-1343-49b3-982d-331b2b54366b",
    "ChatGPTImageJul28_2026_08_12_16PM.png?v=1785273973": "223888bd-f693-455c-9748-13bae9a90aff",
    "ChatGPTImageJul28_2026_08_57_03PM.png?v=1785273972": "13fc3ca8-93fe-496e-83b5-9243c56e8afd",
    "ChatGPTImageMay15_2026_12_01_57PM.png?v=1778839329": "3fae50ff-e914-4058-90f1-7c36c243563d",
    "Outfitfoto_sGijs-89_366ae15f-b08a-456b-9ba9-0847b3ca23d0.jpg?v=1773659428": "f16f430e-2469-422b-a60a-1dd1c00e5f53",
    "ChatGPTImageMay15_2026_11_50_01AM.png?v=1778838615": "32c0ec2f-9907-4e0d-8a90-ed7e8f75b029",
    "Outfitfoto_sGijs-42.jpg?v=1773657092": "36cadcc9-4d35-4068-a5aa-58b3ce818350",
    "twotone_navy.png?v=1787092372": "273afbe5-9fea-473a-bb49-84a1966a13ce",
    "Scherm_afbeelding2026-02-12om18.32.01.png?v=1770921876": "99cfaa08-4ae2-4725-be2f-1cd61ed455aa",
    "morbido_beige.png?v=1787092209": "322fbd6a-523e-465a-bafa-bace44f62111",
    "ChatGPTImageAug7_2026_06_33_30PM.png?v=1786121798": "9e4cb145-9538-4050-bb9f-41598632ec39",
    "ChatGPTImageAug18_2026_11_56_45PM.png?v=1787090219": "b8a571f2-cf5e-4b20-81df-b39562271776",
    "ChatGPTImageAug5_2026_06_07_12PM.png?v=1785946998": "7eadcb08-9ace-495c-9924-e335b9df8565",
    "ChatGPTImageAug5_2026_06_31_10PM.png?v=1785947511": "4651e9fb-44e7-4d4c-bacd-6fdf83dce918",
    "ChatGPTImageAug5_2026_06_06_07PM.png?v=1785946997": "8519032c-d5c0-49b3-a4bb-53af3f979d1d",
}
R = {
    "reverso_nero": ["ChatGPTImageJul17_2026_07_11_07PM.png?v=1784324757", "hf_20260822_130410_3847c12a-f3af-4168-ad00-7fce78052bdd_min.webp?v=1787810925"],
    "midnight": ["ChatGPTImageJul28_2026_06_55_38PM.png?v=1785273393", "ChatGPTImageJul28_2026_08_50_54PM.png?v=1785280107"],
    "onyx": ["ChatGPTImageJul28_2026_08_12_16PM.png?v=1785273973", "ChatGPTImageJul28_2026_08_57_03PM.png?v=1785273972"],
    "excl_navy": ["ChatGPTImageMay15_2026_12_01_57PM.png?v=1778839329", "Outfitfoto_sGijs-89_366ae15f-b08a-456b-9ba9-0847b3ca23d0.jpg?v=1773659428"],
    "imperial_brown": ["ChatGPTImageMay15_2026_11_50_01AM.png?v=1778838615", "Outfitfoto_sGijs-42.jpg?v=1773657092"],
    "twotone_navy": ["twotone_navy.png?v=1787092372", "Scherm_afbeelding2026-02-12om18.32.01.png?v=1770921876"],
    "morbido_beige": ["morbido_beige.png?v=1787092209", "ChatGPTImageAug7_2026_06_33_30PM.png?v=1786121798"],
    "bellagio_ivory": ["ChatGPTImageAug18_2026_11_56_45PM.png?v=1787090219", "ivoor_2_detail.png?v=1786462567", "ivoor_3_model.png?v=1786462567"],
    "camicia_oliva": ["ChatGPTImageAug5_2026_06_31_10PM.png?v=1785947511", "ChatGPTImageAug5_2026_06_06_07PM.png?v=1785946997", "ChatGPTImageAug5_2026_06_07_12PM.png?v=1785946998"],
    "oliva_set": ["ChatGPTImageJul17_2026_04_26_31PM.png?v=1784304015", "hf_20260824_111215_1c799c2c-4439-4943-91e3-40b34c40938f_min.webp?v=1787811185", "hf_20260824_111435_5ca6d4c3-8f9d-4f73-baf1-76ec92d12cf5_min.webp?v=1787811185"],
    "tee": ["ChatGPTImageJul2_2026_09_33_06PM.png?v=1783020802"],
    "loafer_nero": ["ChatGPTImageAug7_2026_07_19_47PM.png?v=1786136732"],
    "loafer_notte": ["ChatGPTImageAug7_2026_07_21_22PM.png?v=1786136813"],
    "loafer_sabbia": ["ChatGPTImageAug7_2026_08_07_01PM.png?v=1786136954"],
    "loafer_moro": ["ChatGPTImageAug7_2026_07_19_02PM.png?v=1786136639"],
    "sart": ["charcoal_1_product.png?v=1787173186"],
    "atelier": ["ChatGPTImageMay15_2026_11_22_06AM.png?v=1778836941"],
}
SPEC = {
    "reverso_nero": "MILANO REVERSO NERO SET: a black smooth padded sleeveless gilet with a stand collar, a full black zip and an elasticated hem, its off-white reverse side showing as a thin white edge at the collar and armholes; a plain white crew-neck T-shirt in smooth mercerised cotton; black slim tapered trousers with a drawstring waist.",
    "midnight": "MILANO REVERSO MIDNIGHT SET: a black smooth hooded full-zip lounge jacket; a black smooth padded sleeveless gilet with a stand collar and full zip, its white reverse side showing as a thin white edge at the collar, armholes and front opening; a plain white crew-neck T-shirt; black slim lounge trousers.",
    "onyx": "MILANO CASHMERE ONYX SET: a black cashmere zip jacket with a ribbed stand collar, ribbed cuffs and ribbed hem; a black cashmere hooded full-zip top; a plain white crew-neck T-shirt; black cashmere joggers with a drawstring and ribbed ankle cuffs.",
    "excl_navy": "EXCLUSIVE MILANO LOUNGE SET - NAVY: a dark navy smooth technical-knit set: a hooded full-zip jacket with a silver zip, ribbed cuffs and a gathered elasticated hem; matching trousers with an elasticated waist and a slim tapered leg.",
    "imperial_brown": "IMPERIAL MILANO ZIP SET - BROWN: a dark chocolate-brown smooth technical-stretch set: a zip-up jacket with a pointed shirt collar, a silver zip and gathered elasticated cuffs and hem; matching trousers with an elasticated waist.",
    "twotone_navy": "MILANO KNITTED TWO-TONE CASHMERE SET - NAVY: a navy cashmere knit set: a full-zip jacket with a stand collar, a silver zip with a rectangular pull, ribbed cuffs and hem, and a cream-and-white stripe running down the outer length of each sleeve; matching joggers with a drawstring, the same stripe down each side and ribbed ankle cuffs.",
    "morbido_beige": "MILANO CASHMERE MORBIDO RELAXED SET - BEIGE: an oatmeal-beige melange cashmere set: a hooded full-zip knit jacket with a drawstring hood, a silver zip, ribbed cuffs and ribbed hem; relaxed wide straight-leg trousers with a drawstring waist.",
    "bellagio_ivory": "MILANO CASHMERE BELLAGIO - IVORY: an ivory cashmere full-zip cardigan with a ribbed stand collar, a fine vertical rib-textured knit body, a silver zip, ribbed cuffs and ribbed hem.",
    "camicia_oliva": "MILANO CASHMERE CAMICIA - OLIVA: a dark olive knitted cashmere overshirt with a pointed collar, a button front with dark buttons, two buttoned flap patch pockets at the lower front, a fine textured knit, ribbed hem and cuffs.",
    "oliva_set": "MILANO OLIVA SET: a smooth olive sleeveless gilet with a high stand collar and a full silver zip; a white long-sleeve crew-neck T-shirt; olive trousers with a drawstring waist.",
    "tee": "PURO SUPIMA MERCER TEE - WHITE: a plain white crew-neck T-shirt in smooth mercerised cotton.",
    "loafer_nero": "MILANO SUEDE LOAFERS - NERO: black suede slip-on loafers with white soles.",
    "loafer_notte": "MILANO SUEDE LOAFER - NOTTE: navy suede slip-on loafers with white soles.",
    "loafer_sabbia": "MILANO SUEDE LOAFER - SABBIA: sand suede slip-on loafers with white soles.",
    "loafer_moro": "MILANO SUEDE LOAFERS - MORO: dark brown suede slip-on loafers with white soles.",
    "sart": "MILANO SARTORIALE PANT - CHARCOAL: charcoal tailored trousers with a drawstring waist and a front crease.",
    "atelier": "MILANO ATELIER TAILORED TROUSER - BEIGE: beige slim tailored trousers.",
}
REAL = ("He looks like a real man photographed on film, not a model: ordinary proportions, a slightly asymmetric face, "
        "visible pores, fine lines and natural under-eye shadows, uneven stubble, an unposed expression caught mid-moment. "
        "The clothes behave like real fabric: soft creases at the elbows and waist, a little slack where they sit. "
        "Real optics: shallow depth of field, slight lens softness, film grain, no retouching, no beauty filter. "
        "The frame feels like a still from a film, not an advert.")
# (titel, man, scène, [(ref, spec)], hoe gedragen, voeten)
S = [
 ("Arcadenhof op het blauwe uur",
  "a man in his late thirties of southern Italian appearance with short black curly hair, a strong nose and a few days of stubble",
  "Blue hour in the empty arcaded courtyard of an old Milanese palazzo: two storeys of stone arches, warm lamps just switched on under the vaults, the sky deep blue above. He walks slowly along the colonnade towards the camera, hands loose, looking off to one side, caught mid-stride. Wide composition: he is small in the lower third of the frame, the arches repeat behind him and there is quiet empty space above. Shot on a 35mm lens at f/2 on Kodak Vision3 500T, gentle halation around the lamps, fine grain, cool blue and warm amber.",
  [("reverso_nero", "reverso_nero"), ("loafer_nero", "loafer_nero")],
  "The gilet zipped halfway over the white T-shirt; black trousers; black loafers without socks, ankles bare.", "loafers"),
 ("Achterbank bij nacht",
  "a man in his early thirties of North African heritage with a shaved head, light brown skin and a short trimmed beard",
  "Night, in the back seat of a car gliding through Milan: he sits by the window with his head turned slightly towards the glass, the streetlights outside streaking past in soft orange and white bokeh, reflections on the window. Intimate waist-up framing from the opposite seat, his face half lit by the passing lights. Plain dark leather interior with no logos, badges or screens. Shot handheld on a 50mm lens at f/1.4 on Kodak Vision3 500T, heavy grain, deep shadows.",
  [("midnight", "midnight")],
  "White T-shirt, the black hooded jacket open over it with the hood down, the gilet worn over the jacket; the trousers mostly out of frame.", "none"),
 ("Penthouse met skyline",
  "a man in his mid-forties of East Asian heritage with straight black hair pushed back, clean-shaven, fine lines at the eyes",
  "Evening in a minimalist Milan penthouse: he sits sideways on a low cream sofa by a floor-to-ceiling window, one knee pulled up, barefoot, a glass of water in his hand, looking out over the city at blue hour. The skyline is a soft field of out-of-focus lights with no lettering on any building. The black zip jacket of the set lies draped over the arm of the sofa. Warm low lamplight inside, cool blue outside. Shot on a 35mm lens at f/2 on Kodak Portra 800, fine grain.",
  [("onyx", "onyx")],
  "White T-shirt with the black hooded zip top open over it, hood down; black joggers; barefoot; the black zip jacket draped over the sofa arm.", "barefoot"),
 ("Zondagochtend in het park",
  "a tall man in his early fifties with sandy grey hair, a weathered face and light stubble",
  "A misty autumn Sunday morning in Parco Sempione: he walks along a path of fallen yellow leaves with a slender grey whippet on a plain leather lead, both seen from the side, low sun backlighting the mist between the plane trees. Full length, he is in the right third of the frame and the path leads off into the soft fog. The dog wears only a plain brown leather collar. Nobody else is in the park. Shot on a 50mm lens at f/2.8 on Kodak Portra 400, fine grain, soft golden backlight.",
  [("excl_navy", "excl_navy"), ("tee", "tee"), ("loafer_notte", "loafer_notte")],
  "The jacket half open over the white T-shirt, hood down; navy trousers; navy loafers without socks, ankles bare.", "loafers"),
 ("Espresso aan de bar",
  "a man in his late forties with dark brown wavy hair greying at the temples and a neat salt-and-pepper beard",
  "Early morning in an old Milanese bar with a long marble counter, a brass rail and wood panelling: he stands at the counter lifting a small white espresso cup, eyes lowered, a quiet moment before the day. Morning sun slants through the window and falls across the marble. Waist-up, seen from slightly beside him. The wall behind is softly out of focus, with no bottles, no labels and no signs; nobody else is in the bar. Shot on a 50mm lens at f/2 on Kodak Portra 400, fine grain, warm.",
  [("imperial_brown", "imperial_brown"), ("tee", "tee")],
  "The jacket zipped halfway over the white T-shirt.", "none"),
 ("Bij het haardvuur",
  "a man in his sixties with thick white hair, a short white beard and a lined, tanned face",
  "A winter evening in a wooden chalet in Cortina d'Ampezzo: he sits deep in a worn leather armchair beside a stone fireplace, a book open on his knee, looking into the fire, barefoot on a sheepskin rug, snow falling outside the dark window. The firelight is the only light, warm and flickering on one side of his face. Three-quarter framing. Shot on a 35mm lens at f/1.8 on Kodak Vision3 500T, warm, deep shadows, fine grain.",
  [("twotone_navy", "twotone_navy"), ("tee", "tee")],
  "The jacket zipped halfway over the white T-shirt, the stripes visible down the sleeves and trouser legs; barefoot.", "barefoot"),
 ("Mist op het Comomeer",
  "a man in his early forties of West African heritage with close-cropped hair and a short beard flecked with grey",
  "Dawn on the stone terrace of a lakeside villa on Lake Como: thick mist lies on the water and the mountains are only faint shapes. He stands at the stone balustrade holding a plain ceramic mug with steam rising, looking out over the water. Wide, quiet composition: he stands on the left and the misty lake fills the rest of the frame. Soft, cool, even light. Shot on a 50mm lens at f/2.8 on Kodak Portra 160, fine grain, muted pastel colour.",
  [("morbido_beige", "morbido_beige"), ("loafer_sabbia", "loafer_sabbia")],
  "The hooded jacket zipped up to the chest, hood down; the relaxed trousers; sand loafers without socks, ankles bare.", "loafers"),
 ("Blauw uur aan de Navigli",
  "a slim man in his mid-thirties with tousled light brown hair and a clean-shaven, slightly asymmetric face",
  "Blue hour on the Naviglio Grande: he leans with his forearms on the iron railing of a small footbridge, looking down the canal, the warm lights of the old houses reflected in the still water. Waist-up from the side, the canal and its reflections filling the background in soft bokeh, with no signs or lettering anywhere. Shot on a 50mm lens at f/1.8 on Kodak Vision3 500T, cool blue and warm amber, fine grain.",
  [("bellagio_ivory", "bellagio_ivory"), ("sart", "sart")],
  "The cardigan zipped up to the collar; charcoal trousers.", "none"),
 ("In de oude tram",
  "a man in his fifties with a receding hairline, short dark grey hair and a strong jaw",
  "Morning in an old wooden Milan tram: he sits on a varnished wooden bench by an open window, one arm on the window ledge, looking out as the city passes in a blur of ochre facades. Sunlight flickers across his face and the warm wooden interior. Nobody else is on the tram, and there are no signs, maps, route numbers or any text inside it. Waist-up. Shot on a 35mm lens at f/2 on Kodak Portra 400, warm, fine grain.",
  [("camicia_oliva", "camicia_oliva"), ("tee", "tee"), ("atelier", "atelier")],
  "The overshirt open over the white T-shirt; beige trousers.", "none"),
 ("Op de fiets langs het kanaal",
  "a man in his late twenties with dark wavy hair to the collar, olive skin and a light moustache",
  "Early morning on the towpath of the Naviglio Pavese just outside Milan: he rides an old plain black bicycle with no badges or lettering, unhurried, one hand on the handlebar, poplars and a low sun behind him and morning haze over the water. Full length from the side, in motion, the background softly blurred. Nobody else is on the path. Shot on a 50mm lens at f/2.8 on Kodak Portra 400, warm golden backlight, fine grain.",
  [("oliva_set", "oliva_set"), ("loafer_moro", "loafer_moro")],
  "The gilet zipped up over the white long-sleeve T-shirt; olive trousers; dark brown loafers without socks, ankles bare.", "loafers"),
]

def build():
    M = json.load(open(MEDIA_PATH))
    for f, mid in NEW.items():
        M["media"].setdefault(B + f, mid)
    json.dump(M, open(MEDIA_PATH, "w"), indent=1)
    out = []
    for i, (title, man, scene, refs, worn, feet) in enumerate(S, 1):
        medias, lines = [], []
        for rk, sk in refs:
            nums = []
            for f in R[rk]:
                medias.append({"value": M["media"][B + f], "role": "image_references"}); nums.append(f"#{len(medias)}")
            lines.append(f"- {SPEC[sk]} (reference image{'s' if len(nums) > 1 else ''} {', '.join(nums)})")
        foot = {"loafers": "Loafers are worn without socks, ankles bare.", "barefoot": "He is barefoot.",
                "none": "His feet are not in the picture."}[feet]
        prompt = "\n\n".join([
            scene,
            f"The man: {man}; he does not resemble any actor or public figure. {REAL}",
            "He wears only these ModernoMilano pieces and nothing else:\n" + "\n".join(lines),
            f"How they are worn: {worn}",
            "Reproduce every piece exactly as in its reference images: same colour and shade, same knit or fabric, same collar, same zip or buttons, same pockets, same stripes or trim, same length and fit. Do not redesign, simplify or add anything.",
            f"His hands and wrists are bare: no ring, no watch, no bracelet, no glasses. {foot} He is the only person in the picture.",
            "No logos, labels, badges or readable text anywhere in the picture. Photographic, not CGI.",
        ])
        out.append({"index": i, "title": title, "params": {"model": "nano_banana_pro", "aspect_ratio": "4:5", "resolution": "2k", "prompt": prompt, "medias": medias}})
    return out

if __name__ == "__main__":
    o = build()
    json.dump(o, open(os.path.join(HERE, "built10.json"), "w"), indent=1)
    print(json.dumps([{"index": x["index"], "params": x["params"]} for x in o], ensure_ascii=False))
