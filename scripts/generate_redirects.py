#!/usr/bin/env python3
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
STATIC = ROOT / "static"

def parse_redirect(frontmatter: str) -> str | None:
    for line in frontmatter.splitlines():
        if line.strip().startswith("redirect"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                return parts[1].strip()
    return None

def render_redirect(target: str, title: str = "Redirecting") -> str:
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta http-equiv=\"refresh\" content=\"0; url={target}\">
  <link rel=\"canonical\" href=\"{target}\">
  <title>{title}</title>
</head>
<body>
  <p>If you are not redirected automatically, <a href=\"{target}\">continue to {target}</a>.</p>
</body>
</html>"""

def main():
    for path in ROOT.glob("*.html"):
        text = path.read_text(encoding="utf-8").strip()
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        target = parse_redirect(parts[1])
        if not target:
            continue
        output = STATIC / path.name
        output.write_text(render_redirect(target, title=path.stem), encoding="utf-8")
        print(f"Generated redirect for {path.name} -> {target}")

if __name__ == "__main__":
    main()
