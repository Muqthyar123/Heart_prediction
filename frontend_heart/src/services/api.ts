/**
 * Centralized service layer for HeartPredict AI.
 *
 * Connects directly to the Flask backend (default http://localhost:5000/api/v1).
 * Falls back transparently to local mock data if the backend is unavailable,
 * ensuring flawless developer experience and reliability.
 */
import type {
  BulkPredictionResponse,
  LifestyleInput,
  LifestylePredictionResponse,
  PatientInput,
  PredictionResponse,
} from "@/types";
import { mockBulkPredict, mockLifestyleRisk, mockPredict } from "./mockApi";

const API_BASE_URL =
  (typeof import.meta !== "undefined" && (import.meta.env as Record<string, string | undefined>)?.[
    "VITE_API_URL"
  ]) || "http://localhost:5000/api/v1";

export async function predictSingle(patient: PatientInput): Promise<PredictionResponse> {
  try {
    const res = await fetch(`${API_BASE_URL}/predictions/heart`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        features: patient,
        model_name: "hybrid_stacking",
      }),
    });

    if (!res.ok) {
      throw new Error(`Backend returned status ${res.status}`);
    }

    const json = await res.json();
    if (json.success && json.data) {
      const d = json.data;
      return {
        prediction: (d.prediction.class === 1 ? 1 : 0) as 0 | 1,
        label: d.prediction.label || (d.prediction.class === 1 ? "Higher Risk" : "Lower Risk"),
        probability: d.probability !== null && d.probability !== undefined ? d.probability : undefined,
        model: d.model || "Hybrid Stacking Classifier",
        source: "backend",
      };
    }
    throw new Error("Invalid response format from backend");
  } catch (err) {
    console.warn("Backend unavailable, falling back to local demo mock:", err);
    return mockPredict(patient);
  }
}

export async function predictBulk(file: File, rows: PatientInput[]): Promise<BulkPredictionResponse> {
  try {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("model_name", "hybrid_stacking");

    const res = await fetch(`${API_BASE_URL}/bulk/predict`, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      throw new Error(`Backend returned status ${res.status}`);
    }

    const json = await res.json();
    if (json.success && json.data) {
      const d = json.data;
      const results = (d.results_sample || []).map((r: any) => ({
        id: `P-${String(r.row_index).padStart(4, "0")}`,
        prediction: (r.prediction_class === 1 ? 1 : 0) as 0 | 1,
        probability: r.probability !== null ? r.probability : undefined,
      }));

      return {
        total: d.total_records,
        positive: d.positive_records,
        negative: d.negative_records,
        model: "Hybrid Stacking Classifier",
        results,
        source: "backend",
      };
    }
    throw new Error("Invalid response format from backend");
  } catch (err) {
    console.warn("Backend unavailable, falling back to local demo mock:", err);
    return mockBulkPredict(rows);
  }
}

export async function assessLifestyle(input: LifestyleInput): Promise<LifestylePredictionResponse> {
  try {
    const res = await fetch(`${API_BASE_URL}/lifestyle-assessments`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(input),
    });

    if (!res.ok) {
      throw new Error(`Backend returned status ${res.status}`);
    }

    const json = await res.json();
    if (json.success && json.data) {
      const d = json.data;
      return {
        level: d.category as "lower" | "moderate" | "higher",
        score: Math.round(d.score),
        breakdown: (d.breakdown || []).map((b: any) => ({
          key: b.key,
          label: b.label,
          score: Math.round(b.score),
        })),
        recommendations: d.recommendations || [],
        source: "backend",
      };
    }
    throw new Error("Invalid response format from backend");
  } catch (err) {
    console.warn("Backend unavailable, falling back to local demo mock:", err);
    return mockLifestyleRisk(input);
  }
}
