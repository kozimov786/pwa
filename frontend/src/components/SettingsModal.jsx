import { useEffect, useState } from "react";
import {
  getExpenses,
  updateExpenses,
  getDestinations,
  createDestination,
  updateDestination,
  deleteDestination,
  getProducts,
  createProduct,
  updateProduct,
  deleteProduct,
} from "../api/client";
import { useLanguage } from "../LanguageContext";

const NAME_LANGS = ["en", "uz", "ru", "tr", "zh"];

export default function SettingsModal({ open, onClose }) {
  const { t } = useLanguage();
  const [values, setValues] = useState(null);
  const [destinations, setDestinations] = useState([]);
  const [newDest, setNewDest] = useState({ name: "", freight_usd_total: "" });
  const [products, setProducts] = useState([]);
  const [newProductName, setNewProductName] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const [saved, setSaved] = useState(false);

  const FIELDS = [
    { key: "cn_docs_cny", label: t("cnDocs") },
    { key: "commission_cny_per_kg", label: t("commissionLabel") },
    { key: "cn_osh_freight_usd", label: t("cnOshFreight") },
    { key: "kg_transit_usd", label: t("kgTransit") },
    { key: "osh_tashkent_freight_usd", label: t("oshTashkentFreight") },
    { key: "uzb_transit_usd", label: t("uzbTransit") },
    { key: "usd_cny_rate_fallback", label: t("fxFallback") },
  ];

  useEffect(() => {
    if (!open) return;
    setError(null);
    setSaved(false);
    getExpenses().then(setValues).catch((err) => setError(err.message));
    getDestinations().then(setDestinations).catch((err) => setError(err.message));
    getProducts().then(setProducts).catch((err) => setError(err.message));
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

  async function updateDestPrice(dest, price) {
    try {
      const updated = await updateDestination(dest.id, { ...dest, freight_usd_total: price });
      setDestinations((prev) => prev.map((d) => (d.id === dest.id ? updated : d)));
    } catch (err) {
      setError(err.message);
    }
  }

  async function removeDest(id) {
    try {
      await deleteDestination(id);
      setDestinations((prev) => prev.filter((d) => d.id !== id));
    } catch (err) {
      setError(err.message);
    }
  }

  async function addDest() {
    const name = newDest.name.trim();
    const price = parseFloat(newDest.freight_usd_total);
    if (!name || !price) return;
    try {
      const created = await createDestination({
        name,
        incoterm: "DAP",
        freight_usd_total: price,
        sort_order: destinations.length + 1,
      });
      setDestinations((prev) => [...prev, created]);
      setNewDest({ name: "", freight_usd_total: "" });
    } catch (err) {
      setError(err.message);
    }
  }

  async function updateProductName(product, langCol, value) {
    try {
      const updated = await updateProduct(product.id, { ...product, [langCol]: value });
      setProducts((prev) => prev.map((p) => (p.id === product.id ? updated : p)));
    } catch (err) {
      setError(err.message);
    }
  }

  async function removeProduct(id) {
    try {
      await deleteProduct(id);
      setProducts((prev) => prev.filter((p) => p.id !== id));
    } catch (err) {
      setError(err.message);
    }
  }

  async function addProduct() {
    const name = newProductName.trim();
    if (!name) return;
    try {
      const created = await createProduct(name);
      setProducts((prev) => [...prev, created]);
      setNewProductName("");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="glass-card w-full max-w-lg p-6 space-y-4 max-h-[90vh] overflow-y-auto">
        <div>
          <h2 className="text-lg font-semibold text-neon-cyan">{t("settingsTitle")}</h2>
          <p className="text-xs text-slate-400 mt-1">{t("settingsHint")}</p>
        </div>

        {!values && !error && <div className="text-sm text-slate-400">{t("loading")}</div>}

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

        <div className="pt-2 border-t border-white/10">
          <h3 className="text-sm font-semibold text-neon-violet">{t("destinationsTitle")}</h3>
          <p className="text-xs text-slate-400 mt-1 mb-3">{t("destinationsHint")}</p>

          <div className="space-y-2">
            {destinations.map((d) => (
              <div key={d.id} className="flex items-center gap-2">
                <span className="flex-1 text-sm">{d.name}</span>
                <input
                  type="number"
                  step="0.01"
                  defaultValue={d.freight_usd_total}
                  onBlur={(e) => updateDestPrice(d, parseFloat(e.target.value) || 0)}
                  className="w-28 bg-base-700/60 border border-white/10 rounded-xl px-3 py-1.5 text-sm
                             focus:outline-none focus:border-neon-cyan/60"
                />
                <button onClick={() => removeDest(d.id)} className="text-red-400 text-xs hover:underline">
                  {t("delete")}
                </button>
              </div>
            ))}
          </div>

          <div className="flex items-center gap-2 mt-3">
            <input
              type="text"
              value={newDest.name}
              onChange={(e) => setNewDest((p) => ({ ...p, name: e.target.value }))}
              placeholder={t("destName")}
              className="flex-1 bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm
                         focus:outline-none focus:border-neon-cyan/60"
            />
            <input
              type="number"
              step="0.01"
              value={newDest.freight_usd_total}
              onChange={(e) => setNewDest((p) => ({ ...p, freight_usd_total: e.target.value }))}
              placeholder={t("destPrice")}
              className="w-28 bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm
                         focus:outline-none focus:border-neon-cyan/60"
            />
          </div>
          <button onClick={addDest} className="neon-btn mt-2 w-full">
            {t("addDestination")}
          </button>
        </div>

        <div className="pt-2 border-t border-white/10">
          <h3 className="text-sm font-semibold text-neon-violet">{t("productsTitle")}</h3>
          <p className="text-xs text-slate-400 mt-1 mb-3">{t("productsHint")}</p>

          <div className="space-y-4">
            {products.map((p) => (
              <div key={p.id} className="border border-white/10 rounded-xl p-3 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">{p.name_en}</span>
                  <button onClick={() => removeProduct(p.id)} className="text-red-400 text-xs hover:underline">
                    {t("delete")}
                  </button>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                  {NAME_LANGS.map((lc) => (
                    <div key={lc}>
                      <label className="text-[10px] uppercase text-slate-500">{lc}</label>
                      <input
                        type="text"
                        defaultValue={p[`name_${lc}`] || ""}
                        onBlur={(e) => updateProductName(p, `name_${lc}`, e.target.value)}
                        className="w-full mt-0.5 bg-base-700/60 border border-white/10 rounded-lg px-2 py-1 text-xs
                                   focus:outline-none focus:border-neon-cyan/60"
                      />
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div className="flex items-center gap-2 mt-3">
            <input
              type="text"
              value={newProductName}
              onChange={(e) => setNewProductName(e.target.value)}
              placeholder={t("newProductPlaceholder")}
              className="flex-1 bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm
                         focus:outline-none focus:border-neon-cyan/60"
            />
          </div>
          <button onClick={addProduct} className="neon-btn mt-2 w-full">
            {t("addButton")}
          </button>
        </div>

        {error && <div className="text-sm text-red-400">{error}</div>}
        {saved && <div className="text-sm text-neon-cyan">{t("saved")}</div>}

        <div className="flex justify-end gap-2 pt-2">
          <button onClick={onClose} className="neon-btn">{t("close")}</button>
          <button onClick={save} disabled={busy || !values} className="action-btn">
            {busy ? t("saving") : `💾 ${t("save")}`}
          </button>
        </div>
      </div>
    </div>
  );
}
