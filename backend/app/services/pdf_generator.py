import io
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
)

DARK_BG = colors.HexColor("#0f172a")
NEON = colors.HexColor("#22d3ee")
ROW_ALT = colors.HexColor("#1e293b")


def generate_quotation_pdf(product_name: str, tonnage: float, base_price: float, legs: list[dict]) -> bytes:
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
        Paragraph("Wholesale Trade Quotation", title_style),
        Paragraph(f"Product: <b>{product_name}</b> &nbsp;|&nbsp; Date: {date.today().isoformat()}", sub_style),
        Paragraph(f"Tonnage: <b>{tonnage} t</b> &nbsp;|&nbsp; Base ex-works price: <b>${base_price}/t</b>", sub_style),
        Spacer(1, 10 * mm),
    ]

    header = ["Destination", "Incoterm", "USD/ton", "EUR/ton", "Total USD", "Total EUR"]
    data = [header]
    for leg in legs:
        data.append(
            [
                leg["destination"],
                leg["incoterm"],
                f"{leg['price_per_ton_usd']:.2f}",
                f"{leg['price_per_ton_eur']:.2f}" if leg.get("price_per_ton_eur") else "-",
                f"{leg['total_usd']:.2f}",
                f"{leg['total_eur']:.2f}" if leg.get("total_eur") else "-",
            ]
        )

    table = Table(data, colWidths=[38 * mm, 22 * mm, 22 * mm, 22 * mm, 26 * mm, 26 * mm])
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
