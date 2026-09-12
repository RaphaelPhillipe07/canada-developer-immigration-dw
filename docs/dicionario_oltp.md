# Dicionário de Dados — Bases OLTP (origem)

Este documento descreve as bases operacionais de origem ("OLTP") usadas no projeto, seguindo a abordagem do exemplo da disciplina (CSVs públicos tratados como sistema OLTP de origem). Os arquivos brutos são preservados sem alteração em `raw/`; as extrações e filtros usados nas análises ficam em `filtered/`.

## 1. Government of Canada — Job Bank / ESDC Wages

**Arquivo:** `raw/job_bank_wages_2025.csv`
**Fonte:** [Government of Canada — Wages Dataset](https://open.canada.ca/data/en/dataset/adad580f-76b0-4502-bd05-20c125de9116)
**Release:** 2025 · **Revisão:** 2025-11-19 · **Formato:** CSV (UTF-8 com BOM) · **Registros:** 44.376 · **Colunas:** 22

Descrição: salários publicados pelo Job Bank para ocupações NOC (National Occupational Classification), em nível nacional (`NAT`/`ER00`), provincial e de região econômica. Vários períodos de referência coexistem no arquivo (2021, 2023-2024, 2024 e `NA`).

### 1.1 Dicionário de campos

| # | Campo | Descrição | Tipo (CSV) | Domínio / Restrições | Exemplo |
|---|---|---|---|---|---|
| 1 | `NOC_CNP` | Código NOC da ocupação | Texto | `NOC_00010` … `NOC_9XXXX`; 516 códigos distintos | `NOC_21232` |
| 2 | `NOC_Title_eng` | Título da ocupação em inglês | Texto | — | `Software developers and programmers` |
| 3 | `NOC_Title_fra` | Título da ocupação em francês | Texto | — | `Développeurs/développeuses et programmeurs/programmeuses de logiciels` |
| 4 | `prov` | Código da província/território ou nacional | Texto | `NAT`, `NL`, `PEI`, `NS`, `NB`, `QC`, `ON`, `MB`, `SK`, `AB`, `BC`, `YK`, `NWT`, `NU` | `ON` |
| 5 | `ER_Code_Code_RE` | Código da região econômica | Texto | `ER00` = Canadá; `ER` + 2 dígitos = província/território; `ER` + 4 dígitos = região econômica | `ER1010` |
| 6 | `ER_Name` | Nome da região econômica em inglês | Texto | — | `Avalon Peninsula` |
| 7 | `Nom_RE` | Nome da região econômica em francês | Texto | — | `Avalon Peninsula` |
| 8 | `Low_Wage_Salaire_Minium` | Salário mínimo (CAD/hora ou anual) | Numérico (texto) | Vazio quando não publicado | `30.77` |
| 9 | `Median_Wage_Salaire_Median` | Salário mediano (CAD/hora ou anual) | Numérico (texto) | Vazio quando não publicado | `43.75` |
| 10 | `High_Wage_Salaire_Maximal` | Salário máximo (CAD/hora ou anual) | Numérico (texto) | Vazio quando não publicado | `74.52` |
| 11 | `Average_Wage_Salaire_Moyen` | Salário médio | Numérico (texto) | Vazio quando não publicado | `46.26` |
| 12 | `Quartile1_Wage_Salaire_Quartile1` | 1º quartil salarial | Numérico (texto) | Vazio quando não publicado | `35.71` |
| 13 | `Quartile3_Wage_Salaire_Quartile3` | 3º quartil salarial | Numérico (texto) | Vazio quando não publicado | `54.49` |
| 14 | `Source2025_NHQ` | Fonte/levantamento do dado | Texto | `Census 2021 CAN/PR/ER NOC5`, `LFS 2023-24 …`, `SAE 2024 …`, `EI 2023-24 …`, `N/A`, etc. | `LFS 2023-24 PR NOC5` |
| 15 | `Data_Source_E` | Descrição da fonte (inglês) | Texto | — | `Labour Force Survey` |
| 16 | `Data_Source_F` | Descrição da fonte (francês) | Texto | — | `Enquête sur la population active` |
| 17 | `Reference_Period` | Período de referência dos salários | Texto | `2021`, `2023-2024`, `2024`, `NA` | `2023-2024` |
| 18 | `Revision_Date_Date_revision` | Data de revisão do dado | Data (texto) | `YYYY-MM-DD` | `2025-11-19` |
| 19 | `Annual_Wage_Flag_Salaire_annuel` | Indicador de salário anual | Inteiro (texto) | `0` = por hora; `1` = anual | `0` |
| 20 | `Wage_Comment_E` | Comentário sobre publicação/ausência (inglês) | Texto | Mensagens como *"Due to data limitations, the wage for this occupation cannot be published…"* | — |
| 21 | `Wage_Comment_F` | Comentário sobre publicação/ausência (francês) | Texto | Idem, em francês | — |
| 22 | `EmployeesWithNonWageBenefit_Pct` | % de empregados com benefícios não salariais | Numérico (texto) | 0–100 ou vazio | `94.8` |

### 1.2 Observações importantes

- O arquivo bruto tem **20.301 / 20.012 / 20.288 células vazias** em low/median/high (≈45% dos 44.376 registros). Para `NOC_21232`, a ausência ocorre principalmente em regiões econômicas e territórios, indicada por `Wage_Comment_E`.
- Para `NOC_21232`, o recorte usado é `Reference_Period = 2023-2024`, `Annual_Wage_Flag = 0` (salário por hora) e `Source2025_NHQ = LFS 2023-24 PR NOC5` no nível provincial.
- O código de província do Job Bank (`prov`) **não** é um DGUID do Statistics Canada; o cruzamento é feito pelo nome da província em inglês.

## 2. Statistics Canada — Census 2021, tabela 98-10-0307-01 (Imigração)

**Fonte:** [Statistics Canada — Census 2021](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=9810030701)
**Arquivo bruto:** ZIP de 383 MB (preservado como asset; não versionado no Git)
**Extração analisada:** `filtered/statcan_98100307_brazil_provinces_territories.csv` — 26 registros = 13 províncias/territórios × 2 recortes (`Brazil` e `Total – Place of birth`), com `Age (8D) = Total - Age` e `Gender (3) = Total - Gender`.

Descrição: estoque de imigrantes por país de nascimento, período de imigração e localização geográfica, no Censo 2021.

### 2.1 Dicionário de campos (colunas da extração, nomes originais do StatCan)

| # | Campo | Descrição | Tipo | Domínio / Restrições | Exemplo |
|---|---|---|---|---|---|
| 1 | `REF_DATE` | Ano de referência do Censo | Inteiro | `2021` | `2021` |
| 2 | `GEO` | Nome da província/território em inglês | Texto | 13 jurisdições | `Ontario` |
| 3 | `DGUID` | Identificador geográfico único do Censo | Texto | `2021A0002XX` (13 códigos) | `2021A000235` |
| 4 | `Age (8D)` | Faixa etária | Texto | `Total - Age` (recorte usado) | `Total - Age` |
| 5 | `Gender (3)` | Gênero | Texto | `Total - Gender` (recorte usado) | `Total - Gender` |
| 6 | `Place of birth (290)` | País de nascimento | Texto | `Brazil`, `Total – Place of birth` | `Brazil` |
| 7 | `Coordinate` | Código de hierarquia geográfica do Censo | Texto | `2.1.1.1` (total), `2.1.1.64` (Brazil) | `2.1.1.64` |
| 8 | `Immigrant status and period of immigration (11):Total - Immigrant status and period of immigration[1]` | População total | Inteiro | ≥ 0 | `502100` |
| 9 | `Symbol` | Símbolo de qualidade/supressão do StatCan | Texto | Vazio na extração; no bruto pode conter `x`, `E`, etc. | — |
| 10 | `…:Non-immigrants[2]` | Não imigrantes | Inteiro | ≥ 0 | `482610` |
| 11 | `…:Immigrants[3]` | Total de imigrantes | Inteiro | ≥ 0 | `14250` |
| 12 | `…:Before 1980[4]` | Imigrantes chegados antes de 1980 | Inteiro | ≥ 0 | `90` |
| 13 | `…:1980 to 1990[5]` | Chegados entre 1980 e 1990 | Inteiro | ≥ 0 | `75` |
| 14 | `…:1991 to 2000[6]` | Chegados entre 1991 e 2000 | Inteiro | ≥ 0 | `120` |
| 15 | `…:2001 to 2010[7]` | Chegados entre 2001 e 2010 | Inteiro | ≥ 0 | `250` |
| 16 | `…:2011 to 2021[8]` | Chegados entre 2011 e 2021 | Inteiro | ≥ 0 | `305` |
| 17 | `…:2011 to 2015[9]` | Chegados entre 2011 e 2015 | Inteiro | ≥ 0 | `120` |
| 18 | `…:2016 to 2021[10]` | Chegados entre 2016 e 2021 | Inteiro | ≥ 0 | `185` |
| 19 | `…:Non-permanent residents[11]` | Residentes não permanentes | Inteiro | ≥ 0 | `5` |

Cada coluna de medida é seguida de uma coluna `Symbol` (supressão/qualidade). No recorte usado todas estão vazias; no bruto devem ser tratadas como metadado, não como medida.

### 2.2 Observações importantes

- As colunas de período são **partições** do total de imigrantes: `Before 1980` + `1980-1990` + `1991-2000` + `2001-2010` + `2011-2021` = `Immigrants[3]`.
- `Total – Place of birth` fornece o denominador (total de imigrantes da província); `Brazil` fornece o numerador.
- O DGUID é a chave geográfica canônica do Statistics Canada; o Job Bank usa `prov`/`ER_Code`, por isso o mapeamento é feito por nome em inglês.

## 3. Statistics Canada — Census 2021, tabela 98-10-0258-01 (Habitação)

**Fonte:** [Statistics Canada — Housing indicators](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=9810025801)
**Arquivo bruto:** `raw/98100258-eng.zip` (60 KB) → `raw/98100258_extracted/98100258.csv` — 2.988 registros (Canada + províncias + CMAs/CAs, Censos 2016 e 2021)
**Extração analisada:** `filtered/statcan_98100258_housing_provinces_territories.csv` — 117 registros = 13 províncias/territórios × 9 indicadores, Censo 2021

Descrição: indicadores habitacionais por posse (total, proprietário, inquilino e moradia fornecida pelo governo local/First Nation/Indian band).

### 3.1 Dicionário de campos

| # | Campo | Descrição | Tipo | Domínio / Restrições | Exemplo |
|---|---|---|---|---|---|
| 1 | `REF_DATE` | Ano de referência | Inteiro | `2021` | `2021` |
| 2 | `GEO` | Nome da geografia em inglês | Texto | 166 geografias no bruto; 13 províncias/territórios no recorte | `Ontario` |
| 3 | `DGUID` | Identificador geográfico único do Censo | Texto | `2021A0002XX` para províncias/territórios | `2021A000235` |
| 4 | `Census year (2)` | Ano do Censo | Texto | `2016`, `2021` (recorte: `2021`) | `2021` |
| 5 | `Housing indicators (9)` | Indicador habitacional | Texto | 9 valores: `Total - Housing indicators`, `Adequacy: inadequate housing`, `Affordability: unaffordable housing`, `Core housing need: in core housing need`, `Percent of households in core housing need`, `Percent of households in inadequate housing`, `Percent of households in unaffordable housing`, `Percent of households in unsuitable housing`, `Suitability: unsuitable housing` | `Affordability: unaffordable housing` |
| 6 | `Coordinate` | Código de hierarquia do Censo | Texto | — | `54.1.6` |
| 7 | `Tenure (4):Total - Tenure[1]` | Total de domicílios | Inteiro | ≥ 0 | `1312095` |
| 8 | `Symbol` | Símbolo de qualidade/supressão | Texto | Vazio no recorte | — |
| 9 | `Tenure (4):Owner[2]` | Domicílios de proprietários | Inteiro | ≥ 0 | `656545` |
| 10 | `Tenure (4):Renter[3]` | Domicílios de inquilinos | Inteiro | ≥ 0 | `655555` |
| 11 | `Tenure (4):Dwelling provided by the local government, First Nation or Indian band[4]` | Moradias fornecidas pelo governo local/First Nation/Indian band | Inteiro | ≥ 0 | `0` |

### 3.2 Observações importantes

- `Affordability: unaffordable housing` corresponde à moradia com **gasto de 30% ou mais da renda** em custos de abrigo (indicador usado na pergunta 9 do plano).
- As linhas `Percent of households in …` já são percentuais derivados (0–100); as demais linhas são contagens.
- No recorte usado, `Tenure (4):Renter[3]` é a medida principal para a pergunta sobre inquilinos; `Owner[2]` e `Total[1]` permitem comparar proprietários vs. inquilinos.

## 4. Artefato de junção (staging, não é OLTP)

**Arquivo:** `canada_provinces_brazil_software_developer_wages.csv` — 13 linhas, 16 colunas.

Resultado do *left join* das 13 jurisdições do StatCan com os salários provinciais do Job Bank pelo nome da província em inglês. `N/A` é preservado onde o Job Bank não publica salário provincial (PEI, Yukon, NWT, Nunavut). Este arquivo **não** é base OLTP; é um artefato de staging usado para validar o cruzamento e a EDA.
