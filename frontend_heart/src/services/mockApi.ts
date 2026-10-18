/**
 * MOCK LAYER — development only.
 *
 * These responses are generated locally with a transparent heuristic so the UI
 * can be exercised without the Python backend. They are NOT model outputs and
 * carry no accuracy claim. Every mock response is tagged `source: "mock"` so the
 * interface can label it clearly.
 */
import type {
  BulkPredictionResponse,
  LifestyleInput,
  LifestylePredictionResponse,
  PatientInput,
  PredictionResponse,
} from "@/types";
import { GENERAL_RECOMMENDATIONS, LIFESTYLE_LABELS } from "@/utils/lifestyle";

const MOCK_MODEL = "Hybrid Stacking Classifier (demo heuristic)";

function delay<T>(value: T, ms = 700): Promise<T> {
  return new Promise((resolve) => setTimeout(() => resolve(value), ms));
}

/** Simple transparent scoring used only to drive the demo UI. */
function demoScore(p: PatientInput): number {
  // Intercept keeps the demo distribution roughly balanced around 0.5.
  let score = -1.5;
  score += (p.age - 45) * 0.012;
  score += p.sex === 1 ? 0.25 : 0;
  score += p.cp === 3 ? 0.45 : p.cp === 2 ? 0.15 : 0;
  score += (p.trestbps - 130) * 0.006;
  score += (p.chol - 240) * 0.002;
  score += p.fbs === 1 ? 0.1 : 0;
  score += p.restecg > 0 ? 0.12 : 0;
  score += (150 - p.thalach) * 0.01;
  score += p.exang === 1 ? 0.4 : 0;
  score += p.oldpeak * 0.28;
  score += p.slope === 2 ? 0.3 : p.slope === 1 ? 0.12 : 0;
  score += p.ca * 0.32;
  score += p.thal === 3 ? 0.35 : p.thal === 2 ? 0.15 : 0;
  return 1 / (1 + Math.exp(-score));
}

export function mockPredict(patient: PatientInput): Promise<PredictionResponse> {
  const probability = Number(demoScore(patient).toFixed(3));
  const prediction: 0 | 1 = probability >= 0.5 ? 1 : 0;
  return delay({
    prediction,
    label: prediction === 1 ? "Higher predicted risk" : "Lower predicted risk",
    probability,
    model: MOCK_MODEL,
    source: "mock",
  });
}

export function mockBulkPredict(rows: PatientInput[]): Promise<BulkPredictionResponse> {
  const results = rows.map((row, index) => {
    const probability = Number(demoScore(row).toFixed(3));
    return {
      id: `P-${String(index + 1).padStart(4, "0")}`,
      prediction: (probability >= 0.5 ? 1 : 0) as 0 | 1,
      probability,
    };
  });
  const positive = results.filter((r) => r.prediction === 1).length;
  return delay(
    {
      total: results.length,
      positive,
      negative: results.length - positive,
      model: MOCK_MODEL,
      results,
      source: "mock" as const,
    },
    900,
  );
}

export function mockLifestyleRisk(input: LifestyleInput): Promise<LifestylePredictionResponse> {
  const entries = Object.entries(input) as [keyof LifestyleInput, number][];
  const score = Math.round(entries.reduce((sum, [, v]) => sum + v, 0) / entries.length);
  const level = score < 30 ? "lower" : score < 60 ? "moderate" : "higher";
  return delay({
    level,
    score,
    breakdown: entries.map(([key, value]) => ({
      key,
      label: LIFESTYLE_LABELS[key],
      score: value,
    })),
    recommendations: GENERAL_RECOMMENDATIONS,
    source: "mock",
  });
}
