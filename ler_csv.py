
import csv
from pathlib import Path

# Localiza o arquivo CSV dentro da pasta data
caminho_csv = Path(__file__).parent / "data" / "patients.csv"

# Abre e lê os dados do arquivo
with open(caminho_csv, mode="r", encoding="cp1252", newline="") as arquivo:
    leitor = csv.DictReader(arquivo)

    print("COLUNAS DO CSV:")
    print(leitor.fieldnames)

    print("\nPRIMEIROS 5 PACIENTES:")
    for numero, paciente in enumerate(leitor, start=1):
        if numero > 5:
            break
        print(f"\nPaciente {numero}:")
        for campo, valor in paciente.items():
            print(f"{campo}: {valor}")
