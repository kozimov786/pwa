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

**LibreOffice is required** for the Vakıfbank China-transfer feature (docx→PDF conversion):
```bash
brew install --cask libreoffice
ln -sf /Applications/LibreOffice.app/Contents/MacOS/soffice /opt/homebrew/bin/soffice
```
Everything else works without it.

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
| POST | `/api/voice/parse` | audio → Whisper transcript → parsed product/weight |

### Adding a new Vakıfbank beneficiary company

Drop a filled-in-once `.docx` copy of the Vakıfbank wire-transfer form for that company into
`backend/app/assets/bank_templates/`, then add an entry to `COMPANY_TEMPLATES` in
`backend/app/services/vakif_transfer.py` with the exact fixed-text prefix found in that template
for each of the four dynamic fields (Tarih, amount-in-words, Valör, Swift Açıklaması/Contract No).
No other code changes needed.

## Frontend (Vite + React + Tailwind, PWA)

```bash
cd frontend
npm install
npm run dev       # http://localhost:5173, proxies /api to :8000
```

Production build: `npm run build` → `dist/` (installable PWA via `manifest.json` + `sw.js`).

Supports English, Uzbek, Russian, Turkish and Chinese — switch via the language selector in the
header; the selection also controls the language of generated PDF/Excel quotations.

The **Docs** button in the header opens a separate page (not part of the calculator) listing
official documents: bank transfers (per beneficiary company, from `/api/vakif-transfer/companies`)
and an Invoice section (placeholder until a template is provided). Picking a company opens a modal
with just the transaction-specific fields for that transfer.

## Notes

- Voice parsing uses OpenAI's Whisper API (`OPENAI_API_KEY`). No local model/ffmpeg required.
- All landed prices are computed server-side in `app/services/pricing.py` — the single source of truth for the cost cascade.
- PDF quotations embed the SIL-OFL-licensed NotoSans font (Cyrillic/Turkish) and reportlab's built-in STSong-Light CID font (Chinese) so ru/tr/zh render correctly — the base-14 PDF fonts can't.
