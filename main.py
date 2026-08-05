from services.excel_service import ExcelService
from services.validation_service import ValidationService
from services.log_service import configurar_logger


def main():

    # ========================================
    # CONFIGURAÇÕES
    # ========================================

    excel = ExcelService()
    validation = ValidationService()
    logger = configurar_logger()

    try:
        df = excel.read()
        df = validation.validate(df)








        logger.info("Processo finalizado com sucesso.")
    except Exception as error:
        logger.exception(f"Aviso: \n{error}")
if __name__ == "__main__":
    main()