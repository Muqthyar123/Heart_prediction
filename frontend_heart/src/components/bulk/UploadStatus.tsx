import { AlertCircle, CheckCircle2, FileSpreadsheet, X } from "lucide-react";
import type { ParsedFile } from "@/utils/parseRecords";

interface UploadStatusProps {
  file: ParsedFile;
  onClear: () => void;
}

export function UploadStatus({ file, onClear }: UploadStatusProps) {
  const valid = file.missingColumns.length === 0;
  return (
    <div className="clinical-card p-5">
      <div className="grid grid-cols-[auto_minmax(0,1fr)_auto] items-center gap-3">
        <span className="grid size-10 shrink-0 place-items-center rounded-xl border border-line bg-surface2 text-brand">
          <FileSpreadsheet className="size-5" aria-hidden />
        </span>
        <div className="min-w-0">
          <p className="truncate font-medium">{file.fileName}</p>
          <p className="text-xs text-muted-foreground">
            {file.rowCount} records · {file.columns.length} columns detected
          </p>
        </div>
        <button
          type="button"
          onClick={onClear}
          aria-label="Remove file"
          className="grid size-8 shrink-0 place-items-center rounded-lg border border-line bg-obsidian text-muted-foreground transition hover:text-foreground"
        >
          <X className="size-4" aria-hidden />
        </button>
      </div>

      <div
        className={`mt-4 flex items-start gap-2 rounded-xl border p-3 text-sm ${
          valid
            ? "border-positive/30 bg-positive/5 text-positive"
            : "border-destructive/40 bg-destructive/5 text-destructive"
        }`}
      >
        {valid ? (
          <CheckCircle2 className="mt-0.5 size-4 shrink-0" aria-hidden />
        ) : (
          <AlertCircle className="mt-0.5 size-4 shrink-0" aria-hidden />
        )}
        <p className="min-w-0">
          {valid
            ? "All 13 required feature columns were found. Ready to predict."
            : `Missing required columns: ${file.missingColumns.join(", ")}`}
        </p>
      </div>
    </div>
  );
}
