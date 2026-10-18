import { Link } from "@tanstack/react-router";
import { Activity } from "lucide-react";
import { NAV_LINKS } from "./Navbar";

export function Footer() {
  return (
    <footer className="mt-16 border-t border-line bg-obsidian/90 backdrop-blur">
      <div className="mx-auto grid max-w-7xl gap-8 px-5 py-12 md:grid-cols-[1.2fr_0.8fr_1fr] lg:px-8">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="brand-heart grid size-8 place-items-center rounded-lg border border-brand/30 bg-brand/10 text-brand"><Activity className="size-4" aria-hidden /></span>
            <span className="font-display font-semibold">Cardio<span className="text-brand">Sight</span></span>
          </div>
          <p className="mt-4 max-w-xs text-sm leading-relaxed text-muted-foreground">
            An AI-assisted cardiovascular risk research interface built around a hybrid stacking ensemble.
          </p>
        </div>
        <div>
          <p className="text-xs uppercase tracking-[0.15em] text-muted-foreground">Navigate</p>
          <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
            {NAV_LINKS.map((link) => (
              <li key={link.to}><Link to={link.to} className="transition hover:text-brand">{link.label}</Link></li>
            ))}
          </ul>
        </div>
        <div>
          <p className="text-xs uppercase tracking-[0.15em] text-muted-foreground">Medical disclaimer</p>
          <p className="mt-4 text-sm leading-relaxed text-muted-foreground">
            This research interface is not a medical diagnosis and does not replace evaluation or advice from a qualified healthcare professional.
          </p>
        </div>
      </div>
    </footer>
  );
}