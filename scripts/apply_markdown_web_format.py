from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


EN_TOC = [
    ("Introduction", "Introduction"),
    ("Chapter 1: Introduction to Open-Source Software", "Chapter 1: Introduction to Open-Source Software"),
    ("1.1 How it started", "1.1 How it started"),
    ("1.2 International Trends and Applications", "1.2 International Trends and Applications"),
    ("1.3 Basic Concept and Licensing Agreement Types of Open-Source Software", "1.3 Basic Concept and Licensing Agreement Types of Open-Source Software"),
    ("1.4 Open-Source Software and Public Code", "1.4 Open-Source Software and Public Code"),
    ("Chapter 2: Open-Source Software Application Evaluation", "Chapter 2: Open-Source Software Application Evaluation"),
    ("2.1 Difference Between Using Open-Source and Proprietary Software", "2.1 Difference Between Using Open-Source and Proprietary Software"),
    ("2.2 Open-Source Software Benefits and Risks Analysis", "2.2 Open-Source Software Benefits and Risks Analysis"),
    ("2.3 Open-Source Software Implementation Model", "2.3 Open-Source Software Implementation Model"),
    ("2.4 Open-Source Software Governance System", "2.4 Open-Source Software Governance System"),
    ("Chapter 3: Open-Source Software Implementation", "Chapter 3: Open-Source Software Implementation"),
    ("3.1 Software Development Process: Needs and Cautions when Designing Open-Source Software", "3.1 Software Development Process: Needs and Cautions when Designing Open-Source Software"),
    ("3.2 Software Development Process: Considerations for Open Source During Development and Testing", "3.2 Software Development Process: Considerations for Open Source During Development and Testing"),
    ("3.3 Software Development Process: Open-Source Considerations for Go-Live and Acceptance", "3.3 Software Development Process: Open-Source Considerations for Go-Live and Acceptance"),
    ("3.4 Releasing Development Outcomes as Open Source", "3.4 Releasing Development Outcomes as Open Source"),
    ("Chapter 4: Open-Source Software Maintenance and Operations", "Chapter 4: Open-Source Software Maintenance and Operations"),
    ("4.1 Open-Source Software Operations and Maintenance", "4.1 Open-Source Software Operations and Maintenance"),
    ("4.2 Sustainable Operations", "4.2 Sustainable Operations"),
    ("4.3 Conclusion", "4.3 Conclusion"),
    ("Appendix I: Terminology", "Appendix I: Terminology"),
    ("Appendix II: FAQ", "Appendix II: FAQ"),
    ("Appendix III: Links", "Appendix III: Links"),
    ("Appendix IV: Requirements Planning Self-Assessment Checklist", "Appendix IV: Requirements Planning Self-Assessment Checklist"),
    ("Appendix V: License Compliance Assessment Checklist", "Appendix V: License Compliance Assessment Checklist"),
]


ZH_TOC = [
    ("緒論", "Introduction"),
    ("第一章 開源軟體介紹", "Chapter 1: Introduction to Open-Source Software"),
    ("1.1 開源軟體發展背景", "1.1 How it started"),
    ("1.2 開源軟體國際趨勢與應用", "1.2 International Trends and Applications"),
    ("1.3 開源軟體基本概念與授權條款類型", "1.3 Basic Concept and Licensing Agreement Types of Open-Source Software"),
    ("1.4 開源軟體與公共程式", "1.4 Open-Source Software and Public Code"),
    ("第二章 開源軟體應用評估", "Chapter 2: Open-Source Software Application Evaluation"),
    ("2.1 使用開源軟體及專有軟體差異說明", "2.1 Difference Between Using Open-Source and Proprietary Software"),
    ("2.2 開源軟體使用效益與風險評估", "2.2 Open-Source Software Benefits and Risks Analysis"),
    ("2.3 開源軟體導入模式", "2.3 Open-Source Software Implementation Model"),
    ("2.4 開源軟體治理制度", "2.4 Open-Source Software Governance System"),
    ("第三章 開源軟體導入方法", "Chapter 3: Open-Source Software Implementation"),
    ("3.1 軟體開發流程：需求與設計開源注意事項", "3.1 Software Development Process: Needs and Cautions when Designing Open-Source Software"),
    ("3.2 軟體開發流程：開發與測試開源注意事項", "3.2 Software Development Process: Considerations for Open Source During Development and Testing"),
    ("3.3 軟體開發流程：上線與驗收開源注意事項", "3.3 Software Development Process: Open-Source Considerations for Go-Live and Acceptance"),
    ("3.4 將開發成果開源釋出", "3.4 Releasing Development Outcomes as Open Source"),
    ("第四章 開源軟體維護與營運", "Chapter 4: Open-Source Software Maintenance and Operations"),
    ("4.1 開源軟體維運", "4.1 Open-Source Software Operations and Maintenance"),
    ("4.2 開源軟體永續經營", "4.2 Sustainable Operations"),
    ("4.3 結語", "4.3 Conclusion"),
    ("附錄一 名詞解釋", "Appendix I: Terminology"),
    ("附錄二 常見問答 FAQ", "Appendix II: FAQ"),
    ("附錄三 參考資源", "Appendix III: Links"),
    ("附錄四 需求規劃自主檢核表", "Appendix IV: Requirements Planning Self-Assessment Checklist"),
    ("附錄五 授權合規評估檢核表", "Appendix V: License Compliance Assessment Checklist"),
]


ZH_HEADING_TO_EN = {
    "緒論": "Introduction",
    "緣起": "Origin",
    "第一章 開源軟體介紹": "Chapter 1: Introduction to Open-Source Software",
    "1.1 開源軟體發展背景": "1.1 How it started",
    "1.2 國際趨勢與應用": "1.2 International Trends and Applications",
    "1.2 開源軟體國際趨勢與應用": "1.2 International Trends and Applications",
    "1.2.1 德國聯邦政府主導開發 openDesk": "1.2.1 German Federal Government Led the Development of openDesk",
    "1.2.2 聯合國提出「數位公共財」的概念": "1.2.2 UN Proposes “Digital Public Goods”",
    "1.2.3 美國的《聯邦程式碼政策》": "1.2.3 The US’ Federal Source Code Policy",
    "1.3 開源軟體基本概念與授權條款類型": "1.3 Basic Concept and Licensing Agreement Types of Open-Source Software",
    "1.3.1 GPL類：AGPL、GPL、LGPL": "1.3.1 GPL：AGPL、GPL、LGPL",
    "1.3.2 Mozilla Public License（MPL） v2": "1.3.2 Mozilla Public License（MPL） v2",
    "1.3.3 Apache License v2": "1.3.3 Apache License v2",
    "1.3.4 MIT License": "1.3.4 MIT License",
    "1.3.5 Boost Software License 1.0": "1.3.5 Boost Software License 1.0",
    "1.3.6 The Unlicense": "1.3.6 The Unlicense",
    "1.4 開源軟體與公共程式": "1.4 Open-Source Software and Public Code",
    "第二章 開源軟體應用評估": "Chapter 2: Open-Source Software Application Evaluation",
    "2.1 使用開源軟體及專有軟體差異說明": "2.1 Difference Between Using Open-Source and Proprietary Software",
    "2.2 開源軟體使用效益與風險評估": "2.2 Open-Source Software Benefits and Risks Analysis",
    "2.2.1 開源軟體的使用效益": "2.2.1 Open-Source Software Benefits",
    "2.2.2 使用開源軟體風險評估": "2.2.2 Risk Analysis of Open-Source Software",
    "2.3 開源軟體導入模式": "2.3 Open-Source Software Implementation Model",
    "2.3.1 開發策略選擇：應用、整合或自主開發？": "2.3.1 Development Strategy: Adopt, integrate or self-build?",
    "2.3.2 查找專案及可參考的平臺": "2.3.2 Explore Projects and Referenceable Platform",
    "2.4 開源軟體治理制度": "2.4 Open-Source Software Governance System",
    "2.4.1 鼓勵制定開源軟體政策": "2.4.1 Open-Source Software Governance System",
    "2.4.2 開源軟體政策及軟體物料清單": "2.4.2 Open-Source Software Policy and Software Bill of Materials",
    "2.4.3 開源合規國際標準介紹": "2.4.3 Introduction to International Open-Source Compliance Standards",
    "第三章 開源軟體導入方法": "Chapter 3: Open-Source Software Implementation",
    "3.1 軟體開發流程：需求與設計開源注意事項": "3.1 Software Development Process: Needs and Cautions when Designing Open-Source Software",
    "3.1.1 開源軟體評估與選型流程": "3.1.1 Open-Source Software Evaluation and Type Selection Process",
    "3.2 軟體開發流程：開發與測試開源注意事項": "3.2 Software Development Process: Considerations for Open Source During Development and Testing",
    "3.2.1 上游優先：避免「開發過多分枝疲勞」": "3.2.1 Upstream First: Avoid “Fork Fatigue”",
    "3.2.2 版本控制與自動化整合": "3.2.2 Version Control and Automated Integration",
    "3.3 軟體開發流程：上線與驗收開源注意事項": "3.3 Software Development Process: Open-Source Considerations for Go-Live and Acceptance",
    "3.3.1 開源軟體授權合規檢核（表）與風險控管建議": "3.3.1 Open-Source Software License Compliance Review (Checklist) and Risk Management Recommendations",
    "3.3.2 驗收的核心：可轉移性、可讀性與永續性": "3.3.2 The core of acceptance: Transferability, Readability and Sustainability",
    "3.3.3 對標國際標準：以公共程式標準評估專案完成度": "3.3.3 Aligning with International Standards: Assessing Project Completion Using the Public Code Standard Framework",
    "3.4 將開發成果開源釋出": "3.4 Releasing Development Outcomes as Open Source",
    "3.4.1 維護政府開源專案的要點": "3.4.1 Key Governance Considerations for Public Code",
    "3.4.2 建立清晰友善的社群貢獻機制": "3.4.2 Establishing Clear and Friendly Community Contribution Processes",
    "3.4.3 積極的社群支持與互動": "3.4.3 Active community support and engagement",
    "第四章 開源軟體維護與營運": "Chapter 4: Open-Source Software Maintenance and Operations",
    "4.1 開源軟體維運": "4.1 Open-Source Software Operations and Maintenance",
    "4.1.1 系統監控": "4.1.1 System Monitoring",
    "4.1.2 日誌管理": "4.1.2 Log Management",
    "4.1.3 容量管理": "4.1.3 Capacity Management",
    "4.1.4 資安管理": "4.1.4 Information Security Management",
    "4.1.5 功能維護": "4.1.5 Functional Maintenance",
    "4.1.6 版本控管": "4.1.6 Version Control",
    "4.1.7 文件管理": "4.1.7 Documentation Management",
    "4.2 開源軟體永續經營": "4.2 Sustainable Operations",
    "4.2.1 開源人才培育與文化形塑": "4.2.1 Open-Source talent development and culture building",
    "4.2.2 社群動態追蹤與持續整合": "4.2.2 Community Activity Monitoring and Continuous Integration",
    "4.2.3 系統管理與升級策略建立": "4.2.3 Establishing System Management and Upgrade Strategies",
    "4.2.4 授權條款管理與程式碼再利用": "4.2.4 License Management and Code Reuse",
    "4.2.5 連結社群與公共程式平臺": "4.2.5 Connecting Communities and Public Code Platforms",
    "4.3 結語": "4.3 Conclusion",
    "附錄一 名詞解釋": "Appendix I: Terminology",
    "附錄二 常見問答 FAQ": "Appendix II: FAQ",
    "附錄三 參考資源": "Appendix III: Links",
    "附錄四 需求規劃自主檢核表": "Appendix IV: Requirements Planning Self-Assessment Checklist",
    "附錄五 授權合規評估檢核表": "Appendix V: License Compliance Assessment Checklist",
}


def slugify(text: str) -> str:
    text = text.lower()
    text = text.replace("’", "").replace("“", "").replace("”", "")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


EN_ANCHORS = {title: slugify(title) for _, title in EN_TOC}


def build_heading_anchor_map(en_text: str) -> tuple[dict[str, str], dict[str, str]]:
    heading_to_anchor: dict[str, str] = {}
    number_to_anchor: dict[str, str] = {}
    for line in en_text.splitlines():
        match = re.match(r"^(#{2,4})\s+(.+)$", line)
        if not match:
            continue
        title = line.lstrip("#").strip()
        if title in {"Document Revision History", "Table of Contents", "Notes"}:
            continue
        anchor = slugify(title)
        heading_to_anchor[title] = anchor
        num = re.match(r"^([1-4](?:\.\d+)+)", title)
        if num:
            number_to_anchor[num.group(1)] = anchor
    heading_to_anchor.update(EN_ANCHORS)
    return heading_to_anchor, number_to_anchor


def flatten_assets(markdowns: list[Path]) -> None:
    ASSETS.mkdir(exist_ok=True)
    from_pptx = ASSETS / "from-pptx"
    if from_pptx.exists():
        for lang in ["en", "zh-tw"]:
            media_dir = from_pptx / lang / "ppt" / "media"
            if not media_dir.exists():
                continue
            prefix = "en" if lang == "en" else "zh-tw"
            for src in media_dir.iterdir():
                if not src.is_file() or src.name.startswith("."):
                    continue
                shutil.copy2(src, ASSETS / f"{prefix}-{src.name}")

    for md in markdowns:
        text = md.read_text(encoding="utf-8")

        def replace_path(match: re.Match[str]) -> str:
            alt, path = match.group(1), match.group(2)
            src = Path(path)
            parts = src.parts
            if len(parts) >= 5 and parts[0] == "assets" and parts[1] == "from-pptx":
                lang = parts[2]
                prefix = "en" if lang == "en" else "zh-tw"
                return f"![{alt}](assets/{prefix}-{src.name})"
            return match.group(0)

        text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_path, text)
        md.write_text(text, encoding="utf-8")

    if from_pptx.exists():
        shutil.rmtree(from_pptx)

    readme = ASSETS / "README.md"
    readme.write_text(
        "# Assets\n\n"
        "Images in this folder are extracted from the source PPTX files and renamed with language prefixes.\n\n"
        "- `zh-tw-*`: extracted from `ZH_TW.pptx`\n"
        "- `en-*`: extracted from `EN.pptx`\n\n"
        "The Markdown manuals reference selected PNG/JPEG images directly from this single `assets/` folder. "
        "`*.wdp` files are JPEG-XR media preserved from the PPTX package.\n",
        encoding="utf-8",
    )


def is_note_definition(line: str) -> re.Match[str] | None:
    if line.startswith("|") or line.startswith("#") or line.startswith("!["):
        return None
    match = re.match(r"^(.+?)(\d{1,2})\s*[：:]\s*(.+)$", line)
    if not match:
        return None
    label = match.group(1).strip()
    if label.startswith(("Case Study", "Tier")):
        return None
    if re.match(r"^\d+(\.\d+)*$", label):
        return None
    return match


def extract_footnotes(text: str, lang: str) -> tuple[str, list[tuple[str, str, str]]]:
    lines = text.splitlines()
    out: list[str] = []
    notes: list[tuple[str, str, str]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        match = is_note_definition(line.strip())
        if match:
            label = match.group(1).strip()
            num = match.group(2)
            definition = match.group(3).strip()
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("http"):
                definition = f"{definition} {lines[i + 1].strip()}"
                i += 1
            notes.append((num, label, definition))
        else:
            out.append(line)
        i += 1

    seen: set[str] = set()
    unique: list[tuple[str, str, str]] = []
    for num, label, definition in notes:
        if num in seen:
            continue
        seen.add(num)
        unique.append((num, label, definition))
    return "\n".join(out), unique


def flexible_label_pattern(label: str) -> str:
    chunks = [re.escape(part) for part in re.split(r"\s+", label.strip()) if part]
    return r"\s*".join(chunks)


def replace_footnote_refs(text: str, notes: list[tuple[str, str, str]], lang: str) -> str:
    body = text
    for num, label, _ in notes:
        clean_label = label.strip()
        if not clean_label:
            continue
        pattern = flexible_label_pattern(clean_label) + rf"\s*{num}(?!\d)"
        body = re.sub(pattern, f"{clean_label}[^{num}]", body)

    manual_patterns = {
        "zh": {
            "6": [r"OSD）\s*6"],
            "7": [r"使用統計\s*7"],
            "22": [r"報告\s*22"],
            "23": [r"Open）\s*23", r"封閉》\s*23"],
            "26": [r"FLOSS-PSO\s*26"],
            "28": [r"公共程式標準\s*28"],
        },
        "en": {
            "6": [r"OSD\)\s*6"],
            "7": [r"November 2025\s*7"],
            "22": [r"Red Hat\s*22"],
            "23": [r"Closed[”\"]\s*23"],
            "26": [r"FLOSS-PSO\s*26"],
            "27": [r"NHS Digital\s*27"],
            "28": [r"Public Code Standard\s*28"],
        },
    }
    for num, patterns in manual_patterns[lang].items():
        for pattern in patterns:
            body = re.sub(pattern, lambda m, n=num: re.sub(r"\s*\d+$", "", m.group(0)) + f"[^{n}]", body)

    # Clean special cases where the generic substitution cannot preserve punctuation.
    body = body.replace("OSD）[^6]", "OSD）[^6]")
    body = body.replace("OSD)[^6]", "OSD)[^6]")
    body = body.replace("November 2025[^7]", "November 2025[^7]")
    return body


def append_footnotes(text: str, notes: list[tuple[str, str, str]], lang: str) -> str:
    text = re.sub(r"\n## (註解|Notes)\n(.|\n)*$", "", text).rstrip()
    if not notes:
        return text + "\n"
    heading = "註解" if lang == "zh" else "Notes"
    colon = "：" if lang == "zh" else ":"
    lines = [text, "", f"## {heading}", ""]
    for num, label, definition in sorted(notes, key=lambda item: int(item[0])):
        label = label.strip()
        definition = definition.strip()
        lines.append(f"[^{num}]: {label}{colon}{definition}")
    return "\n".join(lines).rstrip() + "\n"


def remove_existing_anchors(text: str) -> str:
    text = re.sub(r'<a id="[^"]+"></a>\n', "", text)
    return re.sub(r"^(#{1,6} .+?)\s+\{#[^}]+\}$", r"\1", text, flags=re.MULTILINE)


def add_heading_anchors(text: str, lang: str, heading_to_anchor: dict[str, str]) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^(#{2,4})\s+(.+?)(?:\s+\{#[^}]+\})?$", line)
        if not match or line in {"## 目錄", "## Table of Contents"}:
            lines.append(line)
            continue
        level = match.group(1)
        title = match.group(2).strip()
        english = title
        if lang == "zh":
            english = ZH_HEADING_TO_EN.get(title, title)
        anchor = heading_to_anchor.get(english, slugify(english))
        if anchor:
            lines.append(f"{level} {title} {{#{anchor}}}")
        else:
            lines.append(f"{level} {title}")
    return "\n".join(lines)


def replace_toc(text: str, lang: str, heading_to_anchor: dict[str, str]) -> str:
    toc = ZH_TOC if lang == "zh" else EN_TOC
    title = "## 目錄" if lang == "zh" else "## Table of Contents"
    toc_lines = [title, ""]
    for label, english in toc:
        indent = "  " if re.match(r"^[1-4]\.", label) else ""
        anchor = heading_to_anchor[english]
        toc_lines.append(f"{indent}- [{label}](#{anchor})")
    replacement = "\n".join(toc_lines)
    pattern = re.compile(rf"{re.escape(title)}\n\n(?:- .+\n|  - .+\n)+", re.MULTILINE)
    return pattern.sub(replacement + "\n", text, count=1)


def link_cross_refs(text: str, number_to_anchor: dict[str, str], lang: str) -> str:
    appendix = {
        "附錄四": "appendix-iv-requirements-planning-self-assessment-checklist",
        "附錄五": "appendix-v-license-compliance-assessment-checklist",
        "Appendix IV": "appendix-iv-requirements-planning-self-assessment-checklist",
        "Appendix V": "appendix-v-license-compliance-assessment-checklist",
    }
    out: list[str] = []
    in_toc = False
    for line in text.splitlines():
        if line in {"## 目錄", "## Table of Contents"}:
            in_toc = True
            out.append(line)
            continue
        if in_toc and line.startswith("## ") and line not in {"## 目錄", "## Table of Contents"}:
            in_toc = False
        if in_toc or line.startswith("#") or line.startswith("<a id=") or line.startswith("![") or line.startswith("[^"):
            out.append(line)
            continue

        def num_repl(match: re.Match[str]) -> str:
            num = match.group(1)
            anchor = number_to_anchor.get(num)
            if not anchor:
                return match.group(0)
            return f"[{num}](#{anchor})"

        line = re.sub(r"(?<!\[)(?<!#)\b([1-4]\.\d(?:\.\d+)?)\b(?!\]\()", num_repl, line)
        for label, anchor in appendix.items():
            line = re.sub(rf"(?<!\[){re.escape(label)}(?!\]\()", f"[{label}](#{anchor})", line)
        out.append(line)
    return "\n".join(out)


PROTECT_RE = re.compile(
    r"!\[[^\]]*\]\([^)]+\)|\[[^\]]+\]\([^)]+\)|\[\^\d+\]|`[^`]*`|https?://[^\s）)]+"
)


def protect_segments(line: str) -> tuple[str, list[str]]:
    protected: list[str] = []

    def repl(match: re.Match[str]) -> str:
        protected.append(match.group(0))
        return f"\uE000{len(protected) - 1}\uE001"

    return PROTECT_RE.sub(repl, line), protected


def restore_segments(line: str, protected: list[str]) -> str:
    for idx, value in enumerate(protected):
        line = line.replace(f"\uE000{idx}\uE001", value)
    return line


def normalize_zh_line(line: str) -> str:
    if line.startswith("|"):
        # Tables still need parenthesis normalization, but aggressive spacing can
        # easily break alignment; keep the transform conservative in table rows.
        table = True
    else:
        table = False
    work, protected = protect_segments(line)
    work = work.replace("(", "（").replace(")", "）")
    work = re.sub(r"\s+（", "（", work)
    work = re.sub(r"）\s+", "）", work)
    work = re.sub(r"（\s+", "（", work)
    work = re.sub(r"\s+）", "）", work)
    if not table:
        work = re.sub(r"([\u4e00-\u9fff])([A-Za-z0-9][A-Za-z0-9./+_-]*)", r"\1 \2", work)
        work = re.sub(r"([A-Za-z0-9][A-Za-z0-9./+_-]*)([\u4e00-\u9fff])", r"\1 \2", work)
        work = re.sub(r"(\[\^\d+\])(?=[\u4e00-\u9fff])", r"\1 ", work)
        work = re.sub(r"\s{2,}", " ", work)
    return restore_segments(work, protected)


def normalize_zh_spacing(text: str) -> str:
    return "\n".join(normalize_zh_line(line) for line in text.splitlines())


def fix_known_text_issues(text: str, lang: str) -> str:
    if lang == "en":
        text = text.replace(
            "Against this backdrop, t### 4.3 Conclusion\n\nThe adoption",
            "Against this backdrop, the adoption",
        )
        text = text.replace("Introduction to Open-source Software\n\n", "")
        text = text.replace(
            "This section includes 3 examples",
            "This section includes three examples",
        )
    else:
        text = text.replace("1.2 國際趨勢與應用", "1.2 開源軟體國際趨勢與應用")
    return text


def process_markdown(path: Path, lang: str, heading_to_anchor: dict[str, str], number_to_anchor: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    text = remove_existing_anchors(text)
    text = fix_known_text_issues(text, lang)
    text, notes = extract_footnotes(text, lang)
    text = replace_footnote_refs(text, notes, lang)
    text = replace_toc(text, lang, heading_to_anchor)
    text = link_cross_refs(text, number_to_anchor, lang)
    text = add_heading_anchors(text, lang, heading_to_anchor)
    text = append_footnotes(text, notes, lang)
    if lang == "zh":
        text = normalize_zh_spacing(text)
    text = re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    zh = ROOT / "ZH_TW.md"
    en = ROOT / "EN.md"
    flatten_assets([zh, en])
    en_text = en.read_text(encoding="utf-8")
    heading_to_anchor, number_to_anchor = build_heading_anchor_map(en_text)
    process_markdown(en, "en", heading_to_anchor, number_to_anchor)
    process_markdown(zh, "zh", heading_to_anchor, number_to_anchor)


if __name__ == "__main__":
    main()
