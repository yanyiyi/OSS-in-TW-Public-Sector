from __future__ import annotations

import re
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


SKIP_MEDIA = {
    "hdphoto1.wdp",
    "image1.png",
    "image2.png",
    "image3.svg",
    "image4.png",
    "image5.png",
}


ZH_IMAGE_ALTS = {
    8: {"image6.png": "緒論插圖"},
    13: {"image8.png": "大教堂模式示意圖", "image7.jpeg": "市集模式示意圖"},
    16: {"image9.png": "openDesk 功能示意圖"},
    19: {"image10.png": "Federal Source Code Policy 備忘錄截圖"},
    25: {"image11.png": "開源軟體與公共程式關係示意圖"},
    33: {"image22.png": "開放優先安全治理示意圖"},
    41: {"image23.png": "FLOSS-PSO 公部門 OSPO 全球網絡地圖"},
    52: {"image24.png": "X-Road 架構示意圖"},
    58: {"image25.png": "公共程式維護等級示意圖"},
    64: {"image26.png": "Grafana 監控儀表板截圖"},
    66: {"image27.png": "資安管理關鍵項目示意圖"},
    69: {"image28.png": "文件管理與交付矩陣", "image29.png": "文件重要性圖例"},
}


EN_IMAGE_ALTS = {
    10: {"image6.png": "Preface illustration"},
    16: {"image8.png": "Cathedral model illustration", "image7.jpeg": "Bazaar model illustration"},
    20: {"image9.png": "openDesk feature overview"},
    24: {"image10.png": "Federal Source Code Policy memorandum screenshot"},
    58: {"image26.png": "FLOSS-PSO public-sector OSPO global map"},
    74: {"image27.png": "X-Road architecture diagram"},
    84: {"image28.png": "Public code maintenance tier diagram"},
    93: {"image29.png": "Grafana monitoring dashboard screenshot"},
    100: {"image30.png": "Documentation management and delivery matrix"},
}


ZH_CHAPTERS = {
    "1": "第一章 開源軟體介紹",
    "2": "第二章 開源軟體應用評估",
    "3": "第三章 開源軟體導入方法",
    "4": "第四章 開源軟體維護與營運",
}


EN_CHAPTERS = {
    "1": "Chapter 1: Introduction to Open-Source Software",
    "2": "Chapter 2: Open-Source Software Application Evaluation",
    "3": "Chapter 3: Open-Source Software Implementation",
    "4": "Chapter 4: Open-Source Software Maintenance and Operations",
}


ZH_TOC = [
    ("緒論", 0),
    ("第一章 開源軟體介紹", 0),
    ("1.1 開源軟體發展背景", 1),
    ("1.2 開源軟體國際趨勢與應用", 1),
    ("1.3 開源軟體基本概念與授權條款類型", 1),
    ("1.4 開源軟體與公共程式", 1),
    ("第二章 開源軟體應用評估", 0),
    ("2.1 使用開源軟體及專有軟體差異說明", 1),
    ("2.2 開源軟體使用效益與風險評估", 1),
    ("2.3 開源軟體導入模式", 1),
    ("2.4 開源軟體治理制度", 1),
    ("第三章 開源軟體導入方法", 0),
    ("3.1 軟體開發流程：需求與設計開源注意事項", 1),
    ("3.2 軟體開發流程：開發與測試開源注意事項", 1),
    ("3.3 軟體開發流程：上線與驗收開源注意事項", 1),
    ("3.4 將開發成果開源釋出", 1),
    ("第四章 開源軟體維護與營運", 0),
    ("4.1 開源軟體維運", 1),
    ("4.2 開源軟體永續經營", 1),
    ("4.3 結語", 1),
    ("附錄一 名詞解釋", 0),
    ("附錄二 常見問答 FAQ", 0),
    ("附錄三 參考資源", 0),
    ("附錄四 需求規劃自主檢核表", 0),
    ("附錄五 授權合規評估檢核表", 0),
]


EN_TOC = [
    ("Introduction", 0),
    ("Chapter 1: Introduction to Open-Source Software", 0),
    ("1.1 How it started", 1),
    ("1.2 International Trends and Applications", 1),
    ("1.3 Basic Concept and Licensing Agreement Types of Open-Source Software", 1),
    ("1.4 Open-Source Software and Public Code", 1),
    ("Chapter 2: Open-Source Software Application Evaluation", 0),
    ("2.1 Difference Between Using Open-Source and Proprietary Software", 1),
    ("2.2 Open-Source Software Benefits and Risks Analysis", 1),
    ("2.3 Open-Source Software Implementation Model", 1),
    ("2.4 Open-Source Software Governance System", 1),
    ("Chapter 3: Open-Source Software Implementation", 0),
    ("3.1 Software Development Process: Needs and Cautions when Designing Open-Source Software", 1),
    ("3.2 Software Development Process: Considerations for Open Source During Development and Testing", 1),
    ("3.3 Software Development Process: Open-Source Considerations for Go-Live and Acceptance", 1),
    ("3.4 Releasing Development Outcomes as Open Source", 1),
    ("Chapter 4: Open-Source Software Maintenance and Operations", 0),
    ("4.1 Open-Source Software Operations and Maintenance", 1),
    ("4.2 Sustainable Operations", 1),
    ("4.3 Conclusion", 1),
    ("Appendix I: Terminology", 0),
    ("Appendix II: FAQ", 0),
    ("Appendix III: Links", 0),
    ("Appendix IV: Requirements Planning Self-Assessment Checklist", 0),
    ("Appendix V: License Compliance Assessment Checklist", 0),
]


ZH_EXACT_HEADINGS = {
    "緒論": (2, "緒論"),
    "緣起": (3, "緣起"),
    "第一章 開源軟體介紹": (2, "第一章 開源軟體介紹"),
    "第二章 開源軟體應用評估": (2, "第二章 開源軟體應用評估"),
    "第三章 開源軟體導入方法": (2, "第三章 開源軟體導入方法"),
    "第四章 開源軟體維護與營運": (2, "第四章 開源軟體維護與營運"),
    "附錄一 名詞解釋": (2, "附錄一 名詞解釋"),
    "附錄二 常見問答FAQ": (2, "附錄二 常見問答 FAQ"),
    "附錄三 參考資源": (2, "附錄三 參考資源"),
    "附錄四 需求規劃自主檢核表": (2, "附錄四 需求規劃自主檢核表"),
    "附錄五 授權合規評估檢核表": (2, "附錄五 授權合規評估檢核表"),
}


EN_EXACT_HEADINGS = {
    "Introduction": (2, "Introduction"),
    "Origin": (3, "Origin"),
    "Chapter 1: Introduction to Open-Source Software": (2, "Chapter 1: Introduction to Open-Source Software"),
    "Chapter 2: Open-Source Software Application Evaluation": (2, "Chapter 2: Open-Source Software Application Evaluation"),
    "Chapter 3: Open-source Software Implementation": (2, "Chapter 3: Open-Source Software Implementation"),
    "Chapter 3: Open-Source Software Implementation": (2, "Chapter 3: Open-Source Software Implementation"),
    "Chapter 4: Open-source Software Maintenance and Operations": (2, "Chapter 4: Open-Source Software Maintenance and Operations"),
    "Chapter 4: Open-Source Software Maintenance and Operations": (2, "Chapter 4: Open-Source Software Maintenance and Operations"),
    "Appendix I: Terminology": (2, "Appendix I: Terminology"),
    "Appendix II: FAQ": (2, "Appendix II: FAQ"),
    "Appendix III: Links": (2, "Appendix III: Links"),
    "Appendix IV: Requirements Planning Self-Assessment Checklist": (2, "Appendix IV: Requirements Planning Self-Assessment Checklist"),
    "Appendix V: License Compliance Assessment Checklist": (2, "Appendix V: License Compliance Assessment Checklist"),
}


ZH_SKIP_EXACT = {
    "Public Sector",
    "Open-Source Software Playbook",
    "公部門開源軟體應用參考手冊",
    "公部門開源軟體與公共程式應用參考手冊",
    "文件修訂歷史",
    "目錄",
    "Preface",
    "Chapter 1：",
    "Chapter 2：",
    "Chapter 3：",
    "Chapter 4：",
    "Appendix",
    "附錄",
    "章節大綱",
    "Summary",
    "本節建議各機關",
    "本章建議各機關",
    "資訊專案承辦人員",
    "資訊規劃人員",
    "IT維運人員",
    "重點閱讀",
    "檢核項目",
    "Digital Public Goods Registry",
}


EN_SKIP_EXACT = {
    "Public Sector",
    "Open-Source Software Playbook",
    "公部門開源軟體應用參考手冊",
    "Document Revision History",
    "TABLE OF CONTENT",
    "Preface",
    "Chapter 1：",
    "Chapter 1：Introduction to",
    "Chapter 2：",
    "Chapter 2: Open-Source Software",
    "Chapter 3：",
    "Chapter 4：",
    "Open-Source Software",
    "Application Evaluation",
    "Open-source Software Implementation",
    "Open-source Software Maintenance and Operations",
    "Maintenance and Operation of",
    "Appendix",
    "Summary",
    "This chapter is recommended as priority reading for personnel responsible for information projects at all agencies.",
    "Digital Public Goods Registry",
}


EDIT_PATTERNS = [
    r"^調整",
    r"^避免",
    r"^對齊",
    r"^縮小",
    r"^移除",
    r"^附圖",
    r"^改黑色$",
    r"^次頁",
    r"^將第",
    r"^將所有",
    r"^並將",
    r"^討論!",
    r"^3 大小",
    r"^12>10$",
    r"CASE 背景",
    r"壓到頁碼",
    r"壓頁碼",
    r"避免壓",
    r"文字排版",
    r"表格底部",
    r"框框不要",
    r"不要過於貼近",
]


def slide_media_map(pptx_path: Path) -> dict[int, list[str]]:
    mapping: dict[int, list[str]] = {}
    with ZipFile(pptx_path) as zf:
        for name in zf.namelist():
            match = re.fullmatch(r"ppt/slides/slide(\d+)\.xml", name)
            if not match:
                continue
            slide_no = int(match.group(1))
            rel_name = f"ppt/slides/_rels/slide{slide_no}.xml.rels"
            if rel_name not in zf.namelist():
                continue
            root = ET.fromstring(zf.read(rel_name))
            media: list[str] = []
            for rel in root:
                target = rel.attrib.get("Target", "")
                if "../media/" in target:
                    media.append(Path(target).name)
            mapping[slide_no] = media
    return mapping


def split_slides(source: str) -> list[tuple[int, list[str]]]:
    slides: list[tuple[int, list[str]]] = []
    current_no: int | None = None
    current: list[str] = []
    for raw_line in source.splitlines():
        match = re.fullmatch(r"<!-- Slide number: (\d+) -->", raw_line.strip())
        if match:
            if current_no is not None:
                slides.append((current_no, current))
            current_no = int(match.group(1))
            current = []
        else:
            current.append(raw_line.rstrip())
    if current_no is not None:
        slides.append((current_no, current))
    return slides


def is_edit_note(line: str) -> bool:
    return any(re.search(pattern, line) for pattern in EDIT_PATTERNS)


def is_old_image(line: str) -> bool:
    return bool(re.fullmatch(r"!\[[^\]]*\]\([^)]+\)", line.strip()))


def normalize_line(line: str) -> str:
    line = line.replace("\x0b", "<br>")
    line = re.sub(r"\s+", " ", line).strip()
    line = line.replace("：//", "://")
    line = line.replace("（ ", "（").replace(" ）", "）")
    line = line.replace(" ,", ",")
    return line


def zh_heading(line: str) -> tuple[int, str] | None:
    if line in ZH_EXACT_HEADINGS:
        return ZH_EXACT_HEADINGS[line]
    appendix = re.match(r"^(附錄[一二三四五])\s+(.+)$", line)
    if appendix:
        title = f"{appendix.group(1)} {appendix.group(2).strip()}"
        title = title.replace("常見問答FAQ", "常見問答 FAQ")
        return (2, title)
    subsection = re.match(r"^([1-4]\.\d\.\d+)\s*(.+)$", line)
    if subsection:
        return (4, f"{subsection.group(1)} {subsection.group(2).strip()}")
    section = re.match(r"^([1-4]\.\d)\s*(.+)$", line)
    if section:
        return (3, f"{section.group(1)} {section.group(2).strip()}")
    return None


def en_heading(line: str) -> tuple[int, str] | None:
    line = line.replace("Open-source", "Open-Source")
    if line in EN_EXACT_HEADINGS:
        return EN_EXACT_HEADINGS[line]
    appendix = re.match(r"^(Appendix [IVX]+):?\s+(.+)$", line)
    if appendix:
        return (2, f"{appendix.group(1)}: {appendix.group(2).strip()}")
    subsection = re.match(r"^([1-4]\.\d\.\d+)\s*(.+)$", line)
    if subsection:
        return (4, f"{subsection.group(1)} {subsection.group(2).strip()}")
    section = re.match(r"^([1-4]\.\d)\s*(.+)$", line)
    if section:
        return (3, f"{section.group(1)} {section.group(2).strip()}")
    return None


def emit_heading(
    out: list[str],
    level: int,
    title: str,
    emitted: set[str],
) -> None:
    title = re.sub(r"\s+", " ", title.strip())
    if title in emitted:
        return
    if out and out[-1] != "":
        out.append("")
    out.append(f"{'#' * level} {title}")
    out.append("")
    emitted.add(title)


def ensure_chapter(
    out: list[str],
    title: str,
    emitted: set[str],
) -> None:
    if title not in emitted:
        emit_heading(out, 2, title, emitted)


def insert_images(
    out: list[str],
    slide_no: int,
    media_names: list[str],
    image_alts: dict[int, dict[str, str]],
    asset_dir: str,
) -> None:
    slide_alts = image_alts.get(slide_no, {})
    usable = [name for name in media_names if name not in SKIP_MEDIA and name in slide_alts]
    if not usable:
        return
    if out and out[-1] != "":
        out.append("")
    for name in usable:
        out.append(f"![{slide_alts[name]}]({asset_dir}/{name})")
        out.append("")


def front_matter(lang: str) -> list[str]:
    if lang == "zh":
        toc = ["## 目錄", ""]
        for text, depth in ZH_TOC:
            indent = "  " * depth
            toc.append(f"{indent}- {text}")
        return [
            "# 公部門開源軟體應用參考手冊",
            "",
            "Public Sector Open-Source Software Playbook",
            "",
            "## 文件修訂歷史",
            "",
            "| 版本 | 變更內容摘要 | 原稿頁數 | 發布日期 |",
            "| --- | --- | --- | --- |",
            "| V1.0 | 初版制定 | 88 | 114.10.15 |",
            "| V1.1 | 初版修改（完稿第一版） | 97 | 114.12.01 |",
            "| V2.0 | 完稿第二版 | 97 | 114.12.05 |",
            "| V2.1 | 完稿修訂版 | 88 | 114.12.15 |",
            "| V2.2 | 完稿第三版 | 89 | 114.12.24 |",
            "",
            *toc,
            "",
        ]
    toc = ["## Table of Contents", ""]
    for text, depth in EN_TOC:
        indent = "  " * depth
        toc.append(f"{indent}- {text}")
    return [
        "# Public Sector Open-Source Software Playbook",
        "",
        "公部門開源軟體應用參考手冊",
        "",
        "## Document Revision History",
        "",
        "| Version | Summary of Changes | Source Page Count | Release Date |",
        "| --- | --- | --- | --- |",
        "| V1.0 | Initial release | 127 | 114.12.24 |",
        "",
        *toc,
        "",
    ]


def should_skip_line(line: str, lang: str) -> bool:
    if not line:
        return False
    skip_exact = ZH_SKIP_EXACT if lang == "zh" else EN_SKIP_EXACT
    if line in skip_exact:
        return True
    if re.fullmatch(r"\d+", line):
        return True
    if re.fullmatch(r"0[1-4]", line):
        return True
    if line.startswith("<!--") or line == "### Notes:":
        return True
    if is_edit_note(line):
        return True
    if is_old_image(line):
        return True
    if lang == "zh":
        if re.fullmatch(r"第[一二三四]章", line):
            return True
        if line in {"開源軟體介紹", "開源軟體應用評估", "開源軟體導入方法", "開源軟體維護與營運"}:
            return True
    else:
        if line in {"Introduction to", "Open-Source Software", "Open-source Software"}:
            return True
        if line.startswith("This section includes") and "3 examples" in line:
            return False
    return False


def clean_manual(
    source_file: str,
    pptx_file: str,
    lang: str,
    image_alts: dict[int, dict[str, str]],
    asset_dir: str,
) -> str:
    source = (ROOT / source_file).read_text(encoding="utf-8")
    slides = split_slides(source)
    media_by_slide = slide_media_map(ROOT / pptx_file)
    out = front_matter(lang)
    emitted_headings: set[str] = set()
    last_blank = True

    heading_fn = zh_heading if lang == "zh" else en_heading
    chapters = ZH_CHAPTERS if lang == "zh" else EN_CHAPTERS

    for slide_no, lines in slides:
        if slide_no <= 6:
            continue
        inserted_images = False
        for raw_line in lines:
            normalized = normalize_line(raw_line)
            if is_old_image(normalized) and not inserted_images:
                insert_images(out, slide_no, media_by_slide.get(slide_no, []), image_alts, asset_dir)
                inserted_images = True
                last_blank = bool(out and out[-1] == "")
                continue
            if should_skip_line(normalized, lang):
                continue
            heading = heading_fn(normalized)
            if heading:
                text = heading[1]
                section_match = re.match(r"^([1-4])\.", text)
                if section_match:
                    ensure_chapter(out, chapters[section_match.group(1)], emitted_headings)
                emit_heading(out, heading[0], text, emitted_headings)
                last_blank = True
                continue
            if normalized == "":
                if not last_blank:
                    out.append("")
                    last_blank = True
                continue
            out.append(normalized)
            last_blank = False
        if not inserted_images:
            insert_images(out, slide_no, media_by_slide.get(slide_no, []), image_alts, asset_dir)
        if out and out[-1] != "":
            out.append("")
            last_blank = True

    text = "\n".join(out).strip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def main() -> None:
    conversions = [
        ("ZH_TW.md", "ZH_TW.pptx", "zh", ZH_IMAGE_ALTS, "assets/from-pptx/zh-tw/ppt/media"),
        ("EN.md", "EN.pptx", "en", EN_IMAGE_ALTS, "assets/from-pptx/en/ppt/media"),
    ]
    for source_file, pptx_file, lang, alts, asset_dir in conversions:
        manual = clean_manual(source_file, pptx_file, lang, alts, asset_dir)
        (ROOT / source_file).write_text(manual, encoding="utf-8")


if __name__ == "__main__":
    main()
