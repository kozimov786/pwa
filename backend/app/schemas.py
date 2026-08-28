from typing import Optional
from pydantic import BaseModel, ConfigDict


# ---------- Products ----------

class ProductBase(BaseModel):
    name: str
    price_cny_per_ton: float
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
    usd_cny_rate: float = 7.24
    usd_eur_rate: float = 0.92


class ExpensesUpdate(ExpensesBase):
    pass


class ExpensesOut(ExpensesBase):
    model_config = ConfigDict(from_attributes=True)


# ---------- Calculate ----------

class CalculateRequest(BaseModel):
    product_id: int
    tonnage: float = 21.0
    margin_usd_per_ton: float = 0.0


class DestinationPrice(BaseModel):
    destination: str
    incoterm: str
    price_per_ton_usd: float
    price_per_ton_eur: Optional[float] = None
    total_usd: float
    total_eur: Optional[float] = None


class CalculateResponse(BaseModel):
    product: ProductOut
    tonnage: float
    base_price_usd_per_ton: float
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
