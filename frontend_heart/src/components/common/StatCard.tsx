interface StatCardProps {
  value: string;
  label: string;
  tone?: "brand" | "accent" | "plain";
}

const toneClass = {
  brand: "text-brand",
  accent: "text-accent",
  plain: "text-foreground",
} as const;

export function StatCard({ value, label, tone = "brand" }: StatCardProps) {
  return (
    <div className="rounded-2xl border border-line bg-surface p-5">
      <p className={`font-display text-2xl font-bold sm:text-3xl ${toneClass[tone]}`}>{value}</p>
      <p className="mt-1 text-sm text-muted-foreground">{label}</p>
    </div>
  );
}
