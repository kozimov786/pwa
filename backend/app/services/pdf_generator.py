import io
import os
from datetime import date

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
)

DARK_BG = colors.HexColor("#0f172a")
LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")


def _letterhead(title_style):
    logo = Image(LOGO_PATH, width=16 * mm, height=16 * mm) if os.path.exists(LOGO_PATH) else Spacer(16 * mm, 16 * mm)
    header = Table(
        [[logo, Paragraph("GOKLE", title_style)]],
        colWidths=[20 * mm, None],
    )
    header.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (1, 0), (1, 0), 6)]))
    return header


def generate_quotation_pdf(product_name: str, weight_kg: float, base_price_usd_per_kg: float, legs: list[dict]) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm, leftMargin=18 * mm, rightMargin=18 * mm
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title", parent=styles["Title"], textColor=DARK_BG, fontSize=20, spaceAfter=4
    )
    sub_style = ParagraphStyle("Sub", parent=styles["Normal"], textColor=colors.grey, fontSize=10)

    elements = [
        _letterhead(title_style),
        Spacer(1, 4 * mm),
        Paragraph("Wholesale Trade Quotation", ParagraphStyle("Sub2", parent=sub_style, fontSize=12, textColor=DARK_BG)),
        Paragraph(f"Product: <b>{product_name}</b> &nbsp;|&nbsp; Date: {date.today().isoformat()}", sub_style),
        Paragraph(
            f"Weight: <b>{weight_kg:,.0f} kg</b> &nbsp;|&nbsp; Base purchase price: <b>${base_price_usd_per_kg}/kg</b>",
            sub_style,
        ),
        Spacer(1, 10 * mm),
    ]

    header = ["Mahsulot", "Yo'nalish", "Jami kg", "1 kg narx (USD)", "Jami maliyet (USD)"]
    data = [header]
    for leg in legs:
        data.append(
            [
                product_name,
                leg["destination"],
                f"{weight_kg:,.0f}",
                f"{leg['price_per_kg_usd']:.4f}",
                f"{leg['total_usd']:,.2f}",
            ]
        )

    table = Table(data, colWidths=[32 * mm, 42 * mm, 24 * mm, 32 * mm, 32 * mm])
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), DARK_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    table.setStyle(TableStyle(style))
    elements.append(table)
    elements.append(Spacer(1, 12 * mm))
    elements.append(
        Paragraph(
            "This quotation is indicative and subject to final contract terms, quality inspection and FX rate at time of payment.",
            sub_style,
        )
    )

    doc.build(elements)
    return buf.getvalue()
