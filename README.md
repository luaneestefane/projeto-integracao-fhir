# Projeto de Integração de Dados de Saúde com HL7 FHIR R4

Pipeline de integração de dados de saúde desenvolvido com Python, Docker, HAPI FHIR e PostgreSQL, utilizando o padrão HL7 FHIR R4.

## Objetivo

Simular um processo de integração de dados de pacientes, desde a extração de informações de um arquivo CSV até o armazenamento em um servidor FHIR com banco de dados persistente.

O projeto tem finalidade educacional e utiliza dados fictícios.

## Tecnologias utilizadas

- **Python:** extração, transformação e envio dos dados.
- **HL7 FHIR R4:** padronização dos dados de saúde.
- **API REST:** comunicação com o servidor FHIR.
- **HAPI FHIR:** servidor responsável pelo processamento dos recursos.
- **Docker:** execução dos serviços em contêineres.
- **Docker Compose:** configuração e gerenciamento dos serviços.
- **PostgreSQL:** armazenamento dos dados.
- **Docker Volume:** persistência do banco de dados.
- **Git e GitHub:** versionamento e publicação do código.
- **VS Code:** ambiente de desenvolvimento.

## Arquitetura do projeto

```text
ARQUIVO CSV
    |
    v
PYTHON - EXTRACT
Leitura dos pacientes
    |
    v
PYTHON - TRANSFORM
Mapeamento para Patient FHIR R4
    |
    v
JSON FHIR
    |
    v
BUNDLE FHIR - TRANSACTION
    |
    v
API REST - POST
    |
    v
HAPI FHIR - DOCKER
    |
    v
POSTGRESQL
    |
    v
DOCKER VOLUME
```

## Etapas do pipeline ETL

### 1. Extract — Extração

O script `ler_csv.py` realiza a leitura dos registros do arquivo CSV.

### 2. Transform — Transformação

O script `transformar_fhir.py` converte os dados para recursos `Patient`, seguindo a estrutura HL7 FHIR R4.

Exemplos de mapeamento:

| Campo CSV | Elemento FHIR |
|---|---|
| Nome | Patient.name |
| CPF fictício | Patient.identifier |
| Gênero | Patient.gender |
| Data de nascimento | Patient.birthDate |
| Telefone | Patient.telecom |

### 3. Load — Carregamento

O script `enviar_fhir.py` organiza os recursos em um `Bundle` do tipo `transaction` e realiza o envio ao servidor HAPI FHIR pela API REST.

O envio utiliza criação condicional para reduzir o risco de duplicação de pacientes pelo identificador.

## Infraestrutura Docker

O ambiente utiliza dois serviços principais:

- **HAPI FHIR:** disponibiliza a API FHIR R4.
- **PostgreSQL:** armazena os recursos cadastrados.

O Docker Compose gerencia os serviços e configura um volume para persistência dos dados do PostgreSQL.

O servidor FHIR é disponibilizado localmente em:

`http://localhost:8081/fhir`

## Backup

O script `backup_fhir.py` consulta os pacientes cadastrados no HAPI FHIR e exporta seus recursos em formato JSON.

Os arquivos de backup são mantidos localmente e não são publicados no repositório.

## Resultados obtidos

- 50 registros de pacientes processados.
- 50 recursos `Patient` gerados em JSON FHIR.
- Envio dos pacientes por meio de um `Bundle` transacional.
- Cadastro dos pacientes no servidor HAPI FHIR.
- Integração com PostgreSQL.
- Persistência dos dados confirmada após reinicialização do servidor HAPI FHIR.
- Consulta e exportação dos pacientes pela API REST.

## Organização dos arquivos

```text
projeto-integracao-fhir/
|
|-- ler_csv.py
|-- transformar_fhir.py
|-- enviar_fhir.py
|-- backup_fhir.py
|-- docker-compose.yml
|-- .gitignore
|-- README.md
|
|-- .env/arquivo local (não versionado)
|-- data/        (não versionada)
|-- output/      (não versionada)
|-- backup/      (não versionada)
```

## Segurança e privacidade

O projeto utiliza dados fictícios para fins de aprendizado.

Os arquivos CSV, JSON, backups e variáveis de ambiente são excluídos do versionamento por meio do `.gitignore`.

O ambiente foi desenvolvido para execução local e não deve ser utilizado em produção sem configurações adicionais de segurança, gerenciamento de credenciais e proteção de dados.

## Próximas evoluções

- Validação de recursos FHIR.
- Tratamento e registro de inconsistências.
- Implementação de regras de qualidade de dados.
- Integração com perfis e Guias de Implementação FHIR.
- Automatização do pipeline ETL.

---

**Projeto educacional voltado ao estudo de interoperabilidade em saúde, integração de sistemas e HL7 FHIR R4.**