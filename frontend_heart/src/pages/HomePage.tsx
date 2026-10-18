import { Link } from "@tanstack/react-router";
import { motion } from "framer-motion";
import {
  Activity,
  
  ChartNoAxesCombined,
  GitMerge,
  HeartPulse,
  Microscope,
  ScanSearch,
  ShieldCheck,
} from "lucide-react";
import { HeartVisual } from "@/components/common/HeartVisual";
import { btnPrimary, btnSecondary } from "@/components/common/Kit";

const FEATURES = [
  { title: "Hybrid Stacking Ensemble", detail: "Random Forest, SVM and KNN predictions combined by a Logistic Regression meta-learner.", icon: GitMerge, to: "/methodology" },
  { title: "Feature Analysis", detail: "Human-readable clinical feature ranking for transparent research review.", icon: ScanSearch, to: "/explainable-ai" },
  { title: "Clinical Decision Support", detail: "A medically responsible interface that keeps prediction distinct from diagnosis.", icon: ShieldCheck, to: "/single-prediction" },
  { title: "Predictive Analytics", detail: "A results workspace prepared for measured research outputs and comparisons.", icon: ChartNoAxesCombined, to: "/results" },
  { title: "Research Methodology", detail: "Trace the complete data flow from patient inputs to final estimated class.", icon: Microscope, to: "/methodology" },
] as const;

export function HomePage() {
  return (
    <div>
      <section className="mx-auto grid min-h-[min(920px,calc(100svh-4rem))] max-w-7xl items-center gap-6 px-5 pb-10 pt-8 sm:gap-8 sm:pb-14 sm:pt-10 lg:grid-cols-[0.92fr_1.08fr] lg:px-8 lg:py-12">
        <motion.div >
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }} className="eyebrow inline-flex items-center gap-2 rounded-full border border-brand/20 bg-brand/5 px-3 py-1.5">
            <span className="size-1.5 rounded-full bg-brand pulse-ring" /> Advanced cardiovascular intelligence
          </motion.div>
          <h1 className="mt-6 max-w-2xl font-display text-3xl font-bold leading-[1.08] sm:mt-7 sm:text-4xl lg:text-[2.75rem]">
            Predict Tomorrow&apos;s Risk. <span className="text-brand">Protect Today&apos;s Heart.</span>
          </h1>
          <p className="mt-4 max-w-xl text-base leading-relaxed sm:text-[17px] text-muted-foreground sm:mt-6">
            AI-powered heart attack risk assessment using a hybrid stacking ensemble framework.
          </p>
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }} className="mt-7 flex flex-wrap gap-3 sm:mt-9">
            <Link to="/single-prediction" className={btnPrimary}>
              <HeartPulse className="size-4" aria-hidden /> Predict Heart Risk
            </Link>
            <Link to="/methodology" className={btnSecondary}>
              Explore the AI Model
            </Link>
          </motion.div>
          <div className="mt-8 flex flex-wrap gap-x-6 gap-y-2 text-xs text-muted-foreground"><span className="flex items-center gap-2"><span className="size-1 rounded-full bg-brand" />13 clinical features</span><span className="flex items-center gap-2"><span className="size-1 rounded-full bg-blue" />Hybrid ensemble</span><span className="flex items-center gap-2"><span className="size-1 rounded-full bg-ai" />Research use</span></div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.05 }}
          className="relative isolate"
        >
          <HeartVisual />
        </motion.div>
      </section>

      <section className="section-band border-y border-line/70">
        <div className="mx-auto grid max-w-7xl grid-cols-2 gap-px bg-line/70 lg:grid-cols-3">
          {[["13", "Clinical Features"], ["3 → 1", "Stacking Design"], ["100%", "Frontend Demo"]].map(([value, label]) => <div key={label} className="bg-background px-5 py-7"><p className="font-display text-3xl font-bold text-brand">{value}</p><p className="mt-1 text-xs uppercase tracking-[0.12em] text-muted-foreground">{label}</p></div>)}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-5 py-20 lg:px-8">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div><p className="eyebrow">Research capabilities</p><h2 className="mt-3 font-display text-3xl font-bold sm:text-4xl">Clinical intelligence, clearly structured</h2></div>
          <Link to="/about" className="text-link">Explore the project <span>→</span></Link>
        </div>
        <div className="mt-9 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map(({ title, detail, icon: Icon, to }, i) => (
            <motion.div
              key={title}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "200px" }}
              transition={{ duration: 0.2 }}
            >
              <Link
                to={to}
                className="clinical-card group flex h-full flex-col p-6"
              >
                <span className="icon-well">
                  <Icon className="size-5" aria-hidden />
                </span>
                <h3 className="mt-5 font-display text-lg font-semibold">{title}</h3>
                <p className="mt-2 flex-1 text-sm leading-relaxed text-muted-foreground">{detail}</p>
                <span className="mt-5 text-sm font-medium text-brand">Explore <span className="inline-block transition group-hover:translate-x-1">→</span></span>
              </Link>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  );
}
