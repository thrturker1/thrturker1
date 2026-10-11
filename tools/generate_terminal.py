from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from common import ASSETS, BG, BLUE, CYAN, GREEN, HIGHLIGHT, MUTED, SURFACE, TEXT


WIDTH, HEIGHT = 1080, 610
MARGIN_X, TOP = 42, 74
FONT_SIZE, LINE_H = 17, 24


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = [
        "DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf",
        "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


FONT = load_font(FONT_SIZE)
FONT_BOLD = load_font(FONT_SIZE, bold=True)
FONT_SMALL = load_font(12)


EVENTS: list[tuple[str, str, int]] = [
    ("type", "tahir@controlroom:~$ initialize --identity tahir", 34),
    ("line", "", 210),
    ("line", "[OK] identity.core ............... TAHIR", 210),
    ("line", "[OK] quality_engineering ......... LOADED", 180),
    ("line", "[OK] creative_engine ............. LOADED", 180),
    ("line", "[OK] agent_systems ............... LOADED", 360),
    ("line", "", 180),
    ("type", "tahir@controlroom:~$ inspect --capabilities", 34),
    ("line", "", 180),
    ("line", "QA        :: ISTQB Certified / Full-Stack Quality", 150),
    ("line", "GAMES     :: Godot / Unity / Blender", 150),
    ("line", "SOFTWARE  :: .NET / Node.js / Web + Desktop", 150),
    ("line", "AI        :: Agents / Orchestration / Training", 320),
    ("line", "", 160),
    ("type", "tahir@controlroom:~$ launch addictity-games", 34),
    ("line", "", 170),
    ("line", "[ONLINE] https://addictitygames.com", 450),
    ("line", "", 150),
    ("type", "tahir@controlroom:~$ ", 40),
]


def line_color(value: str) -> str:
    if value.startswith("[OK]") or value.startswith("[ONLINE]"):
        return GREEN
    if value.startswith("tahir@"):
        return HIGHLIGHT
    return TEXT


def background() -> Image.Image:
    im = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((1, 1, WIDTH - 2, HEIGHT - 2), radius=18, fill=BG, outline="#1A6688", width=1)
    d.rectangle((1, 1, WIDTH - 2, 50), fill=SURFACE)
    d.line((1, 50, WIDTH - 2, 50), fill="#16364A")
    for x, c in ((24, "#FF6B6B"), (44, "#FFC857"), (64, GREEN)):
        d.ellipse((x - 5, 20, x + 5, 30), fill=c)
    d.text((91, 16), "CONTROL ROOM // LIVE SHELL", fill=MUTED, font=FONT_SMALL)
    d.text((WIDTH - 235, 16), "SESSION: TR49-VERIFY", fill=MUTED, font=FONT_SMALL)
    for y in range(54, HEIGHT - 20, 4):
        d.line((12, y, WIDTH - 12, y), fill="#030B11")
    d.line((20, HEIGHT - 30, WIDTH - 20, HEIGHT - 30), fill="#0B2737")
    d.text((24, HEIGHT - 23), "secure channel • deterministic capture • loop-safe", fill="#42677F", font=FONT_SMALL)
    return im


def render(lines: list[str], active: str, cursor_on: bool, frame_index: int) -> Image.Image:
    im = background()
    d = ImageDraw.Draw(im)
    all_lines = lines + ([active] if active or cursor_on else [])
    max_lines = 20
    visible = all_lines[-max_lines:]
    for i, value in enumerate(visible):
        y = TOP + i * LINE_H
        d.text((MARGIN_X, y), value, fill=line_color(value), font=FONT_BOLD if value.startswith("tahir@") else FONT)
    if cursor_on and visible:
        last = visible[-1]
        bbox = d.textbbox((MARGIN_X, 0), last, font=FONT_BOLD if last.startswith("tahir@") else FONT)
        cursor_x = bbox[2] + 3
        cursor_y = TOP + (len(visible) - 1) * LINE_H
        d.rectangle((cursor_x, cursor_y + 2, cursor_x + 9, cursor_y + FONT_SIZE + 2), fill=CYAN)

    rnd = random.Random(4901 + frame_index)
    for _ in range(3):
        x = rnd.randint(820, WIDTH - 35)
        y = rnd.randint(60, HEIGHT - 48)
        d.rectangle((x, y, x + rnd.randint(2, 12), y), fill="#104B66")
    return im


def build_frames() -> tuple[list[Image.Image], list[int]]:
    frames: list[Image.Image] = []
    durations: list[int] = []
    lines: list[str] = []
    frame_index = 0

    def add(active: str, duration: int, cursor: bool = True) -> None:
        nonlocal frame_index
        frames.append(render(lines, active, cursor, frame_index).convert("P", palette=Image.Palette.ADAPTIVE, colors=64))
        durations.append(duration)
        frame_index += 1

    for kind, value, timing in EVENTS:
        if kind == "type":
            for n in range(0, len(value) + 1, 2):
                add(value[:n], timing, True)
            if len(value) % 2:
                add(value, timing, True)
            add(value, 260, False)
            lines.append(value)
        else:
            lines.append(value)
            add("", timing, True)

    add("", 420, False)
    add("", 420, True)
    add("", 2200, True)
    return frames, durations


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    frames, durations = build_frames()
    output = ASSETS / "terminal.gif"
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=1,
    )
    print(f"Generated {output.relative_to(Path.cwd())}: {len(frames)} frames, {output.stat().st_size / 1024:.1f} KiB")


if __name__ == "__main__":
    main()
