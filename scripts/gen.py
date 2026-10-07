"""Genera el encabezado del perfil en versión clara y oscura."""
from pathlib import Path

OUT = Path(__file__).parent.parent / "assets"
OUT.mkdir(exist_ok=True)
for old in OUT.glob("*.svg"):
    old.unlink()

SANS = "-apple-system,'Segoe UI','Helvetica Neue',Arial,sans-serif"
THEMES = {
    "dark": dict(bg="#0d1117", text="#f0f6fc", dim="#8b949e", line="#30363d", accent="#2f81f7"),
    "light": dict(bg="#ffffff", text="#1f2328", dim="#59636e", line="#d1d9e0", accent="#0969da"),
}


def header(t):
    W, H = 1000, 180
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .n{{font:600 40px {SANS};fill:{t["text"]};letter-spacing:-.5px}}
  .r{{font:400 18px {SANS};fill:{t["dim"]}}}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{t["bg"]}" stroke="{t["line"]}"/>
<rect x="48" y="58" width="4" height="64" rx="2" fill="{t["accent"]}"/>
<text x="72" y="92" class="n">José David Angarita</text>
<text x="72" y="122" class="r">Desarrollo de software empresarial · Meeteam</text>
</svg>'''


for name, t in THEMES.items():
    (OUT / f"header-{name}.svg").write_text(header(t))
print(sorted(p.name for p in OUT.iterdir()))
