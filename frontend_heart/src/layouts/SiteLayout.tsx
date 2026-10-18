import type { ReactNode } from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";

export function SiteLayout({ children }: { children: ReactNode }) {
  return (
    <div className="relative isolate flex min-h-screen flex-col overflow-hidden text-foreground">
      <Navbar />
      <main className="page-enter relative flex-1">{children}</main>
      <Footer />
    </div>
  );
}

export function PageShell({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle: string;
  children: ReactNode;
}) {
  return (
    <div className="mx-auto max-w-7xl px-5 py-12 lg:px-8 lg:py-16">
      <header className="rise-in max-w-2xl">
        <p className="eyebrow">CardioSight research system</p>
        <h1 className="mt-3 font-display text-3xl font-bold sm:text-5xl">{title}</h1>
        <p className="mt-3 text-base leading-relaxed text-muted-foreground">{subtitle}</p>
      </header>
      <div className="mt-8">{children}</div>
    </div>
  );
}
