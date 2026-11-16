# Guia de apresentação — Guia Canadá

Este guia acompanha as 14 telas: abertura, perguntas, método, consultas 1–10 e conclusões. As falas detalhadas ficam em `src/presenter-notes.ts`, separadas do conteúdo destinado à turma. As perguntas e respostas aprovadas continuam em `src/data.ts`.

## Ritmo sugerido

Reserve cerca de 1 minuto para abertura/perguntas, 2 minutos para método e 40–60 segundos para cada consulta. Em cada resultado: leia a pergunta, diga a resposta, mostre a marca visual que a comprova e explique a limitação principal. Ajuste o ritmo ao tempo concedido pelo professor.

No método, mantenha as quatro etapas visíveis. Na fala, diferencie o modelo Oracle, a integração dos extratos, os planos de carga e o contrato da interface. Abra os detalhes apenas para responder a uma dúvida.

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

Fontes consultadas no repositório [canada-developer-immigration-dw](https://github.com/RaphaelPhillipe07/canada-developer-immigration-dw). A cópia `.presentation-checkout` foi usada somente para leitura nesta revisão das notas. Os arquivos de interface continuam sendo a referência dos valores aprovados:

| Arquivo | O que confirma |
| --- | --- |
| `src/data.ts` | 13 jurisdições, métricas, unidades, períodos, dez perguntas/respostas, cortes e scores fornecidos |
| `src/charts.tsx` | Recortes dos gráficos, cruzamentos, grupos, fontes e tabelas de apoio |
| `src/MethodPreview.tsx` | Quatro etapas do processo, contrato parcial e distinção do esquema físico |
| `main: README.md` e `resumo_do_projeto.txt` | Duas fontes institucionais, três datasets; imigração 98-10-0307-01, habitação 98-10-0258-01 e Job Bank NOC 21232 |
| `main: docs/modelo_dimensional.md` e `docs/dicionario_dw.md` | Constelação de três fatos, dez dimensões, grãos, chaves, medidas não aditivas e cobertura salarial explícita |
| `main: sql/script_oracle.sql` | DDL Oracle: três staging, dimensões, fatos, constraints, sequências e gatilhos de chaves substitutas |
| `main: filtered/statcan_98100258_housing_provinces_territories.csv` | Colunas por posse, incluindo Renter; nove indicadores habitacionais por jurisdição; Censo 2021 |
| `segunda-nota-consultas: etl/README.md` e `docs/etl_planos.md` | Planos PDI/Spoon: três cargas de staging, dez dimensões, três fatos e um job sequencial; regras e contagens esperadas |

## Processo técnico para lembrar durante a fala

1. **Extrair:** três CSVs de duas instituições. Conservar unidade, período, origem e identificadores; filtrar treze DGUIDs canônicos e NOC 21232.
2. **Preparar:** staging conserva os campos brutos antes da transformação. Os planos PDI documentados transformam os cinco períodos de chegada e as quatro posses habitacionais de colunas em linhas (`UNPIVOT`).
3. **Modelar:** `dim_provincia` conecta os três fatos. Salário tem grão jurisdição/ocupação/período; imigração, província/país/período de chegada/Censo; habitação, província/posse/indicador/Censo. Cruzar diretamente linhas de grãos diferentes pode repetir salários; agregar cada tema no recorte necessário antes de combinar.
4. **Carregar:** o job documentado executa staging → dimensões → fatos. Dimensões usam busca por chave natural; fatos resolvem chaves substitutas. As constraints do Oracle protegem relacionamentos e unicidade do grão. A documentação descreve atualização sem duplicar nas dimensões/fatos; isso exige verificação em uma execução real, inclusive da staging.
5. **Consultar:** usar apenas `PROVINCIAL_PUBLICADO` nos rankings. PEI é `APENAS_REGIONAL`; os territórios são `INDISPONIVEL`. Manter a ausência e os dados censitários; nunca converter salário ausente em zero.

**Estado da evidência:** o README de `main` marca a Entrega 1 como concluída e o ETL como pendente. A branch `segunda-nota-consultas` contém planos PDI e documentação de execução. Esta revisão não executou Oracle/PDI, não validou logs de carga e não recalculou resultados a partir do DW. Apresente o que está definido e documentado sem afirmar que a carga foi validada.

**Divergência a conferir no DW:** o plano de imigração documentado carrega 13 jurisdições × 2 países × 5 períodos = 130 linhas; não inclui um período separado para o total publicado. Os totais de comunidade da apresentação são os valores censitários aprovados, que podem diferir da soma dos períodos por arredondamento. Preservamos esses totais; antes de substituir o conjunto da interface por uma consulta ao DW, incluir ou recuperar o total publicado e reconciliar os resultados.
