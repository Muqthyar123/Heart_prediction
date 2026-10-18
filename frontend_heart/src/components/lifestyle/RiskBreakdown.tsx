import type { LifestyleBreakdownItem } from "@/types";

function toneFor(score: number) {
  if (score < 30) return { bar: "bg-positive", label: "Lower" };
  if (score < 60) return { bar: "bg-warning", label: "Moderate" };
  return { bar: "bg-destructive", label: "Higher" };
}

export function RiskBreakdown({ items }: { items: LifestyleBreakdownItem[] }) {
  return (
    <ul className="space-y-4">
      {items.map((item) => {
        const tone = toneFor(item.score);
        return (
          <li key={item.key}>
            <div className="flex items-baseline justify-between gap-3 text-sm">
              <span className="min-w-0 truncate">{item.label}</span>
              <span className="shrink-0 text-xs text-muted-foreground">{tone.label}</span>
            </div>
            <div className="mt-1.5 h-1.5 w-full overflow-hidden rounded-full bg-surface2">
              <div
                className={`h-full rounded-full ${tone.bar}`}
                style={{ width: `${Math.max(6, item.score)}%` }}
              />
            </div>
          </li>
        );
      })}
    </ul>
  );
}
