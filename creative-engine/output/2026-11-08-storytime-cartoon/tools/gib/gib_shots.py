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
         DAVE='c613f1e6-327b-4d41-a628-ddab724d07c3', BAR='afafaccc-f021-4d8f-96ea-8b347d2ba192')
STYLE = "3D animated feature-film still in the style of a modern Pixar movie: stylized characters with slightly oversized heads, large expressive glossy eyes, sculpted hair, smooth subsurface skin, cinematic shallow depth of field. "
END = " Everything is in sharp focus where it matters: no motion blur, no motion lines, no speed lines. Vertical 9:16. No text, no logos, no signs, no readable writing anywhere."
MPRE = "3D animated feature-film look. "
MEND = " Subtle natural performance only; everyone keeps exactly their face, hair, clothes and colours from the start frame. No text, no logos. One continuous take."
def her(n): return f"the young woman from reference image {n} (long wavy brown hair)"
def him(n, top="a plain white T-shirt"): return f"the young man from reference image {n} (exactly the same face, brown hair neatly combed, clean-shaven), in only {top} and navy trousers"
CREAM = 'a plain cream T-shirt'
def knit1(n): return f"exactly the full-zip ribbed cashmere knit from reference image {n} (ribbed stand-up collar, full-length zip, ribbed cuffs and hem), in deep navy blue"
def navy(n): return knit1(n) + ", far too big for her"
def taupe(n): return f"exactly the taupe ribbed cashmere zip cardigan from reference image {n} (ribbed stand-up collar), far too big for her"
def himt(a, b): return (f"the young man from reference image {a} (exactly the same face, brown hair neatly combed, clean-shaven), wearing exactly the taupe ribbed cashmere "
                        f"zip cardigan from reference image {b} (ribbed stand-up collar), fitting him well, zipped over a cream T-shirt, with navy trousers")
LIVING = "A cosy Milan living room at night, warm lamp light, a sofa and a window with city lights behind. "
CANAL = "A cold clear night at the Navigli canal in Milan, street lamps reflected in the dark water, their breath visible in the cold air. "
DOOR = "Night on a quiet, dry Milan street, a tall dark-green wooden front door with a brass handle, one warm wall lamp. "
S = []
def add(k, refs, dur, prompt, motion): S.append(dict(k=k, refs=refs, dur=dur, prompt=STYLE + prompt + END, motion=MPRE + motion + MEND))
def cap(s): return s[0].upper() + s[1:]

# --- 0:00 haar refrein, thuis in zijn donkerblauwe knit
add('N01', ['HER','NAVY'], 3, LIVING + f"Medium close-up of {her(1)}, wearing {navy(2)}, zipped up, with dark brown trousers, the sleeves covering her hands; she hugs it tight around herself with both arms, chin tucked into the collar, eyebrows raised, a teasing stubborn smile, looking straight at the camera.",
    "Static camera. She hugs the knit tighter around herself and slowly shakes her head no with a teasing smile; her hair sways slightly.")
add('N02', ['HER','NAVY'], 3, LIVING + f"Close-up of {her(1)} in {navy(2)}, zipped up, with dark brown trousers: with one sleeve-covered hand she presses the soft ribbed collar against her cheek, eyes closed, a blissful little smile.",
    "Static camera. She rubs her cheek against the soft collar with her eyes closed, then opens her eyes and gives one small firm nod.")
add('N03', ['HER','NAVY'], 3, LIVING + f"Three-quarter shot of {her(1)} standing fully dressed in {navy(2)}, zipped up, with dark brown trousers: she lifts both forearms so the far-too-long sleeves flop over her hands, the ribbed stand-up collar high under her chin, a delighted grin. Family-friendly.",
    "Static camera. She flaps the too-long sleeves once and tucks her chin into the high collar, grinning.")
add('N04', ['HIMN','HER','NAVY'], 3, LIVING + f"Two-shot: {him(1)} holds out one open hand, palm up, asking for his knit back with a hopeful grin; facing him {her(2)} wears {navy(3)}, zipped up, with dark brown trousers, her arms wrapped tight around herself, leaning away from his hand with a cheeky grin.",
    "Static camera. He wiggles the fingers of his open hand, asking; she shakes her head, grins and hugs the knit tighter.")
# --- 0:10 de gracht: hij geeft zijn knit
add('N05', ['HIMN','HER','NAVY'], 3, CANAL + f"Two-shot on the towpath: {him(1)} is draping {knit1(3)} around the shoulders of {her(2)}, who wears a thin cream blouse and dark brown trousers, hugs herself against the cold and looks up at him, surprised and touched.",
    "Static camera. He settles the knit around her shoulders and tugs it closed at the front; she looks up at him and smiles; their breath shows in the cold air.")
add('N06', ['HIMN','HER','NAVY'], 3, CANAL + f"Medium two-shot walking along the towpath toward the camera: {her(2)} is snug in {navy(3)}, zipped up, with dark brown trousers, her hands hidden in the sleeves, smiling to herself; beside her {him(1)} walks with his arms wrapped around himself, shivering with a brave grin.",
    "Slow tracking shot. They walk along the canal; he rubs his bare arms and shivers with a grin; she snuggles deeper into the knit.")
add('N07', ['HER','NAVY'], 3, CANAL + f"Close-up of {her(1)} pulling the zip of {navy(2)} all the way up to the top of the ribbed stand-up collar under her chin, the sleeves over her hands, warm lamp light on her face, a big grin.",
    "Static camera. She pulls the zip all the way up to her chin, tucks her chin into the collar and grins.")
add('N08', ['HER','NAVY'], 3, f"Her cosy living room at night, lit by a warm lamp and the bluish glow of a television off-frame. {cap(her(1))} sits curled up on the sofa in {navy(2)}, zipped up, with dark brown trousers and thick wool socks, knees pulled up, holding a steaming mug of tea in both sleeve-covered hands, watching the screen with a cosy smile.",
    "Static camera. She blows on the tea, takes a small sip and snuggles deeper into the knit; the television light flickers on her face.")
# --- 0:20 zijn rap: hoodies, compliment, lege hanger, huisgenoot, nieuwe knit, wijnbar
add('N27', ['HIMN'], 3, f"His bedroom in daylight: an open wardrobe with a shelf holding a tall neat stack of identical plain grey hoodies. {cap(him(1))}, stands beside it and points at the stack with one thumb, eyebrows raised, a dry amused look at the camera. Medium shot.",
    "Static camera. He jerks his thumb at the untouched stack of grey hoodies, shrugs and shakes his head with a dry grin.")
add('N09', ['HIMN'], 3, f"His bedroom in daylight, an open wardrobe behind him. Medium close-up of the young man from reference image 1 (exactly the same face, brown hair neatly combed, clean-shaven) in a plain white T-shirt, one hand on his chest, eyebrows raised, a surprised, flattered grin, as if he has just been paid a compliment.",
    "Static camera. He points at himself with a 'who, me?' look, then breaks into a flattered grin and shrugs.")
add('N10', ['HIMN'], 3, f"His bedroom in daylight: an open wardrobe with a clothes rail holding a few shirts and, in the middle, one empty wooden hanger. {cap(him(1))}, stands beside it looking at the empty hanger, one hand scratching the back of his head, an amused half-smile. Medium shot from the side.",
    "Static camera. The empty hanger swings gently on the rail; he scratches the back of his head, shrugs and smiles to himself.")
add('N28', ['HIMN','DAVE'], 3, f"Daylight in the hallway of a Milan apartment, the front door open. In the doorway stands the flatmate from reference image 2 (stocky, curly dark hair, short beard, green T-shirt), holding a plain brown cardboard parcel with no print, one eyebrow raised high, a knowing smirk; {him(1)} reaches for the parcel with both hands and a sheepish grin. Medium two-shot.",
    "Static camera. The flatmate raises one eyebrow even higher and holds the parcel back for a moment; he takes it with a sheepish grin.")
add('N29', ['HIMN','TCAR','BAR'], 3, f"The same candlelit Milan wine bar as in reference image 3 (red leather chairs, marble tables, glowing candle glasses, glasses of red wine, warm lamps). Medium shot of {himt(1, 2)}: he sits alone at a small marble table and smooths the ribbed collar of the cardigan with one hand, a proud little smile, looking off to the side.",
    "Static camera. He smooths the collar of the new knit, sits up a little straighter and smiles, pleased with himself; the candle flickers.")
add('N30', ['HER','HIMN','TCAR','BAR'], 3, f"The same candlelit Milan wine bar as in reference image 4 (red leather chairs, marble table, a glowing candle glass, glasses of red wine). Two-shot at the small marble table: {her(1)}, in the same cream trench coat and cream blouse as in reference image 4, lays her hand on the forearm of {himt(2, 3)}, feeling the soft ribbed sleeve, her eyes wide with delight; he looks down at her hand with a knowing, resigned little smile.",
    "Static camera. She strokes the ribbed sleeve with her fingertips, delighted; he looks from her hand to her face and smiles, already knowing what comes next.")
# K39 (bestaande clip): close-up van haar aan de wijnbar, haar vingers op zijn mouw
add('N11', ['HER','HIMN','TCAR'], 3, f"Night on a Milan street outside a warm little wine bar, candlelit windows behind, breath visible in the cold. Two-shot: {her(1)}, in a cream blouse and dark brown trousers, her cream trench coat folded over one arm, is slipping her arms into {taupe(3)}, with a delighted grin; beside her {him(2, CREAM)} watches with a resigned, amused smile.",
    "Static camera. She pulls the big cardigan on and does a little happy shimmy; he shakes his head, smiling, and rubs his arms.")
# --- 0:42 haar refrein, knit nummer twee
add('N12', ['HER','TCAR'], 3, f"Night on a Milan street with tram tracks and warm street lamps. Medium close-up of {her(1)} wearing {taupe(2)}, hugging it tight around herself with both arms, chin tucked into the collar, a teasing stubborn smile, looking at the camera.",
    "Static camera. She hugs the cardigan tighter and shakes her head no with a teasing smile.")
add('N13', ['HER','TCAR'], 3, f"Night on a Milan street with warm street lamps. Close-up of {her(1)} in {taupe(2)}: she holds up two fingers in a V right next to her cheeky grin, one eyebrow raised.",
    "Static camera. She raises two fingers, wiggles them and raises one eyebrow with a cheeky grin.")
add('N14', ['HER','TCAR'], 3, f"Night on a Milan street with warm street lamps. Three-quarter shot of {her(1)} in {taupe(2)}, with dark brown trousers: she holds both arms out so the cuffs hang far past her fingertips, the ribbed collar turned up high, laughing.",
    "Static camera. She does one slow half-turn so the long sleeves swing, then stops and grins.")
add('N15', ['HIMN','HER','TCAR'], 3, f"Night at a Milan tram stop, an orange tram waiting with its doors open, warm street lamps, breath visible. Two-shot: {him(1, CREAM)} holds out one open hand, palm up, with a hopeful grin; {her(2)}, wearing {taupe(3)}, steps backward onto the tram step, laughing and shaking her head.",
    "Static camera. He holds out his open hand; she steps back onto the tram, laughing, and gives a little wave with a too-long sleeve.")
# --- 0:52 zijn rap: tram, perron, T-shirt, haar deur
add('N16', ['HER','TCAR'], 3, f"Night in Milan, an orange tram pulling away from a stop, wet cobblestones, street lamps. Seen from the empty platform, nobody in the foreground: at the lit tram window {her(1)} wears {taupe(2)} and waves with a sleeve-covered hand, a cheeky grin.",
    "Static camera. The tram starts to roll; she waves with the too-long sleeve and grins through the window.")
add('N17', ['HIMN'], 3, f"A tram stop in Milan at night, wet cobblestones, street lamps, an orange tram gliding away in the background. {cap(him(1, CREAM))}, stands alone on the platform, arms hugged against the cold, laughing at himself, his head still. Medium shot.",
    "Static camera. He watches the tram leave, hugs his arms, laughs and shakes his head; the tram glides away.")
add('N18', ['HIMN'], 3, f"Night on a quiet Milan street with warm shop windows and street lamps, breath visible in the cold. {cap(him(1, CREAM))}, walks toward the camera with both hands raised at shoulder height in a relaxed 'you win' shrug, a wide easy grin. Medium shot.",
    "Slow tracking shot backwards. He walks toward the camera, shrugs with both hands up, laughs and shakes his head.")
add('N19', ['HER','TCAR'], 3, DOOR + f"The door has swung open and {her(1)} stands in the doorway wearing {taupe(2)} with dark brown trousers; with one hand she turns one side of the ribbed stand-up collar inside out and looks down at the small sewn-in label inside it (a plain blank fabric label without any letters), her head tilted, curious. Medium shot from the doorstep.",
    "Static camera. She turns the collar out with her fingers, peers down at the label inside and raises her eyebrows.")
# --- 1:03 het label, slotrefrein
add('N20', ['HER','TCAR'], 4, f"Extreme close-up at a dark-green front door, warm wall-lamp light: the fingers of {her(1)} hold the turned-out ribbed collar of exactly the taupe ribbed cashmere zip cardigan from reference image 2, showing a small plain blank fabric label without any letters sewn inside; above it her eyes look down at the label, reading it, with a slow delighted smile.",
    "Static camera. Her eyes move along the label as if reading it, then she looks up with a delighted smile.")
add('N21', ['HER','TCAR'], 4, f"Close-up in the doorway of a tall dark-green front door, warm wall-lamp light: {her(1)}, in {taupe(2)}, hugs the knit tight around herself with both arms, chin lifted, eyes closed, a triumphant grin.",
    "Static camera. She hugs the knit tighter, lifts her chin, then opens her eyes and shakes her head no with a triumphant grin.")
add('N22', ['HIMN','HER','TCAR'], 4, DOOR + f"Two-shot: {her(2)} stands in the open doorway in {taupe(3)} and dark brown trousers, holding up both arms so the too-long sleeves flop over her hands; {him(1, CREAM)} stands on the step in front of her, laughing.",
    "Static camera. She flaps the too-long sleeves at him like little wings; he laughs and shakes his head.")
add('N23', ['HIMN'], 3, f"Night at the doorstep of a tall dark-green front door lit by one warm wall lamp, a quiet dry Milan street behind him, no snow, breath visible in the cold. Seen from inside the doorway: {him(1, CREAM)} stands on the step holding out one open hand, palm up, eyebrows raised, a hopeful grin.",
    "Static camera. He holds out his open hand and wiggles his fingers, hopeful; his breath shows in the cold.")
add('N24', ['HIMN','HER','TCAR'], 5, DOOR + f"Two-shot: {her(2)} stands in the open doorway wearing and hugging {taupe(3)}, with dark brown trousers, grinning; behind her in the warm hallway a deep navy blue ribbed zip knit hangs on a coat hook; on the step in front of her {him(1, CREAM)} laughs with both hands raised in surrender.",
    "Static camera. He laughs and raises both hands in surrender, shaking his head; she hugs the knit and shakes her head no, grinning.")
# --- 1:21 slot
add('N25', ['HIMN','HER','TCAR'], 5, f"Night on a quiet Milan street with tram tracks and warm street lamps, wet cobblestones. Seen from behind at a little distance: {her(2)} in {taupe(3)} and dark brown trousers, and the young man from reference image 1 (neat brown hair) in a plain cream T-shirt and navy trousers, walk away from the camera side by side, her arm hooked through his, their heads turned toward each other, laughing. The two figures are in the upper half of the frame; the lower third of the frame is empty wet cobblestones.",
    "Slow push-in. They walk on away from the camera, arm in arm; she bumps her shoulder against his and he laughs; the street lamps glow on the wet cobblestones.")
add('N26', [], 4, "Very wide night shot of the Navigli canal in Milan: lamps and warm windows reflected in the dark water, a small iron footbridge; far away on the towpath two small figures walk close together away from the camera, one in a taupe knit and one in a cream T-shirt. The lower third of the frame is dark calm water.",
    "Very slow push-in. The two small figures walk on along the canal and grow smaller; the water ripples and the lamp reflections shimmer.")

# montage: (sleutel, t0, t1) op de regels van take N3; K39 is de enige bestaande clip
CUTS = [('N01',0.00,3.00),('N02',3.00,5.60),('N03',5.60,8.30),('N04',8.30,10.50),('N05',10.50,12.90),('N06',12.90,15.40),('N07',15.40,18.20),('N08',18.20,20.60),
        ('N27',20.60,23.30),('N09',23.30,26.10),('N10',26.10,28.50),('N28',28.50,31.50),('N29',31.50,34.20),('N30',34.20,36.60),('K39',36.60,39.20),('N11',39.20,41.80),
        ('N12',41.80,44.70),('N13',44.70,47.20),('N14',47.20,49.90),('N15',49.90,52.10),('N16',52.10,54.50),('N17',54.50,57.40),('N18',57.40,60.40),('N19',60.40,63.20),
        ('N20',63.20,66.90),('N21',66.90,70.50),('N22',70.50,73.80),('N23',73.80,76.40),('N24',76.40,81.40),('N25',81.40,86.40),('N26',86.40,90.04)]
OLD = {'K39': 'clips3/K39.mp4'}
if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'list'
    if mode == 'list':
        for s in S: print(s['k'], s['dur'], ','.join(s['refs']), len(s['prompt']))
        d = {k: t1 - t0 for k, t0, t1 in CUTS}
        for s in S: assert d[s['k']] <= s['dur'] + 0.045, (s['k'], d[s['k']], s['dur'])
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
                 "medias": [{"role": "start_image", "value": ids[s['k']]}], "prompt": s['motion']}} for s in S if s['k'] in ids and (not want or s['k'] in want)]
        for i in range(0, len(reqs), 12): print(json.dumps(reqs[i:i+12]))
    elif mode == 'plan':
        shots = [{"clip": (f"clipsG/{k}.mp4" if k.startswith('N') else OLD[k]), "t0": t0, "t1": t1} for k, t0, t1 in CUTS]
        for s in shots:
            if 'N25' in s['clip'] or 'N26' in s['clip']: s['overlay'] = 'end_overlay.png'
        print(json.dumps({"audio": "song_N3.mp3", "words": "timeline_words_N3.json", "end_hold": True, "end_t": 90.04, "shots": shots}, indent=1))
