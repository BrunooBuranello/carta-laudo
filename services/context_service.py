import logging
import pandas as pd

from services.log_service import NOME_LOGGER

logger = logging.getLogger(NOME_LOGGER)

# ========================================
# CAMPOS UTILIZADOS NO CONTEXTO
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
# CONTEXT SERVICE
# ========================================

class ContextService:

    def create(self, row: pd.Series) -> dict:

        contexto = {
            column: row[column]
            for column in REQUIRED_COLUMNS
        }

        return contexto

    def create_all(self, df: pd.DataFrame):

        logger.info(
            "Criando contextos para %s registros.",
            len(df),
        )

        logger.info("=" * 60)
        for _, row in df.iterrows():
            yield self.create(row)
