# Bouwt generate_video_batch-requests uit clip_requests_v3.json (uit de sandbox) met de bewegingsprompts uit shots_v2.py.
import json, sys
SRC = sys.argv[1]
sys.argv = [sys.argv[0]]
import shots_v2
MOTION = {s['k']: s['motion'] for s in shots_v2.S}
MOTION.update(shots_v2.EXTRA_MOTION)
MOTION['K25b'] = "Static camera. He steps out of the green door onto the pavement, pulls the door shut behind him, lifts his chin and walks toward camera with an easy confident stride; a tram glides past in the background."
MOTION['K38b'] = "Static camera. He walks past the terrace with an amused glance; the blonde woman holds up her phone and waves it at him, the red-haired woman touches her collar and asks something; both turn to follow him with their eyes."
ALT = {  # tweede gebruik van dezelfde keyframe: andere beweging
 'K25_2': "Static. The phone buzzes and slides on the desk, lighting up again and again with blank bubbles; he picks it up, scrolls, shakes his head with a small disbelieving smile.",
 'K14_2': "Very slow push-in. He stares at the TV, the light flickers, a slice of pizza slides off the box onto the couch; he doesn't notice.",
 'K17_2': "Static wide. Rain falls harder; he stays on the pavement in the rain holding the daisies while she closes the door; a tram passes behind him.",
 'K01_2': "Static close two-shot. She tightens her fingers on his sleeve and searches his face; he looks at her kindly but does not move closer.",
 'K05_2': "Static. He turns his head left and right in the mirror, pulls at his greasy hair, lifts his chin to look at his stubble and sighs.",
 'K44': "Static symmetrical shot. The woman on the left studies his sleeve; the woman on the right laughs at his face; he looks from one to the other with a small shrug.",
}
reqs = json.load(open(SRC))
out = []
for i, r in enumerate(reqs):
    key = r['key']; name = r['name']
    if name in ALT: motion = ALT[name]
    elif name != key and key in ALT: motion = ALT[key]
    elif key in MOTION: motion = MOTION[key]
    else: motion = MOTION[key.rstrip('r')]
    prompt = "3D animated feature-film look. " + motion + " Subtle natural performance only; everyone keeps exactly their face, hair, clothes and colours from the start frame. No text, no logos. One continuous take."
    out.append({"index": i + 1, "params": {"model": "kling3_0", "mode": "std", "sound": "off", "duration": r['dur'], "aspect_ratio": "9:16", "medias": [{"role": "start_image", "value": r['start_image']}], "prompt": prompt}, "_name": name})
json.dump(out, open('/tmp/claude-0/-home-user-Shopify-test/f8ea1605-fce8-5041-aa20-559f14436348/scratchpad/kf2/clip_batch_v3.json', 'w'), indent=0)
print(len(out), 'requests;', sum(o['params']['duration'] for o in out), 'clip seconds')
