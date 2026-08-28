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
    cn_docs: float = 0.0
    cn_osh_freight: float = 0.0
    kg_transit: float = 0.0
    osh_tashkent_freight: float = 0.0
    uzb_transit: float = 0.0
    tashkent_antep_freight: float = 0.0
    tashkent_romania_freight: float = 0.0
    tashkent_baku_freight: float = 0.0
    usd_cny_rate_fallback: float = 7.24


class ExpensesUpdate(ExpensesBase):
    pass


class ExpensesOut(ExpensesBase):
    model_config = ConfigDict(from_attributes=True)


# ---------- Calculate ----------

class CalculateRequest(BaseModel):
    product_id: int
    weight_kg: float = 21000.0
    price_cny_per_kg: float
    margin_usd_per_kg: float = 0.0


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


# ---------- Bank Transfer Talimati ----------

class BankTransferRequest(BaseModel):
    beneficiary_name: str
    beneficiary_iban: str
    beneficiary_bank: str
    swift_code: str
    amount: float
    currency: str = "USD"
    reference: str = ""
    ordering_customer: str = ""


# ---------- Dispatch ----------

class DispatchRequest(BaseModel):
    message: str
    include_pdf: bool = False
    include_excel: bool = False
    calculate_payload: Optional[CalculateRequest] = None
