import { createFileRoute } from "@tanstack/react-router";
import { SiteLayout } from "@/layouts/SiteLayout";
import { HomePage } from "@/pages/HomePage";

const title = "CardioSight — Advanced Heart Disease Prediction System";
const description =
  "Machine-learning powered heart disease risk prediction using 13 clinical features, hybrid stacking models, bulk analysis and lifestyle risk assessment.";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title },
      { name: "description", content: description },
      { property: "og:title", content: title },
      { property: "og:description", content: description },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: () => (
    <SiteLayout>
      <HomePage />
    </SiteLayout>
  ),
});
