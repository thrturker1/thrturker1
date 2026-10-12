# Control Room — maintainer guide

The public profile is one continuous control-room chassis. `README.md` places four generated modules directly against each other in this order: hero, terminal, automatic technology deck, and Addictity Games. Only the social buttons sit outside the chassis. Repeated headings, manual page indexes, GitHub telemetry, Verify/Create, and Agent Fabric are not displayed.

`PROFILE-STATIC.md` keeps the same order with motion-free artwork.

## Source and output

```text
README.md                    # primary animated profile
PROFILE-STATIC.md            # motion-free profile
assets/                      # generated, committed images
tools/
  design.py                  # chassis segments, technology deck, studio, social images
  generate_terminal.py       # 1200 px terminal GIF and static SVG/PNG
  generate_all.py            # offline entry point
  fetch_icons.py             # explicit upstream icon refresh; requires network
  icons/                     # vendored logos, licenses, sources.json checksums
```

| Segment | Current design |
| --- | --- |
| Hero | 1200 × 350, rounded upper chassis edge; identity and biography alternate every 14 seconds. |
| Terminal | 1200 × 240, placed directly below the hero with shared vertical rails. |
| Technology deck | 1200 × 342, four columns and two rows. Blender, Godot, Unity, and .NET stay pinned; the lower row advances automatically every six seconds. The dots are status indicators, not links. |
| Addictity Games | 1200 × 278, rounded lower chassis edge; No Respite and Goblet are shown as in-development projects. The whole segment links to the studio. |
| Social links | Five compact, independently clickable icon images. |

`tools/generate_stats.py`, its snapshot, and the scheduled refresh workflow remain as legacy telemetry tooling, but the generated stats strip is not referenced by either public profile document.

## Regenerate and validate

Use Python 3.10 or newer and the pinned dependencies:

```bash
python -m pip install -r requirements.txt
python tools/generate_all.py
python tools/validate.py
```

The validator regenerates output twice, checks determinism, SVG safety, terminal animation, the 4 × 2 technology grid, public links, README segment order, and workflow constraints. It also rejects any reintroduction of the removed manual index or GitHub telemetry panel.

No fonts are bundled. SVG text uses system font fallbacks; the terminal generator rasterizes an available local font. GIF and PNG bytes can vary between Windows and Linux because font rasterizers differ, so CI validates the raster animation without cross-platform byte comparison.

## Technology logos

Technology logos are embedded from `tools/icons`; profile visitors never fetch remote artwork. `sources.json` records pinned upstream URLs and SHA-256 checksums. Most marks come from Simple Icons 14.0.0 under CC0, Devicon v2.16.0 marks use its MIT license, and Gauge uses its official logo from the pinned `getgauge/gauge.org` commit recorded in the manifest. AI concept icons are original artwork.

Refreshing icons is an explicit network operation:

```bash
python tools/fetch_icons.py
python tools/generate_all.py
python tools/validate.py
```

## Links and rendering

Current destinations are [GitHub](https://github.com/thrturker1), [LinkedIn](https://www.linkedin.com/in/thrturker/), [Instagram](https://www.instagram.com/turkertahirr/), [Portfolio](https://thrturker.com), and [Addictity Games](https://addictitygames.com).

GitHub README content cannot run JavaScript, so the technology deck uses a self-contained SVG animation instead of click-controlled state. Reduced-motion visitors receive the first static 4 × 2 page. All artwork is self-contained: no scripts, remote stylesheets, remote fonts, or runtime image dependencies.

Local browser previews can verify the seamless layout, SVG/GIF playback, mobile width, and fallbacks. They cannot reproduce every GitHub image-proxy or sanitizer behavior. This revision is local until explicitly committed and pushed.
