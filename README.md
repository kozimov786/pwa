# GOKLE — Wholesale Trade Calc PWA

International wholesale trade landed-price calculator: FastAPI backend + React/Tailwind PWA frontend.

Route modeled: China (purchase price, CNY/kg) → Osh, KG (CPT/DAP) → Tashkent, UZ (DAP) → any number of
user-managed destinations from Tashkent (Gaziantep/Mersin, Azerbaijan-Baku, Romania, Syria, ...).
Every transit leg is configured as a **fixed total cost per shipment** (one truck/container) and divided
by the actual shipment weight at calculation time — not a per-ton rate.

## Backend (FastAPI)

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in OPENAI_API_KEY for voice parsing
uvicorn app.main:app --reload --port 8000
```

SQLite DB (`backend/data/trade.db`) is auto-created and seeded with two demo products
("Kabuklu 33", "Xinpu 60%"), the China→Tashkent backbone costs, and four demo destinations
on first run.

**LibreOffice is required** for the Vakıfbank transfer and Invoice docx→PDF features:
```bash
brew install --cask libreoffice
ln -sf /Applications/LibreOffice.app/Contents/MacOS/soffice /opt/homebrew/bin/soffice
```
Everything else works without it.

This LibreOffice cask ships with no fontconfig.conf, so on first Invoice generation the backend
auto-copies the bundled `assets/fonts/NotoSansSC.ttf` into
`LibreOffice.app/Contents/Resources/fonts/truetype/` (see `services/docx_pdf.py`) — otherwise
Chinese text in the invoice template renders as blank instead of tofu boxes, since LibreOffice's
headless export doesn't substitute a fallback font for missing glyphs the way Word does. On a
Linux deployment, install a system CJK package instead (e.g. `fonts-noto-cjk`).

### Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET/POST | `/api/products` | product catalog (name/oil-content/packaging; price is entered per calculation) |
| GET/PUT | `/api/expenses` | China→Tashkent backbone costs (fixed per shipment) & FX fallback |
| GET/POST/PUT/DELETE | `/api/destinations` | user-managed final legs from Tashkent — add new routes with no code change |
| POST | `/api/calculate` | landed price cascade, all figures in USD/kg, live daily USD/CNY rate |
| POST | `/api/export/pdf` \| `/api/export/excel` | quotation documents, localized via `lang` (en/uz/ru/tr/zh) |
| GET | `/api/vakif-transfer/companies` | list of beneficiary companies with a Vakıfbank docx template |
| POST | `/api/vakif-transfer/generate` | fills the real Vakıfbank docx wire-transfer form for a Chinese supplier and converts it to PDF (content stays Turkish, never translated) |
| GET | `/api/invoice/companies` | list of sellers with a proforma-invoice docx template |
| POST | `/api/invoice/generate` | fills the real proforma invoice docx for a Chinese seller and converts it to PDF; Quantity is derived as Total Price / Unit Price, never entered |
| POST | `/api/voice/parse` | audio → Whisper transcript → parsed product/weight |

### Adding a new Vakıfbank beneficiary company

Drop a filled-in-once `.docx` copy of the Vakıfbank wire-transfer form for that company into
`backend/app/assets/bank_templates/`, then add an entry to `COMPANY_TEMPLATES` in
`backend/app/services/vakif_transfer.py` with the exact fixed-text prefix found in that template
for each of the four dynamic fields (Tarih, amount-in-words, Valör, Swift Açıklaması/Contract No).
No other code changes needed.

### Adding a new invoice seller

Drop a filled-in-once `.docx` copy of that seller's proforma invoice into
`backend/app/assets/invoice_templates/`, then add an entry to `INVOICE_TEMPLATES` in
`backend/app/services/invoice.py` with the Tarih/Contract prefixes and the line-item/totals table
row & column indices found in that template.

## Frontend (Vite + React + Tailwind, PWA)

```bash
cd frontend
npm install
npm run dev       # http://localhost:5173, proxies /api to :8000
```

Production build: `npm run build` → `dist/` (installable PWA via `manifest.json` + `sw.js`).

Supports English, Uzbek, Russian, Turkish and Chinese — switch via the language selector in the
header; the selection also controls the language of generated PDF/Excel quotations.

The **Docs** button in the header opens a separate page (not part of the calculator): pick a bank
group (currently "Vakıf Bank") → a company → Bank Transfer or Invoice, whichever that company has a
template for. The modal only asks for the transaction-specific fields — everything else
(beneficiary/seller/bank details) comes straight from the template.

## Notes

- Voice parsing uses OpenAI's Whisper API (`OPENAI_API_KEY`). No local model/ffmpeg required.
- All landed prices are computed server-side in `app/services/pricing.py` — the single source of truth for the cost cascade.
- PDF quotations embed the SIL-OFL-licensed NotoSans font (Cyrillic/Turkish) and reportlab's built-in STSong-Light CID font (Chinese) so ru/tr/zh render correctly — the base-14 PDF fonts can't.

## Deployment (single container, always-on URL)

The `Dockerfile` at the repo root builds the frontend and bundles it with the backend into one
image — FastAPI serves both the `/api/*` routes and the built PWA from the same origin, so there's
no CORS/proxy setup in production. LibreOffice + a bundled CJK font are installed at build time so
the Docs (Vakıfbank/Invoice) PDFs work out of the box.

**Railway** (recommended — no server to manage, free HTTPS URL):
1. Push this repo to GitHub (already done: `kozimov786/pwa`).
2. On [railway.app](https://railway.app), **New Project → Deploy from GitHub repo** → select
   `kozimov786/pwa`. Railway auto-detects the `Dockerfile`.
3. **Add a Volume** mounted at `/app/data` — otherwise the SQLite database (products, expenses,
   destinations you configure) resets on every redeploy.
4. **Variables** tab → add `OPENAI_API_KEY` (needed only for the voice-input feature; everything
   else works without it).
5. Deploy. Railway gives you a permanent `https://<something>.up.railway.app` URL — open it on any
   phone, from any network, and use **Add to Home Screen** to install it like a native app.

Any other Docker-friendly host (Render, Fly.io, a plain VPS with `docker run`) works the same way —
just make sure whatever you pick persists `/app/data` across deploys and sets `OPENAI_API_KEY`.
