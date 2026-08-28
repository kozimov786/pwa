from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..routers.expenses import _get_or_create_settings
from ..services.fx import get_usd_cny_rate
from ..services.pricing import calculate_landed_prices, legs_to_response

router = APIRouter(prefix="/api/calculate", tags=["calculate"])


async def build_calculation(db: Session, payload: schemas.CalculateRequest) -> schemas.CalculateResponse:
    product = db.get(models.Product, payload.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    settings = _get_or_create_settings(db)
    fx = await get_usd_cny_rate(fallback=settings.usd_cny_rate_fallback)
    destinations_cfg = (
        db.query(models.Destination)
        .filter(models.Destination.is_active == True)  # noqa: E712
        .order_by(models.Destination.sort_order, models.Destination.id)
        .all()
    )

    base_price, legs = calculate_landed_prices(
        settings, destinations_cfg, payload.price_cny_per_kg, fx.rate, payload.weight_kg, payload.margin_usd_per_kg
    )
    destinations = legs_to_response(legs, payload.weight_kg)

    return schemas.CalculateResponse(
        product=product,
        weight_kg=payload.weight_kg,
        price_cny_per_kg=payload.price_cny_per_kg,
        usd_cny_rate=fx.rate,
        fx_is_live=fx.is_live,
        base_price_usd_per_kg=base_price,
        destinations=destinations,
    )


@router.post("", response_model=schemas.CalculateResponse)
async def calculate(payload: schemas.CalculateRequest, db: Session = Depends(get_db)):
    return await build_calculation(db, payload)
