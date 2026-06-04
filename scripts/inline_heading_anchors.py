from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANCHOR_HEADING_RE = re.compile(
    r'^<a id="([^"]+)"></a>\n(#{1,6} [^\n]*?)(?:\s+\{#[^}]+\})?$',
    re.MULTILINE,
)


def inline_heading_anchors(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        anchor = match.group(1)
        heading = match.group(2).rstrip()
        return f"{heading} {{#{anchor}}}"

    updated = ANCHOR_HEADING_RE.sub(replace, text)
    path.write_text(updated, encoding="utf-8")


def main() -> None:
    for filename in ("EN.md", "ZH_TW.md"):
        inline_heading_anchors(ROOT / filename)


if __name__ == "__main__":
    main()
