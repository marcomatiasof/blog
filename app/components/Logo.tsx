export default function Logo({ className = "" }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 300 48"
      role="img"
      aria-label="AIMonetiza"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Circuito à esquerda do "AI" */}
      <g fill="none" stroke="var(--color-brand-600, #1f5ae4)" strokeWidth="2.4">
        <circle cx="6" cy="12" r="4" fill="var(--color-brand-600, #1f5ae4)" stroke="none" />
        <circle cx="6" cy="34" r="4" fill="var(--color-brand-600, #1f5ae4)" stroke="none" />
        <circle cx="2.5" cy="23" r="3.2" fill="var(--color-brand-600, #1f5ae4)" stroke="none" />
        <path d="M9 12 H22 M9 34 H22 M5 23 H18" strokeLinecap="round" />
      </g>

      {/* AI — sempre azul */}
      <text
        x="26"
        y="36"
        fontFamily="ui-sans-serif, system-ui, 'Segoe UI', Roboto, Arial, sans-serif"
        fontSize="34"
        fontWeight="800"
        fill="var(--color-brand-600, #1f5ae4)"
        letterSpacing="-1"
      >
        AI
      </text>

      {/* Monetiza — acompanha a cor do tema (claro/escuro) */}
      <text
        x="78"
        y="36"
        fontFamily="ui-sans-serif, system-ui, 'Segoe UI', Roboto, Arial, sans-serif"
        fontSize="34"
        fontWeight="800"
        fill="currentColor"
        letterSpacing="-1"
      >
        Monetiza
      </text>

      {/* Seta de crescimento */}
      <g stroke="var(--color-brand-600, #1f5ae4)" strokeWidth="3" fill="none" strokeLinecap="round" strokeLinejoin="round">
        <path d="M262 30 L272 20 L280 26 L292 10" />
        <path d="M285 10 H292 V17" />
      </g>
    </svg>
  );
}
