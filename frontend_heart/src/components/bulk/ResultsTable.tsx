import { ArrowUpDown, Search } from "lucide-react";
import { useMemo, useState } from "react";
import type { BulkRecordResult } from "@/types";

type FilterValue = "all" | "positive" | "negative";
const PAGE_SIZE = 10;

export function ResultsTable({ results }: { results: BulkRecordResult[] }) {
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState<FilterValue>("all");
  const [sortDesc, setSortDesc] = useState(true);
  const [page, setPage] = useState(1);

  const rows = useMemo(() => {
    const filtered = results
      .filter((r) => r.id.toLowerCase().includes(query.trim().toLowerCase()))
      .filter((r) =>
        filter === "all" ? true : filter === "positive" ? r.prediction === 1 : r.prediction === 0,
      );
    return [...filtered].sort((a, b) => {
      const av = a.probability ?? a.prediction;
      const bv = b.probability ?? b.prediction;
      return sortDesc ? bv - av : av - bv;
    });
  }, [results, query, filter, sortDesc]);

  const pageCount = Math.max(1, Math.ceil(rows.length / PAGE_SIZE));
  const current = Math.min(page, pageCount);
  const visible = rows.slice((current - 1) * PAGE_SIZE, current * PAGE_SIZE);

  return (
    <div className="clinical-card overflow-hidden">
      <div className="flex flex-col gap-3 border-b border-line p-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative sm:w-64">
          <Search
            className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground"
            aria-hidden
          />
          <input
            type="search"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setPage(1);
            }}
            placeholder="Search patient ID"
            aria-label="Search patient ID"
            className="w-full rounded-lg border border-line bg-obsidian py-2 pl-9 pr-3 text-sm outline-none focus:border-brand"
          />
        </div>
        <div className="flex flex-wrap items-center gap-2">
          {(["all", "positive", "negative"] as FilterValue[]).map((value) => (
            <button
              key={value}
              type="button"
              onClick={() => {
                setFilter(value);
                setPage(1);
              }}
              className={`rounded-lg border px-3 py-1.5 text-xs transition ${
                filter === value
                  ? "border-brand bg-brand/10 text-brand"
                  : "border-line bg-obsidian text-muted-foreground hover:text-foreground"
              }`}
            >
              {value === "all" ? "All" : value === "positive" ? "Higher risk" : "Lower risk"}
            </button>
          ))}
          <button
            type="button"
            onClick={() => setSortDesc((v) => !v)}
            className="inline-flex items-center gap-1.5 rounded-lg border border-line bg-obsidian px-3 py-1.5 text-xs text-muted-foreground transition hover:text-foreground"
          >
            <ArrowUpDown className="size-3.5" aria-hidden />
            {sortDesc ? "Highest first" : "Lowest first"}
          </button>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[520px] text-sm">
          <caption className="sr-only">Bulk prediction results</caption>
          <thead>
            <tr className="border-b border-line text-left text-xs uppercase tracking-wider text-muted-foreground">
              <th scope="col" className="px-4 py-3 font-medium">
                Patient ID
              </th>
              <th scope="col" className="px-4 py-3 font-medium">
                Prediction
              </th>
              <th scope="col" className="px-4 py-3 font-medium">
                Risk / Probability
              </th>
              <th scope="col" className="px-4 py-3 font-medium">
                Status
              </th>
            </tr>
          </thead>
          <tbody>
            {visible.map((row) => (
              <tr key={row.id} className="border-b border-line/60 last:border-0">
                <td className="px-4 py-3 font-mono text-xs">{row.id}</td>
                <td className="px-4 py-3">
                  <span
                    className={`rounded-full border px-2.5 py-0.5 text-xs ${
                      row.prediction === 1
                        ? "border-destructive/30 bg-destructive/10 text-destructive"
                        : "border-positive/30 bg-positive/10 text-positive"
                    }`}
                  >
                    {row.prediction === 1 ? "Higher risk" : "Lower risk"}
                  </span>
                </td>
                <td className="px-4 py-3 text-muted-foreground">
                  {row.probability !== undefined ? `${Math.round(row.probability * 100)}%` : "—"}
                </td>
                <td className="px-4 py-3 text-muted-foreground">Processed</td>
              </tr>
            ))}
            {visible.length === 0 ? (
              <tr>
                <td colSpan={4} className="px-4 py-8 text-center text-muted-foreground">
                  No records match the current search or filter.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3 border-t border-line p-4 text-sm text-muted-foreground">
        <span>
          Showing {visible.length} of {rows.length} records
        </span>
        <div className="flex items-center gap-2">
          <button
            type="button"
            disabled={current === 1}
            onClick={() => setPage(current - 1)}
            className="rounded-lg border border-line bg-obsidian px-3 py-1.5 text-xs transition disabled:opacity-40"
          >
            Previous
          </button>
          <span className="text-xs">
            Page {current} of {pageCount}
          </span>
          <button
            type="button"
            disabled={current === pageCount}
            onClick={() => setPage(current + 1)}
            className="rounded-lg border border-line bg-obsidian px-3 py-1.5 text-xs transition disabled:opacity-40"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
