from __future__ import annotations

import argparse
import json
import os
import tempfile
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from html import escape
from pathlib import Path

from common import BG, CYAN, MUTED, TEXT, text, write_asset


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "tools" / "data" / "github-snapshot.json"
USER = "thrturker1"
PROFILE_URL = f"https://api.github.com/users/{USER}"


def nonnegative_integer(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"Invalid or missing {field}")
    return value


def validate_snapshot(data: object) -> dict[str, object]:
    if not isinstance(data, dict) or data.get("login") != USER:
        raise ValueError("Snapshot does not identify the expected GitHub account")
    counts = {
        field: nonnegative_integer(data.get(field), field)
        for field in (
            "public_repos", "owned_source_repos", "followers", "following",
            "detected_primary_languages",
        )
    }
    if counts["owned_source_repos"] > counts["public_repos"]:
        raise ValueError("Source repository count exceeds public repository count")
    if counts["detected_primary_languages"] > counts["owned_source_repos"]:
        raise ValueError("Primary language count exceeds source repository count")
    snapshot_date = data.get("snapshot_date")
    if not isinstance(snapshot_date, str) or date.fromisoformat(snapshot_date).isoformat() != snapshot_date:
        raise ValueError("Invalid or missing snapshot date")
    if data.get("source") != PROFILE_URL:
        raise ValueError("Invalid or missing snapshot source")
    return data


def request_json(url: str, token: str | None) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "tahir-control-room-stats",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=25) as response:
        return json.load(response)


def fetch_live() -> dict[str, object]:
    token = os.environ.get("GITHUB_TOKEN")
    profile = request_json(PROFILE_URL, token)
    if not isinstance(profile, dict) or profile.get("login") != USER:
        raise ValueError("Unexpected GitHub profile response")
    public_repos = nonnegative_integer(profile.get("public_repos"), "public_repos")
    followers = nonnegative_integer(profile.get("followers"), "followers")
    following = nonnegative_integer(profile.get("following"), "following")
    repos: list[dict[str, object]] = []
    seen_ids: set[int] = set()
    page = 1
    while True:
        batch = request_json(
            f"{PROFILE_URL}/repos?per_page=100&type=owner&sort=full_name&direction=asc&page={page}", token
        )
        if not isinstance(batch, list) or len(batch) > 100:
            raise ValueError("Unexpected GitHub repository response")
        for repo in batch:
            if not isinstance(repo, dict):
                raise ValueError("Invalid repository record")
            repo_id = nonnegative_integer(repo.get("id"), "repository id")
            owner = repo.get("owner")
            if repo_id == 0 or repo_id in seen_ids:
                raise ValueError("Invalid or duplicate repository id")
            if not isinstance(owner, dict) or owner.get("login") != USER:
                raise ValueError("Unexpected repository owner")
            if repo.get("private") is not False or type(repo.get("fork")) is not bool:
                raise ValueError("Invalid repository visibility or fork status")
            if "language" not in repo or (
                repo["language"] is not None
                and (not isinstance(repo["language"], str) or not repo["language"].strip())
            ):
                raise ValueError("Invalid or missing repository language")
            seen_ids.add(repo_id)
            repos.append(repo)
        if len(batch) < 100 or len(repos) >= public_repos:
            break
        page += 1
    if len(repos) != public_repos:
        raise ValueError("Repository listing is incomplete or changed during refresh")
    sources = [repo for repo in repos if not repo["fork"]]
    languages = {repo["language"] for repo in sources if repo["language"] is not None}
    return validate_snapshot({
        "login": profile["login"],
        "name": profile.get("name"),
        "public_repos": public_repos,
        "owned_source_repos": len(sources),
        "followers": followers,
        "following": following,
        "detected_primary_languages": len(languages),
        "snapshot_date": datetime.now(timezone.utc).date().isoformat(),
        "source": PROFILE_URL,
    })


def load_snapshot() -> dict[str, object]:
    return validate_snapshot(json.loads(SNAPSHOT.read_text(encoding="utf-8")))


def save_snapshot(data: dict[str, object]) -> None:
    validate_snapshot(data)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=SNAPSHOT.parent,
            prefix="github-snapshot-", suffix=".json", delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        os.replace(temporary_path, SNAPSHOT)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def generate(data: dict[str, object]) -> None:
    validate_snapshot(data)
    metrics = [
        ("PUBLIC REPOS", str(data["public_repos"])),
        ("SOURCE REPOS", str(data["owned_source_repos"])),
        ("PRIMARY LANGS", str(data["detected_primary_languages"])),
        ("FOLLOWERS", str(data["followers"])),
    ]
    out = []
    for i, (label, value) in enumerate(metrics):
        center = 150 + i * 300
        if i:
            out.append(f'<path d="M{i * 300} 24v48" stroke="{CYAN}" stroke-opacity=".16"/>')
        out.append(text(center, 48, value, size=32, fill=TEXT, weight=700, anchor="middle"))
        out.append(text(center, 72, label, size=11, fill=MUTED, anchor="middle", spacing=1.6))
    body = f'''
<desc>Public GitHub snapshot for {USER}, dated {escape(str(data['snapshot_date']))}. Source: {PROFILE_URL}; repository details: {PROFILE_URL}/repos. Source repos are owned public non-forks; primary languages count distinct non-null main languages in those source repos.</desc>
<rect width="1200" height="112" rx="16" fill="{BG}"/>
<path d="M24 .5h1152" stroke="{CYAN}" stroke-opacity=".18"/>
{''.join(out)}
{text(1174, 100, str(data['snapshot_date']), size=9, fill=MUTED, anchor='end', spacing=.8, opacity=.7)}
'''
    write_asset("github-stats.svg", body, width=1200, height=112)


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
                raise SystemExit("GitHub refresh failed and no verified snapshot exists.") from None
            print(f"GitHub refresh failed ({type(exc).__name__}); preserving the verified snapshot and its date.")
            data = load_snapshot()
    generate(data)
    print(f"Generated activity snapshot for {data['snapshot_date']}.")


if __name__ == "__main__":
    main()
