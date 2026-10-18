import { Link } from "@tanstack/react-router";
import { AnimatePresence, motion } from "framer-motion";
import { Activity, Menu, X } from "lucide-react";
import { useEffect, useState } from "react";

export const NAV_LINKS = [
  { to: "/", label: "Home" },
  { to: "/single-prediction", label: "Risk Prediction" },
  { to: "/bulk-prediction", label: "Bulk Prediction" },
  { to: "/lifestyle-risk", label: "Lifestyle Risk" },
  { to: "/methodology", label: "Methodology" },
  { to: "/explainable-ai", label: "Explainable AI" },
  { to: "/results", label: "Results" },
  { to: "/about", label: "About" },
] as const;

export function Navbar() {
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 16);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header className={`sticky top-0 z-50 transition-all duration-300 ${scrolled ? "border-b border-line bg-background/90 shadow-lg backdrop-blur-sm" : "border-b border-transparent bg-background/55 backdrop-blur-md"}`}>
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-5 lg:px-8">
        <Link to="/" className="flex items-center gap-2.5" onClick={() => setOpen(false)}>
          <span className="brand-heart grid size-9 place-items-center rounded-lg border border-brand/30 bg-brand/10 text-brand"><Activity className="size-5" aria-hidden /></span>
          <span className="font-display text-[17px] font-semibold">Cardio<span className="text-brand">Sight</span></span>
        </Link>

        <nav aria-label="Main navigation" className="hidden items-center gap-1 lg:flex">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              activeOptions={{ exact: link.to === "/" }}
               activeProps={{ className: "nav-active text-foreground" }}
              inactiveProps={{ className: "text-muted-foreground hover:text-foreground" }}
              className="rounded-md px-3.5 py-2 text-sm transition"
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          <Link to="/single-prediction" className="btn-primary hidden px-4 py-2 sm:inline-flex">
            Predict Risk
          </Link>
          <button
            type="button"
            onClick={() => setOpen((value) => !value)}
            aria-expanded={open}
            aria-label={open ? "Close menu" : "Open menu"}
            className="icon-button lg:hidden"
          >
            {open ? <X className="size-4" aria-hidden /> : <Menu className="size-4" aria-hidden />}
          </button>
        </div>
      </div>

      <AnimatePresence>
        {open ? (
          <motion.nav
            aria-label="Mobile navigation"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden border-t border-line bg-obsidian/95 backdrop-blur-sm lg:hidden"
          >
            <ul className="space-y-1 px-5 py-3">
              {NAV_LINKS.map((link, index) => (
                <motion.li key={link.to} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: index * 0.035 }}>
                  <Link
                    to={link.to}
                    activeOptions={{ exact: link.to === "/" }}
                    activeProps={{ className: "border-l-2 border-brand bg-brand/10 text-foreground" }}
                    inactiveProps={{ className: "text-muted-foreground" }}
                    onClick={() => setOpen(false)}
                    className="block rounded-lg px-3 py-2.5 text-sm"
                  >
                    {link.label}
                  </Link>
                </motion.li>
              ))}
              <li className="pt-2"><Link to="/single-prediction" onClick={() => setOpen(false)} className="btn-primary w-full">Predict Risk <Activity className="size-4" /></Link></li>
            </ul>
          </motion.nav>
        ) : null}
      </AnimatePresence>
    </header>
  );
}