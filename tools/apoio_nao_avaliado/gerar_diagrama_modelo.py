#!/usr/bin/env python3
"""Gera uma figura PNG do modelo dimensional para o relatório."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "figuras" / "modelo_constelacao.png"

W, H = 1800, 1250
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

def font(size, bold=False):
    return ImageFont.truetype(bold_path if bold else font_path, size)

def centered(text, x, y, f, fill="#14213d"):
    box = d.textbbox((0, 0), text, font=f)
    d.text((x - (box[2] - box[0]) / 2, y), text, font=f, fill=fill)

def box(x, y, w, h, title, lines, fact=False):
    fill = "#c1121f" if fact else "#e8f1f8"
    outline = "#780000" if fact else "#1d4e72"
    text = "white" if fact else "#14213d"
    d.rounded_rectangle((x, y, x + w, y + h), radius=16, fill=fill, outline=outline, width=4)
    title_size = 27 if len(title) <= 18 else 20
    centered(title, x + w / 2, y + 18, font(title_size, True), text)
    for i, line in enumerate(lines):
        d.text((x + 20, y + 62 + i * 27), line, font=font(18, fact), fill=text)

def link(a, b):
    d.line((a, b), fill="#52616b", width=4)

centered("Constelação de fatos: três Star Schemas com dimensões conformadas", W / 2, 32, font(35, True))
centered("PK = chave primária · FK = chave estrangeira · cada ligação representa cardinalidade 1:N", W / 2, 82, font(20))

# coordinates
facts = {"sal": (735, 245), "imig": (735, 555), "hab": (735, 865)}
dims = {
    "ocup": (140, 135), "tempo_sal": (140, 365), "disp": (140, 595), "prov": (1390, 135), "fonte": (1390, 365),
    "pais": (140, 765), "periodo": (140, 1005), "ten": (1390, 515), "indic": (1390, 805), "tempo_censo": (765, 1080),
}
for a, b in [((735, 310), (410, 210)), ((735, 340), (410, 440)), ((735, 365), (410, 655)), ((1065, 310), (1390, 210)), ((1065, 340), (1390, 440)),
             ((735, 620), (410, 840)), ((735, 650), (410, 1080)), ((1065, 620), (1390, 590)), ((1065, 650), (1390, 880)),
             ((900, 705), (900, 865)), ((900, 1015), (900, 1080))]:
    link(a, b)

for x, y in [(560, 255), (560, 360), (560, 500), (1190, 255), (1190, 360), (560, 760), (560, 980), (1190, 570), (1190, 815)]:
    d.text((x, y), "1:N", font=font(18, True), fill="#c1121f")

box(140, 135, 270, 120, "dim_ocupacao", ["PK  sk_ocupacao", "AK  cd_noc"])
box(140, 365, 270, 120, "dim_tempo_salario", ["PK  sk_tempo_salario", "AK  cd_periodo_referencia"])
box(140, 595, 270, 120, "dim_disponibilidade", ["PK  sk_disponibilidade", "AK  cd_disponibilidade"])
box(1390, 135, 270, 120, "dim_provincia", ["PK  sk_provincia", "AK  cd_dguid"])
box(1390, 365, 270, 120, "dim_fonte", ["PK  sk_fonte", "AK  cd_fonte"])
box(140, 765, 270, 120, "dim_pais_nascimento", ["PK  sk_pais_nascimento", "AK  cd_pais_nascimento"])
box(140, 1005, 270, 120, "dim_periodo_imigracao", ["PK  sk_periodo_imigracao", "AK  cd_periodo_imigracao"])
box(1390, 515, 270, 120, "dim_tenencia", ["PK  sk_tenencia", "AK  cd_tenencia"])
box(1390, 805, 270, 120, "dim_indicador_habitacao", ["PK  sk_indicador_habitacao", "AK  cd_indicador_habitacao"])
box(765, 1080, 270, 120, "dim_tempo_censo", ["PK  sk_tempo_censo", "AK  nr_ano_censo"])

box(735, 245, 330, 130, "fato_salario", ["PK  sk_fato_salario", "FK  provincia · ocupacao", "FK  tempo · disponibilidade · fonte"], True)
box(735, 555, 330, 130, "fato_imigracao", ["PK  sk_fato_imigracao", "FK  provincia · pais · periodo", "FK  tempo_censo · fonte"], True)
box(735, 865, 330, 130, "fato_habitacao", ["PK  sk_fato_habitacao", "FK  provincia · tenencia · indicador", "FK  tempo_censo · fonte"], True)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG")
print(OUT)
