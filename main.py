from services.excel_service import ExcelService

excel = ExcelService()

try:
    file_path = excel.read()


except Exception as error:
    print(f"Aviso: \n{error}")