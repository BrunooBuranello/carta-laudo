from services.excel_service import ExcelService
from services.pdf_service import PdfService
from services.validation_service import ValidationService
from services.log_service import configurar_logger
from services.template_service import TemplateService
from services.context_service import ContextService

import sys


def main():

    logger = configurar_logger()
    excel = ExcelService()
    validation = ValidationService()
    template_service = TemplateService()
    context_service = ContextService()
    pdf_service = PdfService()

    total_chassis = 0
    documentos_docx_processados = 0
    documentos_pdf_gerados = 0

    try:
        df = excel.read()
        df = validation.validate(df)
        validation.validate_template()

        total_chassis = len(df)

        logger.info(
            "Total de chassis encontrados no arquivo: %s",
            total_chassis,
        )

        for numero, contexto in enumerate(
                context_service.create_all(df),
                start=1,
        ):
            percentual = (numero / total_chassis) * 100

            logger.info(
                "Progresso: %s/%s | %.1f%% | Chassi: %s",
                numero,
                total_chassis,
                percentual,
                contexto["chassis"],
            )

            caminho_docx = template_service.generate(contexto)
            documentos_docx_processados += 1

            pdf_path = pdf_service.convert_pdf(
                caminho_docx,
                delete_docx=True,
            )

            documentos_pdf_gerados += 1

        logger.info("################### RESUMO DA EXECUÇÃO ###################")
        logger.info("Status....................: SUCESSO")
        logger.info("Registros lidos...........: %s", total_chassis)
        logger.info("DOCX processados..........: %s", documentos_docx_processados)
        logger.info("PDFs gerados..............: %s", documentos_pdf_gerados)
        logger.info("##########################################################")

    except Exception as error:
        logger.info("################### RESUMO DA EXECUÇÃO ###################")
        logger.info("Status....................: ERRO")
        logger.info("Registros lidos...........: %s", total_chassis)
        logger.info("DOCX processados..........: %s", documentos_docx_processados)
        logger.info("PDFs gerados..............: %s", documentos_pdf_gerados)
        logger.exception("Erro durante a execução: %s", error)
        logger.info("##########################################################")
        sys.exit(1)


if __name__ == "__main__":
    main()