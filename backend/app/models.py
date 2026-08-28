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
    """Singleton row holding the fixed China->Tashkent backbone costs as a
    FIXED total per shipment (e.g. one truck/container), not per ton or per
    kg — freight is quoted this way in practice, so it's divided by the
    actual shipment weight_kg at calculation time. cn_docs_cny is the only
    leg quoted in CNY; every other leg is USD. usd_cny_rate_fallback is
    only used when the live daily FX rate cannot be fetched."""

    __tablename__ = "expense_settings"

    id = Column(Integer, primary_key=True, default=1)

    cn_docs_cny = Column(Float, default=0.0)
    cn_osh_freight_usd = Column(Float, default=0.0)
    kg_transit_usd = Column(Float, default=0.0)
    osh_tashkent_freight_usd = Column(Float, default=0.0)
    uzb_transit_usd = Column(Float, default=0.0)

    usd_cny_rate_fallback = Column(Float, default=7.24)

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Destination(Base):
    """A final-leg destination reachable from Tashkent (e.g. Romania,
    Azerbaijan-Baku, Syria...), user-manageable from Settings so new
    routes can be added without a code change. freight_usd_total is the
    fixed cost of shipping the whole load from Tashkent to this
    destination, divided by weight_kg at calculation time."""

    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    incoterm = Column(String, default="DAP")
    freight_usd_total = Column(Float, default=0.0)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
