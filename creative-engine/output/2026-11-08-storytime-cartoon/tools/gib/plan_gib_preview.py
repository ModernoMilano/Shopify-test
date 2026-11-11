"""Montageplan voor de proefversie: een clip waar die er is en goed is, anders het startbeeld met een langzame inzoom.
python3 plan_gib_preview.py > plan_gib_preview.json"""
import json, os
CUTS = [('N01',0.00,3.00),('N02',3.00,5.52),('N03',5.52,8.18),('N04',8.18,10.60),('N05',10.60,13.10),('N06',13.10,15.34),('N07',15.34,18.26),('N08',18.26,21.00),
        ('N27',21.00,23.53),('N09',23.53,26.27),('N10',26.27,28.55),('N28',28.55,31.55),('N29',31.55,34.29),('N30',34.29,36.90),('N31',36.90,39.50),('N11',39.50,42.05),
        ('N12',42.05,44.72),('N13',44.72,47.27),('N14',47.27,49.93),('N15',49.93,51.97),('N16',51.97,54.75),('N17',54.75,57.44),('N18',57.44,60.44),('N19',60.44,63.42),
        ('N20',63.42,67.00),('N21',67.00,70.42),('N22',70.42,74.00),('N23',74.00,77.00),('N24',77.00,80.70),('N25',80.70,83.50),('N26',83.50,90.04)]
GOOD = {'N01','N07','N10','N17','N18','N19','N23','N27'}   # clips die na de controle van de clips (wf_5edef9d6) bruikbaar zijn
ALT = {'N02': 'clipsG/N02s.mp4',   # N02: eerste 2 s vertraagd (ogen dicht blijven); de controleur vond dit goed genoeg om te houden
       'N13': 'clipsG/N13p.mp4'}   # N13: eerste 1,29 s vooruit en dan achteruit, zodat de twee vingers de hele regel omhoog blijven
# N03, N08 en N09 hebben een clip met een fout (losscheurende mouwen, lichtsprong, uitgerekt gezicht): hier stilstaand tot de herkansing
CROP = {'N07': 0.04}               # N07: onderste 4% wegsnijden (strookje broek in de verkeerde kleur)
CAP_Y = {'N30': 0.75}; shots = []; still = []
for k, t0, t1 in CUTS:
    if k in GOOD: src = {"clip": f"clipsG/{k}.mp4"}
    elif k in ALT: src = {"clip": ALT[k]}
    else: src = {"still": f"kfG/{k}.png", "zoom": [1.0, 1.05]}; still.append(k)
    sh = dict(src, t0=t0, t1=t1)
    if k in CAP_Y: sh['cap_y'] = CAP_Y[k]
    if k in CROP and 'clip' in sh: sh['crop_bottom'] = CROP[k]
    if k == 'N26': sh.update(overlay="end_card_mid.png", overlay_fade=0.6)
    shots.append(sh)
for s in shots: assert os.path.exists(s.get('clip') or s.get('still')), s
json.dump({"audio": "song_N3.mp3", "words": "timeline_words_N3.json", "cards": "cards_N3.json", "end_hold": True, "end_t": 90.04, "shots": shots, "stills": still}, open('plan_gib_preview.json', 'w'), indent=1)
print('shots', len(shots), 'stilstaand', len(still), still)
