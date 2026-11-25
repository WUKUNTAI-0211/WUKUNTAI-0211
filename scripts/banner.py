"""Draw the animated profile banner in light and dark themes.

Usage: python scripts/banner.py   (writes assets/banner-light.svg and assets/banner-dark.svg)

A request enters vLLM Semantic Router, the router classifies its intent,
and the request is sent to the matching vLLM replica. Animation is SMIL,
which GitHub renders inside <img>. Fonts fall back to system fonts because
an SVG loaded as an image cannot fetch web fonts.
"""

from pathlib import Path

W, H = 1120, 320
CYCLE = 6.0  # seconds for all three requests
SANS = "Inter, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(
        bg0="#0b0d1a", bg1="#171a3d", border="#2a2e55", ink="#f1f0ff",
        sub="#c4b5fd", muted="#8b8fb5", line="#3b3f6e", accent="#a78bfa",
        accent2="#5eead4", box="#14173a", grid="#ffffff", grid_op="0.06",
    ),
    "light": dict(
        bg0="#fbfaff", bg1="#eeeafd", border="#dcd6f5", ink="#15132b",
        sub="#5b43c9", muted="#6b6890", line="#cfc8ef", accent="#6d4fe0",
        accent2="#0f9488", box="#ffffff", grid="#4c3fa0", grid_op="0.09",
    ),
}

# (y of replica, intent label shown under the router)
ROUTES = [
    (92, "code", "replica A"),
    (160, "math", "replica B"),
    (228, "chat", "replica C"),
]
REQ_X0, ROUTER_X0, ROUTER_X1, REP_X = 500, 672, 828, 948
MID_Y = 160


def route_path(y: int) -> str:
    return (f"M{REQ_X0},{MID_Y} L{ROUTER_X1},{MID_Y} "
            f"C{ROUTER_X1 + 60},{MID_Y} {REP_X - 60},{y} {REP_X},{y}")


def branch_path(y: int) -> str:
    return (f"M{ROUTER_X1},{MID_Y} "
            f"C{ROUTER_X1 + 60},{MID_Y} {REP_X - 60},{y} {REP_X},{y}")


def draw(t: dict) -> str:
    third = CYCLE / 3
    # within one CYCLE, a packet travels during [0, 0.30] of its own timeline
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Kun-Tai Wu, LLM inference routing, vLLM Semantic Router maintainer">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t['bg0']}"/><stop offset="1" stop-color="{t['bg1']}"/>
  </linearGradient>
  <radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{t['accent']}" stop-opacity="0.35"/>
    <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="1" fill="{t['grid']}" fill-opacity="{t['grid_op']}"/>
  </pattern>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="frame"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect x="460" width="{W-460}" height="{H}" fill="url(#dots)"/>
  <line x1="480" y1="52" x2="1090" y2="52" stroke="{t['line']}" stroke-width="1"/>
  <line x1="480" y1="268" x2="1090" y2="268" stroke="{t['line']}" stroke-width="1"/>
</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="none" stroke="{t['border']}" stroke-width="1.5"/>

<!-- identity -->
<rect x="52" y="74" width="30" height="3" rx="1.5" fill="{t['accent']}"/>
<text x="50" y="144" font-family="{SANS}" font-size="52" font-weight="700" fill="{t['ink']}" letter-spacing="-0.5">Kun-Tai Wu</text>
<text x="52" y="186" font-family="{SANS}" font-size="27" font-weight="600" fill="{t['sub']}">LLM Inference Routing</text>
<text x="52" y="226" font-family="{SANS}" font-size="16" fill="{t['muted']}">Maintainer · vLLM Semantic Router</text>
<text x="52" y="250" font-family="{SANS}" font-size="16" fill="{t['muted']}">Associate Researcher · Delta Electronics</text>

<!-- wiring -->
<text x="{REQ_X0}" y="{MID_Y-14}" font-family="{MONO}" font-size="12" fill="{t['muted']}" letter-spacing="1.5">REQUEST</text>
<line x1="{REQ_X0}" y1="{MID_Y}" x2="{ROUTER_X0}" y2="{MID_Y}" stroke="{t['line']}" stroke-width="2"/>
''']
    for y, _, _ in ROUTES:
        out.append(f'<path d="{branch_path(y)}" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>\n')

    # packets and lit branches
    for i, (y, intent, rep) in enumerate(ROUTES):
        begin = f"{i * third:.2f}s"
        anim = f'dur="{CYCLE}s" begin="{begin}" repeatCount="indefinite"'
        out.append(f'''<path d="{branch_path(y)}" fill="none" stroke="{t['accent']}" stroke-width="2.5" stroke-opacity="0" filter="url(#glow)">
  <animate attributeName="stroke-opacity" values="0;0;1;0;0" keyTimes="0;0.15;0.28;0.42;1" {anim}/>
</path>
<circle r="5" fill="{t['accent2']}" opacity="0" filter="url(#glow)">
  <animateMotion path="{route_path(y)}" keyPoints="0;1;1" keyTimes="0;0.30;1" calcMode="linear" {anim}/>
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.29;0.30;1" {anim}/>
</circle>
''')

    # router
    rw = ROUTER_X1 - ROUTER_X0
    out.append(f'''<ellipse cx="{(ROUTER_X0+ROUTER_X1)//2}" cy="{MID_Y}" rx="130" ry="70" fill="url(#halo)">
  <animate attributeName="opacity" values="0.55;1;0.55" dur="{third}s" repeatCount="indefinite"/>
</ellipse>
<rect x="{ROUTER_X0}" y="{MID_Y-23}" width="{rw}" height="46" rx="10" fill="{t['box']}" stroke="{t['accent']}" stroke-width="1.5"/>
<text x="{(ROUTER_X0+ROUTER_X1)//2}" y="{MID_Y+6}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="600" fill="{t['ink']}">Semantic Router</text>
''')
    # decision label under router, one per request
    for i, (y, intent, rep) in enumerate(ROUTES):
        anim = f'dur="{CYCLE}s" begin="{i * third:.2f}s" repeatCount="indefinite"'
        out.append(f'''<text x="{(ROUTER_X0+ROUTER_X1)//2}" y="{MID_Y+50}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t['sub']}" opacity="0">intent: {intent} → {rep}
  <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.08;0.30;0.33;1" {anim}/>
</text>
''')

    # replicas
    for i, (y, intent, rep) in enumerate(ROUTES):
        anim = f'dur="{CYCLE}s" begin="{i * third:.2f}s" repeatCount="indefinite"'
        out.append(f'''<rect x="{REP_X}" y="{y-17}" width="122" height="34" rx="8" fill="{t['box']}" stroke="{t['line']}" stroke-width="1.2"/>
<rect x="{REP_X}" y="{y-17}" width="122" height="34" rx="8" fill="none" stroke="{t['accent2']}" stroke-width="2" opacity="0">
  <animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.28;0.31;0.55;1" {anim}/>
</rect>
<text x="{REP_X+61}" y="{y+5}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t['ink']}">vLLM {rep}</text>
''')
    out.append("</svg>\n")
    return "".join(out)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent / "assets"
    root.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (root / f"banner-{name}.svg").write_text(draw(theme), encoding="utf-8")
        print(f"wrote assets/banner-{name}.svg")
