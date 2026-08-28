# Wholesale Trade Calc — PWA

International wholesale trade landed-price calculator: FastAPI backend + React/Tailwind PWA frontend.

Route modeled: China (ex-works) → Osh, KG (CPT/DAP) → Tashkent, UZ (DAP) → Gaziantep/Mersin, Baku, Romania (DAP, USD & EUR).

## Backend (FastAPI)

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in OPENAI_API_KEY and GREEN_API_* for voice + WhatsApp
uvicorn app.main:app --reload --port 8000
```

SQLite DB (`backend/data/trade.db`) is auto-created and seeded with two demo products
("Kabuklu 33", "Xinpu 60%") and default transit-leg costs on first run.

### Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET/POST | `/api/products` | product catalog |
| GET/PUT | `/api/expenses` | transit-leg costs & FX rates |
| POST | `/api/calculate` | landed price cascade |
| POST | `/api/export/pdf` \| `/api/export/excel` | quotation documents |
| POST | `/api/bank-transfer-talimati` | Turkish bank transfer instruction PDF |
| POST | `/api/dispatch-group` | async send quotation to WhatsApp group (Green-API) |
| POST | `/api/voice/parse` | audio → Whisper transcript → parsed product/tonnage/currency |

## Frontend (Vite + React + Tailwind, PWA)

```bash
cd frontend
npm install
npm run dev       # http://localhost:5173, proxies /api to :8000
```

Production build: `npm run build` → `dist/` (installable PWA via `manifest.json` + `sw.js`).

## Notes

- Voice parsing uses OpenAI's Whisper API (`OPENAI_API_KEY`). No local model/ffmpeg required.
- WhatsApp dispatch uses [Green-API](https://green-api.com) — set `GREEN_API_ID_INSTANCE`, `GREEN_API_TOKEN`, `GREEN_API_GROUP_ID`.
- All landed prices are computed server-side in `app/services/pricing.py` — the single source of truth for the cost cascade.
