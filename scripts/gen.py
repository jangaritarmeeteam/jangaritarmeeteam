"""Genera los SVG animados del perfil (versiones dark y light)."""
from pathlib import Path
from html import escape

OUT = Path(__file__).parent.parent / "assets"
OUT.mkdir(exist_ok=True)

THEMES = {
    "dark": dict(bg="#0d1117", panel="#0b0f19", text="#e6edf3", dim="#8b949e",
                 a="#00f0ff", b="#ff2bd6", c="#8b5cf6", ok="#39ff14", grid="#8b5cf6",
                 glow=1.0, chrome="#161b22", border="#30363d"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", text="#0f172a", dim="#57606a",
                  a="#0891b2", b="#c026d3", c="#6d28d9", ok="#15803d", grid="#a78bfa",
                  glow=0.35, chrome="#eaeef2", border="#d0d7de"),
}
MONO = "'JetBrains Mono','Fira Code','SF Mono',Consolas,Menlo,monospace"
SANS = "'Segoe UI','Helvetica Neue',Arial,sans-serif"


def header(t, name):
    W, H, HZ = 1000, 280, 200
    hlines = "".join(f'<line x1="0" y1="{HZ + i * 14}" x2="{W}" y2="{HZ + i * 14}"/>' for i in range(8))
    vlines = "".join(f'<line x1="{W/2}" y1="{HZ}" x2="{W/2 + k * 140}" y2="{H}"/>' for k in range(-12, 13))
    sun_stripes = "".join(f'<rect x="380" y="{150 + i * 9}" width="240" height="{1 + i * 0.8:.1f}" fill="{t["bg"]}"/>' for i in range(6))
    dark = t is THEMES["dark"]
    name_glow = ' filter="url(#glow)"' if dark else ""
    scan = f'<rect width="{W}" height="{H}" fill="url(#scan)"/>' if dark else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["b"]}"/><stop offset="1" stop-color="{t["c"]}"/></linearGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["bg"]}" stop-opacity="1"/><stop offset=".35" stop-color="{t["bg"]}" stop-opacity="0"/></linearGradient>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="{6 * t["glow"]:.1f}" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="floor"><rect x="0" y="{HZ}" width="{W}" height="{H - HZ}"/></clipPath>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".18"/></pattern>
</defs>
<style>
  .name{{font:800 56px {SANS};letter-spacing:4px;fill:{t["text"]};animation:flicker 7s infinite}}
  .sub{{font:600 17px {MONO};letter-spacing:6px;fill:{t["a"]}}}
  .g1{{fill:{t["a"]};opacity:0;animation:gl1 4s infinite steps(1)}}
  .g2{{fill:{t["b"]};opacity:0;animation:gl2 4s infinite steps(1)}}
  .moving{{animation:move 1.2s linear infinite}}
  .sunbox{{animation:pulse 5s ease-in-out infinite;transform-origin:500px 200px}}
  @keyframes move{{from{{transform:translateY(0)}}to{{transform:translateY(14px)}}}}
  @keyframes pulse{{50%{{opacity:.75}}}}
  @keyframes flicker{{0%,19%,21%,62%,64%,100%{{opacity:1}}20%,63%{{opacity:.55}}}}
  @keyframes gl1{{0%,86%{{opacity:0;transform:none}}87%{{opacity:.85;transform:translate(-5px,2px)}}89%{{opacity:.85;transform:translate(4px,-1px)}}91%{{opacity:.85;transform:translate(-2px,0)}}93%,100%{{opacity:0}}}}
  @keyframes gl2{{0%,86%{{opacity:0;transform:none}}87%{{opacity:.85;transform:translate(5px,-2px)}}89%{{opacity:.85;transform:translate(-4px,2px)}}91%{{opacity:.85;transform:translate(3px,1px)}}93%,100%{{opacity:0}}}}
</style>
<rect width="{W}" height="{H}" fill="{t["bg"]}"/>
<g class="sunbox" opacity=".9"><circle cx="500" cy="200" r="120" fill="url(#sun)" opacity="{0.55 if t is THEMES["dark"] else 0.35}"/>{sun_stripes}</g>
<rect x="0" y="{HZ}" width="{W}" height="{H - HZ}" fill="{t["bg"]}"/>
<g clip-path="url(#floor)" stroke="{t["grid"]}" stroke-width="1" opacity=".55">
  <g class="moving">{hlines}<line x1="0" y1="{HZ - 14}" x2="{W}" y2="{HZ - 14}"/></g>{vlines}
</g>
<rect x="0" y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#fade)"/>
<line x1="0" y1="{HZ}" x2="{W}" y2="{HZ}" stroke="{t["b"]}" stroke-width="2" filter="url(#glow)"/>
<g text-anchor="middle">
  <text class="name g1" x="500" y="118">{escape(name)}</text>
  <text class="name g2" x="500" y="118">{escape(name)}</text>
  <text class="name" x="500" y="118"{name_glow}>{escape(name)}</text>
  <text class="sub" x="500" y="160">SOFTWARE PARA LA INDUSTRIA · MEETEAM</text>
</g>
{scan}
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


def terminal(t):
    W, CW, LH, X0, Y0 = 1000, 9.1, 26, 32, 78
    H = Y0 + LH * len(TERM) + 24
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
            body.append(f'<text x="{tx}" y="{y}" class="cmd">{escape(txt)}</text><rect class="o{i}" x="{tx - 2}" y="{y - 17}" width="{W - tx}" height="{LH}" fill="{t["panel"]}"/>')
            now += dur + 0.35
        else:
            s = now / T * 100
            cls = {"out": "out", "dir": "dir", "hl": "hl"}[kind]
            css.append(f".o{i}{{animation:k{i} {T}s infinite steps(1)}}@keyframes k{i}{{0%{{opacity:0}}{s:.2f}%,96%{{opacity:1}}97%,100%{{opacity:0}}}}")
            body.append(f'<text x="{X0}" y="{y}" class="{cls} o{i}">{escape(txt)}</text>')
            now += 0.9
    cy = Y0 + (len(TERM) - 1) * LH
    cx = X0 + len(TERM[-1][1]) * CW + 6
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><clipPath id="inner"><rect x="7" y="42" width="{W - 14}" height="{H - 49}"/></clipPath><filter id="glow"><feGaussianBlur stdDeviation="{2.5 * t["glow"]:.1f}" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>
  text{{font:500 15px {MONO};white-space:pre}}
  .pr{{fill:{t["b"]};font-weight:700}} .cmd{{fill:{t["text"]}}} .out{{fill:{t["dim"]}}}
  .dir{{fill:{t["a"]}}} .hl{{fill:{t["ok"]};font-weight:700}}
  .ttl{{font:500 13px {MONO};fill:{t["dim"]}}}
  .cur{{fill:{t["ok"]};animation:blink 1s steps(1) infinite, show {T}s infinite steps(1)}}
  @keyframes blink{{50%{{fill-opacity:0}}}}
  @keyframes show{{0%{{opacity:0}}{(now - 0.9) / T * 100:.2f}%,96%{{opacity:1}}97%,100%{{opacity:0}}}}
  {"".join(css)}
</style>
<rect x="5" y="5" width="{W - 10}" height="{H - 10}" rx="12" fill="{t["panel"]}" stroke="{t["a"]}" stroke-opacity=".6" filter="url(#glow)"/>
<rect x="5" y="5" width="{W - 10}" height="36" rx="12" fill="{t["chrome"]}"/><rect x="5" y="30" width="{W - 10}" height="11" fill="{t["chrome"]}"/>
<circle cx="24" cy="20" r="6" fill="#ff5f56"/><circle cx="44" cy="20" r="6" fill="#ffbd2e"/><circle cx="64" cy="20" r="6" fill="#27c93f"/>
<text x="{W/2}" y="24" text-anchor="middle" class="ttl">jose@meeteam: ~</text>
<g clip-path="url(#inner)">{"".join(body)}</g>
<rect class="cur" x="{cx:.1f}" y="{cy - 15}" width="9" height="19"/>
</svg>'''


CARDS = [
    ("MANUFACTURA Y PLANTA", "a", ["Taller de herramentales y vida útil", "Producto no conforme (PNC)", "Entrenamiento y polivalencia",
                                   "Mejora continua · Kaizen", "Monitoreo de energía", "Gestión del cambio · SIG"]),
    ("CUMPLIMIENTO Y FINANZAS", "b", ["SAGRILAFT · vinculación de terceros", "Gestión técnica y nutricional", "Retegarantías · Business Central",
                                      "Registro de facturas · DIAN"]),
    ("TALENTO HUMANO", "c", ["Pruebas psicotécnicas con IA", "DISC · CMT · VALANTI · IPV", "Gestión de vacaciones"]),
    ("DATOS E INTELIGENCIA ARTIFICIAL", "ok", ["BI e-commerce · Shopify · Meta Ads", "Agente de voz y WhatsApp", "Compras inteligentes · SAP",
                                               "Cotizador para manufactura"]),
]


def cards(t):
    W, CWD, CH, G = 1000, 488, 230, 24
    H = CH * 2 + G
    per = 2 * (CWD + CH)
    tglow = ' filter="url(#glow)"' if t is THEMES["dark"] else ""
    out = []
    for i, (title, col, items) in enumerate(CARDS):
        x, y = (i % 2) * (CWD + G), (i // 2) * (CH + G)
        c = t[col]
        lis = "".join(f'<text x="{x + 28}" y="{y + 82 + j * 24}" class="it"><tspan fill="{c}">▸ </tspan>{escape(s)}</text>' for j, s in enumerate(items))
        out.append(f'''<g>
<rect x="{x + 1}" y="{y + 1}" width="{CWD - 2}" height="{CH - 2}" rx="14" fill="{t["panel"]}" stroke="{t["border"]}"/>
<rect x="{x + 1}" y="{y + 1}" width="{CWD - 2}" height="{CH - 2}" rx="14" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="160 {per - 160}" filter="url(#glow)" style="animation:run 6s linear infinite;animation-delay:-{i * 1.5}s"/>
<text x="{x + 28}" y="{y + 44}" class="h" fill="{c}"{tglow}>{title}</text>
<line x1="{x + 28}" y1="{y + 58}" x2="{x + 120}" y2="{y + 58}" stroke="{c}" stroke-width="3"/>
{lis}</g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><filter id="glow" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="{3 * t["glow"]:.1f}" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>
  .h{{font:800 17px {SANS};letter-spacing:2px}}
  .it{{font:500 15px {SANS};fill:{t["text"]}}}
  @keyframes run{{to{{stroke-dashoffset:-{per}}}}}
</style>
{"".join(out)}
</svg>'''


for name, t in THEMES.items():
    (OUT / f"header-{name}.svg").write_text(header(t, "JOSÉ DAVID ANGARITA"))
    (OUT / f"terminal-{name}.svg").write_text(terminal(t))
    (OUT / f"products-{name}.svg").write_text(cards(t))
print(sorted(p.name for p in OUT.iterdir()))
