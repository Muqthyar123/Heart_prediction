/** Shared domain types for CardioSight. */

export interface PatientInput {
  age: number;
  sex: number;
  cp: number;
  trestbps: number;
  chol: number;
  fbs: number;
  restecg: number;
  thalach: number;
  exang: number;
  oldpeak: number;
  slope: number;
  ca: number;
  thal: number;
}

export type PatientInputKey = keyof PatientInput;

export interface PredictionResponse {
  /** 0 = lower risk / negative class, 1 = higher risk / positive class */
  prediction: 0 | 1;
  label: string;
  /** Probability of the positive class, when the backend returns one. */
  probability?: number;
  model: string;
  source: "backend" | "mock";
}

export interface BulkRecordResult {
  id: string;
  prediction: 0 | 1;
  probability?: number;
}

export interface BulkPredictionResponse {
  total: number;
  positive: number;
  negative: number;
  model: string;
  results: BulkRecordResult[];
  source: "backend" | "mock";
}

export type LifestyleAnswerKey =
  | "activity"
  | "diet"
  | "smoking"
  | "alcohol"
  | "sleep"
  | "stress"
  | "weight";

export type LifestyleInput = Record<LifestyleAnswerKey, number>;

export type LifestyleRiskLevel = "lower" | "moderate" | "higher";

export interface LifestyleBreakdownItem {
  key: LifestyleAnswerKey;
  label: string;
  /** 0 (best) to 100 (worst) contribution score. */
  score: number;
}

export interface LifestylePredictionResponse {
  level: LifestyleRiskLevel;
  score: number;
  breakdown: LifestyleBreakdownItem[];
  recommendations: string[];
  source: "backend" | "mock";
}

export interface HealthResponse {
  status: "ok" | "unavailable";
  source: "backend" | "mock";
}

export interface ClinicalFeatureMeta {
  key: PatientInputKey;
  name: string;
  code: string;
  type: "Numerical" | "Categorical" | "Binary";
  description: string;
  unit?: string;
  min?: number;
  max?: number;
  step?: number;
  options?: { label: string; value: number }[];
  section: "basic" | "cardiac" | "exercise";
  control: "number" | "select" | "radio" | "slider";
}
