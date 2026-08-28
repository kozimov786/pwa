import { useState } from "react";
import { exportExcel, exportPdf } from "../api/client";
import { useLanguage } from "../LanguageContext";

export default function ActionBar({ calcPayload, canAct }) {
  const { t } = useLanguage();
  const [busy, setBusy] = useState(null);
  const [notice, setNotice] = useState(null);

  async function run(key, fn) {
    setBusy(key);
    setNotice(null);
    try {
      await fn();
    } catch (err) {
      setNotice(`${t("errorPrefix")}: ${err.message}`);
    } finally {
      setBusy(null);
    }
  }

  return (
    <div className="glass-card p-4 space-y-3">
      <div className="grid grid-cols-2 gap-3">
        <button
          disabled={!canAct || busy}
          onClick={() => run("pdf", () => exportPdf(calcPayload))}
          className="action-btn"
        >
          📥 {busy === "pdf" ? "…" : t("pdf")}
        </button>
        <button
          disabled={!canAct || busy}
          onClick={() => run("excel", () => exportExcel(calcPayload))}
          className="action-btn"
        >
          📊 {busy === "excel" ? "…" : t("excel")}
        </button>
      </div>
      {notice && <div className="text-sm text-slate-300">{notice}</div>}
    </div>
  );
}
