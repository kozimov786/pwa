import { useEffect, useMemo, useState } from "react";
import { calculate, getProducts } from "./api/client";
import { CurrencyToggle, ProductPresets, TonnagePresets } from "./components/PresetButtons";
import VoiceInput from "./components/VoiceInput";
import PricingTable from "./components/PricingTable";
import ActionBar from "./components/ActionBar";

export default function App() {
  const [products, setProducts] = useState([]);
  const [productId, setProductId] = useState(null);
  const [tonnage, setTonnage] = useState(21);
  const [currency, setCurrency] = useState("USD");
  const [margin, setMargin] = useState(0);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    getProducts()
      .then((data) => {
        setProducts(data);
        if (data.length) setProductId(data[0].id);
      })
      .catch((err) => setError(err.message));
  }, []);

  const calcPayload = useMemo(
    () =>
      productId
        ? { product_id: productId, tonnage, margin_usd_per_ton: margin }
        : null,
    [productId, tonnage, margin]
  );

  useEffect(() => {
    if (!calcPayload) return;
    setLoading(true);
    setError(null);
    calculate(calcPayload)
      .then(setResult)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [calcPayload]);

  function handleVoiceParsed(parsed) {
    if (parsed.product_id) setProductId(parsed.product_id);
    if (parsed.tonnage) setTonnage(parsed.tonnage);
    if (parsed.currency) setCurrency(parsed.currency);
  }

  return (
    <div className="min-h-screen max-w-4xl mx-auto px-4 py-6 space-y-5">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">
            Trade<span className="text-neon-cyan">Calc</span>
          </h1>
          <p className="text-sm text-slate-400">Xalqaro ulgurji savdo narx kalkulyatori</p>
        </div>
        <VoiceInput onParsed={handleVoiceParsed} />
      </header>

      <section className="glass-card p-4 space-y-4">
        <div>
          <div className="text-xs uppercase tracking-wide text-slate-400 mb-2">Mahsulot</div>
          <ProductPresets products={products} selectedId={productId} onSelect={setProductId} />
        </div>

        <div className="flex flex-wrap items-end gap-6">
          <div>
            <div className="text-xs uppercase tracking-wide text-slate-400 mb-2">Tonnaj</div>
            <TonnagePresets tonnage={tonnage} onChange={setTonnage} />
          </div>
          <div>
            <div className="text-xs uppercase tracking-wide text-slate-400 mb-2">Valyuta</div>
            <CurrencyToggle currency={currency} onChange={setCurrency} />
          </div>
          <div>
            <div className="text-xs uppercase tracking-wide text-slate-400 mb-2">Margin (USD/t)</div>
            <input
              type="number"
              value={margin}
              onChange={(e) => setMargin(parseFloat(e.target.value) || 0)}
              className="w-28 bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm
                         focus:outline-none focus:border-neon-cyan/60"
            />
          </div>
        </div>
      </section>

      {error && <div className="glass-card p-4 text-red-400 text-sm">{error}</div>}
      {loading && !result && <div className="glass-card p-8 text-center text-slate-400">Hisoblanmoqda…</div>}

      <PricingTable result={result} />

      <ActionBar calcPayload={calcPayload} canAct={!!result && !loading} />
    </div>
  );
}
