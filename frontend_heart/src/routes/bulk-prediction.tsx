import { createFileRoute } from "@tanstack/react-router";
import { SiteLayout } from "@/layouts/SiteLayout";
import { BulkPredictionPage } from "@/pages/BulkPredictionPage";

const title = "Bulk Prediction — CardioSight";
const description =
  "Upload an Excel or CSV file of patient records and generate heart disease risk predictions for every row.";

export const Route = createFileRoute("/bulk-prediction")({
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
      <BulkPredictionPage />
    </SiteLayout>
  ),
});
