import type { ClinicalFeatureMeta, PatientInput, PatientInputKey } from "@/types";

/** The 13 clinical features used by the model, with human-readable option labels. */
export const CLINICAL_FEATURES: ClinicalFeatureMeta[] = [
  {
    key: "age",
    name: "Age",
    code: "age",
    type: "Numerical",
    description: "Patient age in years",
    unit: "years",
    min: 1,
    max: 120,
    step: 1,
    section: "basic",
    control: "number",
  },
  {
    key: "sex",
    name: "Sex",
    code: "sex",
    type: "Binary",
    description: "Biological sex recorded in the dataset",
    options: [
      { label: "Female", value: 0 },
      { label: "Male", value: 1 },
    ],
    section: "basic",
    control: "radio",
  },
  {
    key: "cp",
    name: "Chest Pain Type",
    code: "cp",
    type: "Categorical",
    description: "Type of chest pain reported by the patient",
    options: [
      { label: "Typical angina", value: 0 },
      { label: "Atypical angina", value: 1 },
      { label: "Non-anginal pain", value: 2 },
      { label: "Asymptomatic", value: 3 },
    ],
    section: "cardiac",
    control: "select",
  },
  {
    key: "trestbps",
    name: "Resting Blood Pressure",
    code: "trestbps",
    type: "Numerical",
    description: "Resting blood pressure on admission",
    unit: "mmHg",
    min: 50,
    max: 260,
    step: 1,
    section: "cardiac",
    control: "number",
  },
  {
    key: "chol",
    name: "Serum Cholesterol",
    code: "chol",
    type: "Numerical",
    description: "Serum cholesterol measurement",
    unit: "mg/dl",
    min: 50,
    max: 700,
    step: 1,
    section: "cardiac",
    control: "number",
  },
  {
    key: "fbs",
    name: "Fasting Blood Sugar",
    code: "fbs",
    type: "Binary",
    description: "Whether fasting blood sugar is greater than 120 mg/dl",
    options: [
      { label: "120 mg/dl or lower", value: 0 },
      { label: "Above 120 mg/dl", value: 1 },
    ],
    section: "cardiac",
    control: "radio",
  },
  {
    key: "restecg",
    name: "Resting ECG",
    code: "restecg",
    type: "Categorical",
    description: "Resting electrocardiographic result",
    options: [
      { label: "Normal", value: 0 },
      { label: "ST-T wave abnormality", value: 1 },
      { label: "Left ventricular hypertrophy", value: 2 },
    ],
    section: "cardiac",
    control: "select",
  },
  {
    key: "thalach",
    name: "Maximum Heart Rate",
    code: "thalach",
    type: "Numerical",
    description: "Maximum heart rate achieved during testing",
    unit: "bpm",
    min: 40,
    max: 250,
    step: 1,
    section: "cardiac",
    control: "number",
  },
  {
    key: "exang",
    name: "Exercise-Induced Angina",
    code: "exang",
    type: "Binary",
    description: "Angina triggered by exercise",
    options: [
      { label: "No", value: 0 },
      { label: "Yes", value: 1 },
    ],
    section: "cardiac",
    control: "radio",
  },
  {
    key: "oldpeak",
    name: "ST Depression",
    code: "oldpeak",
    type: "Numerical",
    description: "ST depression induced by exercise relative to rest",
    unit: "mm",
    min: 0,
    max: 10,
    step: 0.1,
    section: "exercise",
    control: "slider",
  },
  {
    key: "slope",
    name: "ST-Segment Slope",
    code: "slope",
    type: "Categorical",
    description: "Slope of the peak exercise ST segment",
    options: [
      { label: "Upsloping", value: 0 },
      { label: "Flat", value: 1 },
      { label: "Downsloping", value: 2 },
    ],
    section: "exercise",
    control: "select",
  },
  {
    key: "ca",
    name: "Number of Major Vessels",
    code: "ca",
    type: "Categorical",
    description: "Major vessels coloured by fluoroscopy",
    options: [
      { label: "0 vessels", value: 0 },
      { label: "1 vessel", value: 1 },
      { label: "2 vessels", value: 2 },
      { label: "3 vessels", value: 3 },
      { label: "4 vessels", value: 4 },
    ],
    section: "exercise",
    control: "select",
  },
  {
    key: "thal",
    name: "Thalassemia",
    code: "thal",
    type: "Categorical",
    description: "Thalassemia blood-flow test result",
    options: [
      { label: "Normal", value: 1 },
      { label: "Fixed defect", value: 2 },
      { label: "Reversible defect", value: 3 },
    ],
    section: "exercise",
    control: "select",
  },
];

export const REQUIRED_COLUMNS: PatientInputKey[] = CLINICAL_FEATURES.map((f) => f.key);

export const FORM_SECTIONS = [
  {
    id: "basic" as const,
    title: "Basic Information",
    description: "Demographic details recorded at intake.",
  },
  {
    id: "cardiac" as const,
    title: "Cardiac Information",
    description: "Resting measurements and reported symptoms.",
  },
  {
    id: "exercise" as const,
    title: "Exercise / Clinical Indicators",
    description: "Findings from exercise testing and imaging.",
  },
];

/** Ranking of features by importance as reported in the project's analysis. */
export const FEATURE_IMPORTANCE_RANKING: PatientInputKey[] = [
  "cp",
  "thalach",
  "ca",
  "oldpeak",
  "thal",
  "age",
  "chol",
  "trestbps",
  "exang",
  "slope",
];

export const ML_MODELS = [
  "Logistic Regression",
  "Random Forest",
  "Support Vector Machine",
  "K-Nearest Neighbors",
  "Decision Tree",
  "Naive Bayes",
  "AdaBoost",
  "Neural Network (MLP)",
  "XGBoost",
  "LightGBM",
  "CatBoost",
  "Extra Trees",
  "Hybrid Stacking Classifier",
];

export function getFeature(key: PatientInputKey): ClinicalFeatureMeta {
  return CLINICAL_FEATURES.find((f) => f.key === key)!;
}

export function optionLabel(key: PatientInputKey, value: number): string {
  const feature = getFeature(key);
  return feature.options?.find((o) => o.value === value)?.label ?? String(value);
}

export const EMPTY_PATIENT: Partial<PatientInput> = {};
