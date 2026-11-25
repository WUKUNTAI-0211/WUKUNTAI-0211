"""Draw the animated profile banner in light and dark themes.

Usage: python scripts/banner.py   (writes assets/banner-light.svg and assets/banner-dark.svg)

Scene: a coding agent (Claude Code, Codex or OpenCode) sends a prompt,
vLLM Semantic Router lights up the signals it checks (keyword, embedding,
domain), decides which model should answer, and sends the request there.
Each model is served by a different engine and carries a live load bar,
because the router also weighs in-flight load.

Animation is SMIL, which GitHub renders inside <img>. Fonts fall back to
system fonts because an SVG loaded as an image cannot fetch web fonts.
"""

from pathlib import Path
from xml.sax.saxutils import escape

W, H = 1120, 320
SLOT = 2.0                      # seconds per request
SANS = "Inter, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(
        bg0="#0b0d1a", bg1="#171a3d", border="#2a2e55", ink="#f1f0ff",
        sub="#c4b5fd", muted="#8b8fb5", line="#353a68", accent="#a78bfa",
        hot="#5eead4", box="#13163a", chip="#1b1f48", track="#262a55",
        grid="#ffffff", grid_op="0.05",
    ),
    "light": dict(
        bg0="#fbfaff", bg1="#eeeafd", border="#dcd6f5", ink="#15132b",
        sub="#5b43c9", muted="#6b6890", line="#cfc8ef", accent="#6d4fe0",
        hot="#0f9488", box="#ffffff", chip="#f3f0ff", track="#e7e2fb",
        grid="#4c3fa0", grid_op="0.08",
    ),
}

# agent harnesses that send requests through the router
SOURCES = ["Claude Code", "Codex", "OpenCode"]
# prompt, decision shown in the router, model card index; source cycles
REQUESTS = [
    ("fix the failing Go test", "code → Qwen3-Coder", 0),
    ("prove √2 is irrational", "reasoning → DeepSeek-R1", 1),
    ("what's in this image?", "vision → Qwen2.5-VL", 2),
    ("summarize this email", "simple → Llama-3.2", 3),
]
SOURCE_OF = [0, 1, 2, 0]
# model, engine · tier, resting load (0..1)
ENGINES = [
    ("Qwen3-Coder-30B", "vLLM · data center", 0.35),
    ("DeepSeek-R1", "SGLang · data center", 0.55),
    ("Qwen2.5-VL-7B", "TensorRT-LLM · cloud", 0.25),
    ("Llama-3.2-3B", "Ollama · edge", 0.15),
]
SIGNALS = ["keyword", "embed", "domain"]

SRC_X0, SRC_X1 = 434, 552
SRC_YS = [112, 160, 208]
RTR_X0, RTR_X1 = 640, 816
RTR_Y0, RTR_Y1 = 108, 212
MID_Y = (RTR_Y0 + RTR_Y1) // 2
CARD_X0, CARD_X1 = 890, 1090
CARD_H, CARD_GAP, CARD_TOP = 48, 12, 46
BAR_W = CARD_X1 - CARD_X0 - 28


def card_cy(i: int) -> int:
    return CARD_TOP + i * (CARD_H + CARD_GAP) + CARD_H // 2


def branch(i: int) -> str:
    y = card_cy(i)
    return (f"M{RTR_X1},{MID_Y} C{RTR_X1 + 50},{MID_Y} "
            f"{CARD_X0 - 50},{y} {CARD_X0},{y}")


def intake(s: int) -> str:
    y = SRC_YS[s]
    return (f"M{SRC_X1},{y} C{SRC_X1 + 50},{y} "
            f"{RTR_X0 - 50},{MID_Y} {RTR_X0},{MID_Y}")


def draw(t: dict) -> str:
    cycle = SLOT * len(REQUESTS)

    def anim(i: int) -> str:
        return f'dur="{cycle}s" begin="{i * SLOT:.2f}s" repeatCount="indefinite"'

    # Fractions of one cycle. A request owns [0, 1/len) of its own timeline.
    f = 1 / len(REQUESTS)
    k = lambda x: f"{x * f:.4f}"  # noqa: E731  position inside a slot -> keyTime

    o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Kun-Tai Wu, semantic model routing. Prompts from Claude Code, Codex and OpenCode enter vLLM Semantic Router, which picks a model served by vLLM, SGLang, TensorRT-LLM or Ollama.">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t['bg0']}"/><stop offset="1" stop-color="{t['bg1']}"/>
  </linearGradient>
  <radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{t['accent']}" stop-opacity="0.32"/>
    <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="1" fill="{t['grid']}" fill-opacity="{t['grid_op']}"/>
  </pattern>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="2.6" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="frame"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect x="410" width="{W-410}" height="{H}" fill="url(#dots)"/>
</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="none" stroke="{t['border']}" stroke-width="1.5"/>

<!-- identity -->
<rect x="52" y="74" width="30" height="3" rx="1.5" fill="{t['accent']}"/>
<text x="50" y="144" font-family="{SANS}" font-size="52" font-weight="700" fill="{t['ink']}" letter-spacing="-0.5">Kun-Tai Wu</text>
<text x="52" y="186" font-family="{SANS}" font-size="27" font-weight="600" fill="{t['sub']}">Semantic Model Routing</text>
<text x="52" y="226" font-family="{SANS}" font-size="16" fill="{t['muted']}">Maintainer · vLLM Semantic Router</text>
<text x="52" y="250" font-family="{SANS}" font-size="16" fill="{t['muted']}">Associate Researcher · Delta Electronics</text>

<!-- column labels -->
<text x="{SRC_X0}" y="{SRC_YS[0] - 28}" font-family="{MONO}" font-size="11" fill="{t['muted']}" letter-spacing="1.5">AGENTS</text>
<text x="{CARD_X0}" y="{CARD_TOP - 12}" font-family="{MONO}" font-size="11" fill="{t['muted']}" letter-spacing="1.5">MODELS</text>
<text x="{(RTR_X0 + RTR_X1) // 2}" y="{H - 30}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t['muted']}" letter-spacing="1">cloud · data center · edge</text>

<!-- wiring -->
''']
    for i in range(len(ENGINES)):
        o.append(f'<path d="{branch(i)}" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>\n')

    for s_ in range(len(SOURCES)):
        o.append(f'<path d="{intake(s_)}" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>\n')

    # agent sources: the sending agent lights up, a packet travels to the router
    for s_, name in enumerate(SOURCES):
        y = SRC_YS[s_]
        o.append(f'''<rect x="{SRC_X0}" y="{y-15}" width="{SRC_X1-SRC_X0}" height="30" rx="15" fill="{t['chip']}" stroke="{t['line']}" stroke-width="1.2"/>
<text x="{(SRC_X0+SRC_X1)//2}" y="{y+5}" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="600" fill="{t['ink']}">{name}</text>
''')
    for i, (prompt, _, _) in enumerate(REQUESTS):
        s_ = SOURCE_OF[i]
        y = SRC_YS[s_]
        o.append(f'''<rect x="{SRC_X0}" y="{y-15}" width="{SRC_X1-SRC_X0}" height="30" rx="15" fill="none" stroke="{t['accent']}" stroke-width="2" opacity="0">
  <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{k(.04)};{k(.30)};{k(.45)};1" {anim(i)}/>
</rect>
<path d="{intake(s_)}" fill="none" stroke="{t['accent']}" stroke-width="2.5" opacity="0" filter="url(#glow)">
  <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{k(.06)};{k(.26)};{k(.42)};1" {anim(i)}/>
</path>
<circle r="5" fill="{t['hot']}" opacity="0" filter="url(#glow)">
  <animateMotion path="{intake(s_)}" keyPoints="0;0;1;1" keyTimes="0;{k(.04)};{k(.28)};1" calcMode="linear" {anim(i)}/>
  <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{k(.04)};{k(.27)};{k(.29)};1" {anim(i)}/>
</circle>
<text x="{(RTR_X0+RTR_X1)//2}" y="{RTR_Y0-14}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{t['ink']}" opacity="0">“{escape(prompt)}”
  <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{k(.22)};{k(.30)};{k(.92)};{k(1.0)};1" {anim(i)}/>
</text>
''')

    # router
    cx = (RTR_X0 + RTR_X1) // 2
    o.append(f'''<ellipse cx="{cx}" cy="{MID_Y}" rx="140" ry="90" fill="url(#halo)">
  <animate attributeName="opacity" values="0.5;1;0.5" dur="{SLOT}s" repeatCount="indefinite"/>
</ellipse>
<rect x="{RTR_X0}" y="{RTR_Y0}" width="{RTR_X1-RTR_X0}" height="{RTR_Y1-RTR_Y0}" rx="12" fill="{t['box']}" stroke="{t['accent']}" stroke-width="1.5"/>
<text x="{cx}" y="{RTR_Y0+26}" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="600" fill="{t['ink']}">Semantic Router</text>
<line x1="{RTR_X0+12}" y1="{RTR_Y0+70}" x2="{RTR_X1-12}" y2="{RTR_Y0+70}" stroke="{t['line']}" stroke-width="1"/>
''')
    pill_w, gap = 50, 4
    px0 = cx - (3 * pill_w + 2 * gap) // 2
    for s, name in enumerate(SIGNALS):
        x = px0 + s * (pill_w + gap)
        o.append(f'<rect x="{x}" y="{RTR_Y0+40}" width="{pill_w}" height="18" rx="9" fill="none" stroke="{t["line"]}" stroke-width="1"/>\n')
        # light each signal in turn, once per request
        on0, on1 = .30 + s * .09, .35 + s * .09
        o.append(f'''<rect x="{x}" y="{RTR_Y0+40}" width="{pill_w}" height="18" rx="9" fill="{t['accent']}" fill-opacity="0.25" stroke="{t['accent']}" stroke-width="1" opacity="0">
  <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{on0:.2f};{on1:.2f};0.90;0.98;1" dur="{SLOT}s" repeatCount="indefinite"/>
</rect>
<text x="{x + pill_w // 2}" y="{RTR_Y0+53}" text-anchor="middle" font-family="{MONO}" font-size="9.5" fill="{t['sub']}">{name}</text>
''')
    for i, (_, decision, _) in enumerate(REQUESTS):
        o.append(f'''<text x="{cx}" y="{RTR_Y0+90}" text-anchor="middle" font-family="{MONO}" font-size="11.5" font-weight="600" fill="{t['hot']}" opacity="0">{escape(decision)}
  <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{k(.58)};{k(.64)};{k(.97)};{k(1.0)};1" {anim(i)}/>
</text>
''')

    # packets: router -> engine, with the branch lit underneath
    for i, (_, _, e) in enumerate(REQUESTS):
        o.append(f'''<path d="{branch(e)}" fill="none" stroke="{t['accent']}" stroke-width="2.5" opacity="0" filter="url(#glow)">
  <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{k(.62)};{k(.70)};{k(.92)};{k(1.15)};1" {anim(i)}/>
</path>
<circle r="5" fill="{t['hot']}" opacity="0" filter="url(#glow)">
  <animateMotion path="{branch(e)}" keyPoints="0;0;1;1" keyTimes="0;{k(.64)};{k(.92)};1" calcMode="linear" {anim(i)}/>
  <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{k(.63)};{k(.65)};{k(.92)};{k(.94)};1" {anim(i)}/>
</circle>
''')

    # engine cards with load bars
    for i, (name, tag, rest) in enumerate(ENGINES):
        y0 = card_cy(i) - CARD_H // 2
        req = next(r for r, (_, _, e) in enumerate(REQUESTS) if e == i)
        a = anim(req)
        w0, w1 = int(BAR_W * rest), int(BAR_W * min(rest + 0.45, 0.95))
        o.append(f'''<rect x="{CARD_X0}" y="{y0}" width="{CARD_X1-CARD_X0}" height="{CARD_H}" rx="10" fill="{t['box']}" stroke="{t['line']}" stroke-width="1.2"/>
<rect x="{CARD_X0}" y="{y0}" width="{CARD_X1-CARD_X0}" height="{CARD_H}" rx="10" fill="none" stroke="{t['hot']}" stroke-width="2" opacity="0">
  <animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;{k(.90)};{k(.96)};{k(1.6)};1" {a}/>
</rect>
<text x="{CARD_X0+14}" y="{y0+20}" font-family="{SANS}" font-size="14" font-weight="700" fill="{t['ink']}">{name}</text>
<text x="{CARD_X0+14}" y="{y0+34}" font-family="{MONO}" font-size="10" fill="{t['muted']}">{tag}</text>
<circle cx="{CARD_X1-16}" cy="{y0+15}" r="3.5" fill="{t['hot']}">
  <animate attributeName="opacity" values="1;0.35;1" dur="{1.6 + i * 0.4:.1f}s" repeatCount="indefinite"/>
</circle>
<rect x="{CARD_X0+14}" y="{y0+40}" width="{BAR_W}" height="3" rx="1.5" fill="{t['track']}"/>
<rect x="{CARD_X0+14}" y="{y0+40}" width="{w0}" height="3" rx="1.5" fill="{t['accent']}">
  <animate attributeName="width" values="{w0};{w0};{w1};{w0};{w0}" keyTimes="0;{k(.92)};{k(1.05)};{k(2.4)};1" {a}/>
</rect>
''')

    o.append("</svg>\n")
    return "".join(o)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent / "assets"
    root.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (root / f"banner-{name}.svg").write_text(draw(theme), encoding="utf-8")
        print(f"wrote assets/banner-{name}.svg")
