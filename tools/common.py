from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

BG = "#02060B"
SURFACE = "#07111C"
CYAN = "#55C8FF"
BLUE = "#008CFF"
HIGHLIGHT = "#A9EAFF"
TEXT = "#D8F4FF"
MUTED = "#7299B4"
GREEN = "#65F7B2"
AMBER = "#FFC857"


def write_asset(name: str, body: str, *, width: int = 1200, height: int = 400) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
<title>{escape(name.replace('-', ' ').replace('.svg', '').title())}</title>
<desc>Cyber-terminal control room interface for Tahir.</desc>
{body}
</svg>
'''
    (ASSETS / name).write_text(svg, encoding="utf-8", newline="\n")


def defs() -> str:
    return f'''
<defs>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="2" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <path d="M0 3.5H4" stroke="{CYAN}" stroke-opacity=".035"/>
  </pattern>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="{CYAN}" stroke-opacity=".045"/>
  </pattern>
</defs>'''


def base(width: int, height: int, code: str) -> str:
    return f'''
<rect width="{width}" height="{height}" rx="18" fill="{BG}"/>
<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="17" fill="none" stroke="{CYAN}" stroke-opacity=".34"/>
<path d="M22 1h92l12 12h150M{width - 22} 1h-74l-12 12h-102" fill="none" stroke="{CYAN}" stroke-opacity=".6"/>
<rect width="{width}" height="{height}" rx="18" fill="url(#grid)"/>
<rect width="{width}" height="{height}" rx="18" fill="url(#scan)"/>
<text x="24" y="30" fill="{MUTED}" font-family="ui-monospace,Consolas,monospace" font-size="11" letter-spacing="2">{escape(code)}</text>
<circle cx="{width - 30}" cy="25" r="4" fill="{GREEN}"/>
'''


def section_label(index: str, title: str, x: int = 32, y: int = 68) -> str:
    return f'''
<text x="{x}" y="{y}" fill="{CYAN}" font-family="ui-monospace,Consolas,monospace" font-size="12" letter-spacing="3">{escape(index)} // {escape(title.upper())}</text>'''


def text(x: int, y: int, value: str, *, size: int = 16, fill: str = TEXT, weight: int = 400,
         anchor: str = "start", spacing: int | float = 0, opacity: float = 1) -> str:
    return (f'<text x="{x}" y="{y}" fill="{fill}" fill-opacity="{opacity}" text-anchor="{anchor}" '
            f'font-family="ui-monospace,Consolas,monospace" font-size="{size}" font-weight="{weight}" '
            f'letter-spacing="{spacing}">{escape(value)}</text>')


def pill(x: int, y: int, label: str, width: int, *, accent: str = CYAN) -> str:
    return f'''
<g transform="translate({x} {y})">
  <rect width="{width}" height="34" rx="5" fill="{SURFACE}" stroke="{accent}" stroke-opacity=".45"/>
  <path d="M0 8V0h8M{width} 26v8h-8" fill="none" stroke="{accent}"/>
  <circle cx="17" cy="17" r="3" fill="{accent}"/>
  {text(29, 22, label, size=12, fill=TEXT, spacing=.4)}
</g>'''


def card(x: int, y: int, width: int, height: int, *, opacity: float = .9) -> str:
    return f'''
<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="10" fill="{SURFACE}" fill-opacity="{opacity}" stroke="{CYAN}" stroke-opacity=".25"/>
<path d="M{x} {y + 22}V{y}h22M{x + width} {y + height - 22}v22h-22" fill="none" stroke="{CYAN}" stroke-opacity=".85"/>'''
