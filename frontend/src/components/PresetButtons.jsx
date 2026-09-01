import { useState } from "react";
import { useLanguage } from "../LanguageContext";
import { productName } from "../utils/format";

export function ProductSelect({ products, selectedId, onSelect, onAddProduct }) {
  const { t, lang } = useLanguage();
  const [newName, setNewName] = useState("");
  const [busy, setBusy] = useState(false);

  async function submitNew() {
    const name = newName.trim();
    if (!name || busy) return;
    setBusy(true);
    try {
      await onAddProduct(name);
      setNewName("");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex flex-wrap gap-2 items-center">
      <select
        value={selectedId ?? ""}
        onChange={(e) => onSelect(parseInt(e.target.value, 10))}
        className="bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm min-w-[180px]
                   focus:outline-none focus:border-neon-cyan/60"
      >
        {products.length === 0 && <option value="">{t("noProducts")}</option>}
        {products.map((p) => (
          <option key={p.id} value={p.id}>
            {productName(p, lang)}
          </option>
        ))}
      </select>

      <input
        type="text"
        value={newName}
        onChange={(e) => setNewName(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && submitNew()}
        placeholder={t("newProductPlaceholder")}
        className="bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm w-44
                   focus:outline-none focus:border-neon-cyan/60"
      />
      <button onClick={submitNew} disabled={busy || !newName.trim()} className="neon-btn">
        {busy ? "…" : t("addButton")}
      </button>
    </div>
  );
}

const WEIGHT_PRESETS_KG = [20000, 21000, 22000, 20800];

export function WeightPresets({ weightKg, onChange }) {
  const { t } = useLanguage();
  return (
    <div className="flex flex-wrap items-center gap-2">
      {WEIGHT_PRESETS_KG.map((kg) => (
        <button
          key={kg}
          onClick={() => onChange(kg)}
          className={`neon-btn ${weightKg === kg ? "neon-btn-active" : ""}`}
        >
          {kg.toLocaleString()} kg
        </button>
      ))}
      <input
        type="number"
        min="0"
        step="100"
        value={weightKg}
        onChange={(e) => onChange(parseFloat(e.target.value) || 0)}
        className="w-28 bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm
                   focus:outline-none focus:border-neon-cyan/60"
        placeholder={t("customWeightPlaceholder")}
      />
    </div>
  );
}
