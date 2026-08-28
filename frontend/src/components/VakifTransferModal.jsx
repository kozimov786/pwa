import { useState } from "react";
import { generateVakifTransfer } from "../api/client";
import { useLanguage } from "../LanguageContext";

const EMPTY = {
  tarih: "",
  valor_tarihi: "",
  amount: "",
  currency: "USD",
  contract_no: "",
};

export default function VakifTransferModal({ company, onClose }) {
  const { t } = useLanguage();
  const [form, setForm] = useState(EMPTY);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);

  if (!company) return null;

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  function formatDate(iso) {
    if (!iso) return "";
    const [y, m, d] = iso.split("-");
    return `${d}/${m}/${y}`;
  }

  async function submit() {
    setBusy(true);
    setError(null);
    try {
      await generateVakifTransfer({
        ...form,
        company_key: company.key,
        tarih: formatDate(form.tarih),
        valor_tarihi: formatDate(form.valor_tarihi),
        amount: parseFloat(form.amount) || 0,
      });
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="glass-card w-full max-w-lg p-6 space-y-4">
        <div>
          <h2 className="text-lg font-semibold text-neon-cyan">{t("vakifModalTitle")}</h2>
          <p className="text-xs text-slate-400 mt-1">{company.label}</p>
          <p className="text-xs text-slate-500 mt-1">{t("vakifHint")}</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <Field label={t("tarih")} type="date" value={form.tarih} onChange={(v) => update("tarih", v)} />
          <Field label={t("valorTarihi")} type="date" value={form.valor_tarihi} onChange={(v) => update("valor_tarihi", v)} />
          <Field label={t("amount")} type="number" value={form.amount} onChange={(v) => update("amount", v)} />
          <div>
            <label className="text-xs text-slate-400">{t("currency")}</label>
            <select
              value={form.currency}
              onChange={(e) => update("currency", e.target.value)}
              className="w-full mt-1 bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm"
            >
              {["USD", "EUR", "CNY", "TRY"].map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>
          <div className="sm:col-span-2">
            <Field label={t("contractNo")} value={form.contract_no} onChange={(v) => update("contract_no", v)} />
          </div>
        </div>

        {error && <div className="text-sm text-red-400">{error}</div>}

        <div className="flex justify-end gap-2 pt-2">
          <button onClick={onClose} className="neon-btn">{t("cancel")}</button>
          <button onClick={submit} disabled={busy} className="action-btn">
            {busy ? t("generating") : `🏦 ${t("generatePdf")}`}
          </button>
        </div>
      </div>
    </div>
  );
}

function Field({ label, value, onChange, type = "text" }) {
  return (
    <div>
      <label className="text-xs text-slate-400">{label}</label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full mt-1 bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm
                   focus:outline-none focus:border-neon-cyan/60"
      />
    </div>
  );
}
