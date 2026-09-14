-- ==============================
-- TABLESPACES
-- ==============================

-- PRÉ-REQUISITO: esta seção deve ser executada por usuário com privilégio DBA
-- (CREATE TABLESPACE). Ajuste os caminhos abaixo ao diretório de datafiles do
-- ambiente Oracle. Depois de criar os tablespaces, o dono do DW precisa de
-- CREATE TABLE, CREATE SEQUENCE, CREATE INDEX e quota em TS_DW_DADOS/TS_DW_INDICES.
DEFINE DW_DATAFILE = 'ts_dw_dados01.dbf'
DEFINE DW_INDEXFILE = 'ts_dw_indices01.dbf'

CREATE TABLESPACE TS_DW_DADOS
    DATAFILE '&DW_DATAFILE' SIZE 200M
    AUTOEXTEND ON NEXT 20M MAXSIZE 2G
    EXTENT MANAGEMENT LOCAL
    SEGMENT SPACE MANAGEMENT AUTO;

CREATE TABLESPACE TS_DW_INDICES
    DATAFILE '&DW_INDEXFILE' SIZE 100M
    AUTOEXTEND ON NEXT 10M MAXSIZE 1G
    EXTENT MANAGEMENT LOCAL
    SEGMENT SPACE MANAGEMENT AUTO;

-- ==============================
-- SEQUENCES
-- ==============================

CREATE SEQUENCE SEQ_DIM_PROVINCIA           START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_DIM_OCUPACAO            START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_DIM_TEMPO_SALARIO       START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_DIM_TEMPO_CENSO         START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_DIM_PAIS_NASCIMENTO     START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_DIM_PERIODO_IMIGRACAO   START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_DIM_TENENCIA            START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_DIM_INDICADOR_HABITACAO START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_DIM_FONTE               START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_FATO_SALARIO            START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_FATO_IMIGRACAO          START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_FATO_HABITACAO          START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

-- ==============================
-- STAGING
-- ==============================

-- 3.1 Job Bank / ESDC Wages (job_bank_wages_2025.csv)
CREATE TABLE stg_job_bank_wages (
    noc_cnp                    VARCHAR2(20),
    noc_title_eng              VARCHAR2(200),
    noc_title_fra              VARCHAR2(200),
    prov                       VARCHAR2(10),
    er_code_code_re            VARCHAR2(10),
    er_name                    VARCHAR2(120),
    nom_re                     VARCHAR2(120),
    low_wage_salaire_minium    VARCHAR2(20),
    median_wage_salaire_median VARCHAR2(20),
    high_wage_salaire_maximal  VARCHAR2(20),
    average_wage_salaire_moyen VARCHAR2(20),
    quartile1_wage_sal_quart1  VARCHAR2(20),
    quartile3_wage_sal_quart3  VARCHAR2(20),
    source2025_nhq             VARCHAR2(80),
    data_source_e              VARCHAR2(200),
    data_source_f              VARCHAR2(200),
    reference_period           VARCHAR2(20),
    revision_date_date_rev     VARCHAR2(20),
    annual_wage_flag_annuel    VARCHAR2(10),
    wage_comment_e             VARCHAR2(500),
    wage_comment_f             VARCHAR2(500),
    emp_nonwage_benefit_pct    VARCHAR2(20)
) TABLESPACE TS_DW_DADOS;

-- 3.2 Statistics Canada — imigração (tabela 98-10-0307-01)
CREATE TABLE stg_statcan_imigracao (
    ref_date                   VARCHAR2(10),
    geo                        VARCHAR2(120),
    dguid                      VARCHAR2(20),
    age_8d                     VARCHAR2(80),
    gender_3                   VARCHAR2(80),
    place_of_birth_290         VARCHAR2(120),
    coordinate                 VARCHAR2(30),
    total_status_1             VARCHAR2(30),
    total_status_1_symbol      VARCHAR2(10),
    non_immigrants_2           VARCHAR2(30),
    non_immigrants_2_symbol    VARCHAR2(10),
    immigrants_3               VARCHAR2(30),
    immigrants_3_symbol        VARCHAR2(10),
    before_1980_4              VARCHAR2(30),
    before_1980_4_symbol       VARCHAR2(10),
    from_1980_to_1990_5        VARCHAR2(30),
    from_1980_to_1990_5_symbol VARCHAR2(10),
    from_1991_to_2000_6        VARCHAR2(30),
    from_1991_to_2000_6_symbol VARCHAR2(10),
    from_2001_to_2010_7        VARCHAR2(30),
    from_2001_to_2010_7_symbol VARCHAR2(10),
    from_2011_to_2021_8        VARCHAR2(30),
    from_2011_to_2021_8_symbol VARCHAR2(10),
    from_2011_to_2015_9        VARCHAR2(30),
    from_2011_to_2015_9_symbol VARCHAR2(10),
    from_2016_to_2021_10       VARCHAR2(30),
    from_2016_to_2021_10_symbol VARCHAR2(10),
    non_perm_resid_11          VARCHAR2(30),
    non_perm_resid_11_symbol   VARCHAR2(10)
) TABLESPACE TS_DW_DADOS;

-- 3.3 Statistics Canada — habitação (tabela 98-10-0258-01)
CREATE TABLE stg_statcan_habitacao (
    ref_date              VARCHAR2(10),
    geo                   VARCHAR2(120),
    dguid                 VARCHAR2(20),
    census_year_2         VARCHAR2(10),
    housing_indicators_9  VARCHAR2(120),
    coordinate            VARCHAR2(30),
    tenure_total_1        VARCHAR2(30),
    tenure_total_1_symbol VARCHAR2(10),
    tenure_owner_2        VARCHAR2(30),
    tenure_owner_2_symbol VARCHAR2(10),
    tenure_renter_3       VARCHAR2(30),
    tenure_renter_3_symbol VARCHAR2(10),
    tenure_gov_4          VARCHAR2(30),
    tenure_gov_4_symbol   VARCHAR2(10)
) TABLESPACE TS_DW_DADOS;

-- ==============================
-- DIMENSÕES
-- ==============================

CREATE TABLE dim_provincia (
    sk_provincia         NUMBER(10)   CONSTRAINT NN_DIM_PROVINCIA_SK        NOT NULL,
    cd_dguid             VARCHAR2(16) CONSTRAINT NN_DIM_PROVINCIA_CD_DGUID NOT NULL,
    nm_provincia         VARCHAR2(60) CONSTRAINT NN_DIM_PROVINCIA_NM       NOT NULL,
    sg_provincia_jobbank VARCHAR2(4),
    nm_pais              VARCHAR2(20),
    CONSTRAINT PK_DIM_PROVINCIA PRIMARY KEY (sk_provincia)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT AK_DIM_PROVINCIA UNIQUE (cd_dguid)
        USING INDEX TABLESPACE TS_DW_INDICES
) TABLESPACE TS_DW_DADOS;

CREATE TABLE dim_ocupacao (
    sk_ocupacao    NUMBER(10)   CONSTRAINT NN_DIM_OCUPACAO_SK     NOT NULL,
    cd_noc         VARCHAR2(12) CONSTRAINT NN_DIM_OCUPACAO_CD_NOC NOT NULL,
    nm_ocupacao_en VARCHAR2(120) CONSTRAINT NN_DIM_OCUPACAO_NM_EN NOT NULL,
    nm_ocupacao_fr VARCHAR2(120),
    CONSTRAINT PK_DIM_OCUPACAO PRIMARY KEY (sk_ocupacao)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT AK_DIM_OCUPACAO UNIQUE (cd_noc)
        USING INDEX TABLESPACE TS_DW_INDICES
) TABLESPACE TS_DW_DADOS;

CREATE TABLE dim_tempo_salario (
    sk_tempo_salario      NUMBER(10)   CONSTRAINT NN_DIM_TEMPO_SALARIO_SK NOT NULL,
    cd_periodo_referencia VARCHAR2(20) CONSTRAINT NN_DIM_TEMPO_SALARIO_CD NOT NULL,
    nr_ano_inicio         NUMBER(4),
    nr_ano_fim            NUMBER(4),
    ds_periodo            VARCHAR2(50),
    CONSTRAINT PK_DIM_TEMPO_SALARIO PRIMARY KEY (sk_tempo_salario)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT AK_DIM_TEMPO_SALARIO UNIQUE (cd_periodo_referencia)
        USING INDEX TABLESPACE TS_DW_INDICES
) TABLESPACE TS_DW_DADOS;

CREATE TABLE dim_tempo_censo (
    sk_tempo_censo NUMBER(10) CONSTRAINT NN_DIM_TEMPO_CENSO_SK  NOT NULL,
    nr_ano_censo   NUMBER(4)  CONSTRAINT NN_DIM_TEMPO_CENSO_ANO NOT NULL,
    dt_referencia  DATE,
    CONSTRAINT PK_DIM_TEMPO_CENSO PRIMARY KEY (sk_tempo_censo)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT AK_DIM_TEMPO_CENSO UNIQUE (nr_ano_censo)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT CK_DIM_TEMPO_CENSO_ANO CHECK (nr_ano_censo BETWEEN 2000 AND 2100)
) TABLESPACE TS_DW_DADOS;

CREATE TABLE dim_pais_nascimento (
    sk_pais_nascimento NUMBER(10)  CONSTRAINT NN_DIM_PAIS_NASCIMENTO_SK NOT NULL,
    cd_pais_nascimento VARCHAR2(30) CONSTRAINT NN_DIM_PAIS_NASCIMENTO_CD NOT NULL,
    nm_pais_nascimento VARCHAR2(80) CONSTRAINT NN_DIM_PAIS_NASCIMENTO_NM NOT NULL,
    CONSTRAINT PK_DIM_PAIS_NASCIMENTO PRIMARY KEY (sk_pais_nascimento)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT AK_DIM_PAIS_NASCIMENTO UNIQUE (cd_pais_nascimento)
        USING INDEX TABLESPACE TS_DW_INDICES
) TABLESPACE TS_DW_DADOS;

CREATE TABLE dim_periodo_imigracao (
    sk_periodo_imigracao NUMBER(10)  CONSTRAINT NN_DIM_PERIODO_IMIGRACAO_SK NOT NULL,
    cd_periodo_imigracao VARCHAR2(20) CONSTRAINT NN_DIM_PERIODO_IMIGRACAO_CD NOT NULL,
    ds_periodo_imigracao VARCHAR2(40) CONSTRAINT NN_DIM_PERIODO_IMIGRACAO_DS NOT NULL,
    nr_ordem            NUMBER(2),
    CONSTRAINT PK_DIM_PERIODO_IMIGRACAO PRIMARY KEY (sk_periodo_imigracao)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT AK_DIM_PERIODO_IMIGRACAO UNIQUE (cd_periodo_imigracao)
        USING INDEX TABLESPACE TS_DW_INDICES
) TABLESPACE TS_DW_DADOS;

CREATE TABLE dim_tenencia (
    sk_tenencia NUMBER(10)  CONSTRAINT NN_DIM_TENENCIA_SK NOT NULL,
    cd_tenencia VARCHAR2(10) CONSTRAINT NN_DIM_TENENCIA_CD NOT NULL,
    ds_tenencia VARCHAR2(60) CONSTRAINT NN_DIM_TENENCIA_DS NOT NULL,
    CONSTRAINT PK_DIM_TENENCIA PRIMARY KEY (sk_tenencia)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT AK_DIM_TENENCIA UNIQUE (cd_tenencia)
        USING INDEX TABLESPACE TS_DW_INDICES
) TABLESPACE TS_DW_DADOS;

CREATE TABLE dim_indicador_habitacao (
    sk_indicador_habitacao NUMBER(10)   CONSTRAINT NN_DIM_INDICADOR_HABITACAO_SK NOT NULL,
    cd_indicador_habitacao VARCHAR2(60) CONSTRAINT NN_DIM_INDICADOR_HABITACAO_CD NOT NULL,
    ds_indicador_habitacao VARCHAR2(120),
    tp_medida              VARCHAR2(10),
    CONSTRAINT PK_DIM_INDICADOR_HABITACAO PRIMARY KEY (sk_indicador_habitacao)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT AK_DIM_INDICADOR_HABITACAO UNIQUE (cd_indicador_habitacao)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT CK_DIM_INDICADOR_HABITACAO_TP CHECK (tp_medida IN ('CONTAGEM', 'PERCENTUAL'))
) TABLESPACE TS_DW_DADOS;

CREATE TABLE dim_fonte (
    sk_fonte    NUMBER(10)   CONSTRAINT NN_DIM_FONTE_SK NOT NULL,
    cd_fonte    VARCHAR2(20) CONSTRAINT NN_DIM_FONTE_CD NOT NULL,
    nm_fonte    VARCHAR2(120) CONSTRAINT NN_DIM_FONTE_NM NOT NULL,
    ds_url      VARCHAR2(500),
    dt_extracao DATE,
    ds_checksum VARCHAR2(128),
    CONSTRAINT PK_DIM_FONTE PRIMARY KEY (sk_fonte)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT AK_DIM_FONTE UNIQUE (cd_fonte)
        USING INDEX TABLESPACE TS_DW_INDICES
) TABLESPACE TS_DW_DADOS;

-- ==============================
-- FATOS
-- ==============================

CREATE TABLE fato_salario (
    sk_fato_salario       NUMBER(15)    CONSTRAINT NN_FATO_SALARIO_SK NOT NULL,
    sk_provincia          NUMBER(10)    CONSTRAINT NN_FATO_SALARIO_SK_PROVINCIA NOT NULL,
    sk_ocupacao           NUMBER(10)    CONSTRAINT NN_FATO_SALARIO_SK_OCUPACAO NOT NULL,
    sk_tempo_salario      NUMBER(10)    CONSTRAINT NN_FATO_SALARIO_SK_TEMPO NOT NULL,
    sk_fonte              NUMBER(10)    CONSTRAINT NN_FATO_SALARIO_SK_FONTE NOT NULL,
    vl_salario_minimo     NUMBER(10,2),
    vl_salario_mediano    NUMBER(10,2),
    vl_salario_maximo     NUMBER(10,2),
    vl_salario_medio      NUMBER(10,2),
    vl_quartil1           NUMBER(10,2),
    vl_quartil3           NUMBER(10,2),
    vl_amplitude_salarial NUMBER(10,2),
    fl_salario_anual      NUMBER(1),
    CONSTRAINT PK_FATO_SALARIO PRIMARY KEY (sk_fato_salario)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT AK_FATO_SALARIO UNIQUE (sk_provincia, sk_ocupacao, sk_tempo_salario)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT FK_FATO_SAL_DIM_PROVINCIA FOREIGN KEY (sk_provincia)
        REFERENCES dim_provincia (sk_provincia),
    CONSTRAINT FK_FATO_SAL_DIM_OCUPACAO FOREIGN KEY (sk_ocupacao)
        REFERENCES dim_ocupacao (sk_ocupacao),
    CONSTRAINT FK_FATO_SAL_DIM_TEMPO_SAL FOREIGN KEY (sk_tempo_salario)
        REFERENCES dim_tempo_salario (sk_tempo_salario),
    CONSTRAINT FK_FATO_SAL_DIM_FONTE FOREIGN KEY (sk_fonte)
        REFERENCES dim_fonte (sk_fonte),
    CONSTRAINT CK_FATO_SALARIO_FL_ANUAL CHECK (fl_salario_anual IN (0, 1))
) TABLESPACE TS_DW_DADOS;

CREATE TABLE fato_imigracao (
    sk_fato_imigracao    NUMBER(15) CONSTRAINT NN_FATO_IMIGRACAO_SK NOT NULL,
    sk_provincia         NUMBER(10) CONSTRAINT NN_FATO_IMIGRACAO_SK_PROVINCIA NOT NULL,
    sk_pais_nascimento   NUMBER(10) CONSTRAINT NN_FATO_IMIGRACAO_SK_PAIS NOT NULL,
    sk_periodo_imigracao NUMBER(10) CONSTRAINT NN_FATO_IMIGRACAO_SK_PERIODO NOT NULL,
    sk_tempo_censo       NUMBER(10) CONSTRAINT NN_FATO_IMIGRACAO_SK_TEMPO NOT NULL,
    sk_fonte             NUMBER(10) CONSTRAINT NN_FATO_IMIGRACAO_SK_FONTE NOT NULL,
    qt_imigrantes        NUMBER(12),
    CONSTRAINT PK_FATO_IMIGRACAO PRIMARY KEY (sk_fato_imigracao)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT AK_FATO_IMIGRACAO UNIQUE (sk_provincia, sk_pais_nascimento, sk_periodo_imigracao, sk_tempo_censo)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT FK_FATO_IMIG_DIM_PROVINCIA FOREIGN KEY (sk_provincia)
        REFERENCES dim_provincia (sk_provincia),
    CONSTRAINT FK_FATO_IMIG_DIM_PAIS FOREIGN KEY (sk_pais_nascimento)
        REFERENCES dim_pais_nascimento (sk_pais_nascimento),
    CONSTRAINT FK_FATO_IMIG_DIM_PERIODO FOREIGN KEY (sk_periodo_imigracao)
        REFERENCES dim_periodo_imigracao (sk_periodo_imigracao),
    CONSTRAINT FK_FATO_IMIG_DIM_TEMPO_CENSO FOREIGN KEY (sk_tempo_censo)
        REFERENCES dim_tempo_censo (sk_tempo_censo),
    CONSTRAINT FK_FATO_IMIG_DIM_FONTE FOREIGN KEY (sk_fonte)
        REFERENCES dim_fonte (sk_fonte),
    CONSTRAINT CK_FATO_IMIGRACAO_QT CHECK (qt_imigrantes >= 0)
) TABLESPACE TS_DW_DADOS;

CREATE TABLE fato_habitacao (
    sk_fato_habitacao      NUMBER(15) CONSTRAINT NN_FATO_HABITACAO_SK NOT NULL,
    sk_provincia           NUMBER(10) CONSTRAINT NN_FATO_HABITACAO_SK_PROVINCIA NOT NULL,
    sk_tenencia            NUMBER(10) CONSTRAINT NN_FATO_HABITACAO_SK_TENENCIA NOT NULL,
    sk_indicador_habitacao NUMBER(10) CONSTRAINT NN_FATO_HABITACAO_SK_INDICADOR NOT NULL,
    sk_tempo_censo         NUMBER(10) CONSTRAINT NN_FATO_HABITACAO_SK_TEMPO NOT NULL,
    sk_fonte               NUMBER(10) CONSTRAINT NN_FATO_HABITACAO_SK_FONTE NOT NULL,
    vl_medida              NUMBER(15,2),
    CONSTRAINT PK_FATO_HABITACAO PRIMARY KEY (sk_fato_habitacao)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT AK_FATO_HABITACAO UNIQUE (sk_provincia, sk_tenencia, sk_indicador_habitacao, sk_tempo_censo)
        USING INDEX TABLESPACE TS_DW_INDICES,
    CONSTRAINT FK_FATO_HAB_DIM_PROVINCIA FOREIGN KEY (sk_provincia)
        REFERENCES dim_provincia (sk_provincia),
    CONSTRAINT FK_FATO_HAB_DIM_TENENCIA FOREIGN KEY (sk_tenencia)
        REFERENCES dim_tenencia (sk_tenencia),
    CONSTRAINT FK_FATO_HAB_DIM_INDICADOR FOREIGN KEY (sk_indicador_habitacao)
        REFERENCES dim_indicador_habitacao (sk_indicador_habitacao),
    CONSTRAINT FK_FATO_HAB_DIM_TEMPO_CENSO FOREIGN KEY (sk_tempo_censo)
        REFERENCES dim_tempo_censo (sk_tempo_censo),
    CONSTRAINT FK_FATO_HAB_DIM_FONTE FOREIGN KEY (sk_fonte)
        REFERENCES dim_fonte (sk_fonte),
    CONSTRAINT CK_FATO_HABITACAO_VL CHECK (vl_medida >= 0)
) TABLESPACE TS_DW_DADOS;

-- ==============================
-- ÍNDICES ADICIONAIS (FKS E FILTROS)
-- ==============================

CREATE INDEX IDX_FATO_SAL_SK_PROVINCIA ON fato_salario (sk_provincia)         TABLESPACE TS_DW_INDICES;
CREATE INDEX IDX_FATO_SAL_SK_OCUPACAO  ON fato_salario (sk_ocupacao)          TABLESPACE TS_DW_INDICES;
CREATE INDEX IDX_FATO_SAL_SK_TEMPO     ON fato_salario (sk_tempo_salario)     TABLESPACE TS_DW_INDICES;

CREATE INDEX IDX_FATO_IMIG_SK_PROVINCIA ON fato_imigracao (sk_provincia)       TABLESPACE TS_DW_INDICES;
CREATE INDEX IDX_FATO_IMIG_SK_PAIS      ON fato_imigracao (sk_pais_nascimento) TABLESPACE TS_DW_INDICES;
CREATE INDEX IDX_FATO_IMIG_SK_PERIODO   ON fato_imigracao (sk_periodo_imigracao) TABLESPACE TS_DW_INDICES;

CREATE INDEX IDX_FATO_HAB_SK_PROVINCIA ON fato_habitacao (sk_provincia)        TABLESPACE TS_DW_INDICES;
CREATE INDEX IDX_FATO_HAB_SK_TENENCIA  ON fato_habitacao (sk_tenencia)         TABLESPACE TS_DW_INDICES;
CREATE INDEX IDX_FATO_HAB_SK_INDICADOR ON fato_habitacao (sk_indicador_habitacao) TABLESPACE TS_DW_INDICES;
