"""Montageplan voor de proefversie: een clip waar die er is en goed is, anders het startbeeld met een langzame inzoom.
python3 plan_gib_preview.py > plan_gib_preview.json"""
import json, os
CUTS = [('N01',0.00,3.00),('N02',3.00,5.60),('N03',5.60,8.30),('N04',8.30,10.50),('N05',10.50,12.90),('N06',12.90,15.40),('N07',15.40,18.20),('N08',18.20,20.60),
        ('N27',20.60,23.30),('N09',23.30,26.10),('N10',26.10,28.50),('N28',28.50,31.50),('N29',31.50,34.20),('N30',34.20,36.60),('N31',36.60,39.20),('N11',39.20,41.80),
        ('N12',41.80,44.70),('N13',44.70,47.20),('N14',47.20,49.90),('N15',49.90,52.10),('N16',52.10,54.50),('N17',54.50,57.40),('N18',57.40,60.40),('N19',60.40,63.20),
        ('N20',63.20,66.90),('N21',66.90,70.50),('N22',70.50,73.80),('N23',73.80,76.40),('N24',76.40,81.40),('N25',81.40,86.40),('N26',86.40,90.04)]
GOOD = {'N01','N03','N07','N08','N09','N10','N13','N17','N18','N19','N23','N27'}   # clips die gecontroleerd en goed zijn
ALT = {'N02': 'clipsG/N02s.mp4'}                                                     # N02: eerste 2 s vertraagd (ogen dicht), tot de herkansing er is
CARD = 82.9; shots = []; still = []
for k, t0, t1 in CUTS:
    if k in GOOD: src = {"clip": f"clipsG/{k}.mp4"}
    elif k in ALT: src = {"clip": ALT[k]}
    else: src = {"still": f"kfG/{k}.png", "zoom": [1.0, 1.05]}; still.append(k)
    if k == 'N25':
        shots.append(dict(src, t0=t0, t1=CARD))
        s2 = dict(src, t0=CARD, t1=t1, overlay="end_overlay.png", overlay_fade=0.5)
        if 'clip' in s2: s2['offset'] = round(CARD - t0, 3)
        else: s2['zoom'] = [1.015, 1.05]; shots[-1]['zoom'] = [1.0, 1.015]
        shots.append(s2)
    elif k == 'N26': shots.append(dict(src, t0=t0, t1=t1, overlay="end_overlay.png"))
    else: shots.append(dict(src, t0=t0, t1=t1))
for s in shots: assert os.path.exists(s.get('clip') or s.get('still')), s
json.dump({"audio": "song_N3.mp3", "words": "timeline_words_N3.json", "end_hold": True, "end_t": 90.04, "shots": shots, "stills": still}, open('plan_gib_preview.json', 'w'), indent=1)
print('shots', len(shots), 'stilstaand', len(still), still)
