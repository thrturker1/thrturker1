from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "assets"
FEATURED = ["Blender", "Godot", "Unity", ".NET"]
PUBLIC_LINKS = {
    "https://github.com/thrturker1",
    "https://www.linkedin.com/in/thrturker/",
    "https://www.instagram.com/turkertahirr/",
    "https://sevro49.github.io/My-Portfolio/public/index.html",
    "https://addictitygames.com",
}
PROFILE_ASSETS = {
    "hero.svg", "hero-static.svg", "stack.svg", "studio.svg", "studio-static.svg",
    "terminal.gif", "terminal-static.svg", "terminal-static.png", "github-stats.svg",
    *(f"stack-page-{index}.svg" for index in range(1, 8)),
    *(f"social-{name}.svg" for name in ("github", "linkedin", "instagram", "portfolio", "studio")),
}
TRIGGER_PATHS = {
    "README.md", "PROFILE-STATIC.md", "assets/**",
    "tools/**", "requirements.txt", ".github/workflows/**",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_tag(name: str) -> str:
    return name.rsplit("}", 1)[-1]


def generated_state() -> dict[str, str]:
    paths = [path for path in ASSETS.rglob("*") if path.is_file()]
    return {path.relative_to(ROOT).as_posix(): sha(path) for path in paths}


def validate_determinism() -> None:
    command = [sys.executable, str(ROOT / "tools" / "generate_all.py")]
    subprocess.run(command, cwd=ROOT, check=True)
    first = generated_state()
    subprocess.run(command, cwd=ROOT, check=True)
    second = generated_state()
    changed = sorted(name for name in first.keys() | second.keys() if first.get(name) != second.get(name))
    require(not changed, f"Non-deterministic generated filenames or contents: {', '.join(changed)}")


def validate_svg(path: Path) -> ET.Element:
    source = path.read_text(encoding="utf-8")
    require(not re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", source, re.I), f"XML declarations are not allowed: {path.name}")
    root = ET.fromstring(source)
    require(local_tag(root.tag) == "svg", f"Invalid SVG root: {path.name}")
    require(path.stat().st_size <= 350_000, f"SVG exceeds its size budget: {path.name}")
    for node in root.iter():
        tag = local_tag(node.tag).lower()
        require(tag not in {"script", "foreignobject"}, f"Unsafe SVG element {tag}: {path.name}")
        for name, value in node.attrib.items():
            attribute = local_tag(name).lower()
            require(not attribute.startswith("on"), f"SVG event handler {name}: {path.name}")
            if attribute in {"href", "src"}:
                require(value.startswith("#"), f"External SVG resource {value}: {path.name}")
            for resource in re.findall(r"url\(\s*['\"]?([^'\"\s)]+)", value, re.I):
                require(resource.startswith("#"), f"External SVG URL: {path.name}")
        if tag == "style":
            css = "".join(node.itertext())
            require(not re.search(r"@import\b", css, re.I), f"External CSS import: {path.name}")
            for resource in re.findall(r"url\(\s*['\"]?([^'\"\s)]+)", css, re.I):
                require(resource.startswith("#"), f"External CSS resource: {path.name}")
    return root


def validate_assets() -> None:
    require(ASSETS.is_dir(), "The assets directory is missing")
    missing = sorted(name for name in PROFILE_ASSETS if not (ASSETS / name).is_file())
    require(not missing, f"Required profile assets missing: {', '.join(missing)}")
    for path in sorted(ASSETS.rglob("*.svg")):
        validate_svg(path)
    for name in ("hero-static.svg", "studio-static.svg", "terminal-static.svg"):
        root = ET.parse(ASSETS / name).getroot()
        require(
            not any(local_tag(node.tag).lower() in {"style", "animate", "animatetransform", "animatemotion", "set"} for node in root.iter()),
            f"Static fallback contains animation or style rules: {name}",
        )
    with Image.open(ASSETS / "terminal-static.png") as image:
        require(image.size == (1200, 240), "Terminal PNG fallback has incorrect dimensions")


def validate_cards() -> None:
    paths = sorted(ASSETS.glob("stack-page-*.svg"))
    expected = {f"stack-page-{index}.svg" for index in range(1, 8)}
    require({path.name for path in paths} == expected, "The technology deck must have exactly seven static pages")
    for path in paths:
        root = ET.parse(path).getroot()
        cards = [node for node in root.iter() if "data-tech" in node.attrib]
        require(len(cards) == 8, f"{path.name} must contain exactly eight cards")
        require([node.attrib["data-tech"] for node in cards[:4]] == FEATURED, f"Featured technology order changed: {path.name}")
        require(len({node.attrib["data-tech"] for node in cards}) == 8, f"Duplicate technology cards: {path.name}")
        stars = 0
        for index, card in enumerate(cards):
            shapes = [node for node in card if local_tag(node.tag) == "rect"]
            require(bool(shapes), f"Card has no surface: {path.name}")
            expected_x, expected_y = 38 + 285 * (index % 4), 54 if index < 4 else 186
            require(
                float(shapes[0].attrib["x"]) == expected_x and float(shapes[0].attrib["y"]) == expected_y,
                f"Card does not follow the four-column, two-row grid: {path.name}",
            )
            card_stars = sum(local_tag(node.tag) == "polygon" for node in card)
            require(card_stars == (1 if index < 4 else 0), f"Featured corner star missing or misplaced: {path.name}")
            stars += card_stars
            require(any(local_tag(node.tag) == "svg" for node in card), f"Technology icon missing: {path.name}")
        require(stars == 4, f"{path.name} must have four featured stars")
    animated = ET.parse(ASSETS / "stack.svg").getroot()
    animated_cards = [node for node in animated.iter() if "data-tech" in node.attrib]
    require([node.attrib["data-tech"] for node in animated_cards[:4]] == FEATURED, "Animated deck must pin the featured row first")


def validate_gif() -> None:
    path = ASSETS / "terminal.gif"
    require(path.stat().st_size <= 2_000_000, "terminal.gif exceeds its 2 MB budget")
    with Image.open(path) as image:
        require(image.size == (1200, 240), "terminal.gif must be 1200x240")
        require(getattr(image, "is_animated", False) and image.n_frames >= 20, "Terminal GIF lacks meaningful animation")
        distinct = set()
        for frame in range(image.n_frames):
            image.seek(frame)
            distinct.add(hashlib.sha256(image.convert("RGB").tobytes()).digest())
        require(len(distinct) >= 20, "Terminal GIF must contain at least 20 visibly distinct frames")
        require(image.info.get("duration", 0) >= 4000, "Terminal GIF final scene must remain stable for at least four seconds")
        require(image.info.get("loop") == 0, "Terminal GIF must loop continuously")


class HTMLLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.headings = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.headings |= tag in {"h1", "h2", "h3", "h4", "h5", "h6"}
        for key, value in attrs:
            if not value:
                continue
            if key in {"href", "src"}:
                self.links.append(value)
            elif key == "srcset":
                self.links.extend(candidate.strip().split()[0] for candidate in value.split(",") if candidate.strip())


def document_links(source: str) -> tuple[set[str], HTMLLinks]:
    html = HTMLLinks()
    html.feed(source)
    markdown = re.findall(r"\]\(\s*(<[^>]+>|[^\s)]+)", source)
    references = re.findall(r"(?m)^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)", source)
    return set(html.links) | {link.strip("<>") for link in markdown + references}, html


def validate_documents() -> None:
    documents = [README, ROOT / "PROFILE-STATIC.md"]
    for document in documents:
        require(document.is_file(), f"Missing profile document: {document.name}")
        source = document.read_text(encoding="utf-8")
        links, html = document_links(source)
        for link in links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = ((ROOT if parsed.path.startswith("/") else document.parent) / unquote(parsed.path).lstrip("/")).resolve()
            require(target.is_relative_to(ROOT), f"Local link escapes the repository in {document.name}: {link}")
            require(target.exists(), f"Broken local link in {document.name}: {link}")
        if document in {README, ROOT / "PROFILE-STATIC.md"}:
            require(PUBLIC_LINKS <= links, f"Required public link missing from {document.name}: {sorted(PUBLIC_LINKS - links)}")
        if document == README:
            require(not html.headings and not re.search(r"(?m)^\s{0,3}#{1,6}\s", source), "Main README must not contain section headings")
            removed = {"verify-create.svg", "agent-network.svg", "primary-stack.svg", "featured-stack.svg", "contact.svg", "full-arsenal.svg"}
            require(not any(Path(urlsplit(link).path).name in removed for link in links), "Main README still references an obsolete panel")
            require("github-stats.svg" not in source, "Main README still displays the removed GitHub telemetry panel")
            require("arsenal/" not in source and "nav-prev.svg" not in source and "nav-next.svg" not in source, "Main README still exposes manual technology navigation")
            order = [source.find(name) for name in ("hero.svg", "terminal.gif", "stack.svg", "studio.svg")]
            require(all(position >= 0 for position in order) and order == sorted(order), "Continuous chassis order must be hero, terminal, deck, studio")


def validate_workflows() -> None:
    for filename, permission, events in (
        ("generate-assets.yml", "read", {"workflow_dispatch", "pull_request", "push"}),
        ("update-stats.yml", "write", {"workflow_dispatch", "schedule"}),
    ):
        # BaseLoader preserves GitHub's literal "on" key instead of YAML 1.1's True.
        path = ROOT / ".github" / "workflows" / filename
        workflow = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        require(isinstance(workflow, dict), f"Workflow is not a mapping: {filename}")
        require(workflow.get("permissions") == {"contents": permission}, f"Unexpected workflow permissions: {filename}")
        triggers = workflow.get("on")
        require(isinstance(triggers, dict) and set(triggers) == events, f"Invalid workflow triggers: {filename}")
        require(triggers["workflow_dispatch"] in ("", {}) or triggers["workflow_dispatch"] is None, f"Unexpected dispatch configuration: {filename}")
        if filename == "generate-assets.yml":
            for event in ("push", "pull_request"):
                trigger = triggers[event]
                require(isinstance(trigger, dict), f"Invalid {event} trigger")
                require(isinstance(trigger.get("paths"), list) and TRIGGER_PATHS <= set(trigger["paths"]), f"{event} omits a relevant profile path")
            require(triggers["push"].get("branches") == ["main", "master"], "Asset push verification must cover main and master")
        else:
            schedule = triggers["schedule"]
            require(isinstance(schedule, list) and len(schedule) == 1, "Stats refresh must have one schedule")
            require(isinstance(schedule[0], dict) and set(schedule[0]) == {"cron"} and len(schedule[0]["cron"].split()) == 5, "Invalid telemetry schedule")
        jobs = workflow.get("jobs")
        require(isinstance(jobs, dict) and bool(jobs), f"Workflow jobs missing: {filename}")
        for job in jobs.values():
            require(isinstance(job, dict), f"Invalid job: {filename}")
            require("permissions" not in job or job["permissions"] == {"contents": permission}, f"Job widens workflow permissions: {filename}")
            require(isinstance(job.get("steps"), list) and bool(job["steps"]), f"Job steps missing: {filename}")
            timeout = job.get("timeout-minutes", "")
            require(str(timeout).isdigit() and 0 < int(timeout) <= 15, f"Job needs a bounded timeout: {filename}")


def main() -> None:
    validate_determinism()
    validate_assets()
    validate_cards()
    validate_gif()
    validate_documents()
    validate_workflows()
    size = (ASSETS / "terminal.gif").stat().st_size / 1024
    print(f"Validated deterministic assets, seamless profile order, safe SVGs, automatic seven-page 4x2 deck, terminal GIF ({size:.1f} KiB), links, and workflows.")


if __name__ == "__main__":
    main()
