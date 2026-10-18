import { ArrowLeft, ArrowRight, Loader2, RotateCcw, ShieldAlert } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import { ErrorState, LoadingState } from "@/components/common/States";
import { LifestyleQuestion } from "@/components/lifestyle/LifestyleQuestion";
import { ProgressIndicator } from "@/components/lifestyle/ProgressIndicator";
import { RiskBreakdown } from "@/components/lifestyle/RiskBreakdown";
import { PageShell } from "@/layouts/SiteLayout";
import { assessLifestyle } from "@/services/api";
import { LIFESTYLE_QUESTIONS } from "@/utils/lifestyle";
import type { LifestyleAnswerKey, LifestyleInput, LifestylePredictionResponse } from "@/types";

const LEVEL_COPY: Record<string, { title: string; tone: string }> = {
  lower: { title: "Lower lifestyle risk", tone: "text-positive" },
  moderate: { title: "Moderate lifestyle risk", tone: "text-warning" },
  higher: { title: "Higher lifestyle risk", tone: "text-destructive" },
};

export function LifestyleRiskPage() {
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<Partial<Record<LifestyleAnswerKey, number>>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<LifestylePredictionResponse | null>(null);

  const total = LIFESTYLE_QUESTIONS.length;
  const question = LIFESTYLE_QUESTIONS[step]!;
  const answered = answers[question.key] !== undefined;

  async function submit(final: Partial<Record<LifestyleAnswerKey, number>>) {
    setLoading(true);
    setError(null);
    try {
      const response = await assessLifestyle(final as LifestyleInput);
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "The assessment request failed.");
      toast.error("Assessment failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  function restart() {
    setAnswers({});
    setStep(0);
    setResult(null);
    setError(null);
  }

  return (
    <PageShell
      title="Lifestyle Risk Assessment"
      subtitle="Answer seven short questions about your daily habits to receive a lifestyle-based risk overview and general wellness guidance."
    >
      <div className="mx-auto max-w-2xl">
        {loading ? (
          <LoadingState message="Assessing your lifestyle answers…" />
        ) : error ? (
          <ErrorState message={error} onRetry={() => void submit(answers)} />
        ) : result ? (
          <div className="space-y-5">
            <div className="clinical-card p-6 text-center">
              <p className="text-xs uppercase tracking-[0.15em] text-muted-foreground">
                Lifestyle risk level
              </p>
              <p
                className={`mt-2 font-display text-3xl font-bold ${LEVEL_COPY[result.level]?.tone ?? ""}`}
              >
                {LEVEL_COPY[result.level]?.title ?? result.level}
              </p>
              <p className="mt-3 text-sm text-muted-foreground">
                Based only on the lifestyle answers you provided — not on clinical measurements.
              </p>
              {result.source === "mock" ? (
                <p className="mt-2 text-xs text-ai">
                  Demo response — no assessment backend is connected yet.
                </p>
              ) : null}
            </div>

            <div className="clinical-card p-6">
              <h2 className="font-display text-lg font-semibold">Contributing areas</h2>
              <div className="mt-4">
                <RiskBreakdown items={result.breakdown} />
              </div>
            </div>

            <div className="clinical-card p-6">
              <h2 className="font-display text-lg font-semibold">General wellness suggestions</h2>
              <ul className="mt-4 space-y-2.5 text-sm text-muted-foreground">
                {result.recommendations.map((item) => (
                  <li key={item} className="flex items-start gap-2.5">
                    <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-brand" />
                    <span className="min-w-0">{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="flex items-start gap-3 rounded-lg border border-warning/30 bg-warning/5 p-5">
              <ShieldAlert className="mt-0.5 size-4 shrink-0 text-warning" aria-hidden />
              <p className="min-w-0 text-sm text-muted-foreground">
                This lifestyle overview is general guidance only and is not a medical diagnosis.
                Speak with a qualified healthcare professional about your personal health.
              </p>
            </div>

            <button
              type="button"
              onClick={restart}
              className="btn-secondary px-5 py-2.5"
            >
              <RotateCcw className="size-4" aria-hidden /> Retake assessment
            </button>
          </div>
        ) : (
          <div className="clinical-card p-6 sm:p-8">
            <ProgressIndicator current={step + 1} total={total} label={question.title} />
            <div className="mt-7">
              <LifestyleQuestion
                key={question.key}
                question={question}
                value={answers[question.key]}
                onChange={(value) => setAnswers((prev) => ({ ...prev, [question.key]: value }))}
              />
            </div>
            <div className="mt-7 flex items-center justify-between gap-3">
              <button
                type="button"
                onClick={() => setStep((s) => Math.max(0, s - 1))}
                disabled={step === 0}
                className="btn-secondary px-4 py-2.5 disabled:opacity-40"
              >
                <ArrowLeft className="size-4" aria-hidden /> Back
              </button>
              <button
                type="button"
                disabled={!answered}
                onClick={() => {
                  if (step === total - 1) void submit(answers);
                  else setStep((s) => s + 1);
                }}
                className="btn-primary px-5 py-2.5 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? <Loader2 className="size-4 animate-spin" aria-hidden /> : null}
                {step === total - 1 ? "See my result" : "Next"}
                {step === total - 1 ? null : <ArrowRight className="size-4" aria-hidden />}
              </button>
            </div>
          </div>
        )}
      </div>
    </PageShell>
  );
}
