import { useEffect, useState } from "react";
import { getVakifCompanies } from "../api/client";
import { useLanguage } from "../LanguageContext";
import VakifTransferModal from "./VakifTransferModal";

export default function DocsPage({ onBack }) {
  const { t } = useLanguage();
  const [companies, setCompanies] = useState([]);
  const [error, setError] = useState(null);
  const [activeCompany, setActiveCompany] = useState(null);

  useEffect(() => {
    getVakifCompanies().then(setCompanies).catch((err) => setError(err.message));
  }, []);

  return (
    <div className="min-h-screen max-w-4xl mx-auto px-4 py-6 space-y-5">
      <header className="flex items-center gap-3">
        <button onClick={onBack} className="neon-btn">
          ← {t("backToCalculator")}
        </button>
        <h1 className="text-xl font-bold">{t("docsNav")}</h1>
      </header>

      <section className="glass-card p-4 space-y-3">
        <h2 className="text-sm font-semibold text-neon-violet uppercase tracking-wide">{t("bankDocsTitle")}</h2>
        {error && <div className="text-sm text-red-400">{error}</div>}
        {companies.length === 0 && !error && <div className="text-sm text-slate-400">{t("loading")}</div>}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {companies.map((c) => (
            <button
              key={c.key}
              onClick={() => setActiveCompany(c)}
              className="action-btn justify-start text-left"
            >
              🏦 {c.label}
            </button>
          ))}
        </div>
      </section>

      <section className="glass-card p-4 space-y-3">
        <h2 className="text-sm font-semibold text-neon-violet uppercase tracking-wide">{t("invoiceTitle")}</h2>
        <div className="text-sm text-slate-400">{t("comingSoon")}</div>
      </section>

      <VakifTransferModal company={activeCompany} onClose={() => setActiveCompany(null)} />
    </div>
  );
}
