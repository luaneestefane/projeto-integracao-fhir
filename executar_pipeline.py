
import subprocess
import sys
from pathlib import Path

# Pasta principal do projeto
PASTA_PROJETO = Path(__file__).resolve().parent


def executar_etapa(nome, arquivo):
    print(f"\n=== {nome} ===", flush=True)

    resultado = subprocess.run(
        [sys.executable, str(PASTA_PROJETO / arquivo)],
        cwd=PASTA_PROJETO
    )

    if resultado.returncode != 0:
        print(f"\nERRO: A etapa '{nome}' falhou.")
        print("Pipeline interrompido.")
        sys.exit(resultado.returncode)


print("=== INICIANDO PIPELINE ETL FHIR ===", flush=True)

# Etapa 1: Validação dos dados
executar_etapa(
    "ETAPA 1 - VALIDAÇÃO DOS DADOS",
    "validar_dados.py"
)

# Etapa 2: Transformação para FHIR
executar_etapa(
    "ETAPA 2 - TRANSFORMAÇÃO FHIR",
    "transformar_fhir.py"
)

# Etapa 3: Envio ao servidor HAPI FHIR
executar_etapa(
    "ETAPA 3 - ENVIO AO HAPI FHIR",
    "enviar_fhir.py"
)

print("\n=== PIPELINE ETL FHIR CONCLUÍDO COM SUCESSO! ===")
