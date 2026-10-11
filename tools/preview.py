"""Local GitHub-width review page; requires optional `pip install Markdown`."""
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".preview"


def main():
    OUT.mkdir(exist_ok=True)
    html = markdown.markdown((ROOT / "README.md").read_text(encoding="utf-8"))
    css = '''
    *{box-sizing:border-box}body{margin:0;background:#0d1117;color:#e6edf3;font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
    .markdown-body{max-width:900px;margin:24px auto;padding:24px;border:1px solid #30363d;border-radius:8px}
    p{margin:0 0 12px}picture{display:inline}img{max-width:100%;height:auto;vertical-align:middle}a{color:#58a6ff;text-decoration:none}details{font-size:11px;color:#8b949e;margin-top:10px}details p{font-size:14px}
    summary{cursor:pointer}div[align=center]{margin:6px 0 12px}p[align=center] a{display:inline-block;margin:2px}
    @media(max-width:500px){.markdown-body{padding:10px;margin:8px;border:0}p{margin-bottom:8px}}
    @media(prefers-color-scheme:light){body{background:#fff;color:#1f2328}.markdown-body{border-color:#d1d9e0}a{color:#0969da}details{color:#59636e}}
    '''
    (OUT / "index.html").write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="../"><title>Tahir — local profile preview</title><style>{css}</style></head><body><main class="markdown-body">{html}</main></body></html>', encoding="utf-8")
    print(OUT / "index.html")


if __name__ == '__main__':
    main()
