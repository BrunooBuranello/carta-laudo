from docxtpl import DocxTemplate
from pathlib import Path
import logging
from datetime import datetime

from services.log_service import NOME_LOGGER
logger = logging.getLogger(NOME_LOGGER)

# ========================================
# CONFIGURAÇÕES
# ========================================

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "input"
DEFAULT_FILE_NAME = "template_carta_laudo.docx"
WORD_OUTPUT_DIR = BASE_DIR / "output"

# ========================================
# CONFIGURAÇÕES CLASS
# ========================================

class TemplateService:

    # ========================================
    # VALIDANDO SE O ARQUIVO EXISTE
    # ========================================
    def file_exists(self, file_name: str = DEFAULT_FILE_NAME) -> Path:
        file_path = INPUT_DIR / file_name

        if not INPUT_DIR.is_dir():
            raise FileNotFoundError(
                f"Diretório não encontrado:\n{INPUT_DIR}"
            )

        if not file_path.is_file():
            raise FileNotFoundError(
                f"Arquivo não encontrado:\n{file_path.name}\n"
                f"Caminho procurado:\n{file_path.parent}"
            )

        if file_path.suffix.lower() != ".docx":
            raise ValueError(
                f"Arquivo encontrado não possui formato '.docx':\n"
                f"'{file_path.name}'"
            )

        return file_path

    # ========================================
    # LEITURA DO DOCUMENTO
    # ========================================
    def read(self) -> DocxTemplate:
        file_path = self.file_exists()

        logger.info("Lendo o arquivo: %s", file_path.name)

        template = DocxTemplate(file_path)

        logger.info("Template carregado com sucesso.")
        logger.info("=" * 60)

        return template

    # ========================================
    # VALIDANDO SE O CONTEXTO POSSUI TODOS
    # OS CAMPOS NECESSÁRIOS PARA O TEMPLATE
    # ========================================

    def validate_context(
            self,
            template: DocxTemplate,
            contexto: dict,
    ) -> None:

        template_variables = set(
            template.get_undeclared_template_variables()
        )

        context_variables = set(contexto.keys())

        missing_variables = (
                template_variables - context_variables
        )

        if missing_variables:
            missing_fields = "\n".join(
                f"- {field.replace('_', ' ').title()}"
                for field in sorted(missing_variables)
            )

            raise ValueError(
                "Não foi possível gerar a Carta Laudo.\n"
                "Os seguintes campos do modelo Word não possuem "
                "informações configuradas para preenchimento:\n"
                f"{missing_fields}\n\n"
                "Verifique o mapeamento desses campos no sistema."
            )

    # ========================================
    # PREENCHENDO O TEMPLATE COM O CONTEXTO
    # ========================================

    def render(
            self,
            template: DocxTemplate,
            contexto: dict
    ) -> None:

        logger.info("Preenchendo template com os dados.")
        template.render(contexto)
        logger.info("Template preenchido com sucesso.")

    # ========================================
    # SALVANDO O ARQUIVO NOVO
    # ========================================

    def salvar_template(
        self,
        template: DocxTemplate,
        contexto: dict
    ) -> Path:

        WORD_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        chassi = contexto["chassis"]
        data = datetime.now().strftime("%Y%m%d_%H%M%S")

        nome_arquivo = f"{chassi}_Carta_Laudo_{data}.docx"
        caminho_saida = WORD_OUTPUT_DIR / nome_arquivo

        template.save(caminho_saida)

        logger.info("Documento salvo: %s", caminho_saida.name)

        return caminho_saida

    # ========================================
    # ORQUESTRADOR
    # ========================================

    def generate(self, contexto: dict) -> Path:

        template = self.read()

        self.validate_context(
            template,
            contexto,
        )

        self.render(
            template,
            contexto,
        )

        return self.salvar_template(
            template,
            contexto,
        )