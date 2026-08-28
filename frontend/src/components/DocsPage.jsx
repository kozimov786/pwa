import { useEffect, useState } from "react";
import { getInvoiceCompanies, getVakifCompanies } from "../api/client";
import { useLanguage } from "../LanguageContext";
import VakifTransferModal from "./VakifTransferModal";
import InvoiceModal from "./InvoiceModal";

export default function DocsPage({ onBack }) {
  const { t } = useLanguage();
  const [bankCompanies, setBankCompanies] = useState([]);
  const [invoiceCompanies, setInvoiceCompanies] = useState([]);
  const [error, setError] = useState(null);
  const [activeBankCompany, setActiveBankCompany] = useState(null);
  const [activeInvoiceCompany, setActiveInvoiceCompany] = useState(null);

  useEffect(() => {
    getVakifCompanies().then(setBankCompanies).catch((err) => setError(err.message));
    getInvoiceCompanies().then(setInvoiceCompanies).catch((err) => setError(err.message));
  }, []);

  return (
    <div className="min-h-screen max-w-4xl mx-auto px-4 py-6 space-y-5">
      <header className="flex items-center gap-3">
        <button onClick={onBack} className="neon-btn">
          ← {t("backToCalculator")}
        </button>
        <h1 className="text-xl font-bold">{t("docsNav")}</h1>
      </header>

      {error && <div className="glass-card p-4 text-red-400 text-sm">{error}</div>}

      <section className="glass-card p-4 space-y-3">
        <h2 className="text-sm font-semibold text-neon-violet uppercase tracking-wide">{t("bankDocsTitle")}</h2>
        {bankCompanies.length === 0 && !error && <div className="text-sm text-slate-400">{t("loading")}</div>}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {bankCompanies.map((c) => (
            <button
              key={c.key}
              onClick={() => setActiveBankCompany(c)}
              className="action-btn justify-start text-left"
            >
              🏦 {c.label}
            </button>
          ))}
        </div>
      </section>

      <section className="glass-card p-4 space-y-3">
        <h2 className="text-sm font-semibold text-neon-violet uppercase tracking-wide">{t("invoiceTitle")}</h2>
        {invoiceCompanies.length === 0 && !error && <div className="text-sm text-slate-400">{t("comingSoon")}</div>}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {invoiceCompanies.map((c) => (
            <button
              key={c.key}
              onClick={() => setActiveInvoiceCompany(c)}
              className="action-btn justify-start text-left"
            >
              📄 {c.label}
            </button>
          ))}
        </div>
      </section>

      <VakifTransferModal company={activeBankCompany} onClose={() => setActiveBankCompany(null)} />
      <InvoiceModal company={activeInvoiceCompany} onClose={() => setActiveInvoiceCompany(null)} />
    </div>
  );
}
