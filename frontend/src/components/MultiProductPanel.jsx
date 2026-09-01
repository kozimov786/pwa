import { useEffect, useMemo, useState } from "react";
import { calculate, getDestinations } from "../api/client";
import { useLanguage } from "../LanguageContext";

const WEIGHT_PRESETS_KG = [20000, 21000, 22000, 20800];

function emptyRow(id, productId) {
  return { id, productId: productId ?? null, weightKg: 21000, priceCnyPerKg: "" };
}

export default function MultiProductPanel({ products, lang }) {
  const { t } = useLanguage();
  const [destinations, setDestinations] = useState([]);
  const [destination, setDestination] = useState("");
  const [rows, setRows] = useState([emptyRow(1)]);
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    getDestinations()
      .then((data) => {
        const all = ["Osh (CPT/DAP)", "Tashkent (DAP)", ...data.map((d) => `${d.name} (${d.incoterm})`)];
        setDestinations(all);
        setDestination((cur) => cur || all[0]);
      })
      .catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    if (products.length && rows.length === 1 && !rows[0].productId) {
      setRows([emptyRow(1, products[0].id)]);
    }
  }, [products]);

  function updateRow(id, patch) {
    setRows((rs) => rs.map((r) => (r.id === id ? { ...r, ...patch } : r)));
  }

  function addRow() {
    setRows((rs) => [...rs, emptyRow(Date.now(), products[0]?.id)]);
  }

  function removeRow(id) {
    setRows((rs) => rs.filter((r) => r.id !== id));
  }

  const validRows = useMemo(
    () => rows.filter((r) => r.productId && r.weightKg && parseFloat(r.priceCnyPerKg) > 0),
    [rows]
  );

  useEffect(() => {
    if (!destination || validRows.length === 0) {
      setResults({});
      return;
    }
    setLoading(true);
    setError(null);
    Promise.all(
      validRows.map((r) =>
        calculate({
          product_id: r.productId,
          weight_kg: r.weightKg,
          price_cny_per_kg: parseFloat(r.priceCnyPerKg),
          margin_usd_per_kg: 0,
          lang,
        }).then((res) => ({ rowId: r.id, res }))
      )
    )
      .then((list) => {
        const map = {};
        for (const { rowId, res } of list) map[rowId] = res;
        setResults(map);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [destination, JSON.stringify(validRows), lang]);

  const tableRows = validRows
    .map((r) => {
      const res = results[r.id];
      if (!res) return null;
      const leg = res.destinations.find((d) => d.destination === destination);
      if (!leg) return null;
      const product = products.find((p) => p.id === r.productId);
      return { id: r.id, name: product?.name ?? "", weightKg: res.weight_kg, ...leg };
    })
    .filter(Boolean);

  return (
    <div className="space-y-4">
      <section className="glass-card p-4 space-y-4">
        <div>
          <div className="text-xs uppercase tracking-wide text-slate-400 mb-2">{t("selectDestination")}</div>
          <select
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            className="bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm min-w-[220px]
                       focus:outline-none focus:border-neon-cyan/60"
          >
            {destinations.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>

        <div className="space-y-3">
          {rows.map((row) => (
            <div key={row.id} className="flex flex-wrap items-end gap-3 border-t border-white/5 pt-3 first:border-t-0 first:pt-0">
              <select
                value={row.productId ?? ""}
                onChange={(e) => updateRow(row.id, { productId: parseInt(e.target.value, 10) })}
                className="bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm min-w-[160px]
                           focus:outline-none focus:border-neon-cyan/60"
              >
                {products.map((p) => (
                  <option key={p.id} value={p.id}>{p.name}</option>
                ))}
              </select>

              <div className="flex flex-wrap gap-1.5">
                {WEIGHT_PRESETS_KG.map((kg) => (
                  <button
                    key={kg}
                    onClick={() => updateRow(row.id, { weightKg: kg })}
                    className={`neon-btn !px-2.5 !py-1.5 text-xs ${row.weightKg === kg ? "neon-btn-active" : ""}`}
                  >
                    {kg.toLocaleString()}
                  </button>
                ))}
              </div>

              <input
                type="number"
                min="0"
                step="0.01"
                value={row.priceCnyPerKg}
                onChange={(e) => updateRow(row.id, { priceCnyPerKg: e.target.value })}
                placeholder={t("chinaPricePlaceholder")}
                className="w-32 bg-base-700/60 border border-white/10 rounded-xl px-3 py-2 text-sm
                           focus:outline-none focus:border-neon-cyan/60"
              />

              {rows.length > 1 && (
                <button onClick={() => removeRow(row.id)} className="text-red-400 text-xs hover:underline">
                  {t("removeRow")}
                </button>
              )}
            </div>
          ))}
        </div>

        <button onClick={addRow} className="neon-btn">{t("addProductRow")}</button>
      </section>

      {error && <div className="glass-card p-4 text-red-400 text-sm">{error}</div>}
      {loading && <div className="glass-card p-8 text-center text-slate-400">{t("calculating")}</div>}

      {!loading && tableRows.length > 0 && (
        <div className="glass-card overflow-hidden">
          <div className="p-4 border-b border-white/10 text-sm text-slate-300">
            {t("colDestination")}: <span className="text-neon-cyan font-semibold">{destination}</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-slate-400 bg-white/5">
                  <th className="px-4 py-3 font-medium">{t("product")}</th>
                  <th className="px-4 py-3 font-medium text-right">{t("colTotalKg")}</th>
                  <th className="px-4 py-3 font-medium text-right">{t("colPricePerKg")}</th>
                  <th className="px-4 py-3 font-medium text-right">{t("colTotalCost")}</th>
                </tr>
              </thead>
              <tbody>
                {tableRows.map((r) => (
                  <tr key={r.id} className="border-t border-white/5 hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3 font-medium">{r.name}</td>
                    <td className="px-4 py-3 text-right">{r.weightKg.toLocaleString()}</td>
                    <td className="px-4 py-3 text-right text-neon-cyan">{r.price_per_kg_usd.toFixed(2)}$</td>
                    <td className="px-4 py-3 text-right font-semibold">{r.total_usd.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
