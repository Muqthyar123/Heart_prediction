import { Check, Info, Lock } from "lucide-react";
import type { ReactNode } from "react";

export const btnPrimary =
  "btn-primary px-5 py-3";
export const btnSecondary =
  "btn-secondary px-5 py-3";
export const inputClass =
  "w-full rounded-lg border border-line bg-surface px-3 py-2.5 text-sm outline-none transition focus:border-brand";

export function Card({ children, className = "" }: { children: ReactNode; className?: string }) {
  return (
    <div className={`clinical-card p-5 ${className}`}>
      {children}
    </div>
  );
}

export function DemoBadge() {
  return (
    <span className="inline-flex shrink-0 items-center rounded-full border border-accent/40 bg-accent/10 px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider text-accent">
      DEMO DATA
    </span>
  );
}

export function Notice({
  children,
  tone = "brand",
  icon = "info",
}: {
  children: ReactNode;
  tone?: "brand" | "accent";
  icon?: "info" | "lock";
}) {
  const Icon = icon === "lock" ? Lock : Info;
  return (
    <div
      className={`flex gap-3 rounded-xl border p-4 text-sm leading-relaxed ${
        tone === "accent" ? "border-accent/30 bg-accent/5" : "border-brand/25 bg-brand/5"
      }`}
    >
      <Icon
        className={`mt-0.5 size-4 shrink-0 ${tone === "accent" ? "text-accent" : "text-brand"}`}
        aria-hidden
      />
      <div className="text-muted-foreground">{children}</div>
    </div>
  );
}

export function StepProgress({
  steps,
  current,
  onSelect,
}: {
  steps: string[];
  current: number;
  onSelect?: (index: number) => void;
}) {
  return (
    <nav aria-label="Progress">
      <p className="mb-3 text-xs text-muted-foreground">
        Step {current + 1} of {steps.length} · {steps[current]}
      </p>
      <div className="h-1.5 overflow-hidden rounded-full bg-surface2">
        <div
          className="h-full rounded-full bg-brand transition-all duration-500"
          style={{ width: `${((current + 1) / steps.length) * 100}%` }}
        />
      </div>
      <ol className="mt-4 hidden gap-2 md:flex">
        {steps.map((label, index) => {
          const done = index < current;
          const active = index === current;
          return (
            <li key={label} className="min-w-0 flex-1">
              <button
                type="button"
                disabled={!onSelect || index > current}
                onClick={() => onSelect?.(index)}
                aria-current={active ? "step" : undefined}
                className={`flex w-full items-center gap-2 rounded-lg px-2 py-1.5 text-left text-xs transition ${
                  active ? "text-foreground" : done ? "text-brand" : "text-muted-foreground"
                } disabled:cursor-default`}
              >
                <span
                  className={`grid size-6 shrink-0 place-items-center rounded-full border text-[11px] ${
                    active
                      ? "border-brand bg-brand text-brand-foreground"
                      : done
                        ? "border-brand/50 text-brand"
                        : "border-line"
                  }`}
                >
                  {done ? <Check className="size-3" aria-hidden /> : index + 1}
                </span>
                <span className="truncate">{label}</span>
              </button>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

export function Field({
  id,
  label,
  required,
  hint,
  error,
  children,
}: {
  id: string;
  label: string;
  required?: boolean;
  hint?: string | undefined;
  error?: string | undefined;
  children: ReactNode;
}) {
  return (
    <div>
      <label htmlFor={id} className="flex items-baseline justify-between gap-2 text-sm font-medium">
        <span>{label}</span>
        <span
          className={`text-[11px] font-normal ${required ? "text-accent" : "text-muted-foreground"}`}
        >
          {required ? "Required" : "Optional"}
        </span>
      </label>
      <div className="mt-1.5">{children}</div>
      {error ? (
        <p role="alert" className="mt-1 text-xs text-destructive">
          {error}
        </p>
      ) : hint ? (
        <p className="mt-1 text-xs text-muted-foreground">{hint}</p>
      ) : null}
    </div>
  );
}

export function formatDate(iso: string, lang: string) {
  return new Date(iso).toLocaleDateString(lang === "te" ? "te-IN" : "en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
