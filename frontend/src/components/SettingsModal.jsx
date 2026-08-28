import { useEffect, useState } from "react";
import { getExpenses, updateExpenses } from "../api/client";

const FIELDS = [
  { key: "cn_docs_cny", label: "CN Docs (jami, CNY)" },
  { key: "cn_osh_freight_usd", label: "CN - Osh Nakliye (jami, USD)" },
  { key: "kg_transit_usd", label: "KG Transit (jami, USD)" },
  { key: "osh_tashkent_freight_usd", label: "Osh - Tashkent Nakliye (jami, USD)" },
  { key: "uzb_transit_usd", label: "UZB Transit (jami, USD)" },
  { key: "tashkent_antep_freight_usd", label: "Tashkent - Antep Nakliye (jami, USD)" },
  { key: "tashkent_romania_freight_usd", label: "Tashkent - Ruminiya Nakliye (jami, USD)" },
  { key: "tashkent_baku_freight_usd", label: "Tashkent - Azerbaijan Nakliye (jami, USD)" },
  { key: "usd_cny_rate_fallback", label: "USD/CNY zaxira kurs (internet bo'lmasa)" },
];

export default function SettingsModal({ open, onClose }) {
  const [values, setValues] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (!open) return;
    setError(null);
    setSaved(false);
    getExpenses()
      .then(setValues)
      .catch((err) => setError(err.message));
  }, [open]);

  if (!open) return null;

  function update(key, v) {
    setValues((prev) => ({ ...prev, [key]: v }));
    setSaved(false);
  }

  async function save() {
    setBusy(true);
    setError(null);
    try {
      const updated = await updateExpenses(values);
      setValues(updated);
      setSaved(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="glass-card w-full max-w-lg p-6 space-y-4 max-h-[90vh] overflow-y-auto">
        <div>
          <h2 className="text-lg font-semibold text-neon-cyan">Rasxodlar sozlamalari</h2>
          <p className="text-xs text-slate-400 mt-1">
            Har bir qiymat — butun yuk (mashina) uchun jami xarajat. Hisoblashda avtomatik kg'ga bo'linadi.
          </p>
        </div>

        {!values && !error && <div className="text-sm text-slate-400">Yuklanmoqda…</div>}

        {values && (
          <div className="grid grid-cols-1 gap-3">
            {FIELDS.map((f) => (
              <div key={f.key}>
                <label className="text-xs text-slate-400">{f.label}</label>
                <input
                  type="number"
                  step="0.01"
                  value={values[f.key] ?? 0}
                  onChange={(e) => update(f.key, parseFloat(e.target.value) || 0)}
                  className="w-full mt-1 bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm
                             focus:outline-none focus:border-neon-cyan/60"
                />
              </div>
            ))}
          </div>
        )}

        {error && <div className="text-sm text-red-400">{error}</div>}
        {saved && <div className="text-sm text-neon-cyan">Saqlandi ✅</div>}

        <div className="flex justify-end gap-2 pt-2">
          <button onClick={onClose} className="neon-btn">Yopish</button>
          <button onClick={save} disabled={busy || !values} className="action-btn">
            {busy ? "Saqlanmoqda…" : "💾 Saqlash"}
          </button>
        </div>
      </div>
    </div>
  );
}
