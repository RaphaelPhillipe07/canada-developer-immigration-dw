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

import os

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
    section.top_margin = Cm(3)
    section.left_margin = Cm(3)
    section.bottom_margin = Cm(2)
    section.right_margin = Cm(2)

# ---------------------------------------------------------------- fontes padrão IFAL (Times New Roman)
def force_font(style_or_run, name="Times New Roman"):
    rpr = style_or_run.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    rfonts.set(qn("w:ascii"), name)
    rfonts.set(qn("w:hAnsi"), name)
    rfonts.set(qn("w:cs"), name)


normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(12)
normal.font.color.rgb = RGBColor(0, 0, 0)
normal.paragraph_format.line_spacing = 1.5
force_font(normal)

for hname in ("Heading 1", "Heading 2", "Heading 3"):
    st = doc.styles[hname]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    st.font.bold = True
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
    run.font.name = "Times New Roman"
    force_font(run)
    if align is not None:
        par.alignment = align
    if space_after is not None:
        par.paragraph_format.space_after = Pt(space_after)
    return par


def center(text, bold=False, size=12, space_after=0):
    return p(text, bold=bold, size=size, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=space_after)


def bullet(text):
    par = doc.add_paragraph(text, style="List Bullet")
    for run in par.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        force_font(run)
    return par


def mono(text):
    par = doc.add_paragraph()
    run = par.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    force_font(run, "Consolas")
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
        run.font.name = "Times New Roman"
        run.font.size = Pt(font_size)
        force_font(run)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(str(val))
            run.font.name = "Times New Roman"
            run.font.size = Pt(font_size)
            force_font(run)
    if widths:
        for i, w in enumerate(widths):
            for row in t.rows:
                row.cells[i].width = Inches(w)
    doc.add_paragraph()
    return t


def picture(rel):
    diagram = os.path.join(ROOT, "docs", "figuras", rel)
    image_path = diagram if os.path.exists(diagram) else os.path.join(ROOT, "presentation", "images", rel)
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
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    force_font(run)


def add_toc():
    par = doc.add_paragraph()
    run = par.add_run()
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = r'TOC \o "1-2" \h \z \u'
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "separate")
    fld3 = OxmlElement("w:fldChar")
    fld3.set(qn("w:fldCharType"), "end")
    placeholder = OxmlElement("w:t")
    placeholder.text = "Abra no Word e pressione F9 (ou clique com o botão direito → Atualizar campo) para gerar o sumário."
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)
    run._r.append(placeholder)
    run._r.append(fld3)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    force_font(run)


add_page_number_footer()

# ---------------------------------------------------------------- CAPA
logo_path = os.path.join(ROOT, "ifal_logo.png")
if os.path.exists(logo_path):
    doc.add_picture(logo_path, width=Inches(2.2))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

center("INSTITUTO FEDERAL DE ALAGOAS", bold=True, size=14, space_after=0)
center("CAMPUS MACEIÓ", bold=True, size=14, space_after=0)
center("BACHARELADO EM SISTEMAS DE INFORMAÇÃO", bold=True, size=14, space_after=24)

center("DATA WAREHOUSE DE OPORTUNIDADES PARA", bold=True, size=14, space_after=0)
center("DESENVOLVEDORES IMIGRANTES NO CANADÁ", bold=True, size=14, space_after=24)

center("Eliezir Moreira Peixoto Neto", size=12, space_after=0)
center("Raphael Phillipe da Silva Silverio", size=12, space_after=24)

center("MACEIÓ - AL", bold=True, size=12, space_after=0)
center("14 de dezembro de 2026", bold=True, size=12, space_after=0)
page_break()

# ---------------------------------------------------------------- FOLHA DE ROSTO
center("Eliezir Moreira Peixoto Neto", size=12, space_after=0)
center("Raphael Phillipe da Silva Silverio", size=12, space_after=24)

center("DATA WAREHOUSE DE OPORTUNIDADES PARA", bold=True, size=14, space_after=0)
center("DESENVOLVEDORES IMIGRANTES NO CANADÁ", bold=True, size=14, space_after=24)

p(
    "Projeto de banco de dados apresentado como requisito integrante à nota da disciplina "
    "Tópicos Avançados em Banco de Dados do Bacharelado em Sistemas de Informação. "
    "Orientador: Prof. Me. Luiz Frederico Lopes de Oliveira.",
    size=12,
    align=WD_ALIGN_PARAGRAPH.JUSTIFY,
    space_after=24,
)

center("MACEIÓ - AL", bold=True, size=12, space_after=0)
center("14 de dezembro de 2026", bold=True, size=12, space_after=0)
page_break()

# ---------------------------------------------------------------- SUMÁRIO
h1("Sumário")
add_toc()
page_break()

# ---------------------------------------------------------------- 1. TEMA
h1("1. Tema")
p("Implantação de um Data Warehouse para análise de oportunidades de desenvolvedores de software imigrantes no Canadá.")

# ---------------------------------------------------------------- 2. DELIMITAÇÃO
h1("2. Delimitação do Tema")
p("O projeto abrange as 13 províncias e territórios canadenses e integra duas fontes institucionais: Statistics Canada e Job Bank/ESDC. Elas fornecem três conjuntos de dados: imigração e habitação do Censo 2021, além de salários de Software Developers and Programmers (NOC 21232), com referência salarial 2023–2024.")

# ---------------------------------------------------------------- 3. PROBLEMA
h1("3. Problema")
p("Como estruturar um Data Warehouse que integre dados oficiais de imigração, salários e habitação, permitindo comparar as províncias canadenses para apoiar a decisão de desenvolvedores de software imigrantes?")

# ---------------------------------------------------------------- 4. HIPÓTESE
h1("4. Hipótese")
p("A modelagem dimensional em três esquemas estrela com dimensões conformadas e a preservação das ausências permitem representar os dados necessários para responder às 10 perguntas analíticas sem estimar valores ausentes.")

# ---------------------------------------------------------------- 5. JUSTIFICATIVA
h1("5. Justificativa")
p("Profissionais de desenvolvimento de software que pretendem imigrar para o Canadá precisam escolher uma província ou território considerando, ao mesmo tempo, remuneração, presença de comunidade brasileira e acessibilidade habitacional. Essas informações estão espalhadas em bases oficiais diferentes — Statistics Canada (Censo 2021) e Job Bank/ESDC — com formatos, períodos e códigos geográficos distintos. O Data Warehouse integra essas fontes e permite comparações consistentes entre as jurisdições.")

# ---------------------------------------------------------------- 6. OBJETIVO GERAL
h1("6. Objetivo Geral")
p("Construir um Data Warehouse em Oracle que integre dados oficiais do Statistics Canada e do Job Bank/ESDC para comparar, entre as províncias e territórios canadenses, a distribuição de imigrantes brasileiros, a remuneração de desenvolvedores de software (NOC 21232) e a acessibilidade habitacional.")

# ---------------------------------------------------------------- 7. OBJETIVOS ESPECÍFICOS
h1("7. Objetivos Específicos")
bullet("Modelar uma constelação de fatos composta por três Star Schemas integrados por dimensões conformadas e surrogate keys.")
bullet("Documentar o dicionário de dados das bases públicas de origem e do Data Warehouse.")
bullet("Realizar a análise exploratória das bases de origem.")
bullet("Justificar e analisar o impacto de toda transformação aplicada aos dados de origem.")
bullet("Elaborar o script SQL de implantação do modelo em Oracle (tablespaces, sequences, constraints e índices).")
bullet("Definir as 10 perguntas analíticas que o Data Warehouse deverá responder.")

# ---------------------------------------------------------------- 8. META SMART
h1("8. Meta Smart")
table(
    ["Componente", "Descrição"],
    [
        ("S — Específica", "Construir um DW em Oracle com dados oficiais de imigração, salários e habitação."),
        ("M — Mensurável", "Apresentar o modelo Star Schema, os dicionários e o script SQL que permitem responder às 10 perguntas do plano."),
        ("A — Atingível", "Duas bases no escopo mínimo + uma complementar, já baixadas e filtradas, com modelo viável em Oracle."),
        ("R — Relevante", "Apoiar a decisão de desenvolvedores de software imigrantes sobre a melhor província canadense."),
        ("T — Temporal", "Até 14 de dezembro de 2026."),
    ],
    widths=[1.6, 4.9],
)

# ---------------------------------------------------------------- 9. DESCRIÇÃO DO SISTEMA / DADOS DE ORIGEM
h1("9. Descrição do Sistema e dos Dados de Origem")
p("Os arquivos públicos em CSV/ZIP são datasets analíticos de origem, e não sistemas OLTP transacionais clássicos. Para atender à organização dimensional solicitada, eles são tratados como camada operacional de origem. Os arquivos brutos são preservados sem alteração na pasta raw/ com URL, data de extração e checksum; filtros e padronizações ocorrem apenas em staging e no DW.")

h2("9.1 Fontes selecionadas")
table(
    ["Base", "Órgão / período", "Onde está no repositório", "Uso"],
    [
        ("Statistics Canada 98-10-0307-01", "Statistics Canada · Censo 2021", "filtered/statcan_98100307_brazil_provinces_territories.csv (ZIP bruto de 383 MB mantido fora do Git)", "Imigrantes por país de nascimento, período de imigração e província/território."),
        ("Job Bank / ESDC Wages", "ESDC · release 2025; referência 2023–2024; revisão 2025-11-19", "raw/job_bank_wages_2025.csv", "Salários de Software Developers and Programmers (NOC 21232) por região."),
        ("Statistics Canada 98-10-0258-01", "Statistics Canada · Censo 2021", "raw/98100258_extracted/98100258.csv e filtered/statcan_98100258_housing_provinces_territories.csv", "Indicadores habitacionais por posse (total, proprietário, inquilino, governo/First Nation)."),
    ],
    widths=[1.8, 1.6, 1.6, 1.5],
)

h2("9.2 Volumetria das extrações")
table(
    ["Fonte", "Registros no bruto", "Extração usada", "Registros na extração"],
    [
        ("Job Bank/ESDC Wages", "44.376", "NOC 21232, nível provincial", "9 províncias com salário publicado"),
        ("StatCan 98-10-0307-01", "ZIP 383 MB (tabela completa)", "13 províncias × (Brazil + Total)", "26"),
        ("StatCan 98-10-0258-01", "2.988", "13 províncias × 9 indicadores × 2021", "117"),
    ],
    widths=[1.9, 1.5, 1.9, 1.2],
)

# ---------------------------------------------------------------- 10. REQUISITOS (10 PERGUNTAS)
h1("10. Requisitos — As 10 Perguntas Analíticas")
questions = [
    "Quais províncias possuem os maiores salários medianos para NOC 21232?",
    "Qual é a diferença de salário mediano entre duas províncias selecionadas?",
    "Em quais províncias há maior número de imigrantes nascidos no Brasil?",
    "Qual é a participação de brasileiros no total de imigrantes de cada província?",
    "Qual período de imigração concentra mais brasileiros em cada província?",
    "Quais províncias combinam salário mediano alto e comunidade brasileira numerosa?",
    "Qual província possui a maior amplitude salarial (high wage − low wage)?",
    "Quais jurisdições têm salário não publicado, apenas regional ou indisponível para NOC 21232?",
    "Quais províncias apresentam maior proporção de inquilinos com gasto de 30% ou mais da renda em moradia?",
    "Quais províncias oferecem melhor equilíbrio entre remuneração, comunidade brasileira e acessibilidade habitacional?",
]
for i, q in enumerate(questions, 1):
    p(f"{i}. {q}")

h2("10.1 Regra do indicador combinado da pergunta 10")
p("A pergunta 10 será respondida somente entre as jurisdições com os três indicadores disponíveis, isto é, com salário mediano provincial publicado, população brasileira no Censo 2021 e percentual de inquilinos com moradia inacessível no Censo 2021. Não há imputação de salário para PEI, Yukon, Northwest Territories ou Nunavut; essas jurisdições recebem resultado N/A e não entram no ranking.")
p("Para cada conjunto elegível, os indicadores são normalizados no intervalo de 0 a 1. Salário e comunidade brasileira usam min-max crescente; inacessibilidade habitacional usa min-max invertido, pois menor percentual é melhor. A pontuação é: Índice = 0,40 × Salário_norm + 0,30 × Comunidade_norm + 0,30 × Acessibilidade_norm. Empates são desfeitos pela maior mediana salarial.")
table(
    ["Componente", "Cálculo", "Peso"],
    [
        ("Salário_norm", "(mediana − menor mediana) / (maior mediana − menor mediana)", "0,40"),
        ("Comunidade_norm", "(brasileiros − menor número) / (maior número − menor número)", "0,30"),
        ("Acessibilidade_norm", "1 − ((% inquilinos ≥ 30% − menor %) / (maior % − menor %))", "0,30"),
    ],
    widths=[1.5, 4.3, 0.8],
    font_size=9,
)
page_break()

# ---------------------------------------------------------------- 11. DICIONÁRIO DE ORIGEM
h1("11. Dicionário de Dados das Bases de Origem")

h2("11.1 Job Bank / ESDC Wages — raw/job_bank_wages_2025.csv")
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

h2("11.2 Statistics Canada — imigração (98-10-0307-01)")
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
        ("…: Before 1980[4] … 2011 to 2021[8]", "Inteiro", "Imigrantes por período de chegada (partições de Immigrants[3])."),
        ("…: 2011 to 2015[9] / 2016 to 2021[10]", "Inteiro", "Subdivisões do período 2011–2021."),
        ("…: Non-permanent residents[11]", "Inteiro", "Residentes não permanentes."),
        ("Symbol", "Texto", "Símbolo de qualidade/supressão (vazio na extração)."),
    ],
    widths=[2.6, 0.8, 3.1],
)

h2("11.3 Statistics Canada — habitação (98-10-0258-01)")
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

# ---------------------------------------------------------------- 12. EDA
h1("12. Análise Exploratória das Bases de Origem")

h2("12.1 Salários — Job Bank/ESDC")
p("O arquivo bruto tem 44.376 registros e 516 ocupações NOC distintas; NOC 21232 aparece em 86 registros. Cerca de 45% das células salariais do arquivo completo estão vazias (Low 20.301; Median 20.012; High 20.288), explicadas por Wage_Comment_E. No recorte usado (Reference_Period = 2023-2024, Annual_Wage_Flag = 0), apenas 9 províncias publicam salário provincial de NOC 21232.")
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

h2("12.2 Imigração — Statistics Canada")
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

h2("12.3 Habitação — Statistics Canada")
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

h2("12.4 Junção staging")
p("A junção left join das 13 jurisdições do StatCan com os salários provinciais do Job Bank (por nome de província em inglês) mantém N/A para PEI, Yukon, NWT e Nunavut.")
picture("fig_salario_vs_brasileiros.png")
page_break()

# ---------------------------------------------------------------- 13. ALTERAÇÕES E IMPACTO
h1("13. Transformações nas Bases de Origem e Impacto")
p("Os arquivos brutos são preservados sem alteração física. Toda transformação ocorre em staging/DW; portanto, uma linha fora do recorte não é apagada, apenas deixa de ser carregada no fato correspondente.")
table(
    ["Transformação", "Antes → Depois", "Justificativa / Impacto"],
    [
        ("Filtro Job Bank: NOC_CNP = NOC_21232", "44.376 → 86 registros", "Manter apenas a ocupação do escopo (Software developers and programmers)."),
        ("Filtro Job Bank: nível provincial (ER de 2 dígitos)", "86 → 9 registros usados", "O fato salarial tem grão provincial; regiões econômicas e agregado nacional ficam fora do fato."),
        ("Filtro StatCan imigração: Age/Gender totais e Place of birth em {Brazil, Total – Place of birth}", "ZIP bruto externo (quantidade total não registrada) → 26 registros", "Garante numerador (Brazil) e denominador (Total) comparáveis, sem quebra por idade/gênero. Risco: não permite análises por idade/gênero; a contagem do bruto deve ser registrada se o ZIP for rebaixado."),
        ("Filtro StatCan habitação: 13 províncias/territórios e Census year = 2021", "2.988 → 117 registros", "Remove CMAs/CAs e o Censo 2016; mantém o grão provincial do fato."),
        ("Normalização geográfica", "nome inglês da província como chave de cruzamento", "Job Bank usa prov/ER_Code e StatCan usa DGUID; o nome em inglês é a chave comum. Quebec (inglês) ≠ Québec (francês, não usado). Risco: mudança de grafia pode impedir a junção; o ETL deve registrar linhas sem correspondência."),
        ("Tratamento de ausências salariais", "células vazias → N/A/NULL", "Nenhum valor é estimado; PEI só tem ER1110 e territórios não têm salário publicado no release."),
        ("DGUID canônico", "1 DGUID por jurisdição", "Evita duplicidade geográfica (ex.: Yukon)."),
        ("Percentuais", "não armazenados como medida", "Participação brasileira e percentuais são calculados na apresentação para evitar soma de fatos não aditivos."),
    ],
    widths=[1.9, 1.6, 3.0],
)
p("Impacto geral: o Job Bank cai de 44.376 para 9 registros provinciais efetivamente usados no fato_salario; a habitação cai de 2.988 para 117 registros; a imigração usa 26 registros. Nenhuma linha é excluída dos brutos — apenas filtrada nas camadas seguintes. A redução geográfica introduz viés de cobertura: resultados provinciais não representam regiões econômicas, CMAs/CAs ou valores salariais indisponíveis.")
page_break()

# ---------------------------------------------------------------- 14. MODELO DIMENSIONAL
h1("14. Modelo Lógico/Físico do Data Warehouse")
p("O modelo é uma constelação de fatos composta por três Star Schemas integrados por dimensões conformadas. A separação evita repetir salários em cada período de imigração e impede somas incorretas.")

h2("14.1 Diagrama")
picture("modelo_constelacao.png")
p("Figura 6 — Constelação de fatos com chaves primárias, chaves estrangeiras e cardinalidades 1:N. A dimensão de província é conformada; as dimensões de fonte e tempo do Censo também são reutilizadas entre fatos.", size=10, align=WD_ALIGN_PARAGRAPH.CENTER)

h2("14.2 Dimensões")
table(
    ["Dimensão", "Chave natural", "Atributos principais"],
    [
        ("dim_provincia", "cd_dguid", "nm_provincia, sg_provincia_jobbank, nm_pais"),
        ("dim_ocupacao", "cd_noc", "nm_ocupacao_en, nm_ocupacao_fr"),
        ("dim_tempo_salario", "cd_periodo_referencia", "nr_ano_inicio, nr_ano_fim, ds_periodo"),
        ("dim_tempo_censo", "nr_ano_censo", "dt_referencia"),
        ("dim_pais_nascimento", "cd_pais_nascimento", "nm_pais_nascimento"),
        ("dim_periodo_imigracao", "cd_periodo_imigracao", "ds_periodo_imigracao, nr_ordem"),
        ("dim_tenencia", "cd_tenencia", "ds_tenencia"),
        ("dim_indicador_habitacao", "cd_indicador_habitacao", "ds_indicador_habitacao, tp_medida"),
        ("dim_fonte", "cd_fonte", "nm_fonte, ds_url, dt_extracao, ds_checksum"),
    ],
    widths=[2.0, 1.9, 2.6],
)

h2("14.3 Fatos")
table(
    ["Fato", "Grão", "Medidas"],
    [
        ("fato_salario", "Província + ocupação + período salarial", "vl_salario_minimo, vl_salario_mediano, vl_salario_maximo, vl_salario_medio, vl_quartil1, vl_quartil3, vl_amplitude_salarial, fl_salario_anual"),
        ("fato_imigracao", "Província + país de nascimento + período de imigração + Censo", "qt_imigrantes (aditiva)"),
        ("fato_habitacao", "Província + posse + indicador habitacional + Censo", "vl_medida (contagem ou percentual)"),
    ],
    widths=[1.5, 2.4, 2.6],
)
p("Participação brasileira (%) e percentuais habitacionais não são armazenados; são calculados na camada de apresentação (fatos não aditivos).")

# ---------------------------------------------------------------- 15. DICIONÁRIO DW
h1("15. Dicionário de Dados do Data Warehouse")
p("Nomenclatura: PK_ (primary key), FK_ (foreign key), AK_ (unique), CK_ (check), NN_ (not null), IDX_ (índice), SEQ_ (sequence). Todas as dimensões usam surrogate key NUMBER gerada por sequência.")

dw_tables = {
    "dim_provincia": [
        ("sk_provincia", "NUMBER(10)", "PK", "Gerada por sequência"),
        ("cd_dguid", "VARCHAR2(16)", "AK, NN", "DGUID do StatCan (ex.: 2021A000235)"),
        ("nm_provincia", "VARCHAR2(60)", "NN", "Nome em inglês (ex.: Ontario)"),
        ("sg_provincia_jobbank", "VARCHAR2(4)", "—", "Sigla do Job Bank (ex.: ON)"),
        ("nm_pais", "VARCHAR2(20)", "—", "Canada"),
    ],
    "dim_ocupacao": [
        ("sk_ocupacao", "NUMBER(10)", "PK", "Surrogate key"),
        ("cd_noc", "VARCHAR2(12)", "AK, NN", "NOC_21232"),
        ("nm_ocupacao_en", "VARCHAR2(120)", "NN", "Título em inglês"),
        ("nm_ocupacao_fr", "VARCHAR2(120)", "—", "Título em francês"),
    ],
    "dim_tempo_salario": [
        ("sk_tempo_salario", "NUMBER(10)", "PK", "Surrogate key"),
        ("cd_periodo_referencia", "VARCHAR2(20)", "AK, NN", "2023-2024"),
        ("nr_ano_inicio / nr_ano_fim", "NUMBER(4)", "—", "2023 / 2024"),
        ("ds_periodo", "VARCHAR2(50)", "—", "Descrição legível"),
    ],
    "dim_tempo_censo": [
        ("sk_tempo_censo", "NUMBER(10)", "PK", "Surrogate key"),
        ("nr_ano_censo", "NUMBER(4)", "AK, NN, CK", "2021"),
        ("dt_referencia", "DATE", "—", "Data de referência do Censo"),
    ],
    "dim_pais_nascimento": [
        ("sk_pais_nascimento", "NUMBER(10)", "PK", "Surrogate key"),
        ("cd_pais_nascimento", "VARCHAR2(30)", "AK, NN", "BRA / TOTAL"),
        ("nm_pais_nascimento", "VARCHAR2(80)", "NN", "Brazil / Total – Place of birth"),
    ],
    "dim_periodo_imigracao": [
        ("sk_periodo_imigracao", "NUMBER(10)", "PK", "Surrogate key"),
        ("cd_periodo_imigracao", "VARCHAR2(20)", "AK, NN", "[4] … [8]"),
        ("ds_periodo_imigracao", "VARCHAR2(40)", "NN", "Before 1980 … 2011 to 2021"),
        ("nr_ordem", "NUMBER(2)", "—", "Ordem cronológica"),
    ],
    "dim_tenencia": [
        ("sk_tenencia", "NUMBER(10)", "PK", "Surrogate key"),
        ("cd_tenencia", "VARCHAR2(10)", "AK, NN", "TOTAL / OWNER / RENTER / GOV"),
        ("ds_tenencia", "VARCHAR2(60)", "NN", "Descrição da posse"),
    ],
    "dim_indicador_habitacao": [
        ("sk_indicador_habitacao", "NUMBER(10)", "PK", "Surrogate key"),
        ("cd_indicador_habitacao", "VARCHAR2(60)", "AK, NN", "Texto original do StatCan"),
        ("ds_indicador_habitacao", "VARCHAR2(120)", "—", "Descrição resumida"),
        ("tp_medida", "VARCHAR2(10)", "CK", "CONTAGEM / PERCENTUAL"),
    ],
    "dim_fonte": [
        ("sk_fonte", "NUMBER(10)", "PK", "Surrogate key"),
        ("cd_fonte", "VARCHAR2(20)", "AK, NN", "JOB_BANK_2025 / STATCAN_0307 / STATCAN_0258"),
        ("nm_fonte", "VARCHAR2(120)", "NN", "Nome oficial"),
        ("ds_url", "VARCHAR2(500)", "—", "URL do download"),
        ("dt_extracao", "DATE", "—", "Data de extração"),
        ("ds_checksum", "VARCHAR2(128)", "—", "SHA-256 do arquivo bruto"),
    ],
    "fato_salario": [
        ("sk_fato_salario", "NUMBER(15)", "PK", "Surrogate key"),
        ("sk_provincia / sk_ocupacao / sk_tempo_salario / sk_fonte", "NUMBER(10)", "FK, NN", "Chaves das dimensões"),
        ("vl_salario_minimo / mediano / maximo / medio", "NUMBER(10,2)", "—", "Salários (CAD/hora)"),
        ("vl_quartil1 / vl_quartil3", "NUMBER(10,2)", "—", "Quartis"),
        ("vl_amplitude_salarial", "NUMBER(10,2)", "—", "high − low (derivada)"),
        ("fl_salario_anual", "NUMBER(1)", "CK", "0 = hora; 1 = anual"),
    ],
    "fato_imigracao": [
        ("sk_fato_imigracao", "NUMBER(15)", "PK", "Surrogate key"),
        ("sk_provincia / sk_pais_nascimento / sk_periodo_imigracao / sk_tempo_censo / sk_fonte", "NUMBER(10)", "FK, NN", "Chaves das dimensões"),
        ("qt_imigrantes", "NUMBER(12)", "CK", "Contagem (>= 0)"),
    ],
    "fato_habitacao": [
        ("sk_fato_habitacao", "NUMBER(15)", "PK", "Surrogate key"),
        ("sk_provincia / sk_tenencia / sk_indicador_habitacao / sk_tempo_censo / sk_fonte", "NUMBER(10)", "FK, NN", "Chaves das dimensões"),
        ("vl_medida", "NUMBER(15,2)", "CK", "Contagem ou percentual (>= 0)"),
    ],
}

for tname, rows in dw_tables.items():
    h3(tname)
    table(["Campo", "Tipo", "Constraint", "Descrição / Origem"], rows, widths=[2.4, 1.2, 1.0, 1.9])

h2("15.1 Constraints de relacionamento")
p("Os nomes abaixo correspondem literalmente ao script Oracle e permitem conferir a ligação entre dicionário e DDL.")
table(
    ["Fato", "Constraints FK no script Oracle"],
    [
        ("fato_salario", "FK_FATO_SAL_DIM_PROVINCIA; FK_FATO_SAL_DIM_OCUPACAO; FK_FATO_SAL_DIM_TEMPO_SAL; FK_FATO_SAL_DIM_FONTE"),
        ("fato_imigracao", "FK_FATO_IMIG_DIM_PROVINCIA; FK_FATO_IMIG_DIM_PAIS; FK_FATO_IMIG_DIM_PERIODO; FK_FATO_IMIG_DIM_TEMPO_CENSO; FK_FATO_IMIG_DIM_FONTE"),
        ("fato_habitacao", "FK_FATO_HAB_DIM_PROVINCIA; FK_FATO_HAB_DIM_TENENCIA; FK_FATO_HAB_DIM_INDICADOR; FK_FATO_HAB_DIM_TEMPO_CENSO; FK_FATO_HAB_DIM_FONTE"),
    ],
    widths=[1.5, 5.1],
    font_size=8,
)
page_break()

# ---------------------------------------------------------------- 16. ANEXO SQL
h1("16. Anexo — Script SQL (Oracle)")
p("O script abaixo cria tablespaces, sequences, tabelas de staging, dimensões e fatos do DW com constraints e índices. Identificadores com até 30 caracteres (compatível com Oracle 11g+). A criação dos tablespaces deve ser executada por usuário DBA; os parâmetros DW_DATAFILE e DW_INDEXFILE devem receber os caminhos de datafiles do ambiente. O dono do DW precisa de CREATE TABLE, CREATE SEQUENCE, CREATE INDEX e quota nos tablespaces.")
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
