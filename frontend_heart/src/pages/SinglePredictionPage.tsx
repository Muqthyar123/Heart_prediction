import { Activity, BrainCircuit, Database, GitMerge, Sparkles } from "lucide-react";
import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { ErrorState } from "@/components/common/States";
import { PredictionForm } from "@/components/prediction/PredictionForm";
import { PredictionResult } from "@/components/prediction/PredictionResult";
import { PageShell } from "@/layouts/SiteLayout";
import { predictSingle } from "@/services/api";
import type { PatientInput, PredictionResponse } from "@/types";

const PROCESS_STEPS = [
  { icon: Database, label: "Collecting Inputs" },
  { icon: Activity, label: "Processing Features" },
  { icon: BrainCircuit, label: "Running AI Models" },
  { icon: GitMerge, label: "Stacking Predictions" },
  { icon: Sparkles, label: "Generating Assessment" },
] as const;

export function SinglePredictionPage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [patient, setPatient] = useState<PatientInput | null>(null);
  const [processingStep, setProcessingStep] = useState(0);

  useEffect(() => {
    if (!loading) return;
    setProcessingStep(0);
    const timer = window.setInterval(() => setProcessingStep((value) => Math.min(value + 1, 4)), 450);
    return () => window.clearInterval(timer);
  }, [loading]);

  async function runPrediction(input: PatientInput) {
    setLoading(true);
    setError(null);
    setPatient(input);
    try {
      const response = await predictSingle(input);
      setResult(response);
    } catch (err) {
      setResult(null);
      setError(err instanceof Error ? err.message : "The prediction request failed.");
      toast.error("Prediction failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <PageShell
      title="Heart Risk Prediction"
      subtitle="A guided clinical AI assessment using thirteen standard cardiovascular features and the project’s hybrid ensemble framework."
    >
      {loading ? (
        <div className="clinical-card p-8 sm:p-10" role="status" aria-live="polite">
          <div className="mx-auto grid size-20 place-items-center rounded-full border border-brand/30 bg-brand/10"><BrainCircuit className="size-9 animate-pulse text-brand" aria-hidden /></div>
          <p className="mt-5 text-center font-display text-xl font-semibold">Running clinical AI analysis</p>
          <div className="mx-auto mt-7 grid max-w-3xl gap-3 sm:grid-cols-5">
            {PROCESS_STEPS.map(({ icon: Icon, label }, index) => <motion.div key={label} animate={{ opacity: index <= processingStep ? 1 : .35 }} className={`rounded-lg border p-3 text-center ${index <= processingStep ? "border-brand/30 bg-brand/5" : "border-line bg-obsidian"}`}><Icon className="mx-auto size-4 text-brand" aria-hidden /><p className="mt-2 text-[11px] text-muted-foreground">{label}</p></motion.div>)}
          </div>
        </div>
      ) : error ? (
        <ErrorState
          message={error}
          onRetry={patient ? () => void runPrediction(patient) : undefined}
        />
      ) : result && patient ? (
        <PredictionResult
          result={result}
          patient={patient}
          onPredictAgain={() => {
            setResult(null);
            setPatient(null);
          }}
        />
      ) : (
        <PredictionForm loading={loading} onSubmit={(input) => void runPrediction(input)} />
      )}
    </PageShell>
  );
}
