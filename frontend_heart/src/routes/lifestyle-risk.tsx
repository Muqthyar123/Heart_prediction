import { createFileRoute } from "@tanstack/react-router";
import { SiteLayout } from "@/layouts/SiteLayout";
import { LifestyleRiskPage } from "@/pages/LifestyleRiskPage";

const title = "Lifestyle Risk Assessment — CardioSight";
const description =
  "Answer seven guided lifestyle questions to receive a lifestyle-based heart risk overview and general wellness guidance.";

export const Route = createFileRoute("/lifestyle-risk")({
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
      <LifestyleRiskPage />
    </SiteLayout>
  ),
});
