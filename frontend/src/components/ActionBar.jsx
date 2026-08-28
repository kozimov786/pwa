import { useState } from "react";
import { dispatchGroup, exportExcel, exportPdf } from "../api/client";
import BankTransferModal from "./BankTransferModal";

export default function ActionBar({ calcPayload, canAct }) {
  const [busy, setBusy] = useState(null);
  const [notice, setNotice] = useState(null);
  const [bankModalOpen, setBankModalOpen] = useState(false);

  async function run(key, fn) {
    setBusy(key);
    setNotice(null);
    try {
      await fn();
      if (key === "whatsapp") setNotice("Guruhga yuborish navbatga qo'yildi ✅");
    } catch (err) {
      setNotice(`Xato: ${err.message}`);
    } finally {
      setBusy(null);
    }
  }

  return (
    <div className="glass-card p-4 space-y-3">
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <button
          disabled={!canAct || busy}
          onClick={() => run("pdf", () => exportPdf(calcPayload))}
          className="action-btn"
        >
          📥 {busy === "pdf" ? "…" : "PDF"}
        </button>
        <button
          disabled={!canAct || busy}
          onClick={() => run("excel", () => exportExcel(calcPayload))}
          className="action-btn"
        >
          📊 {busy === "excel" ? "…" : "Excel"}
        </button>
        <button
          disabled={!canAct || busy}
          onClick={() =>
            run("whatsapp", () =>
              dispatchGroup({
                message: "Yangi narx taklifi tayyor.",
                include_pdf: true,
                include_excel: false,
                calculate_payload: calcPayload,
              })
            )
          }
          className="action-btn"
        >
          📤 {busy === "whatsapp" ? "…" : "WhatsApp"}
        </button>
        <button onClick={() => setBankModalOpen(true)} className="action-btn">
          🏦 Talimat
        </button>
      </div>
      {notice && <div className="text-sm text-slate-300">{notice}</div>}

      <BankTransferModal open={bankModalOpen} onClose={() => setBankModalOpen(false)} />
    </div>
  );
}
