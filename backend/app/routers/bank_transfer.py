from fastapi import APIRouter
from fastapi.responses import Response

from .. import schemas
from ..services.bank_transfer import generate_bank_transfer_pdf

router = APIRouter(prefix="/api/bank-transfer-talimati", tags=["bank-transfer"])


@router.post("")
def bank_transfer_talimati(payload: schemas.BankTransferRequest):
    pdf_bytes = generate_bank_transfer_pdf(
        beneficiary_name=payload.beneficiary_name,
        beneficiary_iban=payload.beneficiary_iban,
        beneficiary_bank=payload.beneficiary_bank,
        swift_code=payload.swift_code,
        amount=payload.amount,
        currency=payload.currency,
        reference=payload.reference,
        ordering_customer=payload.ordering_customer,
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="bank_transfer_talimati.pdf"'},
    )
