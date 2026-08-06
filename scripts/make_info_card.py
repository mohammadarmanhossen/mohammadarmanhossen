"""
Build a neofetch-style info card SVG (Andrew6rant style) to sit to the RIGHT of
the ASCII portrait: colored key/value rows for work experience, tech stack, and
highlights -- NOT GitHub stats (the contribution graph covers those).

Static content, hand-authored below. Lines fade/slide in on a short stagger so
it feels like the panel is printing alongside the portrait. STATIC=1 emits the
frozen state for Quick Look previews.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "arman-info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 480, 520
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 92
LINE_H = 20.5

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"      # orange keys (matches Andrew)
SECTION = "#58a6ff"  # blue section headers
GREEN = "#3fb950"
ACCENT = "#22d3ee"

ROWS = [
    ("host",),

    ("kv", "Name", "Md. Arman Hossen"),
    ("kv", "Role", "Full-Stack Developer"),
    ("kv", "Focus", "Django · Next.js · REST API · AI"),
    ("kv", "Open Source", "Contributor"),
    ("kv", "Education", "BBA in Management"),
    ("kv", "Location", "Bangladesh"),

    ("gap",),

    ("sec", "Tech Stack"),

    ("kv", "Languages", "Python, JavaScript, C, C++"),
    ("kv", "Frontend", "React, Next.js, Tailwind CSS"),
    ("kv", "Backend", "Django, DRF, Node.js, Express.js"),
    ("kv", "Databases", "PostgreSQL, MySQL, MongoDB"),
    ("kv", "Tools", "Git, GitHub, Docker, VS Code, Postman"),
    ("kv", "OS", "Windows, Linux"),

    ("gap",),

    ("sec", "Highlights"),

    ("bul", "Building scalable full-stack web applications"),
    ("bul", "Passionate about Open Source"),
    ("bul", "Learning AI and modern web technologies"),
    ("bul", "Strong problem-solving and teamwork skills"),
    ("bul", "Enjoys Chess and Programming Puzzles"),
]

def esc(s):
    return html.escape(s)

def rise(inner, i):
    if STATIC:
        return f'<g class="row" style="transition: transform 0.2s;">{inner}</g>'
    delay = 0.15 + i * 0.06
    return (f'<clipPath id="wipe{i}"><rect x="0" y="0" width="0" height="{H}">'
            f'<animate attributeName="width" from="0" to="{W}" begin="{delay:.2f}s" dur="0.5s" calcMode="spline" keySplines="0.1 0.8 0.2 1" fill="freeze"/></rect></clipPath>'
            f'<g class="row" clip-path="url(#wipe{i})" style="transition: transform 0.2s;" opacity="0" transform="translate(0,5)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.2s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>')

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    f'<style>.row:hover {{ transform: translateX(5px) scale(1.02); filter: drop-shadow(0px 2px 2px rgba(255,166,87,0.2)); }}</style>',
    '<defs>'
    f'<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">'
    f'<path d="M 24 0 L 0 0 0 24" fill="none" stroke="{MUTED}" stroke-width="0.5" stroke-opacity="0.05"/></pattern>'
    f'<radialGradient id="orb" cx="80%" cy="80%" r="50%">'
    f'<stop offset="0%" stop-color="{SECTION}" stop-opacity="0.15"/>'
    f'<stop offset="100%" stop-color="{SECTION}" stop-opacity="0"/>'
    f'</radialGradient>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<circle cx="80%" cy="80%" r="150" fill="url(#orb)">'
    f'<animate attributeName="r" values="150;180;150" dur="4s" repeatCount="indefinite"/></circle>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#grid)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="13" '
             f'text-anchor="middle">arman@github: ~$ neofetch</text>')

y = TITLEBAR_H + 30
for i, row in enumerate(ROWS):
    kind = row[0]
    if kind == "gap":
        y += LINE_H * 0.5
        continue
    if kind == "host":
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" font-size="14" font-weight="700">'
             f'<tspan fill="{GREEN}">arman</tspan><tspan fill="{MUTED}">@</tspan>'
             f'<tspan fill="{ACCENT}">github</tspan></text>'
             f'<line x1="{KEY_X+108}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-opacity="0.8" stroke-dasharray="2 4"/>')
    elif kind == "sec":
        title = esc(row[1])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="13" font-weight="700">'
                 f'&#8212; {title}</text>'
                 f'<line x1="{KEY_X + 12 + len(row[1])*8}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-opacity="0.8" stroke-dasharray="2 4"/>')
    elif kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="13.5" font-weight="700">{key}</text>'
                 f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="13.5">{val}</text>')
    elif kind == "bul":
        txt = esc(row[1])
        inner = (f'<circle cx="{KEY_X+3}" cy="{y-4:.1f}" r="2.5" fill="{GREEN}"/>'
                 f'<text x="{KEY_X+14}" y="{y:.1f}" fill="{INK}" font-size="13.5">{txt}</text>')
    else:
        continue
    parts.append(rise(inner, i))
    y += LINE_H

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", W, "x", H, "content_bottom", round(y))
