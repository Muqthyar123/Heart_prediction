import { Printer, RotateCcw, ShieldCheck } from "lucide-react";
import { useState } from "react";
import { RiskIndicator } from "./RiskIndicator";
import { CLINICAL_FEATURES, optionLabel } from "@/utils/clinicalFeatures";
import type { PatientInput, PredictionResponse } from "@/types";

interface PredictionResultProps {
  result: PredictionResponse;
  patient: PatientInput;
  onPredictAgain: () => void;
}

export function PredictionResult({ result, patient, onPredictAgain }: PredictionResultProps) {
  const [showDetails, setShowDetails] = useState(false);
  const positive = result.prediction === 1;

  return (
    <div className="printable-summary rise-in clinical-card p-6 sm:p-8">
      <div className="print-only mb-5 border-b border-line pb-4">
        <p className="eyebrow">CardioSight · Assessment summary</p>
        <h2 className="mt-2 font-display text-2xl font-bold">Heart Risk Prediction</h2>
        <p className="mt-1 text-sm text-muted-foreground">Generated {new Date().toLocaleString()}</p>
      </div>
      <div className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-3">
        <span className="truncate text-xs uppercase tracking-[0.15em] text-muted-foreground">
          Model Prediction
        </span>
        <span
          className={`shrink-0 rounded-full border px-3 py-1 text-xs font-medium ${
            positive
              ? "border-destructive/30 bg-destructive/10 text-destructive"
              : "border-brand/30 bg-brand/10 text-brand"
          }`}
        >
          {result.label}
        </span>
      </div>

      <div className="mt-6 flex flex-col items-center gap-5 sm:flex-row sm:items-center">
        <RiskIndicator
          {...(result.source !== "mock" && result.probability !== undefined
            ? { probability: result.probability }
            : {})}
          positive={positive}
        />
        <div className="min-w-0 text-center sm:text-left">
          <p className="font-display text-lg font-semibold">
            {positive ? "Higher estimated risk class" : "Lower estimated risk class"}
          </p>
          <p className="mt-1 text-sm text-muted-foreground">Model used: {result.model}</p>
          {result.source === "mock" ? (
            <p className="mt-1 text-xs text-ai">
              Demo classification — no measured probability is shown.
            </p>
          ) : null}
        </div>
      </div>

      <div className="mt-6 flex flex-wrap gap-3">
        <button
          type="button"
          onClick={onPredictAgain}
          className="print-hide btn-secondary flex-1 px-4 py-2.5"
        >
          <RotateCcw className="size-4" aria-hidden /> Predict Again
        </button>
        <button
          type="button"
          onClick={() => setShowDetails((v) => !v)}
          aria-expanded={showDetails}
          className="print-hide btn-primary flex-1 px-4 py-2.5"
        >
          <ShieldCheck className="size-4" aria-hidden />
          {showDetails ? "Hide Details" : "View Details"}
        </button>
        <button type="button" onClick={() => window.print()} className="print-hide btn-secondary flex-1 px-4 py-2.5">
          <Printer className="size-4" aria-hidden /> Print / Save as PDF
        </button>
      </div>

      {showDetails ? (
        <dl className="print-hide mt-6 grid gap-x-6 gap-y-2 border-t border-line pt-5 text-sm sm:grid-cols-2">
          {CLINICAL_FEATURES.map((feature) => (
            <div key={feature.key} className="flex items-baseline justify-between gap-3">
              <dt className="min-w-0 truncate text-muted-foreground">{feature.name}</dt>
              <dd className="shrink-0 font-medium">
                {feature.options
                  ? optionLabel(feature.key, patient[feature.key])
                  : `${patient[feature.key]}${feature.unit ? ` ${feature.unit}` : ""}`}
              </dd>
            </div>
          ))}
        </dl>
      ) : null}

      <dl className="print-only mt-6 grid gap-x-6 gap-y-2 border-t border-line pt-5 text-sm sm:grid-cols-2">
        {CLINICAL_FEATURES.map((feature) => (
          <div key={feature.key} className="flex items-baseline justify-between gap-3">
            <dt className="min-w-0 text-muted-foreground">{feature.name}</dt>
            <dd className="shrink-0 font-medium">
              {feature.options
                ? optionLabel(feature.key, patient[feature.key])
                : `${patient[feature.key]}${feature.unit ? ` ${feature.unit}` : ""}`}
            </dd>
          </div>
        ))}
      </dl>

      <p className="mt-6 text-xs leading-relaxed text-muted-foreground">
        This result is a machine-learning prediction and should not replace professional medical
        evaluation.
      </p>
    </div>
  );
}
