import { Activity, Loader2, Sparkles } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { ClinicalField } from "./FormFields";
import { FormSection } from "./FormSection";
import { CLINICAL_FEATURES, FORM_SECTIONS } from "@/utils/clinicalFeatures";
import { TooltipProvider } from "@/components/ui/tooltip";
import {
  validateField,
  validatePatientForm,
  type PatientFormErrors,
  type PatientFormValues,
} from "@/utils/validation";
import type { PatientInput, PatientInputKey } from "@/types";

interface PredictionFormProps {
  loading: boolean;
  onSubmit: (patient: PatientInput) => void;
}

export function PredictionForm({ loading, onSubmit }: PredictionFormProps) {
  // Slider controls always display a concrete value, so they start at their minimum.
  const [values, setValues] = useState<PatientFormValues>(() =>
    Object.fromEntries(
      CLINICAL_FEATURES.filter((f) => f.control === "slider").map((f) => [f.key, f.min ?? 0]),
    ),
  );
  const [errors, setErrors] = useState<PatientFormErrors>({});
  const [touched, setTouched] = useState(false);

  function setValue(key: PatientInputKey, value: number | undefined) {
    setValues((prev) => ({ ...prev, [key]: value }));
    if (touched || errors[key]) {
      setErrors((prev) => ({ ...prev, [key]: validateField(key, value) }));
    }
  }

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    const nextErrors = validatePatientForm(values);
    setErrors(nextErrors);
    setTouched(true);
    if (Object.keys(nextErrors).length > 0) {
      const firstKey = Object.keys(nextErrors)[0];
      document.getElementById(firstKey!)?.focus();
      return;
    }
    onSubmit(values as PatientInput);
  }

  const errorCount = Object.values(errors).filter(Boolean).length;

  function loadExample(example: PatientInput) {
    setValues({ ...example });
    setErrors({});
    setTouched(false);
  }

  return (
    <form onSubmit={handleSubmit} noValidate className="space-y-5">
      <div className="clinical-card flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-start gap-3">
          <span className="icon-well size-9 shrink-0"><Sparkles className="size-4" aria-hidden /></span>
          <div>
            <p className="text-sm font-semibold">Explore with a fictional example</p>
            <p className="mt-1 text-xs leading-relaxed text-muted-foreground">Sample values are illustrative only, not real patient records or clinical guidance.</p>
          </div>
        </div>
        <div className="flex shrink-0 flex-wrap gap-2">
          <Button type="button" variant="outline" size="sm" onClick={() => loadExample(DEMO_EXAMPLES.exampleA.values)} disabled={loading}>
            Example A
          </Button>
          <Button type="button" variant="outline" size="sm" onClick={() => loadExample(DEMO_EXAMPLES.exampleB.values)} disabled={loading}>
            Example B
          </Button>
        </div>
      </div>
      <TooltipProvider delayDuration={250}>
      {FORM_SECTIONS.map((section, index) => (
        <FormSection
          key={section.id}
          index={index + 1}
          title={section.title}
          description={section.description}
        >
          {CLINICAL_FEATURES.filter((f) => f.section === section.id).map((feature) => (
            <ClinicalField
              key={feature.key}
              feature={feature}
              value={values[feature.key]}
              error={errors[feature.key]}
              onChange={(value) => setValue(feature.key, value)}
            />
          ))}
        </FormSection>
      ))}
      </TooltipProvider>

      <div className="clinical-card flex flex-col gap-3 p-5 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-sm text-muted-foreground">
          {touched && errorCount > 0
            ? `${errorCount} field${errorCount > 1 ? "s" : ""} need attention before predicting.`
            : "All 13 clinical features are required."}
        </p>
        <button
          type="submit"
          disabled={loading}
          className="btn-primary px-6 py-3 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? (
            <Loader2 className="size-4 animate-spin" aria-hidden />
          ) : (
            <Activity className="size-4" aria-hidden />
          )}
          {loading ? "Analyzing…" : "Analyze Heart Risk"}
        </button>
      </div>
    </form>
  );
}

const DEMO_EXAMPLES = {
  exampleA: {
    name: "Example A",
    values: {
      age: 48, sex: 0, cp: 0, trestbps: 118, chol: 190, fbs: 0, restecg: 0,
      thalach: 170, exang: 0, oldpeak: 0, slope: 0, ca: 0, thal: 1,
    },
  },
  exampleB: {
    name: "Example B",
    values: {
      age: 67, sex: 1, cp: 3, trestbps: 155, chol: 270, fbs: 1, restecg: 1,
      thalach: 120, exang: 1, oldpeak: 2, slope: 2, ca: 2, thal: 3,
    },
  },
} satisfies Record<string, { values: PatientInput; name: string }>;
