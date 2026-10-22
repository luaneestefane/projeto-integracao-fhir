
import csv
import json
from pathlib import Path
from datetime import datetime

ARQUIVO_CSV = Path("data/patients.csv")
PASTA_SAIDA = Path("output")

PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

pacientes_validos = []
pacientes_invalidos = []
inconsistencias = []
cpfs_encontrados = set()

with open(ARQUIVO_CSV, "r", encoding="cp1252", newline="") as arquivo:
    leitor = csv.DictReader(arquivo)

    for numero_linha, paciente in enumerate(leitor, start=2):
        erros = []

        nome = (paciente.get("Nome") or "").strip()
        cpf = (paciente.get("CPF") or "").strip()
        genero = (paciente.get("Gênero") or "").strip()
        nascimento = (paciente.get("Data de Nascimento") or "").strip()

        if not nome:
            erros.append("Nome obrigatório não informado")

        cpf_normalizado = "".join(c for c in cpf if c.isdigit())

        if not cpf:
            erros.append("CPF não informado")
        elif len(cpf_normalizado) != 11:
            erros.append("CPF deve conter 11 dígitos")
        elif cpf_normalizado in cpfs_encontrados:
            erros.append("CPF duplicado")

        if cpf_normalizado and len(cpf_normalizado) == 11:
            cpfs_encontrados.add(cpf_normalizado)

        if genero.lower() not in (
            "masculino", "feminino", "outro", "desconhecido"
        ):
            erros.append("Gênero não reconhecido")

        try:
            datetime.strptime(nascimento, "%d/%m/%Y")
        except ValueError:
            erros.append("Data de nascimento inválida")

        if erros:
            pacientes_invalidos.append(paciente)

            inconsistencias.append({
                "linha": numero_linha,
                "nome": nome,
                "cpf": cpf,
                "erros": erros
            })
        else:
            pacientes_validos.append(paciente)


def salvar_json(nome_arquivo, dados):
    caminho = PASTA_SAIDA / nome_arquivo

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


salvar_json("pacientes_validos.json", pacientes_validos)
salvar_json("pacientes_invalidos.json", pacientes_invalidos)
salvar_json("inconsistencias.json", inconsistencias)

print("=== RESULTADO DA VALIDAÇÃO ===")
print(f"Total de registros: {len(pacientes_validos) + len(pacientes_invalidos)}")
print(f"Pacientes válidos: {len(pacientes_validos)}")
print(f"Pacientes inválidos: {len(pacientes_invalidos)}")
print(f"Inconsistências: {len(inconsistencias)}")
print("Arquivos gerados na pasta output/")
