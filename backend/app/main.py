import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import migrations, models
from .database import Base, SessionLocal, engine
from .routers import calculate, destinations, expenses, export, invoice, products, vakif_transfer, voice

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")

# Each product's name is stored per-language so switching the app's language
# also switches product names — name_en is the fallback whenever a
# translation is missing (e.g. a product added via the quick "+ Add" field).
SEED_PRODUCTS = [
    {
        "name_en": "185 Walnut Kernels 90%",
        "name_uz": "185 Yong'oq mag'zi 90%",
        "name_ru": "Ядро грецкого ореха 185 90%",
        "name_tr": "185 İç Ceviz 90%",
        "name_zh": "185 核桃仁 90%",
        "oil_content": "90%",
        "packaging": "50kg jute bags",
    },
    {
        "name_en": "Xinpu 90%",
        "name_uz": "Xinpu 90%",
        "name_ru": "Синьпу 90%",
        "name_tr": "Xinpu 90%",
        "name_zh": "新蒲 90%",
        "oil_content": "90%",
        "packaging": "50kg jute bags",
    },
    {
        "name_en": "Xinpu 60%",
        "name_uz": "Xinpu 60%",
        "name_ru": "Синьпу 60%",
        "name_tr": "Xinpu 60%",
        "name_zh": "新蒲 60%",
        "oil_content": "60%",
        "packaging": "50kg jute bags",
    },
    {
        "name_en": "Xiner 90%",
        "name_uz": "Xiner 90%",
        "name_ru": "Синьер 90%",
        "name_tr": "Xiner 90%",
        "name_zh": "新尔 90%",
        "oil_content": "90%",
        "packaging": "50kg jute bags",
    },
    {
        "name_en": "Yunnan 90%",
        "name_uz": "Yunnan 90%",
        "name_ru": "Юньнань 90%",
        "name_tr": "Yunnan 90%",
        "name_zh": "云南 90%",
        "oil_content": "90%",
        "packaging": "50kg jute bags",
    },
    {
        "name_en": "Yunnan Quarters (1/4)",
        "name_uz": "Yunnan chorak (1/4)",
        "name_ru": "Юньнань 1/4 (четвертинки)",
        "name_tr": "Yunnan Çeyrek (1/4)",
        "name_zh": "云南 四分之一 (1/4)",
        "packaging": "50kg jute bags",
    },
    {
        "name_en": "Walnuts In-shell 185",
        "name_uz": "Po'stli yong'oq 185",
        "name_ru": "Грецкий орех в скорлупе 185",
        "name_tr": "Kabuklu Ceviz 185",
        "name_zh": "带壳核桃 185",
        "packaging": "50kg jute bags",
    },
]

SEED_DESTINATIONS = [
    {"name": "Gaziantep / Mersin", "incoterm": "DAP", "freight_usd_total": 3000.0, "sort_order": 1},
    {"name": "Azerbaijan - Baku", "incoterm": "DAP", "freight_usd_total": 3000.0, "sort_order": 2},
    {"name": "Romania", "incoterm": "DAP", "freight_usd_total": 5500.0, "sort_order": 3},
    {"name": "Syria", "incoterm": "DAP", "freight_usd_total": 3700.0, "sort_order": 4},
]


def seed_data():
    db = SessionLocal()
    try:
        if db.query(models.Product).count() == 0:
            for item in SEED_PRODUCTS:
                db.add(models.Product(**item))
        if db.get(models.ExpenseSettings, 1) is None:
            db.add(
                models.ExpenseSettings(
                    id=1,
                    cn_docs_cny=3500.0,
                    commission_cny_per_kg=0.5,
                    cn_osh_freight_usd=2500.0,
                    kg_transit_usd=1100.0,
                    osh_tashkent_freight_usd=1800.0,
                    uzb_transit_usd=400.0,
                    usd_cny_rate_fallback=7.24,
                )
            )
        if db.query(models.Destination).count() == 0:
            for item in SEED_DESTINATIONS:
                db.add(models.Destination(**item))
        db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    migrations.run_all(engine)
    seed_data()
    yield


app = FastAPI(title="Wholesale Trade Calc API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(expenses.router)
app.include_router(destinations.router)
app.include_router(calculate.router)
app.include_router(export.router)
app.include_router(vakif_transfer.router)
app.include_router(invoice.router)
app.include_router(voice.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Serves the built frontend (frontend/dist copied to ./static by the Docker
# build). Mounted last so it never shadows the /api/* routes above — any
# path not matched by them falls through to this static file server.
if os.path.isdir(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
