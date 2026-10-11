from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "assets"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "tools" / "generate_all.py")], cwd=ROOT, check=True)
    first = {p.name: sha(p) for p in ASSETS.glob("*") if p.is_file()}
    subprocess.run([sys.executable, str(ROOT / "tools" / "generate_all.py")], cwd=ROOT, check=True)
    second = {p.name: sha(p) for p in ASSETS.glob("*") if p.is_file()}
    changed = sorted(name for name, digest in first.items() if second.get(name) != digest)
    if changed:
        raise SystemExit(f"Non-deterministic generated assets: {', '.join(changed)}")

    for path in sorted(ASSETS.glob("*.svg")):
        ET.parse(path)
        if path.stat().st_size > 350_000:
            raise SystemExit(f"SVG is unexpectedly large: {path.name}")

    gif = ASSETS / "terminal.gif"
    with Image.open(gif) as image:
        if not getattr(image, "is_animated", False) or image.n_frames < 20:
            raise SystemExit("terminal.gif is not meaningfully animated")
        if image.width > 1200 or image.height > 700:
            raise SystemExit("terminal.gif exceeds the intended render bounds")
    if gif.stat().st_size > 5_000_000:
        raise SystemExit("terminal.gif exceeds the 5 MB performance budget")

    markdown = README.read_text(encoding="utf-8")
    local_images = set(re.findall(r'(?:src=["\']|\]\()(?P<path>assets/[^"\')]+)', markdown))
    missing = sorted(path for path in local_images if not (ROOT / path).is_file())
    if missing:
        raise SystemExit(f"Missing README assets: {', '.join(missing)}")

    required_links = {
        "https://github.com/thrturker1",
        "https://www.linkedin.com/in/thrturker/",
        "https://www.instagram.com/turkertahirr/",
        "https://sevro49.github.io/My-Portfolio/public/index.html",
        "https://addictitygames.com",
    }
    absent = sorted(link for link in required_links if link not in markdown)
    if absent:
        raise SystemExit(f"Required public links absent from README: {', '.join(absent)}")

    for workflow in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        with workflow.open(encoding="utf-8") as handle:
            yaml.safe_load(handle)

    print(f"Validated {len(list(ASSETS.glob('*.svg')))} SVGs, {gif.name} ({gif.stat().st_size / 1024:.1f} KiB), README paths, links, and workflows.")


if __name__ == "__main__":
    main()
