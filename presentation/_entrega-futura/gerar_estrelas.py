#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera um slide por Star Schema no formato classico de modelo de dados:
tabela fato ao centro, dimensoes em volta, colunas visiveis e setas PK -> FK.
Tudo derivado de sql/script_oracle.sql para nao divergir do DDL."""
import io, os, re, sys

ROOT = "/Users/eliezirmoreira/Documents/IFAL/canada-developer-immigration-dw"
SQL = os.path.join(ROOT, "sql/script_oracle.sql")
HTML = os.path.join(ROOT, "presentation/index.html")

LINHAS = {"dim_provincia": 13, "dim_ocupacao": 1, "dim_tempo_salario": 1,
          "dim_disponibilidade_salario": 3, "dim_tempo_censo": 1,
          "dim_pais_nascimento": 2, "dim_periodo_imigracao": 5, "dim_tenencia": 4,
          "dim_indicador_habitacao": 9, "dim_fonte": 3,
          "fato_salario": 13, "fato_imigracao": 130, "fato_habitacao": 468}

CONFORMADAS = {"dim_provincia", "dim_fonte", "dim_tempo_censo"}

# geometria
BW_D, BW_F = 300, 312          # largura das caixas
HDR, ROW = 23, 15.5            # altura do cabecalho e de cada coluna
X_L, X_F, X_R = 0, 408, 828    # colunas esquerda / fato / direita
GAP = 14

ESTRELAS = [
    dict(fato="fato_salario", titulo="Star Schema · fato_salario",
         esq=["dim_provincia", "dim_ocupacao", "dim_fonte"],
         dir=["dim_tempo_salario", "dim_disponibilidade_salario"],
         bolha="A estrela do <strong>salário</strong>: cinco dimensões apontando para o fato. "
               "<code>dim_disponibilidade_salario</code> é o que permite ter <strong>13 linhas</strong> "
               "mesmo com só 9 jurisdições publicando valor. \U0001F4BC"),
    dict(fato="fato_imigracao", titulo="Star Schema · fato_imigracao",
         esq=["dim_provincia", "dim_pais_nascimento", "dim_fonte"],
         dir=["dim_periodo_imigracao", "dim_tempo_censo"],
         bolha="A estrela da <strong>comunidade</strong>. <code>qt_imigrantes</code> é a única medida, "
               "e é <strong>aditiva</strong> — some por província, por país ou por período. \U0001F465"),
    dict(fato="fato_habitacao", titulo="Star Schema · fato_habitacao",
         esq=["dim_provincia", "dim_tenencia", "dim_fonte"],
         dir=["dim_indicador_habitacao", "dim_tempo_censo"],
         bolha="A estrela da <strong>moradia</strong>. <code>vl_medida</code> guarda contagem "
               "<i>ou</i> percentual — quem diz qual é <code>dim_indicador_habitacao.tp_medida</code>. \U0001F3E0"),
]


def ler_ddl():
    s = io.open(SQL, encoding="utf-8").read()
    t = {}
    for m in re.finditer(r'CREATE TABLE (dim_\w+|fato_\w+) \((.*?)\n\) TABLESPACE', s, re.S):
        nome, corpo = m.group(1), m.group(2)
        pk = re.search(r'PRIMARY KEY \((\w+)\)', corpo)
        pk = pk.group(1) if pk else None
        ak = re.search(r'CONSTRAINT AK_\w+ UNIQUE \(([^)]+)\)', corpo)
        ak = {a.strip() for a in ak.group(1).split(',')} if ak else set()
        fk = dict(re.findall(r'FOREIGN KEY \((\w+)\)\s*\n?\s*REFERENCES (\w+)', corpo))
        cols = []
        for l in corpo.splitlines():
            mm = re.match(r'\s+(\w+)\s+(NUMBER\([\d,]+\)|NUMBER|VARCHAR2\(\d+\)|DATE)', l)
            if mm:
                c, tp = mm.group(1), mm.group(2)
                papel = "PK" if c == pk else ("FK" if c in fk else ("AK" if c in ak else ""))
                cols.append((c, tp, papel))
        t[nome] = dict(cols=cols, pk=pk, fk=fk)
    return t


T = ler_ddl()
alt = lambda n: HDR + len(T[n]["cols"]) * ROW


def caixa(nome, x, y, w, fato=False):
    """Desenha a tabela e devolve o y do centro de cada coluna."""
    cols = T[nome]["cols"]
    h = alt(nome)
    cor = "#c92832" if fato else "#1d3557"
    p = ['<g>']
    p.append('<rect x="%g" y="%g" width="%g" height="%g" rx="4" fill="#fff" stroke="%s" '
             'stroke-width="%s"/>' % (x, y, w, h, "#c92832" if nome in CONFORMADAS else "#c9d3dd",
                                      "1.6" if nome in CONFORMADAS else "1"))
    p.append('<path d="M%g %g h%g v%g a4 4 0 0 1 -4 4 h-%g a4 4 0 0 1 -4 -4 z" fill="%s" '
             'transform="translate(0,0)"/>'
             % (x, y + HDR, w, -(HDR - 4), w - 8, cor))
    p.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s"/>' % (x, y + 4, w, HDR - 4, cor))
    p.append('<rect x="%g" y="%g" width="%g" height="8" rx="4" fill="%s"/>' % (x, y, w, cor))
    p.append('<text class="dh" x="%g" y="%g">%s</text>' % (x + 10, y + 16, nome))
    n = LINHAS.get(nome)
    rot = "" if n is None else ("1 linha" if n == 1 else "%s linhas" % n)
    p.append('<text class="dn" x="%g" y="%g" text-anchor="end">%s</text>'
             % (x + w - 9, y + 16, rot))
    centros = {}
    for i, (c, tp, papel) in enumerate(cols):
        ry = y + HDR + i * ROW
        cy = ry + ROW / 2 + 3.2
        if i:
            p.append('<line class="dsep" x1="%g" y1="%g" x2="%g" y2="%g"/>' % (x, ry, x + w, ry))
        if papel in ("PK", "AK"):
            p.append('<rect x="%g" y="%g" width="%g" height="%g" fill="#f4f7fa"/>' % (x + 1, ry, w - 2, ROW))
        cls = "dc pk" if papel == "PK" else ("dc fk" if papel == "FK" else ("dc ak" if papel == "AK" else "dc"))
        p.append('<text class="%s" x="%g" y="%g">%s</text>' % (cls, x + 10, cy, c))
        p.append('<text class="dt" x="%g" y="%g" text-anchor="end">%s</text>' % (x + w - 9, cy, tp))
        centros[c] = cy - 3.2
    p.append('</g>')
    return "\n            ".join(p), centros, h


def montar(est):
    fato, esq, dire = est["fato"], est["esq"], est["dir"]
    hF = alt(fato)
    hE = sum(alt(n) for n in esq) + GAP * (len(esq) - 1)
    hD = sum(alt(n) for n in dire) + GAP * (len(dire) - 1)
    total = max(hE, hD, hF)

    partes, centros = [], {}
    y = (total - hE) / 2
    for n in esq:
        svg, c, h = caixa(n, X_L, y, BW_D)
        partes.append(svg); centros[n] = (c, X_L + BW_D, y)
        y += h + GAP
    y = (total - hD) / 2
    for n in dire:
        svg, c, h = caixa(n, X_R, y, BW_D)
        partes.append(svg); centros[n] = (c, X_R, y)
        y += h + GAP
    yF = (total - hF) / 2
    svgF, cF, _ = caixa(fato, X_F, yF, BW_F, fato=True)

    # setas PK da dimensao -> FK do fato
    setas = []
    for col, alvo in T[fato]["fk"].items():
        if alvo not in centros:
            continue
        cdim, bordaX, _ = centros[alvo]
        y1 = cdim[T[alvo]["pk"]]
        y2 = cF[col]
        esquerda = alvo in esq
        x1 = bordaX
        x2 = X_F if esquerda else X_F + BW_F
        dx = abs(x2 - x1) * 0.55
        c1 = x1 + (dx if esquerda else -dx)
        c2 = x2 - (dx if esquerda else -dx)
        setas.append('<path class="dln" d="M%g %g C%g %g %g %g %g %g" marker-end="url(#pt)"/>'
                     % (x1, y1, c1, y1, c2, y2, x2 + (-6 if esquerda else 6), y2))

    corpo = "\n            ".join(partes + setas) + "\n            " + svgF
    return corpo, total


def slide(est, num):
    corpo, total = montar(est)
    return '''      <section class="slide" data-title="%(t)s">
        <div class="ob-stage top">
          <div class="ob-speak">
            <div class="ob-duo sm mascot">\U0001F9AB</div>
            <div class="bubble">%(b)s</div>
          </div>
          <svg class="star-svg step" viewBox="-8 -6 1144 %(h)g" role="img" aria-label="%(t)s">
            <defs>
              <marker id="pt" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
                <path d="M0 0 L10 5 L0 10 z" fill="#3d6ea8"/>
              </marker>
              <style>
                .dh{font-family:'DM Mono',monospace;font-size:11.5px;font-weight:500;fill:#fff}
                .dn{font-family:'DM Mono',monospace;font-size:8px;fill:rgba(255,255,255,.72)}
                .dc{font-family:'DM Mono',monospace;font-size:9.5px;fill:#25313f}
                .dc.pk{font-weight:600;fill:#0d1b2a}
                .dc.ak{font-weight:600;fill:#8a6412}
                .dc.fk{fill:#3d6ea8}
                .dt{font-family:'DM Mono',monospace;font-size:8.2px;fill:#93a1b0}
                .dsep{stroke:#edf1f5;stroke-width:1}
                .dln{stroke:#3d6ea8;stroke-width:1.5;fill:none}
              </style>
            </defs>
            %(c)s
          </svg>
        </div>
        <div class="corner-num">%(n)s</div>
      </section>
''' % dict(t=est["titulo"], b=est["bolha"], h=total + 12, c=corpo, n=num)


novos = "\n".join(slide(e, "%02d" % (12 + i)) for i, e in enumerate(ESTRELAS))

src = io.open(HTML, encoding="utf-8").read()
# idempotente: 1a execucao troca as grades; nas seguintes, as proprias estrelas
grades = re.compile(
    r' *<section class="slide" data-title="Fatos \u00b7 coluna a coluna">.*?'
    r'<section class="slide" data-title="Dimens\u00f5es \u00b7 coluna a coluna">.*?</section>\n', re.S)
estrelas = re.compile(
    r' *<section class="slide" data-title="Star Schema \u00b7 fato_salario">.*?'
    r'<section class="slide" data-title="Star Schema \u00b7 fato_habitacao">.*?</section>\n', re.S)
alvo = grades if grades.search(src) else estrelas
if not alvo.search(src):
    sys.exit("!! nao encontrei os slides para substituir")
src = alvo.sub(lambda m: novos, src, count=1)
io.open(HTML, "w", encoding="utf-8").write(src)

print("Tres estrelas geradas a partir do DDL:")
for e in ESTRELAS:
    print("  - %-16s %d colunas, %d dimensoes" % (e["fato"], len(T[e["fato"]]["cols"]),
                                                  len(e["esq"]) + len(e["dir"])))
