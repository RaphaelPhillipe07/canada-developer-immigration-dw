# Guia de apresentação — Guia Canadá

Este guia acompanha as 14 telas: abertura, perguntas, método, consultas 1–10 e conclusões. As falas detalhadas ficam em `src/presenter-notes.ts`, separadas do conteúdo destinado à turma. As perguntas e respostas aprovadas continuam em `src/data.ts`.

## Ritmo sugerido

Reserve cerca de 1 minuto para abertura/perguntas, 2 minutos para método e 40–60 segundos para cada consulta. Em cada resultado: leia a pergunta, diga a resposta, mostre a marca visual que a comprova e explique a limitação principal. Ajuste o ritmo ao tempo concedido pelo professor.

No método, mantenha as quatro etapas visíveis. Na fala, diferencie o processo conceitual do DW, a integração documentada dos extratos e o contrato de dados usado pela interface. Abra os detalhes apenas para responder a uma dúvida.

## Lembretes essenciais

- **Comunidade:** imigrantes nascidos no Brasil, não todos os brasileiros ou descendentes. Referência censitária: 2021.
- **Salário:** mediana em CAD/h para NOC 21232; período 2023–2024. O recurso foi publicado como Job Bank 2025 e revisado em 19/11/2025. Essas datas têm papéis diferentes.
- **Moradia:** percentual de inquilinos que gasta pelo menos 30% da renda com moradia no universo da tabela; não é aluguel nem percentual médio do salário gasto.
- **Cobertura:** 13 jurisdições no conjunto censitário; 10 províncias em certos cruzamentos; 9 salários provinciais utilizáveis. Ausência: Sem dado.
- **Cortes:** salário 45,67 CAD/h; comunidade 1.122,5 pessoas; moradia 33,3%. Explicar a direção do corte em cada pergunta.
- **Consulta 5:** 25.830 / 27.680 × 100 = 93,3%; só chegadas de 2011–2021 nas nove províncias com salário.
- **Consulta 8:** mediana dos valores provinciais por grupo; cobertura salarial 5/5 versus 4/5, sem ponderação por população.
- **Consulta 9:** min–max nos nove casos completos, pesos iguais; inverter o componente de moradia. A interface exibe os scores fornecidos.
- **Conclusão:** análise descritiva, sem causalidade ou recomendação individual de migração.

## Evidência documental consultada

Os seguintes arquivos locais foram lidos; o diretório `.deployment` permaneceu somente para leitura:

| Arquivo | O que confirma |
| --- | --- |
| `src/data.ts` | 13 jurisdições, métricas, unidades, períodos, dez perguntas/respostas, cortes e scores fornecidos |
| `src/charts.tsx` | Recortes dos gráficos, cruzamentos, grupos, fontes e tabelas de apoio |
| `src/MethodPreview.tsx` | Quatro etapas do processo, contrato parcial e distinção do esquema físico |
| `.deployment/README.md` | Fonte censitária 98-10-0307-01; filtros idade/gênero total e Brazil; NOC 21232 provincial; left join por nome inglês normalizado; referência salarial 2023–2024 e publicação 2025 |
| `.deployment/filtered/statcan_98100307_brazil_provinces_territories.csv` | Cabeçalho e linhas de exemplo do extrato censitário, DGUIDs, universo e períodos |
| `.deployment/filtered/job_bank_wages_2025_noc_21232.csv` | Cabeçalho e linhas de exemplo: unidade horária, referência, revisão e cobertura provincial |
| `.deployment/canada_provinces_brazil_software_developer_wages.csv` | Cabeçalho e linhas de exemplo do arquivo integrado e N/A salarial em Prince Edward Island |

A pasta irmã `../tabd-source-1794768513259` estava vazia na inspeção. Os arquivos consultados não descrevem um esquema físico, código SQL ou ferramenta de ETL. O README do extrato não identifica a tabela censitária específica do indicador de moradia; não atribuí-la à tabela de imigração. Esses limites são registrados nas notas e não impedem apresentar os resultados aprovados do conjunto.
