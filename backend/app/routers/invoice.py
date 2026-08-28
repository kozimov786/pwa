from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from .. import schemas
from ..services.invoice import INVOICE_TEMPLATES, generate_invoice_pdf, list_companies

router = APIRouter(prefix="/api/invoice", tags=["invoice"])


@router.get("/companies")
def get_companies():
    return list_companies()


@router.post("/generate")
def generate(payload: schemas.InvoiceRequest):
    if payload.company_key not in INVOICE_TEMPLATES:
        raise HTTPException(status_code=404, detail="Unknown company template")
    try:
        pdf_bytes = generate_invoice_pdf(
            payload.company_key,
            payload.tarih,
            payload.contract_no,
            payload.unit_price,
            payload.total_price,
            payload.currency,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="LibreOffice (soffice) not found on server")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="proforma_invoice.pdf"'},
    )
