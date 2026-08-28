from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func

from .database import Base


class Product(Base):
    """Catalog of tradable products, e.g. 'Kabuklu 33', 'Xinpu 60%'.
    Purchase price is entered fresh on every calculation, not stored here."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    oil_content = Column(String, nullable=True)  # e.g. "33%", "60%"
    packaging = Column(String, nullable=True)  # e.g. "50kg jute bags"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ExpenseSettings(Base):
    """Singleton row holding all dynamic transit-leg costs (USD per ton).
    usd_cny_rate_fallback is only used when the live daily FX rate
    cannot be fetched (e.g. no internet access)."""

    __tablename__ = "expense_settings"

    id = Column(Integer, primary_key=True, default=1)

    # Transit legs, USD per ton
    cn_docs = Column(Float, default=0.0)
    cn_osh_freight = Column(Float, default=0.0)
    kg_transit = Column(Float, default=0.0)
    osh_tashkent_freight = Column(Float, default=0.0)
    uzb_transit = Column(Float, default=0.0)
    tashkent_antep_freight = Column(Float, default=0.0)
    tashkent_romania_freight = Column(Float, default=0.0)
    tashkent_baku_freight = Column(Float, default=0.0)

    usd_cny_rate_fallback = Column(Float, default=7.24)

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
