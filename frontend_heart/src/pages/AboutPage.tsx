import { Link } from "@tanstack/react-router";
import { ArrowRight, CheckCircle2, Layers, ShieldAlert } from "lucide-react";
import { SectionHeader } from "@/components/common/SectionHeader";
import { PageShell } from "@/layouts/SiteLayout";
import {
  CLINICAL_FEATURES,
  FEATURE_IMPORTANCE_RANKING,
  ML_MODELS,
  getFeature,
} from "@/utils/clinicalFeatures";

const PIPELINE = [
  { title: "Data Collection", detail: "Clinical records with 13 standard cardiology features." },
  { title: "Preprocessing", detail: "Missing-value handling, encoding and feature scaling." },
  { title: "Model Training", detail: "Multiple classifiers trained and compared." },
  { title: "Hybrid Stacking", detail: "Base learners combined through a meta-learner." },
  { title: "Prediction", detail: "Final risk estimate returned to the interface." },
];

export function AboutPage() {
  return (
    <PageShell
      title="About the Project"
      subtitle="An overview of the clinical features, machine-learning models and hybrid architecture behind the Advanced Heart Disease Prediction System."
    >
      <div className="space-y-14">
        <section>
          <SectionHeader
            title="Clinical Features"
            description="The system evaluates thirteen standard cardiology attributes for every patient."
            aside={`${CLINICAL_FEATURES.length} features`}
          />
          <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {CLINICAL_FEATURES.map((feature) => (
              <div key={feature.key} className="clinical-card p-5">
                <div className="grid grid-cols-[minmax(0,1fr)_auto] items-start gap-3">
                  <h3 className="min-w-0 font-display font-semibold">{feature.name}</h3>
                  <span className="shrink-0 rounded-full border border-line bg-obsidian px-2 py-0.5 font-mono text-[11px] text-brand">
                    {feature.code}
                  </span>
                </div>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {feature.description}
                </p>
                <p className="mt-3 text-xs text-muted-foreground">{feature.type}</p>
              </div>
            ))}
          </div>
        </section>

        <section>
          <SectionHeader
            title="Machine Learning Models"
            description="Several classifiers were trained and compared before combining the strongest performers."
          />
          <div className="mt-6 grid gap-2.5 sm:grid-cols-2 lg:grid-cols-3">
            {ML_MODELS.map((model) => {
              const hybrid = model.includes("Stacking");
              return (
                <div
                  key={model}
                  className={`flex items-center gap-2.5 rounded-lg border px-4 py-3 text-sm ${
                    hybrid
                      ? "border-brand/30 bg-brand/5 text-brand"
                      : "border-line bg-surface text-foreground"
                  }`}
                >
                  <CheckCircle2 className="size-4 shrink-0" aria-hidden />
                  <span className="min-w-0">{model}</span>
                </div>
              );
            })}
          </div>
          <p className="mt-4 text-xs text-muted-foreground">
            Model performance figures are intentionally not shown here — connect your trained
            backend to report measured results.
          </p>
        </section>

        <section>
          <SectionHeader
            title="Hybrid Stacking Architecture"
            description="Base learners generate predictions that a meta-learner combines into a single estimate."
          />
          <div className="mt-6 grid gap-4 lg:grid-cols-[1fr_1fr]">
            <div className="clinical-card p-6">
              <Layers className="size-5 text-brand" aria-hidden />
              <h3 className="mt-4 font-display font-semibold">Two-Level Design</h3>
              <ul className="mt-4 space-y-3 text-sm text-muted-foreground">
                <li className="rounded-lg border border-line bg-surface p-3.5">
                  <span className="font-medium text-foreground">Level 1 — Base learners.</span>{" "}
                  Random Forest, SVM and KNN learn complementary patterns in the clinical data.
                </li>
                <li className="rounded-lg border border-line bg-surface p-3.5">
                  <span className="font-medium text-foreground">Level 2 — Meta-learner.</span>{" "}
                  Logistic Regression combines the base predictions into the final risk class.
                </li>
              </ul>
            </div>
            <ol className="space-y-2.5">
              {PIPELINE.map((stage, index) => (
                <li
                  key={stage.title}
                  className="clinical-card flex items-start gap-3 p-4"
                >
                  <span className="grid size-7 shrink-0 place-items-center rounded-lg bg-surface2 font-display text-xs text-brand">
                    {index + 1}
                  </span>
                  <div className="min-w-0">
                    <p className="text-sm font-medium">{stage.title}</p>
                    <p className="text-sm text-muted-foreground">{stage.detail}</p>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section>
          <SectionHeader
            title="Feature Importance"
            description="Relative ranking of the features that most influence the model's decisions."
          />
          <ol className="mt-6 grid gap-2 sm:grid-cols-2">
            {FEATURE_IMPORTANCE_RANKING.map((key, index) => (
              <li
                key={key}
                className="clinical-card flex items-center gap-3 px-4 py-3 text-sm"
              >
                <span className="font-mono text-xs text-muted-foreground">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <span className="min-w-0 truncate">{getFeature(key).name}</span>
              </li>
            ))}
          </ol>
        </section>

        <section className="rounded-lg border border-warning/30 bg-warning/5 p-6">
          <div className="flex items-start gap-3">
            <ShieldAlert className="mt-0.5 size-5 shrink-0 text-warning" aria-hidden />
            <div className="min-w-0">
              <h2 className="font-display text-lg font-semibold">Medical Disclaimer</h2>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                This system is a decision-support and educational tool. It does not diagnose heart
                disease and must not replace examination, testing or advice from a qualified
                healthcare professional. Always consult a doctor about any health concern.
              </p>
            </div>
          </div>
        </section>

        <div className="flex flex-wrap gap-3">
          <Link to="/methodology" className="btn-primary px-5 py-2.5">
            Explore the methodology <ArrowRight className="size-4" aria-hidden />
          </Link>
          <Link to="/methodology" className="btn-secondary px-5 py-2.5">View methodology</Link>
        </div>
      </div>
    </PageShell>
  );
}
