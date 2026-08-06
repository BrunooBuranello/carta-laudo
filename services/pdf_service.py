from pathlib import Path
import logging
import subprocess
import shutil
import win32com.client as win32

from services.log_service import NOME_LOGGER
logger = logging.getLogger(NOME_LOGGER)

# ========================================
# CONFIGURAÇÕES CONVERTOR
# ========================================

caminho_soffice_path = shutil.which("soffice")
caminho_soffice_1 = Path("C:/Program Files/LibreOffice/program/soffice.exe")
caminho_soffice_2 = Path("C:/Program Files (x86)/LibreOffice/program/soffice.exe")

class PdfService:

    def file_exists(self, docx_path: Path) -> Path:
        docx_path = Path(docx_path)


        if not docx_path.parent.is_dir():
            raise FileNotFoundError(
                f"Diretório não encontrado:\n{docx_path}"
            )

        if not docx_path.is_file():
            raise FileNotFoundError(
                f"Arquivo não encontrado:\n{docx_path.name}\n"
                f"Caminho procurado:\n{docx_path.parent}"
            )

        if docx_path.suffix.lower() != ".docx":
            raise ValueError(
                f"Arquivo encontrado não possui formato '.docx':\n"
                f"'{docx_path.name}'"
            )

        logger.info(f"Arquivo encontrado: {docx_path.name}")
        return docx_path



    def get_converter(self):

        try:
            # ========================================
            # Word
            # ========================================

            # Inicia uma nova instância do Microsoft Word
            word = win32.DispatchEx("Word.Application")

            # Torna o Word visível na tela
            word.Visible = False
            logger.info(f"Conversor encontrado: Word")
            return "Word", word

        except Exception:
            logger.info(f"Word não encontrado. Tentando LibreOffice...")

            # ========================================
            # LibreOffice
            # ========================================

            if caminho_soffice_path:
                logger.info(f"Conversor encontrado: LibreOffice")
                return "LibreOffice",caminho_soffice_path

            elif caminho_soffice_1.is_file():
                logger.info(f"Conversor encontrado: LibreOffice")
                return "LibreOffice",caminho_soffice_1

            elif caminho_soffice_2.is_file():
                logger.info(f"Conversor encontrado: LibreOffice")
                return "LibreOffice",caminho_soffice_2

            else:
                logger.info("LibreOffice não está instalado ou não está no PATH.")
                return None, None


    def delete_docx(self, docx_path: Path) -> None:
        docx_path = Path(docx_path)

        if docx_path.is_file():
            docx_path.unlink()
            logger.info("DOCX temporário removido: %s", docx_path.name)



    def convert_pdf(
            self,
            docx_path: Path,
            delete_docx: bool = True,
    ) -> Path:

        docx_path = self.file_exists(docx_path)
        path_pdf = docx_path.with_suffix(".pdf")
        conversor, executavel = self.get_converter()

        if conversor is None:
            raise RuntimeError(
                "Nenhum conversor disponível: Word ou LibreOffice."
            )

        try:
            # ========================================
            # Word
            # ========================================
            if conversor == "Word":
                word = executavel
                documento  = None

                try:
                    documento = word.Documents.Open(
                        str(docx_path.resolve())
                    )

                    documento.ExportAsFixedFormat(
                        OutputFileName=str(path_pdf.resolve()),
                        ExportFormat=17
                    )

                    if not path_pdf.is_file():
                        raise RuntimeError(
                            f"O Word não gerou o PDF: {path_pdf.name}"
                        )

                    logger.info(
                        "Conversão realizada com sucesso: %s",
                        path_pdf.name
                    )

                finally:
                    if documento is not None:
                        documento.Close(SaveChanges=False)

                    word.Quit()

            # ========================================
            # LibreOffice
            # ========================================
            elif conversor == "LibreOffice":

                resultado = subprocess.run(
                    [
                        str(executavel),
                        "--headless",
                        "--convert-to",
                        "pdf",
                        "--outdir",
                        str(docx_path.parent.resolve()),
                        str(docx_path.resolve()),
                    ],
                    capture_output=True,
                    text=True,
                )

                if resultado.returncode != 0:
                    raise RuntimeError(
                        f"Erro do LibreOffice: {resultado.stderr.strip()}"
                    )

                if not path_pdf.is_file():
                    raise RuntimeError(
                        f"O LibreOffice não gerou o PDF: {path_pdf.name}"
                    )

                logger.info(
                    "Conversão realizada com sucesso: %s",
                    path_pdf.name
                )

        except Exception:
            logger.exception(
                "Erro ao converter '%s' para PDF.",
                docx_path.name
            )
            raise

        if not path_pdf.is_file():
            raise RuntimeError(
                f"PDF não foi encontrado após a conversão: {path_pdf.name}"
            )

        if delete_docx:
            self.delete_docx(docx_path)
        logger.info("-" * 60)
        return path_pdf
