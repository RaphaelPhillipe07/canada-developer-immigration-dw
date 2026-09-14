# Dicionário de Dados do Data Warehouse

Nomenclatura adotada (conforme aula de SQL Data Modeler): `PK_` (primary key), `FK_` (foreign key), `AK_` (alternate/unique key), `CK_` (check), `NN_` (not null), `IDX_` (índice), `SEQ_` (sequence). Todas as dimensões usam surrogate key `NUMBER` gerada por sequência.

## 1. Dimensões

### 1.1 `dim_provincia`

| Campo | Tipo | Tamanho | Constraint | Descrição / Origem |
|---|---|---|---|---|
| `sk_provincia` | NUMBER | 10 | `PK_DIM_PROVINCIA` | Surrogate key (SEQ_DIM_PROVINCIA) |
| `cd_dguid` | VARCHAR2 | 16 | `AK_DIM_PROVINCIA`, `NN_DIM_PROVINCIA_CD_DGUID` | DGUID do StatCan (ex.: `2021A000235`) |
| `nm_provincia` | VARCHAR2 | 60 | `NN_DIM_PROVINCIA_NM` | Nome em inglês (ex.: `Ontario`) |
| `sg_provincia_jobbank` | VARCHAR2 | 4 | — | Sigla do Job Bank (`ON`); `NULL` quando não houver |
| `nm_pais` | VARCHAR2 | 20 | — | Sempre `Canada` |

### 1.2 `dim_ocupacao`

| Campo | Tipo | Tamanho | Constraint | Descrição / Origem |
|---|---|---|---|---|
| `sk_ocupacao` | NUMBER | 10 | `PK_DIM_OCUPACAO` | Surrogate key (SEQ_DIM_OCUPACAO) |
| `cd_noc` | VARCHAR2 | 12 | `AK_DIM_OCUPACAO`, `NN_DIM_OCUPACAO_CD_NOC` | Código NOC (ex.: `NOC_21232`) |
| `nm_ocupacao_en` | VARCHAR2 | 120 | `NN_DIM_OCUPACAO_NM_EN` | Título em inglês |
| `nm_ocupacao_fr` | VARCHAR2 | 120 | — | Título em francês |

### 1.3 `dim_tempo_salario`

| Campo | Tipo | Tamanho | Constraint | Descrição / Origem |
|---|---|---|---|---|
| `sk_tempo_salario` | NUMBER | 10 | `PK_DIM_TEMPO_SALARIO` | Surrogate key (SEQ_DIM_TEMPO_SALARIO) |
| `cd_periodo_referencia` | VARCHAR2 | 20 | `AK_DIM_TEMPO_SALARIO`, `NN_DIM_TEMPO_SALARIO_CD` | Período do Job Bank (ex.: `2023-2024`) |
| `nr_ano_inicio` | NUMBER | 4 | — | 2023 |
| `nr_ano_fim` | NUMBER | 4 | — | 2024 |
| `ds_periodo` | VARCHAR2 | 50 | — | Descrição legível |

### 1.4 `dim_tempo_censo`

| Campo | Tipo | Tamanho | Constraint | Descrição / Origem |
|---|---|---|---|---|
| `sk_tempo_censo` | NUMBER | 10 | `PK_DIM_TEMPO_CENSO` | Surrogate key (SEQ_DIM_TEMPO_CENSO) |
| `nr_ano_censo` | NUMBER | 4 | `AK_DIM_TEMPO_CENSO`, `NN_DIM_TEMPO_CENSO_ANO` | 2021 |
| `dt_referencia` | DATE | — | — | 15/05/2021 (referência do Censo) |

### 1.5 `dim_pais_nascimento`

| Campo | Tipo | Tamanho | Constraint | Descrição / Origem |
|---|---|---|---|---|
| `sk_pais_nascimento` | NUMBER | 10 | `PK_DIM_PAIS_NASCIMENTO` | Surrogate key (SEQ_DIM_PAIS_NASCIMENTO) |
| `cd_pais_nascimento` | VARCHAR2 | 30 | `AK_DIM_PAIS_NASCIMENTO`, `NN_DIM_PAIS_NASCIMENTO_CD` | `BRA` ou `TOTAL` |
| `nm_pais_nascimento` | VARCHAR2 | 80 | `NN_DIM_PAIS_NASCIMENTO_NM` | `Brazil` ou `Total – Place of birth` |

### 1.6 `dim_periodo_imigracao`

| Campo | Tipo | Tamanho | Constraint | Descrição / Origem |
|---|---|---|---|---|
| `sk_periodo_imigracao` | NUMBER | 10 | `PK_DIM_PERIODO_IMIGRACAO` | Surrogate key (SEQ_DIM_PERIODO_IMIGRACAO) |
| `cd_periodo_imigracao` | VARCHAR2 | 20 | `AK_DIM_PERIODO_IMIGRACAO`, `NN_DIM_PERIODO_IMIGRACAO_CD` | `[4]` … `[8]` |
| `ds_periodo_imigracao` | VARCHAR2 | 40 | `NN_DIM_PERIODO_IMIGRACAO_DS` | `Before 1980`, `1980 to 1990`, … |
| `nr_ordem` | NUMBER | 2 | — | Ordem cronológica p/ eixo do gráfico |

### 1.7 `dim_tenencia`

| Campo | Tipo | Tamanho | Constraint | Descrição / Origem |
|---|---|---|---|---|
| `sk_tenencia` | NUMBER | 10 | `PK_DIM_TENENCIA` | Surrogate key (SEQ_DIM_TENENCIA) |
| `cd_tenencia` | VARCHAR2 | 10 | `AK_DIM_TENENCIA`, `NN_DIM_TENENCIA_CD` | `TOTAL`, `OWNER`, `RENTER`, `GOV` |
| `ds_tenencia` | VARCHAR2 | 60 | `NN_DIM_TENENCIA_DS` | Descrição da posse |

### 1.8 `dim_indicador_habitacao`

| Campo | Tipo | Tamanho | Constraint | Descrição / Origem |
|---|---|---|---|---|
| `sk_indicador_habitacao` | NUMBER | 10 | `PK_DIM_INDICADOR_HABITACAO` | Surrogate key (SEQ_DIM_INDICADOR_HABITACAO) |
| `cd_indicador_habitacao` | VARCHAR2 | 60 | `AK_DIM_INDICADOR_HABITACAO`, `NN_DIM_INDICADOR_HABITACAO_CD` | Texto original do StatCan (ex.: `Percent of households in unaffordable housing`) |
| `ds_indicador_habitacao` | VARCHAR2 | 120 | — | Descrição resumida |
| `tp_medida` | VARCHAR2 | 10 | `CK_DIM_INDICADOR_HABITACAO_TP` (`CONTAGEM`/`PERCENTUAL`) | Tipo de medida |

### 1.9 `dim_fonte`

| Campo | Tipo | Tamanho | Constraint | Descrição / Origem |
|---|---|---|---|---|
| `sk_fonte` | NUMBER | 10 | `PK_DIM_FONTE` | Surrogate key (SEQ_DIM_FONTE) |
| `cd_fonte` | VARCHAR2 | 20 | `AK_DIM_FONTE`, `NN_DIM_FONTE_CD` | `JOB_BANK_2025`, `STATCAN_0307`, `STATCAN_0258` |
| `nm_fonte` | VARCHAR2 | 120 | `NN_DIM_FONTE_NM` | Nome oficial da fonte |
| `ds_url` | VARCHAR2 | 500 | — | URL do download |
| `dt_extracao` | DATE | — | — | Data de extração |
| `ds_checksum` | VARCHAR2 | 128 | — | SHA-256 do arquivo bruto |

## 2. Fatos

### 2.1 `fato_salario`

**Grão:** província + ocupação + período salarial.

| Campo | Tipo | Tamanho | Constraint | Descrição / Origem |
|---|---|---|---|---|
| `sk_fato_salario` | NUMBER | 15 | `PK_FATO_SALARIO` | Surrogate key (SEQ_FATO_SALARIO) |
| `sk_provincia` | NUMBER | 10 | `FK_FATO_SAL_DIM_PROVINCIA` | → `dim_provincia` |
| `sk_ocupacao` | NUMBER | 10 | `FK_FATO_SAL_DIM_OCUPACAO` | → `dim_ocupacao` |
| `sk_tempo_salario` | NUMBER | 10 | `FK_FATO_SAL_DIM_TEMPO_SAL` | → `dim_tempo_salario` |
| `sk_fonte` | NUMBER | 10 | `FK_FATO_SAL_DIM_FONTE` | → `dim_fonte` |
| `vl_salario_minimo` | NUMBER | 10,2 | — | `Low_Wage` (CAD/hora) |
| `vl_salario_mediano` | NUMBER | 10,2 | — | `Median_Wage` (CAD/hora) |
| `vl_salario_maximo` | NUMBER | 10,2 | — | `High_Wage` (CAD/hora) |
| `vl_salario_medio` | NUMBER | 10,2 | — | `Average_Wage` |
| `vl_quartil1` | NUMBER | 10,2 | — | `Quartile1_Wage` |
| `vl_quartil3` | NUMBER | 10,2 | — | `Quartile3_Wage` |
| `vl_amplitude_salarial` | NUMBER | 10,2 | — | `vl_salario_maximo - vl_salario_minimo` (derivada) |
| `fl_salario_anual` | NUMBER | 1 | `CK_FATO_SALARIO_FL_ANUAL` (0/1) | `Annual_Wage_Flag` (0 = hora, 1 = anual) |

### 2.2 `fato_imigracao`

**Grão:** província + país de nascimento + período de imigração + Censo.

| Campo | Tipo | Tamanho | Constraint | Descrição / Origem |
|---|---|---|---|---|
| `sk_fato_imigracao` | NUMBER | 15 | `PK_FATO_IMIGRACAO` | Surrogate key (SEQ_FATO_IMIGRACAO) |
| `sk_provincia` | NUMBER | 10 | `FK_FATO_IMIG_DIM_PROVINCIA` | → `dim_provincia` |
| `sk_pais_nascimento` | NUMBER | 10 | `FK_FATO_IMIG_DIM_PAIS` | → `dim_pais_nascimento` |
| `sk_periodo_imigracao` | NUMBER | 10 | `FK_FATO_IMIG_DIM_PERIODO` | → `dim_periodo_imigracao` |
| `sk_tempo_censo` | NUMBER | 10 | `FK_FATO_IMIG_DIM_TEMPO_CENSO` | → `dim_tempo_censo` |
| `sk_fonte` | NUMBER | 10 | `FK_FATO_IMIG_DIM_FONTE` | → `dim_fonte` |
| `qt_imigrantes` | NUMBER | 12 | `CK_FATO_IMIGRACAO_QT` (`>= 0`) | Contagem de imigrantes (medida aditiva) |

A **participação brasileira** não é coluna do fato; é calculada na apresentação:
`qt_imigrantes(país = Brazil) / qt_imigrantes(país = Total – Place of birth)`.

### 2.3 `fato_habitacao`

**Grão:** província + posse (tenure) + indicador habitacional + Censo.

| Campo | Tipo | Tamanho | Constraint | Descrição / Origem |
|---|---|---|---|---|
| `sk_fato_habitacao` | NUMBER | 15 | `PK_FATO_HABITACAO` | Surrogate key (SEQ_FATO_HABITACAO) |
| `sk_provincia` | NUMBER | 10 | `FK_FATO_HAB_DIM_PROVINCIA` | → `dim_provincia` |
| `sk_tenencia` | NUMBER | 10 | `FK_FATO_HAB_DIM_TENENCIA` | → `dim_tenencia` |
| `sk_indicador_habitacao` | NUMBER | 10 | `FK_FATO_HAB_DIM_INDICADOR` | → `dim_indicador_habitacao` |
| `sk_tempo_censo` | NUMBER | 10 | `FK_FATO_HAB_DIM_TEMPO_CENSO` | → `dim_tempo_censo` |
| `sk_fonte` | NUMBER | 10 | `FK_FATO_HAB_DIM_FONTE` | → `dim_fonte` |
| `vl_medida` | NUMBER | 15,2 | `CK_FATO_HABITACAO_VL` (`>= 0`) | Contagem ou percentual (ver `dim_indicador_habitacao.tp_medida`) |

## 3. Staging (espelha os CSVs antes das transformações)

| Tabela | Origem | Observação |
|---|---|---|
| `stg_job_bank_wages` | `raw/job_bank_wages_2025.csv` | 22 colunas do CSV, todas como `VARCHAR2` para validação |
| `stg_statcan_imigracao` | extração da tabela 98-10-0307-01 | colunas do CSV preservadas |
| `stg_statcan_habitacao` | `raw/98100258_extracted/98100258.csv` | 11 colunas do CSV preservadas |
