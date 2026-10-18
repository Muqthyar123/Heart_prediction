import type { ClinicalFeatureMeta } from "@/types";
import { Button } from "@/components/ui/button";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { CircleHelp } from "lucide-react";

interface FieldProps {
  feature: ClinicalFeatureMeta;
  value: number | undefined;
  error?: string | undefined;
  onChange: (value: number | undefined) => void;
}

function FieldWrapper({
  feature,
  error,
  children,
  valueHint,
}: {
  feature: ClinicalFeatureMeta;
  error?: string | undefined;
  children: React.ReactNode;
  valueHint?: string | undefined;
}) {
  const errorId = `${feature.key}-error`;
  return (
    <div>
      <div className="flex items-baseline justify-between gap-3">
        <label htmlFor={feature.key} className="text-sm font-medium">
          {feature.name}
          {feature.unit ? (
            <span className="ml-1.5 text-xs text-muted-foreground">({feature.unit})</span>
          ) : null}
        </label>
        <div className="flex items-center gap-1.5">
          <Tooltip>
            <TooltipTrigger asChild>
              <Button type="button" variant="ghost" size="icon" aria-label={`Clinical reference for ${feature.name}`} className="size-6 text-muted-foreground hover:text-brand">
                <CircleHelp className="size-3.5" aria-hidden />
              </Button>
            </TooltipTrigger>
            <TooltipContent side="top" className="max-w-64 text-left leading-relaxed">
              <p>{feature.description}</p>
              <p className="mt-1 text-primary-foreground/75">Dataset field: <span className="font-mono">{feature.code}</span>{feature.unit ? ` · Unit: ${feature.unit}` : ""}</p>
              {feature.options?.length ? <p className="mt-1 text-primary-foreground/75">Categories: {feature.options.map((option) => `${option.value} = ${option.label}`).join(" · ")}</p> : null}
            </TooltipContent>
          </Tooltip>
          <span className="font-mono text-[11px] text-muted-foreground">{valueHint ?? feature.code}</span>
        </div>
      </div>
      <div className="mt-2">{children}</div>
      {error ? (
        <p id={errorId} role="alert" className="mt-1.5 text-xs text-destructive">
          {error}
        </p>
      ) : (
        <p className="mt-1.5 text-xs text-muted-foreground">{feature.description}</p>
      )}
    </div>
  );
}

const controlClass =
  "w-full rounded-lg border bg-surface px-3 py-2.5 text-sm outline-none transition focus:border-brand";

export function NumberField({ feature, value, error, onChange }: FieldProps) {
  return (
    <FieldWrapper feature={feature} error={error}>
      <input
        id={feature.key}
        type="number"
        inputMode="decimal"
        min={feature.min}
        max={feature.max}
        step={feature.step}
        value={value ?? ""}
        aria-invalid={Boolean(error)}
        aria-describedby={error ? `${feature.key}-error` : undefined}
        onChange={(e) => onChange(e.target.value === "" ? undefined : Number(e.target.value))}
        className={`${controlClass} ${error ? "border-destructive" : "border-line"}`}
        placeholder={feature.min !== undefined ? `e.g. ${feature.min + 40}` : ""}
      />
    </FieldWrapper>
  );
}

export function SelectField({ feature, value, error, onChange }: FieldProps) {
  return (
    <FieldWrapper feature={feature} error={error}>
      <select
        id={feature.key}
        value={value ?? ""}
        aria-invalid={Boolean(error)}
        aria-describedby={error ? `${feature.key}-error` : undefined}
        onChange={(e) => onChange(e.target.value === "" ? undefined : Number(e.target.value))}
        className={`${controlClass} ${error ? "border-destructive" : "border-line"}`}
      >
        <option value="">Select an option</option>
        {feature.options?.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </FieldWrapper>
  );
}

export function RadioField({ feature, value, error, onChange }: FieldProps) {
  return (
    <FieldWrapper feature={feature} error={error}>
      <div role="radiogroup" aria-label={feature.name} className="flex flex-wrap gap-2">
        {feature.options?.map((option) => {
          const selected = value === option.value;
          return (
            <button
              key={option.value}
              type="button"
              role="radio"
              aria-checked={selected}
              onClick={() => onChange(option.value)}
              className={`rounded-lg border px-3.5 py-2 text-sm transition ${
                selected
                  ? "border-brand bg-brand/10 text-brand"
                  : "border-line bg-surface text-muted-foreground hover:text-foreground"
              }`}
            >
              {option.label}
            </button>
          );
        })}
      </div>
    </FieldWrapper>
  );
}

export function SliderField({ feature, value, error, onChange }: FieldProps) {
  const current = value ?? feature.min ?? 0;
  return (
    <FieldWrapper
      feature={feature}
      error={error}
      valueHint={`${current}${feature.unit ? ` ${feature.unit}` : ""}`}
    >
      <input
        id={feature.key}
        type="range"
        min={feature.min}
        max={feature.max}
        step={feature.step}
        value={current}
        aria-invalid={Boolean(error)}
        onChange={(e) => onChange(Number(e.target.value))}
        className="h-2 w-full cursor-pointer appearance-none rounded-full bg-surface2 accent-brand"
      />
    </FieldWrapper>
  );
}

export function ClinicalField(props: FieldProps) {
  switch (props.feature.control) {
    case "select":
      return <SelectField {...props} />;
    case "radio":
      return <RadioField {...props} />;
    case "slider":
      return <SliderField {...props} />;
    default:
      return <NumberField {...props} />;
  }
}
