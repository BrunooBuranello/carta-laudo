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
            word = win32.Dispatch("Word.Application")

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



    def convert_pdf(self,docx_path: Path) -> Path:

        docx_path = self.file_exists(docx_path)
        path_pdf = docx_path.with_suffix(".pdf")
        conversor, executavel = self.get_converter()

        if conversor is None:
            logger.error("Nenhum conversor disponível.")
            return path_pdf

        try:
            # ========================================
            # Word
            # ========================================
            if conversor == "Word":
                word = executavel
                documento  = word.Documents.Open(...)

                word.Quit()

                ...

            # ========================================
            # LibreOffice
            # ========================================
            elif conversor == "LibreOffice":

                resultado = subprocess.run([
                    executavel,
                    "--headless",
                    "--convert-to",
                    "pdf",
                    docx_path,
                ])

                if resultado.returncode != 0:
                    logger.info(f"erro ao converter para pdf...")

                elif not path_pdf.is_file():
                    logger.info(f"erro ao converter para pdf...")

                else:
                    logger.info(f"Conversao, realizada com sucesso")

        except Exception as e:
            logger.info(f"erro  {e}")



        logger.info("-" * 60)
        return path_pdf







