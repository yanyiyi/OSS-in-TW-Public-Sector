from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


CHAPTER_SECTION_PREFIXES = {
    "ZH_TW.md": {
        "第一章": "1.",
        "第二章": "2.",
        "第三章": "3.",
        "第四章": "4.",
    },
    "EN.md": {
        "Chapter 1": "1.",
        "Chapter 2": "2.",
        "Chapter 3": "3.",
        "Chapter 4": "4.",
    },
}


DROP_LINES = {
    "ZH_TW.md": {
        "Introduction to Open-Source Software",
        "Evaluation of Open-Source Software",
        "Applications",
        "Evaluation of Open-Source Software Applications",
        "重要性",
        "",
    },
    "EN.md": {
        "Evaluation of Open-Source Software Applications",
        "統一表格位置與文字型號",
        "附錄四 需求規劃自主檢核表",
        "Assessment Items",
        "",
    },
}


def remove_chapter_outline_headings(text: str, filename: str) -> str:
    lines = text.splitlines()
    prefixes = CHAPTER_SECTION_PREFIXES[filename]
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if line.startswith("## "):
            prefix = None
            for chapter_key, section_prefix in prefixes.items():
                if chapter_key in line:
                    prefix = section_prefix
                    break
            if prefix:
                j = i + 1
                pending: list[str] = []
                while j < len(lines) and (lines[j] == "" or re.match(rf"^### {re.escape(prefix)}\d\b", lines[j])):
                    pending.append(lines[j])
                    j += 1
                section_headings = [p for p in pending if p.startswith("### ")]
                if len(section_headings) > 1:
                    kept_first = False
                    for p in pending:
                        if p == "":
                            continue
                        if p.startswith("### ") and not kept_first:
                            out.extend(["", p, ""])
                            kept_first = True
                    i = j
                    continue
        i += 1
    return "\n".join(out)


def drop_artifact_lines(text: str, filename: str) -> str:
    drops = DROP_LINES[filename]
    lines = [line for line in text.splitlines() if line.strip() not in drops]
    return "\n".join(lines)


def insert_once(text: str, needle: str, insertion: str) -> str:
    if insertion.strip() in text:
        return text
    return text.replace(needle, insertion + "\n\n" + needle, 1)


def cleanup_zh(text: str) -> str:
    replacements = [
        ("開源軟體授權條款的主要功能", "### 1.3 開源軟體基本概念與授權條款類型"),
        ("總結第一章各小節的說明", "### 1.4 開源軟體與公共程式"),
        ("在2.1小節裡面", "### 2.2 開源軟體使用效益與風險評估"),
        ("導入開源軟體時", "### 2.3 開源軟體導入模式"),
        ("採用開源軟體的開發流程", "### 2.4 開源軟體治理制度"),
        ("#### 3.2.1 上游優先", "### 3.2 軟體開發流程：開發與測試開源注意事項"),
        ("#### 3.3.1 開源軟體授權合規檢核", "### 3.3 軟體開發流程：上線與驗收開源注意事項"),
        ("#### 3.4.1 維護政府開源專案的要點", "### 3.4 將開發成果開源釋出"),
        ("為協助各級機關有效導入", "### 4.2 開源軟體永續經營"),
        ("開源軟體的採用與開發", "### 4.3 結語"),
    ]
    for needle, heading in replacements:
        text = insert_once(text, needle, heading)
    text = text.replace("## 附錄四 公部門專案導入開源軟體（或公共程式）需求規劃自主檢核表", "### 公部門專案導入開源軟體（或公共程式）需求規劃自主檢核表")
    text = text.replace("## 附錄五 公部門使用開源軟體（或公共程式）授權合規評估檢核表", "### 公部門使用開源軟體（或公共程式）授權合規評估檢核表")
    return text


def cleanup_en(text: str) -> str:
    text = text.replace("he adoption of open-source software", "The adoption of open-source software")
    replacements = [
        ("Open-source software’s licensing agreement", "### 1.3 Basic Concept and Licensing Agreement Types of Open-Source Software"),
        ("Summarizing each subsection of Chapter One", "### 1.4 Open-Source Software and Public Code"),
        ("In Section 2.1, we have comprehensively", "### 2.2 Open-Source Software Benefits and Risks Analysis"),
        ("When implementing open-source software", "### 2.3 Open-Source Software Implementation Model"),
        ("The development process for adopting open-source software", "### 2.4 Open-Source Software Governance System"),
        ("#### 3.2.1 Upstream First", "### 3.2 Software Development Process: Considerations for Open Source During Development and Testing"),
        ("#### 3.3.1 Open-Source Software License Compliance", "### 3.3 Software Development Process: Open-Source Considerations for Go-Live and Acceptance"),
        ("#### 3.4.1 Key Governance Considerations", "### 3.4 Releasing Development Outcomes as Open Source"),
        ("To support government agencies at all levels", "### 4.2 Sustainable Operations"),
        ("The adoption of open-source software and public code", "### 4.3 Conclusion"),
    ]
    for needle, heading in replacements:
        text = insert_once(text, needle, heading)
    appendix_block = (
        "## Appendix I: Terminology\n\n"
        "## Appendix II: FAQ\n\n"
        "## Appendix III: Links\n\n"
        "## Appendix IV: Requirements Planning Self-Assessment Checklist\n\n"
        "## Appendix V: License Compliance Assessment Checklist\n\n"
    )
    text = text.replace(appendix_block, "## Appendix I: Terminology\n\n")
    text = insert_once(text, "Since 2023, the Ministry of Digital Affairs", "## Appendix II: FAQ")
    text = insert_once(text, "Public Code Platform by MODA:", "## Appendix III: Links")
    text = insert_once(text, "This self-assessment checklist is designed", "## Appendix IV: Requirements Planning Self-Assessment Checklist")
    text = insert_once(text, "This assessment checklist is divided", "## Appendix V: License Compliance Assessment Checklist")
    return text


def normalize_spacing(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\n(#{2,4} .+)\n(?!\n)", r"\n\1\n\n", text)
    return text.strip() + "\n"


def main() -> None:
    for filename, cleanup in [("ZH_TW.md", cleanup_zh), ("EN.md", cleanup_en)]:
        path = ROOT / filename
        text = path.read_text(encoding="utf-8")
        text = remove_chapter_outline_headings(text, filename)
        text = drop_artifact_lines(text, filename)
        text = cleanup(text)
        text = normalize_spacing(text)
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
