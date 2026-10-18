import type { LifestyleAnswerKey } from "@/types";

export interface LifestyleQuestionDef {
  key: LifestyleAnswerKey;
  step: number;
  title: string;
  question: string;
  helper?: string;
  /** Options ordered best-to-worst; value is a 0-100 risk contribution. */
  options: { label: string; value: number }[];
}

export const LIFESTYLE_QUESTIONS: LifestyleQuestionDef[] = [
  {
    key: "activity",
    step: 1,
    title: "Physical Activity",
    question: "How often do you do moderate or vigorous physical activity?",
    helper: "Brisk walking, cycling, sports or gym sessions of 30 minutes or more.",
    options: [
      { label: "5 or more days a week", value: 0 },
      { label: "3–4 days a week", value: 25 },
      { label: "1–2 days a week", value: 60 },
      { label: "Rarely or never", value: 100 },
    ],
  },
  {
    key: "diet",
    step: 2,
    title: "Diet",
    question: "How would you describe your typical diet?",
    options: [
      { label: "Mostly whole foods, vegetables and fruit", value: 0 },
      { label: "Balanced with occasional processed food", value: 30 },
      { label: "Frequent fried, salty or processed meals", value: 70 },
      { label: "Mostly fast food and sugary drinks", value: 100 },
    ],
  },
  {
    key: "smoking",
    step: 3,
    title: "Smoking / Tobacco",
    question: "Do you use tobacco in any form?",
    options: [
      { label: "Never used", value: 0 },
      { label: "Former user, quit over a year ago", value: 30 },
      { label: "Occasional use", value: 70 },
      { label: "Daily use", value: 100 },
    ],
  },
  {
    key: "alcohol",
    step: 4,
    title: "Alcohol",
    question: "How often do you drink alcohol?",
    options: [
      { label: "Never", value: 0 },
      { label: "Occasionally, within low-risk limits", value: 25 },
      { label: "Several times a week", value: 65 },
      { label: "Daily or heavy sessions", value: 100 },
    ],
  },
  {
    key: "sleep",
    step: 5,
    title: "Sleep",
    question: "On an average night, how much do you sleep?",
    options: [
      { label: "7–8 hours, good quality", value: 0 },
      { label: "6–7 hours", value: 30 },
      { label: "5–6 hours or often disturbed", value: 70 },
      { label: "Less than 5 hours", value: 100 },
    ],
  },
  {
    key: "stress",
    step: 6,
    title: "Stress",
    question: "How would you rate your everyday stress level?",
    options: [
      { label: "Low and well managed", value: 0 },
      { label: "Moderate but manageable", value: 35 },
      { label: "Often high", value: 70 },
      { label: "Constantly high", value: 100 },
    ],
  },
  {
    key: "weight",
    step: 7,
    title: "Weight / General Health",
    question: "How would you describe your current weight and general health?",
    options: [
      { label: "Healthy weight, no known conditions", value: 0 },
      { label: "Slightly above healthy weight", value: 35 },
      { label: "Overweight, or one managed condition", value: 70 },
      { label: "Significantly overweight, or multiple conditions", value: 100 },
    ],
  },
];

export const LIFESTYLE_LABELS: Record<LifestyleAnswerKey, string> = {
  activity: "Physical Activity",
  diet: "Diet",
  smoking: "Smoking",
  alcohol: "Alcohol",
  sleep: "Sleep",
  stress: "Stress",
  weight: "Weight / General Health",
};

export const GENERAL_RECOMMENDATIONS = [
  "Maintain regular physical activity across the week",
  "Follow a balanced diet rich in vegetables, fruit and whole grains",
  "Avoid smoking and other tobacco products",
  "Maintain healthy and consistent sleep habits",
  "Manage stress with rest, support and routine",
  "Keep regular check-ups with a qualified healthcare professional",
];
