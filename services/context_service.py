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
    "descricao_modelo",
    "ano_modelo",
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

        for _, row in df.iterrows():
            yield self.create(row)