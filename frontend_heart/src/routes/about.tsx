import { createFileRoute } from "@tanstack/react-router";
import { SiteLayout } from "@/layouts/SiteLayout";
import { AboutPage } from "@/pages/AboutPage";

const title = "About the Project — CardioSight";
const description =
  "Clinical features, machine-learning models and the hybrid stacking architecture behind the Advanced Heart Disease Prediction System.";

export const Route = createFileRoute("/about")({
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
      <AboutPage />
    </SiteLayout>
  ),
});
