interface RiskIndicatorProps {
  /** 0–1 value for the ring. */
  probability?: number;
  positive: boolean;
  label?: string;
  size?: number;
}

export function RiskIndicator({ probability, positive, label = "Estimated", size = 132 }: RiskIndicatorProps) {
  const stroke = 9;
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const normalized = probability ?? 0;
  const offset = circumference * (1 - normalized);

  return (
    <div className="relative shrink-0" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90" aria-hidden>
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none" strokeWidth={stroke} className="stroke-line" />
        {probability !== undefined ? (
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className={`transition-all duration-1000 ${positive ? "stroke-destructive" : "stroke-positive"}`}
          />
        ) : null}
      </svg>
      <div className="absolute inset-0 grid place-items-center text-center">
        <div>
          <p className="font-display text-xl font-bold">{probability === undefined ? (positive ? "Higher" : "Lower") : `${Math.round(probability * 100)}%`}</p>
          <p className="px-2 text-[10px] uppercase tracking-wider text-muted-foreground">{probability === undefined ? "Risk class" : label}</p>
        </div>
      </div>
    </div>
  );
}
