interface ProgressIndicatorProps {
  current: number;
  total: number;
  label: string;
}

export function ProgressIndicator({ current, total, label }: ProgressIndicatorProps) {
  const percent = Math.round((current / total) * 100);
  return (
    <div>
      <div className="flex items-baseline justify-between gap-3">
        <p className="text-sm font-medium">{label}</p>
        <p className="text-xs text-muted-foreground">
          Step {current} of {total}
        </p>
      </div>
      <div
        role="progressbar"
        aria-valuenow={current}
        aria-valuemin={1}
        aria-valuemax={total}
        aria-label="Questionnaire progress"
        className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-surface2"
      >
        <div
          className="h-full rounded-full bg-brand transition-all duration-300"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}
