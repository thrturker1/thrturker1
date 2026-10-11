# Control Room — maintainer guide

This repository is the source for Tahir's GitHub profile README. Its visual system is generated locally so the profile does not depend on external badge or statistics services.

## Structure

```text
README.md
assets/                      # generated, committed profile assets
tools/
  common.py                  # palette and shared SVG primitives
  generate_assets.py        # hero, diagrams, stack, studio, contacts
  generate_terminal.py      # deterministic animated terminal GIF
  generate_stats.py         # GitHub API snapshot and stats SVG
  generate_all.py           # offline one-command regeneration
  terminal.tape             # optional VHS recreation path
  data/github-snapshot.json # last verified public API snapshot
.github/workflows/
  generate-assets.yml       # reproducibility check
  update-stats.yml          # scheduled public-data refresh
```

## Regenerate locally

Python 3.10+ is recommended.

```bash
python -m pip install -r requirements.txt
python tools/generate_all.py
```

`generate_all.py` is intentionally offline: it uses the committed public-data snapshot. To refresh that snapshot and the GitHub panel from the live public API:

```bash
python tools/generate_stats.py
```

If the API is temporarily unavailable, the generator keeps the last verified snapshot. In GitHub Actions, the built-in `GITHUB_TOKEN` is used only to read public API data and commit the regenerated telemetry asset.

## Terminal animation

`tools/generate_terminal.py` is the canonical generator. It renders actual progressive character frames with natural command pauses, a blinking cursor, scanlines, and restrained interference. Pillow is the only dependency. The resulting GIF is optimized and committed under `assets/terminal.gif`.

`tools/terminal.tape` provides an optional Charmbracelet VHS route for maintainers who already use VHS. Its output is separate so it cannot unexpectedly replace the deterministic canonical GIF.

## GitHub compatibility decisions

- All visual modules use self-contained dark backgrounds, so they remain coherent in GitHub light and dark themes.
- No JavaScript, iframe, remote CSS, webfont, or remote image dependency is used.
- SVG animation is decorative. Primary labels and final states exist in the base SVG, so the assets remain readable when animation is blocked. Each animated SVG also includes a reduced-motion rule.
- The terminal is a GIF because progressive typing is more consistent across GitHub's image pipeline than animated SVG text clipping.
- Expansion uses native `<details>` and `<summary>` elements; no fake interaction is presented.
- Technology marks are compact in-house interface glyphs rather than hot-linked logo assets. Technology names remain explicit and accessible in alt text.
- Telemetry values come from the public GitHub API and are never inferred. There are no streak numbers, proficiency percentages, or fabricated contribution counts.

## Validation

Run the complete local validator:

```bash
python tools/validate.py
```

It regenerates all assets, validates XML, checks GIF animation, verifies local README paths, checks the expected public links, parses both workflow files, and ensures the generated assets are within size limits.

## Editing the visual system

The canonical palette lives in `tools/common.py`. Keep important text at or above the current contrast level and avoid placing required information only in animation. Decorative randomness must use a fixed seed so repeated generation stays deterministic.

The Addictity Games panel contains only public studio information verified from the live site on 2026-10-11. Re-check the site before adding a title, platform, release date, or status.
