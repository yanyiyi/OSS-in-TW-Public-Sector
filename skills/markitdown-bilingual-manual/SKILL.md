---
name: markitdown-bilingual-manual
description: Convert Microsoft MarkItDown-generated Markdown from PPTX/PDF source material into polished external-facing Markdown manuals, including bilingual Traditional Chinese and English versions when present. Use when cleaning slide-like Markdown into a complete article/manual, removing presentation-only marks, comparing multiple source versions, pairing corresponding language files with flexible filenames, synchronizing bilingual line structure, extracting visuals from PPTX and PDF, adding accessible image syntax, rebuilding notes/footnotes, and validating links, anchors, images, and line alignment.
---

# MarkItDown Bilingual Manual

## Purpose

Use this skill to turn rough Markdown exported by Microsoft MarkItDown from PPTX/PDF presentation-style sources into a complete Markdown manual for external publication. The result must read like a handbook or article, not slides. When two language versions exist, keep them structurally comparable line by line.

中文速覽：這個 Skill 是給「簡報或 PDF 經 Microsoft MarkItDown 轉成 Markdown 後」的整理工作使用。它的重點不是單純轉檔，而是把簡報痕跡清掉、整理成可對外發布的單一 Markdown 文件；如果有中英文兩版，還要做段落、圖片、註解與行號對應。

It is fine if files are not named exactly `EN.md` and `ZH_TW.md`. Those names are convenient examples only. Infer language pairing from filenames, directory structure, document title, language content, user instructions, or source-version naming.

中文註解：檔名有清楚標示語言會更好處理，例如 `EN.md`、`ZH_TW.md`、`manual-en.md`、`manual-zhtw.md`，但 Skill 沒有寫死成只能處理這兩個檔名。

## What This Skill Helps Do

- Turn MarkItDown output into a complete article/manual with coherent headings, paragraphs, tables, notes, and images.
- Remove presentation-only marks such as slide page labels, repeated headers/footers, decorative separators, and fragmented bullet leftovers.
- Compare multiple PPTX/PDF/Markdown versions and apply only meaningful changes.
- Pair language versions even when filenames vary.
- Extract images from PPTX when useful and crop final publication visuals from PDF when layout fidelity matters.
- Rebuild references, notes, table-of-contents links, cross-references, and accessible image syntax.

中文註解：簡單說，它可以協助「從簡報式 Markdown 草稿」整理成「可給外部讀者閱讀的一份 Markdown 手冊」。若來源有多版，還會幫忙比對差異；若圖在 PPTX 解析不完整，也要從 PDF 截圖補齊。

## Source Priority

1. Treat the latest user-provided PPTX/PDF/Markdown files as authoritative for content and visuals.
2. Use MarkItDown-generated Markdown as the starting draft, not as the final structure.
3. Use PPTX text extraction to compare old and new versions when identifying text changes.
4. Use PDF rendering for final images because it reflects the publication layout and language shown to readers.
5. Extract images from PPTX when the embedded image is cleaner or when PDF cropping loses fidelity; prefer PDF screenshots when the user asks for page-based visuals.
6. If a user names PDF page numbers, confirm whether they mean the printed page number at the bottom of the page or the PDF file index. Prefer printed page numbers when the user says "頁碼下方的編號".
7. For Traditional Chinese images, find the corresponding section or visual in the Chinese PDF. Do not reuse English screenshots unless the Chinese source genuinely has no equivalent and the user accepts that fallback.

中文註解：MarkItDown 很適合提供初稿，但它常會保留簡報頁眉、頁碼、註解碎片與不完整圖片。真正整理時，應同時回頭查 PPTX/PDF。

## File Pairing And Naming

Do not require fixed filenames.

- Accept common names such as `EN.md`, `ZH_TW.md`, `en.md`, `zh.md`, `zhtw.md`, `manual-en.md`, `manual-zh-tw.md`, or user-provided names.
- Pair files by language markers in the filename first, then by title, source version, section structure, and content language.
- If a project has more than two languages, apply the same structure-pairing process across all requested languages.
- If there is only one Markdown output, still perform manualization, image extraction, note cleanup, link validation, and presentation-artifact removal.
- When output files are renamed for clarity, update image paths, cross-references, and any scripts that assume old filenames.

中文註解：檔名「處理好」會提升成功率，但 Skill 應該寬鬆。核心是判斷哪些檔案彼此對應、哪一份是新版、哪一份是目標輸出，而不是只認固定檔名。

## Manualization Workflow

1. Inventory the workspace:
   - Locate current Markdown outputs, source PPTX/PDF files, `assets/`, and helper scripts. In this PMPC repo, `EN.md` and `ZH_TW.md` are examples, not universal requirements.
   - Check `git status --short` before editing and preserve unrelated user changes.
2. Compare revised sources:
   - Extract text from old and new PPTX/PDF sources.
   - Identify changed sections, revision-history rows, appendix links, captions, and visual-only changes.
   - Compare generated Markdown against source PPTX/PDF when MarkItDown output looks incomplete or slide-like.
   - Keep changes scoped to the source differences unless the user requests broader cleanup.
3. Convert slide fragments into manual prose:
   - Merge slide bullets into coherent paragraphs where they are explanatory text.
   - Keep tables as Markdown tables when they are better as searchable text.
   - Remove presentation-only artifacts such as repeated page headers, footers, page numbers, visual labels used only for slide navigation, and duplicated fragments.
   - Remove or rewrite slide-only labels that do not help external readers understand the manual.
   - Preserve chapter/section hierarchy and make the document feel like a complete handbook.
4. Synchronize bilingual content:
   - When bilingual files exist, every logical block in one language should correspond to the same logical block in the other language.
   - Headings, paragraphs, blank lines, tables, lists, image lines, captions, footnotes, and appendix entries must stay in the same order.
   - If adding a line to one language, add the corresponding line to the other language.
   - Do not leave one-sided blank lines as padding unless the user explicitly asks; prefer aligned equivalent content.
5. Run or update the alignment helper:
   - In this repo, use `scripts/align_bilingual_markdown_lines.py` when block-level reflow is needed.
   - The script should recognize heading anchors written as `{#anchor}` or trailing `<span id="anchor"></span>`.
   - After running it, immediately inspect the diff to ensure content was not reordered incorrectly.

## Heading And Link Rules

Use a linked table of contents at the top of each Markdown file.

For this PMPC project:

- Use English anchor IDs for both languages, so cross-language comparison is stable.
- Avoid standalone `<a id="..."></a>` lines.
- Prefer renderer-compatible heading anchors on the heading line. Current files use:

```markdown
## Chapter 1: Introduction to Open-Source Software <span id="chapter-1-introduction-to-open-source-software"></span>
## 第一章 開源軟體介紹 <span id="chapter-1-introduction-to-open-source-software"></span>
```

For internal references, link to the English anchor:

```markdown
See Section [1.1](#1-1-how-it-started).
可參考 [1.1 小節](#1-1-how-it-started)。
```

Validate all `#anchor` links against heading anchors before finishing.

中文註解：目錄連結與交互參照是對外文件很容易壞掉的地方。整理完之後一定要實際檢查 `#anchor` 是否存在。

## Footnotes And Notes

MarkItDown and PPTX exports often turn slide footnotes into floating text. Rebuild these as Markdown footnotes.

- Convert superscript-style references into `[^n]`.
- Place all notes in a final notes section such as `## Notes` / `## 註解`.
- Keep footnote numbers and ordering aligned between English and Traditional Chinese.
- If a slide note explains an inline term, connect the inline marker to the note instead of leaving a detached paragraph.
- Preserve URLs in notes and appendix resources, normalizing obvious full-width colon issues only when it is safe.

## Traditional Chinese Style

Apply Taiwan academic/manual formatting conventions:

- Insert half-width spaces between Chinese full-width characters and English words, abbreviations, numbers, or Roman numerals.
- Use full-width parentheses `（）` in Traditional Chinese prose.
- Do not add extra spaces before or after full-width parentheses.
- Prefer Traditional Chinese terminology and Taiwan usage.
- Keep technical abbreviations readable, for example `開源 AI 定義（OSAID）`, `Open-Source Initiative（OSI）`, and `ISO／IEC 5230`.
- Preserve Markdown syntax even when spacing rules would otherwise suggest adding spaces.

## Image Extraction

Images are part of the manual, not decorative leftovers.

1. Identify visual assets:
   - Review the source PPTX/PDF for diagrams, screenshots, icons, process charts, comparison graphics, and small explanatory illustrations.
   - Do not assume only large figures matter; small in-slide diagrams may be important.
   - Compare PPTX-extracted images with PDF-rendered visuals; use the version that best reflects the final publication.
2. Use the correct language:
   - English Markdown should reference images cropped from the English PDF.
   - Traditional Chinese Markdown should reference corresponding images cropped from the Chinese PDF.
   - For other language pairs, crop from the PDF/source matching that language.
3. Use printed page numbers:
   - When the user gives page numbers, map them to the printed page number shown at the bottom of the page.
   - If the PDF file index differs, document the mapping during work and crop the rendered page that contains the printed number.
4. Crop intentionally:
   - Crop the visual object, not the whole slide/page, unless the full page is the visual.
   - Exclude page headers, footers, and unrelated surrounding prose.
   - Keep enough internal title/labels for the image to be understandable.
5. Preserve asset structure:
   - Store images directly under `assets/`.
   - Do not introduce `from-pptx` or nested extraction directories in Markdown paths.
   - Reuse existing image numbers when it clearly preserves the document's numbering; otherwise append new numbers without renumbering existing files.
6. Use accessible Markdown syntax:

```markdown
![Accessible description of the image content](assets/en-image12.png "Contextual image title")
![方便無障礙理解的圖片內容描述](assets/zh-tw-image12.png "可由上下文推敲的圖片標題")
```

Alt text should describe the information conveyed by the image, not merely say "screenshot" or "diagram".

中文註解：圖片不是為了好看而已。若圖表提供了文字以外的資訊，就要放進 Markdown，並用 alt/title 讓讀者與輔助工具能理解它。

## Bilingual Alignment Checklist

When bilingual output is required, verify:

- The paired Markdown files report the same line count. In this repo, use `wc -l EN.md ZH_TW.md`.
- No blank-line mismatch exists between the two files.
- Corresponding lines have the same structural class: heading, paragraph, table row, list item, image, footnote, URL, or blank.
- Image counts match between languages.
- Every English image has a Chinese counterpart at the same line number.
- Footnote counts and references match.
- Appendix resource additions appear in both languages.
- Local table-of-contents and cross-reference links resolve.

Useful validation patterns:

```bash
wc -l EN.md ZH_TW.md
rg -n "\\{#|<a id=|<a name=|from-pptx" EN.md ZH_TW.md
git diff --check
```

Use a small script when needed to classify lines and detect structural mismatches; do not rely only on visual inspection for line alignment.

中文註解：如果檔名不是 `EN.md` / `ZH_TW.md`，把上述指令中的檔名換成實際成對檔案即可。重點是同行數、同結構、同位置圖片。

## Single-File Output Checklist

When only one outward-facing Markdown file is requested, still verify:

- It reads continuously as an article/manual.
- Slide-only marks, repeated headers/footers, and page numbers are removed.
- The table of contents links to actual headings.
- Images are stored under a clean `assets/` path and use accessible alt/title syntax.
- Footnotes, appendix links, and cross-references resolve.
- Source-version changes were compared against the latest PPTX/PDF, not just copied from the generated Markdown.

中文註解：即使沒有中英文對齊需求，也不能只把 MarkItDown 結果丟出來；仍要處理成可閱讀、可連結、可維護的 Markdown。

## Quality Bar

The final Markdown should:

- Read as a complete manual, not a slide transcript.
- Preserve user-edited sections unless the task explicitly asks to rewrite them.
- Keep bilingual content semantically corresponding, even when version numbers or source-page counts differ by language.
- Prefer searchable Markdown tables for tabular knowledge and use images as supporting visuals.
- Use clear alt/title text for every image.
- Keep links stable and renderer-compatible.
- Leave unrelated files and untracked user-provided sources alone unless the user asks to stage, commit, or delete them.

## Final Reporting

When done, summarize:

- Which Markdown files changed.
- Which source versions were compared.
- Which visual pages or sections were cropped.
- Whether line counts, images, anchors, and `git diff --check` passed.
- Any files left untracked, especially newly provided PPTX/PDF sources.
