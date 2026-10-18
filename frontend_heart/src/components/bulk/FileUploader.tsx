import { FileSpreadsheet, UploadCloud } from "lucide-react";
import { useRef, useState } from "react";
import { ACCEPTED_EXTENSIONS, isAcceptedFile } from "@/utils/parseRecords";

interface FileUploaderProps {
  disabled?: boolean;
  onFileSelected: (file: File) => void;
  onReject: (message: string) => void;
}

export function FileUploader({ disabled, onFileSelected, onReject }: FileUploaderProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  function handleFiles(files: FileList | null) {
    const file = files?.[0];
    if (!file) return;
    if (!isAcceptedFile(file)) {
      onReject(`Unsupported file type. Accepted formats: ${ACCEPTED_EXTENSIONS.join(", ")}`);
      return;
    }
    onFileSelected(file);
  }

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        if (!disabled) setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDragging(false);
        if (!disabled) handleFiles(e.dataTransfer.files);
      }}
      className={`rounded-lg border border-dashed p-10 text-center backdrop-blur transition ${
        dragging ? "border-brand bg-brand/5" : "border-line bg-obsidian"
      } ${disabled ? "opacity-60" : ""}`}
    >
      <div className="mx-auto grid size-12 place-items-center rounded-xl border border-line bg-surface2 text-brand">
        <UploadCloud className="size-5" aria-hidden />
      </div>
      <h2 className="mt-4 font-display text-lg font-semibold">Upload Patient Data</h2>
      <p className="mx-auto mt-2 max-w-sm text-sm text-muted-foreground">
        Drag and drop your Excel file here or browse from your computer.
      </p>
      <button
        type="button"
        disabled={disabled}
        onClick={() => inputRef.current?.click()}
        className="btn-primary mt-5 px-5 py-2.5 disabled:cursor-not-allowed"
      >
        <FileSpreadsheet className="size-4" aria-hidden /> Browse files
      </button>
      <p className="mt-3 text-xs text-muted-foreground">
        Accepted formats: {ACCEPTED_EXTENSIONS.join(" · ")}
      </p>
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPTED_EXTENSIONS.join(",")}
        className="sr-only"
        aria-label="Upload patient data file"
        onChange={(e) => {
          handleFiles(e.target.files);
          e.target.value = "";
        }}
      />
    </div>
  );
}
