"""Genera el encabezado animado del perfil en versión clara y oscura."""
import math
import random
from pathlib import Path

OUT = Path(__file__).parent.parent / "assets"
OUT.mkdir(exist_ok=True)
for old in OUT.glob("*.svg"):
    old.unlink()

SANS = "-apple-system,'Segoe UI','Helvetica Neue',Arial,sans-serif"
THEMES = {
    "dark": dict(bg="#0b0f17", text="#f0f6fc", dim="#8b949e", line="#262c36",
                 a="#2f81f7", b="#8957e5", c="#1f9e8f", blob=.55, net=.55, shine="#ffffff"),
    "light": dict(bg="#ffffff", text="#1f2328", dim="#59636e", line="#d1d9e0",
                  a="#0969da", b="#8250df", c="#1a7f72", blob=.16, net=.45, shine="#7fb3ff"),
}
W, H = 1000, 220


def network(t):
    rnd = random.Random(11)
    nodes = []
    while len(nodes) < 16:
        p = (rnd.uniform(600, 960), rnd.uniform(30, H - 30))
        if all(math.dist(p, q) > 52 for q in nodes):
            nodes.append(p)
    edges = sorted({tuple(sorted((i, j))) for i, p in enumerate(nodes)
                    for j, q in enumerate(nodes) if i != j and math.dist(p, q) < 120})
    lines = "".join(f'<line x1="{nodes[i][0]:.1f}" y1="{nodes[i][1]:.1f}" x2="{nodes[j][0]:.1f}" y2="{nodes[j][1]:.1f}"/>' for i, j in edges)
    dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.choice([2, 2.5, 3])}" fill="{rnd.choice([t["a"], t["b"], t["c"]])}" '
        f'style="animation:pulse {rnd.uniform(3, 6):.1f}s ease-in-out {-rnd.uniform(0, 6):.1f}s infinite"/>'
        for x, y in nodes)
    # paquetes de datos que recorren algunas conexiones
    packets = []
    for k, (i, j) in enumerate(rnd.sample(edges, min(7, len(edges)))):
        (x1, y1), (x2, y2) = nodes[i], nodes[j]
        if k % 2:
            x1, y1, x2, y2 = x2, y2, x1, y1
        dur = rnd.uniform(2.4, 4.2)
        begin = -rnd.uniform(0, dur)
        packets.append(f'<circle r="2" fill="{t["shine"]}"><animateMotion dur="{dur:.1f}s" begin="{begin:.1f}s" '
                       f'repeatCount="indefinite" path="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}"/>'
                       f'<animate attributeName="opacity" values="0;.9;.9;0" keyTimes="0;.15;.85;1" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/></circle>')
    return f'''<g class="net" opacity="{t["net"]}">
  <g stroke="{t["dim"]}" stroke-opacity=".35" stroke-width="1">{lines}</g>
  {dots}{"".join(packets)}
</g>'''


def header(t):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <clipPath id="card"><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14"/></clipPath>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
  <linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="260" y2="0">
    <stop offset="0" stop-color="{t["text"]}"/><stop offset=".5" stop-color="{t["shine"]}"/><stop offset="1" stop-color="{t["text"]}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-300 0;300 0;900 0;900 0" keyTimes="0;.25;.5;1" dur="7s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="accent" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["a"]}"/><stop offset="1" stop-color="{t["b"]}"/></linearGradient>
</defs>
<style>
  .n{{font:600 42px {SANS};letter-spacing:-.6px}}
  .r{{font:400 18px {SANS};fill:{t["dim"]}}}
  .k{{font:500 12px {SANS};letter-spacing:2.5px;fill:{t["a"]}}}
  .in1{{animation:rise 1s cubic-bezier(.2,.7,.2,1) both}}
  .in2{{animation:rise 1s cubic-bezier(.2,.7,.2,1) .25s both}}
  .in3{{animation:rise 1s cubic-bezier(.2,.7,.2,1) .5s both}}
  .bar{{animation:grow 1.1s cubic-bezier(.2,.7,.2,1) both;transform-origin:50px 162px}}
  .net{{animation:fade 2s ease .6s both}}
  .b1{{animation:drift1 22s ease-in-out infinite alternate}}
  .b2{{animation:drift2 26s ease-in-out infinite alternate}}
  .b3{{animation:drift3 30s ease-in-out infinite alternate}}
  @keyframes rise{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
  @keyframes grow{{from{{transform:scaleY(0)}}to{{transform:none}}}}
  @keyframes fade{{from{{opacity:0}}}}
  @keyframes pulse{{50%{{opacity:.35}}}}
  @keyframes drift1{{to{{transform:translate(160px,40px)}}}}
  @keyframes drift2{{to{{transform:translate(-180px,-30px)}}}}
  @keyframes drift3{{to{{transform:translate(120px,-50px)}}}}
</style>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
  <g filter="url(#blur)" opacity="{t["blob"]}">
    <circle class="b1" cx="620" cy="40" r="120" fill="{t["a"]}"/>
    <circle class="b2" cx="900" cy="190" r="130" fill="{t["b"]}"/>
    <circle class="b3" cx="380" cy="230" r="110" fill="{t["c"]}"/>
  </g>
  {network(t)}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{t["line"]}"/>
<rect class="bar" x="48" y="66" width="4" height="96" rx="2" fill="url(#accent)"/>
<text x="72" y="86" class="k in1">MEETEAM</text>
<text x="72" y="128" class="n in2" fill="url(#shine)">José David Angarita</text>
<text x="72" y="158" class="r in3">Desarrollo de software empresarial</text>
</svg>'''


for name, t in THEMES.items():
    (OUT / f"header-{name}.svg").write_text(header(t))
print(sorted(p.name for p in OUT.iterdir()))
