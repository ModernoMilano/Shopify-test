# 100 gevarieerde beelden (7 okt 2026). Categorieën: P = met model (20-40, Italiaans), O = product op locatie
# zonder model, L = necklabel met logo, A = Italiaanse sfeer zonder kleding.
# Gebruik: python3 -I shots100.py [ids...]  -> print batch-JSON voor generate_image_batch
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(OUT, "..", ".."))
B = "https://cdn.shopify.com/s/files/1/1009/1197/2689/files/"

def _data(path):
    src = open(path).read().split("\ndef build")[0]
    ns = {"__file__": path}; exec(compile(src, path, "exec"), ns); return ns
_a = _data(os.path.join(OUT, "2026-10-07-50-producten", "shots50.py"))
_b = _data(os.path.join(OUT, "2026-10-07-sfeer-10", "shots10.py"))
R = {**_a["R"], **_b["R"]}
SPEC = {**_a["SPEC"], **_b["SPEC"]}
SPEC["reverso_nero"] = SPEC["reverso_nero"].replace("a black smooth padded sleeveless gilet", "a black sleeveless gilet with a SMOOTH, FLAT matte shell (no puffy quilting, no horizontal channels)")
SPEC["midnight"] = SPEC["midnight"].replace("a black smooth padded sleeveless gilet", "a black sleeveless gilet with a SMOOTH, FLAT, thinly padded matte shell (no puffy quilting, no horizontal channels)")
SPEC["notte_set"] = ("MILANO NOTTE CASHMERE SET: a navy gilet with a SMOOTH, FLAT, thinly padded matte shell (no puffy quilting), a stand collar "
                     "and armholes edged in thin WHITE, and a full zip; a navy long-sleeve knit polo with three buttons; navy tailored trousers; "
                     "and navy suede loafers with white soles.")
MEDIA = json.load(open(os.path.join(ROOT, "creative-engine", "data", "higgsfield-media.json")))["media"]

# Logo en echte necklabels (geüpload 7 okt): zwart script-logo op crème, en twee productfoto's met het label.
# Het juiste label (door de eigenaar aangeleverd, brand/assets/necklabel.jpg) + het script-logo.
LABEL_IDS = ["72a49aff-1436-4dc8-8d02-079409275e78", "18dbf76e-4b08-4247-9451-06dd01d50a3c"]

MEN = {
 "a": "a man in his mid-twenties of Italian appearance with thick dark wavy hair, olive skin, dark brown eyes and light stubble",
 "b": "a man of about thirty of Italian appearance with short dark brown hair combed back, a straight strong nose and a trimmed dark beard",
 "c": "a man in his late twenties from Naples with short dark brown curly hair, light olive Mediterranean skin, brown eyes and a clean-shaven face",
 "d": "a man in his mid-thirties of northern Italian appearance with light brown hair, grey-green eyes and short stubble",
 "e": "a man in his early thirties of Italian appearance with dark hair cut short at the sides, thick eyebrows and a neat moustache",
 "f": "a man of about twenty-five from Palermo with dark brown hair falling over his forehead, light olive Mediterranean skin with a summer tan, brown eyes and a short stubble",
 "g": "a man in his late thirties of Italian appearance with dark hair greying slightly at the temples, a lean face and stubble",
 "h": "a tall man of about thirty of Italian appearance with medium-length dark hair tucked behind his ears and a short beard",
 "i": "a man in his early twenties of Italian appearance with short dark hair, a boyish face and a few freckles",
 "j": "a man of about thirty-five of Italian appearance with a closely shaved head, dark eyebrows and a short dark beard",
}
REAL = ("He looks like a real man photographed on film, not a model: ordinary proportions, a slightly asymmetric face, visible pores, "
        "natural skin texture, an unposed expression caught mid-moment. The clothes behave like real fabric: soft creases, a little slack "
        "where they sit. Real optics: shallow depth of field, slight lens softness, film grain, no retouching, no beauty filter.")
LOOK = "An editorial social-media photograph with a warm Italian feeling, natural colour, quietly luxurious, like a still from a film."
REPRO = ("Reproduce every piece exactly as in its reference images: same colour and shade, same knit or fabric, same collar, same zip or "
         "buttons, same pockets, same stripes or trim, same length and fit. Do not redesign, simplify or add anything.")
NOTEXT = "No logos, labels, badges, signs or readable text anywhere in the picture. Photographic, not CGI."
LABEL = ("Inside the back of the neck, centred just below the collar or neckline, is the ModernoMilano neck label exactly as in "
         "reference image #{a}: a soft ivory satin label with a subtle sheen, a fine stitched line running just inside all four edges, "
         "and both short ends folded under and stitched down. On it, centred and filling most of the label, the 'ModernoMilano' wordmark "
         "in black flowing script, drawn exactly like the logo in reference image #{b}. There is no size tab and nothing else on the label. "
         "The label is sharp and clearly legible.")
LABELTEXT = ("The only text anywhere in the picture is the 'ModernoMilano' wordmark on the neck label, spelled exactly like that. "
             "No other logos, labels, badges, signs or readable text. Photographic, not CGI.")
FEET = {"loafers": "Loafers are worn without socks, ankles bare.", "barefoot": "He is barefoot.", "none": "His feet are not in the picture."}

# (id, cat, titel, refs, scène, hoe gedragen/gelegd, voeten, man)
S = [
 # ---------- P: met model ----------
 ("P01","P","Brera bij gouden uur",["reverso_nero","loafer_nero"],
  "Golden hour in a narrow cobbled street in Brera, ochre facades and green shutters: he walks towards the camera and glances back over his shoulder, caught mid-stride. Full length, he is in the lower third of the frame with the warm street rising behind him. Shot on a 35mm lens at f/2 on Kodak Portra 400, low sun, long shadows.",
  "The gilet zipped halfway over the white T-shirt; black trousers; black loafers.","loafers","a"),
 ("P02","P","Op de achtersteven",["sabbia_set","loafer_sabbia"],
  "Late afternoon on Lake Como: he sits at the stern of an old varnished mahogany runabout boat with cream leather seats, one arm along the backrest, looking out over the water towards Bellagio. The boat has no badges or lettering. Full length, seated. Shot on a 50mm lens at f/2.8 on Kodak Portra 160, soft sun glinting on the water.",
  "The sand gilet zipped up over the white T-shirt; sand trousers; sand loafers.","loafers","d"),
 ("P03","P","Ochtend op de kerktrappen",["excl_navy","tee","loafer_notte"],
  "Early morning on the wide stone steps of a church square in Milan, pigeons in the soft background: he sits on a step with his forearms on his knees, holding a small white ceramic espresso cup, looking across the empty square. Full length, seated, the square rising behind him. Shot on a 35mm lens at f/2.8 on Kodak Portra 400, cool morning light.",
  "The hooded jacket half open over the white T-shirt, hood down; navy trousers; navy loafers.","loafers","i"),
 ("P04","P","Lachen aan het cafétafeltje",["imperial_brown","tee"],
  "Early morning at an outdoor café table on an empty Milan piazza, the other tables still empty and nobody else anywhere: he sits at a small round marble table, stirring an espresso, and laughs at something off camera, eyes creased. Waist-up, seated, the empty piazza soft behind him. Shot on a 50mm lens at f/2 on Kodak Portra 400, warm sun.",
  "The jacket zipped halfway over the white T-shirt.","none","b"),
 ("P05","P","Moka op het fornuis",["lounge_gray"],
  "Sunday morning in a sunlit Milan apartment kitchen with old tiles: he stands barefoot at the gas stove waiting for a moka pot, one hand in his pocket, sleepy and relaxed, sunlight across the room. Three-quarter length. Shot on a 35mm lens at f/2 on Kodak Portra 400, soft warm light.",
  "The zip jacket zipped halfway; joggers; barefoot.","barefoot","d"),
 ("P06","P","Ontbijt op het terras",["lusso_beige","loafer_sabbia"],
  "Breakfast on a hotel terrace above Lake Como: he sits at a small table with a cappuccino and a cornetto, legs crossed, looking at the lake, morning sun. Full length, seated, the lake and mountains soft behind. Shot on a 50mm lens at f/2.8 on Kodak Portra 160.",
  "The jacket zipped halfway; trousers; sand loafers.","loafers","g"),
 ("P07","P","Op de steiger bij zonsopkomst",["champagne_set"],
  "Sunrise on the wooden jetty of a lake villa on Lake Como: he sits on the edge of the jetty, barefoot, feet just above the still water, hood down, looking at the mist on the lake. Full length from the side. Shot on a 50mm lens at f/2.8 on Kodak Portra 160, pastel dawn light.",
  "The hooded jacket zipped up to the chest, hood down; trousers; barefoot.","barefoot","a"),
 ("P08","P","Langs de bakkerij",["bellagio_burgundy","sart","loafer_moro"],
  "Dusk in a Milan street: he walks past the warmly lit window of an old bakery, hands in his trouser pockets, looking down the street. The window glows with bread but has no lettering. Full length, slightly from the side. Shot on a 35mm lens at f/2 on Kodak Vision3 500T, warm and cool light.",
  "The cardigan zipped up to the collar; charcoal trousers; dark brown loafers.","loafers","b"),
 ("P09","P","Aperitivo aan de bar",["bergamo_bordeaux","sart"],
  "Evening in an old Milan bar with dark wood and a brass counter: he leans on the counter holding an orange spritz in a plain glass, smiling slightly, warm lamps behind. No bottles or labels in view. Waist-up. Shot on a 50mm lens at f/1.8 on Kodak Vision3 500T.",
  "The polo with the top button open; charcoal trousers.","none","e"),
 ("P10","P","Lunch aan het meer",["lido_notte","atelier_beige"],
  "Lunch on a terrace on Lake Como with a white tablecloth, glasses of water and bread: he sits at the table, turned in his chair, laughing, the lake bright behind him. Waist-up, seated. Shot on a 50mm lens at f/2.8 on Kodak Portra 400, bright soft light.",
  "Navy knit polo with the top button open; beige trousers.","none","h"),
 ("P11","P","In de haven",["sorrento_ottanio","atelier_beige","loafer_sabbia"],
  "A small harbour on Lake Como with colourful old houses: he sits on an iron mooring bollard by the water, one foot up, looking along the harbour, wooden boats behind him. Full length, seated. Shot on a 50mm lens at f/2.8 on Kodak Portra 400, afternoon sun.",
  "Teal short-sleeve knit polo; beige trousers; sand loafers.","loafers","j"),
 ("P12","P","Aan de aanlegsteiger",["torino_perla","tee","sart"],
  "Dusk at the ferry pier of Bellagio: he stands at the end of the pier with his hands in his pockets, looking out at the lake, the lights of the far shore coming on. Waist-up. Shot on a 50mm lens at f/2 on Kodak Vision3 500T, blue hour.",
  "The double-breasted knit blazer open over the white T-shirt; charcoal trousers.","none","b"),
 ("P13","P","Langs de platanen",["pieno_sabbia","sig_ls_white","atelier_beige","loafer_sabbia"],
  "Golden hour on the lakefront promenade of a town on Lake Como, with plane trees: he walks along the promenade, unhurried, looking at the water. Full length, the low lakeside wall and the lake soft behind. Shot on a 50mm lens at f/2.8 on Kodak Portra 400, backlit.",
  "The sleeveless knit gilet zipped up over the white long-sleeve T-shirt; beige trousers; sand loafers.","loafers","e"),
 ("P14","P","Wind op de veerboot",["imperial_green","tee"],
  "On the open deck of a lake ferry on Lake Como: he holds the white railing, wind in his hair, squinting into the sun, mountains behind. Waist-up. Shot on a 35mm lens at f/2.8 on Kodak Portra 400, bright and breezy.",
  "The jacket zipped halfway over the white T-shirt.","none","c"),
 ("P15","P","Station in de ochtend",["midnight"],
  "Early morning in a grand old railway station in Milan with high arched iron and glass roof: he stands on an empty platform with his hands in his jacket pockets, looking down the tracks. No signs, boards or lettering. Waist-up. Shot on a 35mm lens at f/2 on Kodak Portra 800, cool morning light.",
  "White T-shirt, the black hooded jacket open over it, hood down, the gilet over the jacket; black trousers.","none","c"),
 ("P16","P","Trap in Bellagio",["notte_set"],
  "A narrow stepped lane in Bellagio with flower pots and old shutters: he walks down the stone steps towards the camera, one hand on the wall. Full length. Shot on a 35mm lens at f/2.8 on Kodak Portra 400, soft morning light.",
  "Smooth navy gilet with thin white edges over the navy knit polo; navy trousers; navy suede loafers.","loafers","g"),
 ("P17","P","Villatuin met cipressen",["tabacco_set"],
  "The gravel path of a lakeside villa garden with tall cypresses and a stone balustrade on Lake Como: he walks along the path, looking to the side. Full length. Shot on a 50mm lens at f/2.8 on Kodak Portra 400, late afternoon light.",
  "Dark brown hooded jacket open over the cream knit polo; dark brown trousers; dark brown loafers.","loafers","h"),
 ("P18","P","Dak bij nacht",["onyx","loafer_nero"],
  "Night on a Milan rooftop terrace, the city lights soft and out of focus: he zips up the black jacket against the evening chill, looking out over the city. Three-quarter length. Shot on a 35mm lens at f/1.8 on Kodak Vision3 500T.",
  "White T-shirt, the black hooded zip top under the black zip jacket; black joggers; black loafers.","loafers","j"),
 ("P19","P","Langs de Navigli",["excl_brown","tee","loafer_moro"],
  "Sunrise along the Naviglio Grande, the water still and the old houses pastel: he walks along the canal with his hands in his pockets. Full length, from the side. Nobody else on the path. Shot on a 35mm lens at f/2.8 on Kodak Portra 400, soft dawn light.",
  "The jacket half open over the white T-shirt; brown trousers; dark brown loafers.","loafers","f"),
 ("P20","P","Balkon in Brera",["lounge_navy"],
  "Dawn on a small iron balcony with red geraniums over a quiet Brera street: he leans on the railing with a cup of coffee, barefoot, looking down at the street. Three-quarter length. Shot on a 50mm lens at f/2 on Kodak Portra 400, soft pink morning light.",
  "The zip jacket zipped halfway; joggers; barefoot.","barefoot","e"),
 ("P21","P","Vensterbank met regen",["morbido_grey"],
  "A rainy afternoon in a villa on Lake Como: he sits on a deep window seat with a book, barefoot, knees up, rain on the glass and the grey lake outside. Three-quarter. Shot on a 50mm lens at f/2 on Kodak Portra 400, soft grey light.",
  "The hooded cardigan zipped halfway, hood down; relaxed trousers; barefoot.","barefoot","i"),
 ("P22","P","Platanenlaan in de mist",["mocha_set","loafer_moro"],
  "An avenue of plane trees in the park of Monza on a foggy autumn morning: he walks along the avenue, fallen leaves at his feet. Full length, centred, the fog soft around him. Shot on a 50mm lens at f/2.8 on Kodak Portra 400.",
  "The zip jacket zipped halfway; joggers; dark brown loafers.","loafers","h"),
 ("P23","P","Gang met cementtegels",["twotone_navy","tee"],
  "Evening in the hallway of an old Milan apartment with patterned cement tiles and a tall door: he leans in a doorway, barefoot, arms folded, smiling. Three-quarter length. Shot on a 35mm lens at f/2 on Kodak Portra 800, warm lamplight.",
  "The jacket zipped halfway over the white T-shirt; joggers; barefoot.","barefoot","j"),
 ("P24","P","Brug in de Dolomieten",["morbido_beige","loafer_sabbia"],
  "Dawn on an old stone bridge over a mountain stream in the Dolomites, pine forest and peaks behind: he stands on the bridge holding a steaming mug. Full length. Shot on a 35mm lens at f/2.8 on Kodak Portra 160, cool clear light.",
  "The hooded jacket zipped up to the chest, hood down; relaxed trousers; sand loafers.","loafers","c"),
 ("P25","P","Kastanjes aan de kade",["bellagio_green","atelier_beige","loafer_tabacco"],
  "An autumn afternoon on a low stone wall by Lake Como: he sits on the wall holding a paper cone of roasted chestnuts, looking at the water. Full length, seated. Shot on a 50mm lens at f/2.8 on Kodak Portra 400, soft golden light.",
  "The cardigan zipped up; beige trousers; cognac loafers.","loafers","d"),
 ("P26","P","Atelier met hoge ramen",["camicia_sabbia","tee","atelier_beige"],
  "An artist's studio in Milan with tall steel windows and canvases leaning against the wall: he stands by the window, coffee in hand, looking at a canvas. Three-quarter, feet out of frame. Shot on a 35mm lens at f/2 on Kodak Portra 400, soft north light.",
  "The overshirt open over the white T-shirt; beige trousers.","none","f"),
 ("P27","P","Aan het stuur",["camicia_grafite","tee","sart"],
  "On Lake Como: he steers an old varnished mahogany motorboat with a slim wooden steering wheel, wind in his hair, the lake and mountains behind. The boat has no badges or lettering. Waist-up. Shot on a 35mm lens at f/2.8 on Kodak Portra 400, bright sun.",
  "The overshirt open over the white T-shirt; charcoal trousers.","none","g"),
 ("P28","P","Koffie bij het raam",["lido_avena","sart"],
  "Morning by the tall window of a Milan apartment: he holds a cup of coffee in both hands and looks out, soft light on his face. Close portrait from the chest up. Shot on an 85mm lens at f/2 on Kodak Portra 400.",
  "Oatmeal knit polo with the top button open.","none","i"),
 ("P29","P","Binnenplaats met klimop",["torino_oliva","tee","sart","loafer_moro"],
  "An ivy-covered courtyard of an old Milanese palazzo: he walks through the courtyard towards an archway, looking down, one hand in his pocket. Full length. Shot on a 35mm lens at f/2.8 on Kodak Portra 400, soft shade.",
  "The double-breasted knit blazer open over the white T-shirt; charcoal trousers; dark brown loafers.","loafers","a"),
 ("P30","P","Leesstoel",["vela_cammello","tee","atelier_beige"],
  "An afternoon in a Milan apartment with herringbone parquet: he sits sideways in a vintage leather armchair reading a book, barefoot, legs over the armrest. Three-quarter. Shot on a 35mm lens at f/2 on Kodak Portra 400, warm window light.",
  "The V-neck cardigan buttoned over the white T-shirt; beige trousers; barefoot.","barefoot","c"),
 ("P31","P","Café met regen",["verona_navy","tee","atelier_beige"],
  "A rainy morning in a lakeside café in Varenna: he sits by the window with a cappuccino, looking out at the rain on the lake. Waist-up, seated. Shot on a 50mm lens at f/2 on Kodak Portra 400, soft grey light.",
  "The navy zip jacket zipped halfway up over the white T-shirt, so its pointed shirt collar and the silver zip are clearly visible; it has a zip, not buttons, and a deep ribbed hem; beige trousers.","none","d"),
 ("P32","P","Mok op de steiger",["fullzip_taupe","tee","puro_taupe","loafer_tabacco"],
  "A cold misty morning on a wooden lake jetty: he stands with the hood up, holding a steaming mug in both hands, looking at the fog on the water. Three-quarter length. Shot on a 50mm lens at f/2.8 on Kodak Portra 160.",
  "The chunky hooded cardigan zipped up, hood up; taupe joggers; cognac loafers.","loafers","f"),
 ("P33","P","Lachen aan de kade",["voyage_set","loafer_notte"],
  "Morning at the lakefront of Varenna: he leans against the iron railing, laughing with his head tilted back. Full length. Shot on a 35mm lens at f/2.8 on Kodak Portra 400, bright morning light.",
  "The navy gilet zipped halfway over the navy T-shirt; navy trousers; navy loafers.","loafers","b"),
 ("P34","P","Vroeg op de fiets",["oliva_set","loafer_moro"],
  "Early morning on a cobbled street in Brera: he rolls an old plain black bicycle with no badges along the street, walking beside it. Full length. Shot on a 35mm lens at f/2.8 on Kodak Portra 400, low sun.",
  "The gilet zipped up over the white long-sleeve T-shirt; olive trousers; dark brown loafers.","loafers","i"),
 ("P35","P","Zwembad bij de villa",["supremo_set","lido_notte"],
  "Late afternoon by the stone-edged pool of a villa above Lake Como: he sits on a teak lounger, barefoot, one knee up, looking at the lake. Full length, seated. Shot on a 50mm lens at f/2.8 on Kodak Portra 160, warm low sun.",
  "The SLEEVELESS beige knit gilet zipped up over the dark navy polo, so both arms are navy from shoulder to wrist and the beige ribbed armholes are clearly visible; beige trousers; barefoot.","barefoot","h"),
 # ---------- O: product op locatie ----------
 ("O01","O","Set op de boot",["sabbia_set"],
  "Still life on an old varnished mahogany runabout boat on Lake Como: the set lies folded on the cream leather seat, sunlight on the varnished wood and the lake glittering behind. The boat has no badges or lettering. Shot on a 50mm lens at f/2.8 on Kodak Portra 160.",
  "The gilet folded on top, the white T-shirt and the trousers folded beneath.","",""),
 ("O02","O","Op de balustrade",["tabacco_set"],
  "Still life on a stone balustrade overlooking Lake Como at golden hour: the set lies folded on the stone, the pair of loafers beside it. Shot on a 50mm lens at f/2.8 on Kodak Portra 400.",
  "The hooded jacket folded on top, the cream polo and trousers beneath, the loafers beside.","",""),
 ("O03","O","Cafestoel met cappuccino",["excl_brown"],
  "Still life at an outdoor café in Milan: the jacket hangs over the back of a bistro chair beside a small marble table with a cappuccino, morning sun on the cobblestones. Shot on a 50mm lens at f/2 on Kodak Portra 400.",
  "The jacket over the chair back, the trousers folded on the seat.","",""),
 ("O04","O","Bed met espresso",["lounge_navy"],
  "Still life on an unmade white linen bed in a Milan hotel room: the set lies folded beside a small tray with an espresso, morning light through sheer curtains. Shot on a 50mm lens at f/2.8 on Kodak Portra 160.",
  "The zip jacket and the joggers folded neatly on the bed.","",""),
 ("O05","O","Bellagio in drie kleuren",["bellagio_burgundy","bellagio_green","bellagio_ivory"],
  "Still life on a walnut table by a window: three cardigans lie folded in a neat stack, warm afternoon light. Shot on a 50mm lens at f/2.8 on Kodak Portra 400.",
  "Three folded cardigans stacked: burgundy at the bottom, forest green in the middle, ivory on top, collars facing the camera.","",""),
 ("O06","O","Flatlay op terrazzo",["camicia_sabbia","atelier_beige","loafer_sabbia"],
  "Overhead flat lay on a terrazzo floor in a Milan apartment, morning sun: the outfit laid out with a small espresso cup beside it. Shot from directly above on a 35mm lens, Kodak Portra 400.",
  "The overshirt laid flat and buttoned, the trousers below it, the loafers at the bottom.","",""),
 ("O07","O","Blazer aan de cafestoel",["torino_oliva"],
  "Still life at an outdoor café in Brera: the blazer hangs on the back of a wicker bistro chair, a cappuccino on the round marble table, ochre walls soft behind. Shot on a 50mm lens at f/2 on Kodak Portra 400.",
  "The blazer hanging on the chair back, front facing the camera.","",""),
 ("O08","O","Flatlay op zwart marmer",["reverso_nero","loafer_nero"],
  "Overhead flat lay on black marble: the set laid out with an espresso cup, moody side light. Shot from directly above on a 50mm lens, Kodak Portra 400.",
  "The gilet laid flat and zipped, the white T-shirt and trousers folded beside it, the loafers below.","",""),
 ("O09","O","Ligstoel bij zonsondergang",["lusso_beige"],
  "Still life on a terrace on Lake Como at sunset: the set draped over a striped canvas deckchair, the lake glowing behind. Shot on a 50mm lens at f/2.8 on Kodak Portra 400.",
  "The jacket draped over the deckchair, the trousers folded on the seat.","",""),
 ("O10","O","Aan het luik",["notte_set"],
  "Still life at a tall Milan window with green wooden shutters: the gilet and polo hang on one wooden hanger hooked on the open shutter, the loafers on the terracotta floor below. Morning sun. Shot on a 50mm lens at f/2.8 on Kodak Portra 400.",
  "The gilet over the polo on the hanger, the trousers folded over the hanger bar, the loafers on the floor.","",""),
 ("O11","O","Ligbed op de steiger",["voyage_set"],
  "Still life on a teak sun lounger on the jetty of a lake villa, Lake Como behind: the set lies folded on the cushion. Shot on a 50mm lens at f/2.8 on Kodak Portra 160.",
  "The navy gilet folded on top, the navy T-shirt and trousers beneath.","",""),
 ("O12","O","Fluweelstoel met meerzicht",["supremo_set"],
  "Still life in a hotel suite on Lake Como: the set lies folded on a velvet armchair by a tall window with the lake behind. Shot on a 50mm lens at f/2.8 on Kodak Portra 400.",
  "The sleeveless gilet folded on top, the polo and trousers beneath, the loafers on the floor.","",""),
 ("O13","O","Kapstok in de gang",["oliva_set"],
  "Still life in a Milan apartment hallway: the set hangs on a wooden valet stand, morning light on the herringbone parquet. Shot on a 50mm lens at f/2.8 on Kodak Portra 400.",
  "The gilet zipped over the long-sleeve T-shirt on the hanger, the trousers over the bar.","",""),
 ("O14","O","Treinbank",["imperial_green"],
  "Still life on the velvet seat of an old Italian train compartment by the window, the lake landscape passing in a blur. Shot on a 50mm lens at f/2 on Kodak Portra 400.",
  "The jacket folded on the seat, the trousers folded beneath.","",""),
 ("O15","O","Deur in het ochtendlicht",["champagne_set"],
  "Still life: the set hangs on a tall painted door in a Milan apartment, long morning shadows. Shot on a 50mm lens at f/2.8 on Kodak Portra 160.",
  "The hooded jacket on a wooden hanger over the door, the trousers folded over the hanger.","",""),
 ("O16","O","Chaletbank bij het vuur",["mocha_set"],
  "Still life on a wooden bench in a mountain chalet, firelight glowing. Shot on a 35mm lens at f/2 on Kodak Vision3 500T.",
  "The zip jacket and joggers folded on the bench, the sleeve stripes visible.","",""),
 ("O17","O","Vensterbank met regen",["morbido_grey"],
  "Still life on a deep window seat with rain running down the glass and the grey lake outside. Shot on a 50mm lens at f/2 on Kodak Portra 400.",
  "The hooded cardigan and trousers folded on the cushion.","",""),
 ("O18","O","Polo's op de muur in Varenna",["lido_notte","lido_avena"],
  "Still life on a stone wall in Varenna with Lake Como behind, soft afternoon light. Shot on a 50mm lens at f/2.8 on Kodak Portra 400.",
  "The navy polo and the oatmeal polo folded side by side, collars and plackets up.","",""),
 ("O19","O","Polo's op het bootdek",["sorrento_ottanio","sorrento_beige"],
  "Still life on the varnished teak deck of an old wooden boat, rope coiled beside, sun and water reflections. Shot on a 50mm lens at f/2.8 on Kodak Portra 400.",
  "The teal polo and the camel polo folded side by side, tipped collars up.","",""),
 ("O20","O","Kast met vesten",["vela_celeste","vela_cammello"],
  "Still life inside an open antique wooden armoire in a Milan apartment, soft light. Shot on a 50mm lens at f/2.8 on Kodak Portra 400.",
  "The pale blue and the camel cardigans folded on a shelf, buttons visible.","",""),
 ("O21","L","Stoel op het parket",["verona_navy"],
  "Still life in a Milan apartment with herringbone parquet: the zip cardigan hangs over the back of a bentwood chair, afternoon light. Shot on a 50mm lens at f/2.8 on Kodak Portra 400.",
  "The zip jacket over the chair back, front facing the camera, the collar open so the label inside the back neck shows.","",""),
 ("O22","O","Rieten stoel op het terras",["pieno_sabbia","loafer_sabbia"],
  "Still life on a terrace on Lake Como: the knit gilet lies on a rattan chair, the loafers on the stone floor beside it. Shot on a 50mm lens at f/2.8 on Kodak Portra 160.",
  "The gilet laid flat on the seat, front facing up, so the ribbed stand collar, the full silver zip and both welt pockets are clearly visible; it is clearly a sleeveless gilet; the loafers on the stone floor beside the chair.","",""),
 ("O23","O","Achterbank bij nacht",["midnight"],
  "Still life at night on the leather back seat of a classic car without any badges, streetlights glowing through the window. Shot on a 50mm lens at f/1.8 on Kodak Vision3 500T.",
  "The hooded jacket and gilet folded on the seat, the white T-shirt and trousers beneath.","",""),
 ("O24","O","Betonnen bank",["onyx","loafer_nero"],
  "Still life on a concrete bench in a modern Milan courtyard with clean lines, late afternoon light. Shot on a 35mm lens at f/2.8 on Kodak Portra 400.",
  "The jacket and hooded top folded, the joggers and white T-shirt beside, the loafers on the ground.","",""),
 ("O25","O","Kapstok bij sneeuw",["twotone_navy"],
  "Still life in a chalet in Cortina: the jacket hangs on a wooden coat stand beside a window with falling snow. Shot on a 50mm lens at f/2 on Kodak Portra 400.",
  "The jacket on a hanger, the joggers folded over the hanger bar, the stripes visible.","",""),
 # ---------- L: necklabel met logo ----------
 ("L01","L","Label naast de espresso",["imperial_brown"],
  "Close-up still life on a white marble table: the jacket lies folded with its collar opened towards the camera, a small espresso cup beside it, morning side light. Shot on a 100mm macro lens at f/4 on Kodak Portra 400.",
  "The collar turned so the inside of the back neck faces the camera.","",""),
 ("L02","L","Capuchon aan de haak",["excl_navy"],
  "Close-up: the hooded jacket hangs on a brass wall hook, the hood opening towards the camera. Soft window light. Shot on a 100mm macro lens at f/4 on Kodak Portra 400.",
  "Hanging on the hook so the inside of the hood and back neck faces the camera.","",""),
 ("L03","L","Gevouwen op linnen",["lounge_gray"],
  "Close-up still life on white bed linen: the zip jacket lies folded with the collar turned up, morning light. Shot on a 100mm macro lens at f/4 on Kodak Portra 160.",
  "Folded with the inside of the back neck facing the camera.","",""),
 ("L04","L","Kraag bij het meer",["bellagio_ivory"],
  "Close-up still life on a wooden table by a window, Lake Como soft and blue behind: the cardigan lies folded with the collar open. Shot on a 100mm macro lens at f/4 on Kodak Portra 160.",
  "The collar opened so the inside of the back neck faces the camera.","",""),
 ("L05","L","Op de hanger",["camicia_oliva"],
  "Close-up: the overshirt hangs on a wooden hanger against a plaster wall, seen from slightly above so the inside of the collar shows. Shot on a 100mm macro lens at f/4 on Kodak Portra 400.",
  "Hanging, collar open, inside of the back neck visible.","",""),
 ("L06","L","Polo bij het ontbijt",["lido_notte"],
  "Close-up flat lay on linen: the polo lies folded with its collar open, beside the edge of a cappuccino cup and a cornetto. Shot from above on a 100mm macro lens, Kodak Portra 400.",
  "Folded, collar open, inside of the back neck facing the camera.","",""),
 ("L07","L","Blazer van binnen",["torino_perla"],
  "Close-up: the knitted blazer hangs on a wooden hanger in a Milan apartment, seen from the back of the neck down into the collar. Shot on a 100mm macro lens at f/4 on Kodak Portra 400.",
  "The back neck of the blazer facing the camera, inside visible.","",""),
 ("L08","L","Gilet op het bootdek",["reverso_nero"],
  "Close-up on the varnished deck of an old wooden boat: the gilet lies folded with its stand collar open, water reflections dancing. Shot on a 100mm macro lens at f/4 on Kodak Portra 400.",
  "The collar open, the white reverse and the label inside the back neck visible.","",""),
 ("L09","L","Op zwart marmer",["onyx"],
  "Close-up on black marble: the black zip jacket lies folded with its collar open, moody side light. Shot on a 100mm macro lens at f/4 on Kodak Portra 400.",
  "Collar open, inside of the back neck facing the camera.","",""),
 ("L10","L","Capuchon met stoom",["morbido_beige"],
  "Close-up: the hooded knit jacket lies folded on a wooden table beside a steaming cup of coffee, the hood folded back. Shot on a 100mm macro lens at f/4 on Kodak Portra 160.",
  "The jacket lies with its back neck at the top of the frame and the hood folded open away from the camera, so the label inside the back neck is upright and reads left to right.","",""),
 ("L11","L","Strepen en label",["twotone_navy"],
  "Close-up still life: the jacket lies folded on cream linen, collar open, one striped sleeve laid alongside. Shot on a 100mm macro lens at f/4 on Kodak Portra 400.",
  "Collar open showing the inside back neck, a sleeve stripe in frame.","",""),
 ("L12","L","Kraag open in de hand",["imperial_green"],
  "Close-up in a sunlit hotel room: a man's hands hold the jacket up by the collar and open it towards the camera, showing the inside of the back neck. Only the hands and wrists are visible. Shot on a 100mm macro lens at f/4 on Kodak Portra 400.",
  "Held up by the collar, the inside of the back neck facing the camera.","hands",""),
 ("L13","L","Handen vouwen",["lusso_beige"],
  "Close-up of a man's bare hands smoothing the folded jacket on a wooden table, seen from above. Only his bare hands and wrists enter the frame from the bottom edge; no sleeves and no other clothing are in view. Shot on a 100mm macro lens at f/4 on Kodak Portra 400.",
  "Folded, the back neck at the top of the frame, so the label inside the back neck is upright and reads left to right.","hands",""),
 ("L14","L","Polo aan de haak",["sorrento_ottanio"],
  "Close-up: the polo hangs on a wooden hanger against a white plaster wall with the sea light of Lake Como, seen from slightly above into the collar. Shot on a 100mm macro lens at f/4 on Kodak Portra 400.",
  "Hanging, collar open, inside of the back neck visible.","",""),
 ("L15","L","Capuchon over de stoel",["midnight"],
  "Close-up: the black hooded jacket hangs over the back of a café chair, the hood open towards the camera, a terrace soft behind. Shot on a 100mm macro lens at f/4 on Kodak Portra 400.",
  "The hood open, the label inside the back neck upright and visible. The jacket and its hood are black inside and out, with a black lining; the only light element is the ivory label.","",""),
 # ---------- A: Italiaanse sfeer ----------
 ("A01","A","Varenna bij dageraad",[],"Dawn at the small stone harbour of Varenna on Lake Como: an old varnished mahogany runabout boat with cream leather seats is moored at the steps, mist on the water, pastel houses behind. Shot on a 50mm lens at f/2.8 on Kodak Portra 160.","","",""),
 ("A02","A","Twee houten boten",[],"Golden hour on Lake Como, seen from above: two classic varnished wooden runabouts moored side by side at a wooden jetty, the water clear green. Shot on a 35mm lens, Kodak Portra 400.","","",""),
 ("A03","A","Kielzog op het meer",[],"Aerial view of an old wooden motorboat cutting across glassy Lake Como, a long white wake behind it, mountains and villas on the shore. Shot from a drone, soft late light, film colour.","","",""),
 ("A04","A","Villa met cipressen",[],"Morning at a lakeside villa on Lake Como: tall cypresses, a stone balustrade with urns and a terrace stepping down to the water. Shot on a 35mm lens at f/4 on Kodak Portra 160.","","",""),
 ("A05","A","Trapje in Bellagio",[],"An empty stepped lane in Bellagio with flower pots, green shutters and warm stone, early morning sun at the top of the steps. Shot on a 35mm lens at f/2.8 on Kodak Portra 400.","","",""),
 ("A06","A","Pier bij zonsondergang",[],"Sunset at an old wooden ferry pier on Lake Como, wooden posts in the water, the sky orange and violet. Shot on a 50mm lens at f/4 on Kodak Portra 400.","","",""),
 ("A07","A","Espresso aan de bar",[],"Close still life of a small espresso in a thick white cup and saucer on the marble counter of an old Milan bar, a brass rail and a glass of water beside it, morning light. Shot on a 50mm lens at f/2 on Kodak Portra 400.","","",""),
 ("A08","A","Cappuccino en cornetto",[],"A cappuccino and a cornetto on a small round marble café table outdoors in Milan, cobblestones and morning sun. Shot on a 50mm lens at f/2 on Kodak Portra 400.","","",""),
 ("A09","A","Hendel van de espressomachine",[],"Close-up of an old chrome lever espresso machine pouring espresso into a small white cup, steam and crema, warm bar light. No lettering on the machine. Shot on a 100mm lens at f/2.8 on Kodak Portra 400.","","",""),
 ("A10","A","Moka in de keuken",[],"A moka pot steaming on a gas stove in an old Milan apartment kitchen with patterned tiles, morning sun. Shot on a 50mm lens at f/2.8 on Kodak Portra 400.","","",""),
 ("A11","A","Leeg terras in de ochtend",[],"An empty café terrace on a Milan piazza early in the morning, folding chairs and small marble tables, wet cobblestones shining. Shot on a 35mm lens at f/2.8 on Kodak Portra 400.","","",""),
 ("A12","A","Spritz op de muur",[],"Two orange spritz drinks in plain glasses on a stone wall at sunset, Lake Como glowing behind. Shot on a 50mm lens at f/2 on Kodak Portra 400.","","",""),
 ("A13","A","Duomo in de mist",[],"The spires of the Duomo di Milano rising out of morning fog, seen from a rooftop. Shot on an 85mm lens on Kodak Portra 400, soft and pale.","","",""),
 ("A14","A","Koepel van glas",[],"Looking straight up into the glass and iron dome of the Galleria in Milan, early morning, empty. Shot on a 24mm lens on Kodak Portra 400.","","",""),
 ("A15","A","Oranje tram",[],"An old orange Milan tram rolling over cobblestones in Brera, slight motion blur, morning light. No numbers or lettering visible. Shot on a 35mm lens at f/4 on Kodak Portra 400.","","",""),
 ("A16","A","Navigli op het blauwe uur",[],"The Naviglio Grande at blue hour, the warm lights of the old houses reflected in the still water, nobody about. Shot on a 35mm lens at f/2 on Kodak Vision3 500T.","","",""),
 ("A17","A","Lege leunstoel",[],"The interior of an elegant Milan apartment: tall windows with sheer curtains, herringbone parquet, an empty vintage leather armchair in the morning light. Shot on a 35mm lens at f/2.8 on Kodak Portra 160.","","",""),
 ("A18","A","Binnenplaats met klimop",[],"The ivy-covered courtyard of an old Milanese palazzo with stone arches and a small fountain, soft shade. Shot on a 35mm lens at f/4 on Kodak Portra 400.","","",""),
 ("A19","A","Bosco Verticale bij schemer",[],"The Bosco Verticale towers in Milan at dusk, greenery on every balcony, the sky soft violet. Shot on a 50mm lens on Kodak Portra 400.","","",""),
 ("A20","A","Regen op de kasseien",[],"A rainy evening in a Milan street, the cobblestones reflecting the warm light of a café window, no people. Shot on a 35mm lens at f/2 on Kodak Vision3 500T.","","",""),
 ("A21","A","Ontbijt voor één",[],"A breakfast table set for one on a terrace above Lake Como: cappuccino, a cornetto, fresh orange juice and a white cloth, the lake and mountains behind. Shot on a 50mm lens at f/2.8 on Kodak Portra 160.","","",""),
 ("A22","A","Schuim en lepeltje",[],"Close-up of the foam of a cappuccino in a white cup on a marble table with a small silver spoon and a sugar cube. Shot on a 100mm lens at f/2.8 on Kodak Portra 400.","","",""),
 ("A23","A","Botenhuis",[],"Inside an old wooden boathouse on Lake Como: varnished classic boats in their slips, light reflecting off the water onto the beams. Shot on a 35mm lens at f/2.8 on Kodak Portra 400.","","",""),
 ("A24","A","Cipressenweg",[],"A winding lakeside road lined with cypresses at dusk, a classic convertible car without any badges parked by the wall, Lake Como beyond. Shot on a 50mm lens at f/2.8 on Kodak Portra 400.","","",""),
 ("A25","A","Pasticceria",[],"The counter of an old Milan pasticceria with pastries under glass domes and a marble top, warm morning light. No labels or lettering. Shot on a 50mm lens at f/2 on Kodak Portra 400.","","",""),
]
S = [s for s in S]
# kleine reparatie: L13 tekst
S = [(s[0],s[1],s[2],s[3],s[4].replace(", sleeves of the jacket's matching... no other clothing in view","; no other clothing is in view"),s[5],s[6],s[7]) for s in S]

def _spec(rk):
    t = SPEC[rk].replace(" Smooth matte fabric, no labels.", " Smooth matte fabric.").replace(" No labels.", "")
    return t

def lines_for(refs, medias):
    out = []
    total = sum(len(R[rk]) for rk in refs)
    for rk in refs:
        nums = []
        files = R[rk] if total <= 6 else R[rk][:max(1, 6 // len(refs))]
        for f in files:
            medias.append({"value": MEDIA[B + f], "role": "image_references"}); nums.append(f"#{len(medias)}")
        out.append(f"- {_spec(rk)} (reference image{'s' if len(nums) > 1 else ''} {', '.join(nums)})")
    return out

def build(s):
    sid, cat, title, refs, scene, worn, feet, man = s
    medias = []
    if cat == "A":
        p = "\n\n".join([scene, LOOK, "There are no people and no clothing in the picture. No logos, signs, labels, brand names or readable text anywhere. Photographic, not CGI: real optics, film grain."])
        return {"id": sid, "title": title, "params": {"model": "nano_banana_pro", "aspect_ratio": "4:5", "resolution": "2k", "prompt": p, "medias": medias}}
    lines = lines_for(refs, medias)
    parts = [scene, LOOK]
    person = cat == "P" or (cat == "L" and feet == "person")
    if person:
        parts.append(f"The man: {MEN[man]}; he does not resemble any actor or public figure. {REAL}")
        parts.append("He wears only these ModernoMilano pieces and nothing else:\n" + "\n".join(lines))
        parts.append(f"How they are worn: {worn}")
    else:
        parts.append("The only clothing in the picture is these ModernoMilano pieces:\n" + "\n".join(lines))
        parts.append(f"How they are arranged: {worn}")
    parts.append(REPRO)
    if cat == "L":
        n = len(medias)
        for v in LABEL_IDS: medias.append({"value": v, "role": "image_references"})
        parts.append(LABEL.format(a=n + 1, b=n + 2))
    if person:
        foot = "His feet are not in the picture." if cat == "L" else FEET[feet]
        parts.append(f"His hands and wrists are bare: no ring, no watch, no bracelet, no glasses, no bag. {foot} He is the only person in the picture.")
    elif feet == "hands":
        parts.append("Only a man's bare hands and forearms are visible: no ring, no watch, no bracelet; no other clothing in view.")
    else:
        parts.append("There are no people in the picture.")
    parts.append(LABELTEXT if cat == "L" else NOTEXT)
    return {"id": sid, "title": title, "params": {"model": "nano_banana_pro", "aspect_ratio": "4:5", "resolution": "2k", "prompt": "\n\n".join(parts), "medias": medias}}

ALL = {s[0]: s for s in S}
if __name__ == "__main__":
    ids = sys.argv[1:] or list(ALL)
    out = [build(ALL[i]) for i in ids]
    json.dump(out, open(os.path.join(HERE, "built100.json"), "w"), indent=1)
    print(json.dumps([{"index": k + 1, "params": o["params"]} for k, o in enumerate(out)], ensure_ascii=False))
