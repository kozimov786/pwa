import io
from datetime import date

from num2words import num2words
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from .pdf_generator import _letterhead

CURRENCY_WORDS_TR = {
    "USD": ("Amerikan Doları", "Sent"),
    "EUR": ("Euro", "Sent"),
    "TRY": ("Türk Lirası", "Kuruş"),
    "CNY": ("Çin Yuanı", "Fen"),
}


def amount_to_turkish_words(amount: float, currency: str) -> str:
    major = int(amount)
    minor = round((amount - major) * 100)
    unit_name, minor_name = CURRENCY_WORDS_TR.get(currency, (currency, "Kuruş"))
    major_words = num2words(major, lang="tr").capitalize()
    text = f"{major_words} {unit_name}"
    if minor:
        minor_words = num2words(minor, lang="tr")
        text += f" {minor_words} {minor_name}"
    return text + " (Yalnız)"


def generate_bank_transfer_pdf(
    beneficiary_name: str,
    beneficiary_iban: str,
    beneficiary_bank: str,
    swift_code: str,
    amount: float,
    currency: str,
    reference: str,
    ordering_customer: str,
) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm, leftMargin=18 * mm, rightMargin=18 * mm
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("Title", parent=styles["Title"], fontSize=18, spaceAfter=6)
    normal = styles["Normal"]

    amount_words = amount_to_turkish_words(amount, currency)

    rows = [
        ["Talimat Tarihi / Instruction Date", date.today().isoformat()],
        ["Emreden / Ordering Customer", ordering_customer or "-"],
        ["Lehtar / Beneficiary", beneficiary_name],
        ["IBAN", beneficiary_iban],
        ["Banka / Bank", beneficiary_bank],
        ["SWIFT/BIC", swift_code],
        ["Tutar / Amount", f"{amount:,.2f} {currency}"],
        ["Tutar Yazı ile / Amount in Words", amount_words],
        ["Açıklama / Reference", reference or "-"],
    ]

    table = Table(rows, colWidths=[65 * mm, 95 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#0f172a")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
            ]
        )
    )

    elements = [
        _letterhead(title_style),
        Spacer(1, 4 * mm),
        Paragraph("Havale / EFT Talimatı", ParagraphStyle("Sub2", parent=normal, fontSize=14)),
        Paragraph("Turkish Bank Transfer Instruction", normal),
        Spacer(1, 8 * mm),
        table,
        Spacer(1, 12 * mm),
        Paragraph(
            "Bu talimat bilgi amaçlıdır; işlem bankanızın onayına ve güncel kur şartlarına tabidir.",
            normal,
        ),
    ]
    doc.build(elements)
    return buf.getvalue()
