import pandas as pd
import logging
from pathlib import Path
from docxtpl import DocxTemplate

from services.log_service import NOME_LOGGER
logger = logging.getLogger(NOME_LOGGER)

# ========================================
# CONFIGURAÇÕES
# ========================================

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "input"
DEFAULT_FILE_NAME = "template_carta_laudo.docx"

# ========================================
# DECLARANDO COLUNAS
# ========================================

REQUIRED_COLUMNS = [
    "veiculo",
    "marca",
    "modelo",
    "ano_fabri_ano_modelo",
    "tipo_veiculo",
    "chassis",
    "motor",
    "cor",
    "potencia",
    "cilindrada",
    "combustivel",
    "cmt",
    "pbt",
    "capacidade_passageiros",
    "nome_razao_social",
    "cpf_cnpj",
    "campo_correcao",
    "nome_assinante",
    "sede_cidade_byd",
    "data_carta_laudo",
    "cabecalho_empresa",
    "cabecalho_endereco",
    "cabecalho_cep",
    "empresa_cnpj",
]


# ========================================
# CRIANDO A CLASS
# ========================================

class ValidationService:

    # ========================================
    # VALIDANDO COLUNAS OBRIGATÓRIAS NO DF
    # ========================================

    def validate_columns(self,df: pd.DataFrame) -> pd.DataFrame:
        for column in REQUIRED_COLUMNS:
            if column not in df.columns:
                raise ValueError (f"Coluna: '{column}' não encontrada no arquivo no Excel.")
        return df

    # ========================================
    # VALIDANDO COLUNAS VAZIAS
    # ========================================

    def validate_empty(self,df):
        for column in REQUIRED_COLUMNS: # Estou olhando a coluna toda.
            for index, valor in df[column].items(): # Para cada item dentro dessa coluna
                if pd.isna(valor) or str(valor).strip() == "":
                    raise ValueError(
                        f"Valor vazio na coluna: '{column}'\n"
                        f"Linha: '{index + 2}' do seu excel.")  # Mostra a Linha onde esta o erro.

    # ========================================
    # VALIDANDO COLUNA DE CHASSI COM 17 CARACTERES
    # ========================================

    def validate_chassis(self,df):
        for index, chassi in df["chassis"].items():
            if len(chassi) != 17:
                raise ValueError(
                    f"Erro na quantidade de caracteres do CHASSI: '{chassi}'\n"
                    f"Caracteres encontrados: '{len(chassi)}'\n"
                    f"Caracteres esperados: '17'\n"
                    f"Linha: '{index + 2}' do seu Excel."
                )

    # ========================================
    # VALIDANDO COLUNA DO MOTOR COM 9 CARACTERES
    # ========================================

    def validate_motor(self,df):
        for index, motor in df["motor"].items():
            if len(motor) != 9:
                raise ValueError (f"Erro na quantidade de caracteres do número do MOTOR: '{motor}'\n"
                                  f"Caracteres Encontrado: '{len(motor)}'\n"
                                  f"Caracteres Esperado: '9'\n"
                                  f"Linha: '{index + 2}' do seu excel.")

    # ========================================
    # VALIDANDO COLUNA DO DOCUMENTO
    # ========================================

    def validate_cpf_cnpj(self,df):
        for index, document  in df["cpf_cnpj"].items():
            document = "".join(c for c in document if c.isdigit())

            if len(document) not in (11, 14) :
                raise ValueError(f"Erro na quantidade de caracteres do CPF/CNPJ: '{document}'\n"
                                 f"Caracteres Encontrado: '{len(document )}'\n"
                                 f"Caracteres esperados: CPF = 11 ou CNPJ = 14\n"
                                 f"Linha: '{index + 2}' do seu excel.")

    # ========================================
    # ORQUESTRADOR DAS FUNÇÕES DE VALIDAÇÃO
    # ========================================

    def validate(self,df: pd.DataFrame):

        logger.info("validando arquivo excel...")
        logger.info("validando colunas obrigatorias")
        self.validate_columns(df)
        logger.info("validando colunas vazias")
        self.validate_empty(df)
        logger.info("validando coluna do chassis")
        self.validate_chassis(df)
        logger.info("validando coluna do motor")
        self.validate_motor(df)
        logger.info("validando coluna do documento")
        self.validate_cpf_cnpj(df)

        logger.info("Arquivo validado com sucesso")
        logger.info("=" * 60)
        return df

    # ========================================
    # VALIDANDO CAMPOS OBRIGATÓRIOS NO TEMPLATE
    # ========================================

    def validate_template(self, file_name: Path = DEFAULT_FILE_NAME) -> None:

        template_path = INPUT_DIR / file_name

        if not template_path.exists():
            raise FileNotFoundError(
                f"Template Word não encontrado: '{template_path}'"
            )

        template = DocxTemplate(template_path)

        template_variables = (
            template.get_undeclared_template_variables()
        )

        missing_variables = (
                set(REQUIRED_COLUMNS) - set(template_variables)
        )

        if missing_variables:
            missing_fields = "\n".join(
                f"- {{{{ {field} }}}}"
                for field in sorted(missing_variables)
            )

            raise ValueError(
                "Campos obrigatórios não encontrados no template Word:\n"
                f"{missing_fields}"
            )

        logger.info("Template Word validado com sucesso")
        logger.info("=" * 60)