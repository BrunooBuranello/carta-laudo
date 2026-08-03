from services.excel_service import ExcelService
from services.validation_service import ValidationService

excel = ExcelService()
validation = ValidationService()
try:
    df = excel.read()
    df = validation.validate(df)


except Exception as error:
    print(f"Aviso: \n{error}")