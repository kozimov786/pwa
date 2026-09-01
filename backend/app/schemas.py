from typing import Optional
from pydantic import BaseModel, ConfigDict


# ---------- Products ----------

class ProductBase(BaseModel):
    name: str
    oil_content: Optional[str] = None
    packaging: Optional[str] = None
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------- Expenses ----------

class ExpensesBase(BaseModel):
    cn_docs_cny: float = 0.0
    cn_osh_freight_usd: float = 0.0
    kg_transit_usd: float = 0.0
    osh_tashkent_freight_usd: float = 0.0
    uzb_transit_usd: float = 0.0
    usd_cny_rate_fallback: float = 7.24


class ExpensesUpdate(ExpensesBase):
    pass


class ExpensesOut(ExpensesBase):
    model_config = ConfigDict(from_attributes=True)


# ---------- Destinations (dynamic final legs from Tashkent) ----------

class DestinationBase(BaseModel):
    name: str
    incoterm: str = "DAP"
    freight_usd_total: float = 0.0
    sort_order: int = 0
    is_active: bool = True


class DestinationCreate(DestinationBase):
    pass


class DestinationUpdate(DestinationBase):
    pass


class DestinationOut(DestinationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------- Calculate ----------

class CalculateRequest(BaseModel):
    product_id: int
    weight_kg: float = 21000.0
    price_cny_per_kg: float
    margin_usd_per_kg: float = 0.0
    lang: str = "en"


class DestinationPrice(BaseModel):
    destination: str
    price_per_kg_usd: float
    total_usd: float


class CalculateResponse(BaseModel):
    product: ProductOut
    weight_kg: float
    price_cny_per_kg: float
    usd_cny_rate: float
    fx_is_live: bool
    base_price_usd_per_kg: float
    destinations: list[DestinationPrice]


# ---------- Comparison export (multiple products -> one destination) ----------

class ComparisonRow(BaseModel):
    product_id: int
    weight_kg: float = 21000.0
    price_cny_per_kg: float
    margin_usd_per_kg: float = 0.0


class ComparisonExportRequest(BaseModel):
    destination: str
    rows: list[ComparisonRow]
    lang: str = "en"


# ---------- Vakifbank China Transfer (docx template based) ----------

class VakifTransferRequest(BaseModel):
    company_key: str
    tarih: str
    valor_tarihi: str
    amount: float
    currency: str = "USD"
    contract_no: str = ""


# ---------- Proforma Invoice (docx template based) ----------

class InvoiceRequest(BaseModel):
    company_key: str
    tarih: str
    contract_no: str = ""
    unit_price: float
    total_price: float
    currency: str = "USD"
