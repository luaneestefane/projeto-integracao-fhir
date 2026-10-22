
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests

# Servidor HAPI FHIR no Docker
FHIR_URL = "http://localhost:8080/fhir"

# Pasta onde o backup será armazenado
pasta_projeto = Path(__file__).parent
pasta_backup = pasta_projeto / "backup"
pasta_backup.mkdir(exist_ok=True)

# Nome do arquivo com data e hora
data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
arquivo_backup = pasta_backup / f"pacientes_{data_hora}.json"

# Consulta inicial: até 50 pacientes por página
url = f"{FHIR_URL}/Patient"
parametros = {"_count": 50}

pacientes = []
paginas = 0
total_informado = None

try:
    while url:
        resposta = requests.get(
            url,
            params=parametros,
            headers={"Accept": "application/fhir+json"},
            timeout=30
        )
        resposta.raise_for_status()

        bundle = resposta.json()

        if bundle.get("resourceType") != "Bundle":
            raise ValueError("A resposta não é um Bundle FHIR.")

        if bundle.get("type") != "searchset":
            raise ValueError("A resposta não é um Bundle de pesquisa.")

        paginas += 1

        if total_informado is None:
            total_informado = bundle.get("total")

        # Recupera os recursos Patient
        for entrada in bundle.get("entry", []):
            recurso = entrada.get("resource", {})

            if recurso.get("resourceType") == "Patient":
                pacientes.append(recurso)

        # Procura a próxima página
        proxima_url = None

        for link in bundle.get("link", []):
            if link.get("relation") == "next":
                proxima_url = link.get("url")
                break

        # Segurança: não seguir links para outro servidor
        if proxima_url:
            origem = urlparse(FHIR_URL)
            destino = urlparse(proxima_url)

            if (
                destino.scheme != origem.scheme
                or destino.netloc != origem.netloc
                or not destino.path.startswith("/fhir/")
            ):
                raise ValueError("Link de paginação inesperado.")

        url = proxima_url
        parametros = None

    # Confere a quantidade antes de salvar
    if total_informado is not None and len(pacientes) != total_informado:
        raise ValueError(
            f"Consulta incompleta: esperados {total_informado}, "
            f"recuperados {len(pacientes)}."
        )

    # Salva somente após recuperar todas as páginas
    with open(arquivo_backup, "w", encoding="utf-8") as arquivo:
        json.dump(
            pacientes,
            arquivo,
            ensure_ascii=False,
            indent=2
        )

    print("BACKUP CONCLUÍDO!")
    print(f"Páginas consultadas: {paginas}")
    print(f"Pacientes recuperados: {len(pacientes)}")
    print(f"Arquivo salvo: {arquivo_backup}")

except (requests.exceptions.RequestException, ValueError, OSError) as erro:
    print(f"ERRO NO BACKUP: {erro}")
    print("Nenhum backup completo foi confirmado.")
