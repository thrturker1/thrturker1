from __future__ import annotations

import math
import random

from common import (
    AMBER, BG, BLUE, CYAN, GREEN, HIGHLIGHT, MUTED, SURFACE, TEXT,
    base, card, defs, pill, section_label, text, write_asset,
)


def hero() -> None:
    rnd = random.Random(4901)
    specks = []
    for i in range(46):
        x, y = rnd.randint(35, 1165), rnd.randint(52, 390)
        w = rnd.choice((1, 1, 2, 3, 6, 10))
        delay = rnd.uniform(0, 4)
        specks.append(
            f'<rect class="noise n{i % 4}" x="{x}" y="{y}" width="{w}" height="1" fill="{CYAN}" '
            f'fill-opacity="{rnd.uniform(.08, .42):.2f}" style="animation-delay:{delay:.2f}s"/>'
        )

    body = defs() + base(1200, 430, "CR://IDENTITY_HANDSHAKE / NODE-TR49") + f'''
<style>
  .scanline{{animation:sweep 7s ease-in-out infinite}} .pulse{{animation:pulse 2.8s ease-in-out infinite}}
  .scramble{{animation:glitch 7s steps(1,end) infinite}} .s2{{animation-delay:.12s}} .s3{{animation-delay:.24s}}
  .noise{{animation:noise 3.7s steps(1,end) infinite}} .n1{{animation-duration:4.3s}} .n2{{animation-duration:5.1s}} .n3{{animation-duration:6.2s}}
  .packet{{animation:packet 5s linear infinite}} .packet.b{{animation-delay:2.1s}}
  @keyframes sweep{{0%,8%{{transform:translateX(-1260px);opacity:0}}12%{{opacity:.8}}31%{{transform:translateX(1260px);opacity:.15}}32%,100%{{opacity:0}}}}
  @keyframes glitch{{0%,8%{{opacity:0}}9%,12%{{opacity:.72}}13%,15%{{opacity:.12}}16%,18%{{opacity:.5}}19%,100%{{opacity:0}}}}
  @keyframes noise{{0%,11%,16%,100%{{opacity:0}}12%,15%{{opacity:1}}}}
  @keyframes pulse{{0%,100%{{opacity:.36}}50%{{opacity:1}}}}
  @keyframes packet{{0%{{stroke-dashoffset:280}}100%{{stroke-dashoffset:-280}}}}
  @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}.scramble,.noise,.scanline{{display:none}}}}
</style>
<clipPath id="heroClip"><rect x="28" y="46" width="1144" height="350" rx="12"/></clipPath>
<g clip-path="url(#heroClip)">
  <rect class="scanline" x="0" y="48" width="34" height="346" fill="{CYAN}" fill-opacity=".08" filter="url(#glow)"/>
  {''.join(specks)}
</g>
<path d="M32 112h180l34 34h138M816 146h138l34-34h180" fill="none" stroke="{CYAN}" stroke-opacity=".2"/>
<path class="packet" d="M32 112h180l34 34h138" fill="none" stroke="{CYAN}" stroke-width="2" stroke-dasharray="2 278"/>
<path class="packet b" d="M1168 112H988l-34 34H816" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="2 278"/>
<g transform="translate(600 214)">
  <circle class="pulse" r="72" fill="none" stroke="{BLUE}" stroke-opacity=".25"/>
  <circle r="54" fill="{SURFACE}" stroke="{CYAN}" stroke-opacity=".55"/>
  <path d="M-44 0h88M0-44v88" stroke="{CYAN}" stroke-opacity=".12"/>
  <circle r="6" fill="{CYAN}" filter="url(#glow)"/>
</g>
{text(600, 245, 'TAHIR', size=78, fill=TEXT, weight=700, anchor='middle', spacing=16)}
<g class="scramble" transform="translate(-4 1)">{text(600, 245, 'T4H!R', size=78, fill=CYAN, weight=700, anchor='middle', spacing=16)}</g>
<g class="scramble s2" transform="translate(7 -2)">{text(600, 245, '7A#1R', size=78, fill=BLUE, weight=700, anchor='middle', spacing=16)}</g>
<g class="scramble s3" transform="translate(-2 3)">{text(600, 245, 'TAH1R', size=78, fill=HIGHLIGHT, weight=700, anchor='middle', spacing=16)}</g>
{text(600, 294, 'QA ENGINEERING // GAME DEVELOPMENT // AI SYSTEMS', size=16, fill=HIGHLIGHT, anchor='middle', spacing=2)}
<rect x="398" y="326" width="404" height="40" rx="4" fill="{SURFACE}" stroke="{CYAN}" stroke-opacity=".35"/>
<circle cx="418" cy="346" r="4" fill="{GREEN}"/>
{text(600, 352, 'SYSTEM ONLINE — BUILD / TEST / CREATE', size=13, fill=TEXT, anchor='middle', spacing=1)}
<rect class="pulse" x="784" y="338" width="8" height="16" fill="{CYAN}"/>
{text(32, 400, 'ISTQB CERTIFIED  •  FULL-STACK QA SPECIALIST', size=12, fill=MUTED, spacing=1)}
{text(1168, 400, 'TAHIR // CONTROL ROOM', size=12, fill=MUTED, anchor='end', spacing=1)}
'''
    write_asset("hero.svg", body, width=1200, height=430)


def verify_create() -> None:
    left = [
        "MANUAL + EXPLORATORY", "UI AUTOMATION", "API TESTING",
        "PERFORMANCE + LOAD", "INTEGRATION + REGRESSION", "TEST ARCHITECTURE",
        "QUALITY ENGINEERING",
    ]
    right = [
        "INDIE GAME DEVELOPMENT", "GAMEPLAY SYSTEMS", "3D ASSETS + WORLDS",
        "WEB APPLICATIONS", "DESKTOP SOFTWARE", "AI AGENTS", "MODEL + AI WORKFLOWS",
    ]
    left_rows = ''.join(pill(58, 154 + i * 48, v, 378, accent=CYAN) for i, v in enumerate(left))
    right_rows = ''.join(pill(764, 154 + i * 48, v, 378, accent=BLUE) for i, v in enumerate(right))
    body = defs() + base(1200, 570, "CR://DUAL_CORE / ENGINEERING_MINDSET") + f'''
<style>
 .orbit{{transform-origin:600px 274px;animation:orbit 18s linear infinite}} .signal{{animation:dash 4s linear infinite}}
 @keyframes orbit{{to{{transform:rotate(360deg)}}}} @keyframes dash{{to{{stroke-dashoffset:-80}}}}
 @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
{section_label('01', 'VERIFY // CREATE')}
<path d="M468 274H520M680 274h52" stroke="{CYAN}" stroke-opacity=".45" stroke-dasharray="4 8"/>
<path class="signal" d="M468 274H520M680 274h52" stroke="{HIGHLIGHT}" stroke-width="2" stroke-dasharray="8 72"/>
<g class="orbit"><circle cx="600" cy="274" r="72" fill="none" stroke="{CYAN}" stroke-opacity=".24" stroke-dasharray="18 12"/></g>
<circle cx="600" cy="274" r="52" fill="{SURFACE}" stroke="{CYAN}" stroke-opacity=".6"/>
<path d="M585 274l10 10 23-27" fill="none" stroke="{GREEN}" stroke-width="4"/>
{text(600, 346, 'ONE CORE', size=11, fill=MUTED, anchor='middle', spacing=2)}
{text(58, 113, 'VERIFY', size=30, fill=CYAN, weight=700, spacing=4)}
{text(58, 136, 'ISTQB CERTIFIED • FULL-STACK QA SPECIALIST', size=11, fill=MUTED, spacing=1)}
{text(1142, 113, 'CREATE', size=30, fill=BLUE, weight=700, anchor='end', spacing=4)}
{text(1142, 136, 'ENGINEERING POSSIBILITIES INTO WORKING SYSTEMS', size=11, fill=MUTED, anchor='end', spacing=1)}
{left_rows}{right_rows}
<rect x="338" y="520" width="524" height="32" rx="4" fill="{SURFACE}" stroke="{CYAN}" stroke-opacity=".35"/>
{text(600, 541, 'TWO DISCIPLINES. ONE ENGINEERING MINDSET.', size=12, fill=HIGHLIGHT, anchor='middle', spacing=1.4)}
'''
    write_asset("verify-create.svg", body, width=1200, height=570)


def primary_stack() -> None:
    tech = [
        ("DOCKER", "CONTAINERS", "DCK", CYAN),
        ("KUBERNETES", "ORCHESTRATION", "K8S", BLUE),
        ("APACHE KAFKA", "EVENT STREAMS", "KFK", HIGHLIGHT),
        ("APACHE JMETER", "LOAD TESTING", "JMT", AMBER),
        ("GRAFANA k6", "PERFORMANCE", "K6", GREEN),
        ("GAUGE", "TEST SPECS", "GGE", CYAN),
        ("SELENIUM", "UI AUTOMATION", "SEL", GREEN),
        ("PLAYWRIGHT", "E2E AUTOMATION", "PWR", HIGHLIGHT),
        ("POSTMAN", "API TESTING", "PST", "#FF8A5B"),
    ]
    out = []
    for i, (name, role, monogram, accent) in enumerate(tech):
        row, col = divmod(i, 5)
        count = 5 if row == 0 else 4
        cell_w = 210 if row == 0 else 252
        gap = 16
        total = count * cell_w + (count - 1) * gap
        start = (1200 - total) // 2
        x, y = start + col * (cell_w + gap), 116 + row * 130
        out.append(card(x, y, cell_w, 108))
        out.append(f'<circle cx="{x + 36}" cy="{y + 38}" r="19" fill="none" stroke="{accent}" stroke-opacity=".8"/>')
        out.append(text(x + 36, y + 43, monogram, size=10, fill=accent, weight=700, anchor="middle", spacing=.3))
        out.append(text(x + 64, y + 35, name, size=14, fill=TEXT, weight=700, spacing=.5))
        out.append(text(x + 64, y + 57, role, size=9, fill=MUTED, spacing=1))
        out.append(f'<rect x="{x + 18}" y="{y + 82}" width="{cell_w - 36}" height="3" rx="2" fill="{accent}" fill-opacity=".13"/>')
        out.append(f'<rect x="{x + 18}" y="{y + 82}" width="{(cell_w - 36) * (.42 + (i % 4) * .09):.0f}" height="3" rx="2" fill="{accent}" fill-opacity=".65"/>')
    body = defs() + base(1200, 390, "CR://CAPABILITY_MATRIX / PRIORITY_CHANNELS") + f'''
{section_label('02', 'PRIMARY PROFESSIONAL STACK')}
{text(32, 92, 'QUALITY AUTOMATION • PERFORMANCE • INFRASTRUCTURE • OBSERVABILITY', size=12, fill=MUTED, spacing=1)}
{''.join(out)}
{text(1168, 370, 'SIGNAL BARS INDICATE DOMAIN ROUTING — NOT PROFICIENCY SCORES', size=10, fill=MUTED, anchor='end', spacing=.5)}
'''
    write_asset("primary-stack.svg", body, width=1200, height=390)


def star_points(cx: float, cy: float, outer: float = 11, inner: float = 4.8) -> str:
    pts = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        r = outer if i % 2 == 0 else inner
        pts.append(f"{cx + math.cos(angle) * r:.1f},{cy + math.sin(angle) * r:.1f}")
    return " ".join(pts)


def featured_stack() -> None:
    tech = [
        ("BLENDER", "3D CREATION", "#F5792A", "B"),
        ("GODOT ENGINE", "GAME SYSTEMS", "#78C8F0", "G"),
        ("UNITY", "REAL-TIME WORLDS", "#FFFFFF", "U"),
        (".NET", "APPLICATION CORE", "#8A73FF", ".N"),
    ]
    out = []
    for i, (name, role, accent, mark) in enumerate(tech):
        x = 37 + i * 288
        y = 118
        out.append(card(x, y, 262, 144))
        out.append(f'<path d="M{x + 22} {y + 96}h76l18-18h126" fill="none" stroke="{accent}" stroke-opacity=".28"/>')
        out.append(f'<circle cx="{x + 52}" cy="{y + 51}" r="29" fill="{accent}" fill-opacity=".08" stroke="{accent}" stroke-opacity=".75"/>')
        out.append(text(x + 52, y + 58, mark, size=18, fill=accent, weight=700, anchor="middle"))
        out.append(text(x + 91, y + 48, name, size=16, fill=TEXT, weight=700, spacing=.7))
        out.append(text(x + 91, y + 70, role, size=9, fill=MUTED, spacing=1.2))
        out.append(f'<polygon points="{star_points(x + 235, y + 25)}" fill="{CYAN}" filter="url(#softGlow)"/>')
        out.append(f'<circle cx="{x + 235}" cy="{y + 25}" r="17" fill="none" stroke="{CYAN}" stroke-opacity=".28"/>')
        out.append(text(x + 22, y + 124, f"FEATURE NODE 0{i + 1}", size=9, fill=MUTED, spacing=1))
    body = defs() + base(1200, 305, "CR://FEATURE_NODES / CREATIVE_RUNTIME") + f'''
{section_label('03', 'FEATURED TECHNOLOGIES')}
{text(32, 94, 'FOUR CREATIVE + APPLICATION NODES PINNED TO THE CONTROL SURFACE', size=11, fill=MUTED, spacing=1)}
{''.join(out)}
'''
    write_asset("featured-stack.svg", body, width=1200, height=305)


def arsenal() -> None:
    groups = [
        ("QA + AUTOMATION", ["Playwright", "Selenium", "Gauge", "Postman", "JMeter", "k6"], CYAN),
        ("DEVOPS + INFRA", ["Docker", "Kubernetes", "Kafka"], BLUE),
        ("BACKEND", [".NET", "C#", "Node.js", "Java", "Spring"], HIGHLIGHT),
        ("FRONTEND", ["React", "Next.js", "Vue.js", "JavaScript", "TypeScript", "Tailwind CSS"], CYAN),
        ("DESKTOP + GAME + 3D", ["Tauri", "Electron.js", "Godot", "Unity", "Blender"], AMBER),
        ("AI ENGINEERING", ["LLM Integration", "Model Training", "AI Agents", "Orchestration", "Intelligent Workflows"], GREEN),
    ]
    out = []
    for i, (title, items, accent) in enumerate(groups):
        row, col = divmod(i, 2)
        x, y = 35 + col * 575, 112 + row * 190
        out.append(card(x, y, 540, 165))
        out.append(text(x + 24, y + 34, f"0{i + 1} / {title}", size=13, fill=accent, weight=700, spacing=1))
        px, py = x + 24, y + 58
        for item in items:
            w = max(94, 30 + len(item) * 8)
            if px + w > x + 516:
                px, py = x + 24, py + 44
            out.append(pill(px, py, item, w, accent=accent))
            px += w + 10
    body = defs() + base(1200, 700, "CR://ARSENAL_INDEX / EXPANDED_VIEW") + f'''
{section_label('03B', 'FULL TECH ARSENAL')}
{text(32, 92, 'GROUPED BY SYSTEM RESPONSIBILITY — COMPACT, SEARCHABLE, DEPLOYMENT-SAFE', size=11, fill=MUTED, spacing=1)}
{''.join(out)}
'''
    write_asset("full-arsenal.svg", body, width=1200, height=700)


def studio() -> None:
    body = defs() + base(1200, 420, "CR://STUDIO_LINK / ADDICTITY_GAMES") + f'''
<style>.wave{{animation:wave 5s ease-in-out infinite}} @keyframes wave{{50%{{transform:translateX(22px)}}}} @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
{section_label('04', 'INDEPENDENT GAME STUDIO')}
<g transform="translate(58 112)">
  <circle cx="84" cy="96" r="74" fill="none" stroke="{CYAN}" stroke-opacity=".22"/>
  <circle cx="84" cy="96" r="49" fill="{SURFACE}" stroke="{BLUE}" stroke-opacity=".7"/>
  <path d="M58 112c18-42 39-42 54 0M67 80h34M72 65l12-18 12 18" fill="none" stroke="{CYAN}" stroke-width="4"/>
  <path class="wave" d="M-20 96h38l12-18 16 36 14-20 18 2" fill="none" stroke="{HIGHLIGHT}" stroke-opacity=".65"/>
</g>
{text(248, 148, 'ADDICTITY', size=43, fill=TEXT, weight=700, spacing=4)}
{text(551, 148, 'GAMES', size=43, fill=MUTED, weight=700, spacing=4)}
{text(250, 184, 'STRONG MECHANICS. REPLAYABILITY. IDENTITY.', size=14, fill=CYAN, spacing=1.5)}
{text(250, 218, 'Focused games built around strong gameplay loops,', size=15, fill=TEXT)}
{text(250, 242, 'replayability, and the feeling of one more run.', size=15, fill=TEXT)}
<rect x="250" y="258" width="512" height="70" rx="8" fill="{SURFACE}" stroke="{CYAN}" stroke-opacity=".32"/>
<circle cx="276" cy="280" r="4" fill="{AMBER}"/>
{text(294, 285, 'IN DEVELOPMENT', size=10, fill=AMBER, spacing=1.5)}
{text(276, 311, 'NO RESPITE  //  SURVIVAL • ENDLESS WAVE • ACTION', size=13, fill=TEXT, spacing=.7)}
<path d="M830 112h310v216H830z" fill="{SURFACE}" stroke="{BLUE}" stroke-opacity=".25"/>
<path d="M856 293l57-64 43 35 72-98 86 127" fill="none" stroke="{BLUE}" stroke-opacity=".42" stroke-width="2"/>
<path d="M856 293h258M856 265h258M856 237h258M856 209h258M856 181h258" stroke="{CYAN}" stroke-opacity=".08"/>
{text(856, 150, 'STUDIO UPLINK', size=11, fill=MUTED, spacing=2)}
{text(856, 190, 'addictitygames.com', size=17, fill=HIGHLIGHT)}
{text(856, 320, 'OPEN CHANNEL ↗', size=11, fill=CYAN, spacing=1.4)}
{text(32, 394, 'PUBLIC STUDIO SIGNAL • VERIFIED 2026-10-11', size=10, fill=MUTED, spacing=1)}
'''
    write_asset("studio.svg", body, width=1200, height=420)


def agent_network() -> None:
    nodes = [(92, "INPUT"), (316, "REASON"), (548, "TOOLS"), (780, "ACTION"), (1004, "OUTPUT")]
    out = []
    for i, (x, label) in enumerate(nodes):
        out.append(f'<circle cx="{x}" cy="192" r="46" fill="{SURFACE}" stroke="{CYAN if i % 2 == 0 else BLUE}" stroke-opacity=".68"/>')
        out.append(f'<circle cx="{x}" cy="192" r="30" fill="none" stroke="{CYAN}" stroke-opacity=".12" stroke-dasharray="3 5"/>')
        out.append(text(x, 198, label, size=12, fill=TEXT, weight=700, anchor="middle", spacing=1))
        out.append(text(x, 257, f"NODE 0{i + 1}", size=9, fill=MUTED, anchor="middle", spacing=1))
        if i < len(nodes) - 1:
            nx = nodes[i + 1][0]
            out.append(f'<path d="M{x + 46} 192H{nx - 46}" stroke="{CYAN}" stroke-opacity=".25" stroke-dasharray="4 7"/>')
            out.append(f'<circle class="packet p{i}" cx="{x + 64}" cy="192" r="4" fill="{HIGHLIGHT}" filter="url(#softGlow)"/>')
    body = defs() + base(1200, 350, "CR://AGENT_FABRIC / ABSTRACT_PIPELINE") + f'''
<style>
 .packet{{animation:hop 4s ease-in-out infinite}} .p1{{animation-delay:.8s}} .p2{{animation-delay:1.6s}} .p3{{animation-delay:2.4s}}
 @keyframes hop{{0%,15%,100%{{transform:translateX(0);opacity:0}}25%{{opacity:1}}70%{{transform:translateX(118px);opacity:1}}80%{{opacity:0}}}}
 @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}.packet{{display:none}}}}
</style>
{section_label('05', 'AI + AGENT ENGINEERING')}
{text(32, 94, 'LLM APPLICATIONS • TOOL ORCHESTRATION • WORKFLOW AUTOMATION • MODEL EXPERIMENTATION', size=11, fill=MUTED, spacing=.8)}
{''.join(out)}
<rect x="210" y="295" width="780" height="34" rx="5" fill="{SURFACE}" stroke="{CYAN}" stroke-opacity=".25"/>
{text(600, 317, 'A CONCEPTUAL CONTROL FLOW — NOT A CLAIM ABOUT A PROPRIETARY IMPLEMENTATION', size=10, fill=MUTED, anchor='middle', spacing=.7)}
'''
    write_asset("agent-network.svg", body, width=1200, height=350)


def contact() -> None:
    ports = [
        ("GITHUB", "github.com/thrturker1", CYAN),
        ("LINKEDIN", "professional signal", BLUE),
        ("INSTAGRAM", "visual channel", "#C989FF"),
        ("PORTFOLIO", "project archive", HIGHLIGHT),
        ("GAME STUDIO", "addictitygames.com", AMBER),
    ]
    out = []
    for i, (name, detail, accent) in enumerate(ports):
        x = 28 + i * 232
        out.append(f'<g transform="translate({x} 108)"><rect width="216" height="84" rx="8" fill="{SURFACE}" stroke="{accent}" stroke-opacity=".45"/>')
        out.append(f'<path d="M0 16V0h16M216 68v16h-16" fill="none" stroke="{accent}"/>')
        out.append(f'<circle cx="20" cy="24" r="4" fill="{GREEN}"/>')
        out.append(text(34, 29, name, size=12, fill=TEXT, weight=700, spacing=1))
        out.append(text(18, 59, detail, size=9, fill=MUTED, spacing=.4))
        out.append(text(198, 62, "↗", size=14, fill=accent, anchor="end"))
        out.append('</g>')
    body = defs() + base(1200, 225, "CR://COMM_PORTS / PUBLIC_ENDPOINTS") + f'''
{section_label('07', 'OPEN COMMUNICATION CHANNELS')}
{text(32, 92, 'SELECT AN ENDPOINT TO LEAVE THE CONTROL ROOM', size=10, fill=MUTED, spacing=1)}
{''.join(out)}
'''
    write_asset("contact.svg", body, width=1200, height=225)


def main() -> None:
    hero()
    verify_create()
    primary_stack()
    featured_stack()
    arsenal()
    studio()
    agent_network()
    contact()
    print("Generated interface SVG assets.")


if __name__ == "__main__":
    main()
