#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera os arquivos ETL do Pentaho Data Integration (.ktr/.kjb) do DW_CANADA.

Uso:
    python tools/apoio_nao_avaliado/gerar_etl_pdi.py

Saída:
    etl/TR_*.ktr  (transformations)
    etl/JOB_CARGA_DW.kjb  (job)

Os arquivos usam a conexão nomeada "DW_CANADA" (Oracle, Native) cujos parâmetros
são variáveis (${DW_HOST}, ${DW_PORT}, ${DW_SID}, ${DW_USER}) definidas em
kettle.properties; a senha é informada uma única vez no Spoon (passo documentado
em etl/README.md). As cargas são idempotentes: dimensões fazem lookup pela chave
natural e Insert/Update; fatos usam a PK composta como chave de lookup.
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "etl")

CONN_NAME = "DW_CANADA"

# ---------------------------------------------------------------- helpers


def esc(s):
    if s is None:
        return ""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def info_block(name, description, parameters=None):
    params = ""
    if parameters:
        items = "".join(
            f"    <parameter><name>{esc(k)}</name>"
            f"<default_value>{esc(v)}</default_value>"
            f"<description>{esc(d)}</description></parameter>\n"
            for k, v, d in parameters
        )
        params = f"  <parameters>\n{items}  </parameters>\n"
    return f"""  <info>
    <name>{esc(name)}</name>
    <description>{esc(description)}</description>
    <extended_description/>
    <trans_version/>
    <trans_type>Normal</trans_type>
    <trans_status>0</trans_status>
    <directory>&#x2f;</directory>
{params}    <log>
      <trans-log-table><connection/><schema/><table/><size_limit_lines/><interval/><timeout_days/>
        <field><id>ID_BATCH</id><enabled>Y</enabled><name>ID_BATCH</name></field>
        <field><id>CHANNEL_ID</id><enabled>Y</enabled><name>CHANNEL_ID</name></field>
        <field><id>TRANSNAME</id><enabled>Y</enabled><name>TRANSNAME</name></field>
        <field><id>STATUS</id><enabled>Y</enabled><name>STATUS</name></field>
        <field><id>LINES_READ</id><enabled>Y</enabled><name>LINES_READ</name><subject/></field>
        <field><id>LINES_WRITTEN</id><enabled>Y</enabled><name>LINES_WRITTEN</name><subject/></field>
        <field><id>LINES_UPDATED</id><enabled>Y</enabled><name>LINES_UPDATED</name><subject/></field>
        <field><id>LINES_INPUT</id><enabled>Y</enabled><name>LINES_INPUT</name><subject/></field>
        <field><id>LINES_OUTPUT</id><enabled>Y</enabled><name>LINES_OUTPUT</name><subject/></field>
        <field><id>LINES_REJECTED</id><enabled>Y</enabled><name>LINES_REJECTED</name><subject/></field>
        <field><id>ERRORS</id><enabled>Y</enabled><name>ERRORS</name><subject/></field>
        <field><id>STARTDATE</id><enabled>Y</enabled><name>STARTDATE</name><subject/></field>
        <field><id>ENDDATE</id><enabled>Y</enabled><name>ENDDATE</name><subject/></field>
        <field><id>LOGDATE</id><enabled>Y</enabled><name>LOGDATE</name><subject/></field>
        <field><id>DEPDATE</id><enabled>Y</enabled><name>DEPDATE</name><subject/></field>
        <field><id>REPLAYDATE</id><enabled>Y</enabled><name>REPLAYDATE</name><subject/></field>
        <field><id>LOG_FIELD</id><enabled>Y</enabled><name>LOG_FIELD</name><subject/></field>
        <field><id>EXECUTING_SERVER</id><enabled>N</enabled><name>EXECUTING_SERVER</name><subject/></field>
        <field><id>EXECUTING_USER</id><enabled>N</enabled><name>EXECUTING_USER</name><subject/></field>
        <field><id>CLIENT</id><enabled>N</enabled><name>CLIENT</name><subject/></field>
      </trans-log-table>
      <perf-log-table><connection/><schema/><table/><interval/><timeout_days/></perf-log-table>
      <channel-log-table><connection/><schema/><table/><timeout_days/></channel-log-table>
      <step-log-table><connection/><schema/><table/><timeout_days/></step-log-table>
      <metrics-log-table><connection/><schema/><table/><timeout_days/></metrics-log-table>
    </log>
    <maxdate><connection/><table/><field/><offset>0.0</offset><maxdiff>0.0</maxdiff></maxdate>
    <size_rowset>10000</size_rowset>
    <sleep_time_empty>50</sleep_time_empty>
    <sleep_time_full>50</sleep_time_full>
    <unique_connections>N</unique_connections>
    <feedback_shown>Y</feedback_shown>
    <feedback_size>50000</feedback_size>
    <using_thread_priorities>Y</using_thread_priorities>
    <shared_objects_file/>
    <capture_step_performance>N</capture_step_performance>
    <step_performance_capturing_delay>1000</step_performance_capturing_delay>
    <step_performance_capturing_size_limit>100</step_performance_capturing_size_limit>
    <dependencies/>
    <partitionschemas/>
    <slaveservers/>
    <clusterschemas/>
    <created_user>-</created_user>
    <created_date>2026/10/18 12:00:00.000</created_date>
    <modified_user>-</modified_user>
    <modified_date>2026/10/18 12:00:00.000</modified_date>
    <key_for_session_key>H4sIAAAAAAAAAAMAAAAAAAAAAAA=</key_for_session_key>
    <is_key_private>N</is_key_private>
  </info>
"""


def connection_block():
    return f"""  <connection>
    <name>{CONN_NAME}</name>
    <server>${{DW_HOST}}</server>
    <type>ORACLE</type>
    <access>Native</access>
    <database>${{DW_SID}}</database>
    <port>${{DW_PORT}}</port>
    <username>${{DW_USER}}</username>
    <password>Encrypted </password>
    <servername/>
    <data_tablespace/>
    <index_tablespace/>
    <attributes>
      <attribute><code>PORT_NUMBER</code><attribute>${{DW_PORT}}</attribute></attribute>
      <attribute><code>FORCE_IDENTIFIERS_TO_LOWERCASE</code><attribute>N</attribute></attribute>
      <attribute><code>FORCE_IDENTIFIERS_TO_UPPERCASE</code><attribute>N</attribute></attribute>
      <attribute><code>IS_CLUSTERED</code><attribute>N</attribute></attribute>
      <attribute><code>QUOTE_ALL_FIELDS</code><attribute>N</attribute></attribute>
      <attribute><code>PREFERRED_SCHEMA_NAME</code><attribute></attribute></attribute>
      <attribute><code>SUPPORTS_BOOLEAN_DATA_TYPE</code><attribute>Y</attribute></attribute>
      <attribute><code>SUPPORTS_TIMESTAMP_DATA_TYPE</code><attribute>Y</attribute></attribute>
      <attribute><code>USE_POOLING</code><attribute>N</attribute></attribute>
      <attribute><code>MAXIMUM_POOL_SIZE</code><attribute>10</attribute></attribute>
      <attribute><code>INITIAL_POOL_SIZE</code><attribute>10</attribute></attribute>
      <attribute><code>STREAM_RESULTS</code><attribute>Y</attribute></attribute>
    </attributes>
  </connection>
"""


def step_wrap(name, stype, config, x, y):
    return f"""    <step>
      <name>{esc(name)}</name>
      <type>{stype}</type>
      <description/>
      <distribute>Y</distribute>
      <custom_distribution/>
      <copies>1</copies>
      <partitioning>
        <method>none</method>
        <schema_name/>
      </partitioning>
{config}      <cluster_schema/>
      <remotesteps>
        <input> </input>
        <output> </output>
      </remotesteps>
      <GUI>
        <xloc>{x}</xloc>
        <yloc>{y}</yloc>
        <draw>Y</draw>
      </GUI>
    </step>
"""


def csv_input_step(name, filename, fields, x, y):
    field_xml = "".join(
        f"""        <field>
          <name>{esc(n)}</name>
          <type>String</type>
          <format/>
          <currency/>
          <decimal/>
          <group/>
          <nullif/>
          <ifnull/>
          <position>{i}</position>
          <length>-1</length>
          <precision>-1</precision>
          <trim_type>both</trim_type>
          <repeat>N</repeat>
        </field>\n"""
        for i, n in enumerate(fields)
    )
    config = f"""      <filename>{esc(filename)}</filename>
      <filename_field/>
      <rownum_field/>
      <include_filename>N</include_filename>
      <separator>,</separator>
      <enclosure>&quot;</enclosure>
      <header>Y</header>
      <buffer_size>50000</buffer_size>
      <lazy_conversion>Y</lazy_conversion>
      <add_filename_result>N</add_filename_result>
      <parallel>N</parallel>
      <newline_possible>Y</newline_possible>
      <encoding>UTF-8</encoding>
      <fields>
{field_xml}      </fields>
"""
    return step_wrap(name, "CsvInput", config, x, y)


def table_output_step(name, table, fields, x, y):
    field_xml = "".join(
        f"""        <field>
          <column_name>{esc(c)}</column_name>
          <stream_name>{esc(s)}</stream_name>
        </field>\n"""
        for c, s in fields
    )
    config = f"""      <connection>{CONN_NAME}</connection>
      <schema/>
      <table>{esc(table)}</table>
      <commit>1000</commit>
      <truncate_table>N</truncate_table>
      <ignore_errors>N</ignore_errors>
      <use_batch>Y</use_batch>
      <specify_fields>Y</specify_fields>
      <partitioning_enabled>N</partitioning_enabled>
      <partitioning_field/>
      <partitioning_daily>N</partitioning_daily>
      <partitioning_monthly>Y</partitioning_monthly>
      <tablename_in_field>N</tablename_in_field>
      <tablename_field/>
      <tablename_in_table>Y</tablename_in_table>
      <return_keys>N</return_keys>
      <return_field/>
      <fields>
{field_xml}      </fields>
"""
    return step_wrap(name, "TableOutput", config, x, y)


def table_input_step(name, sql, x, y):
    config = f"""      <connection>{CONN_NAME}</connection>
      <sql>{esc(sql)}</sql>
      <limit>0</limit>
      <lookup/>
      <execute_each_row>N</execute_each_row>
      <variables_active>N</variables_active>
      <lazy_conversion_active>Y</lazy_conversion_active>
"""
    return step_wrap(name, "TableInput", config, x, y)


def dblookup_step(name, table, key_name, key_field, value_name, rename, x, y):
    config = f"""      <connection>{CONN_NAME}</connection>
      <schema/>
      <table>{esc(table)}</table>
      <use_schema>N</use_schema>
      <ignore_flag_field/>
      <lookup>
        <key>
          <name>{esc(key_name)}</name>
          <field>{esc(key_field)}</field>
          <condition>=</condition>
          <name2/>
        </key>
      </lookup>
      <value>
        <name>{esc(value_name)}</name>
        <rename>{esc(rename)}</rename>
        <default/>
        <type>Integer</type>
      </value>
      <not_found/>
      <fail_on_multiple>N</fail_on_multiple>
      <order_by/>
      <cache_size>0</cache_size>
      <cached>N</cached>
      <loading_all_data_in_memory>N</loading_all_data_in_memory>
"""
    return step_wrap(name, "DBLookup", config, x, y)


def insert_update_step(name, table, lookup_keys, update_fields, all_fields, x, y):
    lookup_xml = "".join(
        f"""        <key>
          <name>{esc(kn)}</name>
          <field>{esc(kf)}</field>
          <condition>=</condition>
          <name2/>
        </key>\n"""
        for kn, kf in lookup_keys
    )
    update_xml = "".join(
        f"""        <key>
          <name>{esc(kn)}</name>
          <field>{esc(kf)}</field>
        </key>\n"""
        for kn, kf in update_fields
    )
    field_xml = "".join(
        f"""        <field>
          <column_name>{esc(c)}</column_name>
          <stream_name>{esc(s)}</stream_name>
          <update>{upd}</update>
        </field>\n"""
        for c, s, upd in all_fields
    )
    config = f"""      <connection>{CONN_NAME}</connection>
      <schema/>
      <table>{esc(table)}</table>
      <commit>1000</commit>
      <update_bypassed>N</update_bypassed>
      <lookup>
{lookup_xml}      </lookup>
      <update>
{update_xml}      </update>
      <fields>
{field_xml}      </fields>
      <error_ignored>N</error_ignored>
      <ignore_flag_field/>
      <skip_lookup>N</skip_lookup>
"""
    return step_wrap(name, "InsertUpdate", config, x, y)


def write_ktr(name, description, parameters, steps, hops):
    steps_xml = "\n".join(steps)
    hops_xml = "\n".join(
        f"    <hop><from>{esc(a)}</from><to>{esc(b)}</to><enabled>Y</enabled></hop>" for a, b in hops
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<transformation>
{info_block(name, description, parameters)}  <notepads/>
{connection_block()}  <order>
{hops_xml}
  </order>
{steps_xml}  <step_error_handling/>
  <slave-step-copy-partition-distribution/>
  <slave_transformation>N</slave_transformation>
</transformation>
"""
    with open(os.path.join(OUT, name + ".ktr"), "w", encoding="utf-8") as fh:
        fh.write(xml)
    print("gerado:", os.path.join(OUT, name + ".ktr"))


# ---------------------------------------------------------------- definições de campos

JOB_BANK_FIELDS = [
    "noc_cnp", "noc_title_eng", "noc_title_fra", "prov", "er_code_code_re", "er_name",
    "nom_re", "low_wage_salaire_minium", "median_wage_salaire_median",
    "high_wage_salaire_maximal", "average_wage_salaire_moyen",
    "quartile1_wage_sal_quart1", "quartile3_wage_sal_quart3", "source2025_nhq",
    "data_source_e", "data_source_f", "reference_period", "revision_date_date_rev",
    "annual_wage_flag_annuel", "wage_comment_e", "wage_comment_f",
    "emp_nonwage_benefit_pct",
]

HABITACAO_FIELDS = [
    "ref_date", "geo", "dguid", "census_year_2", "housing_indicators_9", "coordinate",
    "tenure_total_1", "tenure_total_1_symbol", "tenure_owner_2", "tenure_owner_2_symbol",
    "tenure_renter_3", "tenure_renter_3_symbol", "tenure_gov_4", "tenure_gov_4_symbol",
]

IMIGRACAO_FIELDS = [
    "ref_date", "geo", "dguid", "age_8d", "gender_3", "place_of_birth_290", "coordinate",
    "total_status_1", "total_status_1_symbol", "non_immigrants_2", "non_immigrants_2_symbol",
    "immigrants_3", "immigrants_3_symbol", "before_1980_4", "before_1980_4_symbol",
    "from_1980_to_1990_5", "from_1980_to_1990_5_symbol", "from_1991_to_2000_6",
    "from_1991_to_2000_6_symbol", "from_2001_to_2010_7", "from_2001_to_2010_7_symbol",
    "from_2011_to_2021_8", "from_2011_to_2021_8_symbol", "from_2011_to_2015_9",
    "from_2011_to_2015_9_symbol", "from_2016_to_2021_10", "from_2016_to_2021_10_symbol",
    "non_perm_resid_11", "non_perm_resid_11_symbol",
]

DGUID_IN = ", ".join(f"'{d}'" for d in [
    "2021A000248", "2021A000259", "2021A000246", "2021A000213", "2021A000210",
    "2021A000261", "2021A000212", "2021A000262", "2021A000235", "2021A000211",
    "2021A000224", "2021A000247", "2021A000260",
])

os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- STAGING

write_ktr(
    "TR_STG_JOB_BANK",
    "Staging: le o CSV bruto do Job Bank/ESDC (44.376 registros, 22 colunas) e grava em stg_job_bank_wages.",
    [("RAW_DIR", "raw", "Diretorio com os CSVs brutos (raw/)")],
    [
        csv_input_step("CSV Job Bank", "${RAW_DIR}/job_bank_wages_2025.csv", JOB_BANK_FIELDS, 100, 100),
        table_output_step("Grava stg_job_bank_wages", "stg_job_bank_wages",
                          [(f, f) for f in JOB_BANK_FIELDS], 320, 100),
    ],
    [("CSV Job Bank", "Grava stg_job_bank_wages")],
)

write_ktr(
    "TR_STG_HABITACAO",
    "Staging: le o CSV bruto do Statistics Canada 98-10-0258-01 (2.990 registros, 14 colunas) e grava em stg_statcan_habitacao.",
    [("RAW_DIR", "raw", "Diretorio com os CSVs brutos (raw/)")],
    [
        csv_input_step("CSV Habitacao", "${RAW_DIR}/98100258_extracted/98100258.csv", HABITACAO_FIELDS, 100, 100),
        table_output_step("Grava stg_statcan_habitacao", "stg_statcan_habitacao",
                          [(f, f) for f in HABITACAO_FIELDS], 320, 100),
    ],
    [("CSV Habitacao", "Grava stg_statcan_habitacao")],
)

write_ktr(
    "TR_STG_IMIGRACAO",
    "Staging: le o CSV extraido do Statistics Canada 98-10-0307-01 (tabela completa) e grava em stg_statcan_imigracao.",
    [("IMIGRACAO_CSV", "raw/98100307_extracted/98100307.csv",
      "Caminho do CSV extraido do ZIP 98100307-eng.zip (383 MB)")],
    [
        csv_input_step("CSV Imigracao", "${IMIGRACAO_CSV}", IMIGRACAO_FIELDS, 100, 100),
        table_output_step("Grava stg_statcan_imigracao", "stg_statcan_imigracao",
                          [(f, f) for f in IMIGRACAO_FIELDS], 320, 100),
    ],
    [("CSV Imigracao", "Grava stg_statcan_imigracao")],
)

# ---------------------------------------------------------------- DIMENSÕES

write_ktr(
    "TR_DIM_PROVINCIA",
    "Dimensao: extrai as 13 provincias/territorios do staging de imigracao e grava em dim_provincia (idempotente pela DGUID).",
    None,
    [
        table_input_step("Le provincias", f"""
SELECT DISTINCT
  i.dguid AS cd_dguid,
  i.geo AS nm_provincia,
  CASE i.dguid
    WHEN '2021A000248' THEN 'AB'
    WHEN '2021A000259' THEN 'BC'
    WHEN '2021A000246' THEN 'MB'
    WHEN '2021A000213' THEN 'NB'
    WHEN '2021A000210' THEN 'NL'
    WHEN '2021A000261' THEN 'NWT'
    WHEN '2021A000212' THEN 'NS'
    WHEN '2021A000262' THEN 'NU'
    WHEN '2021A000235' THEN 'ON'
    WHEN '2021A000211' THEN 'PEI'
    WHEN '2021A000224' THEN 'QC'
    WHEN '2021A000247' THEN 'SK'
    WHEN '2021A000260' THEN 'YK'
  END AS sg_provincia_jobbank,
  'Canada' AS nm_pais
FROM stg_statcan_imigracao i
WHERE i.dguid IN ({DGUID_IN})
""", 100, 100),
        insert_update_step(
            "Grava dim_provincia", "dim_provincia",
            [("cd_dguid", "cd_dguid")],
            [("nm_provincia", "nm_provincia"),
             ("sg_provincia_jobbank", "sg_provincia_jobbank"),
             ("nm_pais", "nm_pais")],
            [("cd_dguid", "cd_dguid", "N"),
             ("nm_provincia", "nm_provincia", "Y"),
             ("sg_provincia_jobbank", "sg_provincia_jobbank", "Y"),
             ("nm_pais", "nm_pais", "Y")],
            320, 100,
        ),
    ],
    [("Le provincias", "Grava dim_provincia")],
)

write_ktr(
    "TR_DIM_OCUPACAO",
    "Dimensao: extrai a ocupacao NOC 21232 do staging de salarios e grava em dim_ocupacao.",
    None,
    [
        table_input_step("Le ocupacao", """
SELECT DISTINCT
  noc_cnp AS cd_noc,
  noc_title_eng AS nm_ocupacao_en,
  noc_title_fra AS nm_ocupacao_fr
FROM stg_job_bank_wages
WHERE noc_cnp = 'NOC_21232'
""", 100, 100),
        insert_update_step(
            "Grava dim_ocupacao", "dim_ocupacao",
            [("cd_noc", "cd_noc")],
            [("nm_ocupacao_en", "nm_ocupacao_en"), ("nm_ocupacao_fr", "nm_ocupacao_fr")],
            [("cd_noc", "cd_noc", "N"),
             ("nm_ocupacao_en", "nm_ocupacao_en", "Y"),
             ("nm_ocupacao_fr", "nm_ocupacao_fr", "Y")],
            320, 100,
        ),
    ],
    [("Le ocupacao", "Grava dim_ocupacao")],
)

write_ktr(
    "TR_DIM_TEMPO_SALARIO",
    "Dimensao: extrai o periodo de referencia salarial 2023-2024 e grava em dim_tempo_salario.",
    None,
    [
        table_input_step("Le periodo salarial", """
SELECT DISTINCT
  reference_period AS cd_periodo_referencia,
  TO_NUMBER(SUBSTR(reference_period, 1, 4)) AS nr_ano_inicio,
  TO_NUMBER(SUBSTR(reference_period, 6, 4)) AS nr_ano_fim,
  reference_period AS ds_periodo
FROM stg_job_bank_wages
WHERE reference_period = '2023-2024'
""", 100, 100),
        insert_update_step(
            "Grava dim_tempo_salario", "dim_tempo_salario",
            [("cd_periodo_referencia", "cd_periodo_referencia")],
            [("nr_ano_inicio", "nr_ano_inicio"), ("nr_ano_fim", "nr_ano_fim"),
             ("ds_periodo", "ds_periodo")],
            [("cd_periodo_referencia", "cd_periodo_referencia", "N"),
             ("nr_ano_inicio", "nr_ano_inicio", "Y"),
             ("nr_ano_fim", "nr_ano_fim", "Y"),
             ("ds_periodo", "ds_periodo", "Y")],
            320, 100,
        ),
    ],
    [("Le periodo salarial", "Grava dim_tempo_salario")],
)

write_ktr(
    "TR_DIM_DISPONIBILIDADE_SALARIO",
    "Dimensao: grava as 3 categorias fixas de cobertura salarial em dim_disponibilidade_salario.",
    None,
    [
        table_input_step("Categorias de cobertura", """
SELECT 'PROVINCIAL_PUBLICADO' AS cd_disponibilidade, 'Salario provincial publicado' AS ds_disponibilidade, 1 AS fl_comparavel_provincial FROM dual
UNION ALL SELECT 'APENAS_REGIONAL', 'Apenas dado regional (PEI - ER1110)', 0 FROM dual
UNION ALL SELECT 'INDISPONIVEL', 'Salario nao publicado para a jurisdicao', 0 FROM dual
""", 100, 100),
        insert_update_step(
            "Grava dim_disponibilidade_salario", "dim_disponibilidade_salario",
            [("cd_disponibilidade", "cd_disponibilidade")],
            [("ds_disponibilidade", "ds_disponibilidade"),
             ("fl_comparavel_provincial", "fl_comparavel_provincial")],
            [("cd_disponibilidade", "cd_disponibilidade", "N"),
             ("ds_disponibilidade", "ds_disponibilidade", "Y"),
             ("fl_comparavel_provincial", "fl_comparavel_provincial", "Y")],
            320, 100,
        ),
    ],
    [("Categorias de cobertura", "Grava dim_disponibilidade_salario")],
)

write_ktr(
    "TR_DIM_TEMPO_CENSO",
    "Dimensao: grava o ano de Censo 2021 em dim_tempo_censo.",
    None,
    [
        table_input_step("Ano de Censo", """
SELECT 2021 AS nr_ano_censo, TO_DATE('2021-05-15','YYYY-MM-DD') AS dt_referencia FROM dual
""", 100, 100),
        insert_update_step(
            "Grava dim_tempo_censo", "dim_tempo_censo",
            [("nr_ano_censo", "nr_ano_censo")],
            [("dt_referencia", "dt_referencia")],
            [("nr_ano_censo", "nr_ano_censo", "N"),
             ("dt_referencia", "dt_referencia", "Y")],
            320, 100,
        ),
    ],
    [("Ano de Censo", "Grava dim_tempo_censo")],
)

write_ktr(
    "TR_DIM_PAIS_NASCIMENTO",
    "Dimensao: extrai Brazil e Total do staging de imigracao e grava em dim_pais_nascimento.",
    None,
    [
        table_input_step("Le paises de nascimento", """
SELECT DISTINCT
  CASE WHEN place_of_birth_290 LIKE 'Brazil%' THEN 'BRA' ELSE 'TOTAL' END AS cd_pais_nascimento,
  CASE WHEN place_of_birth_290 LIKE 'Brazil%' THEN 'Brazil' ELSE 'Total - Place of birth' END AS nm_pais_nascimento
FROM stg_statcan_imigracao
WHERE place_of_birth_290 LIKE 'Brazil%' OR place_of_birth_290 LIKE 'Total%Place of birth%'
""", 100, 100),
        insert_update_step(
            "Grava dim_pais_nascimento", "dim_pais_nascimento",
            [("cd_pais_nascimento", "cd_pais_nascimento")],
            [("nm_pais_nascimento", "nm_pais_nascimento")],
            [("cd_pais_nascimento", "cd_pais_nascimento", "N"),
             ("nm_pais_nascimento", "nm_pais_nascimento", "Y")],
            320, 100,
        ),
    ],
    [("Le paises de nascimento", "Grava dim_pais_nascimento")],
)

write_ktr(
    "TR_DIM_PERIODO_IMIGRACAO",
    "Dimensao: grava os 5 periodos de imigracao ([4]..[8]) em dim_periodo_imigracao.",
    None,
    [
        table_input_step("Periodos de imigracao", """
SELECT '[4]' AS cd_periodo_imigracao, 'Before 1980' AS ds_periodo_imigracao, 1 AS nr_ordem FROM dual
UNION ALL SELECT '[5]', '1980 to 1990', 2 FROM dual
UNION ALL SELECT '[6]', '1991 to 2000', 3 FROM dual
UNION ALL SELECT '[7]', '2001 to 2010', 4 FROM dual
UNION ALL SELECT '[8]', '2011 to 2021', 5 FROM dual
""", 100, 100),
        insert_update_step(
            "Grava dim_periodo_imigracao", "dim_periodo_imigracao",
            [("cd_periodo_imigracao", "cd_periodo_imigracao")],
            [("ds_periodo_imigracao", "ds_periodo_imigracao"), ("nr_ordem", "nr_ordem")],
            [("cd_periodo_imigracao", "cd_periodo_imigracao", "N"),
             ("ds_periodo_imigracao", "ds_periodo_imigracao", "Y"),
             ("nr_ordem", "nr_ordem", "Y")],
            320, 100,
        ),
    ],
    [("Periodos de imigracao", "Grava dim_periodo_imigracao")],
)

write_ktr(
    "TR_DIM_TENENCIA",
    "Dimensao: grava as 4 categorias de posse (tenure) em dim_tenencia.",
    None,
    [
        table_input_step("Categorias de posse", """
SELECT 'TOTAL' AS cd_tenencia, 'Total - Tenure' AS ds_tenencia FROM dual
UNION ALL SELECT 'OWNER', 'Owner' FROM dual
UNION ALL SELECT 'RENTER', 'Renter' FROM dual
UNION ALL SELECT 'GOV', 'Dwelling provided by local government, First Nation or Indian band' FROM dual
""", 100, 100),
        insert_update_step(
            "Grava dim_tenencia", "dim_tenencia",
            [("cd_tenencia", "cd_tenencia")],
            [("ds_tenencia", "ds_tenencia")],
            [("cd_tenencia", "cd_tenencia", "N"),
             ("ds_tenencia", "ds_tenencia", "Y")],
            320, 100,
        ),
    ],
    [("Categorias de posse", "Grava dim_tenencia")],
)

write_ktr(
    "TR_DIM_INDICADOR_HABITACAO",
    "Dimensao: extrai os 9 indicadores habitacionais do staging e grava em dim_indicador_habitacao.",
    None,
    [
        table_input_step("Le indicadores", """
SELECT DISTINCT
  housing_indicators_9 AS cd_indicador_habitacao,
  housing_indicators_9 AS ds_indicador_habitacao,
  CASE WHEN housing_indicators_9 LIKE 'Percent%' THEN 'PERCENTUAL' ELSE 'CONTAGEM' END AS tp_medida
FROM stg_statcan_habitacao
WHERE housing_indicators_9 IS NOT NULL
""", 100, 100),
        insert_update_step(
            "Grava dim_indicador_habitacao", "dim_indicador_habitacao",
            [("cd_indicador_habitacao", "cd_indicador_habitacao")],
            [("ds_indicador_habitacao", "ds_indicador_habitacao"), ("tp_medida", "tp_medida")],
            [("cd_indicador_habitacao", "cd_indicador_habitacao", "N"),
             ("ds_indicador_habitacao", "ds_indicador_habitacao", "Y"),
             ("tp_medida", "tp_medida", "Y")],
            320, 100,
        ),
    ],
    [("Le indicadores", "Grava dim_indicador_habitacao")],
)

write_ktr(
    "TR_DIM_FONTE",
    "Dimensao: grava as 3 fontes institucionais (com URL e data de extracao) em dim_fonte.",
    None,
    [
        table_input_step("Fontes", """
SELECT 'JOB_BANK_2025' AS cd_fonte, 'Job Bank/ESDC Wages' AS nm_fonte, 'https://open.canada.ca/data/en/dataset/adad580f-76b0-4502-bd05-20c125de9116' AS ds_url, DATE '2026-09-14' AS dt_extracao, CAST(NULL AS VARCHAR2(128)) AS ds_checksum FROM dual
UNION ALL SELECT 'STATCAN_0307', 'Statistics Canada - Immigrant status and period of immigration (98-10-0307-01)', 'https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=9810030701', DATE '2026-09-14', CAST(NULL AS VARCHAR2(128)) FROM dual
UNION ALL SELECT 'STATCAN_0258', 'Statistics Canada - Housing indicators by tenure (98-10-0258-01)', 'https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=9810025801', DATE '2026-09-14', CAST(NULL AS VARCHAR2(128)) FROM dual
""", 100, 100),
        insert_update_step(
            "Grava dim_fonte", "dim_fonte",
            [("cd_fonte", "cd_fonte")],
            [("nm_fonte", "nm_fonte"), ("ds_url", "ds_url"),
             ("dt_extracao", "dt_extracao"), ("ds_checksum", "ds_checksum")],
            [("cd_fonte", "cd_fonte", "N"),
             ("nm_fonte", "nm_fonte", "Y"),
             ("ds_url", "ds_url", "Y"),
             ("dt_extracao", "dt_extracao", "Y"),
             ("ds_checksum", "ds_checksum", "Y")],
            320, 100,
        ),
    ],
    [("Fontes", "Grava dim_fonte")],
)

# ---------------------------------------------------------------- FATOS

FATO_SALARIO_SQL = f"""
SELECT
  b.cd_dguid,
  'NOC_21232' AS cd_noc,
  '2023-2024' AS cd_periodo_referencia,
  b.cd_disponibilidade,
  'JOB_BANK_2025' AS cd_fonte,
  TO_NUMBER(w.low_wage_salaire_minium) AS vl_salario_minimo,
  TO_NUMBER(w.median_wage_salaire_median) AS vl_salario_mediano,
  TO_NUMBER(w.high_wage_salaire_maximal) AS vl_salario_maximo,
  TO_NUMBER(w.average_wage_salaire_moyen) AS vl_salario_medio,
  TO_NUMBER(w.quartile1_wage_sal_quart1) AS vl_quartil1,
  TO_NUMBER(w.quartile3_wage_sal_quart3) AS vl_quartil3,
  TO_NUMBER(w.high_wage_salaire_maximal) - TO_NUMBER(w.low_wage_salaire_minium) AS vl_amplitude_salarial,
  CASE WHEN w.annual_wage_flag_annuel = '1' THEN 1 ELSE 0 END AS fl_salario_anual,
  w.er_code_code_re AS cd_regiao_origem,
  w.er_name AS nm_regiao_origem
FROM (
  SELECT cd_dguid, sg_provincia_jobbank,
    CASE
      WHEN sg_provincia_jobbank IN ('YK','NWT','NU') THEN 'INDISPONIVEL'
      WHEN sg_provincia_jobbank = 'PEI' THEN 'APENAS_REGIONAL'
      ELSE 'PROVINCIAL_PUBLICADO'
    END AS cd_disponibilidade
  FROM dim_provincia
) b
LEFT JOIN stg_job_bank_wages w
  ON w.noc_cnp = 'NOC_21232'
 AND w.reference_period = '2023-2024'
 AND (
       (b.cd_disponibilidade = 'PROVINCIAL_PUBLICADO' AND w.prov = b.sg_provincia_jobbank AND LENGTH(w.er_code_code_re) = 4)
    OR (b.cd_disponibilidade = 'APENAS_REGIONAL' AND w.prov = b.sg_provincia_jobbank AND w.er_code_code_re = 'ER1110')
 )
"""

write_ktr(
    "TR_FATO_SALARIO",
    "Fato: 13 jurisdicoes x NOC 21232 x 2023-2024 -> fato_salario (lookup das SKs e Insert/Update pela PK composta).",
    None,
    [
        table_input_step("Le salarios", FATO_SALARIO_SQL, 100, 120),
        dblookup_step("Lookup provincia", "dim_provincia", "cd_dguid", "cd_dguid",
                      "sk_provincia", "sk_provincia", 340, 40),
        dblookup_step("Lookup ocupacao", "dim_ocupacao", "cd_noc", "cd_noc",
                      "sk_ocupacao", "sk_ocupacao", 340, 100),
        dblookup_step("Lookup tempo", "dim_tempo_salario", "cd_periodo_referencia",
                      "cd_periodo_referencia", "sk_tempo_salario", "sk_tempo_salario", 340, 160),
        dblookup_step("Lookup disponibilidade", "dim_disponibilidade_salario",
                      "cd_disponibilidade", "cd_disponibilidade",
                      "sk_disponibilidade_salario", "sk_disponibilidade_salario", 340, 220),
        dblookup_step("Lookup fonte", "dim_fonte", "cd_fonte", "cd_fonte",
                      "sk_fonte", "sk_fonte", 340, 280),
        insert_update_step(
            "Grava fato_salario", "fato_salario",
            [("sk_provincia", "sk_provincia"),
             ("sk_ocupacao", "sk_ocupacao"),
             ("sk_tempo_salario", "sk_tempo_salario")],
            [("sk_disponibilidade_salario", "sk_disponibilidade_salario"),
             ("sk_fonte", "sk_fonte"),
             ("vl_salario_minimo", "vl_salario_minimo"),
             ("vl_salario_mediano", "vl_salario_mediano"),
             ("vl_salario_maximo", "vl_salario_maximo"),
             ("vl_salario_medio", "vl_salario_medio"),
             ("vl_quartil1", "vl_quartil1"),
             ("vl_quartil3", "vl_quartil3"),
             ("vl_amplitude_salarial", "vl_amplitude_salarial"),
             ("fl_salario_anual", "fl_salario_anual"),
             ("cd_regiao_origem", "cd_regiao_origem"),
             ("nm_regiao_origem", "nm_regiao_origem")],
            [("sk_provincia", "sk_provincia", "N"),
             ("sk_ocupacao", "sk_ocupacao", "N"),
             ("sk_tempo_salario", "sk_tempo_salario", "N"),
             ("sk_disponibilidade_salario", "sk_disponibilidade_salario", "Y"),
             ("sk_fonte", "sk_fonte", "Y"),
             ("vl_salario_minimo", "vl_salario_minimo", "Y"),
             ("vl_salario_mediano", "vl_salario_mediano", "Y"),
             ("vl_salario_maximo", "vl_salario_maximo", "Y"),
             ("vl_salario_medio", "vl_salario_medio", "Y"),
             ("vl_quartil1", "vl_quartil1", "Y"),
             ("vl_quartil3", "vl_quartil3", "Y"),
             ("vl_amplitude_salarial", "vl_amplitude_salarial", "Y"),
             ("fl_salario_anual", "fl_salario_anual", "Y"),
             ("cd_regiao_origem", "cd_regiao_origem", "Y"),
             ("nm_regiao_origem", "nm_regiao_origem", "Y")],
            600, 120,
        ),
    ],
    [("Le salarios", "Lookup provincia"), ("Le salarios", "Lookup ocupacao"),
     ("Le salarios", "Lookup tempo"), ("Le salarios", "Lookup disponibilidade"),
     ("Le salarios", "Lookup fonte"),
     ("Lookup provincia", "Grava fato_salario"), ("Lookup ocupacao", "Grava fato_salario"),
     ("Lookup tempo", "Grava fato_salario"), ("Lookup disponibilidade", "Grava fato_salario"),
     ("Lookup fonte", "Grava fato_salario")],
)

FATO_IMIGRACAO_SQL = """
SELECT
  i.dguid AS cd_dguid,
  CASE WHEN i.place_of_birth_290 LIKE 'Brazil%' THEN 'BRA' ELSE 'TOTAL' END AS cd_pais_nascimento,
  u.periodo AS cd_periodo_imigracao,
  2021 AS nr_ano_censo,
  'STATCAN_0307' AS cd_fonte,
  TO_NUMBER(REPLACE(u.qt, ',', '')) AS qt_imigrantes
FROM stg_statcan_imigracao i
UNPIVOT (qt FOR periodo IN (
  before_1980_4 AS '[4]',
  from_1980_to_1990_5 AS '[5]',
  from_1991_to_2000_6 AS '[6]',
  from_2001_to_2010_7 AS '[7]',
  from_2011_to_2021_8 AS '[8]'
)) u
WHERE i.dguid IN (SELECT cd_dguid FROM dim_provincia)
  AND i.age_8d LIKE 'Total%'
  AND i.gender_3 LIKE 'Total%'
  AND (i.place_of_birth_290 LIKE 'Brazil%' OR i.place_of_birth_290 LIKE 'Total%Place of birth%')
"""

write_ktr(
    "TR_FATO_IMIGRACAO",
    "Fato: 13 provincias x 2 paises x 5 periodos -> fato_imigracao (UNPIVOT dos periodos [4]..[8]; Insert/Update pela PK composta).",
    None,
    [
        table_input_step("Le imigracao", FATO_IMIGRACAO_SQL, 100, 120),
        dblookup_step("Lookup provincia", "dim_provincia", "cd_dguid", "cd_dguid",
                      "sk_provincia", "sk_provincia", 340, 40),
        dblookup_step("Lookup pais", "dim_pais_nascimento", "cd_pais_nascimento",
                      "cd_pais_nascimento", "sk_pais_nascimento", "sk_pais_nascimento", 340, 100),
        dblookup_step("Lookup periodo", "dim_periodo_imigracao", "cd_periodo_imigracao",
                      "cd_periodo_imigracao", "sk_periodo_imigracao", "sk_periodo_imigracao", 340, 160),
        dblookup_step("Lookup tempo censo", "dim_tempo_censo", "nr_ano_censo",
                      "nr_ano_censo", "sk_tempo_censo", "sk_tempo_censo", 340, 220),
        dblookup_step("Lookup fonte", "dim_fonte", "cd_fonte", "cd_fonte",
                      "sk_fonte", "sk_fonte", 340, 280),
        insert_update_step(
            "Grava fato_imigracao", "fato_imigracao",
            [("sk_provincia", "sk_provincia"),
             ("sk_pais_nascimento", "sk_pais_nascimento"),
             ("sk_periodo_imigracao", "sk_periodo_imigracao"),
             ("sk_tempo_censo", "sk_tempo_censo")],
            [("sk_fonte", "sk_fonte"), ("qt_imigrantes", "qt_imigrantes")],
            [("sk_provincia", "sk_provincia", "N"),
             ("sk_pais_nascimento", "sk_pais_nascimento", "N"),
             ("sk_periodo_imigracao", "sk_periodo_imigracao", "N"),
             ("sk_tempo_censo", "sk_tempo_censo", "N"),
             ("sk_fonte", "sk_fonte", "Y"),
             ("qt_imigrantes", "qt_imigrantes", "Y")],
            600, 120,
        ),
    ],
    [("Le imigracao", "Lookup provincia"), ("Le imigracao", "Lookup pais"),
     ("Le imigracao", "Lookup periodo"), ("Le imigracao", "Lookup tempo censo"),
     ("Le imigracao", "Lookup fonte"),
     ("Lookup provincia", "Grava fato_imigracao"), ("Lookup pais", "Grava fato_imigracao"),
     ("Lookup periodo", "Grava fato_imigracao"), ("Lookup tempo censo", "Grava fato_imigracao"),
     ("Lookup fonte", "Grava fato_imigracao")],
)

FATO_HABITACAO_SQL = """
SELECT
  i.dguid AS cd_dguid,
  u.tenencia AS cd_tenencia,
  i.housing_indicators_9 AS cd_indicador_habitacao,
  2021 AS nr_ano_censo,
  'STATCAN_0258' AS cd_fonte,
  TO_NUMBER(REPLACE(u.vl, ',', '')) AS vl_medida
FROM stg_statcan_habitacao i
UNPIVOT (vl FOR tenencia IN (
  tenure_total_1 AS 'TOTAL',
  tenure_owner_2 AS 'OWNER',
  tenure_renter_3 AS 'RENTER',
  tenure_gov_4 AS 'GOV'
)) u
WHERE i.dguid IN (SELECT cd_dguid FROM dim_provincia)
  AND i.census_year_2 = '2021'
"""

write_ktr(
    "TR_FATO_HABITACAO",
    "Fato: 13 provincias x 4 posses x 9 indicadores -> fato_habitacao (UNPIVOT das posses; Insert/Update pela PK composta).",
    None,
    [
        table_input_step("Le habitacao", FATO_HABITACAO_SQL, 100, 120),
        dblookup_step("Lookup provincia", "dim_provincia", "cd_dguid", "cd_dguid",
                      "sk_provincia", "sk_provincia", 340, 40),
        dblookup_step("Lookup tenencia", "dim_tenencia", "cd_tenencia",
                      "cd_tenencia", "sk_tenencia", "sk_tenencia", 340, 100),
        dblookup_step("Lookup indicador", "dim_indicador_habitacao",
                      "cd_indicador_habitacao", "cd_indicador_habitacao",
                      "sk_indicador_habitacao", "sk_indicador_habitacao", 340, 160),
        dblookup_step("Lookup tempo censo", "dim_tempo_censo", "nr_ano_censo",
                      "nr_ano_censo", "sk_tempo_censo", "sk_tempo_censo", 340, 220),
        dblookup_step("Lookup fonte", "dim_fonte", "cd_fonte", "cd_fonte",
                      "sk_fonte", "sk_fonte", 340, 280),
        insert_update_step(
            "Grava fato_habitacao", "fato_habitacao",
            [("sk_provincia", "sk_provincia"),
             ("sk_tenencia", "sk_tenencia"),
             ("sk_indicador_habitacao", "sk_indicador_habitacao"),
             ("sk_tempo_censo", "sk_tempo_censo")],
            [("sk_fonte", "sk_fonte"), ("vl_medida", "vl_medida")],
            [("sk_provincia", "sk_provincia", "N"),
             ("sk_tenencia", "sk_tenencia", "N"),
             ("sk_indicador_habitacao", "sk_indicador_habitacao", "N"),
             ("sk_tempo_censo", "sk_tempo_censo", "N"),
             ("sk_fonte", "sk_fonte", "Y"),
             ("vl_medida", "vl_medida", "Y")],
            600, 120,
        ),
    ],
    [("Le habitacao", "Lookup provincia"), ("Le habitacao", "Lookup tenencia"),
     ("Le habitacao", "Lookup indicador"), ("Le habitacao", "Lookup tempo censo"),
     ("Le habitacao", "Lookup fonte"),
     ("Lookup provincia", "Grava fato_habitacao"), ("Lookup tenencia", "Grava fato_habitacao"),
     ("Lookup indicador", "Grava fato_habitacao"), ("Lookup tempo censo", "Grava fato_habitacao"),
     ("Lookup fonte", "Grava fato_habitacao")],
)

# ---------------------------------------------------------------- JOB

TRANS_SEQUENCE = [
    "TR_STG_JOB_BANK", "TR_STG_IMIGRACAO", "TR_STG_HABITACAO",
    "TR_DIM_PROVINCIA", "TR_DIM_OCUPACAO", "TR_DIM_TEMPO_SALARIO",
    "TR_DIM_DISPONIBILIDADE_SALARIO", "TR_DIM_TEMPO_CENSO", "TR_DIM_PAIS_NASCIMENTO",
    "TR_DIM_PERIODO_IMIGRACAO", "TR_DIM_TENENCIA", "TR_DIM_INDICADOR_HABITACAO",
    "TR_DIM_FONTE",
    "TR_FATO_SALARIO", "TR_FATO_IMIGRACAO", "TR_FATO_HABITACAO",
]


def job_entry(name, stype, extra, x, y):
    return f"""    <entry>
      <name>{esc(name)}</name>
      <type>{stype}</type>
      <description/>
      <launch_in_parallel>N</launch_in_parallel>
      <parallel>N</parallel>
      <xloc>{x}</xloc>
      <yloc>{y}</yloc>
      <draw>Y</draw>
      <nr>0</nr>
{extra}    </entry>
"""


def trans_entry(name, x, y):
    extra = f"""      <filename>${{Internal.Entry.Current.Directory}}/{name}.ktr</filename>
      <transname>{name}</transname>
      <arg_from_previous>N</arg_from_previous>
      <params_from_previous>N</params_from_previous>
      <exec_per_row>N</exec_per_row>
      <clear_rows>N</clear_rows>
      <clear_files>N</clear_files>
      <set_logfile>N</set_logfile>
      <logfile/>
      <logext/>
      <add_date>N</add_date>
      <add_time>N</add_time>
      <loglevel>Basic</loglevel>
      <cluster>N</cluster>
      <slave_server_name/>
      <set_append_logfile>N</set_append_logfile>
      <wait_until_finished>Y</wait_until_finished>
      <follow_abort_remote>N</follow_abort_remote>
      <create_parent_folder>N</create_parent_folder>
      <logging_remote_work>N</logging_remote_work>
      <parameters/>
"""
    return job_entry(name, "TRANS", extra, x, y)


def special_entry(name, x, y, start=False, dummy=False):
    extra = f"""      <start>{'Y' if start else 'N'}</start>
      <dummy>{'Y' if dummy else 'N'}</dummy>
      <repeat>N</repeat>
      <schedulerType>0</schedulerType>
      <intervalSeconds>0</intervalSeconds>
      <intervalMinutes>60</intervalMinutes>
      <hour>12</hour>
      <minutes>0</minutes>
      <weekDay>1</weekDay>
      <DayOfMonth>1</DayOfMonth>
"""
    return job_entry(name, "SPECIAL", extra, x, y)


entries = [special_entry("START", 100, 100, start=True)]
x = 280
for i, tname in enumerate(TRANS_SEQUENCE):
    entries.append(trans_entry(tname, x, 100 + (i % 2) * 60))
    x += 180
entries.append(special_entry("SUCCESS", x, 100, dummy=True))

hops = []
prev = "START"
for tname in TRANS_SEQUENCE:
    hops.append((prev, tname))
    prev = tname
hops.append((prev, "SUCCESS"))

entries_xml = "\n".join(entries)
hops_xml = "\n".join(
    f"    <hop><from>{esc(a)}</from><to>{esc(b)}</to><enabled>Y</enabled></hop>" for a, b in hops
)

kjb = f"""<?xml version="1.0" encoding="UTF-8"?>
<job>
  <name>JOB_CARGA_DW</name>
  <description>Orquestra a carga completa do DW_CANADA: staging -> dimensoes -> fatos (idempotente).</description>
  <extended_description/>
  <job_version/>
  <job_status>0</job_status>
  <directory>&#x2f;</directory>
  <created_user>-</created_user>
  <created_date>2026/10/18 12:00:00.000</created_date>
  <modified_user>-</modified_user>
  <modified_date>2026/10/18 12:00:00.000</modified_date>
  <parameters>
    <parameter>
      <name>RAW_DIR</name>
      <default_value>raw</default_value>
      <description>Diretorio com os CSVs brutos</description>
    </parameter>
    <parameter>
      <name>IMIGRACAO_CSV</name>
      <default_value>raw/98100307_extracted/98100307.csv</default_value>
      <description>Caminho do CSV extraido do ZIP de imigracao</description>
    </parameter>
  </parameters>
  <connection>
    <name>{CONN_NAME}</name>
    <server>${{DW_HOST}}</server>
    <type>ORACLE</type>
    <access>Native</access>
    <database>${{DW_SID}}</database>
    <port>${{DW_PORT}}</port>
    <username>${{DW_USER}}</username>
    <password>Encrypted </password>
    <servername/>
    <data_tablespace/>
    <index_tablespace/>
    <attributes>
      <attribute><code>PORT_NUMBER</code><attribute>${{DW_PORT}}</attribute></attribute>
      <attribute><code>FORCE_IDENTIFIERS_TO_LOWERCASE</code><attribute>N</attribute></attribute>
      <attribute><code>FORCE_IDENTIFIERS_TO_UPPERCASE</code><attribute>N</attribute></attribute>
      <attribute><code>IS_CLUSTERED</code><attribute>N</attribute></attribute>
      <attribute><code>QUOTE_ALL_FIELDS</code><attribute>N</attribute></attribute>
      <attribute><code>PREFERRED_SCHEMA_NAME</code><attribute></attribute></attribute>
      <attribute><code>SUPPORTS_BOOLEAN_DATA_TYPE</code><attribute>Y</attribute></attribute>
      <attribute><code>SUPPORTS_TIMESTAMP_DATA_TYPE</code><attribute>Y</attribute></attribute>
      <attribute><code>USE_POOLING</code><attribute>N</attribute></attribute>
      <attribute><code>MAXIMUM_POOL_SIZE</code><attribute>10</attribute></attribute>
      <attribute><code>INITIAL_POOL_SIZE</code><attribute>10</attribute></attribute>
      <attribute><code>STREAM_RESULTS</code><attribute>Y</attribute></attribute>
    </attributes>
  </connection>
  <order>
{hops_xml}
  </order>
  <job-log-table>
    <connection/>
    <schema/>
    <table/>
    <size_limit_lines/>
    <interval/>
    <timeout_days/>
  </job-log-table>
  <jobentry-log-table>
    <connection/>
    <schema/>
    <table/>
    <timeout_days/>
  </jobentry-log-table>
  <channel-log-table>
    <connection/>
    <schema/>
    <table/>
    <timeout_days/>
  </channel-log-table>
  <pass_batchid>N</pass_batchid>
  <shared_objects_file/>
  <entries>
{entries_xml}  </entries>
  <attributes/>
</job>
"""

with open(os.path.join(OUT, "JOB_CARGA_DW.kjb"), "w", encoding="utf-8") as fh:
    fh.write(kjb)
print("gerado:", os.path.join(OUT, "JOB_CARGA_DW.kjb"))
