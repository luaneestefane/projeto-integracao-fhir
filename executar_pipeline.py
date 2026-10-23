
import subprocess
import sys
from pathlib import Path
from registrar_log import registrar_log

# Pasta principal do projeto
PASTA_PROJETO = Path(__file__).resolve().parent


def executar_etapa(nome, arquivo):
    print(f"\n=== {nome} ===", flush=True)

    registrar_log(f"Iniciando: {nome}")

    resultado = subprocess.run(
        [sys.executable, str(PASTA_PROJETO / arquivo)],
        cwd=PASTA_PROJETO
    )

    if resultado.returncode != 0:
        mensagem = f"Falha na etapa: {nome}"

        print(f"\nERRO: {mensagem}")
        print("Pipeline interrompido.")

        registrar_log(mensagem, "ERRO")
        sys.exit(resultado.returncode)

    registrar_log(f"Concluída: {nome}")


print("=== INICIANDO PIPELINE ETL FHIR ===", flush=True)
registrar_log("Pipeline ETL FHIR iniciado")

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

# Etapa 3: Envio ao HAPI FHIR
executar_etapa(
    "ETAPA 3 - ENVIO AO HAPI FHIR",
    "enviar_fhir.py"
)

registrar_log("Pipeline ETL FHIR concluído com sucesso")

print("\n=== PIPELINE ETL FHIR CONCLUÍDO COM SUCESSO! ===")
