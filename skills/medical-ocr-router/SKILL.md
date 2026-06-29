---
name: medical-ocr-router
description: Route medical OCR tasks for screenshots, scanned PDFs, textbook pages, lecture slides, and question-bank images. Use when OCR needs to preserve biomedical notation, formulas, subscripts, superscripts, ions, tables, layout, question options, or Markdown structure, especially for Chinese medical study material.
---

# Medical OCR Router

Use this skill when OCR output must remain medically meaningful. Do not treat medical OCR as plain text extraction when the source may contain biomedical notation, formulas, table structure, question options, figure labels, or mixed textbook layout.

## Workflow

1. Inspect the input before OCR.
2. Classify the input as PDF page, screenshot, textbook page, slide, question bank, table, formula-heavy region, or mixed layout.
3. Prefer embedded PDF text only when it is complete and preserves notation.
4. For scanned PDFs, render pages at 300-400 DPI before OCR.
5. Route regions by content type:
   - normal paragraphs: standard OCR
   - formulas, ions, gases, equations, subscripts, superscripts: formula-aware OCR when available
   - tables: table recognition when available
   - mixed pages: layout parsing first, then route each region
   - question banks: preserve question number, stem, choices, answer, and explanation as separate fields
6. Run biomedical notation correction after recognition.
7. Assemble clean Markdown.
8. Run a quality check for suspicious flattened notation and mark uncertain regions.

## Bundled Resources

- Read `references/ocr-routing.md` when planning or modifying an OCR pipeline.
- Read `references/biomedical-notation.md` when correcting notation or reviewing suspicious output.
- Use `scripts/medical_corrector.py` for deterministic biomedical notation correction and warning generation.
- Use `scripts/test_medical_corrector.py` to smoke-test the correction rules.

## Output Rules

Preserve structure:

- headings and subheadings
- question numbers and choices
- source page numbers when available
- tables as Markdown or HTML
- formulas as LaTeX or readable Unicode notation
- figure placeholders when image content cannot be converted safely

For question banks, prefer:

```text
## 第 X 题
【题型】...
【题干】...
【选项】
A. ...
B. ...
【答案】...
【解析】...
```

If the source does not contain an answer or explanation, write `未在原文中识别到`. Do not invent missing content.

## Non-Negotiable Rules

- Never rely on plain OCR alone for formula-heavy or biomedical-notation-heavy pages.
- Never silently convert all numbers into subscripts.
- Never invent unreadable or missing text.
- Never merge multiple-choice options into the stem.
- Never flatten tables when table structure matters.
- Mark uncertain recognition explicitly, for example `[疑似：PaCO₂，需人工复核]`.
- Report remaining suspicious flattened notation after correction.

