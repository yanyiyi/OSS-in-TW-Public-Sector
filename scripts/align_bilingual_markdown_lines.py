from __future__ import annotations

import difflib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZH_PATH = ROOT / "ZH_TW.md"
EN_PATH = ROOT / "EN.md"


def split_blocks(text: str) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines():
        if not line.strip():
            if current:
                blocks.append(current)
                current = []
            continue
        current.append(line.rstrip())
    if current:
        blocks.append(current)
    return blocks


def block_signature(block: list[str]) -> str:
    first = block[0]
    if first.startswith("# "):
        return "TITLE"

    heading = re.match(
        r"^(#{2,6})\s+(.+?)(?:\s+\{#([^}]+)\}|\s+<span id=\"([^\"]+)\"></span>)?$",
        first,
    )
    if heading:
        level = len(heading.group(1))
        title = heading.group(2)
        anchor = heading.group(3) or heading.group(4)
        if anchor:
            return f"H:{anchor}"
        if "文件修訂歷史" in title or "Document Revision History" in title:
            return "H:document-revision-history"
        if title in {"目錄", "Table of Contents"}:
            return "H:toc"
        return f"H{level}"

    if first.startswith("|"):
        return "TABLE"
    if first.startswith("!["):
        return "IMAGE"
    if first.startswith("*") and first.endswith("*"):
        return "CAPTION"
    if first.startswith("[^"):
        return "NOTE"
    if re.match(r"^https?://", first):
        return "URL"
    if first.startswith("- ") or re.match(r"^\d+\.\s", first):
        return "LIST"
    return "P"


def align_blocks(
    zh_blocks: list[list[str]], en_blocks: list[list[str]]
) -> list[tuple[list[str], list[str]]]:
    zh_signatures = [block_signature(block) for block in zh_blocks]
    en_signatures = [block_signature(block) for block in en_blocks]
    matcher = difflib.SequenceMatcher(None, zh_signatures, en_signatures, autojunk=False)

    pairs: list[tuple[list[str], list[str]]] = []
    for tag, zh_start, zh_end, en_start, en_end in matcher.get_opcodes():
        if tag == "equal":
            for zh_index, en_index in zip(range(zh_start, zh_end), range(en_start, en_end)):
                pairs.append((zh_blocks[zh_index], en_blocks[en_index]))
            continue

        zh_run = zh_blocks[zh_start:zh_end]
        en_run = en_blocks[en_start:en_end]
        run_length = max(len(zh_run), len(en_run))
        for index in range(run_length):
            zh_block = zh_run[index] if index < len(zh_run) else []
            en_block = en_run[index] if index < len(en_run) else []
            pairs.append((zh_block, en_block))

    return pairs


def render_aligned(pairs: list[tuple[list[str], list[str]]]) -> tuple[str, str]:
    zh_lines: list[str] = []
    en_lines: list[str] = []

    for zh_block, en_block in pairs:
        block_height = max(len(zh_block), len(en_block), 1)
        zh_lines.extend(zh_block + [""] * (block_height - len(zh_block)))
        en_lines.extend(en_block + [""] * (block_height - len(en_block)))
        zh_lines.append("")
        en_lines.append("")

    if zh_lines and zh_lines[-1] == "":
        zh_lines.pop()
        en_lines.pop()

    return "\n".join(zh_lines).rstrip() + "\n", "\n".join(en_lines).rstrip() + "\n"


def main() -> None:
    zh_blocks = split_blocks(ZH_PATH.read_text(encoding="utf-8"))
    en_blocks = split_blocks(EN_PATH.read_text(encoding="utf-8"))
    pairs = align_blocks(zh_blocks, en_blocks)
    zh_text, en_text = render_aligned(pairs)
    ZH_PATH.write_text(zh_text, encoding="utf-8")
    EN_PATH.write_text(en_text, encoding="utf-8")


if __name__ == "__main__":
    main()
