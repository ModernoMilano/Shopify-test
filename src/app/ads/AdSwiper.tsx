"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { Ad, AdCollection } from "./types";

type Decision = "yes" | "no";
type Saved = { decisions: Record<string, Decision>; edits: Record<string, Partial<Pick<Ad, "primaryText" | "headline" | "description">>> };

const STORE_KEY = "mm-ads-swipe-v1";
const COLLECTIONS: ("Alle" | AdCollection)[] = ["Alle", "Cashmere", "Reverso", "Bundle & Save", "Other"];
const PLACEMENTS = ["Alle", "Feed", "Stories/Reels"] as const;

const ANGLE_NL: Record<string, string> = {
  "two-in-one": "Twee in één",
  "quiet-luxury": "Quiet luxury",
  "price-vs-quality": "Prijs vs kwaliteit",
  "complete-look": "Complete look",
  "bundle-value": "Bundle-voordeel",
  softness: "Zachtheid",
  occasion: "Moment",
  season: "Seizoen",
  detail: "Detail",
  "social-proof": "Social proof",
  "risk-free": "Zonder risico",
  identity: "Identiteit",
  gift: "Cadeau",
  "new-drop": "Nieuwe drop",
};
const angleLabel = (a: string) => ANGLE_NL[a] ?? a;
const CTA_LABEL: Record<string, string> = { SHOP_NOW: "Shop now", LEARN_MORE: "Learn more", ORDER_NOW: "Order now", GET_OFFER: "Get offer" };
const SWIPE_AT = 110;

function load(): Saved {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    if (raw) {
      const s = JSON.parse(raw) as Saved;
      return { decisions: s.decisions ?? {}, edits: s.edits ?? {} };
    }
  } catch {}
  return { decisions: {}, edits: {} };
}

async function copy(text: string) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    return false;
  }
}

function csvCell(v: string) {
  return `"${v.replace(/"/g, '""')}"`;
}

export function AdSwiper({ ads }: { ads: Ad[] }) {
  const [saved, setSaved] = useState<Saved>({ decisions: {}, edits: {} });
  const [loaded, setLoaded] = useState(false);
  const [history, setHistory] = useState<string[]>([]);
  const [collection, setCollection] = useState<(typeof COLLECTIONS)[number]>("Alle");
  const [placement, setPlacement] = useState<(typeof PLACEMENTS)[number]>("Alle");
  const [view, setView] = useState<"swipe" | "gekozen">("swipe");
  const [toast, setToast] = useState("");

  useEffect(() => {
    setSaved(load());
    setLoaded(true);
  }, []);
  useEffect(() => {
    if (!loaded) return;
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify(saved));
    } catch {}
  }, [saved, loaded]);
  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(""), 1600);
    return () => clearTimeout(t);
  }, [toast]);

  const withEdits = useCallback((ad: Ad): Ad => ({ ...ad, ...saved.edits[ad.id] }), [saved.edits]);

  const filtered = useMemo(
    () => ads.filter((a) => (collection === "Alle" || a.collection === collection) && (placement === "Alle" || a.placement === placement)),
    [ads, collection, placement],
  );
  const queue = useMemo(() => filtered.filter((a) => !saved.decisions[a.id]), [filtered, saved.decisions]);
  const approved = useMemo(() => ads.filter((a) => saved.decisions[a.id] === "yes").map(withEdits), [ads, saved.decisions, withEdits]);
  const skipped = useMemo(() => ads.filter((a) => saved.decisions[a.id] === "no").length, [ads, saved.decisions]);
  const current = queue[0] ? withEdits(queue[0]) : undefined;
  const next = queue[1];

  const decide = useCallback(
    (id: string, d: Decision) => {
      setSaved((s) => ({ ...s, decisions: { ...s.decisions, [id]: d } }));
      setHistory((h) => [...h, id]);
    },
    [],
  );
  const undo = useCallback(() => {
    setHistory((h) => {
      const id = h[h.length - 1];
      if (!id) return h;
      setSaved((s) => {
        const decisions = { ...s.decisions };
        delete decisions[id];
        return { ...s, decisions };
      });
      return h.slice(0, -1);
    });
  }, []);
  const reopen = (id: string) =>
    setSaved((s) => {
      const decisions = { ...s.decisions };
      delete decisions[id];
      return { ...s, decisions };
    });
  const edit = (id: string, patch: Partial<Pick<Ad, "primaryText" | "headline" | "description">>) =>
    setSaved((s) => ({ ...s, edits: { ...s.edits, [id]: { ...s.edits[id], ...patch } } }));

  useEffect(() => {
    if (view !== "swipe") return;
    const onKey = (e: KeyboardEvent) => {
      const el = e.target as HTMLElement;
      if (el.closest("textarea, input, select")) return;
      if (e.key === "ArrowRight" && current) decide(current.id, "yes");
      else if (e.key === "ArrowLeft" && current) decide(current.id, "no");
      else if (e.key === "Backspace" || e.key.toLowerCase() === "z") undo();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [view, current, decide, undo]);

  // Volgende beeld alvast laden zodat swipen niet hapert
  useEffect(() => {
    if (!next) return;
    const img = new Image();
    img.src = next.image;
  }, [next]);

  const exportCsv = () => {
    const head = ["image_url", "collection", "product", "price", "angle", "hook_type", "placement", "primary_text", "headline", "description", "cta"];
    const rows = approved.map((a) =>
      [a.image, a.collection, a.product, a.price, a.angle, a.hookType, a.placement, a.primaryText, a.headline, a.description, a.cta].map(csvCell).join(","),
    );
    const blob = new Blob(["﻿" + [head.join(","), ...rows].join("\n")], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `modernomilano-ads-${new Date().toISOString().slice(0, 10)}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const reviewed = filtered.length - queue.length;

  return (
    <div className="flex flex-col gap-5">
      <div className="flex flex-wrap items-center gap-2">
        <div className="flex rounded-lg border border-line p-0.5" role="tablist">
          {(["swipe", "gekozen"] as const).map((v) => (
            <button
              key={v}
              role="tab"
              aria-selected={view === v}
              onClick={() => setView(v)}
              className={`rounded-md px-3 py-1 text-sm ${view === v ? "bg-accent text-accent-text" : "text-ink-2"}`}
            >
              {v === "swipe" ? "Swipen" : `Gekozen (${approved.length})`}
            </button>
          ))}
        </div>
        <select id="ads-collection" aria-label="Collectie" className="input" value={collection} onChange={(e) => setCollection(e.target.value as typeof collection)}>
          {COLLECTIONS.map((c) => (
            <option key={c} value={c}>
              {c === "Alle" ? "Alle collecties" : c === "Other" ? "Overig" : c}
            </option>
          ))}
        </select>
        <select id="ads-placement" aria-label="Plaatsing" className="input" value={placement} onChange={(e) => setPlacement(e.target.value as typeof placement)}>
          {PLACEMENTS.map((p) => (
            <option key={p} value={p}>
              {p === "Alle" ? "Feed en Stories" : p}
            </option>
          ))}
        </select>
        <div className="num ml-auto text-sm text-ink-2">
          {reviewed} van {filtered.length} beoordeeld · <span className="text-good">{approved.length} plaatsen</span> · {skipped} overgeslagen
        </div>
      </div>
      <div className="h-1 overflow-hidden rounded-full bg-surface-2">
        <div className="h-full bg-accent transition-[width]" style={{ width: `${filtered.length ? (reviewed / filtered.length) * 100 : 0}%` }} />
      </div>

      {view === "swipe" ? (
        !loaded ? (
          <div className="card p-8 text-center text-ink-2">Ads laden…</div>
        ) : current ? (
          <SwipeCard
            key={current.id}
            ad={current}
            onDecide={(d) => decide(current.id, d)}
            onUndo={history.length ? undo : undefined}
            onEdit={(p) => edit(current.id, p)}
            onCopied={setToast}
          />
        ) : (
          <div className="card flex flex-col items-center gap-3 p-10 text-center">
            <div className="serif text-xl">Alles beoordeeld</div>
            <p className="max-w-md text-sm text-ink-2">
              Je hebt {approved.length} ads gekozen om te plaatsen. Bekijk ze bij Gekozen en exporteer ze als CSV, of kies een andere collectie of plaatsing.
            </p>
            <button className="btn" onClick={() => setView("gekozen")}>
              Naar gekozen ads
            </button>
          </div>
        )
      ) : (
        <Chosen ads={approved} onReopen={reopen} onExport={exportCsv} onCopied={setToast} />
      )}

      <AngleSpread ads={approved} />

      {toast && (
        <div className="fixed bottom-[calc(1rem+env(safe-area-inset-bottom,0px))] left-1/2 z-50 -translate-x-1/2 rounded-lg bg-accent px-4 py-2 text-sm text-accent-text shadow-lg" role="status">
          {toast}
        </div>
      )}
    </div>
  );
}

function SwipeCard({
  ad,
  onDecide,
  onUndo,
  onEdit,
  onCopied,
}: {
  ad: Ad;
  onDecide: (d: Decision) => void;
  onUndo?: () => void;
  onEdit: (p: Partial<Pick<Ad, "primaryText" | "headline" | "description">>) => void;
  onCopied: (msg: string) => void;
}) {
  const [dx, setDx] = useState(0);
  const [leaving, setLeaving] = useState<Decision | null>(null);
  const [editing, setEditing] = useState(false);
  const [dragging, setDragging] = useState(false);
  const start = useRef<{ x: number; y: number; id: number } | null>(null);

  const finish = (d: Decision) => {
    setLeaving(d);
    setTimeout(() => onDecide(d), 180);
  };

  const onPointerDown = (e: React.PointerEvent) => {
    if ((e.target as HTMLElement).closest("button, textarea, a")) return;
    start.current = { x: e.clientX, y: e.clientY, id: e.pointerId };
    (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
    setDragging(true);
  };
  const onPointerMove = (e: React.PointerEvent) => {
    if (!start.current || start.current.id !== e.pointerId) return;
    setDx(e.clientX - start.current.x);
  };
  const onPointerUp = () => {
    if (!start.current) return;
    start.current = null;
    setDragging(false);
    if (dx > SWIPE_AT) finish("yes");
    else if (dx < -SWIPE_AT) finish("no");
    else setDx(0);
  };

  const x = leaving === "yes" ? 700 : leaving === "no" ? -700 : dx;
  const strength = Math.min(Math.abs(dx) / SWIPE_AT, 1);
  const ratio = ad.aspect && /^\d+:\d+$/.test(ad.aspect) ? ad.aspect.replace(":", " / ") : "4 / 5";
  const copyAll = `${ad.primaryText}\n\nHeadline: ${ad.headline}\nDescription: ${ad.description}\nCTA: ${CTA_LABEL[ad.cta] ?? ad.cta}`;

  return (
    <div className="grid gap-5 lg:grid-cols-[minmax(0,26rem)_minmax(0,1fr)] lg:items-start">
      <div className="flex flex-col gap-3">
        <div
          className="card relative cursor-grab touch-pan-y overflow-hidden select-none active:cursor-grabbing"
          style={{
            transform: `translateX(${x}px) rotate(${x / 25}deg)`,
            transition: dragging ? "none" : "transform 180ms ease-out",
            opacity: leaving ? 0 : 1,
          }}
          onPointerDown={onPointerDown}
          onPointerMove={onPointerMove}
          onPointerUp={onPointerUp}
          onPointerCancel={onPointerUp}
        >
          <div className="flex items-center gap-2 px-3 py-2.5">
            <div className="grid size-8 place-items-center rounded-full bg-brand text-[11px] font-semibold text-black">MM</div>
            <div className="min-w-0 leading-tight">
              <div className="text-sm font-medium">ModernoMilano</div>
              <div className="text-[11px] text-ink-3">Gesponsord</div>
            </div>
          </div>
          <div className="px-3 pb-2.5 text-[13px] whitespace-pre-line">{ad.primaryText}</div>
          <div className="relative mx-auto w-full bg-surface-2" style={{ aspectRatio: ratio, maxHeight: "70vh" }}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={ad.image} alt={ad.scene} draggable={false} className="absolute inset-0 size-full object-cover" />
            <div
              className="pointer-events-none absolute top-4 left-4 rounded-md border-2 border-good px-2 py-0.5 text-sm font-semibold tracking-wider text-good uppercase"
              style={{ opacity: dx > 0 ? strength : 0, background: "var(--surface)" }}
            >
              Plaatsen
            </div>
            <div
              className="pointer-events-none absolute top-4 right-4 rounded-md border-2 border-neg px-2 py-0.5 text-sm font-semibold tracking-wider text-neg uppercase"
              style={{ opacity: dx < 0 ? strength : 0, background: "var(--surface)" }}
            >
              Overslaan
            </div>
          </div>
          <div className="flex items-center gap-3 border-t border-line bg-surface-2 px-3 py-2.5">
            <div className="min-w-0 flex-1">
              <div className="text-[11px] tracking-wide text-ink-3 uppercase">modernomilano.com</div>
              <div className="truncate text-sm font-semibold">{ad.headline}</div>
              <div className="truncate text-xs text-ink-2">{ad.description}</div>
            </div>
            <span className="btn-ghost rounded-md px-3 py-1.5 text-xs font-medium whitespace-nowrap">{CTA_LABEL[ad.cta] ?? ad.cta}</span>
          </div>
        </div>

        <div className="flex items-center justify-center gap-3">
          <button className="btn btn-ghost size-14 justify-center rounded-full !p-0 text-xl text-neg" onClick={() => finish("no")} aria-label="Overslaan (pijl links)">
            ✕
          </button>
          <button className="btn btn-ghost rounded-full text-xs" onClick={onUndo} disabled={!onUndo} aria-label="Vorige terug (Backspace)">
            ↺ Terug
          </button>
          <button className="btn size-14 justify-center rounded-full !p-0 text-xl" onClick={() => finish("yes")} aria-label="Plaatsen (pijl rechts)">
            ✓
          </button>
        </div>
        <p className="text-center text-xs text-ink-3">Sleep de kaart, of gebruik ← en →. Backspace zet de vorige terug.</p>
      </div>

      <div className="flex min-w-0 flex-col gap-4">
        {ad.warning && (
          <div className="rounded-xl border border-warn/50 bg-surface p-3 text-sm" role="note">
            <span className="font-medium text-warn">Controleer het beeld. </span>
            {ad.warning}
          </div>
        )}
        <div className="card flex flex-col gap-3 p-4 md:p-5">
          <div className="flex flex-wrap gap-1.5">
            <Chip strong>{ad.collection === "Other" ? "Overig" : ad.collection}</Chip>
            <Chip>Angle: {angleLabel(ad.angle)}</Chip>
            <Chip>Hook: {ad.hookType}</Chip>
            <Chip>{ad.placement}</Chip>
            {ad.aspect && <Chip>{ad.aspect}</Chip>}
          </div>
          <div>
            <div className="text-[11px] tracking-wider text-ink-3 uppercase">Op de foto</div>
            <p className="mt-0.5 text-sm">{ad.scene}</p>
          </div>
          <div>
            <div className="text-[11px] tracking-wider text-ink-3 uppercase">Product</div>
            <p className="mt-0.5 text-sm">
              {ad.product}
              {ad.price && <span className="num text-ink-2"> · {ad.price.replace("EUR ", "€ ")}</span>}
            </p>
          </div>
          <div>
            <div className="text-[11px] tracking-wider text-ink-3 uppercase">Hook</div>
            <p className="serif mt-0.5 text-lg leading-snug text-balance">{ad.hook}</p>
          </div>
        </div>

        <div className="card flex flex-col gap-3 p-4 md:p-5">
          <div className="flex items-center justify-between gap-2">
            <h2 className="font-medium">Copy</h2>
            <button className="text-sm text-ink-2 underline underline-offset-2" onClick={() => setEditing((v) => !v)}>
              {editing ? "Klaar" : "Bewerken"}
            </button>
          </div>
          {editing ? (
            <div className="flex flex-col gap-2">
              <label className="text-xs text-ink-3" htmlFor={`pt-${ad.id}`}>
                Primaire tekst
              </label>
              <textarea id={`pt-${ad.id}`} className="input min-h-40 font-[inherit]" value={ad.primaryText} onChange={(e) => onEdit({ primaryText: e.target.value })} />
              <label className="text-xs text-ink-3" htmlFor={`hl-${ad.id}`}>
                Kop ({ad.headline.length}/40)
              </label>
              <input id={`hl-${ad.id}`} className="input" value={ad.headline} onChange={(e) => onEdit({ headline: e.target.value })} />
              <label className="text-xs text-ink-3" htmlFor={`ds-${ad.id}`}>
                Beschrijving ({ad.description.length}/30)
              </label>
              <input id={`ds-${ad.id}`} className="input" value={ad.description} onChange={(e) => onEdit({ description: e.target.value })} />
            </div>
          ) : (
            <dl className="flex flex-col gap-3 text-sm">
              <CopyRow label="Primaire tekst" value={ad.primaryText} onCopied={onCopied} multiline />
              <CopyRow label="Kop" value={ad.headline} onCopied={onCopied} />
              <CopyRow label="Beschrijving" value={ad.description} onCopied={onCopied} />
              <div className="flex items-center justify-between gap-3">
                <dt className="text-ink-3">Knop</dt>
                <dd>{CTA_LABEL[ad.cta] ?? ad.cta}</dd>
              </div>
            </dl>
          )}
          <button
            className="btn btn-ghost self-start"
            onClick={async () => onCopied((await copy(copyAll)) ? "Alle copy gekopieerd" : "Kopiëren lukte niet, selecteer de tekst zelf")}
          >
            Kopieer alles
          </button>
        </div>
      </div>
    </div>
  );
}

function CopyRow({ label, value, onCopied, multiline }: { label: string; value: string; onCopied: (m: string) => void; multiline?: boolean }) {
  return (
    <div className="flex flex-col gap-1">
      <div className="flex items-center justify-between gap-3">
        <dt className="text-ink-3">{label}</dt>
        <button
          className="text-xs text-ink-2 underline underline-offset-2"
          onClick={async () => onCopied((await copy(value)) ? `${label} gekopieerd` : "Kopiëren lukte niet, selecteer de tekst zelf")}
        >
          Kopieer
        </button>
      </div>
      <dd className={`select-text ${multiline ? "whitespace-pre-line" : ""}`}>{value}</dd>
    </div>
  );
}

function Chip({ children, strong }: { children: React.ReactNode; strong?: boolean }) {
  return (
    <span className={`rounded-full border px-2 py-0.5 text-xs whitespace-nowrap ${strong ? "border-accent bg-accent text-accent-text" : "border-line text-ink-2"}`}>
      {children}
    </span>
  );
}

function Chosen({ ads, onReopen, onExport, onCopied }: { ads: Ad[]; onReopen: (id: string) => void; onExport: () => void; onCopied: (m: string) => void }) {
  if (!ads.length)
    return (
      <div className="card p-8 text-center text-sm text-ink-2">
        Nog niets gekozen. Swipe een ad naar rechts om hem hier te zetten, met copy klaar om in Ads Manager te plakken.
      </div>
    );
  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <p className="text-sm text-ink-2">De CSV bevat per ad de beeldlink, collectie, angle, hook en alle copyvelden.</p>
        <button className="btn" onClick={onExport}>
          Exporteer {ads.length} ads als CSV
        </button>
      </div>
      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        {ads.map((a) => (
          <article key={a.id} className="card flex min-w-0 flex-col overflow-hidden">
            <div className="relative bg-surface-2" style={{ aspectRatio: "4 / 5" }}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={a.thumb || a.image} alt={a.scene} loading="lazy" className="absolute inset-0 size-full object-cover" />
              <span className="absolute top-2 left-2 rounded-full bg-surface px-2 py-0.5 text-[11px]">{angleLabel(a.angle)}</span>
              {a.warning && (
                <span className="absolute top-2 right-2 rounded-full border border-warn bg-surface px-2 py-0.5 text-[11px] text-warn" title={a.warning}>
                  Tekst op beeld
                </span>
              )}
            </div>
            <div className="flex flex-1 flex-col gap-2 p-3">
              <div className="text-[11px] tracking-wider text-ink-3 uppercase">
                {a.collection === "Other" ? "Overig" : a.collection} · {a.placement}
              </div>
              <p className="serif leading-snug">{a.hook}</p>
              <p className="line-clamp-4 text-xs whitespace-pre-line text-ink-2">{a.primaryText}</p>
              <div className="mt-auto flex flex-wrap gap-2 pt-1">
                <button
                  className="btn btn-ghost !px-2.5 !py-1 text-xs"
                  onClick={async () =>
                    onCopied((await copy(`${a.primaryText}\n\nHeadline: ${a.headline}\nDescription: ${a.description}`)) ? "Copy gekopieerd" : "Kopiëren lukte niet")
                  }
                >
                  Kopieer copy
                </button>
                <a className="btn btn-ghost !px-2.5 !py-1 text-xs" href={a.image} target="_blank" rel="noreferrer">
                  Beeld openen
                </a>
                <button className="ml-auto text-xs text-ink-3 underline underline-offset-2" onClick={() => onReopen(a.id)}>
                  Opnieuw beoordelen
                </button>
              </div>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}

/** Laat zien hoe breed de gekozen set test: per angle hoeveel ads. */
function AngleSpread({ ads }: { ads: Ad[] }) {
  if (!ads.length) return null;
  const counts = new Map<string, number>();
  for (const a of ads) counts.set(a.angle, (counts.get(a.angle) ?? 0) + 1);
  const rows = [...counts.entries()].sort((a, b) => b[1] - a[1]);
  const max = rows[0][1];
  const missing = Object.keys(ANGLE_NL).filter((k) => !counts.has(k));
  return (
    <section className="card p-4 md:p-5">
      <h2 className="font-medium">Testspreiding van je gekozen ads</h2>
      <p className="mt-1 text-sm text-ink-2">Per angle hoeveel ads je gekozen hebt. Meer verschillende angles geeft een eerlijkere test.</p>
      <div className="mt-3 grid gap-1.5">
        {rows.map(([angle, n]) => (
          <div key={angle} className="grid grid-cols-[8.5rem_minmax(0,1fr)_2rem] items-center gap-3 text-sm">
            <span className="truncate text-ink-2">{angleLabel(angle)}</span>
            <div className="h-2 rounded-full bg-surface-2">
              <div className="h-full rounded-full bg-accent" style={{ width: `${(n / max) * 100}%` }} />
            </div>
            <span className="num text-right">{n}</span>
          </div>
        ))}
      </div>
      {missing.length > 0 && <p className="mt-3 text-xs text-ink-3">Nog niet gekozen: {missing.map(angleLabel).join(", ")}.</p>}
    </section>
  );
}
