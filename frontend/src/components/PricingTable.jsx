export default function PricingTable({ result }) {
  if (!result) {
    return (
      <div className="glass-card p-8 text-center text-slate-400">
        Mahsulot va tonnajni tanlang — narxlar shu yerda ko'rinadi
      </div>
    );
  }

  return (
    <div className="glass-card overflow-hidden">
      <div className="p-4 border-b border-white/10 flex flex-wrap items-center justify-between gap-2">
        <div>
          <div className="text-lg font-semibold text-neon-cyan">{result.product.name}</div>
          <div className="text-xs text-slate-400">
            {result.tonnage} t &middot; ex-works ${result.base_price_usd_per_ton}/t
          </div>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-400 bg-white/5">
              <th className="px-4 py-3 font-medium">Yo'nalish</th>
              <th className="px-4 py-3 font-medium">Incoterm</th>
              <th className="px-4 py-3 font-medium text-right">USD/t</th>
              <th className="px-4 py-3 font-medium text-right">EUR/t</th>
              <th className="px-4 py-3 font-medium text-right">Jami USD</th>
              <th className="px-4 py-3 font-medium text-right">Jami EUR</th>
            </tr>
          </thead>
          <tbody>
            {result.destinations.map((d) => (
              <tr key={d.destination} className="border-t border-white/5 hover:bg-white/5 transition-colors">
                <td className="px-4 py-3 font-medium">{d.destination}</td>
                <td className="px-4 py-3 text-slate-400">{d.incoterm}</td>
                <td className="px-4 py-3 text-right text-neon-cyan">{d.price_per_ton_usd.toFixed(2)}</td>
                <td className="px-4 py-3 text-right text-neon-violet">
                  {d.price_per_ton_eur ? d.price_per_ton_eur.toFixed(2) : "—"}
                </td>
                <td className="px-4 py-3 text-right font-semibold">{d.total_usd.toLocaleString()}</td>
                <td className="px-4 py-3 text-right font-semibold">
                  {d.total_eur ? d.total_eur.toLocaleString() : "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
