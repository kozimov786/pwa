import { useEffect, useState } from "react";
import { getInvoiceCompanies, getVakifCompanies } from "../api/client";
import { useLanguage } from "../LanguageContext";
import VakifTransferModal from "./VakifTransferModal";
import InvoiceModal from "./InvoiceModal";

const GROUPS = [{ key: "vakif", label: "Vakıf Bank", icon: "🏦" }];

export default function DocsPage({ onBack }) {
  const { t } = useLanguage();
  const [bankCompanies, setBankCompanies] = useState([]);
  const [invoiceCompanies, setInvoiceCompanies] = useState([]);
  const [error, setError] = useState(null);

  const [group, setGroup] = useState(null);
  const [company, setCompany] = useState(null);
  const [openModal, setOpenModal] = useState(null); // "bank" | "invoice" | null

  useEffect(() => {
    getVakifCompanies().then(setBankCompanies).catch((err) => setError(err.message));
    getInvoiceCompanies().then(setInvoiceCompanies).catch((err) => setError(err.message));
  }, []);

  const companies = mergeCompanies(bankCompanies, invoiceCompanies);
  const bankEntry = company && bankCompanies.find((c) => c.key === company.key);
  const invoiceEntry = company && invoiceCompanies.find((c) => c.key === company.key);

  function reset() {
    setGroup(null);
    setCompany(null);
  }

  return (
    <div className="min-h-screen max-w-4xl mx-auto px-4 py-6 space-y-5">
      <header className="flex items-center gap-3">
        <button
          onClick={company ? () => setCompany(null) : group ? reset : onBack}
          className="neon-btn"
        >
          ← {company ? group.label : group ? t("docsNav") : t("backToCalculator")}
        </button>
        <h1 className="text-xl font-bold">
          {t("docsNav")}
          {group && ` / ${group.label}`}
          {company && ` / ${company.label}`}
        </h1>
      </header>

      {error && <div className="glass-card p-4 text-red-400 text-sm">{error}</div>}

      {!group && (
        <section className="glass-card p-4 space-y-3">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {GROUPS.map((g) => (
              <button key={g.key} onClick={() => setGroup(g)} className="action-btn justify-start text-left">
                {g.icon} {g.label}
              </button>
            ))}
          </div>
        </section>
      )}

      {group && !company && (
        <section className="glass-card p-4 space-y-3">
          {companies.length === 0 && !error && <div className="text-sm text-slate-400">{t("loading")}</div>}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {companies.map((c) => (
              <button key={c.key} onClick={() => setCompany(c)} className="action-btn justify-start text-left">
                🏢 {c.label}
              </button>
            ))}
          </div>
        </section>
      )}

      {group && company && (
        <section className="glass-card p-4 space-y-3">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {bankEntry && (
              <button onClick={() => setOpenModal("bank")} className="action-btn justify-start text-left">
                🏦 {t("bankDocsTitle")}
              </button>
            )}
            {invoiceEntry && (
              <button onClick={() => setOpenModal("invoice")} className="action-btn justify-start text-left">
                📄 {t("invoiceTitle")}
              </button>
            )}
          </div>
        </section>
      )}

      <VakifTransferModal
        company={openModal === "bank" ? bankEntry : null}
        onClose={() => setOpenModal(null)}
      />
      <InvoiceModal
        company={openModal === "invoice" ? invoiceEntry : null}
        onClose={() => setOpenModal(null)}
      />
    </div>
  );
}

function mergeCompanies(a, b) {
  const map = new Map();
  for (const c of [...a, ...b]) map.set(c.key, c);
  return [...map.values()];
}
