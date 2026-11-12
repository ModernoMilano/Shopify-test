"""Shotlijst voor de video bij I'm Not Giving It Back, lange versie, kandidaat B (take N3, 90,04 s).
Gebruik: python3 gib_shots.py list
         python3 gib_shots.py keyframes [N01 N02 ...] -> keyframe-verzoeken (gpt_image_2_6) als JSON, in groepjes van 4
         python3 gib_shots.py clips kf_ids.json [N01 ...] -> Kling-verzoeken (start_image = keyframe-job), in groepjes van 12
         python3 gib_shots.py plan  -> montageplan (shots met tijden) als JSON

Vaste afspraken (11 nov, na de controle van de eerste keyframes):
- Hij is overal dezelfde man: het blad HIMN (donker golvend haar, gladgeschoren). De oude clips van video 2
  tonen de verteller met lichter warrig haar en stoppels; die worden hier niet gebruikt (alleen K39, waarin
  alleen zijn mouw te zien is).
- Beide knits zijn hetzelfde echte product, de Milano Cashmere Bellagio (full-zip, geribd, opstaande kraag):
  knit 1 in donkerblauw (referentie = de productfoto van de Bellagio Blue), knit 2 in taupe (blad TCAR).
- Zij draagt onder de knit steeds een donkerbruine broek; bij de wijnbar een crème trenchcoat en crème blouse.
- Hij: wit T-shirt in de scènes met knit 1, crème T-shirt vanaf de wijnbar (onder knit 2), navy broek.
- Wijnbar, tram en haar voordeur zijn dezelfde avond: zij in de taupe knit, hij in het crème T-shirt.
Referenties (Higgsfield media-ids): HER = karakterblad van haar, HIMN = hij, TCAR = taupe Bellagio,
NAVY = productfoto Bellagio Blue (modernomilano.com), DAVE = huisgenoot, BAR = keyframe van K39 (de wijnbar)."""
import json, sys
R = dict(HER='915ac841-6d18-449a-9dd7-fa98badf8ea3', HIMN='cc30e31f-f254-4602-9666-733e01dd5b96',
         TCAR='b0747331-a3c4-4f9f-bc58-d82ef671648c', NAVY='911985a1-5d98-467e-b067-3263009f66cd',
         DAVE='c613f1e6-327b-4d41-a628-ddab724d07c3', BAR='afafaccc-f021-4d8f-96ea-8b347d2ba192',
         KF25='c5d7ee59-1e01-4b4d-a758-d709c21a50d5',   # KF25 = het eerste keyframe van N25, als voorbeeld voor het verre stel in N26
         TAUPE='79d9f2ac-4e24-4cf9-ba98-59cb79d795c4',  # productfoto Bellagio Taupe (modernomilano.com); vervangt het getekende blad TCAR, dat zakken had
         KF22='fab5a6ce-ae49-40db-80ea-65ab38832a41', KF30='b5ef1305-a969-403c-8244-54bbcb134d1e',
         KF27='5b406bdd-0139-4724-b952-3695c51e7a94',
         KF07='a96d25f0-2e4f-4412-8e53-af942d5c8b9c', KF18='d19924c8-3d0a-435a-ad6e-6bcb71c7fc5d',
         KF05='66a6560f-4d83-4f76-8dae-24aa53a4143d', KF11='17f9a0cb-24eb-4713-a53e-49e5af6a6a46')   # eerdere startbeelden van N07, N18, N05 en N11 (met een ademsliert), als voorbeeld voor de versie zonder adem                                       # keyframe van N27 (zijn slaapkamer) als voorbeeld voor N09 en N10; invullen na het opnieuw maken van N27                              # keyframes van N22 (de voordeur) en N30 (de wijnbar) als voorbeeld voor de shots in dezelfde scene
STYLE = "3D animated feature-film still in the style of a modern Pixar movie: stylized characters with slightly oversized heads, large expressive glossy eyes, sculpted hair, smooth subsurface skin, cinematic shallow depth of field. "
END = " Everything is in sharp focus where it matters: no motion blur, no motion lines, no speed lines. Vertical 9:16. No text, no logos, no signs, no readable writing anywhere."
MPRE = "3D animated feature-film look. "
MEND = " Subtle natural performance only; everyone keeps exactly their face, hair, clothes and colours from the start frame; whenever eyes open they are brown. No text, no logos. One continuous take."
def her(n): return f"the young woman from reference image {n} (long wavy brown hair)"
def him(n, top="a plain white T-shirt"): return f"the young man from reference image {n} (exactly the same face, brown hair neatly combed, clean-shaven), in only {top} and navy trousers"
CREAM = 'a plain cream T-shirt'
def herL(n): return f"the young woman from reference image {n} (long loose wavy brown hair)"
def him2(n, top=CREAM):   # na de controle van 11 nov: haar en voorhoofd uitdrukkelijk benoemd (N22 en N24 dreven af)
    return (f"the young man from reference image {n} (exactly the same face and head shape; his hair is dark brown, short at the nape and neatly combed back "
            f"in a full wave exactly as in reference image {n}; clean-shaven, slim; the skin of his forehead is an even warm tone), in only {top} and navy trousers")
def knit1(n): return f"exactly the full-zip ribbed cashmere knit from reference image {n} (ribbed stand-up collar, full-length zip, ribbed cuffs and hem), in deep navy blue"
def navy(n): return knit1(n) + ", far too big for her"
def taupe(n): return f"exactly the full-zip ribbed cashmere knit from reference image {n} (taupe, ribbed stand-up collar, full-length zip, ribbed cuffs and hem, no pockets), far too big for her"
def himt(a, b): return (f"the young man from reference image {a} (exactly the same face, brown hair neatly combed, clean-shaven), wearing exactly the taupe full-zip ribbed "
                        f"cashmere knit from reference image {b} (ribbed stand-up collar, full-length zip, no pockets), fitting him well, zipped over a cream T-shirt, with navy trousers")
LIVING = "A cosy Milan living room at night, warm lamp light, a sofa and a window with city lights behind. "
CANAL = "A cold clear night at the Navigli canal in Milan, dry cobblestones, no snow, street lamps reflected in the dark water, their breath visible in the cold air. "
DOOR = "Night on a quiet Milan street, wet cobblestones after rain, no snow, a tall dark-green wooden front door with a brass lever handle, one warm wall lamp. "
SAMEDOOR = "The same dark-green front door, doorway and street as in reference image %d. "
S = []
def add(k, refs, dur, prompt, motion): S.append(dict(k=k, refs=refs, dur=dur, prompt=STYLE + prompt + END, motion=MPRE + motion + MEND))
def cap(s): return s[0].upper() + s[1:]
NOBREATH = " The only change from reference image %d: the night air is completely clear, with no breath cloud, no steam, no smoke and no mist anywhere."

# --- 0:00 haar refrein, thuis in zijn donkerblauwe knit
add('N01', ['HER','NAVY'], 3, LIVING + f"Medium close-up of {her(1)}, wearing {navy(2)}, zipped up, with dark brown trousers, the sleeves covering her hands; she hugs it tight around herself with both arms, chin tucked into the collar, eyebrows raised, a teasing stubborn smile, looking straight at the camera.",
    "Static camera. She hugs the knit tighter around herself and slowly shakes her head no with a teasing smile; her hair sways slightly.")
add('N02', ['HER','NAVY'], 3, LIVING + f"Close-up of {her(1)} in {navy(2)}, zipped up, with dark brown trousers: with one sleeve-covered hand she presses the soft ribbed collar against her cheek, eyes closed, a blissful little smile.",
    "Static camera. She slowly rubs her cheek against the soft collar with a blissful smile and gives one small contented nod. Her eyes stay closed the whole time.")
add('N03', ['HER','NAVY'], 3, LIVING + f"Three-quarter shot of {her(1)} standing fully dressed in {navy(2)}, zipped up, with dark brown trousers: she lifts both forearms so the far-too-long sleeves flop over her hands, the ribbed stand-up collar high under her chin, a delighted grin. Family-friendly.",
    "Static camera. She gives her raised forearms two small shakes so the empty sleeve ends flop, then lowers her chin into the high collar with a grin. She stays in place; her hands never come out of the sleeves; the sleeves stay whole and her hair keeps its shape and length.")
add('N04', ['HIMN','HER','NAVY'], 3, LIVING + f"Two-shot: {him(1)} holds out one open hand, palm up, asking for his knit back with a hopeful grin; facing him {her(2)} wears {navy(3)}, zipped up, with dark brown trousers, her arms wrapped tight around herself, leaning away from his hand with a cheeky grin.",
    "Static camera. He keeps his open hand held out, palm up, and raises his eyebrows with a hopeful grin; she slowly shakes her head no with a cheeky grin and hugs the knit a little tighter. Both stay where they are and keep facing each other; their heads keep their shape and nothing moves fast.")
# --- 0:10 de gracht: hij geeft zijn knit
add('N05', ['HIMN','HER','NAVY','KF05'], 3, f"Exactly the same scene, framing, poses, faces, clothes and light as reference image 4: a cold clear night at the Navigli canal in Milan, dry cobblestones, no snow, street lamps reflected in the dark water. Two-shot on the towpath: {him(1)} is draping {knit1(3)} around the shoulders of {her(2)}, who wears a thin cream blouse and dark brown trousers, hugs herself against the cold and looks up at him, surprised and touched." + NOBREATH % 4,
    "Static camera. He holds the knit on her shoulders with both hands and smiles down at her; she keeps looking up at him, blinks once slowly, and her surprised look softens into a small smile. Nobody turns their head; her hair keeps its shape. The front panels of the knit stay plain and smooth, exactly as in the start frame. The night air stays completely clear. Nothing moves fast.")
add('N06', ['HIMN','HER','NAVY'], 3, f"A cold clear night at the Navigli canal in Milan, dry cobblestones, no snow, street lamps reflected in the dark water, a clean dark sky with no smoke, steam or breath clouds. Medium two-shot walking along the towpath toward the camera: {her(2)} is snug in {navy(3)}, zipped up, with dark brown trousers, her hands hidden in the sleeves, smiling to herself; beside her {him(1)} (slim) walks with his arms wrapped around himself, shoulders hunched, shivering with a brave grin.",
    "Slow tracking shot backwards. They walk slowly toward the camera along the canal; he rubs his arms once and shivers with a grin; she smiles to herself, her hands hidden in the sleeves.")
# N06: de clip van deze prompt (4e2afbf3) wordt gebruikt tot 1,83 s, vertraagd (N06s): daarna breekt zijn gezicht bij het rillen.
# Twee rustiger pogingen vielen af: in 2baca241 steekt zij haar handen in zakken die de knit niet heeft, in 946f8220 wordt zijn gezicht smaller zodra hij opzij kijkt.
# N07 en N18: het startbeeld bevatte een ademsliert ("breath visible in the cold") en Kling maakte daar een wolk zo groot als een hoofd van,
# ook als de bewegingsprompt "no breath cloud" zei. Daarom is het startbeeld zelf opnieuw gemaakt met het oude beeld als voorbeeld en alleen de lucht schoon.
add('N07', ['HER','NAVY','KF07'], 3, f"Exactly the same scene, framing, pose, face and light as reference image 3: a cold clear night at the Navigli canal in Milan, street lamps reflected in the dark water. Close-up of the young woman from reference image 1 (long wavy brown hair, brown eyes) pulling the zip of {navy(2)}, all the way up to the top of the ribbed stand-up collar under her chin, the sleeves over her hands, warm lamp light on her face, a big grin. The only change from reference image 3: the night air is completely clear, with a clean dark starry sky and no breath cloud, no steam, no smoke and no mist anywhere. If any trousers show at the bottom edge they are dark brown.",
    "Static camera. The zip is already closed right up to her chin and stays there the whole time. She snuggles her chin deeper into the high collar, closes her eyes for a moment with a cosy grin and gives a tiny happy wiggle of her shoulders, then opens her eyes again, grinning. Her sleeve-covered hands stay at the collar. The night air stays completely clear. Nothing moves fast.")
add('N08', ['HER','NAVY'], 3, f"Her cosy living room at night, lit by a warm lamp and the bluish glow of a television off-frame. {cap(her(1))} sits curled up on the sofa in {navy(2)}, zipped up, with dark brown trousers and thick wool socks, knees pulled up, holding a steaming mug of tea in both sleeve-covered hands, watching the screen with a cosy smile.",
    "Static camera. She keeps the mug exactly where it is and blows gently across the top of the tea; the steam drifts; then she looks back at the screen with a cosy smile. Her arms, the mug and her body stay still the whole time; the light does not change and the knit keeps its dark navy colour.")
# --- 0:20 zijn rap: hoodies, compliment, lege hanger, huisgenoot, nieuwe knit, wijnbar
add('N27', ['HIMN'], 3, f"His bedroom in daylight, grey curtains: an open walnut wardrobe with a top shelf holding a tall neat stack of identical plain grey hoodies, a rail with white and light-blue shirts on wooden hangers (no navy garments), and drawers with metal bar handles. {cap(him(1))}, stands beside it and points at the stack of hoodies with one thumb, eyebrows raised, a dry amused look at the camera. Medium shot.",
    "Static camera. He tips his thumb toward the untouched stack of grey hoodies twice and slowly shakes his head with a dry grin. His arm stays up.")
add('N09', ['HIMN','KF27'], 3, f"The same bedroom in daylight and the same open walnut wardrobe as in reference image 2 (the tall stack of grey hoodies on the top shelf, white and light-blue shirts on the rail, grey curtains). Medium shot from the hips up of the young man from reference image 1 (exactly the same face, brown hair neatly combed, clean-shaven) in a plain white T-shirt and navy trousers, standing in front of the wardrobe with one hand resting high on his chest, well inside the upper half of the frame, eyebrows raised, a surprised, flattered grin, as if he has just been paid a compliment.",
    "Static camera. He keeps his hand flat on his chest and his head still; a slow bashful smile grows and he gives one slow blink. No head turn, no patting, no shrug; he keeps looking where he looks in the start frame and his face keeps its shape.")
add('N10', ['HIMN','KF27'], 3, f"The same bedroom in daylight and the same open walnut wardrobe as in reference image 2 (the tall stack of grey hoodies on the top shelf, white and light-blue shirts on the rail, drawers with metal bar handles, grey curtains). In the middle of the rail hangs one empty wooden hanger; there is no navy garment anywhere. {cap(him(1))}, stands beside the wardrobe looking at the empty hanger, one hand scratching the back of his head, an amused half-smile. Medium shot from the side.",
    "Static camera. He stands still beside the wardrobe and keeps looking at the empty hanger with an amused half-smile; his hand rests on the back of his head and his fingers scratch once, slowly. The empty hanger and all the clothes hang completely still, exactly as in the start frame. His head stays up and keeps its shape. Nothing moves fast.")
add('N28', ['HIMN','DAVE'], 3, f"Daylight inside the hallway of a shared Milan apartment, the front door closed in the background, a coat rack with a grey jacket. The flatmate from reference image 2 (stocky, curly dark hair, short beard, green T-shirt, grey sweatpants, socks) stands inside the hallway holding a plain brown cardboard parcel with no print in both hands, one eyebrow raised high, a knowing smirk; {him(1)} reaches for the parcel with both hands and a sheepish grin. Medium two-shot.",
    "Static camera. The flatmate holds the parcel out with both hands; his raised eyebrow lifts a little higher and his smirk widens, then he relaxes again. The other man keeps leaning forward with both hands at the parcel, grins sheepishly and gives one small nod, then returns to the same pose. Nobody turns their head and nobody straightens up; both keep their build and their loose T-shirts. The parcel keeps its size and stays plain, with no print. Nothing moves fast.")
add('N29', ['HIMN','TAUPE','BAR'], 3, f"The same candlelit Milan wine bar as in reference image 3 (red leather chairs, marble tables, glowing candle glasses, glasses of red wine, warm lamps). Medium shot of {himt(1, 2)}: he sits alone at a small marble table and smooths the ribbed collar of the knit with one hand, a proud little smile, looking off to the side.",
    "Static camera. He stays in the same three-quarter pose, looking off to the side; he runs two fingers slowly along the edge of the collar once and lets his hand rest on his chest, with a small proud smile and one blink. His body and head do not turn and he never looks at the camera; the zip does not move; the candle flickers.")
add('N30', ['HER','HIMN','TAUPE','BAR'], 3, f"The same candlelit Milan wine bar as in reference image 4 (red leather chairs, marble table, a glowing candle glass, glasses of red wine). Two-shot at the small marble table: {her(1)}, in the same cream trench coat and cream blouse as in reference image 4, lays her hand on the forearm of {himt(2, 3)}, feeling the soft ribbed sleeve, her eyes wide with delight; he looks down at her hand with a knowing, resigned little smile.",
    "Static camera. She strokes the ribbed sleeve with her fingertips, delighted; he looks from her hand to her face and smiles, already knowing what comes next.")
add('N31', ['HER','TAUPE','KF30'], 3, f"The same candlelit Milan wine bar, the same table and the same two people as in reference image 3. Close-up of {her(1)}, in the same cream trench coat and cream blouse, leaning over the small marble table: with her fingertips she strokes the forearm of the man beside her, of whom only the forearm is visible in the foreground, in the sleeve of exactly the taupe full-zip ribbed cashmere knit from reference image 2; her eyes are wide and her mouth is open in delight.",
    "Static camera. She keeps looking down at the sleeve the whole time and strokes it slowly once with her fingertips; her smile widens and she gives one soft blink. Her head stays tilted down and she never looks at the camera; the candle flickers.")
add('N11', ['HER','HIMN','TAUPE','KF11'], 3, f"Exactly the same scene, framing, poses, faces, clothes and light as reference image 4: night on a Milan street outside a warm little wine bar, candlelit windows behind, wet cobblestones. Two-shot: {her(1)}, in a cream blouse and dark brown trousers, has just put on {taupe(3)}, both arms in the sleeves; with one hand she holds the open front of the knit together at her chest, her other arm hangs at her side with her folded cream trench coat draped over the forearm; she has exactly two arms and two hands; a delighted grin. Beside her the young man from reference image 2 (exactly the same face and head shape; dark brown hair neatly combed back in a full wave; clean-shaven, slim), in only a plain cream T-shirt and navy trousers, watches with a resigned, amused smile." + NOBREATH % 4,
    "Static camera. She keeps holding the knit closed at her chest and keeps looking up at him with the same delighted smile; she gives one tiny happy shrug of her shoulders. Her eyes stay open and keep their shape; her face and hair stay exactly as in the start frame. He keeps looking at her with a resigned, amused smile and tilts his head slightly. The coat stays draped over her forearm. The night air stays completely clear. Nothing moves fast.")
# --- 0:42 haar refrein, knit nummer twee
add('N12', ['HER','TAUPE'], 3, f"Night on a Milan street with tram tracks and warm street lamps. Medium close-up of {her(1)} wearing {taupe(2)} over her cream blouse, zipped up, hugging it tight around herself with both arms, chin tucked into the collar, a teasing stubborn smile, looking at the camera.",
    "Static camera. She hugs the knit tighter and shakes her head no with a teasing smile.")
add('N13', ['HER','TAUPE'], 3, f"Night on a Milan street with warm street lamps. Close-up of {her(1)} in {taupe(2)} over her cream blouse, with dark brown trousers: she holds up two fingers in a V right next to her cheeky grin, one eyebrow raised.",
    "Static camera. She raises two fingers, wiggles them and raises one eyebrow with a cheeky grin.")
add('N14', ['HER','TAUPE'], 3, f"Night on a quiet Milan street with warm street lamps and plain stone house fronts with closed wooden shutters, no shops. Three-quarter shot of {her(1)} in {taupe(2)}, zipped up, with dark brown trousers: she holds both arms out so the cuffs hang far past her fingertips, the ribbed stand-up collar high under her chin, laughing.",
    "Static camera. She holds the too-long sleeves out and gives the empty cuffs one small shake, laughing gently. Her head stays almost still and she stays in place, facing the camera: no spinning, no bending forward, no head toss, nothing moves fast. Her hands stay hidden inside the sleeves and the sleeves stay whole.")
add('N15', ['HIMN','HER','TAUPE'], 3, f"Night at a Milan tram stop, an orange tram waiting with its doors open, wet cobblestones, warm street lamps, breath visible. Two-shot: {him2(1)} holds out one open hand, palm up, with a hopeful grin; {her(2)}, wearing {taupe(3)} with dark chocolate-brown trousers (not navy, not black) and brown loafers, steps backward onto the tram step, laughing and shaking her head.",
    "Static camera. She shakes her head, laughing, and wiggles her raised fingers in a little goodbye; he keeps his open hand out and grins. The tram stands still.")
# --- 0:52 zijn rap: tram, perron, T-shirt, haar deur
add('N16', ['HER','TAUPE'], 3, f"Night in Milan, an orange tram pulling away from a stop, wet cobblestones, street lamps. Seen from the empty platform, nobody in the foreground: at the lit tram window {her(1)} wears {taupe(2)} and waves with a sleeve-covered hand, both eyes open, a cheeky grin.",
    "Static camera. She waves her sleeve-covered hand from side to side, clearly waving goodbye, and grins; the tram rolls slowly forward.")
add('N17', ['HIMN'], 3, f"A tram stop in Milan at night, wet cobblestones, street lamps, an orange tram gliding away in the background. {cap(him(1, CREAM))}, stands alone on the platform, arms hugged against the cold, laughing at himself, his head still. Medium shot.",
    "Static camera. He watches the tram leave, hugs his arms, laughs and shakes his head; the tram glides away.")
add('N18', ['HIMN','KF18'], 3, "Exactly the same scene, framing, pose, face and light as reference image 2: night on a quiet Milan street with warm shop windows and street lamps, wet paving. The young man from reference image 1 (exactly the same face, brown hair neatly combed, clean-shaven), in only a plain cream T-shirt, navy trousers and navy loafers, walks toward the camera with both hands raised at shoulder height in a relaxed 'you win' shrug, a wide easy grin. Medium shot. The only change from reference image 2: the night air is completely clear, with no breath cloud, no steam, no smoke and no mist anywhere.",
    "Slow tracking shot backwards. He walks slowly toward the camera with both hands raised in a relaxed 'you win' shrug and laughs warmly, his eyes closing as he laughs. His head keeps facing the camera and keeps its shape: no head shake, no head turn, he does not look up. Nothing moves fast.")
add('N19', ['HER','TAUPE','KF22'], 3, SAMEDOOR % 3 + f"{cap(herL(1))} stands alone in the open doorway wearing {taupe(2)} over her cream blouse, with dark brown trousers; with one hand she folds the front flap of the ribbed stand-up collar outward and looks down at the small label sewn inside it (a plain blank fabric label without any letters), her head tilted, curious. Medium shot.",
    "Static camera. She holds the collar flap out, taps the small label with her fingertip and tilts her head to read it, her eyebrows rising. The label stays completely blank.")
# --- 1:03 het label, slotrefrein
add('N20', ['HER','TAUPE','KF22'], 4, f"Extreme close-up at the same dark-green front door as in reference image 3, warm wall-lamp light: {herL(1)} is wearing {taupe(2)} over her cream blouse; right beside her jaw her fingers fold the front flap of the ribbed stand-up collar outward, showing a small plain blank fabric label without any letters sewn inside the collar; her eyes look down sideways at the label, reading it, with a slow delighted smile. The zip puller is plain metal without any emblem.",
    "Static camera. Her eyes move along the small label as if reading it, then she looks up with a delighted smile. The label stays completely blank.")
add('N21', ['HER','TAUPE','KF22'], 4, f"Close-up in the open doorway of the same dark-green front door as in reference image 3, warm wall-lamp light: {herL(1)}, in {taupe(2)} over her cream blouse, hugs the knit tight around herself with both arms, chin lifted, eyes closed, a triumphant grin.",
    "Static camera. She hugs the knit tighter, lifts her chin and slowly shakes her head no with a triumphant grin. Her eyes stay closed the whole time.")
add('N22', ['HIMN','HER','TAUPE'], 4, DOOR + f"Two-shot: {herL(2)} stands in the open doorway on the left of the frame in {taupe(3)} and dark brown trousers, holding up both arms so the too-long sleeves flop over her hands; {him2(1)} stands on the step on the right of the frame, laughing.",
    "Static camera. She wiggles her raised arms a little so the too-long sleeves flop gently; her hands stay hidden inside the sleeves and the sleeves stay whole. He laughs and shakes his head.")
# N22: de clip van deze prompt (c8eac8e4) wordt gebruikt tot 2,8 s, vertraagd (N22s): daarna laat hij zijn hoofd zakken en wordt hij een andere man.
# Twee rustiger pogingen vielen af: in a7609e15 vegen haar mouwuiteinden twee seconden lang uit, in e230d1b4 verandert haar gezicht vanaf 2,3 s.
add('N23', ['HIMN','KF22'], 3, f"The same dark-green front door with its brass lever handle and the same wet, reflective street at night as in reference image 2, now seen from inside the hallway looking out through the open door: {him2(1)} stands on the wet doorstep holding out one open hand, palm up, eyebrows raised, a hopeful grin. No snow, no smoke or breath cloud.",
    "Static camera. He keeps his arm extended with the palm open and facing up for the whole clip and wiggles his fingers once, hopeful, eyebrows going up. His hand never goes back to his chest and he keeps looking straight ahead. Nothing moves fast.")
add('N24', ['HIMN','HER','TAUPE','KF22'], 4, SAMEDOOR % 4 + f"Seen from the same side. Two-shot: {herL(2)} stands in the open doorway on the left of the frame, wearing and hugging {taupe(3)}, with dark brown trousers, grinning; behind her in the warm hallway a second knit of the same model hangs on a coat hook, in deep navy blue, hanging open so that its two front halves and the zip running from the collar all the way down to the hem are visible; on the step on the right of the frame {him2(1)} laughs with both hands raised in surrender.",
    "Static camera. He keeps both hands raised in surrender, laughing and shaking his head; she hugs the knit and shakes her head no, grinning. The knit on the hook behind her hangs still.")
# --- 1:21 slot
add('N25', ['HIMN','HER','TAUPE'], 3, f"Night on a quiet Milan street with tram tracks and warm street lamps, wet cobblestones. Seen from behind at a little distance: {her(2)}, her long wavy hair hanging loose down her back with no braid and no twist, in {taupe(3)} and dark brown trousers, and the young man from reference image 1 (dark brown hair, short at the nape) in a plain cream T-shirt, navy trousers and navy loafers, walk away from the camera side by side, her arm hooked through his, their heads turned toward each other, laughing. The back of her knit is plain ribbed knit without any zip or seam; the zip is on the front and cannot be seen. The two figures are in the upper half of the frame; the lower third of the frame is empty wet cobblestones.",
    "Slow push-in. They walk on away from the camera, arm in arm; she leans her shoulder against his and he laughs; the street lamps glow on the wet cobblestones. The back of her knit stays plain.")
add('N26', ['KF25'], 5, "Very wide night shot of the Navigli canal in Milan: lamps and warm windows reflected in the dark water, a small iron footbridge. Far away on the towpath, small in the frame, the same couple as in reference image 1 walk close together away from the camera, seen from behind, arm in arm: she has long loose wavy brown hair and wears the taupe ribbed knit and dark brown trousers; he has short dark brown hair and wears a cream T-shirt, navy trousers and navy loafers; neither carries a bag. The lower third of the frame is dark calm water.",
    "Very slow push-in. The two small figures walk on along the canal and grow smaller; the water ripples and the lamp reflections shimmer.")

# montage: (sleutel, t0, t1); elke wissel valt precies op het begin van de gezongen regel volgens tijdlijn v2 (tl2_N3.py),
# of in de stilte ervoor als de vorige regel al uit is;
# alle 31 shots zijn nieuw (K39 uit video 2 is vervangen door N31)
CUTS = [('N01',0.00,3.00),('N02',3.00,5.52),('N03',5.52,8.18),('N04',8.18,10.60),('N05',10.60,13.10),('N06',13.10,15.34),('N07',15.34,18.26),('N08',18.26,21.00),
        ('N27',21.00,23.53),('N09',23.53,26.27),('N10',26.27,28.55),('N28',28.55,31.55),('N29',31.55,34.29),('N30',34.29,36.90),('N31',36.90,39.50),('N11',39.50,42.05),
        ('N12',42.05,44.72),('N13',44.72,47.27),('N14',47.27,49.93),('N15',49.93,51.97),('N16',51.97,54.75),('N17',54.75,57.44),('N18',57.44,60.44),('N19',60.44,63.42),
        ('N20',63.42,67.00),('N21',67.00,70.42),('N22',70.42,74.00),('N23',74.00,77.00),('N24',77.00,80.70),('N25',80.70,83.50),('N26',83.50,90.04)]
OLD = {}
HOLD = {'N26'}       # slotbeeld: de clip van 5 s loopt uit en het laatste beeld blijft staan onder de eindkaart (de laatste 3,5 s van het liedje zijn stilte)
CAP_Y = {'N30': 0.75, 'N14': 0.75}   # ondertitels lager waar ze anders over het belangrijkste van het shot vallen (N30: haar hand op zijn mouw; N14: de mouwuiteinden)
CROP = {}              # N07 had hier 0.04 (strookje broek in de verkeerde kleur); het nieuwe startbeeld van N07 heeft een donkerbruine broek, dus geen uitsnede meer
ENDSAME = {'N07', 'N28'}   # het startbeeld gaat ook als eindbeeld mee (rol end_image): de clip keert terug naar het goedgekeurde beeld, zodat niemand aan het eind verandert
ALT = {'N02': 'clipsG/N02s.mp4', 'N06': 'clipsG/N06s.mp4', 'N13': 'clipsG/N13p.mp4', 'N20': 'clipsG/N20s.mp4', 'N22': 'clipsG/N22s.mp4'}
# bewerkte clips (derive_clips.sh): N02 vertraagd (ogen dicht), N06, N20 en N22 het schone deel vertraagd, N13 vooruit en achteruit (twee vingers blijven omhoog)
if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'list'
    if mode == 'list':
        for s in S: print(s['k'], s['dur'], ','.join(s['refs']), len(s['prompt']))
        d = {k: t1 - t0 for k, t0, t1 in CUTS}
        for s in S: assert d[s['k']] <= s['dur'] + 0.045 or s['k'] in HOLD, (s['k'], d[s['k']], s['dur'])
        assert all(abs(CUTS[i][2] - CUTS[i + 1][1]) < 1e-9 for i in range(len(CUTS) - 1))
        print('shots', len(CUTS), 'nieuw', len(S), 'clipseconden', sum(s['dur'] for s in S), 'credits clips', sum(s['dur'] for s in S) * 1.5)
    elif mode == 'keyframes':
        want = set(sys.argv[2:])
        reqs = [{"index": int(s['k'][1:]), "params": {"model": "gpt_image_2_6", "quality": "medium", "resolution": "2k", "aspect_ratio": "9:16",
                 "medias": [{"role": "image_references", "value": R[r]} for r in s['refs']], "prompt": s['prompt']}} for s in S if not want or s['k'] in want]
        for i in range(0, len(reqs), 4): print(json.dumps(reqs[i:i+4]))
    elif mode == 'clips':
        ids = json.load(open(sys.argv[2])); want = set(sys.argv[3:])
        reqs = [{"index": int(s['k'][1:]), "params": {"model": "kling3_0", "mode": "std", "sound": "off", "duration": s['dur'], "aspect_ratio": "9:16",
                 "medias": [{"role": "start_image", "value": ids[s['k']]}] + ([{"role": "end_image", "value": ids[s['k']]}] if s['k'] in ENDSAME else []),
                 "prompt": s['motion']}} for s in S if s['k'] in ids and (not want or s['k'] in want)]
        for i in range(0, len(reqs), 12): print(json.dumps(reqs[i:i+12]))
    elif mode == 'plan':
        # eindkaart: midden in beeld (end_card_mid.png uit make_end_card.py), faadt in op het slotbeeld bij de laatste klap van de muziek
        shots = []
        for k, t0, t1 in CUTS:
            sh = {"clip": ALT.get(k, f"clipsG/{k}.mp4"), "t0": t0, "t1": t1}
            if k in CAP_Y: sh["cap_y"] = CAP_Y[k]
            if k in CROP: sh["crop_bottom"] = CROP[k]
            if k == 'N26': sh.update(overlay="end_card_mid.png", overlay_fade=0.6)
            shots.append(sh)
        print(json.dumps({"audio": "song_N3.mp3", "words": "timeline_words_N3.json", "cards": "cards_N3.json", "end_hold": True, "end_t": 90.04, "shots": shots}, indent=1))
