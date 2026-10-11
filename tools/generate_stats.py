from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from common import CYAN, GREEN, HIGHLIGHT, MUTED, SURFACE, TEXT, base, card, defs, section_label, text, write_asset


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "tools" / "data" / "github-snapshot.json"
USER = "thrturker1"


def request_json(url: str, token: str | None) -> object:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "tahir-control-room-stats"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=25) as response:
        return json.load(response)


def fetch_live() -> dict[str, object]:
    token = os.environ.get("GITHUB_TOKEN")
    profile = request_json(f"https://api.github.com/users/{USER}", token)
    repos = request_json(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner", token)
    if not isinstance(profile, dict) or not isinstance(repos, list):
        raise ValueError("Unexpected GitHub API response")
    sources = [repo for repo in repos if not repo.get("fork")]
    languages = {repo.get("language") for repo in sources if repo.get("language")}
    return {
        "login": profile.get("login", USER),
        "name": profile.get("name") or "Tahir",
        "public_repos": int(profile.get("public_repos", 0)),
        "owned_source_repos": len(sources),
        "followers": int(profile.get("followers", 0)),
        "following": int(profile.get("following", 0)),
        "detected_primary_languages": len(languages),
        "snapshot_date": datetime.now(timezone.utc).date().isoformat(),
        "source": f"https://api.github.com/users/{USER}",
    }


def load_snapshot() -> dict[str, object]:
    return json.loads(SNAPSHOT.read_text(encoding="utf-8"))


def save_snapshot(data: dict[str, object]) -> None:
    SNAPSHOT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def generate(data: dict[str, object]) -> None:
    metrics = [
        ("PUBLIC REPOS", str(data["public_repos"]), "GitHub account total"),
        ("SOURCE REPOS", str(data["owned_source_repos"]), "Owned • non-fork"),
        ("PRIMARY LANGS", str(data["detected_primary_languages"]), "Detected in source repos"),
        ("FOLLOWERS", str(data["followers"]), "Public account signal"),
    ]
    out = []
    for i, (label, value, note) in enumerate(metrics):
        x = 33 + i * 288
        out.append(card(x, 124, 264, 142))
        out.append(text(x + 22, 155, f"0{i + 1} / {label}", size=10, fill=CYAN, spacing=1.2))
        out.append(text(x + 22, 220, value, size=48, fill=TEXT, weight=700))
        out.append(text(x + 98, 218, note, size=9, fill=MUTED, spacing=.3))
        out.append(f'<circle cx="{x + 236}" cy="{152}" r="4" fill="{GREEN}"/>')
    body = defs() + base(1200, 330, "CR://GITHUB_TELEMETRY / PUBLIC_API") + f'''
{section_label('06', 'GITHUB ACTIVITY SNAPSHOT')}
{text(32, 94, 'REAL PUBLIC DATA • LOCALLY RENDERED • NO THIRD-PARTY CARD SERVICE', size=11, fill=MUTED, spacing=1)}
{''.join(out)}
{text(32, 304, f"SYNC {data['snapshot_date']} UTC", size=10, fill=MUTED, spacing=1)}
{text(1168, 304, f"SOURCE // api.github.com/users/{USER}", size=10, fill=HIGHLIGHT, anchor='end', spacing=.5)}
'''
    write_asset("github-stats.svg", body, width=1200, height=330)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate local GitHub profile telemetry SVG.")
    parser.add_argument("--offline", action="store_true", help="Use the committed verified snapshot without network access.")
    args = parser.parse_args()

    if args.offline:
        data = load_snapshot()
    else:
        try:
            data = fetch_live()
            save_snapshot(data)
        except (OSError, ValueError, urllib.error.URLError) as exc:
            if not SNAPSHOT.exists():
                raise SystemExit(f"GitHub API unavailable and no snapshot exists: {exc}") from exc
            print(f"GitHub API unavailable; preserving verified snapshot: {exc}")
            data = load_snapshot()
    generate(data)
    print(f"Generated activity snapshot for {data['snapshot_date']}.")


if __name__ == "__main__":
    main()
