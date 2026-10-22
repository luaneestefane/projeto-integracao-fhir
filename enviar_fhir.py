
import json
import sys
import requests
from pathlib import Path
from urllib.parse import quote

# Configuração do servidor FHIR local
FHIR_URL = "http://localhost:8081/fhir"

# Localiza o arquivo JSON gerado na transformação
pasta_projeto = Path(__file__).parent
arquivo_json = pasta_projeto / "output" / "patients_fhir.json"

# Carrega os pacientes transformados
with open(arquivo_json, "r", encoding="utf-8") as arquivo:
    pacientes = json.load(arquivo)

# Monta um Bundle FHIR do tipo transaction
bundle = {
    "resourceType": "Bundle",
    "type": "transaction",
    "entry": []
}

for paciente in pacientes:
    identificador = paciente["identifier"][0]
    sistema = identificador["system"]
    valor = identificador["value"]

    # Evita criar outro paciente quando já existe
    # exatamente um com o mesmo identificador
    parametro = quote(f"{sistema}|{valor}", safe="")

    bundle["entry"].append({
        "resource": paciente,
        "request": {
            "method": "POST",
            "url": "Patient",
            "ifNoneExist": f"identifier={parametro}"
        }
    })

print(f"Pacientes preparados para envio: {len(pacientes)}")

# Não envia transação vazia
if not pacientes:
    print("Nenhum paciente válido para enviar.")
    sys.exit(0)

print("Enviando transação ao HAPI FHIR local...")

try:
    resposta = requests.post(
        FHIR_URL,
        json=bundle,
        headers={
            "Accept": "application/fhir+json",
            "Content-Type": "application/fhir+json"
        },
        timeout=120
    )

    print(f"\nHTTP Status: {resposta.status_code}")

    if not resposta.ok:
        print("ERRO: O servidor rejeitou a transação.")
        print(resposta.text[:3000])
        sys.exit(1)

    resultado = resposta.json()

    if resultado.get("resourceType") != "Bundle":
        print("ERRO: Resposta inesperada do servidor.")
        sys.exit(1)

    print("Transação processada com sucesso!")

    for numero, entrada in enumerate(
        resultado.get("entry", []), start=1
    ):
        status = entrada.get("response", {}).get("status", "")
        print(f"Paciente {numero}: {status}")

except requests.exceptions.RequestException as erro:
    print(f"ERRO de comunicação com o servidor: {erro}")
    sys.exit(1)

except (ValueError, KeyError, TypeError) as erro:
    print(f"ERRO ao processar a resposta FHIR: {erro}")
    sys.exit(1)
