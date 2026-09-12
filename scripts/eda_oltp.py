#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Análise Exploratória (EDA) das bases OLTP do projeto.

Uso:
    python scripts/eda_oltp.py

Lê os arquivos preservados em `raw/` e as extrações/filtros em `filtered/`
e imprime um resumo em Markdown para ser copiado para o trabalho escrito.
Não altera nenhum arquivo de dados.
"""

import csv
import os
import sys
from collections import Counter

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def path(*parts):
    return os.path.join(ROOT, *parts)


def read_rows(rel_path):
    full = path(*rel_path.split("/"))
    with open(full, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def as_float(value):
    if value in ("", "N/A", "NA", "n/a"):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def nums(rows, col):
    return [v for v in (as_float(r.get(col)) for r in rows) if v is not None]


def blank(rows, col):
    return sum(1 for r in rows if r.get(col, "") in ("", "N/A", "NA"))


def section(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def markdown_table(headers, rows):
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        print("| " + " | ".join(str(c) for c in row) + " |")


def fmt_int(x):
    return f"{int(x):,}".replace(",", ".")


# ---------------------------------------------------------------------------
# A. Job Bank / ESDC — arquivo bruto (OLTP)
# ---------------------------------------------------------------------------
section("A. Job Bank/ESDC — raw/job_bank_wages_2025.csv (base OLTP de salários)")

jb = read_rows("raw/job_bank_wages_2025.csv")
print(f"Total de registros: {len(jb)}")
print(f"NOCs distintos: {len({r['NOC_CNP'] for r in jb})}")

noc21232 = [r for r in jb if r["NOC_CNP"] == "NOC_21232"]
print(f"Registros NOC_21232 (Software developers and programmers): {len(noc21232)}")

print("\nProvíncias (`prov`) distintas e nº de linhas:")
prov_counts = Counter(r["prov"] for r in jb)
markdown_table(["prov", "linhas"], sorted(prov_counts.items()))

print("\nReference_Period (arquivo bruto completo):")
markdown_table(["Reference_Period", "linhas"], sorted(Counter(r["Reference_Period"] for r in jb).items()))

print("\nAnnual_Wage_Flag_Salaire_annuel (0 = por hora; 1 = anual):")
markdown_table(["flag", "linhas"], sorted(Counter(r["Annual_Wage_Flag_Salaire_annuel"] for r in jb).items()))

print("\nValores ausentes de salário (arquivo bruto completo):")
markdown_table(
    ["coluna", "vazios", "% do total"],
    [
        ("Low_Wage_Salaire_Minium", blank(jb, "Low_Wage_Salaire_Minium"), round(100 * blank(jb, "Low_Wage_Salaire_Minium") / len(jb), 1)),
        ("Median_Wage_Salaire_Median", blank(jb, "Median_Wage_Salaire_Median"), round(100 * blank(jb, "Median_Wage_Salaire_Median") / len(jb), 1)),
        ("High_Wage_Salaire_Maximal", blank(jb, "High_Wage_Salaire_Maximal"), round(100 * blank(jb, "High_Wage_Salaire_Maximal") / len(jb), 1)),
    ],
)

print("\nSource2025_NHQ para NOC_21232:")
markdown_table(
    ["Source2025_NHQ", "linhas"],
    sorted(Counter(r["Source2025_NHQ"] for r in noc21232).items()),
)

print("\nWage_Comment_E para NOC_21232 (motivo de ausência):")
markdown_table(
    ["Wage_Comment_E", "linhas"],
    sorted(Counter(r["Wage_Comment_E"] for r in noc21232).items(), key=lambda x: -x[1]),
)

# ---------------------------------------------------------------------------
# B. Job Bank — nível provincial NOC 21232
# ---------------------------------------------------------------------------
section("B. Job Bank — salários provinciais NOC_21232 (filtered/job_bank_wages_2025_noc_21232.csv)")

prov_rows = read_rows("filtered/job_bank_wages_2025_noc_21232.csv")
print(f"Províncias com salário provincial publicado: {len(prov_rows)}")

prov_rows_sorted = sorted(
    prov_rows,
    key=lambda r: as_float(r["median_wage_cad_per_hour"]) or -1,
    reverse=True,
)
print("\nSalários provinciais por hora (CAD), ordenados por mediana:")
markdown_table(
    ["prov", "low", "median", "high", "amplitude (high-low)"],
    [
        (
            r["province_code"],
            r["low_wage_cad_per_hour"],
            r["median_wage_cad_per_hour"],
            r["high_wage_cad_per_hour"],
            round((as_float(r["high_wage_cad_per_hour"]) or 0) - (as_float(r["low_wage_cad_per_hour"]) or 0), 2),
        )
        for r in prov_rows_sorted
    ],
)

medians = nums(prov_rows, "median_wage_cad_per_hour")
if medians:
    print(f"\nMediana salarial entre as províncias: min={min(medians):.2f} | max={max(medians):.2f} | média={sum(medians)/len(medians):.2f}")

# ---------------------------------------------------------------------------
# C. Statistics Canada — imigração (extração OLTP)
# ---------------------------------------------------------------------------
section("C. Statistics Canada — filtered/statcan_98100307_brazil_provinces_territories.csv")

sc = read_rows("filtered/statcan_98100307_brazil_provinces_territories.csv")
print(f"Registros: {len(sc)} (13 províncias/territórios × 2 recortes de Place of birth)")
print(f"REF_DATE: {sorted({r['REF_DATE'] for r in sc})}")
print(f"Age: {sorted({r['Age (8D)'] for r in sc})}")
print(f"Gender: {sorted({r['Gender (3)'] for r in sc})}")
print(f"Place of birth: {sorted({r['Place of birth (290)'] for r in sc})}")

brazil_rows = [r for r in sc if r["Place of birth (290)"] == "Brazil"]
total_rows = [r for r in sc if r["Place of birth (290)"] != "Brazil"]
by_geo_total = {r["GEO"]: r for r in total_rows}
by_geo_brazil = {r["GEO"]: r for r in brazil_rows}

print("\nImigrantes por província (Total × Brasil) e participação brasileira:")
table = []
for geo in sorted(by_geo_total):
    t = as_float(by_geo_total[geo]["Immigrant status and period of immigration (11):Immigrants[3]"]) or 0
    b = as_float(by_geo_brazil[geo]["Immigrant status and period of immigration (11):Immigrants[3]"]) or 0
    share = 100 * b / t if t else 0
    table.append((geo, fmt_int(t), fmt_int(b), f"{share:.1f}%"))
markdown_table(["GEO", "total_imigrantes", "brasileiros", "% brasileiros"], table)

period_cols = {
    "Before 1980[4]": "Immigrant status and period of immigration (11):Before 1980[4]",
    "1980 to 1990[5]": "Immigrant status and period of immigration (11):1980 to 1990[5]",
    "1991 to 2000[6]": "Immigrant status and period of immigration (11):1991 to 2000[6]",
    "2001 to 2010[7]": "Immigrant status and period of immigration (11):2001 to 2010[7]",
    "2011 to 2021[8]": "Immigrant status and period of immigration (11):2011 to 2021[8]",
}
print("\nDistribuição dos imigrantes brasileiros por período de imigração (soma das 13 jurisdições):")
markdown_table(
    ["período", "brasileiros"],
    [(label, fmt_int(sum(as_float(r[col]) or 0 for r in brazil_rows))) for label, col in period_cols.items()],
)

# ---------------------------------------------------------------------------
# D. Junção final (staging)
# ---------------------------------------------------------------------------
section("D. Junção — canada_provinces_brazil_software_developer_wages.csv")

join = read_rows("canada_provinces_brazil_software_developer_wages.csv")
print(f"Registros: {len(join)}")
print(f"Províncias sem salário provincial publicado (N/A): {blank(join, 'median_developer_wage')}")

print("\nRanking por mediana salarial (N/A no final):")
join_sorted = sorted(
    join,
    key=lambda r: (as_float(r["median_developer_wage"]) is not None, as_float(r["median_developer_wage"]) or 0),
    reverse=True,
)
markdown_table(
    ["province", "brasileiros_2021", "total_imigrantes", "mediana_salarial", "low", "high"],
    [
        (
            r["province"],
            fmt_int(as_float(r["brazilian_immigrants_2021"]) or 0),
            fmt_int(as_float(r["total_immigrants_2021"]) or 0),
            r["median_developer_wage"],
            r["low_developer_wage"],
            r["high_developer_wage"],
        )
        for r in join_sorted
    ],
)

print("\nTop 5 — maior comunidade brasileira:")
top_brazil = sorted(join, key=lambda r: -(as_float(r["brazilian_immigrants_2021"]) or 0))[:5]
markdown_table(
    ["province", "brasileiros_2021", "mediana_salarial"],
    [(r["province"], r["brazilian_immigrants_2021"], r["median_developer_wage"]) for r in top_brazil],
)

# ---------------------------------------------------------------------------
# E. Statistics Canada — habitação (Censo 2021)
# ---------------------------------------------------------------------------
section("E. Statistics Canada — filtered/statcan_98100258_housing_provinces_territories.csv")

hsg = read_rows("filtered/statcan_98100258_housing_provinces_territories.csv")
print(f"Registros: {len(hsg)} (13 jurisdições × {len({r['Housing indicators (9)'] for r in hsg})} indicadores)")
print(f"Census year: {sorted({r['Census year (2)'] for r in hsg})}")

unaff = [r for r in hsg if r["Housing indicators (9)"] == "Percent of households in unaffordable housing"]
unaff_sorted = sorted(unaff, key=lambda r: -(as_float(r["Tenure (4):Renter[3]"]) or 0))
print("\n% de inquilinos com moradia inacessível (gasto ≥ 30% da renda) por província:")
markdown_table(
    ["GEO", "% total", "% owner", "% renter"],
    [
        (
            r["GEO"],
            r["Tenure (4):Total - Tenure[1]"],
            r["Tenure (4):Owner[2]"],
            r["Tenure (4):Renter[3]"],
        )
        for r in unaff_sorted
    ],
)

need = [r for r in hsg if r["Housing indicators (9)"] == "Percent of households in core housing need"]
need_sorted = sorted(need, key=lambda r: -(as_float(r["Tenure (4):Renter[3]"]) or 0))
print("\n% de inquilinos em core housing need por província:")
markdown_table(
    ["GEO", "% total", "% owner", "% renter"],
    [
        (r["GEO"], r["Tenure (4):Total - Tenure[1]"], r["Tenure (4):Owner[2]"], r["Tenure (4):Renter[3]"])
        for r in need_sorted
    ],
)

print("\nFim da EDA.")
