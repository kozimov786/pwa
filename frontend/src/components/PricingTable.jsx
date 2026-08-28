import { useLanguage } from "../LanguageContext";

export default function PricingTable({ result }) {
  const { t } = useLanguage();

  if (!result) {
    return (
      <div className="glass-card p-8 text-center text-slate-400">
        {t("emptyTable")}
      </div>
    );
  }

  return (
    <div className="glass-card overflow-hidden">
      <div className="p-4 border-b border-white/10 flex flex-wrap items-center justify-between gap-2">
        <div>
          <div className="text-lg font-semibold text-neon-cyan">{result.product.name}</div>
          <div className="text-xs text-slate-400">
            {t("chinaPriceInfo")}: ¥{result.price_cny_per_kg}/kg &middot; {t("rateInfo")}: 1 USD = {result.usd_cny_rate} CNY
            {result.fx_is_live ? ` (${t("liveRate")})` : ` (${t("fallbackRate")})`}
          </div>
        </div>
        <div className="text-sm text-slate-300">
          {t("basePrice")}: <span className="text-neon-violet font-semibold">${result.base_price_usd_per_kg}/kg</span>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-400 bg-white/5">
              <th className="px-4 py-3 font-medium">{t("colDestination")}</th>
              <th className="px-4 py-3 font-medium text-right">{t("colTotalKg")}</th>
              <th className="px-4 py-3 font-medium text-right">{t("colPricePerKg")}</th>
              <th className="px-4 py-3 font-medium text-right">{t("colTotalCost")}</th>
            </tr>
          </thead>
          <tbody>
            {result.destinations.map((d) => (
              <tr key={d.destination} className="border-t border-white/5 hover:bg-white/5 transition-colors">
                <td className="px-4 py-3 text-slate-300">{d.destination}</td>
                <td className="px-4 py-3 text-right">{result.weight_kg.toLocaleString()}</td>
                <td className="px-4 py-3 text-right text-neon-cyan">{d.price_per_kg_usd.toFixed(2)}$</td>
                <td className="px-4 py-3 text-right font-semibold">{d.total_usd.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
