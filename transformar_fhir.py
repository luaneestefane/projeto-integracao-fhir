
import csv
import json
from pathlib import Path
from datetime import datetime

# Localização dos arquivos
pasta_projeto = Path(__file__).parent
arquivo_csv = pasta_projeto / "data" / "patients.csv"
pasta_saida = pasta_projeto / "output"

# Cria a pasta de saída, caso não exista
pasta_saida.mkdir(exist_ok=True)


def converter_genero(genero):
    generos = {
        "masculino": "male",
        "feminino": "female",
        "outro": "other",
        "desconhecido": "unknown"
    }
    return generos.get(genero.strip().lower(), "unknown")


def converter_data(data):
    return datetime.strptime(data.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")


def criar_patient(dados):
    nome = dados["Nome"].strip()
    cpf = dados["CPF"].strip()
    telefone = dados["Telefone"].strip()

    patient = {
        "resourceType": "Patient",
        "identifier": [
            {
                "system": "https://saude.gov.br/fhir/r4/identifier/cpf",
                "value": cpf
            }
        ],
        "name": [
            {
                "use": "official",
                "text": nome
            }
        ],
        "gender": converter_genero(dados["Gênero"]),
        "birthDate": converter_data(dados["Data de Nascimento"])
    }

    if telefone:
        patient["telecom"] = [
            {
                "system": "phone",
                "value": telefone
            }
        ]

    return patient


# Lê o CSV e transforma cada registro em Patient
pacientes = []
erros = []

with open(arquivo_csv, encoding="cp1252", newline="") as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha, dados in enumerate(leitor, start=2):
        try:
            paciente = criar_patient(dados)
            pacientes.append(paciente)
        except (ValueError, KeyError, AttributeError) as erro:
            erros.append({
                "linha": linha,
                "erro": str(erro)
            })

# Salva os recursos FHIR em JSON
arquivo_saida = pasta_saida / "patients_fhir.json"

with open(arquivo_saida, "w", encoding="utf-8") as arquivo:
    json.dump(pacientes, arquivo, ensure_ascii=False, indent=2)

print("TRANSFORMAÇÃO CONCLUÍDA!")
print(f"Pacientes transformados: {len(pacientes)}")
print(f"Registros com erro: {len(erros)}")
print(f"Arquivo gerado: {arquivo_saida}")

if erros:
    print("\nERROS ENCONTRADOS:")
    for erro in erros:
        print(f"Linha {erro['linha']}: {erro['erro']}")
