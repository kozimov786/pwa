export default function PricingTable({ result }) {
  if (!result) {
    return (
      <div className="glass-card p-8 text-center text-slate-400">
        Mahsulot, og'irlik va Xitoy narxini kiriting — natija shu yerda ko'rinadi
      </div>
    );
  }

  return (
    <div className="glass-card overflow-hidden">
      <div className="p-4 border-b border-white/10 flex flex-wrap items-center justify-between gap-2">
        <div>
          <div className="text-lg font-semibold text-neon-cyan">{result.product.name}</div>
          <div className="text-xs text-slate-400">
            Xitoy olish narxi: ¥{result.price_cny_per_kg}/kg &middot; kurs: 1 USD = {result.usd_cny_rate} CNY
            {result.fx_is_live ? " (bugungi kurs)" : " (zaxira kurs)"}
          </div>
        </div>
        <div className="text-sm text-slate-300">
          Baza narx: <span className="text-neon-violet font-semibold">${result.base_price_usd_per_kg}/kg</span>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-400 bg-white/5">
              <th className="px-4 py-3 font-medium">Mahsulot</th>
              <th className="px-4 py-3 font-medium">Yo'nalish</th>
              <th className="px-4 py-3 font-medium text-right">Jami kg</th>
              <th className="px-4 py-3 font-medium text-right">1 kg narx (USD)</th>
              <th className="px-4 py-3 font-medium text-right">Jami maliyet (USD)</th>
            </tr>
          </thead>
          <tbody>
            {result.destinations.map((d) => (
              <tr key={d.destination} className="border-t border-white/5 hover:bg-white/5 transition-colors">
                <td className="px-4 py-3 font-medium">{result.product.name}</td>
                <td className="px-4 py-3 text-slate-300">{d.destination}</td>
                <td className="px-4 py-3 text-right">{result.weight_kg.toLocaleString()}</td>
                <td className="px-4 py-3 text-right text-neon-cyan">{d.price_per_kg_usd.toFixed(4)}</td>
                <td className="px-4 py-3 text-right font-semibold">{d.total_usd.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
