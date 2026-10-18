import * as XLSX from "xlsx";
import { REQUIRED_COLUMNS } from "./clinicalFeatures";
import type { PatientInput } from "@/types";

export interface ParsedFile {
  fileName: string;
  rowCount: number;
  columns: string[];
  missingColumns: string[];
  rows: PatientInput[];
}

export const ACCEPTED_EXTENSIONS = [".xlsx", ".xls", ".csv"];

export function isAcceptedFile(file: File): boolean {
  return ACCEPTED_EXTENSIONS.some((ext) => file.name.toLowerCase().endsWith(ext));
}

/** Reads an Excel/CSV file and checks it against the 13 required feature columns. */
export async function parseRecordsFile(file: File): Promise<ParsedFile> {
  const buffer = await file.arrayBuffer();
  const workbook = XLSX.read(buffer, { type: "array" });
  const sheetName = workbook.SheetNames[0];
  if (!sheetName) throw new Error("The file does not contain any sheets.");

  const raw = XLSX.utils.sheet_to_json<Record<string, unknown>>(workbook.Sheets[sheetName]!, {
    defval: null,
  });
  if (raw.length === 0) throw new Error("The file does not contain any data rows.");

  const columns = Object.keys(raw[0]!).map((c) => c.trim());
  const normalized = columns.map((c) => c.toLowerCase());
  const missingColumns = REQUIRED_COLUMNS.filter((c) => !normalized.includes(c));

  const rows: PatientInput[] =
    missingColumns.length > 0
      ? []
      : raw.map((row) => {
          const lookup = new Map(
            Object.entries(row).map(([k, v]) => [k.trim().toLowerCase(), v]),
          );
          const record = {} as PatientInput;
          for (const key of REQUIRED_COLUMNS) {
            record[key] = Number(lookup.get(key) ?? 0);
          }
          return record;
        });

  return {
    fileName: file.name,
    rowCount: raw.length,
    columns,
    missingColumns,
    rows,
  };
}

export function resultsToCsv(
  rows: { id: string; prediction: 0 | 1; probability?: number }[],
): string {
  const header = "patient_id,prediction,risk_label,probability";
  const lines = rows.map(
    (r) =>
      `${r.id},${r.prediction},${r.prediction === 1 ? "Higher risk" : "Lower risk"},${
        r.probability !== undefined ? r.probability : ""
      }`,
  );
  return [header, ...lines].join("\n");
}

export function downloadCsv(fileName: string, csv: string): void {
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = fileName;
  anchor.click();
  URL.revokeObjectURL(url);
}
