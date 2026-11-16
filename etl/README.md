# Execução dos planos de carga (ETL) — DW_CANADA

Este diretório contém os planos ETL do **Pentaho Data Integration (PDI/Spoon)** que
carregam o Data Warehouse `DW_CANADA` (Oracle) a partir dos CSVs brutos. Os arquivos são
gerados por `tools/apoio_nao_avaliado/gerar_etl_pdi.py`.

## Arquivos

| Arquivo | Tipo | Função |
|---|---|---|
| `TR_STG_JOB_BANK.ktr` | Transformation | CSV Job Bank → `stg_job_bank_wages` |
| `TR_STG_IMIGRACAO.ktr` | Transformation | CSV imigração → `stg_statcan_imigracao` |
| `TR_STG_HABITACAO.ktr` | Transformation | CSV habitação → `stg_statcan_habitacao` |
| `TR_DIM_PROVINCIA.ktr` … `TR_DIM_FONTE.ktr` | Transformation | Staging → 10 dimensões |
| `TR_FATO_SALARIO.ktr`, `TR_FATO_IMIGRACAO.ktr`, `TR_FATO_HABITACAO.ktr` | Transformation | Dimensões + staging → 3 fatos |
| `JOB_CARGA_DW.kjb` | Job | Orquestra tudo na ordem staging → dimensões → fatos |

## Pré-requisitos

1. **Oracle** com o schema `DW_CANADA` criado — executar `sql/script_oracle.sql`
   (seção DBA + seção owner) antes da primeira carga.
2. **Pentaho Data Integration** 8.x/9.x (Spoon).
3. Os CSVs de origem presentes em `raw/` (o ZIP de imigração `98100307-eng.zip`, de
   ~383 MB, precisa ser baixado e extraído — ver `README.md` do projeto).

## Configurar a conexão (uma única vez)

A conexão nomeada **`DW_CANADA`** (Oracle, Native) é usada por todos os arquivos e recebe
os parâmetros por variáveis:

| Variável | Significado | Exemplo |
|---|---|---|
| `DW_HOST` | Host do Oracle | `localhost` |
| `DW_PORT` | Porta do listener | `1521` |
| `DW_SID` | SID ou service name | `ORCL` |
| `DW_USER` | Usuário (owner do schema) | `DW_CANADA` |

Defina-as em `~/.kettle/kettle.properties` (ou no `kettle.properties` da instalação do
PDI):

```properties
DW_HOST=localhost
DW_PORT=1521
DW_SID=ORCL
DW_USER=DW_CANADA
```

Depois, no Spoon, abra **um dos `.ktr`** → menu *Tools → Database → Explore* (ou clique
duplo em um passo de banco) → selecione `DW_CANADA` → digite a **senha** uma vez e
clique *Test*. O PDI mantém a conexão compartilhada durante a sessão.

> A senha não é gravada nos arquivos (fica em branco por segurança); informe-a no Spoon
> a cada sessão, ou use o repositório de conexões do PDI.

## Executar

**Forma 1 — pelo JOB (recomendada):** abra `JOB_CARGA_DW.kjb` no Spoon e clique ▶.
O job roda as 16 transformations na ordem correta e para se alguma falhar.

**Forma 2 — manual (para o vídeo, passo a passo):** execute as transformations na ordem:

1. `TR_STG_JOB_BANK`, `TR_STG_IMIGRACAO`, `TR_STG_HABITACAO`
2. `TR_DIM_PROVINCIA`, `TR_DIM_OCUPACAO`, `TR_DIM_TEMPO_SALARIO`,
   `TR_DIM_DISPONIBILIDADE_SALARIO`, `TR_DIM_TEMPO_CENSO`, `TR_DIM_PAIS_NASCIMENTO`,
   `TR_DIM_PERIODO_IMIGRACAO`, `TR_DIM_TENENCIA`, `TR_DIM_INDICADOR_HABITACAO`,
   `TR_DIM_FONTE`
3. `TR_FATO_SALARIO`, `TR_FATO_IMIGRACAO`, `TR_FATO_HABITACAO`

## Idempotência (recarga sem duplicar)

Todas as dimensões fazem **lookup pela chave natural** (`cd_*`) e usam `Insert/Update`;
as fatos usam a **PK composta** como chave de lookup. Executar o JOB mais de uma vez
(atualiza em vez de duplicar) mantém as contagens estáveis:

| Tabela | Contagem esperada |
|---|---|
| `dim_provincia` | 13 |
| `dim_ocupacao` | 1 |
| `dim_tempo_salario` | 1 |
| `dim_disponibilidade_salario` | 3 |
| `dim_tempo_censo` | 1 |
| `dim_pais_nascimento` | 2 |
| `dim_periodo_imigracao` | 5 |
| `dim_tenencia` | 4 |
| `dim_indicador_habitacao` | 9 |
| `dim_fonte` | 3 |
| `fato_salario` | 13 |
| `fato_imigracao` | 130 |
| `fato_habitacao` | 468 |

## Agendamento (produção)

Use o **Kitchen** (linha de comando do PDI) com um agendador do SO:

```bash
# Windows (Task Scheduler) / Linux (cron) — exemplo:
kitchen.sh -file="C:\caminho\etl\JOB_CARGA_DW.kjb" \
  -param:RAW_DIR=raw \
  -param:IMIGRACAO_CSV=raw/98100307_extracted/98100307.csv \
  -level=Basic -logfile="carga_dw.log"
```

## Observações

- **CSV com BOM e acentos:** os steps `CsvInput` usam encoding `UTF-8` e campos
  definidos por posição; o BOM e os caracteres acentuados do francês são preservados.
- **`stg_statcan_imigracao`** é a maior carga (tabela completa 98-10-0307-01); a
  transformação `TR_FATO_IMIGRACAO` filtra os 13 DGUIDs e as linhas de
  `Age/Gender = Total` antes do `UNPIVOT` dos períodos `[4]..[8]`.
- Os arquivos são **ponto de partida validável no Spoon**: revise as conexões e, se o
  ambiente usar identificadores em um case específico, ajuste os nomes de coluna.
