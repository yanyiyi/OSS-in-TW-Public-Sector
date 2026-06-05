---
name: markitdown-bilingual-manual
description: Convert Microsoft MarkItDown-generated Markdown from PPTX/PDF source material into polished bilingual Traditional Chinese and English Markdown manuals with matching line counts, aligned sections, linked table of contents, extracted PDF/PPT visuals, accessible image syntax, footnotes, and PMPC-style formatting. Use when working on this PMPC playbook/manual workflow, cleaning slide-like Markdown into complete article form, synchronizing EN.md and ZH_TW.md, or updating bilingual Markdown from revised PPTX/PDF sources.
---

# MarkItDown Bilingual Manual

## Purpose

Use this skill to turn rough Markdown exported by Microsoft MarkItDown from presentation-style sources into a complete bilingual manual. The result must read like a handbook, not slides, and `EN.md` and `ZH_TW.md` must remain line-by-line comparable.

## Source Priority

1. Treat the latest user-provided PPTX/PDF files as authoritative for content and visuals.
2. Use PPTX text extraction to compare old and new versions when identifying text changes.
3. Use PDF rendering for final images because it reflects the publication layout and language shown to readers.
4. If a user names PDF page numbers, confirm whether they mean the printed page number at the bottom of the page or the PDF file index. Prefer printed page numbers when the user says "頁碼下方的編號".
5. For Traditional Chinese images, find the corresponding section or visual in the Chinese PDF. Do not reuse English screenshots unless the Chinese source genuinely has no equivalent and the user accepts that fallback.

## Manualization Workflow

1. Inventory the workspace:
   - Locate current `EN.md`, `ZH_TW.md`, source PPTX/PDF files, `assets/`, and helper scripts.
   - Check `git status --short` before editing and preserve unrelated user changes.
2. Compare revised sources:
   - Extract text from old and new PPTX/PDF sources.
   - Identify changed sections, revision-history rows, appendix links, captions, and visual-only changes.
   - Keep changes scoped to the source differences unless the user requests broader cleanup.
3. Convert slide fragments into manual prose:
   - Merge slide bullets into coherent paragraphs where they are explanatory text.
   - Keep tables as Markdown tables when they are better as searchable text.
   - Remove presentation-only artifacts such as repeated page headers, footers, page numbers, visual labels used only for slide navigation, and duplicated fragments.
   - Preserve chapter/section hierarchy and make the document feel like a complete handbook.
4. Synchronize bilingual content:
   - Every logical block in `ZH_TW.md` must correspond to the same logical block in `EN.md`.
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
2. Use the correct language:
   - English Markdown should reference images cropped from the English PDF.
   - Traditional Chinese Markdown should reference corresponding images cropped from the Chinese PDF.
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

## Bilingual Alignment Checklist

Before finishing, verify:

- `wc -l EN.md ZH_TW.md` reports the same line count.
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
