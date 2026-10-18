/**
 * Centralized service layer.
 *
 * Frontend-only for now: every function returns locally generated demo data
 * (tagged `source: "mock"`). To connect Flask later, replace the body of each
 * function with a fetch call — the UI depends only on these signatures.
 */
import type {
  BulkPredictionResponse,
  LifestyleInput,
  LifestylePredictionResponse,
  PatientInput,
  PredictionResponse,
} from "@/types";
import { mockBulkPredict, mockLifestyleRisk, mockPredict } from "./mockApi";

export function predictSingle(patient: PatientInput): Promise<PredictionResponse> {
  // Future: POST /predict
  return mockPredict(patient);
}

export function predictBulk(_file: File, rows: PatientInput[]): Promise<BulkPredictionResponse> {
  // Future: POST /bulk-predict (multipart)
  return mockBulkPredict(rows);
}

export function assessLifestyle(input: LifestyleInput): Promise<LifestylePredictionResponse> {
  // Future: POST /lifestyle-risk
  return mockLifestyleRisk(input);
}
