
import logging
from pathlib import Path

# Localiza a pasta principal do projeto
PASTA_PROJETO = Path(__file__).resolve().parent

# Pasta onde os logs serão armazenados
PASTA_LOGS = PASTA_PROJETO / "logs"
PASTA_LOGS.mkdir(exist_ok=True)

# Arquivo de registro das execuções
ARQUIVO_LOG = PASTA_LOGS / "pipeline.log"


def registrar_log(mensagem, nivel="INFO"):
    logging.basicConfig(
        filename=ARQUIVO_LOG,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8"
    )

    if nivel == "ERRO":
        logging.error(mensagem)
    else:
        logging.info(mensagem)
