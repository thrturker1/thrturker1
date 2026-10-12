"""Compact self-contained SVG artwork; no remote fonts, scripts or images."""
from __future__ import annotations

from copy import deepcopy
from html import escape
import math
import random
import xml.etree.ElementTree as ET

from common import ASSETS, ROOT, BG, SURFACE, CYAN, BLUE, HIGHLIGHT, TEXT, MUTED

ICONS = ROOT / "tools" / "icons"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

FEATURED = [
    ("Blender", "blender", "#F79D55", "3D / WORLDS"),
    ("Godot", "godotengine", "#72B8E9", "GAME SYSTEMS"),
    ("Unity", "unity", "#E8F6FF", "REAL-TIME"),
    (".NET", "dotnet", "#AD96FF", "APPLICATIONS"),
]
PAGES = [
    [("Docker", "docker", "#55B9F4", "CONTAINERS"), ("Kubernetes", "kubernetes", "#739BFF", "ORCHESTRATION"),
     ("Apache Kafka", "apachekafka", "#D8F4FF", "EVENT STREAMS"), ("Apache JMeter", "apachejmeter", "#EE819E", "LOAD TESTING")],
    [("Grafana k6", "k6", "#B69AFF", "PERFORMANCE"), ("Gauge", "gauge", "#81D8EF", "TEST SPECS"),
     ("Selenium", "selenium", "#7AD488", "UI AUTOMATION"), ("Playwright", "playwright", "#75D99A", "E2E TESTING")],
    [("Postman", "postman", "#FF996F", "API TESTING"), ("C#", "csharp", "#B79CEB", "BACKEND"),
     ("Node.js", "nodedotjs", "#90CA85", "BACKEND"), ("Java", "java", "#F0A663", "BACKEND")],
    [("Spring", "spring", "#93CF69", "BACKEND"), ("React", "react", "#61DAFB", "FRONTEND"),
     ("Next.js", "nextdotjs", "#E7F4FF", "FRONTEND"), ("Vue.js", "vuedotjs", "#62D7AB", "FRONTEND")],
    [("JavaScript", "javascript", "#E8D963", "FRONTEND"), ("TypeScript", "typescript", "#6CB9F3", "FRONTEND"),
     ("Tailwind CSS", "tailwindcss", "#5AD4EC", "INTERFACES"), ("Tauri", "tauri", "#6AD6E4", "DESKTOP")],
    [("Electron.js", "electron", "#B5E5ED", "DESKTOP"), ("AI Development", "neural", CYAN, "INTELLIGENT SYSTEMS"),
     ("LLM Integration", "chat", HIGHLIGHT, "AI APPLICATIONS"), ("Model Training", "layers", "#9DBBFF", "EXPERIMENTATION")],
    [("AI Agents", "agent", CYAN, "AGENT SYSTEMS"), ("Orchestration", "flow", "#9CC8FF", "AGENT WORKFLOWS"),
     ("AI Workflows", "workflow", HIGHLIGHT, "INTELLIGENT FLOWS"), ("Test Architecture", "check", "#81D9BB", "QUALITY ENGINEERING")],
]
CONTACTS = [
    ("github", "GitHub", "https://github.com/thrturker1"),
    ("linkedin", "LinkedIn", "https://www.linkedin.com/in/thrturker/"),
    ("instagram", "Instagram", "https://www.instagram.com/turkertahirr/"),
    ("portfolio", "Portfolio", "https://thrturker.com"),
    ("studio", "Game studio", "https://addictitygames.com"),
]


def t(x, y, label, size=16, color=TEXT, weight=400, spacing=0, anchor="start", sans=False):
    family = "Arial,Helvetica,sans-serif" if sans else "Consolas,DejaVu Sans Mono,monospace"
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}" text-anchor="{anchor}">{escape(label)}</text>'


def write(name, body, height, title, desc, width=1200):
    target = ASSETS / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f'<svg xmlns="{NS}" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>{body}</svg>\n', encoding="utf-8", newline="\n")


def defs():
    return '''<defs>
      <linearGradient id="edge"><stop stop-color="#55C8FF" stop-opacity=".6"/><stop offset=".5" stop-color="#55C8FF" stop-opacity=".1"/><stop offset="1" stop-color="#008CFF" stop-opacity=".3"/></linearGradient>
      <radialGradient id="aura"><stop stop-color="#008CFF" stop-opacity=".2"/><stop offset="1" stop-color="#008CFF" stop-opacity="0"/></radialGradient>
      <linearGradient id="ice" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#FFFFFF"/><stop offset=".6" stop-color="#A9EAFF"/><stop offset="1" stop-color="#55C8FF"/></linearGradient>
      <filter id="bloom" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="5"/></filter>
      <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".6" fill="#7299B4" opacity=".19"/></pattern>
      <pattern id="scan" width="3" height="5" patternUnits="userSpaceOnUse"><path d="M0 0H3" stroke="#55C8FF" opacity=".018"/></pattern>
    </defs>'''


def shell(height, segment="solo"):
    """Draw one part of the continuous control-room chassis.

    The main profile uses top/middle/bottom segments so separate GitHub images
    visually lock together without repeating rounded cards or horizontal rails.
    """
    if segment == "top":
        fill = f'<path d="M0 {height}V18Q0 0 18 0H1182Q1200 0 1200 18V{height}Z" fill="{BG}"/><path d="M1 {height}V18Q1 1 18 1H1182Q1199 1 1199 18V{height}" fill="none" stroke="url(#edge)"/>'
        texture = f'<path d="M1 {height}V18Q1 1 18 1H1182Q1199 1 1199 18V{height}Z" fill="url(#dots)"/>'
    elif segment == "middle":
        fill = f'<rect width="1200" height="{height}" fill="{BG}"/><path d="M.5 0V{height}M1199.5 0V{height}" stroke="url(#edge)"/>'
        texture = f'<rect x="1" width="1198" height="{height}" fill="url(#dots)"/>'
    elif segment == "bottom":
        fill = f'<path d="M0 0V{height-18}Q0 {height} 18 {height}H1182Q1200 {height} 1200 {height-18}V0Z" fill="{BG}"/><path d="M.5 0V{height-18}Q.5 {height-.5} 18 {height-.5}H1182Q1199.5 {height-.5} 1199.5 {height-18}V0" fill="none" stroke="url(#edge)"/>'
        texture = f'<path d="M1 0V{height-18}Q1 {height-1} 18 {height-1}H1182Q1199 {height-1} 1199 {height-18}V0Z" fill="url(#dots)"/>'
    else:
        fill = f'<rect x=".5" y=".5" width="1199" height="{height-1}" rx="18" fill="{BG}" stroke="url(#edge)"/>'
        texture = f'<rect x="1" y="1" width="1198" height="{height-2}" rx="17" fill="url(#dots)"/>'
    return fill + texture


def glyph(kind, color):
    shapes = {
        "neural": '<path d="M5 5l14 4-7 11L5 5l-2 11 9 4 9-4-2-7"/><circle cx="5" cy="5" r="2"/><circle cx="19" cy="9" r="2"/><circle cx="12" cy="20" r="2"/><circle cx="3" cy="16" r="2"/><circle cx="21" cy="16" r="2"/>',
        "chat": '<path d="M4 4h16v12H9l-5 4V4zM8 8h8M8 12h5"/>',
        "layers": '<path d="M12 3l10 5-10 5L2 8l10-5zM2 12l10 5 10-5M2 16l10 5 10-5"/>',
        "agent": '<rect x="4" y="7" width="16" height="13" rx="4"/><path d="M12 3v4M1 11v5m22-5v5M8 15h8"/><circle cx="8" cy="11" r="1"/><circle cx="16" cy="11" r="1"/>',
        "flow": '<path d="M12 5v6H4v6m8-6h8v6"/><rect x="8" y="1" width="8" height="5" rx="1"/><rect x="1" y="17" width="6" height="5" rx="1"/><rect x="17" y="17" width="6" height="5" rx="1"/>',
        "workflow": '<path d="M7 3h11l3 3v11M17 21H6l-3-3V7M17 13l4 4 3-4M7 11L3 7l-3 4M8 12l3 3 6-7"/>',
        "check": '<path d="M12 2l9 4v6c0 6-9 10-9 10S3 18 3 12V6l9-4zM7 12l3 3 7-7"/>',
        "portfolio": '<path d="M3 4h18v16H3zM3 9h18M7 6h.1M10 6h.1M10 12l-3 2 3 2m4-4 3 2-3 2"/>',
        "studio": '<path d="M5 5h14l3 13-4 2-4-5h-4l-4 5-4-2L5 5zM8 8v5m-2-2h4M16 9h.1m2 3h.1"/>',
    }
    return f'<g fill="none" stroke="{color}" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round">{shapes[kind]}</g>'


def logo(slug, x, y, size, color):
    path = ICONS / f"{slug}.svg"
    if not path.exists():
        return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24">{glyph(slug, color)}</svg>'
    root = ET.parse(path).getroot()
    vb = root.attrib.get("viewBox", "0 0 24 24")
    if slug == "gauge":
        children = [deepcopy(root.findall(f"{{{NS}}}g")[-1])]
        vb = "395 215 325 325"
    else:
        children = [deepcopy(c) for c in root if c.tag.split('}')[-1] not in ("title", "desc", "style", "metadata")]
    for child in children:
        for element in child.iter():
            for attribute in ("class", "id", "style"):
                element.attrib.pop(attribute, None)
            if slug != "playwright":
                element.attrib.pop("fill", None)
    body = ''.join(ET.tostring(c, encoding="unicode") for c in children)
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{vb}" fill="{color}">{body}</svg>'


def static_copy(name, target):
    root = ET.parse(ASSETS / name).getroot()
    for parent in root.iter():
        for child in list(parent):
            if child.tag.split('}')[-1] in ("style", "animate", "animateTransform", "animateMotion"):
                parent.remove(child)
    ET.ElementTree(root).write(ASSETS / target, encoding="utf-8", xml_declaration=False)


def hero():
    noise = ''.join(f'<path d="M{x} {y}h{w}" stroke="{CYAN}" opacity=".3"/>' for x, y, w in
                    [(random.Random(i+91).randint(34, 1160), random.Random(i+301).randint(60, 310), 3+i%7) for i in range(18)])
    body = defs() + shell(350, "top") + f'''
    <style>
    .identity{{animation:identity 14s infinite}} .about{{animation:about 14s infinite}}
    .orbit{{transform-origin:985px 173px;animation:orbit 24s linear infinite}}
    .wave{{animation:wave 6s ease-in-out infinite}} .cursor{{animation:cursor 1.4s steps(1,end) infinite}}
    .scramble{{animation:scramble 14s steps(1,end) infinite}} .specks{{animation:specks 14s steps(1,end) infinite}}
    @keyframes identity{{0%,42%,100%{{opacity:1;transform:translateY(0)}}47%,93%{{opacity:0;transform:translateY(-9px)}}}}
    @keyframes about{{0%,43%,100%{{opacity:0;transform:translateY(9px)}}48%,91%{{opacity:1;transform:translateY(0)}}96%{{opacity:0;transform:translateY(-9px)}}}}
    @keyframes orbit{{to{{transform:rotate(360deg)}}}}
    @keyframes wave{{0%,100%{{opacity:.35}}50%{{opacity:.85}}}}
    @keyframes cursor{{0%,55%{{opacity:1}}56%,100%{{opacity:.25}}}}
    @keyframes scramble{{0%,2%,5%,100%{{opacity:0}}1%,3%{{opacity:.7}}4%{{opacity:.25}}}}
    @keyframes specks{{0%,3%,100%{{opacity:0}}1%,2%{{opacity:1}}}}
    @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}.identity{{opacity:1}}.about,.scramble,.specks{{display:none}}}}
    </style>
    <ellipse cx="990" cy="175" rx="230" ry="200" fill="url(#aura)"/>
    <path d="M36 59H760M36 295H762" stroke="{CYAN}" opacity=".12"/>
    {t(40, 37, 'TAHIR / CONTROL ROOM', 13, CYAN, spacing=2.8)}
    <circle cx="1018" cy="32" r="3" fill="#79D8C8"/>{t(1030, 37, 'SYSTEM ONLINE', 11, MUTED, spacing=1)}
    <g class="identity" opacity="1">
      {t(60, 199, 'TAHIR', 136, 'url(#ice)', 800, 13, sans=True)}
      <g class="scramble" opacity="0"><path d="M61 142h453v8H61zM70 185h440v3H70z" fill="{BG}"/>{t(56, 199, 'T4H1R', 136, CYAN, 800, 13, sans=True)}</g>
      {t(65, 243, 'QA ENGINEERING // GAME DEVELOPMENT // AI SYSTEMS', 16, HIGHLIGHT, spacing=.4)}
      <rect class="cursor" x="65" y="265" width="9" height="3" fill="{CYAN}"/>
      {t(88, 273, 'BUILD / TEST / CREATE', 12, MUTED, spacing=3)}
    </g>
    <g class="about" opacity="0">
      {t(64, 104, 'ISTQB CERTIFIED', 15, CYAN, spacing=4)}
      {t(61, 153, 'Full-Stack QA Specialist', 43, TEXT, 700, -.8, sans=True)}
      {t(64, 191, 'I verify systems. I build worlds.', 23, HIGHLIGHT, sans=True)}
      {t(64, 220, 'I engineer intelligence.', 23, HIGHLIGHT, sans=True)}
      {t(64, 253, 'Independent Game Dev  /  Full-Stack Software  /  AI & Agents', 13, MUTED)}
      {t(64, 275, 'FOUNDER OF ADDICTITY GAMES', 12, CYAN, spacing=1.8)}
    </g>
    <g fill="none">
      <circle cx="985" cy="173" r="121" stroke="{CYAN}" opacity=".12"/>
      <circle cx="985" cy="173" r="91" stroke="{BLUE}" opacity=".35"/>
      <g class="orbit"><circle cx="985" cy="173" r="108" stroke="{CYAN}" stroke-dasharray="50 220 9 400" stroke-width="2"/>
      <circle cx="985" cy="65" r="4" fill="{HIGHLIGHT}" stroke="none"/></g>
      <path d="M885 115v-13h26m174 129v13h-26M886 242h-14v-25m225-115h14v25" stroke="{CYAN}" opacity=".5"/>
      <path class="wave" d="M866 184h51l15-27 18 54 27-79 24 57 16-27 16 22h71" stroke="{CYAN}" stroke-width="2"/>
      <path d="M866 184h51l15-27 18 54 27-79 24 57 16-27 16 22h71" stroke="{CYAN}" stroke-width="8" opacity=".22" filter="url(#bloom)"/>
    </g>
    {t(985, 328, 'VERIFY · CREATE · EVOLVE', 11, MUTED, spacing=1.3, anchor='middle')}
    {t(40, 326, 'ISTQB CERTIFIED  /  FULL-STACK QA', 11, MUTED, spacing=1.3)}
    <g class="specks" opacity="0">{noise}</g>
    <rect x="1" y="1" width="1198" height="348" rx="17" fill="url(#scan)"/>
    '''
    write("hero.svg", body, 350, "Tahir — Control Room", "Alternating identity and biography: Tahir; QA Engineering, Game Development, AI Systems. ISTQB Certified Full-Stack QA Specialist. I verify systems. I build worlds. I engineer intelligence. Independent Game Developer, Full-Stack Software Developer, AI & Agent Systems Developer, Founder of Addictity Games.")
    static_copy("hero.svg", "hero-static.svg")


def star(cx, cy):
    points = []
    for i in range(10):
        a = -math.pi/2 + i*math.pi/5
        r = 7.5 if i%2 == 0 else 3.5
        points.append(f"{cx+r*math.cos(a):.2f},{cy+r*math.sin(a):.2f}")
    return f'<polygon points="{" ".join(points)}" fill="{CYAN}"/>'


def tech_card(item, col, y, featured=False):
    name, slug, color, sub = item
    x, width = 38 + 285*col, 269
    title_size = 19 if len(name) < 14 else 17
    return f'''<g data-tech="{escape(name)}">
      <rect x="{x}" y="{y}" width="{width}" height="111" rx="12" fill="{SURFACE}" stroke="{CYAN}" stroke-opacity="{'.42' if featured else '.17'}"/>
      <path d="M{x+18} {y+111}h233" stroke="{color}" opacity=".3"/>
      <rect x="{x+14}" y="{y+20}" width="70" height="70" rx="17" fill="{color}" opacity=".055"/>
      {logo(slug, x+24, y+30, 50, color)}
      {t(x+99, y+51, name, title_size, TEXT, 700, sans=True)}
      {t(x+100, y+75, sub, 9, MUTED, spacing=.65)}
      {star(x+width-17,y+16) if featured else ''}
    </g>'''


def stack():
    fixed = ''.join(tech_card(item, i, 54, True) for i, item in enumerate(FEATURED))
    frames, rules = [], []
    count = len(PAGES)
    for i in range(count+1):
        page = PAGES[i % count]
        frames.append(f'<g transform="translate({1200*i} 0)">' + ''.join(tech_card(item, j, 186) for j,item in enumerate(page)) + '</g>')
    for i in range(count):
        rules.append(f'{100*i/count:.5f}%,{100*(i+.9083)/count:.5f}%{{transform:translateX(-{i*1200}px)}}')
    rules.append(f'100%{{transform:translateX(-{count*1200}px)}}')
    dots, dot_rules = [], []
    for i in range(count):
        start,end=100*i/count,100*(i+1)/count
        dot_rules.append(f'@keyframes d{i}{{0%,100%{{opacity:.2}}{max(.001,start):.5f}%,{end-.001:.5f}%{{opacity:1}}}}')
        dots.append(f'<rect class="d{i}" x="{531+i*22}" y="319" width="14" height="3" rx="1.5" fill="{CYAN}" opacity="{1 if i==0 else .2}"/>')
    body = defs()+shell(342, "middle")+f'''
    <style>.track{{animation:deck {count*6}s cubic-bezier(.45,0,.2,1) infinite}}
    @keyframes deck{{{''.join(rules)}}}
    {''.join(f'.d{i}{{animation:d{i} {count*6}s steps(1,end) infinite}}' for i in range(count))}{''.join(dot_rules)}
    @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
    </style>
    {t(40,31,'THE TOOLKIT',12,CYAN,spacing=2.2)}
    {t(1158,31,'PINNED FAVORITES',10,MUTED,spacing=1.2,anchor='end')}
    {fixed}
    <clipPath id="cards"><rect x="30" y="175" width="1140" height="130"/></clipPath>
    <g clip-path="url(#cards)"><g class="track">{''.join(frames)}</g></g>
    {''.join(dots)}
    {t(40,326,'QA / INFRA / SOFTWARE / AI',9,MUTED,spacing=.8)}
    {t(1158,326,'AUTO · 6 SEC',9,MUTED,spacing=1.2,anchor='end')}
    '''
    all_names = ', '.join(item[0] for page in PAGES for item in page)
    write("stack.svg",body,342,"Technology deck", "Four columns and two rows. Pinned: Blender, Godot Engine, Unity and .NET. The second row automatically cycles through seven pages: "+all_names+".")
    for i,page in enumerate(PAGES):
        b=defs()+shell(342, "middle")+fixed+''.join(tech_card(item,j,186) for j,item in enumerate(page))
        b+=t(40,31,'THE TOOLKIT',12,CYAN,spacing=2.2)+t(1158,31,f'{i+1:02} / {count:02}',12,MUTED,spacing=2,anchor='end')
        b+=t(600,325,' · '.join(item[3] for item in page),10,MUTED,spacing=1,anchor='middle')
        write(f"stack-page-{i+1}.svg",b,342,f"Technology page {i+1} of {count}","Featured: Blender, Godot Engine, Unity, .NET. "+', '.join(item[0] for item in page))


def studio():
    body=defs()+shell(278, "bottom")+f'''
    <defs>
      <linearGradient id="projectA" x1="0" x2="1"><stop stop-color="#0B1722"/><stop offset="1" stop-color="#102436"/></linearGradient>
      <linearGradient id="projectB" x1="0" x2="1"><stop stop-color="#0B1722"/><stop offset="1" stop-color="#181B35"/></linearGradient>
      <clipPath id="studioClip"><path d="M1 0V260Q1 277 18 277H1182Q1199 277 1199 260V0Z"/></clipPath>
    </defs>
    <style>
    .signal{{animation:signal 4.8s ease-in-out infinite}} .scanA{{animation:scanA 5.4s linear infinite}}
    .scanB{{animation:scanB 6.2s linear infinite}} .core{{transform-origin:126px 174px;animation:core 18s linear infinite}}
    @keyframes signal{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
    @keyframes scanA{{0%{{transform:translateX(-390px)}}100%{{transform:translateX(390px)}}}}
    @keyframes scanB{{0%{{transform:translateX(-410px)}}100%{{transform:translateX(410px)}}}}
    @keyframes core{{to{{transform:rotate(360deg)}}}}
    @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
    </style>
    <g clip-path="url(#studioClip)">
    <ellipse cx="120" cy="170" rx="250" ry="210" fill="url(#aura)"/>
    <path d="M376 24v228M398 24v228" stroke="{CYAN}" opacity=".11"/>
    {t(42,62,'ADDICTITY',48,'url(#ice)',800,2,sans=True)}
    {t(43,96,'G A M E S',19,HIGHLIGHT,400,5,sans=True)}
    <circle cx="126" cy="174" r="57" fill="{SURFACE}" stroke="{CYAN}" stroke-opacity=".55"/>
    <circle class="core" cx="126" cy="174" r="72" fill="none" stroke="{CYAN}" stroke-dasharray="58 18 6 31" opacity=".5"/>
    <path d="M91 194l35-58 35 58-22-16-13 21-13-21-22 16zm22-34h26" fill="none" stroke="{HIGHLIGHT}" stroke-width="3" stroke-linejoin="round"/>
    {t(42,257,'STRONG MECHANICS  /  REPLAYABILITY  /  IDENTITY',10,MUTED,spacing=.8)}

    <g>
      <rect x="425" y="36" width="350" height="198" rx="14" fill="url(#projectA)" stroke="{CYAN}" stroke-opacity=".38"/>
      <path d="M425 69h350M446 211h308" stroke="{CYAN}" opacity=".16"/>
      <path class="scanA" d="M425 36h110l70 198H495z" fill="{CYAN}" opacity=".045"/>
      {t(447,61,'PROJECT 01',10,MUTED,spacing=1.8)}
      {t(447,112,'NO RESPITE',28,TEXT,700,1.1,sans=True)}
      <circle class="signal" cx="451" cy="148" r="4" fill="#FFC85C"/>
      {t(464,153,'IN DEVELOPMENT',11,'#FFC85C',700,spacing=1.3)}
      {t(447,184,'SURVIVAL  /  ENDLESS WAVE  /  ACTION',10,MUTED,spacing=.6)}
      <path d="M710 89l20 20-20 20-20-20zM710 98v22m-11-11h22" fill="none" stroke="{CYAN}" opacity=".75"/>
    </g>
    <g>
      <rect x="797" y="36" width="361" height="198" rx="14" fill="url(#projectB)" stroke="{BLUE}" stroke-opacity=".46"/>
      <path d="M797 69h361M818 211h319" stroke="{BLUE}" opacity=".18"/>
      <path class="scanB" d="M797 36h110l70 198H867z" fill="{BLUE}" opacity=".05"/>
      {t(819,61,'PROJECT 02',10,MUTED,spacing=1.8)}
      {t(819,112,'GOBLET',28,TEXT,700,1.1,sans=True)}
      <circle class="signal" cx="823" cy="148" r="4" fill="#FFC85C"/>
      {t(836,153,'IN DEVELOPMENT',11,'#FFC85C',700,spacing=1.3)}
      {t(819,184,'GAME PROJECT  /  IN DEVELOPMENT',10,MUTED,spacing=.6)}
      <path d="M1086 91h37c0 22-7 34-18 38v13h14m-46 0h46m-33-51c0 22 7 34 19 38" fill="none" stroke="{HIGHLIGHT}" stroke-width="2" opacity=".8"/>
    </g>
    {t(1158,258,'addictitygames.com  ↗',11,HIGHLIGHT,spacing=.5,anchor='end')}
    </g>'''
    write("studio.svg",body,278,"Addictity Games — games in development","Addictity Games. No Respite and Goblet are in development. Click to visit addictitygames.com.")
    static_copy("studio.svg","studio-static.svg")


def contacts():
    for slug,label,_url in CONTACTS:
        body=f'<rect x=".5" y=".5" width="183" height="43" rx="8" fill="{SURFACE}" stroke="#22435A"/>'
        body+=logo(slug,16,12,20,HIGHLIGHT)+t(47,28,label,14,TEXT,sans=True)
        body+='<path d="M159 16h8v8m-8 0 8-8" stroke="#7299B4" fill="none"/>'
        write(f"social-{slug}.svg",body,44,label,f"Open {label}",width=184)


def main():
    hero()
    stack()
    studio()
    contacts()
    print('Generated one continuous hero/terminal/deck/studio chassis, automatic 4x2 technology deck and linked social icons.')


if __name__ == '__main__':
    main()
