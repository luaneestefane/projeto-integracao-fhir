
import json
import sys
from pathlib import Path

import requests

FHIR_URL = "http://localhost:8081/fhir"
ARQUIVO = Path(__file__).resolve().parent / "output" / "patients_fhir.json"

with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
    pacientes = json.load(arquivo)

erros = 0

for numero, paciente in enumerate(pacientes, start=1):
    try:
        resposta = requests.post(
            f"{FHIR_URL}/Patient/$validate",
            json=paciente,
            headers={
                "Content-Type": "application/fhir+json",
                "Accept": "application/fhir+json"
            },
            timeout=30
        )

        resposta.raise_for_status()
        resultado = resposta.json()

        problemas = [
            item for item in resultado.get("issue", [])
            if item.get("severity") in ("error", "fatal")
        ]

        if problemas:
            erros += 1
            print(f"Paciente {numero}: INVÁLIDO")
            for problema in problemas:
                print(problema.get("diagnostics", problema.get("code")))
        else:
            print(f"Paciente {numero}: sem erros de validação")

    except (requests.RequestException, ValueError) as erro:
        print(f"Falha ao validar paciente {numero}: {erro}")
        sys.exit(1)

print(f"\nPacientes analisados: {len(pacientes)}")
print(f"Pacientes com erros: {erros}")

if erros:
    sys.exit(1)

print("VALIDAÇÃO FHIR CONCLUÍDA!")
