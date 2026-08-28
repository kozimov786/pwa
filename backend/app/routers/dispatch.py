from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..database import SessionLocal
from ..routers.calculate import build_calculation
from ..services.excel_generator import generate_quotation_excel
from ..services.pdf_generator import generate_quotation_pdf
from ..services.whatsapp import dispatch_to_group

router = APIRouter(prefix="/api/dispatch-group", tags=["dispatch"])


async def _run_dispatch(payload: schemas.DispatchRequest):
    attachments = []
    if payload.calculate_payload and (payload.include_pdf or payload.include_excel):
        db: Session = SessionLocal()
        try:
            calc = build_calculation(db, payload.calculate_payload)
        finally:
            db.close()
        legs = [d.model_dump() for d in calc.destinations]
        safe_name = calc.product.name.replace(" ", "_")
        if payload.include_pdf:
            pdf_bytes = generate_quotation_pdf(calc.product.name, calc.tonnage, calc.base_price_usd_per_ton, legs)
            attachments.append((pdf_bytes, f"quotation_{safe_name}.pdf"))
        if payload.include_excel:
            xlsx_bytes = generate_quotation_excel(calc.product.name, calc.tonnage, calc.base_price_usd_per_ton, legs)
            attachments.append((xlsx_bytes, f"quotation_{safe_name}.xlsx"))

    await dispatch_to_group(payload.message, attachments)


@router.post("", status_code=202)
def dispatch_group(payload: schemas.DispatchRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(_run_dispatch, payload)
    return {"status": "queued"}
