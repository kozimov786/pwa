export function formatMoney(n) {
  return `${n.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}$`;
}

export function productName(product, lang) {
  if (!product) return "";
  return product[`name_${lang}`] || product.name_en || "";
}
