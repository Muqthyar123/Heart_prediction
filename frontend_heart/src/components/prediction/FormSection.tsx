import type { ReactNode } from "react";

interface FormSectionProps {
  index: number;
  title: string;
  description: string;
  children: ReactNode;
}

export function FormSection({ index, title, description, children }: FormSectionProps) {
  return (
    <section className="clinical-card p-5 sm:p-6">
      <div className="grid grid-cols-[auto_minmax(0,1fr)] items-start gap-3">
        <span className="grid size-8 shrink-0 place-items-center rounded-lg border border-line bg-surface2 font-display text-xs text-brand">
          {String(index).padStart(2, "0")}
        </span>
        <div className="min-w-0">
          <h2 className="font-display text-lg font-semibold">{title}</h2>
          <p className="mt-1 text-sm text-muted-foreground">{description}</p>
        </div>
      </div>
      <div className="mt-6 grid gap-5 sm:grid-cols-2">{children}</div>
    </section>
  );
}
