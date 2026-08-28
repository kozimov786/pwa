from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..routers.expenses import _get_or_create_settings
from ..services.pricing import calculate_landed_prices, legs_to_response

router = APIRouter(prefix="/api/calculate", tags=["calculate"])


def build_calculation(db: Session, payload: schemas.CalculateRequest) -> schemas.CalculateResponse:
    product = db.get(models.Product, payload.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    settings = _get_or_create_settings(db)
    base_price, legs = calculate_landed_prices(
        product, settings, payload.tonnage, payload.margin_usd_per_ton
    )
    destinations = legs_to_response(legs, payload.tonnage)

    return schemas.CalculateResponse(
        product=product,
        tonnage=payload.tonnage,
        base_price_usd_per_ton=base_price,
        destinations=destinations,
    )


@router.post("", response_model=schemas.CalculateResponse)
def calculate(payload: schemas.CalculateRequest, db: Session = Depends(get_db)):
    return build_calculation(db, payload)
