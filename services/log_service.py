import logging
import getpass
import sys
from datetime import datetime
from pathlib import Path
import platform


# ========================================
# CONFIGURAÇÕES DO MODULO LOG_SERVICE.PY
# ========================================


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = (BASE_DIR/"logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
NOME_LOGGER = "CARTA_LAUDO"

# ========================================
# FUNÇÃO LOGGER
# ========================================

def configurar_logger(nome_logger: str = NOME_LOGGER) -> logging.Logger:

    usuario = getpass.getuser()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    nome_arquivo = (
        f"{timestamp}_{usuario}_{nome_logger}.txt"
    )

    caminho_log = LOG_DIR / nome_arquivo


    logger = logging.getLogger(f"{nome_logger}")

    logger.setLevel(logging.INFO)

    # evita duplicar log
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # ========================================
    # LOG ARQUIVO
    # ========================================
    file_handler = logging.FileHandler(
        caminho_log,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    # ========================================
    # LOG CONSOLE
    # ========================================
    console_handler = logging.StreamHandler(sys.stdout)

    console_handler.setFormatter(formatter)

    # ========================================
    # ADD HANDLERS
    # ========================================
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # ========================================
    # LOG INICIAL
    # ========================================
    logger.info("=" * 60)
    logger.info(f"INICIANDO PROCESSO: {nome_logger}")
    logger.info(f"Usuário execução: {usuario}")
    logger.info(f"Arquivo log: {nome_arquivo}")
    logger.info(f"Python: {platform.python_version()}")
    logger.info(f"Sistema: {platform.system()} {platform.release()}")
    logger.info("=" * 60)

    return logger
