export function ProductPresets({ products, selectedId, onSelect }) {
  return (
    <div className="flex flex-wrap gap-2">
      {products.map((p) => (
        <button
          key={p.id}
          onClick={() => onSelect(p.id)}
          className={`neon-btn ${selectedId === p.id ? "neon-btn-active" : ""}`}
        >
          {p.name}
        </button>
      ))}
    </div>
  );
}

const TONNAGE_PRESETS = [21, 22];

export function TonnagePresets({ tonnage, onChange }) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      {TONNAGE_PRESETS.map((t) => (
        <button
          key={t}
          onClick={() => onChange(t)}
          className={`neon-btn ${tonnage === t ? "neon-btn-active" : ""}`}
        >
          {t} t
        </button>
      ))}
      <input
        type="number"
        min="0"
        step="0.1"
        value={tonnage}
        onChange={(e) => onChange(parseFloat(e.target.value) || 0)}
        className="w-24 bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm
                   focus:outline-none focus:border-neon-cyan/60"
        placeholder="Custom t"
      />
    </div>
  );
}

const CURRENCIES = ["USD", "CNY", "EUR"];

export function CurrencyToggle({ currency, onChange }) {
  return (
    <div className="flex gap-2">
      {CURRENCIES.map((c) => (
        <button
          key={c}
          onClick={() => onChange(c)}
          className={`neon-btn ${currency === c ? "neon-btn-active" : ""}`}
        >
          {c}
        </button>
      ))}
    </div>
  );
}
