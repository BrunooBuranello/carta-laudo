from pathlib import Path

from services.excel_service import ExcelService


excel_service = ExcelService()

file_path = Path("input") / "Carta Laudo_2026-07-31_17-30-13.xlsx"

data = excel_service.read(file_path)

print(data.head(10))
