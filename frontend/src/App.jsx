import { useEffect, useMemo, useState } from "react";
import { calculate, createProduct, getProducts } from "./api/client";
import { ProductSelect, WeightPresets } from "./components/PresetButtons";
import VoiceInput from "./components/VoiceInput";
import PricingTable from "./components/PricingTable";
import ActionBar from "./components/ActionBar";
import SettingsModal from "./components/SettingsModal";
import LanguageSelect from "./components/LanguageSelect";
import DocsPage from "./components/DocsPage";
import MultiProductPanel from "./components/MultiProductPanel";
import { useLanguage } from "./LanguageContext";

export default function App() {
  const { lang, t } = useLanguage();
  const [view, setView] = useState("calculator");
  const [calcMode, setCalcMode] = useState("single");
  const [products, setProducts] = useState([]);
  const [productId, setProductId] = useState(null);
  const [weightKg, setWeightKg] = useState(21000);
  const [priceCnyPerKg, setPriceCnyPerKg] = useState("");
  const [margin, setMargin] = useState(0);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [settingsVersion, setSettingsVersion] = useState(0);

  function loadProducts() {
    return getProducts()
      .then((data) => {
        setProducts(data);
        setProductId((current) => current ?? (data.length ? data[0].id : null));
        return data;
      })
      .catch((err) => setError(err.message));
  }

  useEffect(() => {
    loadProducts();
  }, []);

  async function handleAddProduct(name) {
    const product = await createProduct(name);
    await loadProducts();
    setProductId(product.id);
  }

  const calcPayload = useMemo(() => {
    const price = parseFloat(priceCnyPerKg);
    if (!productId || !weightKg || !price || price <= 0) return null;
    return {
      product_id: productId,
      weight_kg: weightKg,
      price_cny_per_kg: price,
      margin_usd_per_kg: margin || 0,
      lang,
    };
  }, [productId, weightKg, priceCnyPerKg, margin, lang]);

  useEffect(() => {
    if (!calcPayload) {
      setResult(null);
      return;
    }
    setLoading(true);
    setError(null);
    calculate(calcPayload)
      .then(setResult)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [calcPayload, settingsVersion]);

  function handleVoiceParsed(parsed) {
    if (parsed.product_id) setProductId(parsed.product_id);
    if (parsed.tonnage) setWeightKg(parsed.tonnage * 1000);
  }

  if (view === "docs") {
    return <DocsPage onBack={() => setView("calculator")} />;
  }

  return (
    <div className="min-h-screen max-w-4xl mx-auto px-4 py-6 space-y-5">
      <header className="flex items-center justify-between flex-wrap gap-3">
        <div className="flex items-center gap-3">
          <img src="/logo.png" alt="GOKLE" className="w-11 h-11 rounded-xl bg-white/95 p-1 shadow-glow" />
          <div>
            <h1 className="text-2xl font-bold tracking-tight">GOKLE</h1>
            <p className="text-sm text-slate-400">{t("appSubtitle")}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <LanguageSelect />
          <button
            onClick={() => setView("docs")}
            className="neon-btn h-12"
            title={t("docsNav")}
          >
            📄 {t("docsNav")}
          </button>
          <button
            onClick={() => setSettingsOpen(true)}
            className="w-12 h-12 rounded-full flex items-center justify-center border border-white/10
                       bg-base-700/60 hover:border-neon-cyan/60 hover:text-neon-cyan transition-all"
            title={t("settingsGear")}
          >
            ⚙️
          </button>
          <VoiceInput onParsed={handleVoiceParsed} />
        </div>
      </header>

      <div className="flex gap-2">
        <button
          onClick={() => setCalcMode("single")}
          className={`neon-btn ${calcMode === "single" ? "neon-btn-active" : ""}`}
        >
          {t("modeSingle")}
        </button>
        <button
          onClick={() => setCalcMode("multi")}
          className={`neon-btn ${calcMode === "multi" ? "neon-btn-active" : ""}`}
        >
          {t("modeMulti")}
        </button>
      </div>

      {calcMode === "single" ? (
        <>
          <section className="glass-card p-4 space-y-4">
            <div>
              <div className="text-xs uppercase tracking-wide text-slate-400 mb-2">{t("product")}</div>
              <ProductSelect
                products={products}
                selectedId={productId}
                onSelect={setProductId}
                onAddProduct={handleAddProduct}
              />
            </div>

            <div>
              <div className="text-xs uppercase tracking-wide text-slate-400 mb-2">{t("weight")}</div>
              <WeightPresets weightKg={weightKg} onChange={setWeightKg} />
            </div>

            <div className="flex flex-wrap items-end gap-6">
              <div>
                <div className="text-xs uppercase tracking-wide text-slate-400 mb-2">{t("chinaPriceLabel")}</div>
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  value={priceCnyPerKg}
                  onChange={(e) => setPriceCnyPerKg(e.target.value)}
                  placeholder={t("chinaPricePlaceholder")}
                  className="w-40 bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm
                             focus:outline-none focus:border-neon-cyan/60"
                />
              </div>
              <div>
                <div className="text-xs uppercase tracking-wide text-slate-400 mb-2">{t("marginLabel")}</div>
                <input
                  type="number"
                  step="0.01"
                  value={margin}
                  onChange={(e) => setMargin(parseFloat(e.target.value) || 0)}
                  className="w-28 bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm
                             focus:outline-none focus:border-neon-cyan/60"
                />
              </div>
            </div>
          </section>

          {error && <div className="glass-card p-4 text-red-400 text-sm">{error}</div>}
          {loading && !result && <div className="glass-card p-8 text-center text-slate-400">{t("calculating")}</div>}

          <PricingTable result={result} />

          <ActionBar calcPayload={calcPayload} canAct={!!result && !loading} />
        </>
      ) : (
        <MultiProductPanel products={products} lang={lang} />
      )}

      <SettingsModal
        open={settingsOpen}
        onClose={() => {
          setSettingsOpen(false);
          setSettingsVersion((v) => v + 1);
        }}
      />
    </div>
  );
}
