from services.excel_service import ExcelService
from services.pdf_service import PdfService
from services.validation_service import ValidationService
from services.log_service import configurar_logger
from services.template_service import TemplateService
from services.context_service import ContextService
from services.wecon_msg import enviar_msg_wecom
from datetime import datetime
import getpass
import platform
import sys

def obter_data_hora() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def main():
    USUARIO = getpass.getuser()
    COMPUTADOR = platform.node()

    logger = configurar_logger()
    excel = ExcelService()
    validation = ValidationService()
    template_service = TemplateService()
    context_service = ContextService()
    pdf_service = PdfService()

    total_chassis = 0
    documentos_docx_processados = 0
    documentos_pdf_gerados = 0
    pdf_path = None

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


        if pdf_path is not None:
            caminho_pdf = pdf_path.parent
        else:
            caminho_pdf = "Não gerado"

        logger.info("################### RESUMO DA EXECUÇÃO ###################")
        logger.info("Status....................: SUCESSO")
        logger.info("Registros lidos...........: %s", total_chassis)
        logger.info("DOCX processados..........: %s", documentos_docx_processados)
        logger.info("PDFs gerados..............: %s", documentos_pdf_gerados)
        logger.info("##########################################################")

        # =====================================================
        # MENSAGEM DE SUCESSO
        # =====================================================
        mensagem = (
            "🚗 Carta de Laudo\n\n"
            "✅ Processo finalizado com sucesso\n\n"
            f"👤 Usuário: {USUARIO}\n"
            f"💻 Computador: {COMPUTADOR}\n"
            f"🕒 Finalizado em: {obter_data_hora()}\n"
            f"📋 Registros lidos: {total_chassis}\n"
            f"📄 DOCX processados: {documentos_docx_processados}\n"
            f"📕 PDFs gerados: {documentos_pdf_gerados}\n"
            f"📂 PDFs salvos em:\n{caminho_pdf}"
        )

        enviar_msg_wecom(mensagem, logger)

    except Exception as error:
        logger.info("################### RESUMO DA EXECUÇÃO ###################")
        logger.info("Status....................: ERRO")
        logger.info("Registros lidos...........: %s", total_chassis)
        logger.info("DOCX processados..........: %s", documentos_docx_processados)
        logger.info("PDFs gerados..............: %s", documentos_pdf_gerados)
        logger.exception("Erro durante a execução: %s", error)
        logger.info("##########################################################")


        # =====================================================
        # MENSAGEM DE ERRO
        # =====================================================
        mensagem = (
            "🚗 Carta de Laudo\n\n"
            "🚨 Processo interrompido por erro\n\n"
            f"👤 Usuário: {USUARIO}\n"
            f"💻 Computador: {COMPUTADOR}\n"
            f"🕒 Interrompido em: {obter_data_hora()}\n"
            f"📋 Registros lidos: {total_chassis}\n"
            f"📄 DOCX processados: {documentos_docx_processados}\n"
            f"📕 PDFs gerados: {documentos_pdf_gerados}\n"
            f"❌ Erro: {error}\n"
        )

        try:
            enviar_msg_wecom(mensagem, logger)

        except Exception:
            logger.exception(
                "[WECOM] Não foi possível enviar a mensagem de erro"
            )

        sys.exit(1)


if __name__ == "__main__":
    main()