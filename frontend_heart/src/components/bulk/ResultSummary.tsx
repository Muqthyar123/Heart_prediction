import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import type { BulkPredictionResponse } from "@/types";

export function ResultSummary({ data }: { data: BulkPredictionResponse }) {
  const chartData = [
    { name: "Higher risk", value: data.positive },
    { name: "Lower risk", value: data.negative },
  ];

  return (
    <div className="grid gap-4 lg:grid-cols-[1.4fr_1fr]">
      <div className="grid gap-4 sm:grid-cols-3">
        <div className="clinical-card p-5">
          <p className="font-display text-3xl font-bold">{data.total}</p>
          <p className="mt-1 text-sm text-muted-foreground">Total Patients</p>
        </div>
        <div className="clinical-card p-5">
          <p className="font-display text-3xl font-bold text-destructive">{data.positive}</p>
          <p className="mt-1 text-sm text-muted-foreground">Higher Risk</p>
        </div>
        <div className="clinical-card p-5">
          <p className="font-display text-3xl font-bold text-positive">{data.negative}</p>
          <p className="mt-1 text-sm text-muted-foreground">Lower Risk</p>
        </div>
        <div className="clinical-card p-5 sm:col-span-3">
          <p className="text-xs uppercase tracking-[0.15em] text-muted-foreground">Model used</p>
          <p className="mt-1.5 text-sm font-medium">{data.model}</p>
          {data.source === "mock" ? (
            <p className="mt-1 text-xs text-ai">
              Demo response — no prediction backend is connected yet.
            </p>
          ) : null}
        </div>
      </div>

      <div className="clinical-card p-5">
        <p className="text-xs uppercase tracking-[0.15em] text-muted-foreground">
          Prediction distribution
        </p>
        <div className="mt-2 h-48">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={chartData} dataKey="value" innerRadius={45} outerRadius={70} stroke="none">
                <Cell fill="var(--color-danger)" />
                <Cell fill="var(--color-positive)" />
              </Pie>
              <Tooltip
                contentStyle={{
                  background: "var(--color-obsidian)",
                  border: "1px solid var(--color-line)",
                  borderRadius: 12,
                  color: "var(--color-foreground)",
                  fontSize: 12,
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-2 flex justify-center gap-5 text-xs text-muted-foreground">
          <span className="flex items-center gap-1.5">
            <span className="size-2 rounded-full bg-destructive" /> Higher risk
          </span>
          <span className="flex items-center gap-1.5">
            <span className="size-2 rounded-full bg-positive" /> Lower risk
          </span>
        </div>
      </div>
    </div>
  );
}
