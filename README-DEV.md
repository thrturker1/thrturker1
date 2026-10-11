# Control Room — maintainer guide

The profile is a compact sequence of locally generated artwork. `README.md` contains the linked images, technology navigation, and a collapsed text inventory; the repeated section headings, biography paragraphs, Verify/Create panel, and Agent Fabric panel are no longer displayed. `PROFILE-STATIC.md` provides a motion-free version.

## Source and output

```text
README.md                    # primary animated profile
PROFILE-STATIC.md            # motion-free profile
arsenal/1.md … 7.md           # manually navigable technology pages
assets/                      # generated, committed images
tools/
  design.py                  # canonical hero, technology deck, studio, social images
  common.py                  # shared SVG primitives used by the stats generator
  generate_terminal.py       # terminal GIF and static SVG/PNG
  generate_stats.py          # validated public GitHub snapshot and stats strip
  generate_all.py            # offline entry point for the current generators
  fetch_icons.py             # explicit upstream icon refresh; requires network
  icons/                     # vendored logos, licenses, sources.json checksums
  data/github-snapshot.json # last verified public API snapshot
.github/workflows/
  generate-assets.yml        # reproducibility and asset checks
  update-stats.yml           # scheduled public-data refresh
```

`tools/generate_assets.py` and unused images remain in the repository as legacy material. They are not the canonical generators or displayed modules for the redesigned profile. Run `generate_all.py`, which invokes `design.py`, instead of the legacy generator.

| Module | Current design |
| --- | --- |
| Hero | 1200 × 350; identity and biography alternate in a 14-second loop. Static and reduced-motion versions are available. |
| Technology deck | 1200 × 342; four columns and two rows. Blender, Godot, Unity, and .NET stay pinned in the top row; the lower four cards rotate through seven pages, six seconds per page. |
| Addictity Games | 1200 × 266; an original animated gateway, with the whole image linking to the studio. |
| Terminal | 1080 × 240; three compact scenes, 91 GIF frames, approximately 49 KiB in the current local render. Static SVG and PNG are also generated. |
| GitHub stats | 1200 × 112; public repositories, owned source repositories, detected primary languages, followers, and a small snapshot date. |
| Social links | Five separate icon images, each with its own clickable destination. |

## Regenerate and validate

Use Python 3.10 or newer and the pinned dependencies:

```bash
python -m pip install -r requirements.txt
python tools/generate_all.py
python tools/validate.py
```

Normal generation is offline: it uses the committed icons and GitHub snapshot. The validator regenerates the output and checks deterministic generation, SVG/XML, GIF animation, local Markdown/image paths, required public links, workflows, and asset size limits. Inspect the generated images visually as well, including the static profile and every technology page.

No fonts are bundled. SVG text uses system font fallbacks; the terminal generator rasterizes an available local font. Repeated generation is deterministic within the same environment, but GIF/PNG bytes and exact text rendering can differ between Windows and Linux because their fonts and rasterizers differ. The verification workflow therefore does not require a cross-platform byte match for raster images.

## Technology logos and navigation

Technology logos are embedded from `tools/icons`, not fetched by profile visitors. `sources.json` records pinned upstream URLs and SHA-256 checksums. Most marks come from Simple Icons 14.0.0 under CC0; the Devicon v2.16.0 marks use its MIT license. License files are retained alongside the SVGs. Gauge uses its official logo from the pinned `getgauge/gauge.org` commit `b20ecfe39a0b74ba3d75476d4eb2ef783d431a35`; its source is recorded separately in the manifest. AI concept icons are original artwork. Brand names and marks retain their respective owners' rights.

Refreshing upstream icons is an explicit maintenance operation that requires network access:

```bash
python tools/fetch_icons.py
python tools/generate_all.py
python tools/validate.py
```

Review the changed SVGs, licenses, and checksum manifest before committing an upstream refresh. Normal regeneration never downloads logos.

GitHub Markdown cannot run the JavaScript or mutable inline state needed for a click-controlled carousel. The main image therefore advances automatically. The arrows and numbered links open real static pages in `arsenal/1.md` through `arsenal/7.md`, where previous/next links provide manual navigation. They do not change the current frame inside the README. Each page keeps the same pinned top row and four lower cards, and the complete text inventory is available in the collapsed section.

## Public data and links

Refresh the public GitHub data explicitly with:

```bash
python tools/generate_stats.py
```

Or rebuild only the stats strip from its committed snapshot:

```bash
python tools/generate_stats.py --offline
```

The refresh validates the account identity, integer counts, repository ownership, visibility, fork state, and primary-language fields. It paginates the repository listing and rejects incomplete, duplicate, or inconsistent results. Cached data is also validated before rendering. A failed request or invalid payload keeps the previous verified snapshot and its original date; missing values are never silently turned into zero. Successful snapshot writes are atomic. The SVG description records the API source and the meaning of the counts.

The stats are a dated public snapshot, not a live contribution feed. Source repositories exclude forks; primary languages count distinct non-null main languages in those source repositories. No streak, contribution, private-repository, or proficiency count is inferred. The scheduled workflow uses `GITHUB_TOKEN` for API access and commits changed snapshot/output files when enabled in GitHub Actions.

Current destinations are [GitHub](https://github.com/thrturker1), [LinkedIn](https://www.linkedin.com/in/thrturker/), [Instagram](https://www.instagram.com/turkertahirr/), [Portfolio](https://sevro49.github.io/My-Portfolio/public/index.html), and [Addictity Games](https://addictitygames.com). The studio panel uses the studio identity and public description; recheck the live studio site before adding release dates, platforms, or current game status. A stored URL or successful local render does not establish the destination's current availability.

## Animation and GitHub rendering

The images have self-contained dark backgrounds and no scripts, remote stylesheets, remote fonts, or runtime image dependencies. Animated modules have static fallbacks; `README.md` uses reduced-motion image sources, and `PROFILE-STATIC.md` gives an explicit motion-free route regardless of browser preference handling. Descriptive alternative text preserves the identity, tool names, and link purposes.

Local browser previews can verify SVG image animation, GIF playback, layout, and links. They cannot establish how GitHub's sanitizer, image proxy, cache, or a particular browser will render the published README. Inspect the profile on GitHub after publication, including reduced-motion behavior and manual technology navigation. This revision was prepared locally; it has not been pushed or deployed. Running the generators and validator does not publish it.
