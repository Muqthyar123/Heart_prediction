import { createFileRoute } from "@tanstack/react-router";
import { SiteLayout } from "@/layouts/SiteLayout";
import { MethodologyPage } from "@/pages/ResearchPage";
const title = "Research Methodology — CardioSight";
const description = "Review the CardioSight preprocessing, model, stacking, and meta-learner pipeline.";
export const Route = createFileRoute("/methodology")({ head: () => ({ meta: [{ title }, { name: "description", content: description }, { property: "og:title", content: title }, { property: "og:description", content: description }, { property: "og:type", content: "website" }, { name: "twitter:card", content: "summary_large_image" }] }), component: () => <SiteLayout><MethodologyPage /></SiteLayout> });