from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import Base, SessionLocal, engine
from .routers import bank_transfer, calculate, dispatch, expenses, export, products, voice

SEED_PRODUCTS = [
    {"name": "Kabuklu 33", "oil_content": "33%", "packaging": "50kg jute bags"},
    {"name": "Xinpu 60%", "oil_content": "60%", "packaging": "50kg jute bags"},
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
                    cn_osh_freight_usd=2500.0,
                    kg_transit_usd=1100.0,
                    osh_tashkent_freight_usd=1800.0,
                    uzb_transit_usd=400.0,
                    tashkent_antep_freight_usd=3000.0,
                    tashkent_romania_freight_usd=5500.0,
                    tashkent_baku_freight_usd=3000.0,
                    usd_cny_rate_fallback=7.24,
                )
            )
        db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
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
app.include_router(calculate.router)
app.include_router(export.router)
app.include_router(bank_transfer.router)
app.include_router(dispatch.router)
app.include_router(voice.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
