import { existsSync } from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import modelJson from "../../creative-engine/data/model.json";
import wardrobeJson from "../../creative-engine/data/wardrobe.json";
import { fromWindsorRow, summarize } from "./competitors";
import { composeLooks, houseLook, lookFamilies, lookFromItems, validateLook } from "./looks";
import { productName, seasonTag } from "./captions";
import * as casting from "./casting";
import { MODEL, modelFrom } from "./casting";
import { CHAPTER, DEFAULT_DAYS, makePlan, MAX_FULL_BODY_SHARE, MAX_SAME_HERO, PERSON_FRAMES, type PlanEntry } from "./plan";
import { buildMotion, buildPrompt, FORBIDDEN, hasFilmWords, MAX_PRODUCT_REFS_WITH_MODEL, MAX_REFERENCES } from "./prompt";
import { judge, MAX_PASSERS_BY, QA_QUESTIONS, type Observation } from "./qa";
import { deriveShot, shotById, SHOTS } from "./shots";
import { seasonFor, splitTitle, toWardrobeItem, type ShopifyProductNode, type WardrobeItem } from "./wardrobe";

const wardrobe = wardrobeJson.items as unknown as WardrobeItem[];
const REPO = path.resolve(__dirname, "../..");
/** De gezichtsfoto's van de terugval: ref-1, ref-4, ref-2 in 4K (model.json → face_ref_order). */
const FALLBACK_IDS = ["ref-1", "ref-4", "ref-2"].map((id) => modelJson.higgsfield.face_refs.find((r) => r.file.endsWith(`/${id}.jpg`))!.upscale_job_id);
/** Een tweede of andere man in een shottekst of prompt (de vaste must_not-regel van het model niet meegerekend). */
const SECOND_MAN = /exactly two men|two men\b|\bmen\b|older man|younger man|second man|another man|his son|father|brothers?\b/i;
/** Een gezicht of haar dat niet het zijne is (model.json → must_not_en). */
const OTHER_FACE = /beard|moustache|mustache|goatee|grey hair|gray hair|silver|blond|bald|in his (forties|fifties|sixties)/i;
const own = (prompt: string) => prompt.replace(`For him: ${MODEL.mustNot.join("; ")}.`, "");
const img = (name: string) => ({ image: { url: `https://cdn.shopify.com/s/files/1/x/files/${name}?v=1` } });

const polo: ShopifyProductNode = {
  id: "gid://shopify/Product/1",
  title: "MILANO CASHMERE CORTINA POLO - NAVY",
  handle: "cortina-navy",
  description: "Crafted from a rich, high-quality cashmere knit",
  category: { fullName: "Apparel & Accessories > Clothing > Clothing Tops > Sweaters" },
  options: [{ name: "SIZE", values: ["S", "M"] }],
  priceRangeV2: { minVariantPrice: { amount: "120.0" } },
  media: { nodes: [img("navy_3_model.png"), img("navy_1_product.png"), img("navy_2_detail.png")] },
};

describe("garderobe", () => {
  it("splitst titel en kleur", () => {
    expect(splitTitle("MILANO SUEDE LOAFER - AVIO")).toEqual({ line: "MILANO SUEDE LOAFER", colour: "AVIO" });
    expect(splitTitle("MILANO REVERSO SABBIA SET")).toEqual({ line: "MILANO REVERSO SABBIA SET", colour: "SABBIA" });
  });

  it("deelt een cashmere polo in als top, ook als Shopify hem Sweaters noemt", () => {
    const item = toWardrobeItem(polo)!;
    expect(item.pieces).toEqual([{ slot: "top", kind: "knit-polo", label: "long-sleeve cashmere knit polo" }]);
    expect(item.family).toBe("navy");
    expect(item.season).toBe("fw");
    expect(item.images.primary).toContain("navy_1_product");
    expect(item.images.model).toContain("navy_3_model");
  });

  it("haalt de stukken van een bundel uit de opties", () => {
    const item = toWardrobeItem({
      ...polo,
      title: "MILANO AZZURRO SET",
      options: ["LOAFER", "SIGNATURE TROUSER", "BERGAMO POLO", "REVERSO GILET"].map((name) => ({ name, values: ["M"] })),
    })!;
    expect(item.isSet).toBe(true);
    expect(item.pieces.map((p) => `${p.slot}:${p.kind}`)).toEqual(["shoes:loafers", "bottom:trousers", "top:knit-polo", "outer:gilet"]);
    expect(item.family).toBe("blue");
  });

  it("leest een set met alleen maten uit de omschrijving", () => {
    const item = toWardrobeItem({ ...polo, title: "MILANO RIVIERA SET - NAVY", description: "this matching short-sleeve shirt and shorts set" })!;
    expect(item.pieces.map((p) => p.kind)).toEqual(["shirt", "shorts"]);
    expect(item.season).toBe("ss");
  });

  it("legt een tracksuit-bundel uit in vier lagen", () => {
    const item = toWardrobeItem({
      ...polo,
      title: "MILANO REVERSO TERRA SET",
      options: ["TRACKSUIT", "SHIRT", "REVERSIBLE BODYWARMER"].map((name) => ({ name, values: ["M"] })),
    })!;
    expect(item.pieces.map((p) => p.slot).sort()).toEqual(["bottom", "mid", "outer", "top"]);
  });

  it("vindt het palet van een bundel in de tekst", () => {
    const item = toWardrobeItem({ ...polo, title: "MILANO NOBILE SET", description: "four signature pieces in a sharp, monochrome black palette" })!;
    expect(item.family).toBe("black");
  });

  it("de echte garderobe bevat geen accessoires, alleen kleding en loafers", () => {
    const kinds = new Set(wardrobe.flatMap((w) => w.pieces.map((p) => p.kind)));
    for (const k of kinds) expect(["tee", "longsleeve", "polo", "knit-polo", "shirt", "zip-knit", "cardigan", "knit-gilet", "lounge-top", "gilet", "jacket", "blazer", "trousers", "joggers", "shorts", "loafers"]).toContain(k);
    expect(wardrobe.length).toBeGreaterThan(200);
  });

  it("kiest het seizoen op datum", () => {
    expect(seasonFor(new Date("2026-10-06"))).toBe("fw");
    expect(seasonFor(new Date("2026-06-01"))).toBe("ss");
  });
});

const byTitle = (t: string) => wardrobe.find((w) => w.title === t)!;

describe("looks", () => {
  it("keurt een look af met twee tops, zonder broek of met een onbekend product", () => {
    const tee = byTitle("PURO SUPIMA MERCER TEE - WHITE");
    const knit = byTitle("MILANO CASHMERE CORTINA POLO - NAVY");
    const fake = { ...tee, id: "999", title: "ANDER MERK T-SHIRT" };
    const issues = validateLook(lookFromItems([{ item: tee, as: ["top"] }, { item: knit, as: ["top"] }, { item: fake, as: ["mid"] }], null), wardrobe);
    const text = issues.map((i) => i.message).join(" | ");
    expect(text).toContain("precies één bovenstuk");
    expect(text).toContain("precies één broek");
    expect(text).toContain("ANDER MERK T-SHIRT staat niet");
  });

  it("weigert een stuk in een laag die het niet kan zijn", () => {
    const trousers = byTitle("MILANO CLASSICO PANTS - BEIGE");
    const issues = validateLook(lookFromItems([{ item: trousers, as: ["top"] }], null), wardrobe);
    expect(issues.some((i) => i.message.includes("kan niet als top"))).toBe(true);
  });

  it("elke samengestelde look is geldig, compleet en uit één palet", () => {
    for (const seed of [1, 2, 3, 4, 5]) {
      const looks = composeLooks(wardrobe, { season: "fw", count: 30, seed });
      expect(looks.length).toBeGreaterThanOrEqual(20);
      for (const look of looks) {
        expect(validateLook(look, wardrobe, "fw").filter((i) => i.level === "error")).toEqual([]);
        expect(look.hasShoes).toBe(true);
        expect(lookFamilies(look).length).toBeLessThanOrEqual(3);
        for (const { item } of look.items) expect(item.season).not.toBe("ss");
      }
    }
  });

  it("begint bij het anker dat je opgeeft", () => {
    const anchor = byTitle("MILANO CASHMERE TORINO BLAZER - PERLA");
    const [first] = composeLooks(wardrobe, { season: "fw", count: 1, anchors: [anchor.handle] });
    expect(first.items.map((x) => x.item.id)).toContain(anchor.id);
  });

  it("gebruikt een complete bundel met loafers als huislook", () => {
    const look = houseLook(byTitle("MILANO TERRA SET"))!;
    expect(look.source).toBe("house");
    expect(look.hasShoes).toBe(true);
    expect(validateLook(look, wardrobe).filter((i) => i.level === "error")).toEqual([]);
  });
});

describe("prompt", () => {
  const look = composeLooks(wardrobe, { season: "fw", count: 1, seed: 7 })[0];
  const studio = SHOTS.find((s) => s.id === "studio-full")!;

  it("noemt elk product, met alleen hun eigen foto's als referentie", () => {
    const req = buildPrompt(look, studio);
    const allowed = new Set(look.items.flatMap(({ item }) => item.images.all));
    for (const { item } of look.items) expect(req.prompt).toContain(item.title);
    for (const r of req.references.filter((x) => x.kind === "product")) expect(allowed.has(r.url)).toBe(true);
    expect(req.references.length).toBeLessThanOrEqual(MAX_REFERENCES);
    expect(req.prompt).toContain("ONLY the following ModernoMilano pieces");
    for (const f of FORBIDDEN) expect(req.prompt).toContain(f);
  });

  it("noemt bij een halflang beeld geen loafers en geen enkels", () => {
    const req = buildPrompt(look, SHOTS.find((s) => s.id === "milano-courtyard")!);
    expect(req.prompt).toContain("The feet are out of frame.");
    expect(req.prompt).not.toContain("bare ankles");
    expect(req.references.some((r) => r.label.includes("LOAFER"))).toBe(false);
  });

  it("houdt de voeten uit beeld als er geen loafers in de look zitten", () => {
    const noShoes = lookFromItems(look.items.filter((x) => !x.as.includes("shoes")), look.palette);
    expect(buildPrompt(noShoes, SHOTS.find((s) => s.id === "studio-full")!).prompt).toContain("keep the feet out of frame");
  });

  it("stuurt standaard alleen productfoto's mee: het element brengt zijn gezicht", () => {
    for (const shot of SHOTS.filter((s) => s.people === 1)) {
      const req = buildPrompt(look, shot, { wardrobe });
      expect(req.references.every((r) => r.kind === "product")).toBe(true);
      expect(req.references.length).toBeGreaterThan(0);
      expect(req.references.length).toBeLessThanOrEqual(MAX_PRODUCT_REFS_WITH_MODEL);
      expect(req.prompt).toContain(MODEL.elementPlaceholder);
      expect(req.prompt).not.toContain(MODEL.identity);
      expect(req.resolution).toBe("4k");
    }
  });

  it("zet in de terugval ref-1, ref-4 en ref-2 (4K) vooraan, nooit ref-3", () => {
    for (const shot of SHOTS.filter((s) => s.people === 1)) {
      const req = buildPrompt(look, shot, { wardrobe, faces: "refs" });
      const k = shot.framing === "detail" ? 1 : 3;
      expect(req.references.slice(0, k).map((r) => r.kind)).toEqual(Array(k).fill("face"));
      expect(req.references.slice(0, k).map((r) => r.mediaId)).toEqual(FALLBACK_IDS.slice(0, k));
      expect(req.references.slice(k).every((r) => r.kind === "product")).toBe(true);
      expect(req.references.some((r) => r.url.endsWith("ref-3.jpg"))).toBe(false);
      expect(req.references.length).toBeLessThanOrEqual(MAX_REFERENCES);
      expect(req.prompt).not.toContain(MODEL.elementPlaceholder);
    }
  });

  it("nummert de producten vanaf #1, en in de terugval na de gezichtsfoto's", () => {
    const req = buildPrompt(look, studio);
    expect(req.prompt).toContain("exactly as shown in reference image #1");
    expect(req.prompt).toContain(`The garment references (#1-#${req.references.length})`);
    expect(req.prompt).not.toContain("His reference image");
    const fallback = buildPrompt(look, studio, { faces: "refs" });
    expect(fallback.prompt).toContain("Subject: the man in reference images #1-#3, ");
    expect(fallback.prompt).toContain("His reference images are #1-#3");
    expect(fallback.prompt).toContain("exactly as shown in reference image #4");
    expect(fallback.prompt).toContain(`The garment references (#4-#${fallback.references.length})`);
    for (let n = 1; n <= 3; n++) expect(fallback.prompt).not.toMatch(new RegExp(`reference image #${n}\\b`));
    // Zonder persoon geen gezicht, en de producten beginnen bij #1.
    const flat = buildPrompt(look, shotById("look-flatlay"));
    expect(flat.references.every((r) => r.kind === "product")).toBe(true);
    expect(flat.prompt).toContain("exactly as shown in reference image #1");
    expect(flat.prompt).not.toContain(MODEL.elementPlaceholder);
    expect(flat.resolution).toBe("2k");
  });

  it("beperkt de productfoto's als het model in beeld is", () => {
    // Vier stukken met elk een hoofd-, model- en detailfoto: zonder grens zouden het er 8 zijn.
    const layered = lookFromItems(
      [
        { item: byTitle("MILANO CASHMERE TORINO BLAZER - NOTTE"), as: ["outer"] },
        { item: byTitle("MILANO CASHMERE BELLAGIO - BLUE"), as: ["mid"] },
        { item: byTitle("MILANO CASHMERE LIDO - NOTTE"), as: ["top"] },
        { item: byTitle("MILANO CASHMERE COMODO JOGGER - NAVY"), as: ["bottom"] },
      ],
      null,
    );
    for (const { item } of layered.items) expect([item.images.primary, item.images.model, item.images.detail].every(Boolean)).toBe(true);
    for (const faces of ["element", "refs"] as const) {
      const products = buildPrompt(layered, shotById("milano-courtyard"), { faces }).references.filter((r) => r.kind === "product");
      expect(products).toHaveLength(MAX_PRODUCT_REFS_WITH_MODEL);
      for (const { item } of layered.items) expect(products.filter((r) => r.label === item.title)).toHaveLength(1);
    }
    // Zonder persoon geen grens van 4: twee foto's per stuk.
    expect(buildPrompt(layered, shotById("look-flatlay")).references).toHaveLength(8);
  });

  it("beschrijft het model met element, realisme, licht en uitdrukking, maar niet zijn gezicht in woorden", () => {
    const courtyard = shotById("milano-courtyard");
    const req = buildPrompt(look, courtyard);
    expect(req.prompt).toContain(`Subject: ${MODEL.elementPlaceholder}. ${MODEL.keep} Pose: `);
    expect(req.prompt).not.toContain(MODEL.identity);
    expect(req.prompt).toContain(MODEL.realism);
    expect(req.prompt).toContain(courtyard.keyLight!);
    expect(req.prompt).toContain(`Framing: ${MODEL.framing}.`);
    expect(req.prompt).toContain(MODEL.expression);
    for (const rule of MODEL.mustNot) expect(req.prompt).toContain(rule);
    // Licht, uitsnede en uitdrukking vóór de kledingregels, en maar één lichtbeschrijving.
    const at = (text: string) => req.prompt.indexOf(text);
    for (const t of [courtyard.keyLight!, MODEL.framing, MODEL.expression]) expect(at(t)).toBeLessThan(at("He wears ONLY"));
    expect(req.prompt).not.toContain(`Light: ${courtyard.light}`);
    // Zonder eigen lichtbron het standaardlicht van het model.
    expect(buildPrompt(look, { ...courtyard, keyLight: undefined }).prompt).toContain(MODEL.light);
    // De studio en ten voeten uit krijgen geen framing_en (dat zegt "waist-up or three-quarter by default").
    const studioReq = buildPrompt(look, studio);
    expect(studioReq.prompt).toContain(studio.keyLight!);
    expect(studioReq.prompt).not.toContain(MODEL.light);
    expect(studioReq.prompt).not.toContain(MODEL.framing);
    expect(buildPrompt(look, shotById("landscape")).prompt).not.toContain(MODEL.framing);
    // Zonder persoon blijft het licht in de Setting-regel staan.
    expect(buildPrompt(look, shotById("hanger")).prompt).toContain(`Light: ${shotById("hanger").light}`);
    // Bij een detail is het gezicht uit beeld: wel het element, geen gezichtsbeschrijving of uitdrukking.
    const detail = buildPrompt(look, shotById("texture"));
    expect(detail.prompt).toContain(MODEL.elementPlaceholder);
    expect(detail.prompt).toContain("his face is out of frame");
    expect(detail.prompt).not.toContain(MODEL.identity);
    expect(detail.prompt).not.toContain(MODEL.expression);
  });

  it("gebruikt geen filmrol-woorden in de prompts", () => {
    for (const shot of SHOTS) {
      for (const faces of ["element", "refs"] as const) expect(hasFilmWords(buildPrompt(look, shot, { wardrobe, faces }).prompt)).toBe(false);
      expect(hasFilmWords(buildMotion(shot).prompt)).toBe(false);
    }
    for (const bad of ["like a quiet film photograph", "fine grain", "slight halation", "shot on 35mm film stock", "Fuji colours", "analogue look"]) {
      expect(hasFilmWords(bad)).toBe(true);
    }
    expect(hasFilmWords(MODEL.realism)).toBe(false); // "No film borders" mag
  });

  it("zet op een openbare plek verre voorbijgangers in de prompt, en elders niemand", () => {
    for (const shot of SHOTS) {
      const prompt = buildPrompt(look, shot, { wardrobe }).prompt;
      if (shot.publicPlace) {
        expect(prompt).toContain(MODEL.publicPlaces.slice(1));
        expect(prompt).toContain("any other person who is near, sharp or recognisable");
        expect(shot.setting).not.toMatch(/\bempty\b|nobody else|no other people/);
      } else {
        expect(prompt).not.toContain(MODEL.publicPlaces.slice(1));
        expect(prompt).toMatch(/, other people\./);
      }
    }
    expect(SHOTS.filter((s) => s.publicPlace).map((s) => s.id).sort()).toEqual(["borgo", "espresso-terrace", "loafer-walk", "milano-courtyard", "riviera"]);
  });

  it("maakt reels alleen met Seedance 2.5 vanaf het goedgekeurde beeld, eerst als concept", () => {
    const v = buildMotion(shotById("milano-courtyard"));
    expect(v).toMatchObject({
      model: "seedance_2_5", mode: "omni_reference", startFrame: "approved-still", aspect: "9:16",
      resolution: "1080p", bitrate: "high", duration: 5, audio: false, draftFirst: true,
    });
    expect(v.prompt).toContain("Start from the approved still");
    expect(v.prompt).toContain("exactly the same man");
    // Seedance 2.5 negeert het element: zijn gezicht komt uit het startbeeld en de gezichtsfoto's.
    expect(v.prompt).not.toContain(MODEL.elementPlaceholder);
    expect(v.faceRefs.map((r) => r.id)).toEqual(["ref-1", "ref-4"]);
    expect(v.prompt).toContain("no head turn of more than 45 degrees");
    expect(v.prompt).toContain("no new people");
    const still = buildMotion(shotById("hanger"));
    expect(still.faceRefs).toEqual([]);
    expect(still.prompt).not.toContain("reference images");
  });

  it("vraagt bij een reel van een detail niet om zijn gezicht", () => {
    const v = buildMotion(shotById("loafer-walk"));
    expect(v.faceRefs).toEqual([]);
    expect(v.prompt).toContain("His face stays out of frame for the whole shot");
    expect(v.prompt).toContain("the camera does not tilt up");
    expect(v.prompt).not.toContain("same face");
  });
});

describe("kwaliteitscontrole", () => {
  const look = houseLook(byTitle("MILANO TERRA SET"))!;
  const shot = SHOTS.find((s) => s.id === "studio-full")!;
  const ok: Observation = {
    garments: ["brown hooded jacket", "brown knit polo", "beige trousers", "suede loafers"],
    matches: { "MILANO TERRA SET": true },
    accessories: [],
    logosOrText: false,
    people: 1,
    feetVisible: true,
    socksVisible: false,
    clean: true,
    anatomyOk: true,
    faceVisible: true,
    sameModel: true,
    faceWidthPx: MODEL.faceMinPx + 100,
  };

  it("keurt een schoon beeld goed", () => {
    expect(judge(look, shot, ok)).toEqual({ approved: true, reasons: [] });
  });

  it("keurt af bij een horloge, sokken of een extra kledingstuk", () => {
    const v = judge(look, shot, { ...ok, accessories: ["watch"], socksVisible: true, garments: [...ok.garments, "white scarf"] });
    expect(v.approved).toBe(false);
    expect(v.reasons.join(" ")).toMatch(/watch.*|sokken/);
    expect(v.reasons).toHaveLength(3);
  });

  it("keurt af als een product niet op de referentie lijkt", () => {
    expect(judge(look, shot, { ...ok, matches: { "MILANO TERRA SET": false } }).approved).toBe(false);
  });

  it("keurt af als het niet dezelfde man is als het model", () => {
    const v = judge(look, shot, { ...ok, sameModel: false });
    expect(v.approved).toBe(false);
    expect(v.reasons).toEqual(["niet dezelfde man als op de referentiefoto's (brand/assets/model)"]);
  });

  it("keurt twee mannen, een te klein gezicht of een nepfoto af", () => {
    expect(judge(look, shot, { ...ok, people: 2 }).approved).toBe(false);
    expect(judge(look, shot, { ...ok, faceWidthPx: MODEL.faceMinPx - 1 }).approved).toBe(false);
    expect(judge(look, shot, { ...ok, faceWidthPx: MODEL.faceMinPx }).approved).toBe(true);
    expect(judge(look, shot, { ...ok, realPhoto: false }).approved).toBe(false);
  });

  it("laat een beeld zonder zichtbaar gezicht toe (sameModel null)", () => {
    const noFace = { ...ok, faceVisible: false, sameModel: null, faceWidthPx: undefined };
    expect(judge(look, shotById("texture"), { ...noFace, feetVisible: false }).approved).toBe(true);
    // Van achteren in een wijd beeld: geen gezicht om te vergelijken of te meten.
    expect(judge(look, shotById("landscape"), noFace).approved).toBe(true);
  });

  it("keurt af als zijn gezicht in beeld is maar niet beoordeeld of gemeten", () => {
    const unjudged = judge(look, shot, { ...ok, sameModel: null });
    expect(unjudged.approved).toBe(false);
    expect(unjudged.reasons).toEqual(["zijn gezicht is in beeld, maar niet naast de referentiefoto's gelegd"]);
    expect(judge(look, shotById("bw-portrait"), { ...ok, feetVisible: false, sameModel: null }).approved).toBe(false);
    const unmeasured = judge(look, shot, { ...ok, faceWidthPx: undefined });
    expect(unmeasured.reasons).toEqual(["breedte van zijn gezicht niet gemeten"]);
  });

  it("staat verre voorbijgangers alleen toe op een openbare plek, hooguit 3", () => {
    const courtyard = shotById("milano-courtyard");
    expect(judge(look, courtyard, { ...ok, passersBy: 2 }).approved).toBe(true);
    expect(judge(look, courtyard, { ...ok, passersBy: MAX_PASSERS_BY + 1 }).approved).toBe(false);
    expect(judge(look, shot, { ...ok, passersBy: 1 }).approved).toBe(false);
    // Een tweede scherpe, herkenbare persoon is nooit een voorbijganger.
    expect(judge(look, courtyard, { ...ok, people: 2 }).approved).toBe(false);
  });

  it("vraagt bij elk beeld of het dezelfde man is en hoe breed zijn gezicht is", () => {
    expect(QA_QUESTIONS.some((q) => q.includes("is dit dezelfde man als in brand/assets/model?"))).toBe(true);
    expect(QA_QUESTIONS.some((q) => q.includes("faceVisible") && q.includes("sameModel null"))).toBe(true);
    expect(QA_QUESTIONS.some((q) => q.includes("in pixels (faceWidthPx)"))).toBe(true);
    expect(QA_QUESTIONS.some((q) => q.includes("passersBy"))).toBe(true);
  });
});

describe("concurrenten", () => {
  const rows = [
    { username: "loropiana", timestamp: "2026-09-01T10:00:00Z", media_type: "IMAGE", caption: "Quiet #LoroPiana #cashmere", like_count: 1000, comments_count: 20, followers_count: 100000 },
    { username: "loropiana", timestamp: "2026-09-08T10:00:00Z", media_type: "CAROUSEL_ALBUM", caption: "#cashmere", like_count: 3000, comments_count: 50 },
    { username: "loropiana", timestamp: "2026-09-15T10:00:00Z", media_type: "VIDEO", caption: "", like_count: 500, comments_count: 5 },
    { foo: "geen account" },
  ];

  it("zet Windsor-rijen om en slaat onbruikbare rijen over", () => {
    const posts = rows.map(fromWindsorRow);
    expect(posts[3]).toBeNull();
    expect(posts[1]).toMatchObject({ account: "loropiana", type: "carousel", likes: 3000 });
  });

  it("vat per account samen wat werkt", () => {
    const [s] = summarize(rows.map(fromWindsorRow).filter((p) => p !== null));
    expect(s.posts).toBe(3);
    expect(s.mix).toEqual({ image: 1, carousel: 1, video: 1 });
    expect(s.postsPerWeek).toBe(1.5);
    expect(s.bestType).toBe("carousel");
    expect(s.topHashtags[0]).toBe("#cashmere");
    expect(s.engagementRate).toBe(1.53); // (1020 + 3050 + 505) / 3 = 1525 op 100k volgers
  });
});

describe("contentplan", () => {
  const plan = makePlan(wardrobe, { start: new Date("2026-10-11"), posts: 18, seed: 2 });
  const chapter = plan.slice(0, 9);

  it("post op zondag, maandag, woensdag en vrijdag", () => {
    expect(plan).toHaveLength(18);
    for (const e of plan) expect(DEFAULT_DAYS).toContain(new Date(e.date).getUTCDay());
  });

  it("heeft per hoofdstuk 4 carrousels, 3 reels en 2 losse beelden", () => {
    const count = (f: string) => chapter.filter((e) => e.format === f).length;
    expect([count("carousel"), count("reel"), count("single")]).toEqual([4, 3, 2]);
    for (const e of chapter.filter((x) => x.format === "carousel")) expect(e.frames.length).toBeGreaterThanOrEqual(3);
  });

  it("maakt reels in 9:16 met een beweging vanaf het goedgekeurde beeld", () => {
    for (const e of plan.filter((x) => x.format === "reel")) {
      expect(e.frames[0].request.aspect).toBe("9:16");
      expect(e.video).toMatchObject({ model: "seedance_2_5", mode: "omni_reference", startFrame: "approved-still", aspect: "9:16", audio: false, draftFirst: true });
    }
  });

  it("volgt de rasterregels: hooguit één studio-hoofdbeeld, nooit hetzelfde naast elkaar, hooguit twee keer hetzelfde", () => {
    for (const part of [plan.slice(0, 9), plan.slice(9, 18)]) {
      const heroes = part.map((e) => e.frames[0].shot.id);
      expect(heroes.filter((h) => h.startsWith("studio")).length).toBeLessThanOrEqual(1);
      heroes.forEach((h, i) => i > 0 && expect(h).not.toBe(heroes[i - 1]));
      for (const h of heroes) expect(heroes.filter((x) => x === h).length).toBeLessThanOrEqual(MAX_SAME_HERO);
    }
  });

  it("gebruikt full-body shots alleen voor looks met loafers", () => {
    for (const e of plan) for (const f of e.frames) if (f.shot.framing === "full-body") expect(e.look.hasShoes).toBe(true);
  });

  it("toont hem hooguit 2 op de 10 beelden ten voeten uit", () => {
    const share = (p: PlanEntry[]) => {
      const person = p.flatMap((e) => e.frames).filter((f) => f.shot.people === 1);
      return person.filter((f) => f.shot.framing === "full-body").length / person.length;
    };
    for (const start of ["2026-10-11", "2026-05-03"]) {
      for (const seed of [1, 2, 3, 5]) {
        for (const posts of [2, 9, 18, 27]) expect(share(makePlan(wardrobe, { start: new Date(start), posts, seed }))).toBeLessThanOrEqual(0.2);
      }
    }
    expect(MAX_FULL_BODY_SHARE).toBe(0.2);
    // De studioslide van de productcarrousel gaat voor: in een heel hoofdstuk staat hij ten voeten uit.
    expect(plan.filter((e) => e.frames[0].shot.id === "studio-full").length).toBeGreaterThan(0);
    for (const e of plan) {
      if (e.pillar === "styling" && e.format === "carousel") expect(e.frames.map((f) => f.shot.id)).toContain("studio-portrait");
    }
  });

  it("rekent het quotum met het echte aantal beelden met hem per post", () => {
    plan.forEach((e, i) => expect(e.frames.filter((f) => f.shot.people === 1).length).toBe(PERSON_FRAMES[CHAPTER[i % CHAPTER.length].kind]));
  });

  it("stuurt alleen foto's van eigen producten mee, en alleen van wat in beeld komt", () => {
    for (const e of plan) {
      for (const f of e.frames) {
        const allowed = new Set(e.look.items.flatMap(({ item }) => wardrobe.filter((w) => w.line === item.line).flatMap((w) => w.images.all)));
        const products = f.request.references.filter((x) => x.kind === "product");
        for (const r of products) expect(allowed.has(r.url)).toBe(true);
        expect(f.request.references.length).toBeLessThanOrEqual(MAX_REFERENCES);
        if (f.shot.people === 1) {
          // Hoogstens 4; alleen een look van 5 stukken krijgt er 5, één per stuk.
          const pieces = new Set(products.map((r) => r.label)).size;
          expect(products.length).toBeLessThanOrEqual(Math.max(MAX_PRODUCT_REFS_WITH_MODEL, pieces));
          if (pieces > MAX_PRODUCT_REFS_WITH_MODEL) expect(products.length).toBe(pieces);
        }
      }
    }
  });

  it("zet in elk beeld en elke reel alleen het vaste model, nooit een tweede man", () => {
    for (const e of plan) {
      expect(e).not.toHaveProperty("secondLook");
      for (const f of e.frames) {
        expect(f.request.references.every((r) => r.kind === "product")).toBe(true);
        expect(f.request.prompt.includes(MODEL.elementPlaceholder)).toBe(f.shot.people === 1);
        expect(f.request.prompt).not.toContain(MODEL.identity);
        expect(own(f.request.prompt)).not.toMatch(SECOND_MAN);
        expect(hasFilmWords(f.request.prompt)).toBe(false);
      }
      if (e.video) {
        expect(e.video.prompt).not.toMatch(SECOND_MAN);
        // Seedance 2.5 negeert het element; zijn gezicht komt uit het startbeeld en, als het in beeld is, de gezichtsfoto's.
        expect(e.video.prompt).not.toContain(MODEL.elementPlaceholder);
        const face = e.frames[0].shot.people === 1 && e.frames[0].shot.framing !== "detail";
        expect(e.video.faceRefs.length > 0).toBe(face);
        if (e.frames[0].shot.people === 1) expect(e.video.prompt).toMatch(/same man|His face stays out of frame/);
      }
    }
  });

  it("zet in de terugval zijn gezichtsfoto's vooraan in elk beeld met hem", () => {
    for (const e of makePlan(wardrobe, { start: new Date("2026-10-11"), posts: 9, seed: 2, faces: "refs" })) {
      for (const f of e.frames) {
        const faces = f.request.references.filter((r) => r.kind === "face").map((r) => r.mediaId);
        expect(faces).toEqual(f.shot.people === 0 ? [] : FALLBACK_IDS.slice(0, f.shot.framing === "detail" ? 1 : 3));
        expect(f.request.references.slice(0, faces.length).every((r) => r.kind === "face")).toBe(true);
      }
    }
  });

  it("heeft een captionopzet met productregel en hooguit 4 hashtags", () => {
    for (const e of plan) {
      expect(e.caption.wearing.startsWith("Wearing: ")).toBe(true);
      expect(e.caption.hashtags[0]).toBe("#ModernoMilano");
      expect(e.caption.hashtags.length).toBeLessThanOrEqual(4);
    }
  });
});

describe("shots en prompts volgens de norm", () => {
  const look = composeLooks(wardrobe, { season: "fw", count: 2, seed: 4 });

  it("maakt zwart-wit portretten en gedempte locatiebeelden", () => {
    expect(buildPrompt(look[0], shotById("bw-portrait")).prompt).toContain("Black-and-white");
    expect(buildPrompt(look[0], shotById("volcanic-coast")).prompt).toContain("desaturated");
  });

  it("toont bij een schets en een hanger alleen het hoofdstuk", () => {
    const sketch = buildPrompt(look[0], shotById("sketch"));
    expect(sketch.prompt).toContain("pencil fashion sketch");
    expect(sketch.prompt).toContain(look[0].items[0].item.title);
    for (const { item } of look[0].items.slice(1)) expect(sketch.prompt).not.toContain(item.title);
    expect(buildPrompt(look[0], shotById("hanger")).prompt).not.toContain("no hanger");
  });

  it("stapelt alle kleuren van hetzelfde stuk", () => {
    const anchor = byTitle("MILANO CASHMERE CORTINA POLO - NAVY");
    const l = lookFromItems([{ item: anchor, as: ["top"] }], null);
    const req = buildPrompt(l, shotById("folded-stack"), { wardrobe });
    const titles = new Set(req.references.map((r) => r.label));
    expect(titles.size).toBeGreaterThan(1);
    for (const t of titles) expect(t.startsWith("MILANO CASHMERE CORTINA POLO")).toBe(true);
  });

  it("heeft geen shot met twee mannen, ook niet in het hoofdstukschema", () => {
    expect(SHOTS.every((s) => s.people === 0 || s.people === 1)).toBe(true);
    expect(SHOTS.some((s) => s.id === "two-generations")).toBe(false);
    for (const slot of CHAPTER) for (const season of ["fw", "ss"] as const) expect(slot.heroes(season)).not.toContain("two-generations");
    for (const s of SHOTS) {
      const text = `${s.setting} ${s.pose} ${s.motion} ${s.camera} ${s.light} ${s.keyLight ?? ""}`;
      expect(text).not.toMatch(SECOND_MAN);
      expect(text).not.toMatch(OTHER_FACE);
      expect(text).not.toMatch(/\bcentred\b|towards? the camera/i);
    }
    for (const s of SHOTS) expect(own(buildPrompt(look[0], s, { wardrobe }).prompt)).not.toMatch(SECOND_MAN);
  });

  it("verbiedt merktekens op auto's en boten, koptelefoons en tassen", () => {
    for (const f of ["car or boat badges, emblems or brand names", "readable number plates", "headphones", "holdall", "women"]) expect(FORBIDDEN).toContain(f);
    expect(FORBIDDEN).not.toContain("cars");
  });

  it("een afgeleid carrouselbeeld houdt plek en licht maar kadert anders", () => {
    const d = deriveShot(shotById("milano-courtyard"), "detail");
    expect(d.setting).toBe(shotById("milano-courtyard").setting);
    expect(d.framing).toBe("detail");
    expect(d.subject).toBe("anchor");
  });
});

describe("captions en het vaste model", () => {
  it("schrijft productnamen zoals in de winkel", () => {
    expect(productName("MILANO CASHMERE TORINO BLAZER - TORTORA")).toBe("Milano Cashmere Torino Blazer in Tortora");
    expect(productName("MILANO REVERSO SABBIA SET")).toBe("Milano Reverso Sabbia Set");
  });

  it("geeft de juiste seizoenstag", () => {
    expect(seasonTag("2026-10-11")).toBe("#ModernoMilanoFW26");
    expect(seasonTag("2027-02-01")).toBe("#ModernoMilanoFW26");
    expect(seasonTag("2027-05-01")).toBe("#ModernoMilanoSS27");
  });

  it("heeft precies één model, uit model.json", () => {
    expect(Object.keys(casting).sort()).toEqual(["MODEL", "modelFrom"]);
    expect(MODEL.id).toBe(modelJson.id);
    expect(MODEL.identity).toBe(modelJson.prompt.identity_en);
    expect(MODEL.identity).toMatch(/\bman\b/);
    expect(MODEL.keep).toContain("does not resemble any actor or public figure");
    expect(MODEL.elementPlaceholder).toBe(`<<<${MODEL.elementId}>>>`);
    expect(MODEL.soulId).toBe(modelJson.higgsfield.soul_id);
    expect(MODEL.faceRefs.length).toBeGreaterThan(0);
    for (const r of MODEL.faceRefs) {
      expect(existsSync(path.join(REPO, r.file))).toBe(true);
      expect(r.mediaId).toMatch(/^[0-9a-f-]{36}$/);
      expect(r.upscaleJobId).toMatch(/^[0-9a-f-]{36}$/);
    }
    expect(MODEL.fallbackFaceRefs.map((r) => r.id)).toEqual(["ref-1", "ref-4", "ref-2"]);
    expect(MODEL.fallbackFaceRefs.map((r) => r.upscaleJobId)).toEqual(FALLBACK_IDS);
    expect(MODEL.mustNot.join(" ")).toContain("never a second man who is near, sharp or recognisable");
  });

  it("stopt als er iets van het model ontbreekt", () => {
    const broken = JSON.parse(JSON.stringify(modelJson));
    broken.higgsfield.face_refs[0].media_id = "";
    expect(() => modelFrom(broken)).toThrow(/face_refs\[0\]\.media_id/);
    expect(() => modelFrom({ ...modelJson, prompt: { ...modelJson.prompt, identity_en: undefined } })).toThrow(/identity_en/);
    expect(() => modelFrom({ ...modelJson, higgsfield: { ...modelJson.higgsfield, element_placeholder: "<<<x>>>" } })).toThrow(/element_placeholder/);
    expect(() => modelFrom({ ...modelJson, higgsfield: { ...modelJson.higgsfield, face_ref_order: ["ref-9"] } })).toThrow(/ref-9/);
  });
});
