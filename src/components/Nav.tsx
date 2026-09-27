"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/", label: "Dashboard" },
  { href: "/products", label: "Producten & kostprijs" },
  { href: "/orders", label: "Orders" },
  { href: "/suppliers", label: "Leveranciers" },
  { href: "/ads", label: "Advertenties" },
  { href: "/expenses", label: "Vaste lasten" },
  { href: "/settings", label: "Instellingen" },
];

export function Nav() {
  const pathname = usePathname();
  return (
    <nav className="border-b border-line bg-surface md:sticky md:top-0 md:h-screen md:w-60 md:shrink-0 md:border-r md:border-b-0">
      <div className="px-4 py-4 md:px-5 md:py-6">
        <div className="text-[11px] font-medium tracking-[0.2em] text-ink-3 uppercase">Backoffice</div>
        <div className="mt-0.5 text-lg font-semibold tracking-tight">ModernoMilano</div>
      </div>
      <ul className="flex gap-1 overflow-x-auto px-3 pb-3 md:flex-col md:overflow-visible md:pb-0">
        {LINKS.map((l) => {
          const active = l.href === "/" ? pathname === "/" : pathname.startsWith(l.href);
          return (
            <li key={l.href}>
              <Link
                href={l.href}
                className={`block rounded-lg px-3 py-2 text-sm whitespace-nowrap ${
                  active ? "bg-surface-2 font-medium text-ink" : "text-ink-2 hover:bg-surface-2"
                }`}
              >
                {l.label}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
