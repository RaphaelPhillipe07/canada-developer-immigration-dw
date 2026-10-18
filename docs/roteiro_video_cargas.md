# Roteiro do Vídeo — Parte 1 (Demonstração das Cargas ETL)

> Objetivo: demonstrar, passo a passo, a execução dos planos de carga do Data Warehouse
> **DW_CANADA** no Pentaho Data Integration (PDI/Spoon), atendendo aos cinco requisitos do
> professor para o vídeo. Cada requisito vira uma **cena** com comandos prontos para
> copiar/colar no SQL Developer e passos para executar no Spoon.

**Premissas do ambiente (deixar pronto antes de gravar):**

- Oracle acessível com o schema `DW_CANADA` criado pelo `sql/script_oracle.sql`
  (tablespaces, sequences, staging, dimensões, fatos, índices e gatilhos de SK).
- Pentaho Data Integration (Spoon) aberto com o **JOB** de carga (que encadeia as
  transformations de staging → dimensões → fatos).
- SQL Developer (ou SQL*Plus) aberto, **conectado como `DW_CANADA`**.
  Se necessário: `ALTER SESSION SET CURRENT_SCHEMA = DW_CANADA;`
- Tela de gravação: Spoon e SQL Developer **lado a lado**, com zoom para o log ficar legível.

---

## Cena 0 — Preparação: deixar o schema vazio

Para mostrar "tabelas vazias antes da carga", a forma mais limpa é **recriar o schema do zero**:

```sql
-- executar por usuário com privilégio DBA
DROP USER DW_CANADA CASCADE;
```

Em seguida, reexecutar **o `sql/script_oracle.sql` por inteiro** (seção DBA + seção owner).
Isso garante tabelas vazias **e** sequences zeradas — a situação ideal para o início do vídeo.

> Alternativa (sem DROP USER): apagar os dados na ordem **filho → pai** com `DELETE`
> (funciona mesmo com as FKs habilitadas, mas as sequences NÃO voltam ao 1):
>
> ```sql
> DELETE FROM fato_salario;
> DELETE FROM fato_imigracao;
> DELETE FROM fato_habitacao;
> DELETE FROM dim_provincia;
> DELETE FROM dim_ocupacao;
> DELETE FROM dim_tempo_salario;
> DELETE FROM dim_disponibilidade_salario;
> DELETE FROM dim_tempo_censo;
> DELETE FROM dim_pais_nascimento;
> DELETE FROM dim_periodo_imigracao;
> DELETE FROM dim_tenencia;
> DELETE FROM dim_indicador_habitacao;
> DELETE FROM dim_fonte;
> DELETE FROM stg_job_bank_wages;
> DELETE FROM stg_statcan_imigracao;
> DELETE FROM stg_statcan_habitacao;
> COMMIT;
> ```

---

## Cena 1 — Mostrar as tabelas vazias ANTES da carga (requisito 1)

1. No SQL Developer, rodar a **conferência de vazio** abaixo (16 tabelas). Todas devem
   retornar `QTD = 0`.

```sql
SELECT 'stg_job_bank_wages'        AS tabela, COUNT(*) AS qtd FROM stg_job_bank_wages
UNION ALL SELECT 'stg_statcan_imigracao', COUNT(*) FROM stg_statcan_imigracao
UNION ALL SELECT 'stg_statcan_habitacao', COUNT(*) FROM stg_statcan_habitacao
UNION ALL SELECT 'dim_provincia', COUNT(*) FROM dim_provincia
UNION ALL SELECT 'dim_ocupacao', COUNT(*) FROM dim_ocupacao
UNION ALL SELECT 'dim_tempo_salario', COUNT(*) FROM dim_tempo_salario
UNION ALL SELECT 'dim_disponibilidade_salario', COUNT(*) FROM dim_disponibilidade_salario
UNION ALL SELECT 'dim_tempo_censo', COUNT(*) FROM dim_tempo_censo
UNION ALL SELECT 'dim_pais_nascimento', COUNT(*) FROM dim_pais_nascimento
UNION ALL SELECT 'dim_periodo_imigracao', COUNT(*) FROM dim_periodo_imigracao
UNION ALL SELECT 'dim_tenencia', COUNT(*) FROM dim_tenencia
UNION ALL SELECT 'dim_indicador_habitacao', COUNT(*) FROM dim_indicador_habitacao
UNION ALL SELECT 'dim_fonte', COUNT(*) FROM dim_fonte
UNION ALL SELECT 'fato_salario', COUNT(*) FROM fato_salario
UNION ALL SELECT 'fato_imigracao', COUNT(*) FROM fato_imigracao
UNION ALL SELECT 'fato_habitacao', COUNT(*) FROM fato_habitacao;
```

2. **Narrar**: "Todas as 16 tabelas (3 de staging, 10 dimensões e 3 fatos) estão vazias —
   nenhuma carga foi executada ainda."
3. **Enquadrar** o resultado na tela por ~5 segundos.

---

## Cena 2 — Executar a carga e mostrar o LOG (requisito 2)

1. No Spoon, executar o **JOB** de carga (botão ▶). Deixar rodar até o final.
2. Mostrar o **log de execução do job** (aba *Logging* do job) — os passos e o status
   `Finished`/`Success` de cada transformation.
3. Abrir **cada transformation** e mostrar a aba **Step Metrics** (métricas por passo):
   - passo de leitura (`CSV file input` / `Table input`) → coluna **Read** = **registros lidos**;
   - passo de gravação (`Table output`) → coluna **Written** = **registros gravados**.
4. **Narrar** os números: "O passo de leitura do Job Bank leu *N* registros; a gravação em
   `fato_salario` gravou *M* registros; ...".
5. Anotar (para exibir na cena 3) os valores lidos/gravados de cada etapa — eles devem bater
   com a **tabela de valores esperados** do Anexo B.

> Dica: no PDI, se o passo grava **0 linhas novas** porque os registros já existiam
> (idempotência), o `Written` mostra 0 e o `Read` continua mostrando a leitura completa.
> É exatamente isso que a Cena 5 vai evidenciar.

---

## Cena 3 — Mostrar os dados gravados e conferir a quantidade (requisito 2/3)

1. Rodar a **conferência de contagem** (mesma estrutura da Cena 1, agora com valores):

```sql
SELECT 'dim_provincia' AS tabela, COUNT(*) AS qtd FROM dim_provincia
UNION ALL SELECT 'dim_ocupacao', COUNT(*) FROM dim_ocupacao
UNION ALL SELECT 'dim_tempo_salario', COUNT(*) FROM dim_tempo_salario
UNION ALL SELECT 'dim_disponibilidade_salario', COUNT(*) FROM dim_disponibilidade_salario
UNION ALL SELECT 'dim_tempo_censo', COUNT(*) FROM dim_tempo_censo
UNION ALL SELECT 'dim_pais_nascimento', COUNT(*) FROM dim_pais_nascimento
UNION ALL SELECT 'dim_periodo_imigracao', COUNT(*) FROM dim_periodo_imigracao
UNION ALL SELECT 'dim_tenencia', COUNT(*) FROM dim_tenencia
UNION ALL SELECT 'dim_indicador_habitacao', COUNT(*) FROM dim_indicador_habitacao
UNION ALL SELECT 'dim_fonte', COUNT(*) FROM dim_fonte
UNION ALL SELECT 'fato_salario', COUNT(*) FROM fato_salario
UNION ALL SELECT 'fato_imigracao', COUNT(*) FROM fato_imigracao
UNION ALL SELECT 'fato_habitacao', COUNT(*) FROM fato_habitacao;
```

2. Comparar cada valor com o **Anexo B** e narrar a conferência.
3. Mostrar uma **amostra do conteúdo** para provar que os dados foram gravados de fato:

```sql
SELECT * FROM dim_provincia ORDER BY sk_provincia;
SELECT * FROM fato_salario WHERE ROWNUM <= 10;
SELECT * FROM fato_imigracao WHERE ROWNUM <= 10;
SELECT * FROM fato_habitacao WHERE ROWNUM <= 10;
```

---

## Cena 4 — Mostrar que NÃO há dados repetidos (requisito "sem duplicatas")

### 4.1 Dimensões — contagem = contagem de chaves naturais distintas

Para cada dimensão, `total` deve ser **igual** a `distintos` (se fossem iguais e houvesse
repetição, `distintos` seria menor).

```sql
SELECT 'dim_provincia' tabela, COUNT(*) total, COUNT(DISTINCT cd_dguid) distintos FROM dim_provincia
UNION ALL SELECT 'dim_ocupacao', COUNT(*), COUNT(DISTINCT cd_noc) FROM dim_ocupacao
UNION ALL SELECT 'dim_tempo_salario', COUNT(*), COUNT(DISTINCT cd_periodo_referencia) FROM dim_tempo_salario
UNION ALL SELECT 'dim_disponibilidade_salario', COUNT(*), COUNT(DISTINCT cd_disponibilidade) FROM dim_disponibilidade_salario
UNION ALL SELECT 'dim_tempo_censo', COUNT(*), COUNT(DISTINCT nr_ano_censo) FROM dim_tempo_censo
UNION ALL SELECT 'dim_pais_nascimento', COUNT(*), COUNT(DISTINCT cd_pais_nascimento) FROM dim_pais_nascimento
UNION ALL SELECT 'dim_periodo_imigracao', COUNT(*), COUNT(DISTINCT cd_periodo_imigracao) FROM dim_periodo_imigracao
UNION ALL SELECT 'dim_tenencia', COUNT(*), COUNT(DISTINCT cd_tenencia) FROM dim_tenencia
UNION ALL SELECT 'dim_indicador_habitacao', COUNT(*), COUNT(DISTINCT cd_indicador_habitacao) FROM dim_indicador_habitacao
UNION ALL SELECT 'dim_fonte', COUNT(*), COUNT(DISTINCT cd_fonte) FROM dim_fonte;
```

> Narrar: "Em todas as dimensões, `TOTAL = DISTINTOS`, ou seja, nenhuma chave natural se
> repete."

### 4.2 Fatos — nenhum grupo de PK composta repetido

Cada consulta abaixo deve retornar **0** (nenhum grupo duplicado):

```sql
-- fato_salario: PK = (sk_provincia, sk_ocupacao, sk_tempo_salario)
SELECT COUNT(*) AS grupos_duplicados FROM (
  SELECT sk_provincia, sk_ocupacao, sk_tempo_salario
  FROM fato_salario
  GROUP BY sk_provincia, sk_ocupacao, sk_tempo_salario
  HAVING COUNT(*) > 1
);

-- fato_imigracao: PK = (sk_provincia, sk_pais_nascimento, sk_periodo_imigracao, sk_tempo_censo)
SELECT COUNT(*) AS grupos_duplicados FROM (
  SELECT sk_provincia, sk_pais_nascimento, sk_periodo_imigracao, sk_tempo_censo
  FROM fato_imigracao
  GROUP BY sk_provincia, sk_pais_nascimento, sk_periodo_imigracao, sk_tempo_censo
  HAVING COUNT(*) > 1
);

-- fato_habitacao: PK = (sk_provincia, sk_tenencia, sk_indicador_habitacao, sk_tempo_censo)
SELECT COUNT(*) AS grupos_duplicados FROM (
  SELECT sk_provincia, sk_tenencia, sk_indicador_habitacao, sk_tempo_censo
  FROM fato_habitacao
  GROUP BY sk_provincia, sk_tenencia, sk_indicador_habitacao, sk_tempo_censo
  HAVING COUNT(*) > 1
);
```

> Narrar: "As três fatos usam PK composta pelas FKs do grão, então a própria constraint
> impede a duplicata; a consulta confirma `0` grupos repetidos."

---

## Cena 5 — Executar a carga OUTRA VEZ e conferir idempotência (requisito "mais de uma vez")

Aqui se simula o **agendamento** (diário/semanal): rodar a mesma carga mais de uma vez e
provar que ela **não duplica dados**.

1. **Antes de rodar**, anotar as contagens atuais (resultado da Cena 3).
2. Rodar o **JOB de novo** no Spoon (2ª execução — e, se quiser, uma 3ª).
3. No log/metrics da 2ª execução, **destacar**:
   - `Read` continua com o mesmo número (relê a origem);
   - `Written` = **0** para as dimensões (nada novo inserido, pois as chaves naturais já
     existem) e comportamento de *update/upsert* (ou 0 inserções) nas fatos.
4. Rodar **de novo** a conferência de contagem (Cena 3) e a de duplicatas (Cena 4):
   - **contagens idênticas** às da 1ª execução;
   - **0 duplicatas**.
5. **Narrar**: "Executando a carga pela 2ª (e 3ª) vez — simulando o agendamento — as
   contagens permanecem as mesmas e não há registros duplicados, porque o ETL faz *lookup*
   pela chave natural nas dimensões e *upsert* pela PK composta nas fatos."

> Nota opcional (agendamento real): comentar que no ambiente de produção o JOB seria
> executado por agendador via **Kitchen** (Pentaho) + cron / Windows Task Scheduler; o vídeo
> simula isso rodando o mesmo JOB repetidamente.

---

## Cena 6 — Encerramento

1. Fechar com um resumo de 15–20s: tabelas vazias → carga executada → contagens conferidas →
   sem duplicatas → carga repetida sem duplicar.
2. Conferir o **checklist de requisitos** abaixo antes de encerrar a gravação.

### Checklist de requisitos do professor × cena

| Requisito do vídeo | Onde é demonstrado |
|---|---|
| Tabelas vazias antes das cargas | Cena 1 |
| Log de execução com registros lidos e gravados | Cena 2 |
| Dados gravados e conferência de quantidade | Cena 3 |
| Sem dados repetidos (dimensão e fato) | Cena 4 |
| Carga executada mais de uma vez (agendamento) sem duplicar | Cena 5 |

---

## Anexo A — SQL de apoio consolidado

### Conferência de vazio (Cena 1)
```sql
SELECT 'stg_job_bank_wages'        AS tabela, COUNT(*) AS qtd FROM stg_job_bank_wages
UNION ALL SELECT 'stg_statcan_imigracao', COUNT(*) FROM stg_statcan_imigracao
UNION ALL SELECT 'stg_statcan_habitacao', COUNT(*) FROM stg_statcan_habitacao
UNION ALL SELECT 'dim_provincia', COUNT(*) FROM dim_provincia
UNION ALL SELECT 'dim_ocupacao', COUNT(*) FROM dim_ocupacao
UNION ALL SELECT 'dim_tempo_salario', COUNT(*) FROM dim_tempo_salario
UNION ALL SELECT 'dim_disponibilidade_salario', COUNT(*) FROM dim_disponibilidade_salario
UNION ALL SELECT 'dim_tempo_censo', COUNT(*) FROM dim_tempo_censo
UNION ALL SELECT 'dim_pais_nascimento', COUNT(*) FROM dim_pais_nascimento
UNION ALL SELECT 'dim_periodo_imigracao', COUNT(*) FROM dim_periodo_imigracao
UNION ALL SELECT 'dim_tenencia', COUNT(*) FROM dim_tenencia
UNION ALL SELECT 'dim_indicador_habitacao', COUNT(*) FROM dim_indicador_habitacao
UNION ALL SELECT 'dim_fonte', COUNT(*) FROM dim_fonte
UNION ALL SELECT 'fato_salario', COUNT(*) FROM fato_salario
UNION ALL SELECT 'fato_imigracao', COUNT(*) FROM fato_imigracao
UNION ALL SELECT 'fato_habitacao', COUNT(*) FROM fato_habitacao;
```

### Conferência de contagem pós-carga (Cena 3)
```sql
SELECT 'dim_provincia' AS tabela, COUNT(*) AS qtd FROM dim_provincia
UNION ALL SELECT 'dim_ocupacao', COUNT(*) FROM dim_ocupacao
UNION ALL SELECT 'dim_tempo_salario', COUNT(*) FROM dim_tempo_salario
UNION ALL SELECT 'dim_disponibilidade_salario', COUNT(*) FROM dim_disponibilidade_salario
UNION ALL SELECT 'dim_tempo_censo', COUNT(*) FROM dim_tempo_censo
UNION ALL SELECT 'dim_pais_nascimento', COUNT(*) FROM dim_pais_nascimento
UNION ALL SELECT 'dim_periodo_imigracao', COUNT(*) FROM dim_periodo_imigracao
UNION ALL SELECT 'dim_tenencia', COUNT(*) FROM dim_tenencia
UNION ALL SELECT 'dim_indicador_habitacao', COUNT(*) FROM dim_indicador_habitacao
UNION ALL SELECT 'dim_fonte', COUNT(*) FROM dim_fonte
UNION ALL SELECT 'fato_salario', COUNT(*) FROM fato_salario
UNION ALL SELECT 'fato_imigracao', COUNT(*) FROM fato_imigracao
UNION ALL SELECT 'fato_habitacao', COUNT(*) FROM fato_habitacao;
```

### Duplicatas — dimensões (Cena 4.1)
```sql
SELECT 'dim_provincia' tabela, COUNT(*) total, COUNT(DISTINCT cd_dguid) distintos FROM dim_provincia
UNION ALL SELECT 'dim_ocupacao', COUNT(*), COUNT(DISTINCT cd_noc) FROM dim_ocupacao
UNION ALL SELECT 'dim_tempo_salario', COUNT(*), COUNT(DISTINCT cd_periodo_referencia) FROM dim_tempo_salario
UNION ALL SELECT 'dim_disponibilidade_salario', COUNT(*), COUNT(DISTINCT cd_disponibilidade) FROM dim_disponibilidade_salario
UNION ALL SELECT 'dim_tempo_censo', COUNT(*), COUNT(DISTINCT nr_ano_censo) FROM dim_tempo_censo
UNION ALL SELECT 'dim_pais_nascimento', COUNT(*), COUNT(DISTINCT cd_pais_nascimento) FROM dim_pais_nascimento
UNION ALL SELECT 'dim_periodo_imigracao', COUNT(*), COUNT(DISTINCT cd_periodo_imigracao) FROM dim_periodo_imigracao
UNION ALL SELECT 'dim_tenencia', COUNT(*), COUNT(DISTINCT cd_tenencia) FROM dim_tenencia
UNION ALL SELECT 'dim_indicador_habitacao', COUNT(*), COUNT(DISTINCT cd_indicador_habitacao) FROM dim_indicador_habitacao
UNION ALL SELECT 'dim_fonte', COUNT(*), COUNT(DISTINCT cd_fonte) FROM dim_fonte;
```

### Duplicatas — fatos (Cena 4.2)
```sql
SELECT COUNT(*) AS grupos_duplicados FROM (
  SELECT sk_provincia, sk_ocupacao, sk_tempo_salario
  FROM fato_salario
  GROUP BY sk_provincia, sk_ocupacao, sk_tempo_salario
  HAVING COUNT(*) > 1);

SELECT COUNT(*) AS grupos_duplicados FROM (
  SELECT sk_provincia, sk_pais_nascimento, sk_periodo_imigracao, sk_tempo_censo
  FROM fato_imigracao
  GROUP BY sk_provincia, sk_pais_nascimento, sk_periodo_imigracao, sk_tempo_censo
  HAVING COUNT(*) > 1);

SELECT COUNT(*) AS grupos_duplicados FROM (
  SELECT sk_provincia, sk_tenencia, sk_indicador_habitacao, sk_tempo_censo
  FROM fato_habitacao
  GROUP BY sk_provincia, sk_tenencia, sk_indicador_habitacao, sk_tempo_censo
  HAVING COUNT(*) > 1);
```

---

## Anexo B — Valores esperados (referência para conferir no vídeo)

> Derivados dos dados de origem versionados em `raw/` e `filtered/`. O **valor definitivo é o
> que o log do PDI reportar** — use esta tabela para conferir e, se houver divergência,
> investigar antes de gravar.

### Staging (espelha o arquivo de origem antes das transformações)

| Tabela | Origem | Registros esperados |
|---|---|---|
| `stg_job_bank_wages` | `raw/job_bank_wages_2025.csv` | 44.376 |
| `stg_statcan_habitacao` | `raw/98100258_extracted/98100258.csv` | 2.990 |
| `stg_statcan_imigracao` | extração 98-10-0307-01 (ZIP 383 MB) | conferir no log |

### Dimensões

| Tabela | Registros esperados | Justificativa |
|---|---|---|
| `dim_provincia` | 13 | 13 províncias/territórios |
| `dim_ocupacao` | 1 | apenas NOC 21232 |
| `dim_tempo_salario` | 1 | período 2023-2024 |
| `dim_disponibilidade_salario` | 3 | PROVINCIAL_PUBLICADO / APENAS_REGIONAL / INDISPONIVEL |
| `dim_tempo_censo` | 1 | Censo 2021 |
| `dim_pais_nascimento` | 2 | Brazil / Total – Place of birth |
| `dim_periodo_imigracao` | 5 | períodos `[4]..[8]` (Before 1980 … 2011 to 2021) |
| `dim_tenencia` | 4 | TOTAL / OWNER / RENTER / GOV |
| `dim_indicador_habitacao` | 9 | 9 indicadores habitacionais |
| `dim_fonte` | 3 | JOB_BANK_2025 / STATCAN_0307 / STATCAN_0258 |

### Fatos

| Tabela | Registros esperados | Cálculo |
|---|---|---|
| `fato_salario` | 13 | 13 jurisdições × 1 ocupação × 1 período |
| `fato_imigracao` | 130 | 13 províncias × 2 países × 5 períodos |
| `fato_habitacao` | 468 | 13 províncias × 4 tenências × 9 indicadores |
