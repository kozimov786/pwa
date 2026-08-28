from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from .. import schemas
from ..services.vakif_transfer import COMPANY_TEMPLATES, generate_transfer_pdf, list_companies

router = APIRouter(prefix="/api/vakif-transfer", tags=["vakif-transfer"])


@router.get("/companies")
def get_companies():
    return list_companies()


@router.post("/generate")
def generate(payload: schemas.VakifTransferRequest):
    if payload.company_key not in COMPANY_TEMPLATES:
        raise HTTPException(status_code=404, detail="Unknown company template")
    try:
        pdf_bytes = generate_transfer_pdf(
            payload.company_key,
            payload.tarih,
            payload.valor_tarihi,
            payload.amount,
            payload.currency,
            payload.contract_no,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="LibreOffice (soffice) not found on server")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="vakifbank_transfer.pdf"'},
    )
