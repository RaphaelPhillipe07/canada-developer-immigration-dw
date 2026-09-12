#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera os gráficos dos slides (Entrega 1) em PNG.

Uso:
    python scripts/gerar_graficos.py

Saída:
    presentation/images/*.png
"""

import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "presentation", "images")
os.makedirs(OUT, exist_ok=True)


def read_rows(rel_path):
    with open(os.path.join(ROOT, *rel_path.split("/")), encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def as_float(value):
    if value in ("", "N/A", "NA"):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("gerado:", os.path.relpath(path, ROOT))


# 1) Salário mediano NOC 21232 por província
wages = read_rows("filtered/job_bank_wages_2025_noc_21232.csv")
wages = sorted(wages, key=lambda r: as_float(r["median_wage_cad_per_hour"]) or 0)
provinces = [r["province_code"] for r in wages]
medians = [as_float(r["median_wage_cad_per_hour"]) for r in wages]

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(provinces, medians, color="#176fb4")
for i, v in enumerate(medians):
    ax.text(v + 0.4, i, f"{v:.2f}", va="center", fontsize=9)
ax.set_xlabel("CAD por hora")
ax.set_title("Salário mediano de Software Developers (NOC 21232) por província")
ax.set_xlim(0, max(medians) * 1.12)
save(fig, "fig_salario_mediano.png")

# 2) Imigrantes brasileiros por período de imigração
sc = read_rows("filtered/statcan_98100307_brazil_provinces_territories.csv")
brazil = [r for r in sc if r["Place of birth (290)"] == "Brazil"]
period_cols = {
    "Before 1980": "Immigrant status and period of immigration (11):Before 1980[4]",
    "1980-1990": "Immigrant status and period of immigration (11):1980 to 1990[5]",
    "1991-2000": "Immigrant status and period of immigration (11):1991 to 2000[6]",
    "2001-2010": "Immigrant status and period of immigration (11):2001 to 2010[7]",
    "2011-2021": "Immigrant status and period of immigration (11):2011 to 2021[8]",
}
labels = list(period_cols)
values = [sum(as_float(r[col]) or 0 for r in brazil) for col in period_cols.values()]

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(labels, values, color="#0d2d53")
for i, v in enumerate(values):
    ax.text(i, v + 250, f"{v:,.0f}".replace(",", "."), ha="center", fontsize=9)
ax.set_ylabel("Imigrantes brasileiros")
ax.set_title("Imigrantes brasileiros por período de imigração (Censo 2021)")
save(fig, "fig_imigracao_periodos.png")

# 3) Comunidade brasileira por província
join = read_rows("canada_provinces_brazil_software_developer_wages.csv")
top = sorted(join, key=lambda r: -(as_float(r["brazilian_immigrants_2021"]) or 0))[:6]
provinces = [r["province"] for r in top]
counts = [as_float(r["brazilian_immigrants_2021"]) for r in top]

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(provinces, counts, color="#e4a700")
for i, v in enumerate(counts):
    ax.text(i, v + 150, f"{v:,.0f}".replace(",", "."), ha="center", fontsize=9)
ax.set_ylabel("Imigrantes brasileiros")
ax.set_title("Províncias com maior comunidade brasileira (Censo 2021)")
save(fig, "fig_comunidade_brasileira.png")

# 4) Inquilinos com moradia inacessível (gasto >= 30% da renda)
hsg = read_rows("filtered/statcan_98100258_housing_provinces_territories.csv")
unaff = [r for r in hsg if r["Housing indicators (9)"] == "Percent of households in unaffordable housing"]
unaff = sorted(unaff, key=lambda r: -(as_float(r["Tenure (4):Renter[3]"]) or 0))
provinces = [r["GEO"] for r in unaff]
renters = [as_float(r["Tenure (4):Renter[3]"]) for r in unaff]

fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(provinces[::-1], renters[::-1], color="#c0392b")
for i, v in enumerate(renters[::-1]):
    ax.text(v + 0.3, i, f"{v:.1f}%", va="center", fontsize=9)
ax.set_xlabel("% de inquilinos")
ax.set_title("Inquilinos com gasto ≥ 30% da renda em moradia (Censo 2021)")
ax.set_xlim(0, max(renters) * 1.12)
save(fig, "fig_moradia_inquilinos.png")

# 5) Salário mediano x comunidade brasileira
join = [r for r in join if as_float(r["median_developer_wage"]) is not None]
xs = [as_float(r["brazilian_immigrants_2021"]) for r in join]
ys = [as_float(r["median_developer_wage"]) for r in join]
names = [r["province"] for r in join]

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.scatter(xs, ys, color="#176fb4")
for name, x, y in zip(names, xs, ys):
    ax.annotate(name, (x, y), textcoords="offset points", xytext=(6, 4), fontsize=8)
ax.set_xlabel("Imigrantes brasileiros (2021)")
ax.set_ylabel("Salário mediano (CAD/h)")
ax.set_title("Salário mediano NOC 21232 × comunidade brasileira")
save(fig, "fig_salario_vs_brasileiros.png")

print("OK")
