import { createFileRoute } from "@tanstack/react-router";
import { SiteLayout } from "@/layouts/SiteLayout";
import { ExplainableAiPage } from "@/pages/ResearchPage";
const title = "Explainable AI — CardioSight";
const description = "Explore feature ranking and responsible model explanations in CardioSight.";
export const Route = createFileRoute("/explainable-ai")({ head: () => ({ meta: [{ title }, { name: "description", content: description }, { property: "og:title", content: title }, { property: "og:description", content: description }, { property: "og:type", content: "website" }, { name: "twitter:card", content: "summary_large_image" }] }), component: () => <SiteLayout><ExplainableAiPage /></SiteLayout> });