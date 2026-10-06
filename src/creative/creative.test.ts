import { describe, expect, it } from "vitest";
import wardrobeJson from "../../creative-engine/data/wardrobe.json";
import { fromWindsorRow, summarize } from "./competitors";
import { composeLooks, houseLook, lookFamilies, lookFromItems, validateLook } from "./looks";
import { productName, seasonTag } from "./captions";
import { castFor, FACES } from "./casting";
import { DEFAULT_DAYS, makePlan, MAX_SAME_HERO } from "./plan";
import { buildPrompt, FORBIDDEN } from "./prompt";
import { judge, type Observation } from "./qa";
import { deriveShot, shotById, SHOTS } from "./shots";
import { seasonFor, splitTitle, toWardrobeItem, type ShopifyProductNode, type WardrobeItem } from "./wardrobe";

const wardrobe = wardrobeJson.items as unknown as WardrobeItem[];
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
    for (const r of req.references) expect(allowed.has(r.url)).toBe(true);
    expect(req.references.length).toBeLessThanOrEqual(14);
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
      expect(e.video).toMatchObject({ model: "kling3_0", startFrame: "approved-still", aspect: "9:16", sound: "off" });
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

  it("stuurt alleen foto's van eigen producten mee, en alleen van wat in beeld komt", () => {
    for (const e of plan) {
      for (const f of e.frames) {
        const allowed = new Set(
          [e.look, e.secondLook]
            .filter(Boolean)
            .flatMap((l) => l!.items.flatMap(({ item }) => wardrobe.filter((w) => w.line === item.line).flatMap((w) => w.images.all))),
        );
        for (const r of f.request.references) expect(allowed.has(r.url)).toBe(true);
        expect(f.request.references.length).toBeLessThanOrEqual(14);
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

  it("kleedt bij twee generaties beide mannen alleen in eigen looks", () => {
    const req = buildPrompt(look[0], shotById("two-generations"), { second: { look: look[1], casting: "a younger man" } });
    expect(req.prompt).toContain("exactly two men");
    for (const l of look) for (const { item } of l.items) expect(req.prompt).toContain(item.title);
  });

  it("verbiedt ook auto's, boten, koptelefoons en tassen", () => {
    for (const f of ["cars", "boats", "headphones", "holdall", "women"]) expect(FORBIDDEN).toContain(f);
  });

  it("een afgeleid carrouselbeeld houdt plek en licht maar kadert anders", () => {
    const d = deriveShot(shotById("milano-courtyard"), "detail");
    expect(d.setting).toBe(shotById("milano-courtyard").setting);
    expect(d.framing).toBe("detail");
    expect(d.subject).toBe("anchor");
  });
});

describe("captions en casting", () => {
  it("schrijft productnamen zoals in de winkel", () => {
    expect(productName("MILANO CASHMERE TORINO BLAZER - TORTORA")).toBe("Milano Cashmere Torino Blazer in Tortora");
    expect(productName("MILANO REVERSO SABBIA SET")).toBe("Milano Reverso Sabbia Set");
  });

  it("geeft de juiste seizoenstag", () => {
    expect(seasonTag("2026-10-11")).toBe("#ModernoMilanoFW26");
    expect(seasonTag("2027-02-01")).toBe("#ModernoMilanoFW26");
    expect(seasonTag("2027-05-01")).toBe("#ModernoMilanoSS27");
  });

  it("kiest per seed een vaste cast, alleen mannen", () => {
    expect(castFor(3)).toEqual(castFor(3));
    expect(castFor(1, { main: "<<<abc>>>" }).main.description).toBe("<<<abc>>>");
    for (const f of FACES) expect(f.description).toMatch(/\bman\b/);
  });
});
