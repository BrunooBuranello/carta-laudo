from services.excel_service import ExcelService
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

    try:
        df = excel.read()
        df = validation.validate(df)

        validation.validate_template()

        total_chassis = len(df)

        logger.info(
            "Total de chassis encontrados no arquivo: %s",
            total_chassis,
        )

        documentos_gerados = 0

        for numero, contexto in enumerate(
            context_service.create_all(df),
            start=1,
        ):
            caminho = template_service.generate(contexto)

            documentos_gerados += 1
            percentual = (numero / total_chassis) * 100

            logger.info(
                "Progresso: %s/%s | %.1f%% | Chassi: %s",
                numero,
                total_chassis,
                percentual,
                contexto["chassis"],
            )

            logger.info(
                "Documento gerado: %s",
                caminho.name,
            )

        logger.info("=" * 60)
        logger.info(
            "Processo finalizado com sucesso. "
            "Total de documentos gerados: %s",
            documentos_gerados,
        )

    except Exception as error:
        logger.error("Aviso:\n%s", error)
        sys.exit(1)


if __name__ == "__main__":
    main()