# Documentação dos Planos ETL — DW_CANADA (Entrega 2)

Documentação dos planos de carga do Data Warehouse `DW_CANADA` implementados no **Pentaho
Data Integration (PDI/Spoon)**. Os arquivos (`etl/*.ktr`, `etl/JOB_CARGA_DW.kjb`) são
gerados por `tools/apoio_nao_avaliado/gerar_etl_pdi.py`; as orientações de execução estão
em `etl/README.md`.

## 1. Visão geral do pipeline

O ETL segue o fluxo clássico **Extract → Transform → Load** em três camadas:

```
raw (CSV bruto) ──► staging (stg_*) ──► dimensões (dim_*) ──► fatos (fato_*)
```

1. **Staging** (3 transformations): espelha os CSVs brutos em tabelas `stg_*` sem alterar
   os arquivos de origem.
2. **Dimensões** (10 transformations): extraem as chaves naturais do staging e gravam em
   `dim_*` por *lookup* + `Insert/Update` (idempotentes).
3. **Fatos** (3 transformations): cruzam staging com as dimensões (lookup das surrogate
   keys) e gravam por `Insert/Update` usando a **PK composta** como chave.
4. **Job** (`JOB_CARGA_DW.kjb`): orquestra as 16 transformations na ordem correta.

## 2. Conexão e variáveis

Todos os planos usam a conexão nomeada **`DW_CANADA`** (Oracle, Native). Parâmetros por
variável (`~/.kettle/kettle.properties`): `DW_HOST`, `DW_PORT`, `DW_SID`, `DW_USER`;
a senha é informada no Spoon (não fica gravada nos arquivos).

| Variável | Significado |
|---|---|
| `DW_HOST` | Host do Oracle |
| `DW_PORT` | Porta do listener |
| `DW_SID` | SID / service name |
| `DW_USER` | Owner do schema (`DW_CANADA`) |
| `RAW_DIR` | Diretório com os CSVs brutos (padrão `raw`) |
| `IMIGRACAO_CSV` | Caminho do CSV extraído do ZIP de imigração |

## 3. Staging

| Plan | Origem → Destino | Passos |
|---|---|---|
| `TR_STG_JOB_BANK` | `raw/job_bank_wages_2025.csv` (44.376 × 22) → `stg_job_bank_wages` | `CsvInput` → `TableOutput` |
| `TR_STG_IMIGRACAO` | extração 98-10-0307-01 (tabela completa) → `stg_statcan_imigracao` | `CsvInput` → `TableOutput` |
| `TR_STG_HABITACAO` | `raw/98100258_extracted/98100258.csv` (2.990 × 14) → `stg_statcan_habitacao` | `CsvInput` → `TableOutput` |

Os steps `CsvInput` usam encoding `UTF-8`, campos definidos **por posição** (toleram BOM
e acentos do francês) e `newline_possible=Y` (campos com quebra de linha entre aspas).

## 4. Dimensões

Todas seguem o mesmo padrão: `TableInput` (extrai as chaves naturais com SQL) →
`InsertUpdate` (lookup pela chave natural; insere se não existe, atualiza se existe).
A surrogate key `sk_*` é atribuída pelo gatilho `TRG_DIM_*` no banco — não entra nos campos
do passo.

| Plan | Chave natural (lookup) | Atributos gravados | Fonte / regra |
|---|---|---|---|
| `TR_DIM_PROVINCIA` | `cd_dguid` | `nm_provincia`, `sg_provincia_jobbank`, `nm_pais` | 13 DGUIDs canônicos do staging de imigração; sigla do Job Bank mapeada por DGUID (`PEI`, `YK`, `NWT`, `NU` incluídos) |
| `TR_DIM_OCUPACAO` | `cd_noc` | `nm_ocupacao_en`, `nm_ocupacao_fr` | `stg_job_bank_wages` filtrado `noc_cnp = 'NOC_21232'` |
| `TR_DIM_TEMPO_SALARIO` | `cd_periodo_referencia` | `nr_ano_inicio`, `nr_ano_fim`, `ds_periodo` | `reference_period = '2023-2024'` |
| `TR_DIM_DISPONIBILIDADE_SALARIO` | `cd_disponibilidade` | `ds_disponibilidade`, `fl_comparavel_provincial` | 3 categorias fixas (`PROVINCIAL_PUBLICADO`, `APENAS_REGIONAL`, `INDISPONIVEL`) |
| `TR_DIM_TEMPO_CENSO` | `nr_ano_censo` | `dt_referencia` | 1 registro fixo (2021) |
| `TR_DIM_PAIS_NASCIMENTO` | `cd_pais_nascimento` | `nm_pais_nascimento` | `Brazil` e `Total – Place of birth` do staging de imigração |
| `TR_DIM_PERIODO_IMIGRACAO` | `cd_periodo_imigracao` | `ds_periodo_imigracao`, `nr_ordem` | 5 períodos fixos `[4]..[8]` |
| `TR_DIM_TENENCIA` | `cd_tenencia` | `ds_tenencia` | 4 posses fixas (`TOTAL`, `OWNER`, `RENTER`, `GOV`) |
| `TR_DIM_INDICADOR_HABITACAO` | `cd_indicador_habitacao` | `ds_indicador_habitacao`, `tp_medida` | 9 indicadores do staging; `tp_medida = PERCENTUAL` para `Percent…`, senão `CONTAGEM` |
| `TR_DIM_FONTE` | `cd_fonte` | `nm_fonte`, `ds_url`, `dt_extracao`, `ds_checksum` | 3 fontes institucionais (`JOB_BANK_2025`, `STATCAN_0307`, `STATCAN_0258`) |

## 5. Fatos

Cada fato segue: `TableInput` (SQL que cruza staging + dimensões e normaliza o grão) →
5× `DBLookup` (resolve as surrogate keys) → `InsertUpdate` (lookup pela PK composta).

### 5.1 `TR_FATO_SALARIO` — 13 registros

**Grão:** jurisdição + ocupação + período salarial.

- SQL dirige a carga por `dim_provincia` (13 linhas) e faz `LEFT JOIN` no
  `stg_job_bank_wages` para `NOC 21232`, período `2023-2024`.
- Classificação de cobertura: `PROVINCIAL_PUBLICADO` (9 províncias, `ER` de 2 dígitos),
  `APENAS_REGIONAL` (PEI — `ER1110`, com `cd_regiao_origem`/`nm_regiao_origem`),
  `INDISPONIVEL` (YK, NWT, NU — valores salariais `NULL`).
- `vl_amplitude_salarial = high − low` (derivada); `fl_salario_anual` mapeado do flag.
- Lookups: `dim_provincia` (`cd_dguid`), `dim_ocupacao` (`cd_noc`),
  `dim_tempo_salario` (`cd_periodo_referencia`), `dim_disponibilidade_salario`
  (`cd_disponibilidade`), `dim_fonte` (`cd_fonte`).
- PK de lookup: `(sk_provincia, sk_ocupacao, sk_tempo_salario)`.

### 5.2 `TR_FATO_IMIGRACAO` — 130 registros

**Grão:** província + país de nascimento + período de imigração + Censo.

- SQL faz `UNPIVOT` das colunas de período `[4]..[8]` do `stg_statcan_imigracao` em linhas
  (13 províncias × 2 países × 5 períodos = 130).
- Filtros: `dguid IN (dim_provincia)`, `Age/Gender = Total`, país ∈ {`Brazil`, `Total`}.
- Lookups: `dim_provincia`, `dim_pais_nascimento`, `dim_periodo_imigracao`,
  `dim_tempo_censo` (`nr_ano_censo`), `dim_fonte`.
- PK de lookup: `(sk_provincia, sk_pais_nascimento, sk_periodo_imigracao, sk_tempo_censo)`.

### 5.3 `TR_FATO_HABITACAO` — 468 registros

**Grão:** província + posse + indicador habitacional + Censo.

- SQL faz `UNPIVOT` das 4 colunas de posse do `stg_statcan_habitacao` em linhas
  (13 províncias × 4 posses × 9 indicadores = 468).
- Filtros: `dguid IN (dim_provincia)`, `census_year_2 = '2021'`.
- Lookups: `dim_provincia`, `dim_tenencia`, `dim_indicador_habitacao`,
  `dim_tempo_censo`, `dim_fonte`.
- PK de lookup: `(sk_provincia, sk_tenencia, sk_indicador_habitacao, sk_tempo_censo)`.

## 6. Job — `JOB_CARGA_DW.kjb`

Encadeia, **em sequência** (cada passo aguarda o anterior terminar), na ordem:

```
START
 └─ TR_STG_JOB_BANK → TR_STG_IMIGRACAO → TR_STG_HABITACAO
 └─ TR_DIM_PROVINCIA → … → TR_DIM_FONTE (10 dimensões)
 └─ TR_FATO_SALARIO → TR_FATO_IMIGRACAO → TR_FATO_HABITACAO
 └─ SUCCESS
```

A ordem garante: staging antes das dimensões; dimensões antes dos fatos (os lookups de SK
exigem as dimensões carregadas).

## 7. Idempotência e recarga

- **Dimensões:** lookup pela chave natural (`cd_*`) — reexecutar **atualiza** a linha em vez
  de duplicar.
- **Fatos:** lookup pela **PK composta** — reexecutar atualiza as medidas sem criar
  duplicatas (a própria PK/constraint impede a duplicação).
- **Resultado:** executar o JOB N vezes mantém as contagens estáveis (ver tabela abaixo),
  comportamento exigido para agendamento diário/semanal.

| Tabela | Contagem esperada |
|---|---|
| `stg_job_bank_wages` | 44.376 |
| `stg_statcan_habitacao` | 2.990 |
| `stg_statcan_imigracao` | conforme a extração completa |
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

## 8. Mapeamento origem → destino (resumo)

| Origem | Destino | Regra |
|---|---|---|
| Job Bank `prov`/`ER_Code`/`ER_Name` | `dim_provincia`, `dim_disponibilidade_salario`, `fato_salario` | 9 provinciais + PEI regional (`ER1110`) + 3 territórios indisponíveis |
| Job Bank `NOC_CNP` | `dim_ocupacao` | filtrar `NOC_21232` |
| Job Bank `Low/Median/High…`, `Reference_Period` | `fato_salario` | `2023-2024`; nunca estimar vazios |
| StatCan `DGUID`/`GEO` | `dim_provincia` | 13 DGUIDs canônicos |
| StatCan `Place of birth`, períodos `[4]..[8]` | `fato_imigracao`, `dim_pais_nascimento`, `dim_periodo_imigracao` | `Brazil`/`Total`, totais de idade/gênero |
| StatCan `Housing indicators`, `Tenure (4)` | `fato_habitacao`, `dim_indicador_habitacao`, `dim_tenencia` | 13 províncias, Censo 2021 |

## 9. Referência cruzada com os arquivos

| Documento | Conteúdo |
|---|---|
| `etl/README.md` | Pré-requisitos, conexão, execução (Spoon e Kitchen), agendamento |
| `docs/roteiro_video_cargas.md` | Roteiro do vídeo (Parte 1): tabelas vazias, logs, contagens, sem duplicatas, recarga |
| `tools/apoio_nao_avaliado/gerar_etl_pdi.py` | Gerador reproduzível dos `.ktr`/`.kjb` |
| `sql/script_oracle.sql` | DDL do DW (tablespaces, staging, dimensões, fatos, gatilhos de SK) |
