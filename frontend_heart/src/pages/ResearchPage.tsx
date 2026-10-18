import { Link } from "@tanstack/react-router";
import { motion } from "framer-motion";
import type { ReactNode } from "react";
import {
  Activity,
  ArrowRight,
  BarChart3,
  BrainCircuit,
  CheckCircle2,
  Database,
  FileSearch,
  GitMerge,
  Layers3,
  ScanSearch,
  SlidersHorizontal,
} from "lucide-react";
import { PageShell } from "@/layouts/SiteLayout";
import { FEATURE_IMPORTANCE_RANKING, ML_MODELS, getFeature } from "@/utils/clinicalFeatures";

const fade = {
  initial: { opacity: 0, y: 18 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-80px" },
};

function ResearchCard({ icon: Icon, title, children }: { icon: typeof Activity; title: string; children: ReactNode }) {
  return (
    <motion.article {...fade} className="clinical-card group p-6">
      <span className="icon-well"><Icon className="size-5 transition-transform duration-300 group-hover:-translate-y-0.5" aria-hidden /></span>
      <h2 className="mt-5 font-display text-xl font-semibold">{title}</h2>
      <div className="mt-3 text-sm leading-relaxed text-muted-foreground">{children}</div>
    </motion.article>
  );
}

export function ModelsPage() {
  return (
    <PageShell title="Machine Learning Models" subtitle="A comparative model suite culminating in a hybrid stacking classifier for cardiovascular risk research.">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {ML_MODELS.map((model, index) => (
          <motion.div key={model} {...fade} transition={{ delay: index * 0.035 }} className={`clinical-card group flex items-center gap-4 p-5 ${model.includes("Stacking") ? "ai-card sm:col-span-2 lg:col-span-1" : ""}`}>
            <span className="grid size-10 shrink-0 place-items-center rounded-lg border border-brand/20 bg-brand/10 font-mono text-xs text-brand">{String(index + 1).padStart(2, "0")}</span>
            <div><p className="font-medium">{model}</p><p className="mt-1 text-xs text-muted-foreground">{model.includes("Stacking") ? "Ensemble prediction layer" : "Candidate base classifier"}</p></div>
          </motion.div>
        ))}
      </div>
      <div className="mt-8 flex items-center justify-between gap-4 rounded-lg border border-line bg-obsidian/70 p-5">
        <p className="text-sm text-muted-foreground">Measured performance values appear only when connected to the trained research output.</p>
        <Link to="/methodology" className="text-link shrink-0">View methodology <ArrowRight className="size-4" /></Link>
      </div>
    </PageShell>
  );
}

const PIPELINE = [
  [Database, "Patient Data", "13 clinical attributes"],
  [SlidersHorizontal, "Preprocessing", "Clean, encode and scale"],
  [ScanSearch, "Feature Selection", "Retain relevant signals"],
  [BrainCircuit, "ML Models", "RF · SVM · KNN"],
  [GitMerge, "Hybrid Stacking", "Combine base predictions"],
  [Layers3, "Meta-Learner", "Logistic Regression"],
  [Activity, "Risk Prediction", "Final estimated class"],
] as const;

export function MethodologyPage() {
  return (
    <PageShell title="Research Methodology" subtitle="A transparent view of how clinical inputs move through the project’s hybrid stacking architecture.">
      <div className="pipeline-grid">
        {PIPELINE.map(([Icon, title, detail], index) => (
          <motion.div key={title} {...fade} transition={{ delay: index * 0.08 }} className="pipeline-node group">
            <span className="icon-well"><Icon className="size-5" aria-hidden /></span>
            <p className="mt-4 font-display font-semibold">{title}</p><p className="mt-1 text-xs text-muted-foreground">{detail}</p>
            {index < PIPELINE.length - 1 ? <span className="pipeline-connector" aria-hidden /> : null}
          </motion.div>
        ))}
      </div>
      <div className="mt-10 grid gap-4 md:grid-cols-3">
        <ResearchCard icon={Database} title="Input Layer">Standard heart-disease dataset fields are validated before processing.</ResearchCard>
        <ResearchCard icon={GitMerge} title="Ensemble Layer">Random Forest, SVM and KNN predictions feed the stacking layer.</ResearchCard>
        <ResearchCard icon={CheckCircle2} title="Decision Layer">A Logistic Regression meta-learner produces the final model class.</ResearchCard>
      </div>
    </PageShell>
  );
}

export function ExplainableAiPage() {
  return (
    <PageShell title="Explainable AI" subtitle="Understand which clinical signals carry the most influence in the project’s analysis—without turning a model estimate into a diagnosis.">
      <div className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
        <motion.section {...fade} className="clinical-card p-6 sm:p-8">
          <div className="flex items-center justify-between"><div><p className="eyebrow">Feature analysis</p><h2 className="mt-2 font-display text-2xl font-semibold">Importance ranking</h2></div><BarChart3 className="size-6 text-ai" aria-hidden /></div>
          <ol className="mt-7 space-y-4">
            {FEATURE_IMPORTANCE_RANKING.map((key, index) => (
              <li key={key} className="group">
                <div className="flex items-center justify-between gap-3 text-sm"><span>{getFeature(key).name}</span><span className="font-mono text-xs text-muted-foreground">#{index + 1}</span></div>
                <div className="mt-2 h-px overflow-hidden bg-line"><motion.div initial={{ width: 0 }} whileInView={{ width: "2.5rem" }} viewport={{ once: true }} transition={{ duration: 0.45, delay: index * 0.04 }} className="h-full bg-ai" /></div>
              </li>
            ))}
          </ol>
          <p className="mt-6 text-xs text-muted-foreground">Numbers communicate ranking order only, not measured contribution percentages.</p>
        </motion.section>
        <div className="grid gap-4">
          <ResearchCard icon={FileSearch} title="Why this prediction?">Explanations should connect the model output to the most influential supplied clinical features.</ResearchCard>
          <ResearchCard icon={ScanSearch} title="Clinical context">Specialized test values should always come from a report or qualified healthcare professional.</ResearchCard>
          <ResearchCard icon={BrainCircuit} title="Responsible AI">Model explanations support review and research; they do not establish a medical diagnosis.</ResearchCard>
        </div>
      </div>
    </PageShell>
  );
}

export function ResultsPage() {
  const metrics = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"];
  return (
    <PageShell title="Research Results" subtitle="A publication-ready analytics surface prepared for the project’s measured evaluation outputs.">
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
        {metrics.map((metric, index) => <motion.div key={metric} {...fade} transition={{ delay: index * 0.06 }} className="clinical-card p-5"><p className="text-xs uppercase tracking-[0.12em] text-muted-foreground">{metric}</p><p className="mt-4 font-display text-2xl font-semibold text-brand">Not connected</p><p className="mt-1 text-xs text-muted-foreground">Awaiting measured output</p></motion.div>)}
      </div>
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        {["Model Comparison", "Confusion Matrix", "Classification Report", "Training vs Testing Accuracy"].map((title, index) => (
          <motion.section key={title} {...fade} transition={{ delay: index * 0.08 }} className="clinical-card min-h-64 p-6">
            <div className="flex items-center justify-between"><h2 className="font-display text-lg font-semibold">{title}</h2><BarChart3 className="size-5 text-brand" aria-hidden /></div>
            <div className="mt-8 grid h-32 place-items-center rounded-lg border border-dashed border-line bg-obsidian/40"><p className="max-w-xs text-center text-sm text-muted-foreground">Connect the project’s evaluated results to render this visualization. No values are fabricated.</p></div>
          </motion.section>
        ))}
      </div>
    </PageShell>
  );
}