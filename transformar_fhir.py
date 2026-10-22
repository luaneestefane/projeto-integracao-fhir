
import json
from pathlib import Path
from datetime import datetime

# Localização dos arquivos
pasta_projeto = Path(__file__).parent
pasta_saida = pasta_projeto / "output"
arquivo_validos = pasta_saida / "pacientes_validos.json"
arquivo_saida = pasta_saida / "patients_fhir.json"

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
    return datetime.strptime(
        data.strip(), "%d/%m/%Y"
    ).strftime("%Y-%m-%d")


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


# Verifica se a validação foi executada
if not arquivo_validos.exists():
    raise SystemExit(
        "ERRO: pacientes_validos.json não encontrado. "
        "Execute primeiro: python validar_dados.py"
    )

# Carrega somente os registros aprovados
with open(arquivo_validos, "r", encoding="utf-8") as arquivo:
    dados_validos = json.load(arquivo)

pacientes = []
erros = []

# Transforma os registros aprovados em recursos FHIR
for numero, dados in enumerate(dados_validos, start=1):
    try:
        paciente = criar_patient(dados)
        pacientes.append(paciente)
    except (ValueError, KeyError, AttributeError) as erro:
        erros.append({
            "registro": numero,
            "erro": str(erro)
        })

# Salva os recursos FHIR
with open(arquivo_saida, "w", encoding="utf-8") as arquivo:
    json.dump(pacientes, arquivo, ensure_ascii=False, indent=2)

print("TRANSFORMAÇÃO CONCLUÍDA!")
print(f"Pacientes aprovados na validação: {len(dados_validos)}")
print(f"Pacientes transformados: {len(pacientes)}")
print(f"Registros com erro na transformação: {len(erros)}")
print(f"Arquivo gerado: {arquivo_saida}")

if erros:
    print("\nERROS ENCONTRADOS:")
    for erro in erros:
        print(f"Registro {erro['registro']}: {erro['erro']}")
