# Roteiro da Análise Exploratória — Bases de origem

Roteiro e resultados da EDA exigida na Entrega 1. O script de apoio `tools/apoio_nao_avaliado/eda_oltp.py` lê os arquivos preservados em `raw/` e `filtered/`, imprime um resumo em Markdown e **não altera nenhum dado**.

## 1. Como executar

```bash
python tools/apoio_nao_avaliado/eda_oltp.py
```

Requisitos: apenas a biblioteca padrão do Python 3 (sem dependências externas).

## 2. Fontes analisadas

| Arquivo | Papel na EDA |
|---|---|
| `raw/job_bank_wages_2025.csv` | Dataset bruto de salários (Job Bank/ESDC) |
| `filtered/job_bank_wages_2025_noc_21232.csv` | Recorte provincial NOC 21232 usado para a análise salarial |
| `filtered/statcan_98100307_brazil_provinces_territories.csv` | Extração de origem do Statistics Canada (Censo 2021, imigração) |
| `filtered/statcan_98100258_housing_provinces_territories.csv` | Extração de origem do Statistics Canada (Censo 2021, habitação) |
| `canada_provinces_brazil_software_developer_wages.csv` | Junção staging das duas fontes principais (validação do cruzamento) |

Observação: o ZIP bruto do Statistics Canada de imigração (383 MB) não está versionado; a EDA de imigração usa a extração `filtered/` que preserva os nomes originais das colunas. O ZIP de habitação (60 KB) está preservado em `raw/98100258-eng.zip`.

## 3. Resultados

### 3.1 Job Bank — dataset bruto de salários

- **44.376 registros** e **516 ocupações NOC distintas**.
- A ocupação de interesse, `NOC_21232` (Software developers and programmers), tem **86 registros**.
- `prov` tem 14 valores: `NAT` (nacional) + 13 províncias/territórios.
- `Reference_Period` do arquivo bruto: `2021` (431), `2023-2024` (13.454), `2024` (10.509) e `NA` (19.982). O recorte do projeto usa `2023-2024`.
- `Annual_Wage_Flag_Salaire_annuel`: `0` = por hora (43.161 linhas) e `1` = anual (1.215 linhas). Para NOC 21232, no recorte provincial, o flag é `0` (salário por hora).
- Valores ausentes no arquivo bruto: `Low_Wage` 20.301 vazios (45,7%), `Median_Wage` 20.012 (45,1%) e `High_Wage` 20.288 (45,7%). A ausência é explicada por `Wage_Comment_E` (limitações de dados; remete ao nível provincial ou nacional).

Para NOC 21232, `Source2025_NHQ`:

| Source2025_NHQ | linhas |
|---|---|
| LFS 2023-24 CAN NOC5 | 1 |
| LFS 2023-24 ER NOC5 | 20 |
| LFS 2023-24 PR NOC5 | 11 |
| N/A | 29 |
| SAE 2024 ER NOC5 | 25 |

Para NOC 21232, `Wage_Comment_E`:

| Wage_Comment_E | linhas |
|---|---|
| (vazio — salário publicado) | 57 |
| *Due to data limitations… refer to the wage published … at the provincial level.* | 26 |
| *Due to data limitations… refer to the wage published … at the national level.* | 3 |

### 3.2 Job Bank — salários provinciais NOC 21232 (recorte analisado)

Apenas **9 províncias** têm salário provincial publicado. Salários em CAD/hora, ordenados pela mediana:

| prov | low | median | high | amplitude (high-low) |
|---|---|---|---|---|
| BC | 31.25 | 52.40 | 84.13 | 52.88 |
| ON | 30.29 | 48.08 | 77.40 | 47.11 |
| AB | 29.81 | 48.08 | 76.92 | 47.11 |
| SK | 28.85 | 48.07 | 68.68 | 39.83 |
| NB | 28.00 | 45.67 | 74.04 | 46.04 |
| QC | 29.00 | 45.67 | 68.13 | 39.13 |
| NL | 30.77 | 43.75 | 74.52 | 43.75 |
| MB | 30.00 | 41.03 | 62.02 | 32.02 |
| NS | 24.50 | 40.87 | 66.67 | 42.17 |

Mediana entre as 9 províncias: **mín. 40,87 | máx. 52,40 | média 45,96**. A maior amplitude salarial é em **BC (52,88)**; a menor, em **MB (32,02)**.

### 3.3 Statistics Canada — imigração (Censo 2021)

- **26 registros** = 13 jurisdições × 2 recortes de `Place of birth` (`Brazil` e `Total – Place of birth`).
- `REF_DATE = 2021`, `Age = Total - Age`, `Gender = Total - Gender`.

Imigrantes por província e participação brasileira:

| GEO | total_imigrantes | brasileiros | % brasileiros |
|---|---|---|---|
| Alberta | 970.975 | 3.800 | 0,4% |
| British Columbia | 1.425.715 | 8.765 | 0,6% |
| Manitoba | 257.615 | 1.810 | 0,7% |
| New Brunswick | 44.120 | 240 | 0,5% |
| Newfoundland and Labrador | 14.250 | 90 | 0,6% |
| Northwest Territories | 4.150 | 10 | 0,2% |
| Nova Scotia | 71.570 | 435 | 0,6% |
| Nunavut | 1.165 | 10 | 0,9% |
| Ontario | 4.206.590 | 23.120 | 0,5% |
| Prince Edward Island | 11.765 | 85 | 0,7% |
| Quebec | 1.210.595 | 9.700 | 0,8% |
| Saskatchewan | 137.615 | 380 | 0,3% |
| Yukon | 5.380 | 0 | 0,0% |

Distribuição dos imigrantes brasileiros por período de imigração (soma das 13 jurisdições):

| período | brasileiros |
|---|---|
| Before 1980 | 2.740 |
| 1980 to 1990 | 2.030 |
| 1991 to 2000 | 4.530 |
| 2001 to 2010 | 11.395 |
| 2011 to 2021 | 27.740 |

Leitura: a imigração brasileira é **recente** — mais da metade (27.740 de 48.435) chegou entre 2011 e 2021 — e concentra-se em **Ontário, Quebec e Colúmbia Britânica**.

### 3.4 Junção staging (validação do cruzamento)

A junção cobre **13 jurisdições**; **4 não têm salário provincial publicado** (PEI, Yukon, NWT, Nunavut) e mantêm `N/A`.

Ranking por mediana salarial (N/A no final):

| province | brasileiros_2021 | total_imigrantes | mediana_salarial | low | high |
|---|---|---|---|---|---|
| British Columbia | 8.765 | 1.425.715 | 52.40 | 31.25 | 84.13 |
| Ontario | 23.120 | 4.206.590 | 48.08 | 30.29 | 77.40 |
| Alberta | 3.800 | 970.975 | 48.08 | 29.81 | 76.92 |
| Saskatchewan | 380 | 137.615 | 48.07 | 28.85 | 68.68 |
| New Brunswick | 240 | 44.120 | 45.67 | 28.00 | 74.04 |
| Quebec | 9.700 | 1.210.595 | 45.67 | 29.00 | 68.13 |
| Newfoundland and Labrador | 90 | 14.250 | 43.75 | 30.77 | 74.52 |
| Manitoba | 1.810 | 257.615 | 41.03 | 30.00 | 62.02 |
| Nova Scotia | 435 | 71.570 | 40.87 | 24.50 | 66.67 |
| Prince Edward Island | 85 | 11.765 | N/A | N/A | N/A |
| Yukon | 0 | 5.380 | N/A | N/A | N/A |
| Northwest Territories | 10 | 4.150 | N/A | N/A | N/A |
| Nunavut | 10 | 1.165 | N/A | N/A | N/A |

Top 5 — maior comunidade brasileira:

| province | brasileiros_2021 | mediana_salarial |
|---|---|---|
| Ontario | 23.120 | 48.08 |
| Quebec | 9.700 | 45.67 |
| British Columbia | 8.765 | 52.40 |
| Alberta | 3.800 | 48.08 |
| Manitoba | 1.810 | 41.03 |

### 3.5 Statistics Canada — habitação (Censo 2021)

- **117 registros** = 13 jurisdições × 9 indicadores, `Census year = 2021`.
- Indicadores disponíveis: total, adequação, acessibilidade (affordability), core housing need, adequação/suitability e suas versões percentuais.

% de **inquilinos** com moradia inacessível (gasto ≥ 30% da renda) por província — responde à pergunta 9 do plano:

| GEO | % total | % owner | % renter |
|---|---|---|---|
| Ontario | 24.2 | 17.7 | 38.4 |
| British Columbia | 25.5 | 19.3 | 37.8 |
| Nova Scotia | 17.9 | 9.7 | 34.7 |
| Alberta | 21.2 | 16.0 | 34.0 |
| Manitoba | 17.3 | 9.9 | 33.5 |
| Saskatchewan | 17.2 | 11.1 | 33.1 |
| Newfoundland and Labrador | 14.6 | 8.9 | 32.5 |
| Prince Edward Island | 15.5 | 8.8 | 30.2 |
| New Brunswick | 12.9 | 7.5 | 28.0 |
| Quebec | 16.1 | 10.0 | 25.2 |
| Yukon | 16.2 | 11.7 | 24.9 |
| Northwest Territories | 11.9 | 8.7 | 15.6 |
| Nunavut | 5.7 | 7.3 | 5.2 |

% de inquilinos em **core housing need** por província:

| GEO | % total | % owner | % renter |
|---|---|---|---|
| Nunavut | 32.9 | 14.6 | 37.3 |
| Ontario | 12.1 | 6.4 | 24.9 |
| British Columbia | 13.4 | 8.0 | 24.7 |
| Yukon | 13.1 | 8.0 | 23.3 |
| Saskatchewan | 10.3 | 5.7 | 22.1 |
| Manitoba | 10.1 | 4.8 | 22.0 |
| Newfoundland and Labrador | 8.0 | 4.0 | 20.8 |
| Nova Scotia | 10.0 | 5.0 | 20.7 |
| Alberta | 9.9 | 5.6 | 20.7 |
| Northwest Territories | 13.2 | 8.2 | 18.9 |
| Prince Edward Island | 7.0 | 3.8 | 14.1 |
| New Brunswick | 6.2 | 3.4 | 13.9 |
| Quebec | 6.0 | 2.1 | 11.9 |

Leitura: **ON e BC** têm os maiores percentuais de inquilinos comprometendo ≥ 30% da renda (38,4% e 37,8%); **Nunavut** tem o maior core housing need geral (32,9%), mas o menor percentual de inacessibilidade (5,2%).

## 4. O que escrever no trabalho (interpretação)

1. **Cobertura:** o Job Bank publica salário provincial para 9 das 13 jurisdições; PEI aparece só como região econômica (`ER1110`) e os territórios não têm salário publicado. Nenhum valor regional foi usado para "preencher" essas lacunas.
2. **Distribuição salarial:** BC lidera a mediana (52,40 CAD/h) e a amplitude; NS tem a menor mediana (40,87 CAD/h).
3. **Comunidade brasileira:** concentra-se em ON (23.120), QC (9.700) e BC (8.765); Yukon não registrou brasileiros no Censo 2021.
4. **Perfil temporal:** a chegada de brasileiros é predominantemente recente (2011–2021 = 27.740).
5. **Habitação:** ON e BC concentram os maiores percentuais de inquilinos com gasto ≥ 30% da renda (38,4% e 37,8%); Quebec, apesar da 2ª maior comunidade brasileira, tem os menores percentuais de inquilinos em core housing need (11,9%) e inacessibilidade (25,2%).
6. **Cruzamento inicial:** BC combina a maior mediana salarial com a 3ª maior comunidade brasileira, mas tem alto custo de moradia para inquilinos; ON tem a maior comunidade e a 2ª maior mediana, também com moradia cara. Para a pergunta 10, o ranking será calculado somente para jurisdições com os três indicadores disponíveis: 40% salário mediano normalizado, 30% comunidade brasileira normalizada e 30% acessibilidade normalizada de forma inversa. Valores salariais N/A não recebem imputação nem entram no ranking.
7. **Impacto das transformações:** os filtros aplicados (Age/Gender totais, `Brazil`/`Total – Place of birth`, `NOC_CNP = NOC_21232`, nível provincial, `Census year = 2021`) reduziram 44.376 registros do Job Bank para 9 registros provinciais usados na análise e 2.988 registros de habitação para 117; nenhum valor foi estimado — ausências permanecem como `N/A`/`NULL`.

## 5. Limitações e próximos passos

- **ZIP bruto do StatCan de imigração (383 MB):** para a versão final, registrar checksum e, se possível, executar a EDA sobre a tabela completa extraída do ZIP.
- **Gráficos:** os números acima podem ser transformados em gráficos no Python (matplotlib), no Excel ou no Orange para os slides.
- **Habitação:** os indicadores de percentual já vêm calculados; as contagens (`Affordability: unaffordable housing`) permitem validar os percentuais no DW.
