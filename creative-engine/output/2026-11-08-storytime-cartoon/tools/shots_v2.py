# Video 2 (verhaal 3, tekst v2): shotlijst met keyframe-prompts. Een shot per regel; 59/60 delen een clip.
# Referenties: HIM_FACE f2d47eb2 (verteller-blad, grijze hoodie), HIM_NAVY cc30e31f (held in navy Reverso), DAVE c613f1e6,
# HER 915ac841 (+ HER_LAUGH 46045520), outfits: T_REVERSO 4b4f96a5, T_LOUNGE 5c3f865a (oatmeal), T_CARDIGAN b0747331 (taupe), T_BLAZER c20b9e73.
# W_OTHER = het andere meisje (character sheet, wordt eerst gegenereerd).
import json, sys
R = dict(HIM='f2d47eb2-2f89-4cdd-8ecf-88d938affb6f', HIMN='cc30e31f-f254-4602-9666-733e01dd5b96', DAVE='c613f1e6-327b-4d41-a628-ddab724d07c3',
         HER='915ac841-6d18-449a-9dd7-fa98badf8ea3', HERL='46045520-f4c1-4e84-81de-0a1a0d4bec6e', TREV='4b4f96a5-c8c4-4751-ba47-16f241dc1f70',
         TLNG='5c3f865a-5960-4dd3-a22c-e98f2e959739', TCAR='b0747331-a3c4-4f9f-bc58-d82ef671648c', TBLZ='c20b9e73-74a9-42b6-9983-e6127b59d646',
         OTHER='OTHER_SHEET_ID')
STYLE = "3D animated feature-film still in the style of a modern Pixar movie: stylized characters with slightly oversized heads, large expressive glossy eyes, sculpted hair, smooth subsurface skin, cinematic shallow depth of field. "
END = " Vertical 9:16. No text, no logos, no signs, no readable writing anywhere."
H = "the young man from reference image 1, exactly the same face and messy brown hair, three-day stubble, in his baggy grey hoodie with a greasy orange pizza stain on the chest"
HN = "the young man from reference image 1, exactly the same face, brown hair neatly combed, clean-shaven, wearing exactly the navy knit set from reference image 2 (ribbed stand collar, slim zip, matching navy trousers) and navy suede loafers without socks"
HO = "the young man from reference image 1, exactly the same face, brown hair neatly combed, clean-shaven, wearing exactly the oatmeal-beige knit set from reference image 2 (ribbed stand collar, slim silver zip, matching trousers) and navy suede loafers without socks"
HC = "the young man from reference image 1, exactly the same face, brown hair neatly combed, clean-shaven, wearing exactly the taupe ribbed cashmere full-zip cardigan from reference image 2 (ribbed stand-up collar, no hood) zipped halfway over a plain cream knit, navy tailored trousers and navy suede loafers"
HB = "the young man from reference image 1, exactly the same face, brown hair neatly combed, clean-shaven, wearing exactly the midnight-navy double-breasted knitted blazer from reference image 2 over a plain cream knit, with navy trousers and navy suede loafers"
HERD = "the young woman from reference image {n} (long wavy brown hair, camel coat)"
OTH = "the young woman from reference image {n} (sleek chin-length black bob, dark green wool jacket over a white tee)"
S = []
def add(k, line, who, refs, dur, prompt, motion):
    S.append(dict(k=k, line=line, who=who, refs=refs, dur=dur, prompt=STYLE + prompt + END, motion=motion))
add('W_OTHER', 0, 'sheet', [], 0,
    "Character sheet, plain warm light-grey background, soft studio light: a young woman of about twenty-seven with a sleek chin-length black bob, olive skin, dark eyes and a warm open laugh, wearing a dark green wool jacket over a plain white t-shirt and black trousers, standing full length relaxed; next to her a large close-up of her laughing face.", '')
add('K01', 1, 'both', ['HIM','TCAR','HER'], 4,
    f"Night, a warm little wine bar in Milan, candlelight, blurred bottles. Close two-shot at the counter: {HERD.format(n=3)} and {HC} face to face, very close, her fingertips resting on his cardigan sleeve, both looking into each other's eyes, a held breath.",
    "Very slow push-in. She glances down at his sleeve and back up to his eyes; he holds her gaze and breathes in. Candle flames flicker.")
add('K02', 2, 'her', ['HER','HERL'], 4,
    f"Autumn afternoon, a park bench in Parco Sempione, Milan, golden leaves. Close-up of {HERD.format(n=1)}, turned toward someone off-frame left, a kind apologetic smile, slowly shaking her head no, eyes warm and honest.",
    "She shakes her head slowly, apologetic, then gives a small kind smile; leaves drift behind her.")
add('K03', 3, 'him', ['HIM'], 4,
    f"Evening, the hallway of a Milanese apartment building, a tall dark-green wooden door that has just closed. {H} stands alone facing the closed door, one hand half raised as if to knock again, head down, a small wilted bunch of daisies hanging from his other hand, one warm wall lamp.",
    "He lowers the raised hand slowly, his shoulders sink, he looks down at the daisies. The lamp flickers slightly.")
add('K04', 4, 'her', ['HER'], 4,
    f"Dusk at the Navigli canal, Milan. {HERD.format(n=1)} walks away over a small iron footbridge, looking back once over her shoulder with a soft hopeful look, canal lights reflecting in the water.",
    "She walks on slowly across the bridge, turns her head back once over her shoulder, then faces forward again; water ripples.")
add('K05', 5, 'him', ['HIM'], 4,
    f"A small bathroom, harsh cold fluorescent light. Seen from behind his shoulder into the mirror: {H} leans on the sink and stares at his own reflection: stubble, tired eyes, greasy hair, the pizza stain.",
    "He leans closer to the mirror, studies his face, rubs his stubble, exhales. The fluorescent tube flickers once.")
add('K06', 6, 'both', ['HIM','HER'], 4,
    f"Autumn late afternoon, wide shot of a park bench in Milan: {H} and {HERD.format(n=2)} sit at opposite ends of the same bench with a clear gap between them, both looking straight ahead, not at each other; golden leaves drifting, two far pedestrians blurred.",
    "Static wide. Leaves drift down; she tucks her hair behind her ear, he fidgets with his hoodie string; neither looks at the other.")
add('K07', 7, 'him', ['HIM'], 3,
    "Extreme close-up in soft daylight: the chest of a baggy grey hoodie with a greasy orange pizza stain; above it the young man's stubbled chin and jaw (face mostly out of frame) as he looks down at the stain and flicks at it with one finger.",
    "His finger flicks at the stain twice, then he shrugs; the fabric moves.")
add('K08', 8, 'him', ['HIM','HER'], 4,
    f"Park bench, autumn afternoon. {H} sits leaning toward {HERD.format(n=2)}, holding out a small wilted bunch of daisies with a hopeful lopsided grin; she looks at him half-surprised, hands in her coat pockets.",
    "He pushes the daisies a little closer with a hopeful grin; she looks from the daisies to his face, uncertain.")
add('K09', 9, 'her', ['HER','HERL'], 4,
    f"Close-up of {HERD.format(n=1)} on the park bench, speaking gently to someone off-frame, her hand resting on a grey hoodie sleeve at the edge of frame, eyes kind and honest, golden autumn light.",
    "She speaks gently, a small shake of the head, her hand gives the sleeve a kind squeeze.")
add('K10', 10, 'both', ['HIM','HER'], 4,
    f"Two-shot on the park bench: {HERD.format(n=2)} gestures softly at his hoodie and stubble with an open palm, explaining kindly; {H} looks down at himself, face falling, shoulders sagging.",
    "Her open hand gestures gently from his hoodie to his chin; he looks down at himself and his shoulders sag.")
add('K11', 11, 'both', ['HIM','HER'], 4,
    f"Close two-shot on the park bench: {HERD.format(n=2)} winces in sympathy like a nurse before a needle, squeezing his shoulder; {H} braces, eyes shut tight, grimacing comically.",
    "She winces and squeezes his shoulder; he screws his eyes shut and braces, then peeks with one eye.")
add('K12', 12, 'both', ['HIM','HER'], 4,
    f"Evening at her front door, a tall dark-green Milanese door with brass handle. {HERD.format(n=2)} gives {H} a quick friendly peck on the cheek, already half turned to go inside; he stands stiff holding the wilted daisies, eyes wide.",
    "She pecks his cheek, turns and steps inside, the green door swings shut; he stays frozen with the daisies, blinking.")
add('K13', 13, 'her', ['HER','HERL'], 4,
    f"Night, a small Milan balcony with a wrought-iron railing, city lights behind. Close-up of {HERD.format(n=1)} singing softly, eyes closed, one hand on her heart, hair moving in a light breeze.",
    "She sings softly, eyes closed, then opens them and looks out over the city; her hair moves in the breeze.")
add('K14', 14, 'him', ['HIM'], 4,
    f"Night, a messy living room lit only by a glowing television: {H} slumped on a couch among open pizza boxes and crumpled cans, a game controller in his hands, a blank stare. Medium wide.",
    "Static. The TV light flickers over him; his thumbs move on the controller; he yawns without looking away.")
add('K15', 15, 'both', ['HIM','HER'], 4,
    f"Evening, a dark Milan shop window. {HERD.format(n=2)} turns {H} gently by the shoulders to face the dark glass; his slouched reflection in the hoodie looks back at him while she watches him, not the glass. Two-shot from the side.",
    "She turns him by the shoulders to face the glass; he looks at his reflection and winces; she watches his face.")
add('K16', 16, 'her', ['HER'], 4,
    f"Evening, the dark-green front door half open, warm light spilling out. {HERD.format(n=1)} leans in the doorway with a small patient smile, looking out at someone off-frame as if waiting to see what he will do.",
    "She leans on the door frame, a patient smile, tilts her head slightly, then slowly starts to close the door.")
add('K17', 17, 'both', ['HIM','HER'], 4,
    f"Evening, wide shot of a quiet Milanese street with a tram wire above, soft rain beginning: {HERD.format(n=2)} stands in her lit doorway, {H} stands on the pavement a few steps away holding the wilted daisies; they look at each other across the gap.",
    "Rain begins to fall; they look at each other across the street; she steps back inside and the door closes; he stays.")
add('K18', 18, 'him', ['HIM'], 4,
    f"Bathroom mirror, close on his reflection: {H}, eyes narrowing with new determination, jaw set; a toothbrush cup and a razor on the sink below.",
    "He stares at himself, his eyes narrow with determination, he nods once and reaches for the razor.")
add('K19', 19, 'him', ['HIM'], 4,
    f"A classic old Milan barber shop, morning light, chequered floor. {H} sits in the barber chair under a striped cape (the hoodie collar visible), eyes wide, as clumps of brown hair fall; the barber's hands with scissors and comb work above him, the barber's head out of frame.",
    "Scissors snip, clumps of hair fall onto the cape, his eyes go wide and then he grins a little.")
add('K20', 20, 'him', ['HIM'], 4,
    "A narrow apartment hallway, morning light. The young man from reference image 1, exactly the same face, now with a fresh short haircut and clean-shaven, in a plain white t-shirt and grey sweatpants, stuffs three grey hoodies into a black bin bag with gusto, one hoodie still hanging out.",
    "He stuffs the last hoodie into the bin bag, ties it shut with a decisive tug and dusts off his hands.")
add('K21', 21, 'him', ['HIM','DAVE'], 4,
    "Apartment doorway, daylight. The flatmate from reference image 2, exactly his face and hair, leans in holding a large plain brown cardboard box, one eyebrow raised; the young man from reference image 1 (same face, fresh short haircut, clean-shaven, plain white t-shirt) reaches for the box eagerly.",
    "Dave hands over the box with a suspicious eyebrow; he grabs it eagerly and hugs it to his chest.")
add('K22', 22, 'him', ['HIMN','TREV'], 4,
    f"Bedroom mirror, soft morning light. {HN} zips the navy knit up in front of the mirror; close on the ribbed stand collar and the slim zip, his chin lifting for the first time.",
    "He pulls the zip up slowly to the collar, straightens the collar, lifts his chin and looks at himself.")
add('K23', 23, 'him', ['DAVE','HIMN'], 4,
    "Living room, daylight. The flatmate from reference image 1 sits on the couch with a cereal bowl, spoon frozen halfway to his mouth, starting a slow approving nod; in the doorway the young man from reference image 2, exactly the same face and neat brown hair, stands tall in the navy knit set with ribbed stand collar and navy suede loafers, arms slightly out.",
    "Dave's spoon stays frozen, then he nods slowly in approval; the young man gives a small shrug and a grin.")
add('K24', 24, 'him', ['HIMN','TREV'], 4,
    f"A Milan espresso bar, marble counter, morning light. A smiling barista in a white shirt and black apron slides a small plain espresso cup and saucer across the marble toward {HN}, who looks up pleasantly surprised; the cup has no writing.",
    "The barista slides the cup over with a smile; he looks up, surprised, and smiles back; steam rises from the cup.")
add('K25', 25, 'him', ['HIMN','TREV'], 4,
    f"Night, a desk by a window. {HN} looks puzzled at his phone lying face up on the desk, its screen lit with a stack of blank glowing message bubbles with no letters; the phone light on his face.",
    "The phone buzzes and lights up again and again with new blank bubbles; he leans back, eyebrows up, half laughing.")
add('K26', 26, 'her', ['HER','HIM','TLNG'], 4,
    f"Grey afternoon, seen from inside an orange Milan tram through the window: {HERD.format(n=1)} in the foreground looks out; outside on the pavement {HO.replace('reference image 1','reference image 2').replace('reference image 2 (ribbed','reference image 3 (ribbed')} walks with his head up, relaxed, shoulders back.",
    "The tram glides slowly; outside he walks on with his head up; she follows him with her eyes, lips parting.")
add('K27', 27, 'him', ['HIM','TLNG'], 4,
    f"Grey afternoon on a Milan street. {HO} glances briefly toward a passing orange tram, then looks away ahead, unbothered, walking on; medium shot, the tram a blur at the edge of frame.",
    "He glances toward the tram for half a second, looks away ahead and keeps walking; the tram blurs past.")
add('K28', 28, 'her', ['HER','HERL'], 4,
    f"Inside the tram, close-up of {HERD.format(n=1)}: hand flat on the window glass, lips parted, eyes following something outside, a small frown of disbelief.",
    "Her eyes track something moving outside; her hand presses flat on the glass; she swallows.")
add('K29', 29, 'her', ['HER'], 4,
    f"Wide high angle at dusk: {HERD.format(n=1)} stands alone and small on an empty tram platform, the big grey city and tram wires around her, hugging her coat.",
    "Static high wide. She hugs her coat tighter; a tram passes behind her without stopping; her hair moves.")
add('K30', 30, 'her', ['HER'], 4,
    f"Night, her bedroom, warm lamp light. {HERD.format(n=1)}, in a cream knit instead of the coat, sits on the edge of her bed holding her dark phone in both hands, looking at nothing, thinking.",
    "She turns the dark phone over in her hands, almost unlocks it, then lays it face down on the bed.")
add('K31', 31, 'her', ['HER'], 4,
    f"Autumn late afternoon, the park bench in Milan: {HERD.format(n=1)} sits alone at one end; the other end is empty with a few fallen leaves on it; she looks at the empty space beside her.",
    "Static. She looks at the empty seat beside her; a leaf falls onto it; she brushes it off slowly.")
add('K32', 32, 'both', ['HIM','TLNG','HER'], 4,
    f"The Galleria arcade in Milan, evening, glass roof, mosaic floor, people blurred. {HO} walks toward camera on the left; {HERD.format(n=3)} walks away from camera on the right; they pass each other without seeing. Symmetrical wide shot.",
    "They walk past each other in opposite directions without noticing; the crowd blurs; slow push-in.")
add('K33', 33, 'her', ['HER','HERL'], 4,
    f"Evening in the Galleria. {HERD.format(n=1)} has stopped and turned; close-up over her shoulder as she watches someone walk away, a bittersweet half-smile.",
    "She stops, turns her head to look back after him, a bittersweet half-smile, then looks down.")
add('K34', 34, 'him', ['HIM','TLNG'], 4,
    f"Evening, a dark shop window in Milan reflects {HO}: he straightens his back, lifts his chin and tugs the ribbed collar straight, a quiet confident look. Medium close on the reflection.",
    "He straightens up, tugs the collar straight, lifts his chin and gives his reflection a small nod.")
add('K35', 35, 'both', ['HER','HIM','TLNG'], 4,
    f"Evening, across a Milan street with tram tracks: {HERD.format(n=1)} in the blurred foreground has just seen him; in focus beyond her, {HO.replace('reference image 1','reference image 2').replace('reference image 2 (ribbed','reference image 3 (ribbed')} waits at a crossing, head up, unaware of her.",
    "The crossing light changes, he walks on with his head up; she stays where she is and watches him go.")
add('K36', 36, 'him', ['HIM','TCAR'], 4,
    f"Evening, his kitchen table, warm light. {HC} looks at his phone buzzing face-up on the table, lit with one blank glowing message bubble; he raises one eyebrow with a dry half-smile.",
    "The phone buzzes and slides a little on the table; he raises an eyebrow, picks it up and reads with a dry smile.")
add('K37', 37, 'him', ['HIM','TCAR'], 4,
    f"Hallway mirror by the front door, evening. {HC} fixes his hair with one hand, keys in the other, a wry look at himself, a scarf on a coat hook behind him.",
    "He fixes his hair with two quick strokes, checks himself, jingles the keys and turns to the door.")
add('K38', 38, 'both', ['HER','HIM','TCAR'], 4,
    f"Night, the warm little wine bar in Milan, candlelight. Two-shot at the counter: {HERD.format(n=1)} leans in and touches his cardigan sleeve with her fingertips; {HC.replace('reference image 1','reference image 2').replace('reference image 2 (ribbed','reference image 3 (ribbed')} looks at her hand, then at her, calm.",
    "She leans in and touches his sleeve; he looks down at her hand, then up at her face, calm and amused.")
add('K39', 39, 'her', ['HER','HERL'], 4,
    f"Close-up of {HERD.format(n=1)} at the wine bar, eyebrows raised, looking down at a taupe knit sleeve she is touching with her fingertips, lips slightly open, warm candlelight.",
    "She rubs the knit between her fingertips, eyebrows rising, and looks up slowly.")
add('K40', 40, 'her', ['HER','HERL'], 4,
    f"Close-up of {HERD.format(n=1)} at the wine bar, head tilted, asking a playful curious question, eyes bright, a strand of hair falling over her cheek, candlelight.",
    "She tilts her head, asks a question with a playful smile, and tucks the strand of hair behind her ear.")
add('K41', 41, 'him', ['HIM','TCAR'], 4,
    f"Close-up of {HC} at the wine bar, answering calmly with a small proud smile, one hand resting on the ribbed collar of the taupe cardigan, candlelight.",
    "He answers calmly, touches his collar once, a small proud smile, then lifts his glass.")
add('K42', 42, 'other', ['OTHER'], 4,
    f"Night, the warm wine bar. At the next small table, {OTH.format(n=1)} laughs out loud, head thrown back, a hand on her chest, a glass of red wine in front of her, candlelight.",
    "She laughs out loud, head back, hand on her chest, then wipes an eye, still laughing.")
add('K43', 43, 'him', ['HIM','TCAR','OTHER'], 4,
    f"The wine bar at night. {HC} is mid-joke, hands animated, turned toward the next table where {OTH.format(n=3)} laughs, looking at his face; medium two-shot, candlelight.",
    "He gestures as he tells the joke; she laughs and leans toward him; he grins, surprised at himself.")
add('K44', 44, 'both', ['HER','HIM','OTHER'], 4,
    f"The wine bar at night, symmetrical medium shot: the young man from reference image 2 (exactly his face and neat brown hair, taupe ribbed cashmere full-zip cardigan over a cream knit) sits in the centre; on the left {HERD.format(n=1)} looks at his sleeve; on the right {OTH.format(n=3)} laughs looking at his face.",
    "Static symmetrical shot. The woman on the left studies his sleeve; the woman on the right laughs at his face; he looks from one to the other.")
add('K45', 45, 'both', ['HIM','TCAR','HER'], 4,
    f"The wine bar at night. {HC} has stood up and gives {HERD.format(n=3)} a quick friendly peck on the cheek with a kind smile, already turning toward the next table; she sits very still, hands around her glass.",
    "He pecks her cheek kindly, squeezes her shoulder once and turns away toward the next table; she stays very still.")
add('K46', 46, 'her', ['HER'], 4,
    f"The wine bar, late at night. {HERD.format(n=1)} slowly pulls on her camel coat, eyes down, one arm in a sleeve, the candle burned low in front of her.",
    "She pulls the coat on slowly, one arm, then the other, eyes down; the low candle flickers.")
add('K47', 47, 'her', ['HER','HIM','OTHER'], 4,
    f"The wine bar at night, over the shoulder of {HERD.format(n=1)} (coat on, at the door): deeper inside, the young man from reference image 2 (exactly his face, taupe ribbed cardigan) sits at a small table with {OTH.format(n=3)}, both laughing; he does not look back.",
    "She pauses at the door and looks back; inside they keep laughing; he never turns around; she steps out.")
add('K48', 48, 'her', ['HER'], 4,
    f"Night inside an almost empty orange Milan tram: {HERD.format(n=1)} sits alone by the window, her reflection in the dark glass, city lights streaking past.",
    "The tram sways gently; city lights streak past the window; she leans her head against the glass.")
add('K49', 49, 'her', ['HER'], 4,
    f"From the tram window at night: an empty tram stop with a lit shelter glides past, nobody waiting; the faint reflection of {HERD.format(n=1)} in the glass.",
    "The empty lit tram stop slides past the window and disappears; her faint reflection stays.")
add('K50', 50, 'other', ['HIM','OTHER'], 4,
    f"Night street in Milan, seen from outside through the warm window of the little wine bar: at a small table the young man from reference image 1 (exactly his face, neat brown hair, taupe ribbed cardigan) and {OTH.format(n=2)} laugh together over two glasses of wine; cold blue street in the foreground.",
    "Through the window they laugh and clink glasses; a reflection of a passing tram slides over the glass.")
add('K51', 51, 'her', ['HER','HERL'], 4,
    f"Night tram, close-up: {HERD.format(n=1)} looks at her own reflection in the dark window, a small bitter smile, eyes shining.",
    "She looks at her reflection, a small bitter smile, then closes her eyes.")
add('K52', 52, 'her', ['HER'], 4,
    f"Night, {HERD.format(n=1)} stands at her apartment window with the camel coat still on, forehead almost touching the glass, the city lights and an orange tram passing in the street below.",
    "Static. A tram passes below with its lights; she rests her forehead on the glass and breathes out.")
add('K53', 53, 'none', [], 4,
    "Night, a park bench in Milan under a single lamp post, empty, wet from rain, a small wilted bunch of daisies left lying on the seat among fallen leaves. No people.",
    "Static. Light rain falls through the lamp light; a leaf lands on the bench next to the daisies.")
add('K54', 54, 'him', ['HIM','TBLZ'], 4,
    f"Night in the Galleria arcade, Milan, warm lights, mosaic floor. Close-up of {HB}, calm and kind, speaking straight to the camera with a slight nod.",
    "He speaks calmly to camera, a slight nod, a kind look, then a small honest shrug.")
add('K55', 55, 'her', ['HER','HERL'], 4,
    f"Night at her window. Close-up of {HERD.format(n=1)} nodding slowly, wiping a tear away with the back of her hand, a small brave smile.",
    "She nods slowly, wipes a tear with the back of her hand and manages a small brave smile.")
add('K56', 56, 'him', ['HIM','TBLZ','OTHER'], 4,
    f"Night in the Galleria. {HB} helps {OTH.format(n=3)} into her dark green coat, attentive and careful; medium shot, mosaic floor, warm arcade lights.",
    "He holds the coat as she slips her arms in, settles it on her shoulders; she looks back at him and smiles.")
add('K57', 57, 'him', ['HIM','TBLZ'], 4,
    f"Night in the Galleria. {HB} pauses and looks back over his shoulder toward the camera with a grateful gentle nod. Medium close.",
    "He pauses mid-step, looks back over his shoulder to camera, a grateful nod, then walks on.")
add('K58', 58, 'her', ['HER'], 4,
    f"Night, the park bench under the lamp post: {HERD.format(n=1)} sits alone at one end, the wilted daisies lying beside her on the empty seat; she looks down at them.",
    "Static. She looks at the daisies beside her, picks them up gently and holds them in her lap.")
add('K59', 59, 'both', ['HIM','TBLZ','OTHER'], 5,
    f"Night, wide shot of the Galleria in Milan: {HB} and {OTH.format(n=3)} walk away from camera arm in arm toward the glowing arcade, the mosaic floor shining, nobody else near.",
    "Static wide. They walk away arm in arm into the glowing arcade, getting smaller; the lights shimmer on the mosaic floor.")
if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'list'
    if mode == 'list':
        for s in S: print(s['k'], s['line'], s['who'], ','.join(s['refs']), len(s['prompt']))
    elif mode == 'batch':
        ks = sys.argv[2].split(','); other = sys.argv[3] if len(sys.argv) > 3 else R['OTHER']
        reqs = []
        for i, s in enumerate([x for x in S if x['k'] in ks]):
            medias = [{"role": "image_references", "value": (other if r == 'OTHER' else R[r])} for r in s['refs']]
            reqs.append({"index": int(s['k'][1:]) if s['k'][0] == 'K' else 0, "params": {"model": "gpt_image_2_6", "quality": "medium", "resolution": "2k", "aspect_ratio": "9:16", "medias": medias, "prompt": s['prompt']}})
        print(json.dumps(reqs, ensure_ascii=False))
    elif mode == 'json':
        json.dump(S, open(sys.argv[2], 'w'), indent=1, ensure_ascii=False)
