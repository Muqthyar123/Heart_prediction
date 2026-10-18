import { AlertTriangle, Inbox, Loader2 } from "lucide-react";
import type { ReactNode } from "react";

export function LoadingState({ message = "Working…" }: { message?: string }) {
  return (
    <div
      role="status"
      aria-live="polite"
      className="clinical-card flex flex-col items-center justify-center gap-3 p-10 text-center"
    >
      <Loader2 className="size-6 animate-spin text-brand" aria-hidden />
      <p className="text-sm text-muted-foreground">{message}</p>
    </div>
  );
}

export function ErrorState({
  title = "Something went wrong",
  message,
  onRetry,
}: {
  title?: string | undefined;
  message: string;
  onRetry?: (() => void) | undefined;
}) {
  return (
    <div
      role="alert"
      className="rounded-2xl border border-destructive/40 bg-destructive/5 p-6 text-center"
    >
      <AlertTriangle className="mx-auto size-6 text-destructive" aria-hidden />
      <p className="mt-3 font-display font-semibold">{title}</p>
      <p className="mt-1 text-sm text-muted-foreground">{message}</p>
      {onRetry ? (
        <button
          type="button"
          onClick={onRetry}
          className="btn-secondary mt-4 px-4 py-2"
        >
          Try again
        </button>
      ) : null}
    </div>
  );
}

export function EmptyState({
  title,
  message,
  action,
}: {
  title: string;
  message: string;
  action?: ReactNode;
}) {
  return (
    <div className="rounded-lg border border-dashed border-line bg-obsidian/70 p-10 text-center backdrop-blur">
      <Inbox className="mx-auto size-6 text-muted-foreground" aria-hidden />
      <p className="mt-3 font-display font-semibold">{title}</p>
      <p className="mx-auto mt-1 max-w-sm text-sm text-muted-foreground">{message}</p>
      {action ? <div className="mt-4">{action}</div> : null}
    </div>
  );
}

export function SkeletonRows({ rows = 5 }: { rows?: number }) {
  return (
    <div className="space-y-2" aria-hidden>
      {Array.from({ length: rows }).map((_, index) => (
        <div key={index} className="h-10 animate-pulse rounded-lg bg-surface2" />
      ))}
    </div>
  );
}
