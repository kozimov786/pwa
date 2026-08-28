import { useMemo, useState } from "react";
import { generateInvoice } from "../api/client";
import { useLanguage } from "../LanguageContext";

const EMPTY = {
  tarih: "",
  contract_no: "",
  unit_price: "",
  total_price: "",
  currency: "USD",
};

export default function InvoiceModal({ company, onClose }) {
  const { t } = useLanguage();
  const [form, setForm] = useState(EMPTY);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);

  const quantity = useMemo(() => {
    const unit = parseFloat(form.unit_price);
    const total = parseFloat(form.total_price);
    if (!unit || !total) return null;
    return total / unit;
  }, [form.unit_price, form.total_price]);

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
      await generateInvoice({
        ...form,
        company_key: company.key,
        tarih: formatDate(form.tarih),
        unit_price: parseFloat(form.unit_price) || 0,
        total_price: parseFloat(form.total_price) || 0,
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
          <h2 className="text-lg font-semibold text-neon-cyan">{t("invoiceModalTitle")}</h2>
          <p className="text-xs text-slate-400 mt-1">{company.label}</p>
          <p className="text-xs text-slate-500 mt-1">{t("vakifHint")}</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <Field label={t("tarih")} type="date" value={form.tarih} onChange={(v) => update("tarih", v)} />
          <Field label={t("contractNo")} value={form.contract_no} onChange={(v) => update("contract_no", v)} />
          <Field label={t("unitPrice")} type="number" value={form.unit_price} onChange={(v) => update("unit_price", v)} />
          <Field label={t("totalPrice")} type="number" value={form.total_price} onChange={(v) => update("total_price", v)} />
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
          <div>
            <label className="text-xs text-slate-400">{t("quantityAuto")}</label>
            <div className="w-full mt-1 bg-base-700/40 border border-white/10 rounded-xl px-3 py-2 text-sm text-neon-cyan">
              {quantity !== null ? `${quantity.toLocaleString()} kg` : "—"}
            </div>
          </div>
        </div>

        {error && <div className="text-sm text-red-400">{error}</div>}

        <div className="flex justify-end gap-2 pt-2">
          <button onClick={onClose} className="neon-btn">{t("cancel")}</button>
          <button onClick={submit} disabled={busy} className="action-btn">
            {busy ? t("generating") : `📄 ${t("generatePdf")}`}
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
