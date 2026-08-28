from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..routers.calculate import build_calculation
from ..services.excel_generator import generate_quotation_excel
from ..services.pdf_generator import generate_quotation_pdf

router = APIRouter(prefix="/api/export", tags=["export"])


@router.post("/pdf")
def export_pdf(payload: schemas.CalculateRequest, db: Session = Depends(get_db)):
    calc = build_calculation(db, payload)
    pdf_bytes = generate_quotation_pdf(
        calc.product.name, calc.tonnage, calc.base_price_usd_per_ton,
        [d.model_dump() for d in calc.destinations],
    )
    filename = f"quotation_{calc.product.name.replace(' ', '_')}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/excel")
def export_excel(payload: schemas.CalculateRequest, db: Session = Depends(get_db)):
    calc = build_calculation(db, payload)
    xlsx_bytes = generate_quotation_excel(
        calc.product.name, calc.tonnage, calc.base_price_usd_per_ton,
        [d.model_dump() for d in calc.destinations],
    )
    filename = f"quotation_{calc.product.name.replace(' ', '_')}.xlsx"
    return Response(
        content=xlsx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
