import { Link } from "@tanstack/react-router";
import type { LucideIcon } from "lucide-react";

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
  ctaLabel: string;
  to: string;
  tone?: "brand" | "accent";
}

export function FeatureCard({
  icon: Icon,
  title,
  description,
  ctaLabel,
  to,
  tone = "brand",
}: FeatureCardProps) {
  const accentText = tone === "accent" ? "text-accent" : "text-brand";
  return (
    <div className="group rounded-2xl border border-line bg-obsidian p-6 transition hover:border-brand/40">
      <div
        className={`grid size-11 place-items-center rounded-xl border border-line bg-surface2 ${accentText}`}
      >
        <Icon className="size-5" aria-hidden />
      </div>
      <h3 className="mt-5 font-display text-lg font-semibold">{title}</h3>
      <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{description}</p>
      <Link
        to={to}
        className={`mt-5 inline-flex items-center gap-1.5 text-sm font-semibold transition-all group-hover:gap-2.5 ${accentText}`}
      >
        {ctaLabel} <span aria-hidden>→</span>
      </Link>
    </div>
  );
}
