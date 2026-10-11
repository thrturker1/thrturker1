from __future__ import annotations

from html import escape

from PIL import Image, ImageDraw, ImageFont

from common import ASSETS


WIDTH, HEIGHT = 1200, 240
BG, SURFACE = "#050B13", "#091621"
CYAN, TEXT, MUTED, GREEN = "#67DCED", "#E3F5F8", "#7898AA", "#62E5AF"
PROMPT = "tahir@controlroom:~$ "
LEFT, COMMAND_Y, LINE_HEIGHT = 30, 62, 32


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
    return ImageFont.load_default(size=size)


FONT = load_font(21)
FONT_BOLD = load_font(21, bold=True)
FONT_SMALL = load_font(13)

# Each scene has a command followed by no more than three readable output lines.
SCENES = [
    (
        "initialize --identity tahir",
        [
            ("[OK] ISTQB certified / full-stack QA", GREEN),
            ("     Build worlds. Engineer intelligence.", TEXT),
        ],
    ),
    (
        "inspect --capabilities",
        [
            ("QA     / test architecture + automation", CYAN),
            ("GAMES  / Godot + Unity + Blender", TEXT),
            ("AI     / agents + orchestration", GREEN),
        ],
    ),
    (
        "launch addictity-games",
        [
            ("[ONLINE] ADDICTITY GAMES", GREEN),
            ("         https://addictitygames.com", CYAN),
        ],
    ),
]


def render(scene_index: int, command: str, shown_lines: int, cursor: bool = True) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    # Middle segment of the profile chassis: vertical rails only, no card gap.
    draw.line((0, 0, 0, HEIGHT), fill="#194050")
    draw.line((WIDTH - 1, 0, WIDTH - 1, HEIGHT), fill="#194050")
    draw.rectangle((1, 0, WIDTH - 2, 42), fill=SURFACE)
    draw.line((22, 43, WIDTH - 23, 43), fill="#143443")
    for x, color in ((31, "#286173"), (49, "#398C98"), (67, CYAN)):
        draw.ellipse((x - 3, 19, x + 3, 25), fill=color)
    draw.text((88, 14), "TAHIR / LIVE SHELL", font=FONT_SMALL, fill=MUTED)
    draw.text((WIDTH - 158, 14), f"SESSION 0{scene_index + 1} / 03", font=FONT_SMALL, fill=MUTED)

    draw.text((LEFT, COMMAND_Y), PROMPT, fill=MUTED, font=FONT)
    command_x = LEFT + draw.textlength(PROMPT, font=FONT)
    draw.text((command_x, COMMAND_Y), command, fill=TEXT, font=FONT_BOLD)
    if cursor:
        cursor_x = command_x + draw.textlength(command, font=FONT_BOLD) + 4
        draw.rectangle((cursor_x, COMMAND_Y + 4, cursor_x + 9, COMMAND_Y + 22), fill=CYAN)

    for index, (value, color) in enumerate(SCENES[scene_index][1][:shown_lines]):
        draw.text((LEFT, COMMAND_Y + 42 + index * LINE_HEIGHT), value, font=FONT, fill=color)

    draw.line((LEFT, 202, WIDTH - LEFT, 202), fill="#102D3B")
    draw.ellipse((LEFT, 217, LEFT + 5, 222), fill=GREEN)
    draw.text((LEFT + 15, 210), "READY", font=FONT_SMALL, fill=MUTED)
    for index in range(3):
        x = WIDTH - 137 + index * 36
        draw.rounded_rectangle((x, 217, x + 25, 220), radius=1, fill=CYAN if index == scene_index else "#183746")
    return image


def build_frames() -> tuple[list[Image.Image], list[int]]:
    frames: list[Image.Image] = []
    durations: list[int] = []
    # A shared palette preserves flat UI colors and prevents frame-to-frame flicker.
    palette_source = render(1, SCENES[1][0], 3)
    palette = palette_source.quantize(colors=64, method=Image.Quantize.MEDIANCUT)

    def add(scene_index: int, command: str, shown_lines: int, duration: int, cursor: bool = True) -> None:
        frame = render(scene_index, command, shown_lines, cursor)
        frames.append(frame.quantize(palette=palette, dither=Image.Dither.NONE))
        durations.append(duration)

    for scene_index, (command, output) in enumerate(SCENES):
        add(scene_index, "", 0, 420)
        for length, character in enumerate(command, start=1):
            delay = 90 if character == " " else 100 if character == "-" else 40 + (length % 3) * 10
            add(scene_index, command[:length], 0, delay)
        add(scene_index, command, 0, 320, False)
        for count in range(1, len(output) + 1):
            add(scene_index, command, count, 220, False)
        if scene_index == len(SCENES) - 1:
            add(scene_index, command, len(output), 4000)
        else:
            add(scene_index, command, len(output), 500)
            add(scene_index, command, len(output), 420, False)
            add(scene_index, command, len(output), 800)
    return frames, durations


def write_static() -> None:
    scene_index = len(SCENES) - 1
    command, output = SCENES[scene_index]
    png_target = ASSETS / "terminal-static.png"
    png_temporary = ASSETS / "terminal-static.tmp.png"
    render(scene_index, command, len(output)).save(png_temporary, optimize=True)
    png_temporary.replace(png_target)
    font = 'font-family="Consolas,DejaVu Sans Mono,monospace"'
    output_lines = "".join(
        f'<text x="30" y="{122 + index * LINE_HEIGHT}" fill="{color}" font-size="21" xml:space="preserve">{escape(value)}</text>'
        for index, (value, color) in enumerate(output)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img">
<title>Tahir — Addictity Games terminal</title>
<desc>The terminal launches Addictity Games. Studio website: https://addictitygames.com</desc>
<rect width="{WIDTH}" height="{HEIGHT}" fill="{BG}"/>
<path d="M.5 0V{HEIGHT}M{WIDTH-.5} 0V{HEIGHT}" stroke="#194050"/>
<path d="M1 0H{WIDTH-1}V42H1Z" fill="{SURFACE}"/>
<path d="M22 43H{WIDTH-23}M30 202H{WIDTH-30}" stroke="#143443"/>
<circle cx="31" cy="22" r="3" fill="#286173"/><circle cx="49" cy="22" r="3" fill="#398C98"/><circle cx="67" cy="22" r="3" fill="{CYAN}"/>
<g {font}>
<text x="88" y="26" font-size="13" fill="{MUTED}">TAHIR / LIVE SHELL</text>
<text x="{WIDTH-158}" y="26" font-size="13" fill="{MUTED}">SESSION 03 / 03</text>
<text x="30" y="80" font-size="21" fill="{TEXT}" xml:space="preserve"><tspan fill="{MUTED}">{escape(PROMPT)}</tspan><tspan font-weight="700">{escape(command)}</tspan><tspan fill="{CYAN}"> ▌</tspan></text>
{output_lines}
<text x="45" y="222" font-size="13" fill="{MUTED}">READY</text>
</g>
<circle cx="32.5" cy="219.5" r="2.5" fill="{GREEN}"/>
<path d="M{WIDTH-137} 218H{WIDTH-112}M{WIDTH-101} 218H{WIDTH-76}" stroke="#183746" stroke-width="3" stroke-linecap="round"/>
<path d="M{WIDTH-65} 218H{WIDTH-40}" stroke="{CYAN}" stroke-width="3" stroke-linecap="round"/>
</svg>
'''
    (ASSETS / "terminal-static.svg").write_text(svg, encoding="utf-8", newline="\n")


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
    write_static()
    if output.stat().st_size > 2_000_000:
        raise SystemExit("terminal.gif exceeds its 2 MB performance budget")
    print(f"Generated assets/{output.name}: {WIDTH}x{HEIGHT}, {len(frames)} frames, {sum(durations) / 1000:.1f}s, {output.stat().st_size / 1024:.1f} KiB")
    print("Generated assets/terminal-static.svg and assets/terminal-static.png")


if __name__ == "__main__":
    main()
