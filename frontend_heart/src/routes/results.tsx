import { createFileRoute } from "@tanstack/react-router";
import { SiteLayout } from "@/layouts/SiteLayout";
import { ResultsPage } from "@/pages/ResearchPage";
const title = "Research Results — CardioSight";
const description = "View the research evaluation workspace for CardioSight model results.";
export const Route = createFileRoute("/results")({ head: () => ({ meta: [{ title }, { name: "description", content: description }, { property: "og:title", content: title }, { property: "og:description", content: description }, { property: "og:type", content: "website" }, { name: "twitter:card", content: "summary_large_image" }] }), component: () => <SiteLayout><ResultsPage /></SiteLayout> });