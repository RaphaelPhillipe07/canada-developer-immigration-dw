#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o trabalho escrito (Nota 1) em DOCX no padrão IFAL.

Estrutura e fonte baseadas no documento "APLICATIVO DE ENSINO GAMIFICADO (2)":
capa institucional, folha de rosto, sumário, seções numeradas e fonte
Times New Roman 12 (ABNT).

Uso:
    python tools/apoio_nao_avaliado/gerar_docx.py

Saída:
    docs/dw_canada.docx
"""

import io
import os
import re

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "docs", "dw_canada.docx")

doc = Document()

# ---------------------------------------------------------------- página A4 + margens ABNT
for section in doc.sections:
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

# ---------------------------------------------------------------- fontes padrão IFAL (Times New Roman)
def force_font(style_or_run, name="Arial"):
    rpr = style_or_run.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    rfonts.set(qn("w:ascii"), name)
    rfonts.set(qn("w:hAnsi"), name)
    rfonts.set(qn("w:cs"), name)
    rfonts.set(qn("w:eastAsia"), name)
    # os estilos de título do template herdam a fonte do tema (Calibri Light).
    # sem remover esses atributos, o tema vence o w:ascii e o Word/LibreOffice
    # renderiza Carlito no lugar de Arial.
    for attr in ("asciiTheme", "hAnsiTheme", "cstheme", "eastAsiaTheme"):
        if rfonts.get(qn("w:" + attr)) is not None:
            del rfonts.attrib[qn("w:" + attr)]


normal = doc.styles["Normal"]
normal.font.name = "Arial"
normal.font.size = Pt(12)
normal.font.color.rgb = RGBColor(0, 0, 0)
normal.paragraph_format.line_spacing = 1.5
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
force_font(normal)

for hname in ("Heading 1", "Heading 2", "Heading 3"):
    st = doc.styles[hname]
    st.font.name = "Arial"
    st.font.size = Pt(12)
    # na referência, H1 e H3 são negrito e H2 é regular
    st.font.bold = hname != "Heading 2"
    st.font.italic = False
    st.font.color.rgb = RGBColor(0, 0, 0)
    force_font(st)


def h1(text):
    doc.add_heading(text.upper(), level=1)


def h2(text):
    doc.add_heading(text, level=2)


def h3(text):
    doc.add_heading(text, level=3)


def p(text, bold=False, italic=False, size=12, align=None, space_after=None):
    par = doc.add_paragraph()
    run = par.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.name = "Arial"
    force_font(run)
    if align is not None:
        par.alignment = align
    else:
        par.paragraph_format.first_line_indent = Cm(1.25)
    if space_after is not None:
        par.paragraph_format.space_after = Pt(space_after)
    return par


def center(text, bold=False, size=12, space_after=0):
    return p(text, bold=bold, size=size, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=space_after)


def bullet(text):
    par = doc.add_paragraph(text, style="List Bullet")
    for run in par.runs:
        run.font.name = "Arial"
        run.font.size = Pt(12)
        force_font(run)
    return par


def mono(text):
    par = doc.add_paragraph()
    run = par.add_run(text)
    run.font.name = "Courier New"
    run.font.size = Pt(9)
    force_font(run, "Courier New")
    par.paragraph_format.space_after = Pt(0)
    par.paragraph_format.line_spacing = 1.0
    return par


def table(headers, rows, widths=None, font_size=10):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    hdr = t.rows[0].cells
    for i, htext in enumerate(headers):
        hdr[i].text = ""
        run = hdr[i].paragraphs[0].add_run(htext)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(font_size)
        force_font(run)
    tr_pr = hdr[0]._tc.getparent().get_or_add_trPr()
    header = OxmlElement("w:tblHeader")
    header.set(qn("w:val"), "true")
    tr_pr.append(header)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(str(val))
            run.font.name = "Arial"
            run.font.size = Pt(font_size)
            force_font(run)
        tr_pr = cells[0]._tc.getparent().get_or_add_trPr()
        cant_split = OxmlElement("w:cantSplit")
        tr_pr.append(cant_split)
    if widths:
        for i, w in enumerate(widths):
            for row in t.rows:
                row.cells[i].width = Inches(w)
    doc.add_paragraph()
    return t


def picture(rel):
    diagram = os.path.join(ROOT, "docs", "figuras", rel)
    image_path = diagram if os.path.exists(diagram) else os.path.join(ROOT, "docs", "presentation", "images", rel)
    doc.add_picture(image_path, width=Inches(5.9))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER


def page_break():
    doc.add_page_break()


def add_page_number_footer():
    footer = doc.sections[0].footer
    par = footer.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = par.add_run()
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)
    run.font.name = "Arial"
    run.font.size = Pt(10)
    force_font(run)


def add_toc(entries):
    for title, page in entries:
        par = doc.add_paragraph()
        par.paragraph_format.space_after = Pt(2)
        left = par.add_run(title)
        left.font.name = "Arial"
        left.font.size = Pt(12)
        force_font(left)
        tab = par.add_run("\t")
        tab.font.name = "Arial"
        page_run = par.add_run(str(page))
        page_run.font.name = "Arial"
        page_run.font.size = Pt(12)
        force_font(page_run)
        tabs = par.paragraph_format.tab_stops
        tabs.add_tab_stop(Cm(15.5), 2, 1)


# O documento de referência não numera as páginas; mantemos o mesmo padrão.
# add_page_number_footer()

# ---------------------------------------------------------------- CAPA
def folha(rosto=False):
    """Capa (com logo, tudo em negrito) e folha de rosto (sem logo, regular),
    no mesmo desenho do documento de referência da disciplina."""
    if not rosto:
        logo = os.path.join(ROOT, "docs", "ifal_logo.png")
        if os.path.exists(logo):
            doc.add_picture(logo, width=Cm(2.8))
            par_logo = doc.paragraphs[-1]
            par_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
            par_logo.paragraph_format.space_after = Pt(0)
            # com entrelinha 1,5 herdada do estilo Normal a imagem é recortada
            par_logo.paragraph_format.line_spacing = 1.0
        vazios_topo, vazios_meio, vazios_fim = 2, 7, 11
    else:
        for _ in range(3):
            p("", space_after=0)
        vazios_topo, vazios_meio, vazios_fim = 0, 7, 0

    forte = not rosto           # a capa é toda em negrito; a folha de rosto, regular

    for _ in range(vazios_topo):
        p("", space_after=0)
    center("ELIEZIR MOREIRA PEIXOTO NETO", bold=forte, size=12, space_after=0)
    center("RAPHAEL PHILLIPE DA SILVA SILVERIO", bold=forte, size=12, space_after=0)

    for _ in range(vazios_meio):
        p("", space_after=0)
    center("DATA WAREHOUSE DE OPORTUNIDADES PARA DESENVOLVEDORES", bold=forte, size=12, space_after=0)
    center("IMIGRANTES NO CANADÁ", bold=forte, size=12, space_after=0)

    if rosto:
        for _ in range(6):
            p("", space_after=0)
        nota = p(
            "Trabalho apresentado à Disciplina Tópicos Avançados de Banco de Dados, "
            "ministrada pelo Prof. Luiz Frederico, no Bacharelado em Sistemas de "
            "Informação do Instituto Federal de Alagoas, campus Maceió.",
            size=10, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=0)
        nota.paragraph_format.left_indent = Cm(8)
        nota.paragraph_format.line_spacing = 1.15
        for _ in range(5):
            p("", space_after=0)
    else:
        for _ in range(vazios_fim):
            p("", space_after=0)

    center("MACEIÓ, AL", bold=forte, size=12, space_after=0)
    center("2026", bold=forte, size=12, space_after=0)
    page_break()


folha()
folha(rosto=True)

# ---------------------------------------------------------------- SUMÁRIO
p("SUMÁRIO", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
add_toc([
    ('1 INTRODUÇÃO', 5),
    ('2 OBJETIVOS', 5),
    ('    2.1 META SMART E PERGUNTAS ESTRATÉGICAS', 6),
    ('        2.1.1 Meta SMART', 6),
    ('        2.1.2 Perguntas estratégicas a serem respondidas pelo DW', 6),
    ('        2.1.3 Cobertura das perguntas por fonte', 7),
    ('3 BASES DE DADOS UTILIZADAS', 9),
    ('    3.1 FONTES SELECIONADAS', 9),
    ('        3.1.1 Procedência do ZIP de imigração fora do Git', 9),
    ('    3.2 VOLUMETRIA DAS EXTRAÇÕES', 10),
    ('    3.3 PRÉ-PROCESSAMENTO (ETL) E IMPACTO DAS TRANSFORMAÇÕES', 10),
    ('4 ANÁLISE EXPLORATÓRIA', 13),
    ('    4.1 SALÁRIOS — JOB BANK/ESDC', 13),
    ('    4.2 IMIGRAÇÃO — STATISTICS CANADA', 14),
    ('    4.3 HABITAÇÃO — STATISTICS CANADA', 15),
    ('5 DICIONÁRIO DE DADOS', 18),
    ('    5.1 BASE JOB BANK / ESDC', 18),
    ('    5.2 BASE STATISTICS CANADA — IMIGRAÇÃO (98-10-0307-01)', 19),
    ('    5.3 BASE STATISTICS CANADA — HABITAÇÃO (98-10-0258-01)', 20),
    ('    5.4 DICIONÁRIO DE DADOS DO DATA WAREHOUSE', 21),
    ('        5.4.1 Tabelas Fato', 21),
    ('        5.4.2 Tabelas Dimensão', 23),
    ('        5.4.3 Constraints de relacionamento', 24),
    ('6 MODELAGEM DO DATA WAREHOUSE', 26),
    ('    6.1 MODELO LÓGICO/FÍSICO DO DATA WAREHOUSE', 26),
    ('        6.1.1 Diagrama', 26),
    ('        6.1.2 Dimensões', 26),
    ('        6.1.3 Fatos', 27),
    ('7 ANEXOS', 28),
    ('    7.1 SCRIPT DDL (ORACLE SQL)', 28),
    ('REFERÊNCIAS', 37),
])
page_break()

# ---------------------------------------------------------------- 1 INTRODUÇÃO
h1("1 Introdução")
p("Implantação de um Data Warehouse para análise de oportunidades de desenvolvedores de software imigrantes no Canadá.")

p("O projeto abrange as 13 províncias e territórios canadenses e integra duas fontes institucionais: Statistics Canada e Job Bank/ESDC. Elas fornecem três conjuntos de dados: imigração e habitação do Censo 2021, além de salários de Software Developers and Programmers (NOC 21232), com referência salarial 2023–2024.")

p("Como estruturar um Data Warehouse que integre dados oficiais de imigração, salários e habitação, permitindo comparar as províncias canadenses para apoiar a decisão de desenvolvedores de software imigrantes?")

p("A modelagem dimensional em três esquemas estrela com dimensões conformadas e a preservação das ausências permitem representar os dados necessários para responder às 10 perguntas analíticas sem estimar valores ausentes.")

p("Profissionais de desenvolvimento de software que pretendem imigrar para o Canadá precisam escolher uma província ou território considerando, ao mesmo tempo, remuneração, presença de comunidade brasileira e acessibilidade habitacional. Essas informações estão espalhadas em bases oficiais diferentes — Statistics Canada (Censo 2021) e Job Bank/ESDC — com formatos, períodos e códigos geográficos distintos. O Data Warehouse integra essas fontes e permite comparações consistentes entre as jurisdições.")


# ---------------------------------------------------------------- 2 OBJETIVOS
h1("2 Objetivos")
p("Construir um Data Warehouse em Oracle que integre dados oficiais do Statistics Canada e do Job Bank/ESDC para comparar, entre as províncias e territórios canadenses, a distribuição de imigrantes brasileiros, a remuneração de desenvolvedores de software (NOC 21232) e a acessibilidade habitacional.")

p("Para alcançar esse objetivo geral, o trabalho persegue os seguintes objetivos específicos:")
bullet("Modelar uma constelação de fatos composta por três Star Schemas integrados por dimensões conformadas e surrogate keys.")
bullet("Documentar o dicionário de dados das bases públicas de origem e do Data Warehouse.")
bullet("Realizar a análise exploratória das bases de origem.")
bullet("Justificar e analisar o impacto de toda transformação aplicada aos dados de origem.")
bullet("Elaborar o script SQL de implantação do modelo em Oracle (tablespaces, sequences, constraints e índices).")
bullet("Definir as 10 perguntas analíticas que o Data Warehouse deverá responder.")

h2("2.1 META SMART E PERGUNTAS ESTRATÉGICAS")
h3("2.1.1 Meta SMART")
table(
    ["Componente", "Descrição"],
    [
        ("S — Específica", "Construir um DW em Oracle com dados oficiais de imigração, salários e habitação."),
        ("M — Mensurável", "Integrar os três conjuntos de dados em um modelo dimensional capaz de responder às 10 perguntas analíticas definidas, contemplando as 13 províncias e territórios canadenses sempre que houver dados disponíveis na fonte."),
        ("A — Atingível", "Duas fontes institucionais e três conjuntos de dados, já baixados e filtrados, com modelo viável em Oracle."),
        ("R — Relevante", "Apoiar a decisão de desenvolvedores de software imigrantes sobre a melhor província canadense."),
        ("T — Temporal", "Até 14 de dezembro de 2026."),
    ],
    widths=[1.6, 4.9],
)

h3("2.1.2 Perguntas estratégicas a serem respondidas pelo DW")
p("As perguntas foram definidas priorizando o cruzamento entre fontes: sete das dez só podem ser respondidas combinando duas ou três bases. Esse é o argumento central do projeto — nenhuma das fontes, isoladamente, responde a essas perguntas, e é isso que justifica a construção de um Data Warehouse em vez da consulta avulsa a três arquivos.")

p("Respondidas por uma única base:", bold=True)
for i, q in enumerate([
    "Quais províncias pagam os maiores salários medianos para NOC 21232? (salário)",
    "Onde estão os imigrantes nascidos no Brasil e em que período chegaram? (imigração)",
    "Onde os inquilinos mais comprometem 30% ou mais da renda com moradia? (habitação)",
], 1):
    p(f"{i}. {q}")

p("Que cruzam duas bases:", bold=True)
for i, q in enumerate([
    "Quais províncias combinam salário mediano alto e comunidade brasileira numerosa? (salário + imigração)",
    "A imigração brasileira do período 2011–2021 concentrou-se nas províncias de maior salário mediano? (salário + imigração)",
    "Em quais províncias o salário mediano é alto e a proporção de inquilinos com moradia inacessível é baixa? (salário + habitação)",
    "Em quais províncias a comunidade brasileira é numerosa e a moradia é menos acessível? (imigração + habitação)",
], 4):
    p(f"{i}. {q}")

p("Que integram as três bases:", bold=True)
for i, q in enumerate([
    "As províncias com maior presença brasileira apresentam salários e condições de moradia diferentes das províncias com menor presença brasileira?",
    "Qual província oferece o melhor equilíbrio entre remuneração, comunidade brasileira e acessibilidade habitacional?",
    "Nas jurisdições sem salário provincial publicado para NOC 21232, o que a comunidade brasileira e a acessibilidade habitacional revelam?",
], 8):
    p(f"{i}. {q}")

h3("2.1.3 Cobertura das perguntas por fonte")
table(
    ["Pergunta", "Bases utilizadas", "Fatos consultados"],
    [
        ("1", "Job Bank", "fato_salario"),
        ("2", "StatCan 98-10-0307-01", "fato_imigracao"),
        ("3", "StatCan 98-10-0258-01", "fato_habitacao"),
        ("4", "Job Bank + StatCan 0307", "fato_salario, fato_imigracao"),
        ("5", "Job Bank + StatCan 0307", "fato_salario, fato_imigracao"),
        ("6", "Job Bank + StatCan 0258", "fato_salario, fato_habitacao"),
        ("7", "StatCan 0307 + StatCan 0258", "fato_imigracao, fato_habitacao"),
        ("8", "Job Bank + StatCan 0307 + StatCan 0258", "os três fatos"),
        ("9", "Job Bank + StatCan 0307 + StatCan 0258", "os três fatos"),
        ("10", "Job Bank + StatCan 0307 + StatCan 0258", "os três fatos"),
    ],
    widths=[0.9, 3.0, 2.7],
    font_size=9,
)
p("O cruzamento das perguntas 4 a 10 só é possível porque dim_provincia é uma dimensão conformada, compartilhada pelos três fatos: é ela que permite alinhar as medidas das três fontes na mesma jurisdição.")
page_break()


# ---------------------------------------------------------------- 3 BASES DE DADOS UTILIZADAS
h1("3 Bases de Dados Utilizadas")

p("Os arquivos públicos em CSV/ZIP são datasets analíticos de origem, e não sistemas OLTP transacionais clássicos. Para atender à organização dimensional solicitada, eles são tratados como camada operacional de origem. Os brutos versionados ficam em raw/; o ZIP de imigração, com cerca de 383 MB, não é versionado devido ao tamanho. Sua obtenção reproduzível, URL, data de extração e checksum são documentados na seção 9.1. Filtros e padronizações ocorrem apenas em staging e no DW.")

h2("3.1 FONTES SELECIONADAS")
table(
    ["Base", "Órgão / período", "Onde está no repositório", "Uso"],
    [
        ("Statistics Canada 98-10-0307-01", "Statistics Canada · Censo 2021", "Extração filtered/. ZIP fora do Git; download reproduzível: https://www150.statcan.gc.ca/n1/en/tbl/csv/98100307-eng.zip", "Imigrantes por país de nascimento, período de imigração e província/território."),
        ("Job Bank / ESDC Wages", "ESDC · release 2025; referência 2023–2024; revisão 2025-11-19", "raw/job_bank_wages_2025.csv", "Salários de Software Developers and Programmers (NOC 21232) por região."),
        ("Statistics Canada 98-10-0258-01", "Statistics Canada · Censo 2021", "raw/98100258_extracted/98100258.csv e filtered/statcan_98100258_housing_provinces_territories.csv", "Indicadores habitacionais por posse (total, proprietário, inquilino, governo/First Nation)."),
    ],
    widths=[1.8, 1.6, 1.6, 1.5],
)

h3("3.1.1 Procedência do ZIP de imigração fora do Git")
p("O arquivo 98100307-eng.zip não é versionado porque seu tamanho aproximado é 383 MB. Foi extraído em 14 de setembro de 2026 a partir de https://www150.statcan.gc.ca/n1/en/tbl/csv/98100307-eng.zip. Para reproduzir, baixar esse URL, registrar o SHA-256 com o comando shasum -a 256 98100307-eng.zip, descompactar o CSV e aplicar os filtros documentados para gerar filtered/statcan_98100307_brazil_provinces_territories.csv. O valor do checksum deve ser carregado em dim_fonte.ds_checksum junto com a data efetiva do download; ele não é inventado no repositório, pois o ZIP não está presente para conferência.")

h2("3.2 VOLUMETRIA DAS EXTRAÇÕES")
table(
    ["Fonte", "Registros no bruto", "Extração usada", "Registros na extração"],
    [
        ("Job Bank/ESDC Wages", "44.376", "NOC 21232, nível provincial", "9 províncias com salário publicado"),
        ("StatCan 98-10-0307-01", "ZIP 383 MB (tabela completa)", "13 províncias × (Brazil + Total)", "26"),
        ("StatCan 98-10-0258-01", "2.990", "13 províncias × 9 indicadores × 2021", "117"),
    ],
    widths=[1.9, 1.5, 1.9, 1.2],
)

h2("3.3 PRÉ-PROCESSAMENTO (ETL) E IMPACTO DAS TRANSFORMAÇÕES")
p("Os arquivos brutos são preservados sem alteração física. Toda transformação ocorre em staging/DW; portanto, uma linha fora do recorte não é apagada, apenas deixa de ser carregada no fato correspondente.")
table(
    ["Transformação", "Antes → Depois", "Justificativa / Impacto"],
    [
        ("Filtro Job Bank: NOC_CNP = NOC_21232", "44.376 → 86 registros", "Manter apenas a ocupação do escopo (Software developers and programmers)."),
        ("Classificação da cobertura salarial", "86 → 13 jurisdições classificadas", "O DW preserva 9 salários provinciais, 1 caso apenas regional (PEI/ER1110) e 3 indisponíveis (territórios), sem usar regional como se fosse provincial."),
        ("Filtro StatCan imigração: Age/Gender totais e Place of birth em {Brazil, Total – Place of birth}", "ZIP bruto externo (quantidade total não registrada) → 26 registros", "Garante numerador (Brazil) e denominador (Total) comparáveis, sem quebra por idade/gênero. Risco: não permite análises por idade/gênero; a contagem do bruto deve ser registrada se o ZIP for rebaixado."),
        ("Filtro StatCan habitação: 13 províncias/territórios e Census year = 2021", "2.990 → 117 registros", "Remove CMAs/CAs e o Censo 2016; mantém o grão provincial do fato."),
        ("Normalização geográfica", "nome inglês da província como chave de cruzamento", "Job Bank usa prov/ER_Code e StatCan usa DGUID; o nome em inglês é a chave comum. Quebec (inglês) ≠ Québec (francês, não usado). Risco: mudança de grafia pode impedir a junção; o ETL deve registrar linhas sem correspondência."),
        ("Tratamento de cobertura salarial", "provincial / regional / indisponível", "O status é registrado em fato_salario; valores ficam NULL quando indisponíveis e o código/nome da região é preservado quando houver somente dado regional."),
        ("DGUID canônico", "1 DGUID por jurisdição", "Evita duplicidade geográfica (ex.: Yukon)."),
        ("Percentuais", "participação derivada; habitação armazenada", "Participação brasileira é calculada na apresentação; percentuais oficiais de habitação são armazenados como medidas não aditivas."),
    ],
    widths=[1.9, 1.6, 3.0],
)
p("Impacto geral: o Job Bank é reduzido de 44.376 registros a 13 situações de cobertura para NOC 21232: 9 provinciais, 1 apenas regional e 3 indisponíveis. A habitação cai de 2.990 para 117 registros; a imigração usa 26 registros. Nenhuma linha é excluída dos brutos — apenas filtrada nas camadas seguintes. A redução geográfica introduz viés de cobertura: resultados provinciais não representam CMAs/CAs; salários apenas regionais são identificados e não comparados como provinciais.")
picture("fig_salario_vs_brasileiros.png")
page_break()


# ---------------------------------------------------------------- 4 ANÁLISE EXPLORATÓRIA
h1("4 Análise Exploratória")

h2("4.1 SALÁRIOS — JOB BANK/ESDC")
p("O arquivo bruto tem 44.376 registros e 516 ocupações NOC distintas; NOC 21232 aparece em 86 registros. Cerca de 45% das células salariais do arquivo completo estão vazias (Low 20.301; Median 20.012; High 20.288), explicadas por Wage_Comment_E. No recorte usado (Reference_Period = 2023-2024, Annual_Wage_Flag = 0), 9 jurisdições têm salário provincial publicado; PEI possui dado apenas regional (ER1110) e Yukon, Northwest Territories e Nunavut não possuem salário publicado.")
table(
    ["Província", "Low", "Median", "High", "Amplitude"],
    [
        ("BC", "31,25", "52,40", "84,13", "52,88"),
        ("ON", "30,29", "48,08", "77,40", "47,11"),
        ("AB", "29,81", "48,08", "76,92", "47,11"),
        ("SK", "28,85", "48,07", "68,68", "39,83"),
        ("NB", "28,00", "45,67", "74,04", "46,04"),
        ("QC", "29,00", "45,67", "68,13", "39,13"),
        ("NL", "30,77", "43,75", "74,52", "43,75"),
        ("MB", "30,00", "41,03", "62,02", "32,02"),
        ("NS", "24,50", "40,87", "66,67", "42,17"),
    ],
    widths=[1.0, 1.0, 1.1, 1.0, 1.3],
)
p("Mediana entre as 9 províncias: mín. 40,87 · máx. 52,40 · média 45,96 CAD/hora.")
picture("fig_salario_mediano.png")

h2("4.2 IMIGRAÇÃO — STATISTICS CANADA")
p("A extração tem 26 registros (13 jurisdições × Brazil / Total – Place of birth). A comunidade brasileira concentra-se em Ontário (23.120), Quebec (9.700) e Colúmbia Britânica (8.765); Yukon registrou 0 brasileiros.")
table(
    ["Província", "Total imigrantes", "Brasileiros", "% brasileiros"],
    [
        ("Ontario", "4.206.590", "23.120", "0,5%"),
        ("Quebec", "1.210.595", "9.700", "0,8%"),
        ("British Columbia", "1.425.715", "8.765", "0,6%"),
        ("Alberta", "970.975", "3.800", "0,4%"),
        ("Manitoba", "257.615", "1.810", "0,7%"),
        ("Nova Scotia", "71.570", "435", "0,6%"),
        ("Saskatchewan", "137.615", "380", "0,3%"),
        ("New Brunswick", "44.120", "240", "0,5%"),
        ("Newfoundland and Labrador", "14.250", "90", "0,6%"),
        ("Prince Edward Island", "11.765", "85", "0,7%"),
        ("Northwest Territories", "4.150", "10", "0,2%"),
        ("Nunavut", "1.165", "10", "0,9%"),
        ("Yukon", "5.380", "0", "0,0%"),
    ],
    widths=[2.0, 1.5, 1.2, 1.0],
)
p("Por período de imigração (soma das 13 jurisdições): Before 1980 = 2.740; 1980–1990 = 2.030; 1991–2000 = 4.530; 2001–2010 = 11.395; 2011–2021 = 27.740 — a chegada é predominantemente recente.")
picture("fig_imigracao_periodos.png")
picture("fig_comunidade_brasileira.png")

h2("4.3 HABITAÇÃO — STATISTICS CANADA")
p("Na extração (117 registros), o indicador Percent of households in unaffordable housing mostra, para inquilinos (Renter), o percentual com gasto de 30% ou mais da renda em moradia:")
table(
    ["Província", "% total", "% owner", "% renter"],
    [
        ("Ontario", "24,2", "17,7", "38,4"),
        ("British Columbia", "25,5", "19,3", "37,8"),
        ("Nova Scotia", "17,9", "9,7", "34,7"),
        ("Alberta", "21,2", "16,0", "34,0"),
        ("Manitoba", "17,3", "9,9", "33,5"),
        ("Saskatchewan", "17,2", "11,1", "33,1"),
        ("Newfoundland and Labrador", "14,6", "8,9", "32,5"),
        ("Prince Edward Island", "15,5", "8,8", "30,2"),
        ("New Brunswick", "12,9", "7,5", "28,0"),
        ("Quebec", "16,1", "10,0", "25,2"),
        ("Yukon", "16,2", "11,7", "24,9"),
        ("Northwest Territories", "11,9", "8,7", "15,6"),
        ("Nunavut", "5,7", "7,3", "5,2"),
    ],
    widths=[1.9, 1.0, 1.0, 1.0],
)
p("Para core housing need (inquilinos), destacam-se Nunavut (37,3%), Ontário (24,9%) e Colúmbia Britânica (24,7%); Quebec tem o menor percentual entre inquilinos (11,9%).")
picture("fig_moradia_inquilinos.png")

page_break()


# ---------------------------------------------------------------- 5 DICIONÁRIO DE DADOS
h1("5 Dicionário de Dados")

h2("5.1 BASE JOB BANK / ESDC")
p("CSV UTF-8 com BOM, 22 colunas e 44.376 registros. Domínio de prov: NAT, NL, PEI, NS, NB, QC, ON, MB, SK, AB, BC, YK, NWT, NU. ER_Code: ER00 = Canadá; ER + 2 dígitos = província/território; ER + 4 dígitos = região econômica.")
table(
    ["Campo", "Tipo", "Descrição / Domínio"],
    [
        ("NOC_CNP", "Texto", "Código NOC da ocupação (ex.: NOC_21232)."),
        ("NOC_Title_eng / NOC_Title_fra", "Texto", "Título da ocupação em inglês/francês."),
        ("prov", "Texto", "Código da província/território ou NAT (nacional)."),
        ("ER_Code_Code_RE / ER_Name / Nom_RE", "Texto", "Código e nome da região econômica (inglês/francês)."),
        ("Low_Wage_Salaire_Minium", "Numérico", "Salário mínimo; vazio quando não publicado."),
        ("Median_Wage_Salaire_Median", "Numérico", "Salário mediano; vazio quando não publicado."),
        ("High_Wage_Salaire_Maximal", "Numérico", "Salário máximo; vazio quando não publicado."),
        ("Average_Wage_Salaire_Moyen", "Numérico", "Salário médio."),
        ("Quartile1_Wage_Salaire_Quartile1 / Quartile3", "Numérico", "1º e 3º quartis salariais."),
        ("Source2025_NHQ", "Texto", "Fonte do dado (LFS 2023-24…, SAE 2024…, Census 2021…, N/A)."),
        ("Data_Source_E / Data_Source_F", "Texto", "Descrição da fonte (inglês/francês)."),
        ("Reference_Period", "Texto", "2021, 2023-2024, 2024 ou NA."),
        ("Revision_Date_Date_revision", "Data", "Data de revisão (YYYY-MM-DD)."),
        ("Annual_Wage_Flag_Salaire_annuel", "Inteiro", "0 = por hora; 1 = anual."),
        ("Wage_Comment_E / Wage_Comment_F", "Texto", "Motivo de publicação/ausência do salário."),
        ("EmployeesWithNonWageBenefit_Pct", "Numérico", "% de empregados com benefícios não salariais."),
    ],
    widths=[2.3, 0.9, 3.3],
)

h2("5.2 BASE STATISTICS CANADA — IMIGRAÇÃO (98-10-0307-01)")
p("Extração filtered/statcan_98100307_brazil_provinces_territories.csv: 26 registros (13 províncias × Brazil e Total – Place of birth), com Age (8D) = Total - Age e Gender (3) = Total - Gender. Cada medida é seguida de uma coluna Symbol (qualidade/supressão).")
table(
    ["Campo", "Tipo", "Descrição / Domínio"],
    [
        ("REF_DATE", "Inteiro", "Ano do Censo (2021)."),
        ("GEO / DGUID", "Texto", "Nome em inglês e DGUID da província/território (ex.: 2021A000235)."),
        ("Age (8D) / Gender (3)", "Texto", "Recortes usados: Total - Age e Total - Gender."),
        ("Place of birth (290)", "Texto", "Brazil ou Total – Place of birth."),
        ("Coordinate", "Texto", "Código de hierarquia geográfica do Censo."),
        ("Immigrant status…: Total[1] / Non-immigrants[2] / Immigrants[3]", "Inteiro", "População total, não imigrantes e total de imigrantes."),
        ("…: Before 1980[4] … 2011 to 2021[8]", "Inteiro", "Imigrantes por período de chegada (partições de Immigrants[3]; a soma não fecha exatamente por causa do arredondamento de base 5 do Censo)."),
        ("…: 2011 to 2015[9] / 2016 to 2021[10]", "Inteiro", "Subdivisões do período 2011–2021."),
        ("…: Non-permanent residents[11]", "Inteiro", "Residentes não permanentes."),
        ("Symbol", "Texto", "Símbolo de qualidade/supressão (vazio na extração)."),
    ],
    widths=[2.6, 0.8, 3.1],
)

h2("5.3 BASE STATISTICS CANADA — HABITAÇÃO (98-10-0258-01)")
p("Extração filtered/statcan_98100258_housing_provinces_territories.csv: 117 registros (13 províncias × 9 indicadores × Censo 2021).")
table(
    ["Campo", "Tipo", "Descrição / Domínio"],
    [
        ("REF_DATE / Census year (2)", "Inteiro/Texto", "2021 (recorte usado)."),
        ("GEO / DGUID", "Texto", "Província/território e DGUID."),
        ("Housing indicators (9)", "Texto", "Total, Adequacy, Affordability, Core housing need, Suitability e versões Percent of households…."),
        ("Coordinate", "Texto", "Código de hierarquia do Censo."),
        ("Tenure (4):Total - Tenure[1]", "Inteiro", "Total de domicílios."),
        ("Tenure (4):Owner[2]", "Inteiro", "Domicílios de proprietários."),
        ("Tenure (4):Renter[3]", "Inteiro", "Domicílios de inquilinos."),
        ("Tenure (4):Dwelling provided by…[4]", "Inteiro", "Moradias fornecidas pelo governo local/First Nation/Indian band."),
        ("Symbol", "Texto", "Símbolo de qualidade/supressão."),
    ],
    widths=[2.3, 0.8, 3.4],
)
page_break()


# ---------------------------------------------------------------- 5.4 DICIONÁRIO DW (derivado do DDL)
h2("5.4 DICIONÁRIO DE DADOS DO DATA WAREHOUSE")
p("As tabelas abaixo são geradas diretamente a partir de sql/script_oracle.sql, de modo que o "
  "dicionário e o script de implantação não divergem. Todas as dimensões usam chave substituta "
  "(surrogate key) NUMBER gerada por sequência e atribuída por gatilho BEFORE INSERT, e mantêm a "
  "chave natural da origem como chave "
  "alternativa (AK) — é por ela que a carga faz o lookup e evita duplicar registros na reexecução.")

_ddl = io.open(os.path.join(ROOT, "sql", "script_oracle.sql"), encoding="utf-8").read()
_desc = {
    "sk_": "Chave substituta gerada por sequência",
    "cd_": "Código de negócio vindo da origem",
    "nm_": "Nome descritivo",
    "ds_": "Descrição textual",
    "nr_": "Valor numérico",
    "dt_": "Data",
    "vl_": "Valor medido",
    "qt_": "Quantidade (medida aditiva)",
    "fl_": "Indicador booleano (0/1)",
    "tp_": "Tipo/classificação",
    "sg_": "Sigla",
}


def _papel(col, pk, ak, fks):
    if col == pk:
        return "PK"
    if col in fks:
        return "FK → %s" % fks[col]
    if col in ak:
        return "AK"
    return ""


def _dicionario(prefixo):
    linhas = []
    for m in re.finditer(r"CREATE TABLE (%s\w+) \((.*?)\n\) TABLESPACE" % prefixo, _ddl, re.S):
        nome, corpo_t = m.group(1), m.group(2)
        pk = re.search(r"PRIMARY KEY \((\w+)\)", corpo_t)
        pk = pk.group(1) if pk else ""
        ak = re.search(r"CONSTRAINT AK_\w+ UNIQUE \(([^)]+)\)", corpo_t)
        ak = {a.strip() for a in ak.group(1).split(",")} if ak else set()
        fks = dict(re.findall(r"FOREIGN KEY \((\w+)\)\s*\n?\s*REFERENCES (\w+)", corpo_t))
        for l in corpo_t.splitlines():
            mm = re.match(r"\s+(\w+)\s+(NUMBER\([\d,]+\)|NUMBER|VARCHAR2\(\d+\)|DATE)", l)
            if not mm:
                continue
            col, tipo = mm.group(1), mm.group(2)
            papel = _papel(col, pk, ak, fks)
            base = next((v for k, v in _desc.items() if col.startswith(k)), "Atributo da tabela")
            linhas.append((nome, col, tipo, (papel + " · " if papel else "") + base))
    return linhas


h3("5.4.1 Tabelas Fato")
table(["Tabela", "Coluna", "Tipo", "Descrição"], _dicionario("fato_"),
      widths=[1.5, 2.0, 1.2, 2.2], font_size=9)

h3("5.4.2 Tabelas Dimensão")
table(["Tabela", "Coluna", "Tipo", "Descrição"], _dicionario("dim_"),
      widths=[1.7, 1.9, 1.1, 2.2], font_size=9)
h3("5.4.3 Constraints de relacionamento")
p("Os nomes abaixo correspondem literalmente ao script Oracle e permitem conferir a ligação entre dicionário e DDL.")
table(
    ["Fato", "Constraints FK no script Oracle"],
    [
        ("fato_salario", "FK_FATO_SAL_DIM_PROVINCIA; FK_FATO_SAL_DIM_OCUPACAO; FK_FATO_SAL_DIM_TEMPO_SAL; FK_FATO_SAL_DIM_DISP; FK_FATO_SAL_DIM_FONTE"),
        ("fato_imigracao", "FK_FATO_IMIG_DIM_PROVINCIA; FK_FATO_IMIG_DIM_PAIS; FK_FATO_IMIG_DIM_PERIODO; FK_FATO_IMIG_DIM_TEMPO_CENSO; FK_FATO_IMIG_DIM_FONTE"),
        ("fato_habitacao", "FK_FATO_HAB_DIM_PROVINCIA; FK_FATO_HAB_DIM_TENENCIA; FK_FATO_HAB_DIM_INDICADOR; FK_FATO_HAB_DIM_TEMPO_CENSO; FK_FATO_HAB_DIM_FONTE"),
    ],
    widths=[1.5, 5.1],
    font_size=8,
)
page_break()


# ---------------------------------------------------------------- 6 MODELAGEM
h1("6 Modelagem do Data Warehouse")
h2("6.1 MODELO LÓGICO/FÍSICO DO DATA WAREHOUSE")
p("O modelo é uma constelação de fatos composta por três Star Schemas integrados por dimensões conformadas. A separação evita repetir salários em cada período de imigração e impede somas incorretas. A fato salarial registra a cobertura do Job Bank para cada jurisdição, distinguindo salário provincial publicado, dado somente regional e indisponibilidade. Fisicamente, o modelo é implantado em Oracle com tablespaces separados para dados e índices (TS_DW_DADOS e TS_DW_INDICES), sequences e gatilhos BEFORE INSERT para controle automatizado das chaves substitutas.")

h3("6.1.1 Diagrama")
picture("modelo_constelacao.png")
p("Figura 6 — Constelação de fatos com chaves primárias, chaves estrangeiras e cardinalidades 1:N. A dimensão de província é conformada; as dimensões de fonte e tempo do Censo também são reutilizadas entre fatos.", size=10, align=WD_ALIGN_PARAGRAPH.CENTER)

h3("6.1.2 Dimensões")
table(
    ["Dimensão", "Chave natural", "Atributos principais"],
    [
        ("dim_provincia", "cd_dguid", "nm_provincia, sg_provincia_jobbank, nm_pais"),
        ("dim_ocupacao", "cd_noc", "nm_ocupacao_en, nm_ocupacao_fr"),
        ("dim_tempo_salario", "cd_periodo_referencia", "nr_ano_inicio, nr_ano_fim, ds_periodo"),
        ("dim_disponibilidade_salario", "cd_disponibilidade", "ds_disponibilidade, fl_comparavel_provincial"),
        ("dim_tempo_censo", "nr_ano_censo", "dt_referencia"),
        ("dim_pais_nascimento", "cd_pais_nascimento", "nm_pais_nascimento"),
        ("dim_periodo_imigracao", "cd_periodo_imigracao", "ds_periodo_imigracao, nr_ordem"),
        ("dim_tenencia", "cd_tenencia", "ds_tenencia"),
        ("dim_indicador_habitacao", "cd_indicador_habitacao", "ds_indicador_habitacao, tp_medida"),
        ("dim_fonte", "cd_fonte", "nm_fonte, ds_url, dt_extracao, ds_checksum"),
    ],
    widths=[2.0, 1.9, 2.6],
)

h3("6.1.3 Fatos")
table(
    ["Fato", "Grão", "Medidas"],
    [
        ("fato_salario", "Jurisdição + ocupação + período salarial", "salários, flag anual, região de origem e disponibilidade"),
        ("fato_imigracao", "Província + país de nascimento + período de imigração + Censo", "qt_imigrantes (aditiva)"),
        ("fato_habitacao", "Província + posse + indicador habitacional + Censo", "vl_medida (contagem ou percentual)"),
    ],
    widths=[1.5, 2.4, 2.6],
)
p("A participação brasileira (%) não é armazenada: é calculada na camada de apresentação a partir das contagens de brasileiros e do total de imigrantes. Os percentuais habitacionais fornecidos oficialmente pelo Statistics Canada são armazenados em fato_habitacao.vl_medida, identificados por dim_indicador_habitacao.tp_medida = 'PERCENTUAL', e tratados como medidas não aditivas.")
p("Cada uma das 13 jurisdições recebe uma linha em fato_salario. O ETL atribui PROVINCIAL_PUBLICADO às 9 com salário provincial; APENAS_REGIONAL a PEI, preservando ER1110 e seu nome; e INDISPONIVEL a Yukon, Northwest Territories e Nunavut, mantendo os valores salariais NULL. Comparações e rankings entre jurisdições usam somente fl_comparavel_provincial = 1.")


# ---------------------------------------------------------------- 7 ANEXOS
h1("7 Anexos")
h2("7.1 SCRIPT DDL (ORACLE SQL)")
p("O script abaixo cria tablespaces, sequences, tabelas da camada OLTP de origem, dimensões e fatos do DW com constraints e índices, além dos gatilhos que atribuem as chaves substitutas. Identificadores com até 30 caracteres (compatível com Oracle 11g+). A criação dos tablespaces deve ser executada por usuário DBA; os parâmetros DW_DATAFILE e DW_INDEXFILE devem receber os caminhos de datafiles do ambiente. O dono do DW precisa de CREATE TABLE, CREATE SEQUENCE, CREATE TRIGGER, CREATE INDEX e quota nos tablespaces.")
sql_path = os.path.join(ROOT, "sql", "script_oracle.sql")
with open(sql_path, encoding="utf-8") as fh:
    for line in fh.read().splitlines():
        mono(line)


# ---------------------------------------------------------------- REFERÊNCIAS
page_break()
h1("Referências")
for ref in [
    "Statistics Canada. Table 98-10-0307-01 — Immigrant status and period of immigration by place of birth. Censo 2021. Disponível em: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=9810030701. Acesso em: 14 set. 2026.",
    "Government of Canada / ESDC. Job Bank Wages — Software developers and programmers (NOC 21232). Release 2025. Disponível em: https://open.canada.ca/data/en/dataset/adad580f-76b0-4502-bd05-20c125de9116. Acesso em: 14 set. 2026.",
    "Statistics Canada. Table 98-10-0258-01 — Housing indicators by tenure. Censo 2021. Disponível em: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=9810025801. Acesso em: 14 set. 2026.",
]:
    p(ref, size=12)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print("gerado:", OUT)
