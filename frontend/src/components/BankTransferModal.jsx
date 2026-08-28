import { useState } from "react";
import { bankTransferTalimati } from "../api/client";

const EMPTY = {
  beneficiary_name: "",
  beneficiary_iban: "",
  beneficiary_bank: "",
  swift_code: "",
  amount: "",
  currency: "USD",
  reference: "",
  ordering_customer: "",
};

export default function BankTransferModal({ open, onClose }) {
  const [form, setForm] = useState(EMPTY);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);

  if (!open) return null;

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function submit() {
    setBusy(true);
    setError(null);
    try {
      await bankTransferTalimati({ ...form, amount: parseFloat(form.amount) || 0 });
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
        <h2 className="text-lg font-semibold text-neon-cyan">Turk Bank Transfer Talimati</h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <Field label="Beneficiary Name" value={form.beneficiary_name} onChange={(v) => update("beneficiary_name", v)} />
          <Field label="IBAN" value={form.beneficiary_iban} onChange={(v) => update("beneficiary_iban", v)} />
          <Field label="Bank" value={form.beneficiary_bank} onChange={(v) => update("beneficiary_bank", v)} />
          <Field label="SWIFT/BIC" value={form.swift_code} onChange={(v) => update("swift_code", v)} />
          <Field label="Amount" type="number" value={form.amount} onChange={(v) => update("amount", v)} />
          <div>
            <label className="text-xs text-slate-400">Currency</label>
            <select
              value={form.currency}
              onChange={(e) => update("currency", e.target.value)}
              className="w-full mt-1 bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm"
            >
              {["USD", "EUR", "TRY", "CNY"].map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>
          <Field label="Reference" value={form.reference} onChange={(v) => update("reference", v)} />
          <Field label="Ordering Customer" value={form.ordering_customer} onChange={(v) => update("ordering_customer", v)} />
        </div>

        {error && <div className="text-sm text-red-400">{error}</div>}

        <div className="flex justify-end gap-2 pt-2">
          <button onClick={onClose} className="neon-btn">Bekor qilish</button>
          <button onClick={submit} disabled={busy} className="action-btn">
            {busy ? "Yaratilmoqda…" : "🏦 PDF yaratish"}
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
