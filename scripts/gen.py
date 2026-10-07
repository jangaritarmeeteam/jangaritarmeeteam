"""Genera los SVG animados del perfil. Estética: negro puro, carmesí, glitch."""
import random
from pathlib import Path
from html import escape

OUT = Path(__file__).parent.parent / "assets"
OUT.mkdir(exist_ok=True)
for old in OUT.glob("*.svg"):
    old.unlink()

BG, PANEL, BORDER = "#000000", "#050505", "#1c1c1c"
RED, RED_DIM, CYAN = "#ff1f3d", "#4a000c", "#00e5ff"
TEXT, DIM = "#f2f2f2", "#7d7d7d"
MONO = "'JetBrains Mono','Fira Code','SF Mono',Consolas,Menlo,monospace"
SANS = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
GLYPHS = "アイウエオカキクケコサシスセソタチツテトナニヌネノ0123456789ABCDEF<>/#$%&"

rnd = random.Random(7)


def defs_common():
    return f'''<filter id="glow" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="redglow" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur in="SourceAlpha" stdDeviation="7" result="b"/><feFlood flood-color="{RED}" flood-opacity=".9"/><feComposite in2="b" operator="in" result="g"/><feGaussianBlur in="SourceAlpha" stdDeviation="1.2" result="b2"/><feFlood flood-color="#fff" flood-opacity=".6"/><feComposite in2="b2" operator="in" result="w"/><feMerge><feMergeNode in="g"/><feMergeNode in="g"/><feMergeNode in="w"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="1"><animate attributeName="seed" values="1;2;3;4;5;6;7;8" dur=".8s" repeatCount="indefinite" calcMode="discrete"/></feTurbulence><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 0"/></filter>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".95"/></radialGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED}" stop-opacity="0"/><stop offset=".85" stop-color="{RED}" stop-opacity=".18"/><stop offset="1" stop-color="#fff" stop-opacity=".9"/></linearGradient>
<pattern id="scan" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="1" fill="#000" opacity=".45"/></pattern>'''


def brackets(x, y, w, h, s=18, col=RED, sw=2):
    p = [f"M{x},{y + s}V{y}H{x + s}", f"M{x + w - s},{y}H{x + w}V{y + s}",
         f"M{x + w},{y + h - s}V{y + h}H{x + w - s}", f"M{x + s},{y + h}H{x}V{y + h - s}"]
    return f'<path d="{" ".join(p)}" fill="none" stroke="{col}" stroke-width="{sw}"/>'


def rain(W, H, step=22, rows=16, dim=.55):
    cols = []
    for k in range(W // step + 1):
        x = k * step + 6
        dur = rnd.uniform(3.5, 9)
        delay = -rnd.uniform(0, dur)
        chars = []
        for j in range(rows):
            op = (j + 1) / rows
            col = "#ffd0d6" if j == rows - 1 else RED
            o = 1 if j == rows - 1 else op * dim
            chars.append(f'<text x="{x}" y="{j * 18}" fill="{col}" fill-opacity="{o:.2f}">{escape(rnd.choice(GLYPHS))}</text>')
        cols.append(f'<g style="animation:fall {dur:.2f}s linear {delay:.2f}s infinite">{"".join(chars)}</g>')
    return f'<g class="rain" transform="translate(0,-{rows * 18})">{"".join(cols)}</g>'


def header(name):
    W, H, T = 1000, 330, 10.0
    cx, ny, slot = W / 2, 150, 40
    n = len(name)
    x0 = cx - (n - 1) * slot / 2
    letters, css = [], []
    steps = 7
    for i, ch in enumerate(name):
        x = x0 + i * slot
        if ch == " ":
            continue
        start = 0.3 + i * 0.06
        # glifos aleatorios que se van mostrando antes de fijar la letra real
        for s in range(steps):
            a = (start + s * 0.07) / T * 100
            b = (start + (s + 1) * 0.07) / T * 100
            css.append(f".l{i}s{s}{{animation:l{i}s{s} {T}s infinite steps(1)}}@keyframes l{i}s{s}{{0%,{a:.2f}%{{opacity:0}}{a:.2f}%{{opacity:1}}{b:.2f}%,100%{{opacity:0}}}}")
            letters.append(f'<text x="{x}" y="{ny}" class="scr l{i}s{s}">{escape(rnd.choice(GLYPHS))}</text>')
        fin = (start + steps * 0.07) / T * 100
        css.append(f".l{i}f{{animation:l{i}f {T}s infinite steps(1)}}@keyframes l{i}f{{0%,{fin:.2f}%{{opacity:0}}{fin:.2f}%,97%{{opacity:1}}98%,100%{{opacity:0}}}}")
        letters.append(f'<text x="{x}" y="{ny}" class="nm l{i}f">{escape(ch)}</text>')
    final = "".join(f'<text x="{x0 + i * slot}" y="{ny}">{escape(c)}</text>' for i, c in enumerate(name) if c != " ")
    # franjas de glitch: copias recortadas que se desplazan en momentos puntuales
    bands = [(ny - 48, 14), (ny - 30, 10), (ny - 16, 18), (ny + 2, 9)]
    slices, clips = [], []
    for j, (by, bh) in enumerate(bands):
        clips.append(f'<clipPath id="b{j}"><rect x="0" y="{by}" width="{W}" height="{bh}"/></clipPath>')
        col = [CYAN, RED, "#fff", CYAN][j]
        slices.append(f'<g clip-path="url(#b{j})"><g class="nm sl{j}" fill="{col}">{final}</g></g>')
        dx = [-22, 16, -9, 26][j]
        css.append(f".sl{j}{{opacity:0;animation:sl{j} {T}s infinite steps(1)}}@keyframes sl{j}{{0%,40%{{opacity:0}}40.5%{{opacity:1;transform:translateX({dx}px)}}41.5%{{transform:translateX({-dx // 2}px)}}42.5%,71%{{opacity:0;transform:none}}71.5%{{opacity:1;transform:translateX({-dx}px)}}72.3%,100%{{opacity:0}}}}")
    rgb = (f'<g class="nm rgb1" fill="{CYAN}">{final}</g><g class="nm rgb2" fill="{RED}">{final}</g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{defs_common()}{"".join(clips)}
<clipPath id="frame"><rect x="0" y="0" width="{W}" height="{H}" rx="16"/></clipPath></defs>
<style>
  text{{font-family:{MONO}}}
  .rain text{{font-size:15px}}
  @keyframes fall{{from{{transform:translateY(0)}}to{{transform:translateY({H + 300}px)}}}}
  .nm,.scr{{font:800 58px {MONO};text-anchor:middle}}
  .nm{{fill:{TEXT}}} .scr{{fill:{RED}}}
  .rgb1{{opacity:.7;animation:r1 {T}s infinite steps(1)}} .rgb2{{opacity:.7;animation:r2 {T}s infinite steps(1)}}
  @keyframes r1{{0%,14%{{opacity:0}}14.5%,97%{{opacity:.3;transform:translate(-1.5px,0)}}40.5%{{transform:translate(-9px,1px)}}42.5%{{transform:translate(-1.5px,0)}}98%,100%{{opacity:0}}}}
  @keyframes r2{{0%,14%{{opacity:0}}14.5%,97%{{opacity:.3;transform:translate(1.5px,0)}}40.5%{{transform:translate(9px,-1px)}}42.5%{{transform:translate(1.5px,0)}}98%,100%{{opacity:0}}}}
  .sweep{{animation:sweep 4s cubic-bezier(.6,0,.4,1) infinite}}
  @keyframes sweep{{0%{{transform:translateY(-140px)}}100%{{transform:translateY({H + 20}px)}}}}
  .sub{{font:600 15px {MONO};letter-spacing:7px;fill:{RED}}}
  .hud{{font:500 11px {MONO};letter-spacing:2px;fill:{DIM}}}
  .dot{{animation:blink 1.2s steps(1) infinite}} @keyframes blink{{50%{{opacity:0}}}}
  .typ{{animation:typ {T}s infinite}}
  @keyframes typ{{0%,16%{{transform:translateX(0);animation-timing-function:steps(36,end)}}30%,97%{{transform:translateX(560px)}}100%{{transform:translateX(0)}}}}
  .flick{{animation:flick 6s infinite}} @keyframes flick{{0%,30%,32%,70%,71%,100%{{opacity:1}}31%,70.5%{{opacity:.3}}}}
  {"".join(css)}
</style>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{BG}"/>
{rain(W, H)}
<rect width="{W}" height="{H}" fill="url(#vig)"/>
<rect x="{cx - 420}" y="{ny - 80}" width="840" height="140" fill="{BG}" opacity=".72" filter="url(#soft)"/>
<g class="flick">
  <g filter="url(#redglow)">{"".join(letters)}</g>
  {rgb}{"".join(slices)}
</g>
<line x1="{cx - 300}" y1="{ny + 34}" x2="{cx + 300}" y2="{ny + 34}" stroke="{RED}" stroke-width="1" opacity=".6"/>
<g>
  <text x="{cx - 280}" y="{ny + 68}" class="sub">&gt; SOFTWARE PARA LA INDUSTRIA</text>
  <rect class="typ" x="{cx - 262}" y="{ny + 52}" width="580" height="22" fill="{BG}"/>
</g>
<rect x="30" y="28" width="190" height="24" fill="#000" opacity=".85"/><rect x="{W - 240}" y="28" width="210" height="24" fill="#000" opacity=".85"/><rect x="30" y="{H - 46}" width="300" height="24" fill="#000" opacity=".85"/><rect x="{W - 360}" y="{H - 46}" width="330" height="24" fill="#000" opacity=".85"/>
<text x="40" y="44" class="hud">[ MEETEAM // CO ]</text>
<text x="{W - 40}" y="44" class="hud" text-anchor="end">SYS.STATUS <tspan fill="{RED}" class="dot">●</tspan> ONLINE</text>
<text x="40" y="{H - 30}" class="hud">BUILD 2026.10 · NODE // PY // TS</text>
<text x="{W - 40}" y="{H - 30}" class="hud" text-anchor="end">MANUFACTURA · CUMPLIMIENTO · IA</text>
{brackets(20, 20, W - 40, H - 40, 26)}
<rect class="sweep" x="0" y="0" width="{W}" height="120" fill="url(#beam)" opacity=".55"/>
<rect width="{W}" height="{H}" fill="url(#scan)"/>
<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".07"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{BORDER}"/>
</svg>'''


TERM = [
    ("cmd", "whoami"),
    ("out", "José David Angarita — Software para la industria @ Meeteam"),
    ("cmd", "cat stack.txt"),
    ("out", "TypeScript · Next.js · NestJS · FastAPI · PostgreSQL · Docker"),
    ("cmd", "ls productos/"),
    ("dir", "manufactura/   cumplimiento/   talento-humano/   datos-ia/"),
    ("cmd", "integraciones --list"),
    ("out", "SAP · Business Central · SIESA · SQL Server · Shopify · Twilio"),
    ("cmd", "echo $MISION"),
    ("hl", "Llevo la planta del Excel al software en producción."),
]


def terminal():
    W, CW, LH, X0, Y0 = 1000, 9.1, 26, 36, 84
    H = Y0 + LH * len(TERM) + 28
    T, now = 22.0, 0.6
    css, body = [], []
    for i, (kind, txt) in enumerate(TERM):
        y = Y0 + i * LH
        if kind == "cmd":
            body.append(f'<text x="{X0}" y="{y}" class="pr">❯</text>')
            tx, n = X0 + 22, len(txt)
            dur = n * 0.07
            s, e = now / T * 100, (now + dur) / T * 100
            css.append(f".o{i}{{animation:k{i} {T}s infinite}}@keyframes k{i}{{0%,{s:.2f}%{{transform:translateX(0);animation-timing-function:steps({n},end)}}{e:.2f}%,96%{{transform:translateX({n * CW + 12:.1f}px)}}97%,100%{{transform:translateX(0)}}}}")
            body.append(f'<text x="{tx}" y="{y}" class="cmd">{escape(txt)}</text><rect class="o{i}" x="{tx - 2}" y="{y - 17}" width="{W - tx}" height="{LH}" fill="{PANEL}"/>')
            now += dur + 0.35
        else:
            s = now / T * 100
            css.append(f".o{i}{{animation:k{i} {T}s infinite steps(1)}}@keyframes k{i}{{0%{{opacity:0}}{s:.2f}%,96%{{opacity:1}}97%,100%{{opacity:0}}}}")
            body.append(f'<text x="{X0}" y="{y}" class="{kind} o{i}">{escape(txt)}</text>')
            now += 0.9
    cy = Y0 + (len(TERM) - 1) * LH
    cx = X0 + len(TERM[-1][1]) * CW + 6
    show = (now - 0.9) / T * 100
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{defs_common()}
<clipPath id="inner"><rect x="2" y="46" width="{W - 4}" height="{H - 48}"/></clipPath>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>
<style>
  text{{font:500 15px {MONO};white-space:pre}}
  .pr{{fill:{RED};font-weight:700}} .cmd{{fill:{TEXT}}} .out{{fill:{DIM}}}
  .dir{{fill:{RED}}} .hl{{fill:#fff;font-weight:700}}
  .ttl{{font:500 12px {MONO};letter-spacing:2px;fill:{DIM}}}
  .cur{{fill:{RED};animation:blink 1s steps(1) infinite, show {T}s infinite steps(1)}}
  @keyframes blink{{50%{{fill-opacity:0}}}}
  @keyframes show{{0%{{opacity:0}}{show:.2f}%,96%{{opacity:1}}97%,100%{{opacity:0}}}}
  .sweep{{animation:sweep 5s linear infinite}}
  @keyframes sweep{{from{{transform:translateY(-120px)}}to{{transform:translateY({H}px)}}}}
  {"".join(css)}
</style>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{PANEL}"/>
<rect width="{W}" height="44" fill="#0b0b0b"/><line x1="0" y1="44" x2="{W}" y2="44" stroke="{BORDER}"/>
<circle cx="26" cy="22" r="5.5" fill="{RED}"/><circle cx="46" cy="22" r="5.5" fill="#3a3a3a"/><circle cx="66" cy="22" r="5.5" fill="#3a3a3a"/>
<text x="{W / 2}" y="27" text-anchor="middle" class="ttl">ROOT@MEETEAM — ~/perfil</text>
<g clip-path="url(#inner)">{"".join(body)}</g>
<rect class="cur" x="{cx:.1f}" y="{cy - 15}" width="9" height="19" filter="url(#soft)"/>
<rect class="sweep" x="0" y="0" width="{W}" height="90" fill="url(#beam)" opacity=".25"/>
<rect width="{W}" height="{H}" fill="url(#scan)" opacity=".6"/>
<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".05"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{BORDER}"/>
{brackets(8, 8, W - 16, H - 16, 14, RED, 1.5)}
</svg>'''


CARDS = [
    ("MANUFACTURA Y PLANTA", ["Taller de herramentales y vida útil", "Producto no conforme (PNC)", "Entrenamiento y polivalencia",
                              "Mejora continua · Kaizen", "Monitoreo de energía", "Gestión del cambio · SIG"]),
    ("CUMPLIMIENTO Y FINANZAS", ["SAGRILAFT · vinculación de terceros", "Gestión técnica y nutricional", "Retegarantías · Business Central",
                                 "Registro de facturas · DIAN"]),
    ("TALENTO HUMANO", ["Pruebas psicotécnicas con IA", "DISC · CMT · VALANTI · IPV", "Gestión de vacaciones"]),
    ("DATOS E INTELIGENCIA ARTIFICIAL", ["BI e-commerce · Shopify · Meta Ads", "Agente de voz y WhatsApp", "Compras inteligentes · SAP",
                                         "Cotizador para manufactura"]),
]


def cards():
    W, CWD, CH, G = 1000, 488, 236, 24
    H = CH * 2 + G
    out = []
    for i, (title, items) in enumerate(CARDS):
        x, y = (i % 2) * (CWD + G), (i // 2) * (CH + G)
        lis = "".join(f'<text x="{x + 30}" y="{y + 96 + j * 23}" class="it"><tspan fill="{RED}">▸ </tspan>{escape(s)}</text>' for j, s in enumerate(items))
        out.append(f'''<g>
<rect x="{x + .5}" y="{y + .5}" width="{CWD - 1}" height="{CH - 1}" rx="10" fill="{PANEL}" stroke="{BORDER}"/>
<text x="{x + CWD - 24}" y="{y + CH - 20}" class="num" text-anchor="end">0{i + 1}</text>
<g style="animation:pulse 4s ease-in-out {-i}s infinite">{brackets(x + 8, y + 8, CWD - 16, CH - 16, 16, RED, 2)}</g>
<text x="{x + 30}" y="{y + 44}" class="mono">// MÓDULO 0{i + 1}</text>
<text x="{x + 30}" y="{y + 68}" class="h" filter="url(#soft)">{title}</text>
{lis}
<g clip-path="url(#c{i})"><rect class="beam" style="animation-delay:{-i * 0.9}s" x="{x - 160}" y="{y}" width="160" height="{CH}" fill="url(#hbeam)"/></g>
</g>''')
    clips = "".join(f'<clipPath id="c{i}"><rect x="{(i % 2) * (CWD + G)}" y="{(i // 2) * (CH + G)}" width="{CWD}" height="{CH}" rx="10"/></clipPath>' for i in range(4))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{defs_common()}{clips}
<linearGradient id="hbeam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{RED}" stop-opacity="0"/><stop offset=".9" stop-color="{RED}" stop-opacity=".12"/><stop offset="1" stop-color="#fff" stop-opacity=".5"/></linearGradient></defs>
<style>
  .h{{font:800 18px {SANS};letter-spacing:2.5px;fill:{RED}}}
  .mono{{font:500 11px {MONO};letter-spacing:2px;fill:{DIM}}}
  .it{{font:500 15px {SANS};fill:{TEXT}}}
  .num{{font:900 110px {SANS};fill:none;stroke:{RED_DIM};stroke-width:1.5}}
  .beam{{animation:beam 3.6s cubic-bezier(.7,0,.3,1) infinite}}
  @keyframes beam{{0%{{transform:translateX(0)}}60%,100%{{transform:translateX({CWD + 200}px)}}}}
  @keyframes pulse{{50%{{opacity:.25}}}}
</style>
{"".join(out)}
</svg>'''


def ecg():
    W, H, mid = 1000, 120, 62
    pts, x = [], 0
    while x < W:
        pts += [f"{x},{mid}", f"{x + 60},{mid}", f"{x + 70},{mid - 8}", f"{x + 80},{mid}", f"{x + 92},{mid}",
                f"{x + 98},{mid + 14}", f"{x + 108},{mid - 46}", f"{x + 118},{mid + 26}", f"{x + 126},{mid}",
                f"{x + 150},{mid}", f"{x + 162},{mid - 12}", f"{x + 176},{mid}"]
        x += 200
    d = "M" + " L".join(pts)
    L = 3200
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{defs_common()}
<linearGradient id="fadeX" x1="0" x2="1"><stop offset="0" stop-color="{BG}"/><stop offset=".1" stop-color="{BG}" stop-opacity="0"/><stop offset=".9" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>
<style>
  .ln{{fill:none;stroke:{RED};stroke-width:2.2;stroke-dasharray:{L};stroke-dashoffset:{L};animation:draw 3.2s linear infinite}}
  .bg{{fill:none;stroke:{RED_DIM};stroke-width:1}}
  @keyframes draw{{to{{stroke-dashoffset:0}}}}
  .t{{font:600 12px {MONO};letter-spacing:6px;fill:{DIM}}}
  .dot{{animation:b 1s steps(1) infinite}} @keyframes b{{50%{{opacity:0}}}}
</style>
<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>
<path class="bg" d="{d}"/>
<path class="ln" d="{d}" filter="url(#glow)"/>
<rect width="{W}" height="{H}" fill="url(#fadeX)"/>
<text x="{W / 2}" y="{H - 10}" text-anchor="middle" class="t"><tspan fill="{RED}" class="dot">●</tspan> SYSTEM ONLINE — SIEMPRE CONSTRUYENDO</text>
</svg>'''


(OUT / "header.svg").write_text(header("JOSÉ DAVID ANGARITA"))
(OUT / "terminal.svg").write_text(terminal())
(OUT / "products.svg").write_text(cards())
(OUT / "pulse.svg").write_text(ecg())
for p in sorted(OUT.iterdir()):
    print(p.name, p.stat().st_size)
