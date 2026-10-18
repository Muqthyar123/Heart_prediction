import { Download, Loader2, Play } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { FileUploader } from "@/components/bulk/FileUploader";
import { ResultSummary } from "@/components/bulk/ResultSummary";
import { ResultsTable } from "@/components/bulk/ResultsTable";
import { UploadStatus } from "@/components/bulk/UploadStatus";
import { EmptyState, ErrorState, SkeletonRows } from "@/components/common/States";
import { PageShell } from "@/layouts/SiteLayout";
import { predictBulk } from "@/services/api";
import { REQUIRED_COLUMNS } from "@/utils/clinicalFeatures";
import { downloadCsv, parseRecordsFile, resultsToCsv, type ParsedFile } from "@/utils/parseRecords";
import type { BulkPredictionResponse } from "@/types";

export function BulkPredictionPage() {
  const [file, setFile] = useState<File | null>(null);
  const [parsed, setParsed] = useState<ParsedFile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<BulkPredictionResponse | null>(null);

  async function handleFile(selected: File) {
    setError(null);
    setData(null);
    setFile(selected);
    try {
      const result = await parseRecordsFile(selected);
      setParsed(result);
      if (result.missingColumns.length > 0) {
        toast.error("Some required columns are missing from the file.");
      } else {
        toast.success(`${result.rowCount} records ready for prediction.`);
      }
    } catch (err) {
      setParsed(null);
      setError(err instanceof Error ? err.message : "The file could not be read.");
    }
  }

  async function runBulk() {
    if (!file || !parsed || parsed.missingColumns.length > 0) return;
    setLoading(true);
    setError(null);
    try {
      const response = await predictBulk(file, parsed.rows);
      setData(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "The bulk prediction request failed.");
      toast.error("Bulk prediction failed.");
    } finally {
      setLoading(false);
    }
  }

  function reset() {
    setFile(null);
    setParsed(null);
    setData(null);
    setError(null);
  }

  const ready = parsed !== null && parsed.missingColumns.length === 0;

  return (
    <PageShell
      title="Bulk Prediction"
      subtitle="Upload an Excel or CSV file with multiple patient records and generate predictions for every row."
    >
      <div className="space-y-6">
        {!parsed ? (
          <FileUploader
            disabled={loading}
            onFileSelected={(selected) => void handleFile(selected)}
            onReject={(message) => {
              setError(message);
              toast.error(message);
            }}
          />
        ) : (
          <UploadStatus file={parsed} onClear={reset} />
        )}

        <div className="clinical-card p-5">
          <p className="text-sm font-medium">Required columns</p>
          <p className="mt-1 text-xs text-muted-foreground">
            Your file must include a header row with these column names.
          </p>
          <div className="mt-3 flex flex-wrap gap-2">
            {REQUIRED_COLUMNS.map((column) => (
              <span
                key={column}
                className="rounded-lg border border-line bg-surface px-2.5 py-1 font-mono text-xs text-muted-foreground"
              >
                {column}
              </span>
            ))}
          </div>
        </div>

        {ready && !data ? (
          <button
            type="button"
            onClick={() => void runBulk()}
            disabled={loading}
            className="btn-primary px-6 py-3 disabled:opacity-60"
          >
            {loading ? (
              <Loader2 className="size-4 animate-spin" aria-hidden />
            ) : (
              <Play className="size-4" aria-hidden />
            )}
            {loading ? "Processing records…" : `Predict ${parsed.rowCount} records`}
          </button>
        ) : null}

        {error ? <ErrorState message={error} onRetry={ready ? () => void runBulk() : reset} /> : null}

        {loading ? (
          <div className="clinical-card p-5">
            <SkeletonRows rows={6} />
          </div>
        ) : null}

        {data ? (
          <div className="space-y-5">
            <ResultSummary data={data} />
            <div className="flex flex-wrap gap-3">
              <button
                type="button"
                onClick={() =>
                  downloadCsv("heart-disease-predictions.csv", resultsToCsv(data.results))
                }
                className="btn-secondary px-5 py-2.5"
              >
                <Download className="size-4" aria-hidden /> Download results (CSV)
              </button>
              <button
                type="button"
                onClick={reset}
                className="btn-secondary px-5 py-2.5 text-muted-foreground hover:text-foreground"
              >
                Upload another file
              </button>
            </div>
            <ResultsTable results={data.results} />
          </div>
        ) : !parsed && !error ? (
          <EmptyState
            title="No file analyzed yet"
            message="Upload a patient dataset to see prediction results here."
          />
        ) : null}

        <p className="text-xs leading-relaxed text-muted-foreground">
          Results are model predictions for decision support only and do not constitute a medical
          diagnosis.
        </p>
      </div>
    </PageShell>
  );
}
