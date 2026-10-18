import { CLINICAL_FEATURES } from "./clinicalFeatures";
import type { PatientInput, PatientInputKey } from "@/types";

export type PatientFormValues = Partial<Record<PatientInputKey, number | undefined>>;
export type PatientFormErrors = Partial<Record<PatientInputKey, string>>;

/** Validates a single clinical field and returns an error message, or undefined when valid. */
export function validateField(key: PatientInputKey, value: number | undefined): string | undefined {
  const feature = CLINICAL_FEATURES.find((f) => f.key === key)!;

  if (value === undefined || Number.isNaN(value)) {
    return `${feature.name} is required`;
  }
  if (feature.options) {
    const allowed = feature.options.some((o) => o.value === value);
    return allowed ? undefined : `Select a valid ${feature.name.toLowerCase()}`;
  }
  if (value < 0) {
    return `${feature.name} cannot be negative`;
  }
  if (feature.min !== undefined && value < feature.min) {
    return `${feature.name} must be at least ${feature.min}${feature.unit ? ` ${feature.unit}` : ""}`;
  }
  if (feature.max !== undefined && value > feature.max) {
    return `${feature.name} must be ${feature.max}${feature.unit ? ` ${feature.unit}` : ""} or less`;
  }
  return undefined;
}

export function validatePatientForm(values: PatientFormValues): PatientFormErrors {
  const errors: PatientFormErrors = {};
  for (const feature of CLINICAL_FEATURES) {
    const message = validateField(feature.key, values[feature.key]);
    if (message) errors[feature.key] = message;
  }
  return errors;
}

export function isCompletePatient(values: PatientFormValues): values is PatientInput {
  return Object.keys(validatePatientForm(values)).length === 0;
}
