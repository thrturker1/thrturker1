"""Explicit maintenance command; normal generation uses committed, offline icons."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools" / "icons"
SIMPLE = "https://raw.githubusercontent.com/simple-icons/simple-icons/14.0.0"
DEVICON = "https://raw.githubusercontent.com/devicons/devicon/v2.16.0"
SLUGS = "blender godotengine unity dotnet docker kubernetes apachekafka apachejmeter k6 gauge selenium playwright postman nodedotjs spring react nextdotjs vuedotjs javascript typescript tailwindcss tauri electron github linkedin instagram".split()
URLS = {slug: f"{SIMPLE}/icons/{slug}.svg" for slug in SLUGS}
URLS.update({"csharp": f"{DEVICON}/icons/csharp/csharp-plain.svg", "java": f"{DEVICON}/icons/java/java-plain.svg"})
URLS.update({
    "playwright": f"{DEVICON}/icons/playwright/playwright-original.svg",
    "linkedin": f"{DEVICON}/icons/linkedin/linkedin-plain.svg",
    "gauge": "https://raw.githubusercontent.com/getgauge/gauge.org/b20ecfe39a0b74ba3d75476d4eb2ef783d431a35/source/assets/images/gauge-logo_white.svg",
})


def fetch(item):
    slug, url = item
    req = urllib.request.Request(url, headers={"User-Agent": "tahir-profile-assets"})
    with urllib.request.urlopen(req, timeout=25) as response:
        data = response.read()
    ET.fromstring(data)
    (TARGET / f"{slug}.svg").write_bytes(data)
    return slug, {"url": url, "sha256": sha256(data).hexdigest()}


def main():
    TARGET.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {slug: pool.submit(fetch, (slug, url)) for slug, url in URLS.items()}
        manifest, failures = {}, []
        for slug, future in futures.items():
            try:
                key, value = future.result()
                manifest[key] = value
            except Exception as exc:
                failures.append(f"{slug}: {exc}")
        if failures:
            raise SystemExit("\n".join(failures))
    (TARGET / "sources.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for name, url in [("SIMPLE-ICONS-LICENSE.md", f"{SIMPLE}/LICENSE.md"), ("DEVICON-LICENSE", f"{DEVICON}/LICENSE")]:
        with urllib.request.urlopen(url, timeout=25) as response:
            (TARGET / name).write_bytes(response.read())
    print(f"Vendored {len(manifest)} icons with pinned sources and hashes.")


if __name__ == "__main__":
    main()
