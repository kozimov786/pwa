import io
import os
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
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

from .fonts import font_for_lang
from .i18n import t

DARK_BG = colors.HexColor("#0f172a")
LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")


def _letterhead(name_style):
    logo = Image(LOGO_PATH, width=16 * mm, height=16 * mm) if os.path.exists(LOGO_PATH) else Spacer(16 * mm, 16 * mm)
    header = Table(
        [[logo, Paragraph("GOKLE", name_style)]],
        colWidths=[18 * mm, 40 * mm],
    )
    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (1, 0), (1, 0), 4),
                ("LEFTPADDING", (0, 0), (0, 0), 0),
            ]
        )
    )
    return header


def _build_pdf(subtitle_html: str, table_headers: list[str], table_rows: list[list[str]], col_widths: list[float], lang: str) -> bytes:
    font = font_for_lang(lang)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm, leftMargin=18 * mm, rightMargin=18 * mm
    )
    styles = getSampleStyleSheet()
    name_style = ParagraphStyle(
        "GokleName", parent=styles["Title"], fontName=font, textColor=DARK_BG, fontSize=20, spaceAfter=4, alignment=TA_LEFT
    )
    sub_style = ParagraphStyle("Sub", parent=styles["Normal"], fontName=font, textColor=colors.grey, fontSize=10)
    header_style = ParagraphStyle(
        "TableHeader", parent=styles["Normal"], fontName=font, fontSize=9.5, textColor=colors.white, leading=11
    )

    elements = [
        _letterhead(name_style),
        Spacer(1, 6 * mm),
        Paragraph(subtitle_html, sub_style),
        Spacer(1, 10 * mm),
    ]

    data = [[Paragraph(h, header_style) for h in table_headers]] + table_rows
    table = Table(data, colWidths=[w * mm for w in col_widths])
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), DARK_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), font),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    table.setStyle(TableStyle(style))
    elements.append(table)
    elements.append(Spacer(1, 12 * mm))
    elements.append(Paragraph(t(lang, "disclaimer"), sub_style))

    doc.build(elements)
    return buf.getvalue()


def generate_quotation_pdf(product_name: str, weight_kg: float, legs: list[dict], lang: str = "en") -> bytes:
    subtitle = (
        f"{t(lang, 'product')}: <b>{product_name}</b> &nbsp;|&nbsp; "
        f"{t(lang, 'weight')}: <b>{weight_kg:,.0f} kg</b> &nbsp;|&nbsp; "
        f"{t(lang, 'date')}: {date.today().isoformat()}"
    )
    headers = [t(lang, "col_destination"), t(lang, "col_total_kg"), t(lang, "col_price_per_kg"), t(lang, "col_total_cost")]
    rows = [
        [
            leg["destination"],
            f"{weight_kg:,.0f}",
            f"{leg['price_per_kg_usd']:.2f}$",
            f"{leg['total_usd']:,.2f}",
        ]
        for leg in legs
    ]
    return _build_pdf(subtitle, headers, rows, [52, 26, 40, 44], lang)


def generate_comparison_pdf(destination: str, rows: list[dict], lang: str = "en") -> bytes:
    subtitle = (
        f"{t(lang, 'destination')}: <b>{destination}</b> &nbsp;|&nbsp; "
        f"{t(lang, 'date')}: {date.today().isoformat()}"
    )
    headers = [t(lang, "col_product"), t(lang, "col_total_kg"), t(lang, "col_price_per_kg"), t(lang, "col_total_cost")]
    table_rows = [
        [
            row["product_name"],
            f"{row['weight_kg']:,.0f}",
            f"{row['price_per_kg_usd']:.2f}$",
            f"{row['total_usd']:,.2f}",
        ]
        for row in rows
    ]
    return _build_pdf(subtitle, headers, table_rows, [52, 26, 40, 44], lang)
