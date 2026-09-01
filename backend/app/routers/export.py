from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..routers.calculate import build_calculation
from ..services.excel_generator import generate_comparison_excel, generate_quotation_excel
from ..services.pdf_generator import generate_comparison_pdf, generate_quotation_pdf

router = APIRouter(prefix="/api/export", tags=["export"])


@router.post("/pdf")
async def export_pdf(payload: schemas.CalculateRequest, db: Session = Depends(get_db)):
    calc = await build_calculation(db, payload)
    product_name = calc.product.name_for(payload.lang)
    pdf_bytes = generate_quotation_pdf(
        product_name, calc.weight_kg,
        [d.model_dump() for d in calc.destinations],
        lang=payload.lang,
    )
    filename = f"quotation_{product_name.replace(' ', '_')}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/excel")
async def export_excel(payload: schemas.CalculateRequest, db: Session = Depends(get_db)):
    calc = await build_calculation(db, payload)
    product_name = calc.product.name_for(payload.lang)
    xlsx_bytes = generate_quotation_excel(
        product_name, calc.weight_kg,
        [d.model_dump() for d in calc.destinations],
        lang=payload.lang,
    )
    filename = f"quotation_{product_name.replace(' ', '_')}.xlsx"
    return Response(
        content=xlsx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


async def _build_comparison_rows(db: Session, payload: schemas.ComparisonExportRequest) -> list[dict]:
    rows = []
    for row in payload.rows:
        calc = await build_calculation(
            db,
            schemas.CalculateRequest(
                product_id=row.product_id,
                weight_kg=row.weight_kg,
                price_cny_per_kg=row.price_cny_per_kg,
                margin_usd_per_kg=row.margin_usd_per_kg,
                lang=payload.lang,
            ),
        )
        leg = next((d for d in calc.destinations if d.destination == payload.destination), None)
        if leg is None:
            raise HTTPException(status_code=400, detail=f"Unknown destination: {payload.destination}")
        rows.append(
            {
                "product_name": calc.product.name_for(payload.lang),
                "weight_kg": calc.weight_kg,
                "price_per_kg_usd": leg.price_per_kg_usd,
                "total_usd": leg.total_usd,
            }
        )
    return rows


@router.post("/comparison/pdf")
async def export_comparison_pdf(payload: schemas.ComparisonExportRequest, db: Session = Depends(get_db)):
    rows = await _build_comparison_rows(db, payload)
    pdf_bytes = generate_comparison_pdf(payload.destination, rows, lang=payload.lang)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="comparison.pdf"'},
    )


@router.post("/comparison/excel")
async def export_comparison_excel(payload: schemas.ComparisonExportRequest, db: Session = Depends(get_db)):
    rows = await _build_comparison_rows(db, payload)
    xlsx_bytes = generate_comparison_excel(payload.destination, rows, lang=payload.lang)
    return Response(
        content=xlsx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="comparison.xlsx"'},
    )
