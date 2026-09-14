# Data Warehouse de Oportunidades para Desenvolvedores Imigrantes no Canadá

Projeto da disciplina **Tópicos Avançados em Banco de Dados (IFAL)**. Integra dados oficiais do Statistics Canada e do Job Bank/ESDC em um Data Warehouse Oracle para comparar, entre as províncias e territórios canadenses, a remuneração de desenvolvedores de software (NOC 21232), a comunidade imigrante brasileira e a acessibilidade habitacional.

**Equipe:** Eliezir Moreira Peixoto Neto e Raphael Phillipe da Silva Silverio.

## Objetivo e Meta SMART

Construir um Data Warehouse em Oracle que integre **duas fontes institucionais** — Statistics Canada e Job Bank/ESDC — por meio de **três conjuntos de dados** e permita responder às 10 perguntas analíticas do plano **sem estimar valores ausentes**.

- **S** — Construir um DW em Oracle com dados oficiais de imigração, salários e habitação.
- **M** — Integrar os três conjuntos de dados em um modelo dimensional capaz de responder às 10 perguntas analíticas definidas, contemplando as 13 províncias e territórios canadenses sempre que houver dados disponíveis na fonte.
- **A** — Duas fontes institucionais e três conjuntos de dados, já baixados e filtrados, com modelo viável em Oracle.
- **R** — Apoiar a decisão de devs imigrantes sobre a melhor província.
- **T** — Até 14 de dezembro de 2026.

## As 10 perguntas analíticas

Definidas priorizando o **cruzamento entre fontes**: sete das dez só podem ser respondidas combinando duas ou três bases — é o que justifica o Data Warehouse. O cruzamento das perguntas 4 a 10 depende de `dim_provincia` ser dimensão conformada entre os três fatos.

| # | Pergunta | Bases |
|---|---|---|
| 1 | Quais províncias pagam os maiores salários medianos para NOC 21232? | salário |
| 2 | Onde estão os imigrantes nascidos no Brasil e em que período chegaram? | imigração |
| 3 | Onde os inquilinos mais comprometem ≥ 30% da renda com moradia? | habitação |
| 4 | Quais províncias combinam salário mediano alto e comunidade brasileira numerosa? | salário + imigração |
| 5 | A imigração brasileira de 2011–2021 concentrou-se nas províncias de maior salário mediano? | salário + imigração |
| 6 | Em quais províncias o salário é alto e a proporção de inquilinos com moradia inacessível é baixa? | salário + habitação |
| 7 | Em quais províncias a comunidade brasileira é numerosa e a moradia é menos acessível? | imigração + habitação |
| 8 | As províncias com maior presença brasileira apresentam salários e condições de moradia diferentes das de menor presença? | as três |
| 9 | Qual província oferece o melhor equilíbrio entre remuneração, comunidade e acessibilidade habitacional? | as três |
| 10 | Nas jurisdições sem salário provincial publicado, o que comunidade e moradia revelam? | as três |

## Bases de dados

| Base | Órgão / período | Onde está |
|---|---|---|
| Statistics Canada 98-10-0307-01 (imigração) | Census 2021 | extração `filtered/statcan_98100307_brazil_provinces_territories.csv`; ZIP bruto de 383 MB fora do Git |
| Job Bank / ESDC Wages (NOC 21232) | Release 2025 · referência 2023–2024 | `raw/job_bank_wages_2025.csv` + `filtered/job_bank_wages_2025_noc_21232.csv` |
| Statistics Canada 98-10-0258-01 (habitação) | Census 2021 | `raw/98100258_extracted/98100258.csv` + `filtered/statcan_98100258_housing_provinces_territories.csv` |

São duas fontes institucionais: Statistics Canada fornece os datasets de imigração e habitação; Job Bank/ESDC fornece o dataset salarial.

## Estrutura do repositório

```
├── planning/
│   └── project_plan.html           # plano das 4 entregas
├── presentation/                   # slides HTML (Entrega 1 · 13 slides · tema Canadá)
│   ├── index.html
│   ├── css/theme.css
│   ├── js/engine.js, intro.js
│   └── images/                     # gráficos usados nos slides
├── docs/
│   ├── dw_canada.docx              # trabalho escrito (padrão IFAL)
│   ├── dicionario_oltp.md
│   ├── eda_oltp.md
│   ├── modelo_dimensional.md
│   ├── dicionario_dw.md
│   └── figuras/                    # cópias avulsas dos gráficos
├── sql/
│   └── script_oracle.sql           # tablespaces, sequences, staging, dimensões, fatos e índices
├── tools/apoio_nao_avaliado/       # scripts de reprodução, fora da avaliação
│   ├── eda_oltp.py                 # análise exploratória
│   ├── gerar_diagrama_modelo.py    # gera o diagrama do DW
│   └── gerar_docx.py               # gera o trabalho escrito DOCX
├── raw/                            # brutos versionados (não inclui o ZIP de imigração)
├── filtered/                       # extrações e filtros
├── resumo_do_projeto.txt           # resumo da meta e bases
└── canada_provinces_brazil_software_developer_wages.csv  # junção staging
```

## Como executar

```bash
# Scripts de apoio não avaliáveis
python tools/apoio_nao_avaliado/eda_oltp.py
python tools/apoio_nao_avaliado/gerar_docx.py

# Abrir os slides
cd presentation && python -m http.server 8765
# acesse http://127.0.0.1:8765/index.html
```

## Status das entregas

- **Entrega 1 — projeto e desenho:** concluída (slides, trabalho escrito, dicionários, EDA, modelo Star Schema e script SQL Oracle).
- **Entrega 2 — ETL:** pendente (vídeo das cargas + documentação dos plans PDI e instruções de execução).
- **Entrega 3 — dashboards:** pendente (slides + painéis respondendo às 10 perguntas).
- **Entrega 4 — grafos:** pendente (Arrows.app + Cypher/PGQL + comparação com dashboards).

## Fontes preservadas sem modificação

- `raw/job_bank_wages_2025.csv` — Job Bank/ESDC, dataset `adad580f-76b0-4502-bd05-20c125de9116`, revisão 2025-11-19.
- `raw/98100258_extracted/98100258.csv` — Statistics Canada, tabela 98-10-0258-01 (habitação), extraído do ZIP oficial.
- Tabela 98-10-0307-01 — Statistics Canada (imigração): o ZIP bruto de cerca de 383 MB não é versionado no Git. Download reproduzível: `https://www150.statcan.gc.ca/n1/en/tbl/csv/98100307-eng.zip` (extração: 14 set. 2026). Após baixar, executar `shasum -a 256 98100307-eng.zip`, registrar o resultado em `dim_fonte.ds_checksum`, descompactar e aplicar os filtros documentados para gerar a extração em `filtered/`.

## Transformações (raw → filtered)

- `filtered/statcan_98100307_brazil_provinces_territories.csv` — 13 províncias/territórios × (`Brazil`, `Total – Place of birth`), com `Age = Total - Age` e `Gender = Total - Gender`.
- `filtered/job_bank_wages_2025_all_regions_noc_21232.csv` — 86 registros de NOC 21232.
- `filtered/job_bank_wages_2025_noc_21232.csv` — 9 províncias com salário provincial publicado (CAD/hora).
- `filtered/statcan_98100258_housing_provinces_territories.csv` — 13 províncias × 9 indicadores × Censo 2021.
- `canada_provinces_brazil_software_developer_wages.csv` — left join StatCan × Job Bank por nome de província em inglês; `N/A` onde não há salário publicado.

## Tratamento geográfico e limitações

- StatCan usa DGUID (ex.: Ontário `2021A000235`); Job Bank usa códigos `prov` (ex.: `ON`) e regiões econômicas (`ER...`). O cruzamento é feito pelo **nome da província em inglês**.
- Job Bank 2025 publica salário provincial de NOC 21232 para NL, NS, NB, QC, ON, MB, SK, AB e BC. PEI só aparece como região econômica (`ER1110`); Yukon, NWT e Nunavut ficam `N/A`. Nenhum valor regional foi usado para preencher essas lacunas.
- Imigração e habitação são do Censo 2021; salários têm referência 2023–2024. Os períodos não são tratados como o mesmo ano — cada fato tem sua própria dimensão de tempo.
