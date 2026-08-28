const BASE = "/api";

async function handle(res) {
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || JSON.stringify(body);
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  return res;
}

export async function getProducts() {
  const res = await handle(await fetch(`${BASE}/products`));
  return res.json();
}

export async function createProduct(name) {
  const res = await handle(
    await fetch(`${BASE}/products`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    })
  );
  return res.json();
}

export async function getExpenses() {
  const res = await handle(await fetch(`${BASE}/expenses`));
  return res.json();
}

export async function updateExpenses(payload) {
  const res = await handle(
    await fetch(`${BASE}/expenses`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  );
  return res.json();
}

export async function getDestinations() {
  const res = await handle(await fetch(`${BASE}/destinations`));
  return res.json();
}

export async function createDestination(payload) {
  const res = await handle(
    await fetch(`${BASE}/destinations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  );
  return res.json();
}

export async function updateDestination(id, payload) {
  const res = await handle(
    await fetch(`${BASE}/destinations/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  );
  return res.json();
}

export async function deleteDestination(id) {
  await handle(await fetch(`${BASE}/destinations/${id}`, { method: "DELETE" }));
}

export async function calculate(payload) {
  const res = await handle(
    await fetch(`${BASE}/calculate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  );
  return res.json();
}

async function downloadBlob(path, payload, filename) {
  const res = await handle(
    await fetch(`${BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  );
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

export function exportPdf(payload, filename = "quotation.pdf") {
  return downloadBlob("/export/pdf", payload, filename);
}

export function exportExcel(payload, filename = "quotation.xlsx") {
  return downloadBlob("/export/excel", payload, filename);
}

export async function getVakifCompanies() {
  const res = await handle(await fetch(`${BASE}/vakif-transfer/companies`));
  return res.json();
}

export function generateVakifTransfer(payload, filename = "vakifbank_transfer.pdf") {
  return downloadBlob("/vakif-transfer/generate", payload, filename);
}

export async function getInvoiceCompanies() {
  const res = await handle(await fetch(`${BASE}/invoice/companies`));
  return res.json();
}

export function generateInvoice(payload, filename = "proforma_invoice.pdf") {
  return downloadBlob("/invoice/generate", payload, filename);
}

export async function parseVoice(audioBlob) {
  const form = new FormData();
  form.append("audio", audioBlob, "voice.webm");
  const res = await handle(
    await fetch(`${BASE}/voice/parse`, {
      method: "POST",
      body: form,
    })
  );
  return res.json();
}
