interface SectionHeaderProps {
  title: string;
  description?: string;
  aside?: string;
  eyebrow?: string;
}

export function SectionHeader({ title, description, aside, eyebrow }: SectionHeaderProps) {
  return (
    <div className="flex flex-wrap items-end justify-between gap-4">
      <div className="min-w-0">
        {eyebrow ? (
          <p className="eyebrow mb-2">{eyebrow}</p>
        ) : null}
        <h2 className="text-2xl font-bold sm:text-3xl">{title}</h2>
        {description ? (
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
            {description}
          </p>
        ) : null}
      </div>
      {aside ? <span className="text-sm text-muted-foreground">{aside}</span> : null}
    </div>
  );
}
