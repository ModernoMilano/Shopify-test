"""Bouwt de JSON-bestanden voor het dashboard 'Productiekamer Una giornata'."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
J = lambda name, rows: json.dump(rows, open(os.path.join(D, name + ".json"), "w"), ensure_ascii=False, indent=1)
C = "https://d8j0ntlcm91z4.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/"

VIDEOS = [
 dict(video="lago", nr=1, titel="Il lago", product="MILANO NOBILE SET", moment="Late middag", plek="Comomeer bij Varenna, oude mahoniehouten motorboot",
      idee="Zwart cashmere op warm mahonie en goud water. De camera vaart naast de boot mee, daarna dichtbij op de boot zelf.",
      shot_a="4 s: de boot glijdt over het meer, de camera vaart mee", shot_b="5 s: dichtbij in profiel, camera vast op de boot, logo de laatste 2 s"),
 dict(video="pioggia", nr=2, titel="Pioggia", product="MILANO REVERSO SET TOTAL ANTRACITE", moment="Grijze ochtend", plek="Arcade van een rationalistisch gebouw in Milaan, regen op straat",
      idee="Grijs op grijs. De camera schuift van achter een zuil vandaan; bij de snede is het gilet omgekeerd naar lichtgrijs.",
      shot_a="4 s: camera schuift langs de zuil, hij kijkt naar de regen", shot_b="5 s: zelfde moment, gilet omgekeerd, vaste camera, logo"),
 dict(video="giardino", nr=3, titel="Giardino", product="MILANO REVERSO SET BLU & CREMA", moment="Late ochtend", plek="Tuin met lang zwembad van een villa uit de jaren dertig in Milaan",
      idee="Navy en crème bij travertin en water. Hij trekt de rits op; bij de snede is het gilet crème.",
      shot_a="4 s: hij trekt de rits op en steekt de hand in zijn zak", shot_b="5 s: zelfde moment, gilet omgekeerd, vaste camera, logo"),
 dict(video="sera", nr=4, titel="Sera", product="MILANO KNITTED TWO-TONE CASHMERE SET - DARK MOCHA", moment="Blauw uur", plek="Oud appartement in Milaan, leren fauteuil bij het raam",
      idee="Materiaal eerst: een macro van het breisel in lamplicht, daarna hij in de fauteuil met de stad achter het glas.",
      shot_a="4 s: macro van mouw en hand, zonder gezicht", shot_b="5 s: in de fauteuil bij het raam, vaste camera, logo"),
]
J("videos", VIDEOS)

B = []  # beelden
def b(id, video, wat, status, reden, door, credits, job=None, url=None, tijd=None, shot=""):
    B.append(dict(id=id, video=video, shot=shot, wat=wat, status=status, reden=reden, beoordeeld_door=door, credits=credits,
                  job=job or "", link=url or "", gemaakt=tijd or ""))
T1, T2, T3, T4, T5 = "2026-10-08T21:20:21Z", "2026-10-08T21:24:54Z", "2026-10-08T21:26:02Z", "2026-10-08T21:32:35Z", "2026-10-08T21:35:18Z"
u = lambda stamp, job: f"{C}hf_20261008_{stamp}_{job}.png"
b("como0", "lago", "Startbeeld A, variant 1", "afgekeurd", "Het zwarte gilet lijkt een jasje met lange mouwen.", "Kleding-controleur", 4, "7152bf4b-6462-4b20-835b-d1ec47238260", u("212021","7152bf4b-6462-4b20-835b-d1ec47238260"), T1, "A")
b("como1", "lago", "Startbeeld A, variant 2", "afgekeurd", "Zijn gezicht oogt ouder dan Luca.", "Regisseur", 4, "eb8997cb-13b7-4713-950b-1e1c8a8a6924", u("212021","eb8997cb-13b7-4713-950b-1e1c8a8a6924"), T1, "A")
b("como8", "lago", "Startbeeld A, variant 3", "afgekeurd", "Een klein merkteken met letters op het glas van de voorruit. Verder goed.", "Kleding- en Echtheid-controleur", 4, "afc686cd-de3f-4f7c-b870-c40490003b42", u("212454","afc686cd-de3f-4f7c-b870-c40490003b42"), T2, "A")
b("comoAcrop", "lago", "Startbeeld A, bijgesneden", "gekozen", "Variant 3 zonder de onderste 10%, dus zonder het merkteken.", "Kleding- en Echtheid-controleur", 0, "304515f9-5388-4a7b-a8c2-5f06eb77a44d", "https://d2ol7oe51mr4n9.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/304515f9-5388-4a7b-a8c2-5f06eb77a44d.png", "2026-10-08T21:34:05Z", "A")
b("comoB21", "lago", "Startbeeld B, close-up op de boot", "gekozen", "Zelfde licht en boot; de geribde armsgaten van het gilet zijn goed te zien.", "Kleding- en Echtheid-controleur", 4, "7292b98e-3543-489b-88e2-727ac10f9835", u("213235","7292b98e-3543-489b-88e2-727ac10f9835"), T4, "B")
b("antr2", "pioggia", "Startbeeld A, variant 1", "gekozen", "Lichtgrijs alleen in de kraag en langs de voorkant; zuil zacht op de voorgrond.", "Kleding- en Echtheid-controleur", 4, "6f98f485-59f7-4e29-a5a0-baf6c7789207", u("212021","6f98f485-59f7-4e29-a5a0-baf6c7789207"), T1, "A")
b("antr3", "pioggia", "Startbeeld A, variant 2", "goedgekeurd", "Ook goed; reserve.", "Kleding- en Echtheid-controleur", 4, "c5358423-f8d1-47a4-b3a0-ce8d842e84f1", u("212021","c5358423-f8d1-47a4-b3a0-ce8d842e84f1"), T1, "A")
b("blu4", "giardino", "Startbeeld A, variant 1", "goedgekeurd", "Ook goed; reserve.", "Kleding- en Echtheid-controleur", 4, "4c64fc86-58e0-42f7-a4c5-0f535a303a8e", u("212021","4c64fc86-58e0-42f7-a4c5-0f535a303a8e"), T1, "A")
b("blu5", "giardino", "Startbeeld A, variant 2", "gekozen", "Hij pakt het lipje van de rits echt vast; crème alleen in de kraag.", "Kleding- en Echtheid-controleur", 4, "b3851105-101c-41c6-9e16-ad4e5ad5abf2", u("212021","b3851105-101c-41c6-9e16-ad4e5ad5abf2"), T1, "A")
b("mocha6", "sera", "Startbeeld B, ronde 1", "afgekeurd", "De jas is grijs en de capuchon heeft koordjes die het product niet heeft.", "Regisseur", 4, "555e84b9-f50d-4c73-8ad1-91a7ab9e12d0", u("212021","555e84b9-f50d-4c73-8ad1-91a7ab9e12d0"), T1, "B")
b("mocha7", "sera", "Startbeeld B, ronde 1", "afgekeurd", "De jas is grijs en de capuchon heeft koordjes.", "Regisseur", 4, "2db76a0c-fb0d-428a-b088-fead84a70d17", u("212021","2db76a0c-fb0d-428a-b088-fead84a70d17"), T1, "B")
b("mocha9", "sera", "Startbeeld B, ronde 2", "afgekeurd", "Nog koordjes aan de capuchon. Oorzaak: een verkeerde productfoto (stapel in vier kleuren) als referentie.", "Regisseur", 4, "9b57c3c4-4141-46ad-a01c-9cc7270ad608", u("212454","9b57c3c4-4141-46ad-a01c-9cc7270ad608"), T2, "B")
b("mocha10", "sera", "Startbeeld B, ronde 2", "afgekeurd", "Koordjes aan de capuchon; zelfde verkeerde referentie.", "Regisseur", 4, "a1acfb21-7585-45e9-834c-2aadaf6b33a4", u("212454","a1acfb21-7585-45e9-834c-2aadaf6b33a4"), T2, "B")
b("mocha11", "sera", "Startbeeld B, ronde 3", "gekozen", "Juiste referenties: geen koordjes, strepen kloppen, Luca herkenbaar.", "Kleding- en Echtheid-controleur", 4, "7782c3c1-130a-4e08-8487-fe86a0713224", u("212602","7782c3c1-130a-4e08-8487-fe86a0713224"), T3, "B")
b("mocha12", "sera", "Startbeeld B, ronde 3", "afgekeurd", "Een koordje met metalen puntje aan de capuchon.", "Regisseur", 4, "67df7df0-4381-4eeb-9ca9-c94b20c3a1aa", u("212602","67df7df0-4381-4eeb-9ca9-c94b20c3a1aa"), T3, "B")
b("det30", "sera", "Startbeeld A, mouwdetail 1", "afgekeurd", "De broek mist de crème streep langs de zijkant van het bovenbeen.", "Kleding-controleur", 4, "8194a054-d122-4cfe-a01d-249f515257b2", u("213518","8194a054-d122-4cfe-a01d-249f515257b2"), T5, "A")
b("det31", "sera", "Startbeeld A, mouwdetail 2", "gekozen", "Breisel in strijklicht, twee crème strepen op de mouw, een natuurlijke hand.", "Kleding- en Echtheid-controleur", 4, "98e8323c-ebb0-4e04-82cc-1d0391ab05e7", u("213518","98e8323c-ebb0-4e04-82cc-1d0391ab05e7"), T5, "A")
b("ref1", "luca", "Luca, referentie 1", "referentie", "Het vaste gezicht waar elk beeld mee vergeleken wordt.", "", 0, "603d494f-d72d-4f7c-a2f6-c21d3b445030", C+"hf_20261008_130350_603d494f-d72d-4f7c-a2f6-c21d3b445030.png")
b("ref4", "luca", "Luca, referentie 4", "referentie", "Tweede vaste referentie van zijn gezicht.", "", 0, "0eda0253-6087-4aa8-8daa-2b5f2c6d3b51", C+"hf_20261008_130358_0eda0253-6087-4aa8-8daa-2b5f2c6d3b51.png")
S = "https://cdn.shopify.com/s/files/1/1009/1197/2689/files/"
b("p_nobile", "lago", "Productfoto Nobile Set", "productfoto", "Flat-lay uit de winkel: gilet, polo, broek, loafers.", "", 0, "", S+"ChatGPTImageAug22_2026_02_25_30PM.png?v=1787402069")
b("p_antr", "pioggia", "Productfoto Total Antracite", "productfoto", "Uit de winkel: gilet open, lichtgrijs aan de binnenkant.", "", 0, "", S+"74777dc3-7ce4-4fb1-bc85-739878e62324.png?v=1791398184")
b("p_blu", "giardino", "Productfoto Blu & Crema", "productfoto", "Uit de winkel: navy gilet met crème binnenkant.", "", 0, "", S+"f9cc26b6-128d-4daa-8dbb-9973ca7216a1.png?v=1791398240")
b("p_mocha", "sera", "Productfoto Dark Mocha", "productfoto", "Flat-lay uit de winkel met de witte tee eronder.", "", 0, "", S+"dark_mocha.png?v=1787091946")
b("p_mocha_j", "sera", "Productfoto Dark Mocha jas", "productfoto", "De jas gevouwen: crème rand om de capuchon, geen koordjes.", "", 0, "", S+"Scherm_afbeelding2026-02-13om16.45.40.png?v=1787671383")
J("beelden", B)

th = json.load(open(os.path.join(D, "thumbs.json")))
J("voorbeelden", [dict(id=k, src=v) for k, v in th.items()])

AGENTS = [
 dict(agent="Regisseur", wie="Claude, in deze chat", rol="Bedenkt de video's, schrijft de prompts, controleert zelf, snijdt bij en houdt de kosten bij.", status="bezig", volgorde=1),
 dict(agent="Beeldmaker", wie="Nano Banana Pro op Higgsfield", rol="Maakt de startbeelden in 4K, met Luca en de echte productfoto's als referentie.", status="klaar voor nu", volgorde=2),
 dict(agent="Kleding-controleur", wie="Claude-agent, één per beeld", rol="Legt elk beeld naast de productfoto's: kleur, kraag, rits, strepen, geen accessoires, jouw regels.", status="klaar voor nu", volgorde=3),
 dict(agent="Echtheid-controleur", wie="Claude-agent, één per beeld", rol="Kijkt of het Luca is en of het echt oogt: handen, huid, licht, geen tekst of AI-fouten.", status="klaar voor nu", volgorde=4),
 dict(agent="Prompt-nakijkers", wie="3 Claude-agents en een samenvatter", rol="Lezen de Seedance-prompts na op beweging, kleding en startbeeld, vóór er credits naar video gaan.", status="bezig", volgorde=5),
 dict(agent="Samenvatter", wie="Claude-agents", rol="Zet de bevindingen van de controleurs om in gewoon Nederlands voor dit dashboard.", status="bezig", volgorde=6),
 dict(agent="Eigenaar", wie="Jij", rol="Keurt de startbeelden goed; daarna pas gaan er credits naar video.", status="aan zet straks", volgorde=7),
 dict(agent="Videomaker", wie="Seedance 2.5 op Higgsfield", rol="Maakt van een goedgekeurd startbeeld een clip: eerst een concept in 480p, dan 1080p.", status="wacht", volgorde=8),
 dict(agent="Monteur", wie="ffmpeg in de Higgsfield-sandbox", rol="Zet de twee shots aan elkaar, legt de snede gelijk en zet je logo erop.", status="wacht", volgorde=9),
]
J("agents", AGENTS)

L = []
def l(tijd, agent, actie, video="", beeld=""): L.append(dict(nr=len(L)+1, tijd=tijd, agent=agent, actie=actie, video=video, beeld=beeld))
l("2026-10-08T21:20:21Z", "Beeldmaker", "Ronde 1: acht startbeelden in 4K, twee per video.", "", "")
l("2026-10-08T21:20:59Z", "Regisseur", "Draaiboek geschreven: vier momenten van één dag in Italië.", "", "")
l("2026-10-08T21:23:00Z", "Regisseur", "Eigen controle ronde 1: Mocha afgekeurd (grijs, koordjes), boot variant 2 afgekeurd (ouder gezicht).", "sera", "mocha6")
l("2026-10-08T21:24:54Z", "Beeldmaker", "Herkansing: Mocha twee keer opnieuw, boot één extra variant.", "lago", "como8")
l("2026-10-08T21:26:00Z", "Regisseur", "Eigen fout gevonden: de productfoto met vier kleuren ging mee als referentie. Gecorrigeerd.", "sera", "mocha9")
l("2026-10-08T21:26:02Z", "Beeldmaker", "Mocha opnieuw met de juiste productfoto's.", "sera", "mocha11")
l("2026-10-08T21:26:53Z", "Kleding-controleur", "Start controle van vijf beelden: boot, regen en zwembad.", "", "antr2")
l("2026-10-08T21:26:53Z", "Echtheid-controleur", "Start controle van dezelfde vijf beelden: is het Luca, oogt het echt.", "", "blu5")
l("2026-10-08T21:28:56Z", "Kleding-controleur", "Start controle van boot variant 3 en Mocha ronde 3.", "", "como8")
l("2026-10-08T21:29:06Z", "Regisseur", "Draaiboek en startbeeld-prompts opgeslagen in GitHub.", "", "")
l("2026-10-08T21:32:35Z", "Beeldmaker", "Close-up op de boot, als bewerking van variant 3. Eén poging mislukte, credits terug.", "lago", "comoB21")
l("2026-10-08T21:34:05Z", "Regisseur", "Boot variant 3 bijgesneden zonder het merkteken op de ruit en klaargezet voor Seedance.", "lago", "comoAcrop")
l("2026-10-08T21:34:35Z", "Echtheid-controleur", "Boot variant 3 afgekeurd om het merkteken; Mocha ronde 3 goedgekeurd.", "sera", "mocha11")
l("2026-10-08T21:35:18Z", "Beeldmaker", "Mouwdetail van Mocha, twee varianten.", "sera", "det31")
l("2026-10-08T21:37:25Z", "Kleding-controleur", "Start controle van de bijsnede, de close-up en de twee mouwdetails.", "lago", "comoAcrop")
l("2026-10-08T21:40:03Z", "Kleding-controleur", "Alle regen- en zwembadbeelden goed; boot variant 1 afgekeurd (gilet lijkt jasje).", "", "como0")
l("2026-10-08T21:40:53Z", "Prompt-nakijkers", "Start voorcontrole van de acht Seedance-prompts: beweging, kleding en startbeeld.", "", "")
l("2026-10-08T21:42:14Z", "Echtheid-controleur", "Bijsnede van de boot en close-up goed; mouwdetail 1 afgekeurd (broek zonder streep).", "sera", "det30")
l("2026-10-08T21:42:58Z", "Samenvatter", "Bevindingen van de controleurs naar gewoon Nederlands voor dit dashboard.", "", "")
l("2026-10-08T21:43:30Z", "Regisseur", "Dashboard gestart: voorbeeldbeelden gemaakt via de Higgsfield-sandbox.", "", "")
l("2026-10-08T21:45:52Z", "Echtheid-controleur", "Mouwdetail 2 goedgekeurd: alle acht startbeelden van de vier video's zijn nu goed.", "sera", "det31")
J("log", L)

K = [
 dict(nr=1, stap="Startbeelden ronde 1", soort="uitgegeven", credits=32),
 dict(nr=2, stap="Herkansing Mocha en boot", soort="uitgegeven", credits=12),
 dict(nr=3, stap="Mocha met juiste productfoto's", soort="uitgegeven", credits=8),
 dict(nr=4, stap="Close-up op de boot", soort="uitgegeven", credits=4),
 dict(nr=5, stap="Mouwdetail Mocha", soort="uitgegeven", credits=8),
 dict(nr=6, stap="Startbeeld B Antracite en Blu", soort="gepland", credits=8),
 dict(nr=7, stap="Concept-video's 480p", soort="gepland", credits=108),
 dict(nr=8, stap="Video's afmaken in 1080p", soort="gepland", credits=432),
]
J("kosten", K)
J("saldo", [dict(moment="Start van de serie", credits=653.55), dict(moment="Nu", credits=589.55)])

STEPS = ["Draaiboek", "Startbeelden", "Controle startbeelden", "Jouw akkoord", "Voorcontrole prompts", "Concept-video 480p", "Controle video", "Afmaken 1080p", "Snede en logo", "Oplevering"]
ST = {
 "lago": ["klaar", "klaar", "klaar", "wacht", "bezig", "wacht", "wacht", "wacht", "wacht", "wacht"],
 "pioggia": ["klaar", "klaar", "klaar", "wacht", "bezig", "wacht", "wacht", "wacht", "wacht", "wacht"],
 "giardino": ["klaar", "klaar", "klaar", "wacht", "bezig", "wacht", "wacht", "wacht", "wacht", "wacht"],
 "sera": ["klaar", "klaar", "klaar", "wacht", "bezig", "wacht", "wacht", "wacht", "wacht", "wacht"],
}
J("stappen", [dict(video=v, nr=i+1, stap=s, status=st[i]) for v, st in ST.items() for i, s in enumerate(STEPS)])
print("ok", len(B), len(L))
