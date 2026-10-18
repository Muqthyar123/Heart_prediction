import type { LifestyleQuestionDef } from "@/utils/lifestyle";

interface LifestyleQuestionProps {
  question: LifestyleQuestionDef;
  value: number | undefined;
  onChange: (value: number) => void;
}

export function LifestyleQuestion({ question, value, onChange }: LifestyleQuestionProps) {
  return (
    <div className="rise-in">
      <h2 className="font-display text-xl font-semibold">{question.question}</h2>
      {question.helper ? (
        <p className="mt-2 text-sm text-muted-foreground">{question.helper}</p>
      ) : null}
      <div role="radiogroup" aria-label={question.title} className="mt-5 space-y-2.5">
        {question.options.map((option) => {
          const selected = value === option.value;
          return (
            <button
              key={option.label}
              type="button"
              role="radio"
              aria-checked={selected}
              onClick={() => onChange(option.value)}
              className={`flex w-full items-center gap-3 rounded-lg border px-4 py-3.5 text-left text-sm transition ${
                selected
                  ? "border-brand bg-brand/10"
                  : "border-line bg-surface hover:border-brand/40"
              }`}
            >
              <span
                className={`grid size-4 shrink-0 place-items-center rounded-full border ${
                  selected ? "border-brand" : "border-line"
                }`}
              >
                {selected ? <span className="size-2 rounded-full bg-brand" /> : null}
              </span>
              <span className="min-w-0">{option.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
