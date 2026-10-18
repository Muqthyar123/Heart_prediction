import { createFileRoute } from "@tanstack/react-router";
import { SiteLayout } from "@/layouts/SiteLayout";
import { SinglePredictionPage } from "@/pages/SinglePredictionPage";

const title = "Single Patient Prediction — CardioSight";
const description =
  "Enter 13 clinical values for one patient and generate a machine-learning heart disease risk prediction.";

export const Route = createFileRoute("/single-prediction")({
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
      <SinglePredictionPage />
    </SiteLayout>
  ),
});
