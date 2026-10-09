"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const GROUPS = [
  {
    label: "Financieel",
    links: [
      { href: "/", label: "Overzicht" },
      { href: "/geld", label: "Waar mijn geld staat" },
      { href: "/winst-naar-bank", label: "Winst naar bank" },
      { href: "/prognose", label: "Prognose" },
      { href: "/meta", label: "Meta ads" },
      { href: "/bank", label: "Bankmutaties" },
      { href: "/payouts", label: "Payouts en disputes" },
    ],
  },
  {
    label: "Producten",
    links: [
      { href: "/marges", label: "Marge per product" },
      { href: "/products", label: "Kostprijzen" },
      { href: "/orders", label: "Orders" },
      { href: "/suppliers", label: "Leveranciers" },
    ],
  },
  {
    label: "Marketing",
    links: [{ href: "/ads", label: "Ads swipen" }],
  },
  {
    label: "Beheer",
    links: [
      { href: "/invoer", label: "Handmatige invoer" },
      { href: "/settings", label: "Instellingen en sync" },
    ],
  },
];

export function Nav() {
  const pathname = usePathname();
  return (
    <nav className="border-b border-line bg-surface md:sticky md:top-0 md:h-screen md:w-60 md:shrink-0 md:overflow-y-auto md:border-r md:border-b-0">
      <div className="px-4 pt-4 pb-2 md:px-5 md:pt-6 md:pb-4">
        <div className="serif text-xl">
          Moderno<span className="italic">Milano</span>
        </div>
        <div className="text-[11px] tracking-[0.2em] text-ink-3 uppercase">Backoffice</div>
      </div>
      <div className="flex gap-1 overflow-x-auto px-3 pb-3 md:block md:overflow-visible">
        {GROUPS.map((g) => (
          <div key={g.label} className="contents md:mb-4 md:block">
            <div className="hidden px-3 pb-1 text-[11px] font-medium tracking-wider text-ink-3 uppercase md:block">{g.label}</div>
            {g.links.map((l) => {
              const active = l.href === "/" ? pathname === "/" : pathname.startsWith(l.href);
              return (
                <Link
                  key={l.href}
                  href={l.href}
                  className={`block shrink-0 rounded-lg px-3 py-1.5 text-sm whitespace-nowrap ${
                    active ? "bg-surface-2 font-medium text-ink" : "text-ink-2 hover:bg-surface-2"
                  }`}
                >
                  {l.label}
                </Link>
              );
            })}
          </div>
        ))}
      </div>
    </nav>
  );
}
