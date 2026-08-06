import os
import requests
from dotenv import load_dotenv

load_dotenv()

MSG_WECOM = os.getenv("WECOM_WEBHOOK")

if not MSG_WECOM:
    raise RuntimeError(
        "Variável 'WECOM_WEBHOOK' não encontrada no arquivo .env."
    )


def enviar_msg_wecom(mensagem, logger):
    try:
        payload = {
            "msgtype": "text",
            "text": {
                "content": mensagem
            }
        }

        resposta = requests.post(
            MSG_WECOM,
            json=payload,
            timeout=10,
        )

        resposta.raise_for_status()

        logger.info(
            "[WECOM] Mensagem enviada com sucesso."
        )

    except Exception as erro:
        logger.exception(
            f"[WECOM] Falha ao enviar mensagem | erro='{erro}'"
        )
        raise