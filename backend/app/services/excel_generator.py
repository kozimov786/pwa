import io
from datetime import date

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HEADER_FILL = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
ALT_FILL = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=11)
THIN = Side(style="thin", color="CBD5E1")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def generate_quotation_excel(product_name: str, tonnage: float, base_price: float, legs: list[dict]) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Quotation"

    ws.merge_cells("A1:F1")
    ws["A1"] = "Wholesale Trade Quotation"
    ws["A1"].font = Font(bold=True, size=16)

    ws["A2"] = "Product"
    ws["B2"] = product_name
    ws["A3"] = "Date"
    ws["B3"] = date.today().isoformat()
    ws["A4"] = "Tonnage (t)"
    ws["B4"] = tonnage
    ws["A5"] = "Base ex-works price (USD/t)"
    ws["B5"] = base_price
    for r in range(2, 6):
        ws[f"A{r}"].font = Font(bold=True)

    header_row = 7
    headers = ["Destination", "Incoterm", "USD/ton", "EUR/ton", "Total USD", "Total EUR"]
    for col, h in enumerate(headers, start=1):
        cell = ws.cell(row=header_row, column=col, value=h)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center")
        cell.border = BORDER

    for i, leg in enumerate(legs):
        row = header_row + 1 + i
        values = [
            leg["destination"],
            leg["incoterm"],
            leg["price_per_ton_usd"],
            leg.get("price_per_ton_eur") or "-",
            leg["total_usd"],
            leg.get("total_eur") or "-",
        ]
        for col, v in enumerate(values, start=1):
            cell = ws.cell(row=row, column=col, value=v)
            cell.border = BORDER
            if i % 2 == 1:
                cell.fill = ALT_FILL

    for col in range(1, 7):
        ws.column_dimensions[get_column_letter(col)].width = 20

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()
